import util
import logging
import telegram.ext
from telegram import ReplyKeyboardMarkup
from telegram.ext import (ConversationHandler, CommandHandler, MessageHandler, Filters)
from database_tools import DatabaseEditor

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

reply_keyboard = [['Add keyword', 'Remove keyword'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

CHOOSING, SELECTING_STICKER, SELECTING_KEYWORD = range(3)

db_editor = DatabaseEditor()


def start(update, context):
    user: telegram.User = update.message.from_user
    if util.is_user_permitted(user.id):
        logging.info(user.full_name + " started the bot. User has editing permission")
        update.message.reply_text("You have editing permissions. Use command /edit to "
                                  "add or remove keywords from the database")
    else:
        logging.info(user.full_name + " started the bot")
        update.message.reply_text("You do not have editing permission. "
                                  "This is where permitted users would edit the database")


def edit(update, context):
    user: telegram.User = update.message.from_user
    if util.is_user_permitted(user.id):
        update.message.reply_text("Please select what to do.", reply_markup=markup)
        return CHOOSING
    else:
        update.message.reply_text("You do not have editing permission.")


def add_keyword(update, context):
    update.message.reply_text("Adding a keyword. Send me a sticker that will be searched for.")
    context.user_data["add"] = True
    return SELECTING_STICKER


def remove_keyword(update, context):
    context.user_data["add"] = False
    update.message.reply_text("Removing a keyword. Send me a sticker from which you would like to remove a keyword.")
    return SELECTING_STICKER


def select_sticker(update, context):
    sticker: str = update.message.sticker.file_id
    context.user_data["current_sticker"] = sticker
    if context.user_data.get("add", True):
        update.message.reply_text("Sticker with ID:{} selected. Now type a keyword for the sticker".format(
                                sticker))
    else:
        update.message.reply_text("Sticker with ID:{} selected. Now type a keyword you would like to remove. "
                                  "The sticker currently has these keywords: "
                                  "{} ".format(sticker, db_editor.get_keywords(sticker)))
    return SELECTING_KEYWORD


def select_keyword(update, context):
    context.user_data["current_keyword"] = update.message.text
    result: str = db_editor.perform_action(context.user_data)
    logging.info(update.message.from_user.full_name + " performed an edit operation")
    update.message.reply_text("Selected keyword is \"{}\". {}"
                              "Choose next action or \"Done\" "
                              .format(update.message.text, result), reply_markup=markup)
    return CHOOSING


def done(update, context):
    context.user_data["current_sticker"] = ""
    context.user_data["current_keyword"] = ""
    update.message.reply_text("Interaction ended succesfully")
    return ConversationHandler.END


def main():
    updater = telegram.ext.Updater(util.get_bot_token(), use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("edit", edit)],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Add keyword)$'), add_keyword),
                       MessageHandler(Filters.regex('^(Remove keyword)$'), remove_keyword)],
            SELECTING_STICKER: [MessageHandler(Filters.sticker, select_sticker)],
            SELECTING_KEYWORD: [MessageHandler(Filters.text, select_keyword)]
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()
