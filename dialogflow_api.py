from google.cloud import dialogflow


def detect_intent_texts(session_id, texts, project_id='testedproject-381406', language_code='ru-ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print(f'Session path: {session}', end='\n')

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={'session': session, 'query_input': query_input}
        )

        print('=' * 20)
        print(f'Query text: {response.query_result.query_text}')
        print(
            f'Detected intent: {response.query_result.intent.display_name} '
            f'(confidence: {response.query_result.intent_detection_confidence})',
            end='\n'
        )
        print(f'Fulfillment text: {response.query_result.fulfillment_text}', end='\n')
        return response.query_result.fulfillment_text


def main(project_id, message):
    texts = [message]
    return detect_intent_texts(project_id, texts)


if __name__ == '__main__':
    user_id = 'test_123456789'
    user_message = 'Привет!'
    main(user_id, user_message)
