import sqlite3
import os.path
from sqlite3 import Error


# Save currently input data in a database cache
class DatabaseTables:
    def __init__(self):

        # Create the connection
        self.conn = None
        self.cursor = None
        base_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            self.conn = sqlite3.connect(base_dir + "cache.db")
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)

    # --------------------------- EMAIL SENDER FUNCTIONS ------------------------- #
    def create_sender_table(self):
        create_sender_table = """
        CREATE TABLE IF NOT EXISTS sender (
            email VARCHAR(50),
            password VARCHAR(50)
        );
        """
        if self.conn is not None:
            self.cursor.execute(create_sender_table)
        else:
            print("error, did not work")

    # Create the main user
    def create_sender(self, details):
        insert_script = """
        INSERT INTO sender(email,password) VALUES (?, ?)
        """
        self.cursor.execute(insert_script, details)
        self.conn.commit()

    # get the info to send to the recipients
    def get_sender_info(self):
        self.cursor.execute("SELECT * FROM sender")
        dictionary = {}
        values = self.cursor.fetchall()
        for value in values:
            dictionary[value[0]] = value[1]
        return dictionary

    def clear_sender_info(self):
        self.cursor.execute("DELETE FROM sender")
        self.conn.commit()

    # --------------------------- RECIPIENT FUNCTIONS ------------------------- #
    def create_name_list_table(self):
        create_main_table = """
        CREATE TABLE IF NOT EXISTS cache (
            name VARCHAR(20),
            email VARCHAR(50)
        );
        """
        if self.conn is not None:
            self.cursor.execute(create_main_table)
        else:
            print("error, did not work")

    # Insert data into table
    def insert_data(self, name):
        insert_script = """
        INSERT INTO cache(name,email) VALUES (?, ?)
        """
        self.cursor.execute(insert_script, name)
        self.conn.commit()

    # Return all data
    def select_data(self):
        self.cursor.execute("SELECT * FROM cache")
        dictionary = {}
        values = self.cursor.fetchall()
        for value in values:
            dictionary[value[0]] = value[1]
        return dictionary

    # Clear the cache
    def clear_db(self):
        self.cursor.execute("DELETE FROM cache")
        self.conn.commit()

    # Remove most recent row
    def remove_row(self, name):
        self.cursor.execute("DELETE FROM cache WHERE name=?", (name,))
        self.conn.commit()

    # Called when finished with db
    def close_db(self):
        self.conn.close()
