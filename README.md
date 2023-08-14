# "Game of Verbs" support bot

The bot is designed to help support staff in Telegram and VK. 
It answers users' messages with common questions. 
Recognition mechanism is implemented with the help of Google DialogFlow tool integration.

## How to install

- Python 3.11 and poetry must be pre-installed on the system.
- Copy the repository: shell git clone <repository link>. 
- Install all dependencies: 
```shell 
poetry shell 
poetry install 
```
## How to run

In the project directory, create an '.env' file with the following contents:
```
TG_BOT_TOKEN - Telegram bot token
DIALOG_FLOW_PROJECT_ID - Google DialogFlow project id
GOOGLE_APPLICATION_CREDENTIALS - Path to google cloud credentials json file
VK_BOT_TOKEN - VK community token
```

## Launch bots

```shell
python tg_bot_api.py
python vk_bot_api_py
```

## CLI for training Google DialogFlow Agent from a json file

Structure of a json file:
```json
{
  "Устройство на работу": {
    "questions": [
      "Как устроиться к вам на работу?",
      "Как устроиться к вам?",
      "Как работать у вас?",
      "Хочу работать у вас",
      "Возможно-ли устроиться к вам?",
      "Можно-ли мне поработать у вас?",
      "Хочу работать редактором у вас"
    ],
    "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
  },
  ...
}
```
### Training start command

```shell
python dialogflow_api.py --intent_from_file <path/to/file.json>
```

Example interaction with bot:
[example interaction](https://github.com/Sangdak/game_of_verbs_bot/blob/master/readme.gif)



## Project Goals 
This code is written for educational purposes - it is a lesson in a course on Python 
and web development from [Devman](https://dvmn.org)
