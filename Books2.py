"""
   # Pydantic is a Python library that validates, parses, and serializes data using Python type hints.
   # It's especially popular for building APIs, reading configuration files, and handling JSON data safely.

   # Data Validation, Exceptional Handling , Status Code, Swagger Configuration, Python Request Object
   # Exceptions, status code, dealing with python objects and dealing with validation of request objects

   # After we reload the webserver the changes we made through CRUD gets reset
     We haven't yet started DATABASES
"""
from typing import Optional
from fastapi import HTTPException                # HTTP exception is something that we have to raise within our method, which will cancel the functionality of our Method and return a message in a status code back to our user
from fastapi import FastAPI, Body, Path, Query   # Path and Query are there for Data Validation of the Input through Path Parameters and Query Parameters
from pydantic import BaseModel, Field            # We will use BaseModel to validate the variables in object
                                                 # Field is used to add validation to each Field(Key) of the request object
from starlette import status       # When a api-endpoint successfully responses, we should provide specific STATUS_CODES
class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int

    def __init__(self,id,title,author,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating


app=FastAPI()
BOOKS=[
    Book(1,'Computer science PRO','codingwithroby','A very nice book!', 5),
    Book(2,'Be Fast with FastAPI','codingwithroby','A great book!', 5),
    Book(3,'Master Endpoints','codingwithroby','A awesome book!', 5),
    Book(4,'HP1','Author 1','Book Description', 2),
    Book(5,'HP2','Author 2','Book Description', 3),
    Book(6,'HP3','Author 3','Book Description', 1),
]

@app.get("/books" , status_code=status.HTTP_200_OK) # Here we are using the status object from starlette library to print the SPECIFIC SUCCESSFUL CODE  // WE WILL ADD THIS TO ALL THE API-ENDPOINTS
async def read_all_books_man():
    return BOOKS


@app.post("/create-book", status_code=status.HTTP_200_OK)
def add_book(new_book=Body()): # Rem:- the new_book is a dictionary but the items in BOOKS list are objects of Book object
    BOOKS.append(new_book)     # We can still append it in BOOKS because ,It is fine, lists can store anything
                               # but FastAPI will convert all the items into JSON , IRRESPECTIVE of there type

'''
Why do we need validation:--(Making sure that our Data is correct before creating it/ updating it)
1) post:- we need to make sure that we dont create a wrong data ( Ex:- creating a book with -500 rating points/ creating a nude book  etc)

We will use Pydantics to implement Data Validation, Data handling, Data parsing, Efficient error Handling
 1) Insted of Body() we will use BaseModel to get somemore features
  Ex:- Field():- Used for data validation of the data that is coming in
'''

class BookRequest1(BaseModel):  # DESCRIPTION OF WHAT A VALID BOOKS SHOULD LOOK LIKE
    id:int
    title:str
    author:str
    description:str
    rating:int

@app.post("/create-book-pydantic-noField" , status_code=status.HTTP_200_OK)
async def create_books(book_request: BookRequest1):    # The parameter book_request must be a object of BookRequest1
    new_book=Book(**book_request.model_dump())
    BOOKS.append(new_book)

"""
User
 │ sends JSON in Swagger
 ▼
FastAPI
 │ reads the JSON and validates it using BookRequest
 ▼
BookRequest object (NOT a dictionary)
 │
 ▼
Your function receives this object as 'book_request'

Since BOOKS currently stores Book objects,
we create a Book() object from the BookRequest().

First, convert the BookRequest object to a dictionary:
book_request.model_dump()    OBJECT ----.model_dump()------>DICTIONARY

This returns:
{
    "id": ...,
    "title": ...,
    "author": ...,
    "description": ...,
    "rating": ...
}

Now create a Book object using dictionary unpacking:

new_book = Book(**book_request.model_dump())

The ** operator unpacks the dictionary into keyword arguments.

It is equivalent to:

Book(
    id=data["id"],
    title=data["title"],
    author=data["author"],
    description=data["description"],
    rating=data["rating"]
)

Finally,

BOOKS.append(new_book)

adds the Book object to the list.
"""



class BookRequest2(BaseModel):         # Instead of just checking the datatype validation ,We will also do some specific validations using FIELD
    id:Optional[int]=None              # The author sometimes doesn't know what is th id of the previous book, so me may not know the id, hence he can leave it Empty(NONE) or Enter and Int
    title:str=Field(min_length=3)      # User cannot input a JSON with len(title) shorted than 3 characters
    author:str=Field(min_length=1)     # author name should be greater than 1 character
    description:str= Field(min_length=1,max_length=100)  # Description should lie btw 1 to 100 characters
    rating:int=Field(gt=-1,lt=6)        # The rating Should be greater than -1 but less than 6

@app.post("/create-book-pydantic-withField" , status_code=status.HTTP_200_OK)
async def create_books(book_request: BookRequest2):    # The parameter book_request must be a object of BookRequest
    new_book=Book(**book_request.model_dump())
    find_book_id(new_book)   # Overwriting the new_book.id with the valid id
    BOOKS.append(new_book)

# NTG SPECIAL JUST A FUNCTION TO MAKE SURE THAT ID's OF BOOK ARE UNIQUE
def find_book_id(book:Book):
    book.id=1 if len(BOOKS)==0 else BOOKS[-1].id+1
                #   same as top
                # if len(BOOKS)>0:
                #     book.id=BOOKS[-1].id+1
                #else:
                #     book.id=1
    return book
    

""" BASIC IDEA:-
   We are making sure that USERS input JSON is Valid
   before appending/adding it to our database
"""


class BookRequest3(BaseModel):
    id:Optional[int]=Field(description='ID is not needed on create', default=None) # Compare this line to " age:int=20" don't worry about description parameter it will not affect the code
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str= Field(min_length=1,max_length=100)
    rating:int=Field(gt=-1,lt=6)

    model_config={               # This to change the default example that is displayed in the SWAGGER
        "json_schema_extra":{
            "example":{                    # We haven't included the id as it isn't required we have a function to get it, ut still if we want to add we can add
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5
            }
        }
    }

@app.post("/create-book-pydantic-optional-Model-cofig" , status_code=status.HTTP_201_CREATED) # Used 201 as we didn't return anything but CREATED
async def create_books(book_request: BookRequest3):    # The parameter book_request must be a object of BookRequest
    new_book=Book(**book_request.model_dump())
    find_book_id(new_book)   # Overwriting the new_book.id with the valid id
    BOOKS.append(new_book)



# Fetching Book based on its ID ( WE will use query parameters just to Learn Data validation on Query parameters)
@app.get("/books/" , status_code=status.HTTP_200_OK)
async def fetch_book_based_on_id(book_id:int=Query(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404,detail='Item not found')    # If the input passed by the suer passes the Query parameter Validation and other validation, but doesnt exist/return anything we can raise an error
    # Top line, if any book_id doesn't exist, it will create a ERROR

# Using PUT request method to update the books

@app.put("/books/update_book" , status_code=status.HTTP_204_NO_CONTENT) # Any there is no response or Ntg created Just update we will return 204 status code
async def update_book(book:BookRequest3):
    Book_change=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            Book_change=True
            BOOKS[i]=book
    if not Book_change:
        raise HTTPException(status_code=404,detail='Item not found')

@app.delete("/books/delete/{book_id}")
async def delete_book(book_id:int= Path(gt=0)):   # We can also do data validation here the API-endpoint gets in the Input(book_id) we then check its validaty before sending it into the function as parameter
    Book_removed = False
    for book in BOOKS:                              # Hence this is known as extra Validation to PATH PARAMETERS
        if book.id==book_id:
            BOOKS.remove(book)
            Book_removed = True
            break
    if not Book_removed:
        raise HTTPException(status_code=404,detail='Item not found')


"""                   HTTP EXCEPTION
HTTP exception is something that we have to raise within our method, 
which will cancel the functionality of our Method and return a message 
in a status code back to our user

"""



