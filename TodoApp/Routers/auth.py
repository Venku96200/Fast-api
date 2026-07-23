''''''


'''
 Now we want to run all the apiendpoints on the same port, ie
 I should press unicorn main:app --reload only once to start
 the entire application should include all the APIEndpoints 
 event the once not in the main.py files, We will need routers
 for this task
 
 
 Hashing:-  (pip install paslib, pip install bcrypt==4.0.1)
 We convert the password into a Hash using bcrypt
 We then save that hashed password into our database
 This is done to provide security and getting hacked etc
 
 
 Authenticate a User:-
   Letting user authenticate himself to signin as a user in our database
   A token is what we are going to return back to the user, tha s going to have
   all the information about the user inside, this token is a JWT (JSON web token)
   
 Python-Multipart:-
      # python-multipart is a library that allows FastAPI to read HTML form data.
      # Normally, your API receives JSON:
                    {
                      "username": "venku",
                      "password": "abc123"
                    }
      # But HTML forms send data differently:
                        username=venku
                        password=abc123

      # FastAPI cannot parse this format by itself
      
      
FORMS:-
       # A form is simply a way for a user to send information to a server.
           ex:- a login page:
                When you click Login, the browser sends the values to the server.
       
             1) IN HTML:-       <form action="/login" method="post">
                                    <input name="username">
                                    <input name="password" type="password">
                                    <button>Login</button>
                                </form>
                                
             2) IN FASTAPI:-    from fastapi import Form
                                @app.post("/login")
                                async def login(
                                    username: str = Form(),
                                    password: str = Form()
                                ):
                                    return {"username": username}
                                    
                                    
JWT(Json Web Tokens) Overview    (CHECK NOTES)
   # JWT is a self-contained way to securely transmit data and information between two parties using a JSON Object               
   # JWT is one of the most popular bearer tokens and authorization protocols within API's.    
   # JWT is not an authentication method,    It is an authorization method which allows
     the client and server to maintain a relationship without having to login each request
   # JWT is a greate way for information to be exchanged between the server and client  
   # JWT can be trusted because each JWT can be digitally signed, which in return allows the server to know
   if the JWT has been changed at all
   
                                   LOGIN
                                     │
                                     ▼
                               Authentication
                                     │
                                     ▼
                                Generate JWT
                                     │
                                     ▼
                              Client stores JWT
                                     │
                                     ▼
                              Future API Requests
                                     │
                                     ▼
                              Authorization Check
                                     │
                                     ▼
                              Allow / Deny Access
                              
   We will have to install "python-jose[cryptography]" library to USE JWTs                           
'''





from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from fastapi import FastAPI, APIRouter,Depends  # APIRouter will allow us to be able to route from our main.py file to our auth.py file
from pydantic import BaseModel
from Models import Users
from passlib.context import CryptContext   # Used for encrypting the passwords
from fastapi.security import OAuth2PasswordRequestForm  # We should use this as a dependency injection gor our apiendpoints
from jose import jwt  # A JWT needs a secret and an algorithm
from datetime import timedelta, datetime, timezone
router =APIRouter()    # Instead of creating a new APP for the authorization endpoints, create a router and route in to main.py

# The Secret and algorithm will work together to add a signature to the JWT to make sure that JWT is secure and authorized
SECRET_KEY='randomshitSECREATIMGAY873897fe975639a50f1d73869f8f0d07155c8480fa'
ALGORITHM='HS256'



bcrypt_context=CryptContext(schemes=['bcrypt'], deprecated='auto')  # Inside our bcrypt_context algorithm we can now use bcrypt

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str


def get_db():
    db = SessionLocal()  # Runs first and creates a session
    try:
        yield db  # Gives the session too whoever asked ( endpoint1, endpoint2 etc any one)
    finally:  # When the request is finished we delete the session
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def create_access_token(username:str,user_id:int,expires_delta:timedelta):

    # The information that lives inside a JWT
    encode={'sub':username,'id':user_id}
    expires=datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)




@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency , create_user_request: CreateUserRequest):
    create_user_model=Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name = create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),   # Nobody knows the algorithm of hashing a password
        is_active=True                                                       # If somebody did then he will just unhash the password and get it
    )

    db.add(create_user_model)
    db.commit()

'''
1) This function takes in the Username, Password and the Database
2) Fetches the row of the username and store it in user
3) Check weather user is null(user doesnt exist) or not
4) If Entered password is equal to stored password return true else return false
'''
def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    else:
        return True

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db:db_dependency):
    user=authenticate_user(form_data.username,form_data.password, db)
    if not user:
        return "Failed Authentication"
    return "Successful Authentication"




