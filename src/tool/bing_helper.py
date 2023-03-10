# https://github.com/acheong08/EdgeGPT

import os
import asyncio
from EdgeGPT import Chatbot

chatbot = None


async def ask_bing():
    global chatbot
    if chatbot is None:
        print("--------------------------------- create new chatbot ---------------------------------")
        cur_file_path = os.path.dirname(os.path.realpath(__file__))
        chatbot = Chatbot(cookiePath=cur_file_path + '/cookie.json')

    while True:
        question = input(">> ")
        if question == 'exit':
            await chatbot.close()
            return

        prev_text = ""
        response = chatbot.ask_stream(prompt=question)
        async for data in response:
            if not data[0]:
                message = data[1][len(prev_text):]
                print(message, end="", flush=True)
                prev_text = data[1]
        print("\n")


def get_bing_answer():
    asyncio.run(ask_bing())


if __name__ == '__main__':
    get_bing_answer()
