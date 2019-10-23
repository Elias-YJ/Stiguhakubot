import util
import logging
import telegram.ext
from telegram import ReplyKeyboardMarkup
from telegram.ext import (ConversationHandler, CommandHandler, MessageHandler, Filters)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['Add search term', 'Remove search term'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

CHOOSING, SELECTING_STICKER, SELECTING_SEARCH_TERM = range(3)


def start(update, context):
    user: telegram.User = update.message.from_user
    if util.is_user_permitted(user.id):
        update.message.reply_text("You have editing permissions.")
    else:
        update.message.reply_text("You do not have editing permission.")


def edit(update, context):
    update.message.reply_text("Please select what to do.", reply_markup=markup)
    return CHOOSING


def add_search_term(update, context):
    update.message.reply_text("Adding a search term. Send me a sticker.")
    return SELECTING_STICKER


def remove_search_term(update, context):
    update.message.reply_text("Removing a search term. Send me a sticker.")
    return SELECTING_STICKER


def select_sticker(update, context):
    update.message.reply_text("Sticker selected (ID:{}). Now choose a keyword for the sticker.".format(
                                update.message.sticker.file_id))
    return SELECTING_SEARCH_TERM


def select_search_term(update, context):
    update.message.reply_text("Complete! Selected keyword is {}. " \
                              "Choose next action or \"Done\" ".format(update.message.text))
    return CHOOSING


def done(update, context):
    update.message.reply_text("Interaction ended.")
    return ConversationHandler.END


def main():
    updater = telegram.ext.Updater(util.get_bot_token(), use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("edit", edit)],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Add search term)$'), add_search_term),
                       MessageHandler(Filters.regex('^(Remove search term)$'), remove_search_term)],
            SELECTING_STICKER: [MessageHandler(Filters.sticker, select_sticker)],
            SELECTING_SEARCH_TERM: [MessageHandler(Filters.text, select_search_term)]
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]


    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()
