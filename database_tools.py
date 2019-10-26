class DatabaseEditor:
    def __init__(self):
        pass

    # INSERT a new row to the database
    def add_keyword(self, sticker_id, keyword):
        return "Keyword added succesfully. "

    # Get (SELECT) keys from the database for a sticker
    def get_keywords(self, sticker_id):
        pass

    # DELETE a row from the database
    def remove_keyword(self, sticker_id, keyword):
        return "Keyword removed succesfully. "

    # Execute selected action (add or remove)
    def perform_action(self, user_data):
        add = user_data.get("add")
        sticker = user_data.get("current_sticker")
        keyword = user_data.get("current_keyword")

        if type(add) is bool and type(sticker) is str and type(keyword) is str:
            if add:
                result = self.add_keyword(sticker, keyword)
            else:
                result = self.remove_keyword(sticker, keyword)
            return result
        else:
            error_message = "Data type error. Dictionary \"user_data\" contains information that is wrong type."
            return error_message



