import sqlite3
from sqlite3 import Error


# Save currently input data in a database cache
class Database:
    def __init__(self, db_file):

        # Create the connection
        self.conn = None
        self.cursor = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)

    # Create the table
    def table_schema(self):
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