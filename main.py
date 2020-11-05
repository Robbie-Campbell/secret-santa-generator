# Run the function
from database import DatabaseTables
from GUI.email_list import EmailList
from GUI.email_sender import Sender

if __name__ == "__main__":
    database = DatabaseTables()
    database.create_name_list_table()
    database.create_sender_table()
    if database.get_sender_info():
        main_function = EmailList()
        database.close_db()
    else:
        main_function = Sender()
        database.close_db()