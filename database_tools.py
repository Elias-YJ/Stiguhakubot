import sqlite3


class DatabaseEditor:
    def __init__(self, database):
        self.database = database

    # INSERT a new row to the database
    def add_keyword(self, sticker_id, keyword):
        data = (sticker_id, keyword.lower())
        try:
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
            c.execute('''INSERT INTO Stickers
                    VALUES (?,?);''', data)
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            conn.close()
            return "The sticker already has that keyword. Please choose another sticker or keyword."
        except sqlite3.DatabaseError:
            return "Connection to the database is not availble. Please try again later."
        return "Keyword added succesfully. "

    # Get (SELECT) keys from the database for a sticker
    def get_keywords(self, sticker_id):
        sticker_id = (sticker_id,)
        result = []
        try:
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
            for row in c.execute('''SELECT Keyword FROM Stickers WHERE ID=?;''', sticker_id):
                result.append(row[0])
            conn.close()
        except sqlite3.DatabaseError:
            return "Connection to the database is not availble. Please try again later."
        if len(result) == 0:
            return "The sticker has no keywords registered"
        else:
            return "The sticker has these keywords registered: {}".format('\n'.join(result))

    # DELETE a row from the database
    def remove_keyword(self, sticker_id, keyword):
        data = (sticker_id, keyword.lower())
        try:
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
            c.execute('''DELETE FROM Stickers WHERE ID=? AND Keyword=?;''', data)
            conn.commit()
            conn.close()
        except sqlite3.DatabaseError:
            return "Connection to the database is not availble. Please try again later."
        return "Keyword removed succesfully. "

    def search_stickers(self, keyword):
        keyword = ('%'+keyword+'%',)
        result = []
        try:
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
            for row in c.execute('''SELECT ID FROM Stickers WHERE Keyword LIKE ?;''', keyword):
                result.append(row[0])
            conn.close()
        except sqlite3.DatabaseError:
            return result

        return result

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



