import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

MAIN_IP = "173.249.51.206"
CERTIFICATE_SERIAL = "7121d851d63039bd"

def on_radio_selected():
    if selected_option.get() == "Client":
        client_entry.config(state=tk.NORMAL)
    else:
        client_entry.config(state=tk.DISABLED)

def on_enter_key(event):
    launch_script()

def check_certificate():
    global CERTIFICATE_SERIAL
    # Check if the certificate is installed in the Trusted Root store
    try:
        certutil_output = subprocess.check_output(["certutil", "-verifystore", "Root"], stderr=subprocess.STDOUT, text=True)
        if CERTIFICATE_SERIAL in certutil_output:
            print("Certificate is already installed.")
            return True
        print("Certificate is not installed.")
        return False
    except Exception as e:
        print("Error checking/installing certificate:", str(e))
        return False
        
    return True

def install_certificate():
    try:
        install_script = os.getcwd() + "install_VHS_Redirect.bat"
        subprocess.run([install_script], shell=True)
        messagebox.showinfo("Success", "Certificate installed successfully. You can now proceed.")
    except Exception as e:
        messagebox.showerror("Error", f"Error installing the certificate: {str(e)}")
        root.destroy()

def launch_script():
    global MAIN_IP
    is_error_free = True
    try:
        hostsfile_path = os.path.join(os.environ['windir'], 'System32', 'drivers', 'etc', 'hosts')
    except Exception as e:
        print("This is not a Windows environment. Testing with a local file \"hosts.txt\"")
        hostsfile_path = "hosts.txt"
    ip_address = "127.0.0.1" # Set to localhost by default

    if selected_option.get() == "Host":
        print("Hello, World! - Host")
    
    elif selected_option.get() == "Main":
        ip_address = MAIN_IP # Set to the main server
        print("Hello, World! - Main")

    elif selected_option.get() == "Client":
        client_input = client_entry.get()
        if not client_input.strip():
            messagebox.showwarning("Warning", "Please enter an address for the client.")
            return
        else:
            ip_address = client_input
            # Write IP address input to the cache file
            with open("ipcache.txt", "w") as file:
                file.write(ip_address)
            print(f"Hello, World! - Client: {ip_address}")
    
    if not check_certificate():
        # Ask the user if they want to install the certificate
        response = messagebox.askquestion("Certificate Not Installed", "The required certificate is not installed. Do you want to install it now?")
        if response == "yes":
            install_certificate()
        else:
            return
    
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
        messagebox.showinfo("An error occurred:", str(e))
        is_error_free = False

    if is_error_free:
        messagebox.showinfo("Success", "Server set successfully!")

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

    # Prevent window resizing
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
    selected_option = tk.StringVar(value="Main")

    # Radio buttons for "Main", "Host", and "Client"
    main_radio = tk.Radiobutton(content_frame, text="Main Server", variable=selected_option, value="Main", command=on_radio_selected)
    host_radio = tk.Radiobutton(content_frame, text="Self-Host", variable=selected_option, value="Host", command=on_radio_selected)
    client_radio = tk.Radiobutton(content_frame, text="Remote Server", variable=selected_option, value="Client", command=on_radio_selected)

    # Label and text entry widget for the client
    client_label = tk.Label(content_frame, text="IP Address:")
    client_entry = tk.Entry(content_frame, width=30, fg="black")

    # Read the last known IP Address and display it in the entry field
    last_ip_address = read_last_ip_address()
    client_entry.insert(0, last_ip_address)
    client_entry.config(state=tk.DISABLED)

    # Launch button
    launch_button = tk.Button(content_frame, text="Set Server", command=launch_script)

    # Pack widgets inside the content frame
    main_radio.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    host_radio.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    client_radio.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    client_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")  # Align label to the right (east)
    client_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")  # Align entry to the left (west
    launch_button.grid(row=5, column=0, padx=5, pady=10, columnspan=2)

    root.bind("<Return>", on_enter_key)
    root.mainloop()
    
    
