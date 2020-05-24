def get_bot_token():
    with open('token.txt', 'r') as token_file:
        token = token_file.readlines()[0].strip(" \n")
    return token


def is_user_permitted(user_id: int):
    with open('permissions.txt', 'r') as permissions:
        if str(user_id) in permissions.read():
            return True
        else:
            return False
