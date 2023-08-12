from google.cloud import dialogflow


def detect_intent_texts(session_id, texts, project_id='testedproject-381406', language_code='ru-ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print(f'Session path: {session}', end='\n')

    for text in [texts,]:
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


def create_intent(display_name, training_phrases_parts, message_texts, project_id='testedproject-381406'):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
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
    pass
    # option =
    # texts = [message]
    # return detect_intent_texts(project_id, texts)


if __name__ == '__main__':
    main()
