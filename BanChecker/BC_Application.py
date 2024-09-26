import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os

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
    username = username_entry.get()
    if username:
        active_count = 0
        banned_count = 0

        # Run the check five times, updating the progress label
        for i in range(5):
            progress_label.config(text=f"Checking... {i+1}/5 cycles complete")
            root.update_idletasks()

            status = check_account_status(username)
            if "active" in status:
                active_count += 1
            else:
                banned_count += 1

        # Determine the final result
        if banned_count > 0:
            result_label.config(text="The account is either banned or does not exist.", fg="red")
        else:
            result_label.config(text="The account is active.", fg="lightgreen")

        # Reset progress label after completion
        progress_label.config(text="Status check complete.")
    else:
        result_label.config(text="Please enter an Instagram username.", fg="black")

# Storage section (Database Management)
file_path = "usernames.txt"

def load_usernames():
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, "r") as file:
        usernames = file.read().splitlines()
    return usernames

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
    update_total_label(len(usernames))
    view_usernames()

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

def view_usernames():
    usernames = load_usernames()
    user_list.delete(0, tk.END)
    if usernames:
        for username in usernames:
            user_list.insert(tk.END, username)
    update_total_label(len(usernames))

def update_total_label(count):
    total_label.config(text=f"Total Usernames: {count}")

def compare_file():
    file_to_compare = filedialog.askopenfilename(title="Select a .txt file", filetypes=[("Text files", "*.txt")])
    
    if file_to_compare:
        try:
            with open(file_to_compare, "r") as file:
                new_usernames = file.read().splitlines()

            existing_usernames = load_usernames()
            unique_usernames = [name for name in new_usernames if name not in existing_usernames]

            if unique_usernames:
                existing_usernames.extend(unique_usernames)
                save_usernames(existing_usernames)
                
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

def alphabetize_usernames():
    usernames = load_usernames()
    sorted_usernames = sorted(usernames)
    save_usernames(sorted_usernames)
    view_usernames()
    messagebox.showinfo("Success", "Usernames have been alphabetized.")

# Set up the GUI
root = tk.Tk()
root.title("Ban Tracker")
root.geometry("600x500")
root.configure(bg="gray")

# Create a frame for central alignment
frame = tk.Frame(root, bg="gray")
frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

# Configure grid weights for responsive resizing inside root
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configure grid weights for the frame
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Input field shared for both checking and database management
username_entry = tk.Entry(frame, width=40, bg="lightgray", fg="black")
username_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
username_entry.insert(0, "Enter Instagram Username")
username_entry.bind("<FocusIn>", lambda e: username_entry.delete(0, tk.END) if username_entry.get() == "Enter Instagram Username" else None)
username_entry.bind("<FocusOut>", lambda e: username_entry.insert(0, "Enter Instagram Username") if username_entry.get() == "" else None)

# Buttons for checking account status and managing database
check_button = tk.Button(frame, text="Check Status", command=check_account, bg="darkblue", fg="white")
check_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

add_button = tk.Button(frame, text="Add Username", command=lambda: add_username(username_entry.get()), bg="green", fg="white")
add_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

remove_button = tk.Button(frame, text="Remove Username", command=lambda: remove_username(username_entry.get()), bg="darkred", fg="white")
remove_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

progress_label = tk.Label(frame, text="", font=("Helvetica", 12), bg="gray", fg="yellow")
progress_label.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

result_label = tk.Label(frame, text="", font=("Helvetica", 12), bg="gray", fg="white")
result_label.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

# Frame for Listbox and Scrollbar
listbox_frame = tk.Frame(root)
listbox_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

user_list = tk.Listbox(listbox_frame, height=10, width=50, bg="lightgray", fg="black")
user_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
user_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=user_list.yview)

total_label = tk.Label(root, text="Total Usernames: 0", bg="gray", fg="white")
total_label.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

alphabetize_button = tk.Button(root, text="Alphabetize Usernames", command=alphabetize_usernames, bg="blue", fg="white")
alphabetize_button.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

compare_button = tk.Button(root, text="Compare Files", command=compare_file, bg="darkblue", fg="white")
compare_button.grid(row=9, column=0, padx=10, pady=10, sticky="ew")

view_usernames()

# Run the GUI event loop
root.mainloop()
