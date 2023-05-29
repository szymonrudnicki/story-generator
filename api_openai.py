import openai

from config import OPENAI_API_KEY, OPENAI_MODEL


def set_api_key():
    openai.api_key = OPENAI_API_KEY


def create_completion(messages):
    set_api_key()
    completion = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages
    )

    return completion['choices'][0]['message']['content']