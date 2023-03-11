# https://github.com/acheong08/ChatGPT
"""
get accessToken from  https://chat.openai.com/api/auth/session:
from key=accessToken,other is useless!
"""

from revChatGPT.V1 import Chatbot
from helper.access_helper import chatgpt_token

chatbot = None
access_token = chatgpt_token()


def get_chatgpt_answer():
    global chatbot
    if chatbot is None:
        print("--------------------------------- create new chatgpt ---------------------------------")
        chatbot = Chatbot(config={"access_token": access_token})

    question = input(">> ")
    if question == 'exit':
        return

    prev_text = ""
    for data in chatbot.ask(question, ):
        message = data["message"][len(prev_text):]
        print(message, end="", flush=True)
        prev_text = data["message"]
    print("\n")

    get_chatgpt_answer()


if __name__ == '__main__':
    print('********************************* Chat GPT Init *********************************')
    get_chatgpt_answer()
