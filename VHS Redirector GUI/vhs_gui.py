import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def on_radio_selected():
    if selected_option.get() == "Client":
        client_entry.config(state=tk.NORMAL)
    else:
        client_entry.config(state=tk.DISABLED)

def on_enter_key(event):
    launch_script()

def launch_script():
    try:
        hostsfile_path = os.path.join(os.environ['windir'], 'System32', 'drivers', 'etc', 'hosts')
    except Exception as e:
        print("This is not a Windows enviornment. Testing with a local file \"hosts.txt\"")
        hostsfile_path = "hosts.txt"
    ip_address = "127.0.0.1" # Set to localhost by default

    if selected_option.get() == "Host":
        print("Hello, World! - Host")

    elif selected_option.get() == "Client":
        client_input = client_entry.get()
        if not client_input.strip():
            messagebox.showwarning("Warning", "Please enter an address for the client.")
            return
        else:
            ip_address = client_input
            # Write ip address input to cache file
            with open("ipcache.txt", "w") as file:
                lines = file.write(ip_address)
            print(f"Hello, World! - Client: {ip_address}")
    
    try:
        with open(hostsfile_path, 'r') as file:
            lines = file.readlines()
        # Filter out lines containing "api.vhsgame.com"
        lines = [line for line in lines if ".vhsgame.com" not in line]
        lines.append(f"{ip_address} api.vhsgame.com\n")
        lines.append(f"{ip_address} ns.vhsgame.com\n")
        lines.append(f"{ip_address} cdn.vhsgame.com\n")
        lines.append(f"{ip_address} mms.vhsgame.com\n")

        with open(hostsfile_path, 'w') as file:
            file.writelines(lines)
        print("Hosts file updated successfully.")

    except Exception as e:
        print("An error occurred:", str(e))
            
    root.destroy()

def read_last_ip_address():
    try:
        with open("ipcache.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        open("ipcache.txt", "w").close()
        return ""

if __name__ == "__main__":
    root = tk.Tk()
    root.title("VHS Server Coordinator")

    # Set window size and center the window on the screen
    window_width = 400
    window_height = 260  # Increased height to accommodate the image
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2  
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Prevent window resizings
    root.resizable(False, False)

    # Frame to contain all the widgets except the image
    content_frame = tk.Frame(root)
    content_frame.pack()  # Add 30 pixels of padding to the top of the frame

    # Load the banner image
    try:
        banner_photo = ImageTk.PhotoImage(Image.open("banner.png"))
        img_label = tk.Label(content_frame, image=banner_photo)
        img_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")  # Place the image at the top right
    except Exception as e:
        print("Issues printing banner, so skipped...")
        pass

    # Shared variable for the radio buttons
    selected_option = tk.StringVar(value="Host")

    # Radio buttons for "Host" and "Client"
    host_radio = tk.Radiobutton(content_frame, text="Host", variable=selected_option, value="Host", command=on_radio_selected)
    client_radio = tk.Radiobutton(content_frame, text="Client", variable=selected_option, value="Client", command=on_radio_selected)

    # Label and text entry widget for the client
    client_label = tk.Label(content_frame, text="IP Address:")
    client_entry = tk.Entry(content_frame, width=30, fg="black")

    # Read the last known IP Address and display it in the entry field
    last_ip_address = read_last_ip_address()
    client_entry.insert(0, last_ip_address)
    client_entry.config(state=tk.DISABLED)

    # Launch button
    launch_button = tk.Button(content_frame, text="Launch", command=launch_script)

    # Pack widgets inside the content frame
    host_radio.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    client_radio.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    client_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")  # Align label to the right (east)
    client_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")  # Align entry to the left (west)
    launch_button.grid(row=4, column=0, padx=5, pady=10, columnspan=2)

    root.bind("<Return>", on_enter_key)
    root.mainloop()
