import smtplib
import random
from pass_hasher import decrypt_pass
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# An application that shuffles secret santa email names.


# The class that passes in the Recipient information
from database import DatabaseTables


class Logic:
    def __init__(self, **kwargs):
        self.details = kwargs

    def shuffle_method(self):
        return 0.2

    def shuffle(self):
        keys = list(self.details.keys())
        random.shuffle(keys, self.shuffle_method)
        return keys

    def email_sender(self):

        # Create a secure connection to the server
        database = DatabaseTables("sender.db")
        sender_email = next(iter(database.get_sender_info()))
        password = decrypt_pass(next(iter(database.get_sender_info().values())))
        database.close_db()

        # Create a secure SSL context
        server = smtplib.SMTP('smtp.gmail.com', 25)
        server.connect('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)

        # Try to log in to server and send email
        try:
            for index, name in enumerate(self.details):
                message = MIMEMultipart('related')
                message['Subject'] = "HO HO HO It's Santa!"
                message_alt = MIMEMultipart('alternative')
                message.attach(message_alt)

                image = open("santa.jpg", "rb")
                santa_clause = MIMEImage(image.read())
                image.close()
                santa_clause.add_header("Content-ID", "<santa>")
                present_receiver = self.shuffle()[index]
                message_text = MIMEText("<h1>It's Christmas time {}!</h1><br><p>It's time to celebrate christmas "
                                        "and i'm your secret santa! Don't tell anyone, but you have <h1>{}</h1> as "
                                        "your gift receiver, good luck and have a <b>Merry Christmas!</b><br>"
                                        "<img src='cid:santa'>!".format(name, present_receiver), 'html')
                message_alt.attach(message_text)
                message['From'] = sender_email
                message['To'] = self.details[name]
                message.attach(santa_clause)

                server.sendmail(sender_email, self.details[name], message.as_string())

        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()
