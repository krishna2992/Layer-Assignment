from .models import *
from .serializers import *
from django.db.models import F
from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view



@api_view(('GET', 'POST',))
def books(request):
    '''
        This view is called to get all books or to add a book to database

            On POST request uses request body to add a book using field name

            On GET request return all books or available books based on 
            url such  as
                'http(s)://<domain>:<port>/books/?is_avalilable=True' 
                returns books that are only avaliable



        usages:
            To POST one  book
            >>> import requests as r
            >>> data = {'book_id':<your_book_id>, 'borrower_id':<your_borrower_id>}
            >>> res = r.post('http(s)://<domain>:<port>/books/', json=data)
            >>> res.json()

            more than one book 
            >>> import requests as r
            >>> data = [{'name':'<your_book_name>'}, {}'name':<your_book_name_2>}, ...]
            >>> res = r.post('http(s)://<domain>:<port>/books/', json=data)
            >>> res.json()
        
        on success returns 201
        on error return error text as responce json
    '''
    if request.method == 'POST':
        data = request.data
        if not isinstance(data, list):
            data = [data]
        serializer = BookSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()  # This will create the books
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    books = Book.objects.all()
    if 'is_available' in request.GET:
        is_available = request.GET.get('is_available')
        is_available = True if is_available.lower() == 'true' else False
        books = books.filter(is_available=is_available)
    data = BookSerializer(books, many=True).data
    return Response(data, status=status.HTTP_200_OK)

    
@api_view(('POST',))
def borrow_book(request):
    '''
        This view is called to borrow a book
        It extracts 'book_id' and 'borrower_id' from request body
        and updates book status and borrower's books_borrowed

        usages:
            >>> import requests as r
            >>> data = {'book_id':<your_book_id>, 'borrower_id':<your_borrower_id>}
            >>> res = r.post('http(s)://<domain>:<port>/borrow/', json=data)
            >>> res.json()
        
        on success returns 201
        on error return error text as responce json
    '''
    
    book_id =  request.data.get('book_id', None)
    if not book_id:
        return Response('Must have book_id  inside request body', status=400)
    borrower_id = request.data.get('borrower_id', None)
    if not borrower_id:
        return Response('Must have borrower_id  inside request body', status=400)
    


    try:
        borrower = Borrower.objects.get(pk=borrower_id)
        if not borrower.is_active:
            return Response('Borrower is currently not active', status=400)
    except Borrower.DoesNotExist:
        return Response(f'Borrower with id {borrower_id} does not found', status=404)
    if borrower.books_borrowed >= 3:
        return Response('Maximum borrow limit reached', status=400)
    
    try:
        book = Book.objects.get(pk=book_id)
        if not book.is_available:
            return Response('Requested book is currently not avaliable', status=404)
    except Book.DoesNotExist:
        return Response('Book does not found', status=404)
    
    

    try:
        with transaction.atomic():
            book  = Book.objects.select_for_update().get(pk=book_id)
            loan = Loan(book=book, borrower=borrower)
            book.is_available = False
            borrower.books_borrowed = F('books_borrowed')+1
            loan.save()
            book.save()
            borrower.save()
    except Book.DoesNotExist:
        return Response('Requested book does not exist', status=404)
    
    data = BorrowSerializer(loan).data
    return Response(data, status=201)



@api_view(('POST',))
def return_book(request):
    '''
        This view is called to return a borrowed book
        It extracts 'book_id' from request body
        and updates book status

        usages:
            >>> import requests as r
            >>> data = {'book_id':<your_book_id>}
            >>> res = r.post('http(s)://<domain>:<port>/return/', json=data)
            >>> res.json()
        
        on success returns 202
        on error return error text as responce json
    '''
    book_id =  request.data.get('book_id', None)
    if not book_id:
        return Response('Must have book_id  inside request body', status=400)
    
    try:
        with transaction.atomic():
            book = Book.objects.select_for_update().get(pk=book_id)
            loan = Loan.objects.select_for_update().filter(
                book=book, is_retured=False).last()
            
            if not loan:
                raise Loan.DoesNotExist('Does not Exist')
            
            loan.is_retured = True
            loan.returned_on = timezone.now()
            book.is_available = True
            loan.borrower.books_borrowed = F('books_borrowed')-1
            loan.save()
            book.save()

    except Loan.DoesNotExist:
        return Response(f'No Record of Book id={book_id} ',status=400)
    
    except Book.DoesNotExist:
        return Response(f'Book id={book_id} does not exist',status=400)

    serializer = BorrowSerializer(loan).data
    return Response(serializer, status=status.HTTP_202_ACCEPTED)

@api_view(('GET',))
def get_active(request, borrower_id):
    '''
        This view is called to get all borrowed books
        by 'borrower_id'
        It takes 'borrwer_id' from encoded url
        

        usages:
            >>> import requests as r
            >>> res = r.get('http(s)://<domain>:<port>/borrowed/<borrower_id>/')
            >>> res.json()
        
        on success returns 200
        on error return error text as responce json
    '''
    try:
        borrower = Borrower.objects.get(pk=borrower_id)
    except Borrower.DoesNotExist:
        return Response(f'Requested borrower id={borrower_id} does not exist', status=404)
    
    loan = Loan.objects.filter(borrower=borrower, is_retured=False)
    serializer = ActiveBorrowSerializer(loan, many=True)
    return Response(serializer.data)



@api_view(('GET',))
def get_history(request, borrower_id):
    '''
        This view is called to get all borrowed books and as well returned books
        i.e. complete history off books borrowed by 'borrower_id'
        It takes 'borrwer_id' from encoded url
        

        usages:
            >>> import requests as r
            >>> res = r.get('http(s)://<domain>:<port>/history/<borrower_id>/')
            >>> res.json()
        
        on success returns 200
        on error return error text as responce json
    '''
    try:
        borrower = Borrower.objects.get(pk=borrower_id)
    except Borrower.DoesNotExist:
        return Response(f'Requested borrower id={borrower_id} does not exist', status=404)

    loan = Loan.objects.filter(borrower=borrower)
    serializer = BorrowSerializer(loan, many=True)
    return Response(serializer.data)    
