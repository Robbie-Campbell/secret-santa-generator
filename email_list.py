# Create a gui for user input

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font

from database import DatabaseTables
from logic import Logic


class EmailList:
    def __init__(self):

        # Define frame and root variables
        self.root = tk.Tk()
        self.font = Font(family="helvetica", size=9, weight="bold")
        self.root.title("Secret Santa Designator")
        self.root.resizable(False, False)
        self.root.geometry("+750+250")
        self.frame = tk.Frame(master=self.root).grid()

        # Define a database to save user progress and populate the dictionary with existing data
        self.database = DatabaseTables("cache.db")
        self.recipients = self.database.select_data()

        # Create Output area for names to be checked
        self.names_display = tk.Text(self.frame, font=self.font,  width=50, height=25)
        self.names_display.grid(row=0, column=0, columnspan=2)

        # Display the data to the user if there is anything in the database
        self.names_display.config(state="normal")
        for key in self.recipients:
            output_value = key + " : " + self.recipients[key]
            self.names_display.insert("end", output_value + "\n" + "-" * round(len(output_value) * 1.5) + "\n")
        self.database.close_db()
        self.names_display.config(state="disabled")

        # Create entry areas and prompts
        self.name_label = tk.Label(self.frame, font=self.font,  text="Enter First Name of Recipient").grid(row=1, column=0)
        self.email_label = tk.Label(self.frame, font=self.font,  text="Enter Email of Recipient").grid(row=1, column=1)

        self.name_input = tk.StringVar()
        self.name = ttk.Entry(self.frame, width=30, textvariable=self.name_input)
        self.name.grid(row=2, column=0)
        self.email_input = tk.StringVar()
        self.email = ttk.Entry(self.frame, width=30, textvariable=self.email_input)
        self.email.grid(row=2, column=1)

        # Add a key listener for email/ name entry
        self.email.bind("<Return>", lambda event: self.enter_name())
        self.name.bind("<Return>", lambda event: self.enter_name())

        # Set default focus
        self.name.focus_set()

        # Submit a name button
        self.submit = tk.Button(self.frame, pady=10, font=self.font, text="Submit a recipient", bg="#FFF",
                                command=self.enter_name).grid(row=3, column=0, columnspan=2, sticky="W" + "E")

        # Edit last name entered
        self.send = tk.Button(self.frame, pady=10, font=self.font,  text="Send to addresses", bg="#600", fg="#FFF",
                              command=self.send_emails).grid(row=4, column=0, columnspan=2, sticky="W" + "E")

        # Send the emails
        self.remove = tk.Button(self.frame, pady=10, font=self.font, text="Remove last entry", bg="#006", fg="#FFF",
                                command=self.remove_last).grid(row=5, column=0, columnspan=2, sticky="W" + "E")

        # Reset the names button
        self.reset = tk.Button(self.frame, pady=10, font=self.font, text="Reset entered names", bg="#060", fg="#FFF",
                               command=self.remove_all).grid(row=6, column=0, columnspan=2, sticky="W" + "E")

        self.reconfigure_email = tk.Button(self.frame, pady=10, font=self.font, text="Reset Email Sender", bg="#000", fg="#FFF",
                                           command=self.reset_email).grid(row=7, column=0, columnspan=2, sticky="W" + "E")

        self.root.mainloop()
        self.root.quit()
    
    # Enter the details for each person
    def enter_name(self):
        # Error handling for repeat values, empty input and not an email
        if self.email_input.get() in self.recipients.values():
            tk.messagebox.showinfo("Repetition!", "Email already entered!", icon="warning")
        elif self.email_input.get() == "" or self.name_input.get() == "":
            tk.messagebox.showinfo("Empty!", "Please insert a value!", icon="warning")
        elif not self.email_input.get().__contains__("@"):
            tk.messagebox.showinfo("Value Error!", "Email does not contain an @!!", icon="info")

        # Add to the dictionary
        else:
            # Input the values into the cache database
            self.database = DatabaseTables("cache.db")
            enter_value = (self.name_input.get().capitalize(), self.email_input.get())
            self.database.insert_data(enter_value)
            self.database.close_db()

            # Save the values in current memory
            self.recipients[self.name_input.get().capitalize()] = self.email_input.get()
            self.names_display.config(state="normal")
            output_value = self.name_input.get().capitalize() + " : " + self.email_input.get()
            self.names_display.insert("end", output_value + "\n" + "-" * round(len(output_value) * 1.5) + "\n")
            self.names_display.config(state="disabled")

        # Reset to defaults
        self.name_input.set("")
        self.email_input.set("")
        self.name.focus_set()

    # Removes the last entered value from the dictionary
    def remove_last(self):
        try:

            # Remove the most recent entry from the database
            self.database = DatabaseTables("cache.db")
            self.database.remove_row(list(self.recipients.keys())[-1])
            self.database.close_db()

            # Remove the most recent entry from memory and repopulate the text area
            self.names_display.config(state="normal")
            self.names_display.delete("1.0", "end")
            self.recipients.pop(list(self.recipients.keys())[-1])
            for key in self.recipients:
                self.names_display.insert("end", key + " : " + self.recipients.get(key) + "\n")
            self.names_display.config(state="disabled")
            self.name.focus_set()

        # Error handling for no available deletion
        except IndexError:
            tk.messagebox.showinfo("No Value Error!", "There are no values in the recipient list!", icon="warning")

    # Removes all of the recipients from the list
    def remove_all(self):
        result = tk.messagebox.askquestion("Start Again!?", "Are You Sure you want to remove all entered "
                                           "recipients?", icon='warning')
        if result == 'yes':

            # Remove all from the database
            self.database = DatabaseTables("cache.db")
            self.database.clear_db()
            self.database.close_db()

            # Remove all from current memory
            self.recipients.clear()
            self.names_display.config(state="normal")
            self.names_display.delete("1.0", "end")
            self.names_display.config(state="disabled")
        else:
            return

        # Reset to default
        self.name.focus_set()

    # Send all of the emails
    def send_emails(self):
        result = tk.messagebox.askquestion("Send emails", "Are you ready to spread christmas joy to the recipients?",
                                           icon='warning')
        if result == 'yes':

            # Remove all from the database
            self.database = DatabaseTables("cache.db")
            self.database.clear_db()
            self.database.close_db()

            # Send the emails to the end users
            send = Logic(**self.recipients)
            send.email_sender()
            tk.messagebox.showinfo("Success!", "Emails have successfully been sent!", icon="info")
            self.root.destroy()

        else:
            return

        # Reset to default
        self.name.focus_set()

    # Allows the user to use a different sender Address
    def reset_email(self):
        self.root.destroy()
        database = DatabaseTables("sender.db")
        database.clear_sender_info()
        database.close_db()
