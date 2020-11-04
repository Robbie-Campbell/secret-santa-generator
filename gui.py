# Create a gui for user input

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from logic import EmailList


class GUI:
    def __init__(self):

        # Initialise frame variables
        self.root = tk.Tk()
        self.root.title("Secret Santa Designator")
        self.frame = tk.Frame(master=self.root).grid()

        # Create Output area for names to be checked
        self.names_display = tk.Text(self.frame, width=50, height=15, state="disabled")
        self.names_display.grid(row=0, column=0, columnspan=2)

        # Initialise a data dictionary for user input
        self.recipients = {}

        # Create entry areas and prompts
        self.name_label = tk.Label(self.frame, text="Enter Name of recipient").grid(row=1, column=0)
        self.email_label = tk.Label(self.frame, text="Enter Email of recipient").grid(row=1, column=1)

        self.name_input = tk.StringVar()
        self.name = ttk.Entry(self.frame, textvariable=self.name_input).grid(row=2, column=0)
        self.email_input = tk.StringVar()
        self.email = ttk.Entry(self.frame, textvariable=self.email_input).grid(row=2, column=1)

        # Submit a name button
        self.submit = tk.Button(self.frame, pady=10, text="Submit a recipient", bg="#FFF", command=self.enter_name)\
            .grid(row=3, column=0, columnspan=2, sticky="W" + "E")

        # Edit last name entered
        self.send = tk.Button(self.frame, pady=10,  text="Send to addresses", bg="#600", fg="#FFF", command=self.send_emails)\
            .grid(row=4, column=0, columnspan=2, sticky="W" + "E")

        # Send the emails
        self.remove = tk.Button(self.frame, pady=10,  text="Remove last entry", bg="#006", fg="#FFF", command=self.remove_last)\
            .grid(row=5, column=0, columnspan=2, sticky="W" + "E")

        # Reset the names button
        self.reset = tk.Button(self.frame, pady=10,  text="Reset entered names", bg="#060", fg="#FFF", command=self.remove_all)\
            .grid(row=6, column=0, columnspan=2, sticky="W" + "E")

        self.root.mainloop()
        self.root.quit()
    
    # Enter the details for each person
    def enter_name(self):
        self.recipients[self.name_input.get()] = self.email_input.get()
        self.names_display.config(state="normal")
        self.names_display.insert("end", self.name_input.get() + " : " + self.email_input.get() + "\n")
        self.names_display.config(state="disabled")
        self.name_input.set("")
        self.email_input.set("")

    # Removes the last entered value from the dictionary
    def remove_last(self):
        self.names_display.config(state="normal")
        self.names_display.delete("1.0", "end")
        self.recipients.pop(list(self.recipients.keys())[-1])
        for key in self.recipients:
            self.names_display.insert("end", key + " : " + self.recipients.get(key) + "\n")
        self.names_display.config(state="disabled")

    # Removes all of the recipients from the list
    def remove_all(self):
        result = tk.messagebox.askquestion("Start Again", "Are You Sure you want to remove all entered"
                                                          "recipients?", icon='warning')
        if result == 'yes':
            self.recipients.clear()
            self.names_display.config(state="normal")
            self.names_display.delete("1.0", "end")
            self.names_display.config(state="disabled")
        else:
            return

    # Send all of the emails
    def send_emails(self):
        result = tk.messagebox.askquestion("Send emails", "Are you ready to spread christmas joy to the recipients?",
                                           icon='warning')
        if result == 'yes':
            print(self.recipients)
            send = EmailList(**self.recipients)
            send.email_sender()
            tk.messagebox.showinfo("Success!", "Emails have successfully been sent!", icon="info")
            self.root.destroy()

        else:
            return


if __name__ == "__main__":
    test = GUI()