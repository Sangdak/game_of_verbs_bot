import json
import logging
from pathlib import Path
from pprint import pprint

from environs import Env

import dialogflow_api, telegram_bot_api


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
    intent_json = 'questions.json'
    adding_mode = False

    if adding_mode:
        create_intent_from_json(intent_json)

    telegram_bot_api.activate_tg_bot(tg_bot_token)


if __name__ == '__main__':
    main()
