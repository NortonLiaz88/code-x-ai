# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from chat import GPTModelWrapper
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

model_wrapper = GPTModelWrapper()
# broker = RabbitBroker("amqp://guest:guest@localhost:5673/")

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
    model_wrapper.initialize_chat_session()
    logging.info('Application started')

@app.post("/response")
async def message(message: Message):
    response =  model_wrapper.chat_with_model(message.message)
    return {"messages":  [response]}


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='192.168.0.168')