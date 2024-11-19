from django.db import models

# Create your models here.
class Book(models.Model):
    ''' Book model for strong book in database '''

    name = models.CharField(max_length=50, unique=True)
    is_available = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name
    
class Borrower(models.Model):
    ''' Borrower model for our borrower '''

    name = models.CharField(max_length=50)
    books_borrowed = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Loan(models.Model):
    ''' This class to keep track of book and its borrower and borrowed status
        Acts as a history and active transaction keeper for our application

        book :  Foreign Key Relation to Book
        borrower : Foreign Key Constraint to Borrower
        borrowed_on: DateTimeField to keep track of borrowed date
        is_returned: Boolean to see if Book is returned by Borrower
        returned_on = DateTimeField to  record return date
    '''

    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey(Borrower, on_delete=models.SET_NULL, null=True)
    borrowed_on = models.DateTimeField(auto_now_add=True)
    is_retured = models.BooleanField(default=False)
    returned_on = models.DateTimeField(null=True)

    
    