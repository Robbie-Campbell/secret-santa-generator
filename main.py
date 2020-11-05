# Run the function
from database import DatabaseTables
from email_list import EmailList
from email_sender import Sender

if __name__ == "__main__":
    database = DatabaseTables("sender.db")
    if database.get_sender_info() is not None:
        main_function = EmailList()
    else:
        main_function = Sender()
