import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
import webbrowser
from pass_hasher import encrypt_pass
from database import DatabaseTables
from email_list import EmailList


class Sender:
    def __init__(self):
        self.root = tk.Tk()
        self.font = Font(family="helvetica", size=9, weight="bold")
        self.font_alt = Font(family="helvetica", size=14, weight="bold")
        self.root.title("Set Email For Send")
        self.root.resizable(False, False)
        self.root.geometry("+750+250")
        self.frame = tk.Frame(master=self.root).grid()
        text = "Thank you for using the secret santa generator! Before we start you have to" \
               " enter a few details, there is information on how to set this up here:"

        # Links the user to documentation to set up a gmail account for this service
        self.information = tk.Label(self.frame, font=self.font, padx=20, pady=10, text=text, wraplength=300)
        self.information.grid(row=0, column=0, columnspan=2)
        self.link = tk.Button(self.frame, font=self.font_alt, padx=5, pady=5, bg="black", text=r"DOCUMENTATION",
                              fg="white", cursor="hand2")
        self.link.grid(row=1, column=0, columnspan=2)
        self.link.bind("<Button-1>", lambda e: webbrowser.open_new("https://realpython.com/python-send-email/#option-1-"
                                                                   "setting-up-a-gmail-account-for-development"))
        self.prompt1 = tk.Label(self.frame, pady=10, text="But without further ado, please enter the email and password"
                                " of your gmail account: ", font=self.font, wraplength=300).grid(row=2, column=0, columnspan=2)

        # Get the email and password of the user
        self.prompt2 = tk.Label(self.frame, text="Enter email:", font=self.font).grid(row=3, column=0)
        self.prompt3 = tk.Label(self.frame, text="Enter Password:", font=self.font).grid(row=3, column=1)
        self.email_input = tk.StringVar()
        self.email = ttk.Entry(self.frame, width=30, textvariable=self.email_input)
        self.email.grid(row=4, column=0)
        self.password_input = tk.StringVar()
        self.password = ttk.Entry(self.frame, width=30, textvariable=self.password_input, show="*")
        self.password.grid(row=4, column=1)
        
        # Submit Email and Password
        self.submit = tk.Button(self.frame, pady=15, text="SUBMIT SENDER INFO", bg="black", fg="white",
                                command=self.submit_sender_acc)
        self.submit.grid(row=5, column=0, columnspan=2, sticky="w"+"e")

        self.root.mainloop()
        self.root.quit()
        
    def submit_sender_acc(self):
        result = tk.messagebox.askquestion("Are you sure?", "Are you happy with the email sender details of "
                                            + self.email_input.get(), icon='warning')
        if result == 'yes':
            if self.email_input.get().__contains__("@gmail.com"):
                database = DatabaseTables("sender.db")
                sender_details = (self.email_input.get(), encrypt_pass(self.password_input.get()))
                database.create_sender(sender_details)
                database.close_db()
                tk.messagebox.showinfo("Success!", "Sender email entered successfully!", icon="info")
                self.root.destroy()
                EmailList()
            else:
                tk.messagebox.showinfo("Enter a valid address!", "That isn't a gmail account!")
                return

        else:
            return


if __name__ == "__main__":
    Sender()
