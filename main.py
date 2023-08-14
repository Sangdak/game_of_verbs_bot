import json
import logging
from pathlib import Path
from pprint import pprint

import requests.exceptions
import urllib3.exceptions
from environs import Env

import dialogflow_api, tg_bot_api
import vk_bot_api

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def create_intent_from_json(filepath):
    file = Path(filepath)
    with open(file, 'r', encoding='utf8') as f:
        intents = json.load(f)

    for title, value in intents.items():
        dialogflow_api.create_intent(title, value.get('questions'), value.get('answer'))


def main():
    env = Env()
    env.read_env(override=True)

    tg_bot_token = env.str('TG_BOT_TOKEN')
    vk_group_token = env.str('VK_BOT_TOKEN')
    intent_json = 'questions.json'
    adding_mode = False

    if adding_mode:
        create_intent_from_json(intent_json)

    vk_bot_api.interaction_vk_bot(vk_group_token)
    tg_bot_api.interaction_tg_bot(tg_bot_token)


if __name__ == '__main__':
    main()
