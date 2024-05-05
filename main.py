# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from groc_adapter import GroqModelWrapper
from fastapi.middleware.cors import CORSMiddleware
import logging

model_wrapper = GroqModelWrapper()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    expose_headers=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str
  
@app.on_event("startup")
async def on_start_up():
    logging.info('Application started')

@app.post("/response")
async def message(message: Message):
    logging.info(message)
    response = model_wrapper.chat_with_model(message.message)
    return {"messages":  [response]}
