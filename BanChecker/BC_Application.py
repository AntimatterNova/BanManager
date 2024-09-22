import subprocess
import tkinter as tk

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
        status = check_account_status(username)
        result_label.config(text=status, fg="lightgreen" if "active" in status else "red")
    else:
        result_label.config(text="Please enter an Instagram username.", fg="black")

# Set up the GUI
root = tk.Tk()
root.title("Ban Checker")
root.geometry("800x600")
root.configure(bg="gray")

# Create a frame for central alignment
frame = tk.Frame(root, bg="gray")
frame.pack(expand=True, fill=tk.BOTH)  # Allow frame to expand and fill the window

# Configure grid weights for responsive resizing
frame.grid_rowconfigure(0, weight=0)
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=0)
frame.grid_rowconfigure(3, weight=0)
frame.grid_columnconfigure(0, weight=1)

# Create and place widgets within the frame with adjusted padding
label = tk.Label(frame, text="Enter Instagram Username Below:", bg="gray", fg="white")
label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

entry = tk.Entry(frame, width=30, bg="lightgray")
entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

check_button = tk.Button(frame, text="Check Status", command=check_account, bg="darkblue", fg="white")
check_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

result_label = tk.Label(frame, text="", font=("Helvetica", 12), bg="gray", fg="white")
result_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

# Run the GUI event loop
root.mainloop()
