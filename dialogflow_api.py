import argparse
from environs import Env
import json
import logging
import os.path
from pathlib import Path

from google.cloud import dialogflow


logger = logging.getLogger(__name__)


def create_parser():
    parser = argparse.ArgumentParser(
        prog='interact_dialogflow_api',
        description='Script helps to interact with Google DialogFlow API.',
    )

    parser.add_argument(
        '-f',
        '--intent_from_file',
        help='Specify the path or URL of the json file from which to create new intent(s). ',
        type=Path,
    )
    return parser


def detect_intent_texts(session_id, text, project_id, language_code='ru-ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )

    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback


def create_intent_from_json(filepath, project_id):
    file = Path(filepath)
    with open(file, 'r', encoding='utf8') as f:
        intents = json.load(f)

    for title, value in intents.items():
        create_intent(title, value.get('questions'), value.get('answer'), project_id)


def create_intent(display_name, training_phrases_parts, message_texts, project_id):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[message_texts,])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )

    print(f'Intent created: {response}')


def main():
    env = Env()
    env.read_env(override=True)
    project_id = env.str('DIALOGFLOW_PROJECT_ID')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    parser = create_parser()
    args = parser.parse_args()

    if os.path.isfile(args.intent_from_file):
        print('File exists, start processing')
        create_intent_from_json(args.intent_from_file, project_id)
    else:
        print(
            f'ERROR: File {args.intent_from_file} not found,'
            'check path and filename.',
        )
        parser.print_help()


if __name__ == '__main__':
    main()
