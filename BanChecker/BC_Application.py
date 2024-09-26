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

# Set up the GUI
root = tk.Tk()
root.title("Ban Tracker")
root.geometry("800x600")
root.configure(bg="gray")

# Create a frame for central alignment
frame = tk.Frame(root, bg="gray")
frame.pack(expand=True, fill=tk.BOTH)

# Configure grid weights for responsive resizing
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Combined input field for account status check and database operations
entry = tk.Entry(frame, width=30, bg="lightgray")
entry.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

# Buttons for checking status, adding, and searching usernames
button_frame = tk.Frame(frame, bg="gray")
button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

check_button = tk.Button(button_frame, text="Check Status", command=check_account, bg="darkblue", fg="white")
check_button.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(button_frame, text="Search Username", command=search_username, bg="darkorange", fg="white")
search_button.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(button_frame, text="Add Username", command=lambda: add_username(entry.get()), bg="green", fg="white")
add_button.pack(side=tk.LEFT, padx=5)

remove_button = tk.Button(button_frame, text="Remove Username", command=lambda: remove_username(entry.get()), bg="darkred", fg="white")
remove_button.pack(side=tk.LEFT, padx=5)

# Result label for account status check
progress_label = tk.Label(frame, text="", font=("Helvetica", 12), bg="gray", fg="yellow")
progress_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

result_label = tk.Label(frame, text="", font=("Helvetica", 12), bg="gray", fg="white")
result_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

# Label to display total usernames
total_label = tk.Label(root, text="Total Usernames: 0", bg="gray", fg="white")
total_label.pack(padx=10, pady=5, fill=tk.X)

# Frame for Listbox and Scrollbar
list_frame = tk.Frame(root)
list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

user_list = tk.Listbox(list_frame, height=10, width=50, bg="lightgray", fg="black")
user_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

user_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=user_list.yview)

# Initialize by displaying any existing usernames
view_usernames()

# Run the GUI event loop
root.mainloop()
