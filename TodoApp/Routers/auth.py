''''''
from fastapi import FastAPI, APIRouter # APIRouter will allow us to be able to route from our main.py file to our auth.py file

# app=FastAPI()               # This a new application , this is not the app in main.py
                              # We will have to use routing
router =APIRouter()


@router.get("/auth/")
async def get_user():
    return {'user':'authenticated'}

'''
 Now we want to run all the apiendpoints on the same port, ie
 I should press unicorn main:app --reload only once to start
 the entire application should include all the APIEndpoints 
 event the once not in the main.py files, We will need routers
 for this task
 
 
'''
