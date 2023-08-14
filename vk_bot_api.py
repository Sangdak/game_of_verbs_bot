import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from environs import Env

import dialogflow_api


def send_message(event, vk_api_session, message_text):
    vk_api_session.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=message_text,
    )


def main():
    env = Env()
    env.read_env(override=True)
    vk_group_token = env.str('VK_BOT_TOKEN')

    vk_session = vk_api.VkApi(token=vk_group_token)

    while True:
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                vk_api_session = vk_session.get_api()
                message, is_fallback = dialogflow_api.detect_intent_texts(event.user_id, event.text)
                if not is_fallback:
                    send_message(event, vk_api_session, message)


if __name__ == '__main__':
    main()
