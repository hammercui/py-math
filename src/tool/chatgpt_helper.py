# https://github.com/acheong08/ChatGPT
from core.base_class import Core
from common.lib.revchatgpt.V1 import Chatbot

chatbot = None


def get_chatgpt_answer(access_token):
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

    get_chatgpt_answer(access_token)


if __name__ == '__main__':
    env = "dev"
    core = Core()
    core.init(env=env)

    logger = core.logger
    config = core.config
    logger.info('********************************* Chat GPT Init *********************************')

    # https://chat.openai.com/api/auth/session
    access_token = ""
    get_chatgpt_answer(access_token)
