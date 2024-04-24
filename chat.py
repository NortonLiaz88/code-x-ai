import logging
from gpt4all import GPT4All

class GPTModelWrapper:
    def __init__(self, model_name="replit-code-v1_5-3b-newbpe-q4_0.gguf", model_path='./', allow_download=False):
        logging.basicConfig(level=logging.INFO)
        self.model = GPT4All(model_name, model_path, allow_download=allow_download)
        self.chat_session_initialized = False
        self.initialize_chat_session()

    def initialize_chat_session(self):
        if not self.chat_session_initialized:
            self.model.chat_session('You are a python programming languages expert, transcribe the responses in Brazilian Portuguese.\nBe terse.',
                                    '### Instruction:\n{0}\n### Response:\n')
            self.chat_session_initialized = True

    def chat_with_model(self, message):
        if not self.chat_session_initialized:
            self.initialize_chat_session()
        response = self.model.generate(message, temp=0)
        return response
    def main(self):
        self.chat_with_model()

if __name__ == "__main__":
    model_wrapper = GPTModelWrapper('replit-code-v1_5-3b-newbpe-q4_0.gguf')
    model_wrapper.main()