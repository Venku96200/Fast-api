from fastapi import FastAPI

app=FastAPI() # Here FastAPI() is a class and app is an object
              # This is to tell to uvicorn that we are creating a new app
              #uvicorn:- Is the web server we use to start a FastAPI application

@app.get("/api-endpoint")                  # A decorator which creates an API endpoint
async def first_api():                     # If someone does an HTTPS request of get("/api-endpoint") somewhere then they will be pointing here
    return {"message":"Hello Venkatesh!"}  # They will receive the response provided by the function just below the decorator

# To run the application we use ' uvicorn Books:app --reload ' in terminal
# We can also do ' fastapi run Books.py ' in terminal
# We can also do ' fastapi dev Books.py ' in terminal
# Press CTRL+C to stop the server


BOOKS=[
    {'title':'Title One', 'author': 'Author one', 'category':'science'},
    {'title':'Title Two', 'author': 'Author Two', 'category':'science'},
    {'title':'Title Three', 'author': 'Author Three', 'category':'history'},
    {'title':'Title Four', 'author': 'Author Four', 'category':'math'},
    {'title':'Title Five', 'author': 'Author Five', 'category':'math'},
    {'title':'Title Six', 'author': 'Author Two', 'category':'math'},
]


@app.get("/books")
async def read_all_books():
    return BOOKS

# -------- SWAGGER-------------------------
'''
    # Automatically implemented with fastapi
    1) Allows us to see all our api endpoints
    2) Able to call our api endpoints
    3) Able to see response of each API endpoint
    
    Just do:- http://127.0.0.1:8000/docs
'''


''' -------------------------------------------------------------------------------------
Path parameter:-  is a way for us to be able to locate in fastapi where we want an application to run and its just overall path of a URL

All the endpoints that we have discussed at the top have a STATIC PATH PARAMETER

If we want to access First/Second book from the dictionary, then its not 
recommended to create multiple api endpoints for each book, INSTEAD
we create an api endpoint with dynamic path
to add spaces in URl use %20

ORDER OF API_ENDPOINTS MATTERS WITH PARAMETERS
# All the endpoints with static parms should be at the top of the dynamic ones

I commented it out because it was causing ORDER problem

@app.get("/books/{dynamic_param}")        # If we provide a dynamic_param while get request,
async def try_out_dynamic_param(dynamic_param):  # We can pass that in the function and use it
    return {'dynamic_param':dynamic_param}
'''

@app.get("/books/{book_title}")
async def read_individual_books(book_title:str):  # Makes sure that the parameter is string
    for book in BOOKS:
        if book.get('title').casefold()==book_title.casefold():
            return book

'''
                                  
                                Query parameters
A way to filter data based on the URL provided  (filtering is done after a ?)                               
These are request parameters that have been attached after a "?"
Query Parameters have ' name=value ' pair
Ex:- 127.0.0.1:800/books/?category=math

'''

"""  ONLY QUERY PARAMETER """
@app.get('/books/')     # adding a '/' at the end automatically makes the parameter a query parameter
async def read_category_by_query(category:str):
    array=[]
    for book in BOOKS:
        if book.get('category')==category:
            array.append(book)
    return array

# if we run this http://127.0.0.1:8000/books/?category=science then all books with category as science are printed
# Or in SWAGGER just enter parameter science

"""  BOTH PATH AND QUERY PARAMETER """

@app.get('/books/{book_author}/')
async def read_both_path_and_query(book_author:str,category:str):
    array=[]
    for book in BOOKS:
        if book.get('category').casefold()==category.casefold() and book_author.casefold()==book.get('author').casefold():
            array.append(book)
    return array






