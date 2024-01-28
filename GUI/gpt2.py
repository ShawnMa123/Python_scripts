import tkinter as tk
from tkinter import messagebox

class ParameterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parameter Input")

        self.parameters = []

        # Create and place labels and entry widgets for user input
        self.entries = []
        for i in range(5):
            label = tk.Label(root, text=f"Parameter {i+1}:")
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(root)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(entry)

        # Create a submit button
        self.submit_button = tk.Button(root, text="Submit", command=self.store_parameters)
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def store_parameters(self):
        # Store the parameters from the entries into the class variable
        self.parameters = [entry.get() for entry in self.entries]
        messagebox.showinfo("Success", "Parameters have been stored successfully!")
        print(self.parameters)  # For demonstration, print to console

# Create the main window
root = tk.Tk()

# Create an instance of the app
app = ParameterApp(root)

# Run the app
root.mainloop()