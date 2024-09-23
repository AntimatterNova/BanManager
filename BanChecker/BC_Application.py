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
            check=True  # This will raise an error if the command fails
        )
        return result.stdout.strip()  # Get the output and remove extra whitespace
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)  # Print the error message
        return "Error checking account status."

def check_account():
    username = entry.get()
    if username:
        active_count = 0
        banned_count = 0

        # Run the check five times, updating the progress label
        for i in range(5):
            progress_label.config(text=f"Checking... {i+1}/5 cycles complete")
            root.update_idletasks()  # Force update of the progress label
            
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

# Storage section ========================================================================
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
    user_list.delete(0, tk.END)  # Clear the listbox first
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
root.geometry("")
root.configure(bg="gray")

# Create a frame for central alignment
frame = tk.Frame(root, bg="gray")
frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")  # Use grid instead of pack

# Configure grid weights for responsive resizing
root.grid_rowconfigure(9, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configure grid weights for the frame
frame.grid_rowconfigure(0, weight=1)  # Top label
frame.grid_rowconfigure(1, weight=1)  # Entry field
frame.grid_rowconfigure(2, weight=1)  # Button
frame.grid_rowconfigure(3, weight=1)  # Progress label
frame.grid_rowconfigure(4, weight=1)  # Result label
frame.grid_columnconfigure(0, weight=1)  # Allow column to expand horizontally

# Create and place widgets within the frame with adjusted padding
label = tk.Label(frame, text="Enter account name below to check ban status:", bg="gray", fg="white")
label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

entry = tk.Entry(frame, width=30, bg="lightgray")
entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

check_button = tk.Button(frame, text="Check Account Status", command=check_account, bg="darkblue", fg="white")
check_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

progress_label = tk.Label(frame, text="", font=("Helvetica", 12), bg="gray", fg="yellow")
progress_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

result_label = tk.Label(frame, text="", font=("Helvetica", 12), bg="gray", fg="white")
result_label.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

# Rest of the code using grid
username_entry = tk.Entry(root, width=40, bg="lightgray", fg="black")
username_entry.insert(0, "Enter username...")
username_entry.bind("<FocusIn>", lambda e: username_entry.delete(0, tk.END) if username_entry.get() == "Enter username..." else None)
username_entry.bind("<FocusOut>", lambda e: username_entry.insert(0, "Enter username...") if username_entry.get() == "" else None)
username_entry.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

add_button = tk.Button(root, text="Add Username", command=lambda: add_username(username_entry.get()), bg="green", fg="white")
add_button.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

remove_button = tk.Button(root, text="Remove Username", command=lambda: remove_username(username_entry.get()), bg="darkred", fg="white")
remove_button.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

# Frame for Listbox and Scrollbar
listbox_frame = tk.Frame(root)
listbox_frame.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")

# Listbox to display usernames
user_list = tk.Listbox(listbox_frame, height=10, width=50, bg="lightgray", fg="black")
user_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the Listbox
scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Linking the scrollbar to the Listbox
user_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=user_list.yview)

# Label to display total usernames
total_label = tk.Label(root, text="Total Banned Users: 0", bg="gray", fg="white")
total_label.grid(row=10, column=0, padx=10, pady=5, sticky="ew")

# Button to alphabetize usernames
alphabetize_button = tk.Button(root, text="Alphabetize Usernames", command=alphabetize_usernames, bg="blue", fg="white")
alphabetize_button.grid(row=11, column=0, padx=10, pady=5, sticky="ew")

# Button to open a file and compare usernames
compare_button = tk.Button(root, text="Compare Files", command=compare_file, bg="darkblue", fg="white")
compare_button.grid(row=12, column=0, padx=10, pady=10, sticky="ew")

# Initialize by displaying any existing usernames
view_usernames()

# Run the GUI event loop
root.mainloop()

