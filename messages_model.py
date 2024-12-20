from datetime import datetime


class Messages:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        if self._id == -1:
            cursor.execute(
                "INSERT INTO messages (from_id, to_id, text, creation_date) VALUES (%s, %s, %s, %s) RETURNING id",
                (self.from_id, self.to_id, self.text, datetime.now()),
            )
            self._id = cursor.fetchone()[0]
            return self
        else:
            cursor.execute(
                "UPDATE messages SET from_id = %s, to_id = %s, text = %s, creation_date = %s WHERE id = %s",
                (self.from_id, self.to_id, self.text, self.id, datetime.now()),
            )
            return self

    @staticmethod
    def load_all_messages(cursor):
        cursor.execute("SELECT * FROM messages")

        return [Messages.load_message_by_id(cursor, message_id) for message_id in cursor.fetchall()]
