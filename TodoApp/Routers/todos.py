from fastapi import FastAPI, APIRouter # APIRouter will allow us to be able to route from our main.py file to our auth.py file

# app=FastAPI()               # This a new application , this is not the app in main.py
                              # We will have to use routing
router =APIRouter()