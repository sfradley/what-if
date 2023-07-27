import openai
import os


class ChatAgent:

    def __init__(self) -> None:
        openai.api_key = os.getenv('openai_token')
        self.model = "gpt-3.5-turbo"

    def beseech(self, messages, max_tokens=None):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens
            )
            return response
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    openai.api_key = os.getenv('openai_token')

    agent = ChatAgent()

    conversation = [
        {"role": "system", "content": "You are an unhelpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won " +
                                         "the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
    response = agent.beseech(conversation)
    print("Assistant:", response)
