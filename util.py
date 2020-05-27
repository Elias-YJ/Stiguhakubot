import os

super_admin = os.environ.get("SUPER_ADMIN")
token = os.environ.get("BOT_TOKEN")


def get_bot_token():
    return token


def is_user_permitted(user_id: int):
    if str(user_id) == super_admin:
        return True
    else:
        return False
