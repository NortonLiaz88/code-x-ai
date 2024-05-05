import os
import logging
from groq import Groq


class GroqModelWrapper:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

    def chat_with_model(self, message: str):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a python programming languages expert, transcribe the responses in Brazilian Portuguese.\nBe terse."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0,
            # Streaming is not supported in JSON mode
            stream=False,
            # Enable JSON mode by setting the response format
        )
        return chat_completion.choices[0].message.content


if __name__ == "__main__":
    model_wrapper = GroqModelWrapper()
    model_wrapper.main()