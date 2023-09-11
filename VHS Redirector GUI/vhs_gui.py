import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

MAIN_IP = "173.249.51.206"

CERTIFICATE_SERIAL = "7121d851d63039bd"
CERTIFICATE_DATA = """\
-----BEGIN CERTIFICATE-----
MIIEHDCCAwSgAwIBAgIIcSHYUdYwOb0wDQYJKoZIhvcNAQELBQAwgZMxCzAJBgNV
BAYTAkVTMQswCQYDVQQIEwJFUzEPMA0GA1UEBxMGTUFMQUdBMREwDwYDVQQKEwhM
dWlnaURldjERMA8GA1UECxMITHVpZ2lEZXYxFDASBgNVBAMMC0x1aWdpRGV2X0NB
MSowKAYJKoZIhvcNAQkBFhtsdWlzbWF5b3ZhbGJ1ZW5hQG91dGxvb2suZXMwHhcN
MjMwODAyMTA1ODAwWhcNMzMwODAyMTA1ODAwWjCBkzELMAkGA1UEBhMCRVMxCzAJ
BgNVBAgTAkVTMQ8wDQYDVQQHEwZNQUxBR0ExETAPBgNVBAoTCEx1aWdpRGV2MREw
DwYDVQQLEwhMdWlnaURldjEUMBIGA1UEAwwLTHVpZ2lEZXZfQ0ExKjAoBgkqhkiG
9w0BCQEWG2x1aXNtYXlvdmFsYnVlbmFAb3V0bG9vay5lczCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBALTnrf0bwtgLnlgqi/e5PgtYiwl0eprt5G3Dq4kc
hep83OIqBHj+eHtdBPZSpw71jYjDZMA1PrVZpc1pN8mLuKoY3TjwxUH/H1tZh3RF
DecDoY9o5ELE9AIhGlc842sF0WpPDCQzyMycj3WVC+ZYgz8ANC1hI/ee8jbGRRaJ
M56mSF1cVESGr63VIaULuc5YOcC0ZH3d74sqhDP/zJDNIe/IlJyMwVWkb/TWwZsp
i9zgZwBJFwFwUUr8UIgYQEYgZ48saj6tMgXO3k7Nlp+0lS6GUDMWlmCJPvSCkn9O
F8zEc4v0rGN3m6E4FEmOf+l3M+r0VU1EDxaVAZj7FZDAB1ECAwEAAaNyMHAwDwYD
VR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQU2wyzNbwNsvkNvlt95LoiR7IXgY4wCwYD
VR0PBAQDAgEGMBEGCWCGSAGG+EIBAQQEAwIABzAeBglghkgBhvhCAQ0EERYPeGNh
IGNlcnRpZmljYXRlMA0GCSqGSIb3DQEBCwUAA4IBAQBO9D7AReyNaZYK4MEi5ic1
RUg/zX/E6IbJDRAnxNRxvzz6XWNSjID4SwEbuBvspNlkeuIUXDj2Osz9NRTkwIS7
p9u71bWSPF0ybYQH+SaawxyY6ovrvMJK2UboyfUokJjpGX0AZPmmOX7rVW88T1DC
u6dAKxR9i1SWQNb/RfSosW0ymgeXsFbqlVKSosBK/BL6644JBc8VCMbPO5WO5PN/
eyMXNIKeaL4USPqwMCn7MusQEQYVe2uGuxdSa+vHPqU4tlRyIOQmWVOnb+No8YUl
iq5VP6suaMEYdCpHUYAza/FelsGb7qsdtR5S739btFo9jAWi1J+HX9PKHdFeEPXg
-----END CERTIFICATE-----
    """

def on_radio_selected():
    if selected_option.get() == "Client":
        client_entry.config(state=tk.NORMAL)
    else:
        client_entry.config(state=tk.DISABLED)

def on_enter_key(event):
    launch_script()

def read_last_ip_address():
    pass
    # try:
    #     with open("ipcache.txt", "r") as file:
    #         return file.read().strip()
    # except FileNotFoundError:
    #     open("ipcache.txt", "w").close()
    #     return ""
    
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
    global CERTIFICATE_DATA
    try:
        certificate_filename = "VHS_Redirection_Certificate.crt"
        if not os.path.isfile(certificate_filename):
            with open(certificate_filename, "w") as cert_file:
                cert_file.write(CERTIFICATE_DATA)

        subprocess.run(['certutil', '-addstore', 'Root', certificate_filename], check=True)
        messagebox.showinfo("Success", "Certificate installed successfully. You can now proceed.")
        # Remove the certificate once installed successfully
        if os.path.exists(certificate_filename):
            os.remove(certificate_filename)

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

def uninstall_script():
    response = messagebox.askquestion("Warning", "Are you sure you want to uninstall?")
    if response == "no":
        return
    
    try:
        hostsfile_path = os.path.join(os.environ['windir'], 'System32', 'drivers', 'etc', 'hosts')
        print(hostsfile_path)
    except Exception as e:
        print("This is not a Windows environment. Testing with a local file \"hosts.txt\"")
        hostsfile_path = "hosts.txt"

    try: 
        with open(hostsfile_path, 'r') as file:
            lines = file.readlines()
        
        # Filter out lines containing "api.vhsgame.com"
        lines = [line for line in lines if ".vhsgame.com" not in line]

        with open(hostsfile_path, 'w') as file:
            file.writelines(lines)
        print("Hosts file updated successfully.")

    except Exception as e:
        messagebox.showinfo("An error occurred:", str(e))
    
    try:
        subprocess.run(['certutil', '-delstore', 'Root', CERTIFICATE_SERIAL], check=True)
        messagebox.showinfo("Success", "Hosts file edits and Certificates uninstalled successfully. Be sure to double check!")
    except Exception as e:
        messagebox.showerror("Error", f"Error uninstalling the certificate: {str(e)}")
        
    root.destroy()

if __name__ == "__main__":
    WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
    root = tk.Tk()
    root.title("VHS Server Coordinator")
    global WIDTH, HEIGHT

    # Set window size and center the window on the screen
    window_width = 220 
    window_height = 200
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
        img_path = os.path.join(WORKING_DIR, "banner.png")
        banner_photo = ImageTk.PhotoImage(Image.open(img_path))
        img_label = tk.Label(content_frame, image=banner_photo)
        img_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    except Exception as e:
        print("Exception: ", e)
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
    # last_ip_address = read_last_ip_address()
    # client_entry.insert(0, last_ip_address)
    # client_entry.config(state=tk.DISABLED)

    # Launch button
    launch_button = tk.Button(content_frame, text="Set Server", command=launch_script)
    uninstall_button = tk.Button(content_frame, text="Uninstall", command=uninstall_script)

    # Pack widgets inside the content frame
    # Commenting this out as this functionality is incomplete and needs to be addressed

    # main_radio.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    # host_radio.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    # client_radio.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    # client_label.grid(row=4, column=0, padx=5, pady=5) #, sticky="e") 
    # client_entry.grid(row=4, column=1, padx=5, pady=5 , sticky="w") 

    launch_button.grid(row=3, column=0, padx=5, pady=10, columnspan=1)
    uninstall_button.grid(row=3, column=1, padx=5, pady=10, columnspan=1)

    root.bind("<Return>", on_enter_key)
    root.mainloop()
    
    
