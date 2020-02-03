import sqlite3


class DB:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            Users (
                cid INT PRIMARY KEY,
                name VARCHAR(255),
                
            )
        """)
        self.connection.commit()
        print(self.select_all_users())

    def select_all_users(self):
        return self.connection.cursor().execute("SELECT * FROM Users").fetchall()

    def select_user(self, user_cid):
        return self.connection.cursor().execute("SELECT * FROM Users WHERE cid = (?)", int(user_cid)).fetchone()

    def add_user(self, user_cid, user_name):
        if self.select_user(user_cid) is None:
            self.connection.cursor().execute("INSERT INTO Users VALUES ((?), (?)) LIMIT 1", int(user_cid), str(user_name))
            self.connection.commit()
            return True
        else:
            return False