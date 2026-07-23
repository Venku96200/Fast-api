"""
We have already created the database.py file which has the location of where we want to store
our todos.db and now we will create a model which is going to be our table that we
want to be stored in or database
"""

"""
# Models is a way for SQlalchemy to be able to understand what kind of databasetables we are going to be creating within our database in the future
# Database model is going to be actual record that is inside a database table

"""
from database import Base  # We will use this to create a model for database.py file
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey  # Used to create columns and Integer,String,Boolean values in the table  ( Column and Integer,String,Boolean are Classes)

class Users(Base):
    __tablename__ ='users'
    id = Column(Integer, primary_key=True, index=True)
    email=Column(String, unique=True)
    username=Column(String, unique=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password=Column(String)
    is_active=Column(Boolean,default=True)
    role=Column(String)


class Todos(Base):
    __tablename__='todos' # A way for SqlAlchemy to know what to name this table inside our database later on
    id=Column(Integer, primary_key=True, index=True) # All the values in this column Should be integer and Unique, Index:- As we know that this column has unique values, we tell the database that it can do Indexing to find the result quickly
    title=Column(String)
    description= Column(String)
    priority=Column(Integer)
    complete=Column(Boolean, default=False)
    owner_id=Column(Integer, ForeignKey("users.id"))   # This is a foreign Key referencing id column from Users table