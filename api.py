from fastapi import FastAPI
from classifier import classify_intent
from router import route_and_respond
from pydantic import BaseModel
app=FastAPI()
class ChatRequest(BaseModel):
    message:str

@app.get('/')
def root():
    return{"message":"Hello! this is a python application :)"}

@app.post("/chat")
def chat(request:ChatRequest):
    message=request.message
    intent_data=classify_intent(message)
    response=route_and_respond(message,intent_data)
    return{
        "intent":intent_data.get("intent"),
        "confidence":intent_data.get("confidence"),
        "response":response
    }


