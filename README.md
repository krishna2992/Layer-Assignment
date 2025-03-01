
# Installation

Follow these steps to install and set up the project locally:
1. Clone the Repository

First, clone the repository to your local machine.
```
    git clone https://github.com/your-username/Layer-Assignment.git
    cd Layer-Assignment
```
2. Create a Python Virtual Environment

It's a good practice to use a virtual environment to isolate your dependencies.
```
    python -m venv venv
```
3. Activate the Virtual Environment

   On Linux:

        source venv/bin/activate

    On macOS/Linux:

        source venv/bin/activate

    On Windows:

        venv\Scripts\activate

5. Install Dependencies

Install the required Python dependencies using pip.
```
    pip install -r requirements.txt
```

# Setup

1. Create Database Migrations

```
    python manage.py makemigrations
```

2. Apply Database Migrations

```
    python manage.py migrate
```

# Supported APIS

### Book (list or add to database)

        This API is called to get all books or to add a book to database

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

### Borrow a Book

        This API is called to borrow a book
        It extracts 'book_id' and 'borrower_id' from request body
        and updates book status and borrower's books_borrowed

        usages:
            >>> import requests as r
            >>> data = {'book_id':<your_book_id>, 'borrower_id':<your_borrower_id>}
            >>> res = r.post('http(s)://<domain>:<port>/borrow/', json=data)
            >>> res.json()
        
        on success returns 201
        on error return error text as responce json

### Return a borrowed book


        This API is called to return a borrowed book
        It extracts 'book_id' from request body
        and updates book status

        usages:
            >>> import requests as r
            >>> data = {'book_id':<your_book_id>}
            >>> res = r.post('http(s)://<domain>:<port>/return/', json=data)
            >>> res.json()
        
        on success returns 202
        on error return error text as responce json

### User Borrowed Books

        This view is called to get all borrowed books or currently borrowed
        by 'borrower_id'
        It takes 'borrwer_id' from encoded url
        

        usages:
            to get currently borrowed books by a user
            >>> import requests as r
            >>> res = r.get('http(s)://<domain>:<port>/borrowed/<borrower_id>/')
            >>> res.json()

            to get user borrowing  history
            >>> import requests as r
            >>> res = r.get('http(s)://<domain>:<port>/history/<borrower_id>/')
            >>> res.json()
        
        on success returns 200
        on error return error text as responce json
