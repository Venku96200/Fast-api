''''''
'''
# This is a main file where all the magic for this project is going to happen.
# This is going to be our root folder where we create our fastapi application

# Remember:- In our database.py file, we said we wanted our SQL alchemy database
URL to just create a SQLite database called todos.bd in the location of our TODO app
'''

from fastapi import FastAPI
import Models
from database import engine
app=FastAPI()

Models.Base.metadata.create_all (bind=engine) # Now if we start the server we will successfully create our database
                                              # Now we will install Sqlite to play around this db using query commands