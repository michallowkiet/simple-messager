from security import hash_password


class Users:
    def __init__(self, username="", password=""):
        self.username = username
        self._hashed_password = hash_password(password)
        self._user_id = -1

    @property
    def user_id(self):
        return self._user_id

    @property
    def hashed_password(self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, value):
        self._hashed_password = value

    def save_to_db(self, cursor):
        if self._user_id == -1:
            sql = "INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id"
            params = (self.username, self.hashed_password)
            cursor.execute(sql, params)
            self._user_id = cursor.fetchone()[0]

        else:
            sql = "UPDATE users SET username = %s, hashed_password = %s WHERE id = %s"
            params = (self.username, self.hashed_password, self.user_id)
            cursor.execute(sql, params)

        return self

    def delete(self, cursor):
        if self._user_id != -1:
            cursor.execute("DELETE FROM users WHERE id = %s", (self.user_id,))
            self._user_id = -1
            return True
        return None

    @staticmethod
    def load_user_by_id(cursor, user_id):
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        data = cursor.fetchone()
        if data:
            loaded_id, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._user_id = loaded_id
            loaded_user.hashed_password = hashed_password
            return loaded_user
        return None

    @staticmethod
    def load_user_by_username(cursor, username):
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        data = cursor.fetchone()
        if data:
            loaded_id, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._user_id = loaded_id
            loaded_user.hashed_password = hashed_password
            return loaded_user
        return None

    @staticmethod
    def load_all_users(cursor):
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()

        for i in range(len(result)):
            loaded_id, username, hashed_password = result[i]
            result[i] = Users(username)
            result[i]._user_id = loaded_id
            result[i].hashed_password = hashed_password

        return result
