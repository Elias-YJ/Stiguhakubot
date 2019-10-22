import util
import telegram.ext


def start(update, context):
    user: telegram.User = update.message.from_user
    if util.is_user_permitted(user.id):
        update.message.reply_text("You have editing permissions.")
    else:
        update.message.reply_text("You do not have editing permission.")


def main():
    updater = telegram.ext.Updater(util.get_bot_token(), use_context=True)

    dp = updater.dispatcher

    dp.add_handler(telegram.ext.CommandHandler("start", start))

    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()
