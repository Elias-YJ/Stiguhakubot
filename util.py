def get_bot_token():
    text = open('token.txt', 'r')
    token = text.readlines()[0]
    token = token.strip(" \n")
    text.close()
    return token


def is_user_permitted(user_id: int):
    with open('permissions.txt', 'r') as permissions:
        if str(user_id) in permissions.read():
            return True
        else:
            return False
