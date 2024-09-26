import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Account status checker function
def check_account_status(username):
    try:
        result = subprocess.run(
            ['node', 'BanChecker.js', username],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return "Error checking account status."

def check_account():
    username = entry.get()
    if username:
        active_count = 0
        banned_count = 0
        for i in range(5):
            progress_label.config(text=f"Checking... {i+1}/5 cycles complete")
            root.update_idletasks()
            
            status = check_account_status(username)
            if "active" in status:
                active_count += 1
            else:
                banned_count += 1
        
        if banned_count > 0:
            result_label.config(text="The account is either banned or does not exist.", fg="red")
        else:
            result_label.config(text="The account is active.", fg="lightgreen")

        progress_label.config(text="Status check complete.")
    else:
        result_label.config(text="Please enter an Instagram username.", fg="black")

# Database functions
file_path = "usernames.txt"

def load_usernames():
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as file:
        return file.read().splitlines()

def save_usernames(usernames):
    with open(file_path, "w") as file:
        file.write("\n".join(usernames))
    update_total_label(len(usernames))

def add_username(username):
    usernames = load_usernames()
    if username not in usernames:
        usernames.append(username)
        save_usernames(usernames)
        messagebox.showinfo("Success", f"Username '{username}' added.")
    else:
        messagebox.showwarning("Warning", f"Username '{username}' already exists.")
    view_usernames()

def search_username():
    search_term = entry.get()
    usernames = load_usernames()
    if search_term in usernames:
        idx = usernames.index(search_term)
        user_list.see(idx)
        user_list.selection_clear(0, tk.END)
        user_list.selection_set(idx)
        messagebox.showinfo("Success", f"Found '{search_term}' at position {idx + 1}.")
    else:
        messagebox.showwarning("Not Found", f"Username '{search_term}' not found in the list.")

def remove_username(username):
    usernames = load_usernames()
    if username in usernames:
        usernames.remove(username)
        save_usernames(usernames)
        messagebox.showinfo("Success", f"Username '{username}' removed.")
    else:
        messagebox.showwarning("Warning", f"Username '{username}' not found.")
    view_usernames()

def view_usernames():
    usernames = load_usernames()
    user_list.delete(0, tk.END)
    for username in usernames:
        user_list.insert(tk.END, username)
    update_total_label(len(usernames))

def update_total_label(count):
    total_label.config(text=f"Total Usernames: {count}")

def alphabetize_usernames():
    usernames = load_usernames()
    usernames.sort()  # Sort the usernames alphabetically
    save_usernames(usernames)  # Save the sorted list back to the file
    view_usernames()  # Refresh the Listbox to display the sorted usernames
    messagebox.showinfo("Success", "Usernames alphabetized successfully.")

# Set up the GUI
root = tk.Tk()
root.title("Ban Tracker")
root.geometry("800x600")
root.configure(bg="gray")

# Configure grid weights to make widgets expand with window resize
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)  # For the Listbox to expand
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)

# Combined input field for account status check and database operations
entry = tk.Entry(root, width=30, bg="lightgray")
entry.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

# Buttons for checking status, adding, and searching usernames
button_frame = tk.Frame(root, bg="gray")
button_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
button_frame.grid_columnconfigure([0, 1, 2, 3, 4], weight=1)  # Allow buttons to expand

check_button = tk.Button(button_frame, text="Check Status", command=check_account, bg="darkblue", fg="white")
check_button.grid(row=0, column=0, padx=5, sticky="ew")

search_button = tk.Button(button_frame, text="Search Username", command=search_username, bg="orange", fg="white")
search_button.grid(row=0, column=1, padx=5, sticky="ew")

add_button = tk.Button(button_frame, text="Add Username", command=lambda: add_username(entry.get()), bg="green", fg="white")
add_button.grid(row=0, column=2, padx=5, sticky="ew")

remove_button = tk.Button(button_frame, text="Remove Username", command=lambda: remove_username(entry.get()), bg="darkred", fg="white")
remove_button.grid(row=0, column=3, padx=5, sticky="ew")

alphabetize_button = tk.Button(button_frame, text="Alphabetize List", command=alphabetize_usernames, bg="purple", fg="white")
alphabetize_button.grid(row=0, column=4, padx=5, sticky="ew")

# Result label for account status check
progress_label = tk.Label(root, text="", font=("Helvetica", 12), bg="gray", fg="yellow")
progress_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="gray", fg="white")
result_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

# Frame for Listbox and Scrollbar
list_frame = tk.Frame(root)
list_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

# Configure the listbox to resize with the window
list_frame.grid_columnconfigure(0, weight=1)
list_frame.grid_rowconfigure(0, weight=1)

user_list = tk.Listbox(list_frame, height=10, width=50, bg="lightgray", fg="black")
user_list.grid(row=0, column=0, sticky="nsew")

scrollbar = tk.Scrollbar(list_frame)
scrollbar.grid(row=0, column=1, sticky="ns")

user_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=user_list.yview)

# Label to display total usernames
total_label = tk.Label(root, text="Total Usernames: 0", bg="gray", fg="white")
total_label.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

# Initialize by displaying any existing usernames
view_usernames()

# Run the GUI event loop
root.mainloop()
