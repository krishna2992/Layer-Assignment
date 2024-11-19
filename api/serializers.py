from rest_framework import serializers
from .models import Book, Loan, Borrower

class BookSerializer(serializers.ModelSerializer):
    '''Book serialization class to serialize Book instance '''
    class Meta:
        model = Book
        fields = '__all__'

class BorrowSerializer(serializers.ModelSerializer):
    '''Loan serialization class to serialize Loan instance '''
    class Meta:
        model = Loan
        fields = '__all__'

class BorrowerSerializer(serializers.ModelSerializer):
    '''Borrower serialization class to serialize Borrower instance '''
    class Meta:
        model = Borrower
        fields = '__all__'



class ActiveBorrowSerializer(serializers.ModelSerializer):
    ''' Loan serialization class to serialize Loan instance 
        but only following fields are included
        ['id', 'book', 'borrower', 'borrowed_on',]
    '''
    class Meta:
        model = Loan
        fields = ['id', 'book', 'borrower', 'borrowed_on',]