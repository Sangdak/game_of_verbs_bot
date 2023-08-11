import logging

from environs import Env

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_start_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def handle_help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def handle_echo_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main():
    env = Env()
    env.read_env(override=True)

    tg_bot_token = env.str('TG_BOT_TOKEN')

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handle_start_command))
    dispatcher.add_handler(CommandHandler("help", handle_help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_echo_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
