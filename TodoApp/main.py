''''''
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from Routers import auth

'''
# This is a main file where all the magic for this project is going to happen.
# This is going to be our root folder where we create our fastapi application

# Remember:- In our database.py file, we said we wanted our SQL alchemy database
URL to just create a SQLite database called todos.bd in the location of our TODO app
'''

from fastapi import FastAPI, Depends, HTTPException, Path
import Models
from Models import Todos
from database import engine, SessionLocal
app=FastAPI()

Models.Base.metadata.create_all (bind=engine) # Now if we start the server we will successfully create our database
                                              # Only runs if there is no DB
                                              # Alembic Section of course will teach how to enhance DB without deleting each time
                                              # Now we will install Sqlite to play around this db using query commands

app.include_router(auth.router)  # We are conecting the auth.py to main.py through router
                                 # We are including all the APIEndpoints from auth.py files here




'''                              
    Enter 'sqlite3 todos.db' in terminal to activate sqlite3
    # .schema :- Shows all the tables in our db currently
    # adding Todo:- insert into todos (title,description,priority,complete) values ('Go to the store','Pick up eggs', 5, False);
    # Viewing the entries:- select * from todos; :- We can do .mode to change the viewing of the tables. Ex:- .mode markdown, .mode column etc
    # Delete the todo:- delete * from todos where id=4
    
    After doing all this we will create APIendpoints to fetch and get all the 
    data from this database
'''

# Creating DB dependencies
# "Why not make one function that creates and closes the session?"

def get_db():
    db=SessionLocal() # Runs first and creates a session
    try:
        yield db       # Gives the session too whoever asked ( endpoint1, endpoint2 etc any one)
    finally:           # When the request is finished we delete the session
        db.close()

"""
DB Dependencies summary:- 
for Each request, We can now call SessionLocal() to create
a Connection(session) , then we will use that connection and finally
delete the connection.

Depends:- (Dependency Injection)

Dependency injection really just means that we need to do something
before we exectue what we are trying to execute

                    Request arrives
                          │
                          ▼
                    Run get_db()
                          │
                    Create SessionLocal()
                          │
                    yield db
                          │
                    Give db to endpoint
                          │
                    Endpoint finishes
                          │
                    finally runs
                          │
                    db.close()


#  db:Annotated[Session, Depends(get_db)]  this line simply means:-
       ***db is a Session, obtained using Depends(get_db)***
"""

db_dependency= Annotated[Session,Depends(get_db)]

# Getting pydantic for data validation and etc
class TodoRequest(BaseModel):
    title:str=Field(min_length=3)
    description:str= Field(min_length=3, max_length=100)
    priority:int=Field(gt=0,lt=6)
    complete:bool
# We don't have to create a function to get id, like we did in Books2.py. Sqlalchemy will automatically assign id to each todoz as id is primary key(cannot be null)

# 1st APIEndpoint:- To get all todos
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency ):
    return db.query(Todos).all()


# 2nd APIEndpoint:- To get ttodo based on id
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db:db_dependency, todo_id:int=Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()   # We added .first() to return the first value, and not iterate throught the table, as id is a primary key
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')

# 3rd APIEndpoint:- To Create a ttodo in the database
@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency,todo_request: TodoRequest):
    todo_model=Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()

# 4th APIEndpoint:- To update a ttodo in the database
@app.put("/todo/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,
                      todo_request:TodoRequest,
                      todo_id:int=Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete
    db.add(todo_model)
    db.commit()

# 5th APIEndpoint:- To update a ttodo in the database
@app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency, todo_id:int=Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
