'''
'''
'''
# Before SQLAlchemy
# Earlier, your books were stored like this:
                                        BOOKS = [
                                            {"id": 1, "title": "Python"},
                                            {"id": 2, "title": "FastAPI"}
                                        ]
# Everything was stored in RAM.
# When you stopped the server:
        Ctrl + C
# everything disappeared.
# That's obviously not practical.


# We need permanent storage
# Instead of RAM, we want
   FastAPI
      │
      ▼
   Database
# A database remembers everything even after the program stops.
-------------------------------------------------------------------------------------
#                SQLite
# SQLite is the simplest database.
# Unlike MySQL or PostgreSQL, it doesn't run as a separate server.
# It is literally just one file.
-----------------------------------------------------------------------------------------
#                But can Python directly talk to SQLite?
# Technically yes.
# Python has a module:
# import sqlite3
# You could write
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute(
    INSERT INTO todos(title)
      VALUES('Study FastAPI')
    )
# This works...
# But imagine writing SQL strings everywhere.
# Very messy.
--------------------------------------------------------------------------------
                     Enters SQLAlchemy
SQLAlchemy is an ORM.
ORM means :- Object Relational Mapper
Instead of writing SQL manually...
You write Python objects.

Instead of
                 INSERT INTO todos ...   (SQL CODE)
you simply write
                 todo = Todo(title="Study")
                 session.add(todo)
                 session.commit()
                 
SQLAlchemy secretly converts it into SQL.
Think of SQLAlchemy as a translator.   

        You
         │
         ▼
        Python objects
         │
         ▼
        SQLAlchemy
         │
         ▼
        SQL Queries
         │
         ▼
        SQLite       

-------------------------------------------------------------------------------
                        ENGINE
# Database engine is something that we can use to open up a connection and be able to use our database
# Connect Arguments:- are arguments that we can pass into our create engine, which will allow
                      us to be able to define some kind of connection to a database
                                        or
                      connect_args is simply a dictionary of extra settings that SQLAlchemy 
                      passes to the SQLite driver when connecting to the database.  
                      

----------------------------------------------------------------------------------------------------------------------              
# SQLite's Safety rule:-  The thread that opens the database connection must be the same thread that uses it.
      
                   #     What is a thread?
# A thread is like a worker inside your program.
# Suppose your FastAPI server receives two requests at the same time:
                        User 1 ----> FastAPI
                                         │
                                     Thread 1
                        
                        User 2 ----> FastAPI
                                         │
                                     Thread 2
# FastAPI may use different threads to handle different requests.

# 'check_same_thread':False   :- #  "It's okay if a different thread uses this database connection."
                                 # This connect argument disables the Safety Rule of SQlite

---------------------------------------------------------------------------------
                               SESSIONS
 # Think of a Session as your conversation with the database.    
 
 # Suppose you want to:
    Insert a row
    Update a row
    Delete a row
    Read some rows

# You need someone to communicate with the database.
# That someone is the Session.                          
            Your Python Code
                   │
                   ▼
               Session
                   │
                   ▼
                Engine
                   │
                   ▼
               SQLite Database
# Each HTTP request gets its own Session.        
-----------------------------------------------------------------------------------
                             SESSIONMAKER    
 1) SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
                    # The sessionmaker() function runs.
                    # It returns a session factory (stored in SessionLocal (SessionLocal=A callable object of sessionMaker() class)).
  ################### SessionLocal is not a class, but a callable object. Calling it returns a Session  
                    # It is a callable Object:-   Rough Example:-
                                    class sessionmaker:
                                        def __init__(self, bind):
                                            self.bind = bind
                                        def __call__(self):
                                            return Session(bind=self.bind)
                                            
                                    SessionLocal = sessionmaker(bind=engine)   # you create a sessionmaker object.
                                    
                                    db = SessionLocal() # Python sees the parentheses and actually does (db = SessionLocal.__call__()) which returns a new Session.                                     
---------------------------------------------------------------------------------                               
# This file is going to be used for us to be able to create
  our URL string which will connect our fastApi application to our new database
# We will use SQL Lite

# SQLAlchemy is an ORM(Object Relational Mapping), Our fastapi application is
  going to use this to be able to create a database and be able to create a connection to a database.
  and be able to use all the database records within our application

'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  # sessionmaker is a class (technically, a callable factory class in SQLAlchemy).
from sqlalchemy.ext.declarative import declarative_base # Used to create a Database object, We can interact with it later on
SQLALCHEMY_DATABASE_URL='sqlite:///./todos.db'   # Create a location for our database in our application

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base() # We should be able to call our database.py file and
                        # be able to create a base which is an object(BASE) of the database
                        # which is going to be able to then control our database
                        # We will be able to create tables , this object BASE will help us
                        # interact with the tables we create