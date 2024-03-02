# main.py
from fastapi import FastAPI
from chat import GPTModelWrapper
# from propan import PropanApp, RabbitBroker
import json
import logging
import aio_pika



model_wrapper = GPTModelWrapper()
# broker = RabbitBroker("amqp://guest:guest@localhost:5673/")

app = FastAPI()


# @broker.handle(queue="application")
# async def base_handler(body):
#     logging.info(body)
#     # Mensagem recebida do RabbitMQ em bytes
#     message_bytes = b'{"pattern":"create-message","data":{"message":"Voce poderia me ajudar? Eu nao sei criar uma classe em Python"}}'

#     # Decodifica os bytes para uma string
#     message_str = message_bytes.decode('utf-8')

#     # Converte a string JSON para um objeto Python
#     message_json = json.loads(message_str)

#     print(message_json)

#     print(f"This is the queue result :: {body}")
#     response = model_wrapper.chat_with_model(message_json['data']['message'])
#     # return "ok"

#     # return str(response)


# @app.on_startup
# async def on_start_up():
#      # Starts the broker 
#     await broker.start()
#     model_wrapper.initialize_chat_session()


# @app.after_shutdown
# async def shutdown():
#     await broker.close()


@app.on_event("shutdown")
async def shutdown():
    await broker.close()


@app.on_event("startup")
async def on_start_up():

    model_wrapper.initialize_chat_session()
     # Starts the broker 
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost:5673/")
    queue_name = "application1"

    logging.info('Application started')

    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10)
        callback_queue = await channel.declare_queue(exclusive=True)
        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)
                    logging.info(message.body)
                    # Mensagem recebida do RabbitMQ em bytes
                    message_bytes = b'{"pattern":"create-message","data":{"message":"Voce poderia me ajudar? Eu nao sei criar uma classe em Python"}}'

                    # Decodifica os bytes para uma string
                    message_str = message_bytes.decode('utf-8')

                    # Converte a string JSON para um objeto Python
                    message_json = json.loads(message_str)

                    print(message_json)

                    print(f"This is the queue result :: {message_json}")
                    response = model_wrapper.chat_with_model(message_json['data']['message'])

                    await channel.default_exchange.publish(
                        aio_pika.Message(json.dumps(response).encode()),
                        routing_key=message.reply_to,
                        correlation_id=message.correlation_id
                    )
                    # await channel.default_exchange.publish(
                    #     aio_pika.Message(json.dumps(response).encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT), routing_key='create-message'
                    # )

                    # await channel.default_exchange.publish(
                    #     aio_pika.Message(
                    #         json.dumps(response).encode(),
                    #         reply_to=callback_queue.name
                    #     ),
                    #     routing_key='rpc_queue'
                    # )
                    logging.info("Response sent to RabbitMQ")
                    # return "ok"
                   
                       

   
#     # return str(response)


@app.post("/")
async def message(message: str):
    response = model_wrapper.chat_with_model(message)
    return {"message": response}