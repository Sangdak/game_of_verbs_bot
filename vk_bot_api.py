import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from environs import Env

import requests

import dialogflow_api


def get_message(vk_session):
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)

            # else:
            #     print('От меня для: ', event.user_id)
            # print('Текст:', event.text)

        return event.user_id, event.text


def send_message(event, vk_api_session, message_text):
    vk_api_session.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=message_text,
    )

def echo(event, vk_api_session):
    vk_api_session.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=get_random_id()
    )


def main():
    env = Env()
    env.read_env(override=True)

    tg_group_token = env.str('VK_BOT_TOKEN')
    vk_session = vk_api.VkApi(token=tg_group_token)

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            vk_api_session = vk_session.get_api()
            message = dialogflow_api.detect_intent_texts(event.user_id, event.text)
            send_message(event, vk_api_session, message)
            # echo(event, vk_api_session)


if __name__ == '__main__':
    main()
