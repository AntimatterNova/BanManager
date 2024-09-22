import os
import tkinter as tk
from tkinter import filedialog, messagebox

#Passionately crafted by AntimatterNova for use by members of the you.are.a.hitman (YAAH) group. 9/22/2024

# Path to the text file storing usernames
file_path = "usernames.txt"

# Function to load usernames from the .txt file
def load_usernames():
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, "r") as file:
        usernames = file.read().splitlines()  # Read lines into a list
    return usernames

# Function to save the list of usernames to the .txt file
def save_usernames(usernames):
    with open(file_path, "w") as file:
        file.write("\n".join(usernames))  # Write each username on a new line
    update_total_label(len(usernames))

# Function to add a new username to the list
def add_username(username):
    usernames = load_usernames()
    if username not in usernames:
        usernames.append(username)
        save_usernames(usernames)
        messagebox.showinfo("Success", f"Username '{username}' added.")
    else:
        messagebox.showwarning("Warning", f"Username '{username}' already exists.")
    update_total_label(len(usernames))
    view_usernames()

# Function to remove a username from the list
def remove_username(username):
    usernames = load_usernames()
    if username in usernames:
        usernames.remove(username)
        save_usernames(usernames)
        messagebox.showinfo("Success", f"Username '{username}' removed.")
    else:
        messagebox.showwarning("Warning", f"Username '{username}' not found.")
    update_total_label(len(usernames))
    view_usernames()

# Function to display all usernames
def view_usernames():
    usernames = load_usernames()
    user_list.delete(0, tk.END)  # Clear the listbox first
    if usernames:
        for username in usernames:
            user_list.insert(tk.END, username)
    update_total_label(len(usernames))

# Function to update the label that shows the total number of usernames
def update_total_label(count):
    total_label.config(text=f"Total Usernames: {count}")

# Function to open a new .txt file and compare with current usernames
def compare_file():
    # Open file dialog to select the new file to compare
    file_to_compare = filedialog.askopenfilename(title="Select a .txt file", filetypes=[("Text files", "*.txt")])
    
    if file_to_compare:
        try:
            # Read the new file
            with open(file_to_compare, "r") as file:
                new_usernames = file.read().splitlines()

            # Compare and merge with the current list
            existing_usernames = load_usernames()
            unique_usernames = [name for name in new_usernames if name not in existing_usernames]

            if unique_usernames:
                # Extend the existing list with unique new usernames
                existing_usernames.extend(unique_usernames)
                
                # Save the updated list of usernames
                save_usernames(existing_usernames)
                
                # Ask for confirmation to delete the compared file
                if messagebox.askyesno("Delete File", "Do you want to delete the compared file?"):
                    os.remove(file_to_compare)
                    messagebox.showinfo("Success", f"Added {len(unique_usernames)} new usernames and deleted the compared file.")
                else:
                    messagebox.showinfo("File Not Deleted", "The compared file was not deleted.")
            else:
                messagebox.showinfo("No New Usernames", "No new usernames found in the selected file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the file: {e}")
    else:
        messagebox.showwarning("No File", "Please select a valid .txt file.")
    
    view_usernames()

# Function to alphabetize the usernames
def alphabetize_usernames():
    usernames = load_usernames()
    sorted_usernames = sorted(usernames)
    save_usernames(sorted_usernames)
    view_usernames()
    messagebox.showinfo("Success", "Usernames have been alphabetized.")

# Create the main window
root = tk.Tk()
root.title("Ban Manager")
root.geometry("800x600")
root.configure(bg="gray")

# Create UI elements with specified colors
username_entry = tk.Entry(root, width=40, bg="lightgray", fg="black")
username_entry.insert(0, "Enter username...")  # Placeholder text
username_entry.bind("<FocusIn>", lambda e: username_entry.delete(0, tk.END) if username_entry.get() == "Enter username..." else None)
username_entry.bind("<FocusOut>", lambda e: username_entry.insert(0, "Enter username...") if username_entry.get() == "" else None)
username_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

add_button = tk.Button(root, text="Add Username", command=lambda: add_username(username_entry.get()), bg="green", fg="white")
add_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

remove_button = tk.Button(root, text="Remove Username", command=lambda: remove_username(username_entry.get()), bg="darkred", fg="white")
remove_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

# Frame for Listbox and Scrollbar
frame = tk.Frame(root)
frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Configure grid weights to allow resizing
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# Listbox to display usernames
user_list = tk.Listbox(frame, height=10, width=50, bg="lightgray", fg="black")
user_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the Listbox
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the scrollbar to the Listbox
user_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=user_list.yview)

# Label to display total usernames
total_label = tk.Label(root, text="Total Banned Users: 0", bg="gray", fg="white")
total_label.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

# Button to alphabetize usernames
alphabetize_button = tk.Button(root, text="Alphabetize Usernames", command=alphabetize_usernames, bg="blue", fg="white")
alphabetize_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

# Button to open a file and compare usernames
compare_button = tk.Button(root, text="Compare Files", command=compare_file, bg="darkblue", fg="white")
compare_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

# Initialize by displaying any existing usernames
view_usernames()

# Start the application
root.mainloop()
