''''''
# We USED ALL THIS CODE BEFORE INTORDUCING ROUTING
'''
# This is a main file where all the magic for this project is going to happen.
# This is going to be our root folder where we create our fastapi application

# Remember:- In our database.py file, we said we wanted our SQL alchemy database
URL to just create a SQLite database called todos.bd in the location of our TODO app
'''
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from fastapi import FastAPI
import Models
from database import engine
from Routers import auth,todos
app=FastAPI()

Models.Base.metadata.create_all (bind=engine) # Now if we start the server we will successfully create our database
                                              # Only runs if there is no DB
                                              # Alembic Section of course will teach how to enhance DB without deleting each time
                                              # Now we will install Sqlite to play around this db using query commands

app.include_router(auth.router)  # We are conecting the auth.py to main.py through router
                                 # We are including all the APIEndpoints from auth.py files here

app.include_router(todos.Router) # We are also connecting the todos.py to main.py through router
                                 # We are including all the APIEndpoints from todos.py files here




