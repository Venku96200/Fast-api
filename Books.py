from fastapi import FastAPI

app=FastAPI() # Here FastAPI() is a class and app is an object
              # This is to tell to Uvicorn that we are creating a new app
              #Uvicorn:- Is the web server we use to start a FastAPI application

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

