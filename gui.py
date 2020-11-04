# Create a gui for user input

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font

from logic import EmailList


class GUI:
    def __init__(self):

        # Initialise frame variables
        self.root = tk.Tk()
        self.font = Font(family="helvetica", size=9, weight="bold")
        self.root.title("Secret Santa Designator")
        self.frame = tk.Frame(master=self.root).grid()

        # Create Output area for names to be checked
        self.names_display = tk.Text(self.frame, font=self.font,  width=50, height=15, state="disabled")
        self.names_display.grid(row=0, column=0, columnspan=2)

        # Initialise a data dictionary for user input
        self.recipients = {}

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

        self.root.mainloop()
        self.root.quit()
    
    # Enter the details for each person
    def enter_name(self):
        # Error handling
        if self.email_input.get() in self.recipients.values():
            tk.messagebox.showinfo("Repetition!", "Email already entered!", icon="warning")
        elif self.email_input.get() == "" or self.name_input.get() == "":
            tk.messagebox.showinfo("Empty!", "Please insert a value!", icon="warning")
        elif not self.email_input.get().__contains__("@"):
            tk.messagebox.showinfo("Value Error!", "Email does not contain an @!!", icon="info")

        # Add to the dictionary
        else:
            self.recipients[self.name_input.get()] = self.email_input.get()
            self.names_display.config(state="normal")
            output_value = self.name_input.get() + " : " + self.email_input.get()
            self.names_display.insert("end", output_value + "\n" + "-" * round(len(output_value) * 1.5) + "\n")
            self.names_display.config(state="disabled")
        self.name_input.set("")
        self.email_input.set("")
        self.name.focus_set()

    # Removes the last entered value from the dictionary
    def remove_last(self):
        try:
            self.names_display.config(state="normal")
            self.names_display.delete("1.0", "end")
            self.recipients.pop(list(self.recipients.keys())[-1])
            for key in self.recipients:
                self.names_display.insert("end", key + " : " + self.recipients.get(key) + "\n")
            self.names_display.config(state="disabled")
            self.name.focus_set()
        except IndexError:
            tk.messagebox.showinfo("No Value Error!", "There are no values in the recipient list!", icon="warning")

    # Removes all of the recipients from the list
    def remove_all(self):
        result = tk.messagebox.askquestion("Start Again!?", "Are You Sure you want to remove all entered "
                                           "recipients?", icon='warning')
        if result == 'yes':
            self.recipients.clear()
            self.names_display.config(state="normal")
            self.names_display.delete("1.0", "end")
            self.names_display.config(state="disabled")
        else:
            return
        self.name.focus_set()

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
        self.name.focus_set()