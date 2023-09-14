import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import subprocess
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from certgen import genCert

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

# This is definitely bad practice, but Python was
# having some trouble reading a separate file for some reason.
# This is just a temporary solution :).
SAFETY_SCRIPT = "Although the risk of using this server is infintessimally small (>0.01%), we know that safety online is a top priority.\n\nIn an effort to make people both feel and be safer while using the server, we've compiled important tips for folks to know about, alongside official recommendations:\n\n1. Uninstall the server as soon as you log off.\n2. Play only with people you know and trust.\n3. Raise any security concerns with the developers of this tool via the Discord server.\n\nThe private server is made more secure by the private key (the server uses to confirm legitimacy via decrypting data encrypted from a public key) being stored in an offline storage medium. This means it cannot be compromised via the internet.\n\nSecurity is a top priority for us. If you have any additional concerns, feel free to raise them in the Discord!\n\n- The VHS: END Team"

def on_radio_selected():
    if selected_option.get() == "Client":
        client_entry.config(state=tk.NORMAL)
    else:
        client_entry.config(state=tk.DISABLED)

def on_enter_key(event):
    launch_script()

def read_last_ip_address():
    try:
        with open("ipcache.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        open("ipcache.txt", "w").close()
        return ""
    
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

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select a .crt File",
        filetypes=[("Certificate Files", "*.crt"), ("All Files", "*.*")]
    )
    
    if not file_path:
        messagebox.showwarning("Warning", "Please select a .crt file.")
        return

    return file_path

def extract_certificate_info(cert_path):
    try:
        with open(cert_path, "rb") as cert_file:
            cert_data = cert_file.read()
        
        certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
        serial_number = certificate.serial_number
        
        return serial_number, cert_data
    except Exception as e:
        messagebox.showerror("Error", f"Error extracting certificate info: {str(e)}")
        return None, None

def launch_script():
    global MAIN_IP

    is_error_free = True
    try:
        hostsfile_path = os.path.join(os.environ['windir'], 'System32', 'drivers', 'etc', 'hosts')
    except Exception as e:
        print("This is not a Windows environment. Testing with a local file \"hosts.txt\"")
        hostsfile_path = "hosts.txt"


    ip_address = "127.0.0.1"  # Set to localhost by default

    if selected_option.get() == "Host":
        print("Hello, World! - Host")
        private_key_path, certificate_path = genCert()

        # Display information in a dialog box
        messagebox.showinfo(
            "Certificate Information",
            f"Private Key Path: {private_key_path}\n"
            f"Certificate Path: {certificate_path}\n\n"
            "Please make sure to keep the private key secure and do not share it with anyone (Best practice, store it on an offline storage device).\n"
            "The certificate should be distributed to users who wish to connect to your server."
        )
        # Run the Server Executable
        try:
            if sys.platform == "win32":
                # Windows-specific code
                subprocess.run("vhs-server-win.exe", shell=True)
            elif sys.platform == "linux" or sys.platform == "linux2":
                # Linux-specific code
                subprocess.run("./vhs-server-linux", shell=True)
            else:
                print("Unsupported platform")
        except Exception as e:
            messagebox.showinfo("An error occurred:", str(e))
            is_error_free = False
    
    elif selected_option.get() == "Main":
        ip_address = MAIN_IP # Set to the main server
        print("Hello, World! - Main")

        # Check if the main server is online by pinging it.
        # If the ping fails, ask the user if they want to continue anyway but warn them that the server may be offline.
        try:
            subprocess.run(["ping", "-n", "1", "-w", "1000", MAIN_IP], check=True)
        except Exception as e:
            ping_response = messagebox.askquestion("Warning", f"The main server was unable to be pinged.\nThe server may be offline or your internet connection may be down.\n\nWould you like to continue anyway?")
            
            if ping_response == "no":
                return

        if not check_certificate():
            # Ask the user if they want to install the certificate
            response = messagebox.askquestion("Certificate Not Installed", "The required certificate is not installed. Do you want to install it now?")
            if response == "yes":
                install_certificate()
            else:
                return

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

            message = "Please locate the .crt file that you want to use for the client."
            messagebox.showinfo("Client Certificate Selection", message)
            client_input = open_file_dialog()  # Use the selected .crt file as the client input
            if not client_input:
                return  # User canceled the file selection
            
            CERTIFICATE_SERIAL, CERTIFICATE_DATA = extract_certificate_info(client_input)
            
            print("Serial Number: ", CERTIFICATE_SERIAL)
            print("\nCertificate Data: ", CERTIFICATE_DATA)

            if CERTIFICATE_SERIAL and CERTIFICATE_DATA:
                messagebox.showinfo("Success", "Certificate information extracted successfully. You can now proceed.")
            else:
                return           
            
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

# Display the safety info.
def safety_info_script():
    global SAFETY_SCRIPT
    messagebox.showinfo("Safety Tips for the Private Server", SAFETY_SCRIPT)

if __name__ == "__main__":
    WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
    root = tk.Tk()
    root.title("VHS Server Coordinator")
    root.iconbitmap(os.path.join(WORKING_DIR, r"END_ICON.ico"))

    # Set window size and center the window on the screen
    window_width = 420 
    window_height = 320
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
        img_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
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
    last_ip_address = read_last_ip_address()
    client_entry.insert(0, last_ip_address)
    client_entry.config(state=tk.DISABLED)

    # Button LabelFrame
    button_frame = tk.LabelFrame(content_frame)
    
    # Make button_frame borderless
    button_frame.config(borderwidth=0, highlightthickness=0)

    # Launch button
    launch_button = tk.Button(button_frame, text="Set Server", command=launch_script)
    safety_button = tk.Button(button_frame, text="Safety Notice", command=safety_info_script)
    uninstall_button = tk.Button(button_frame, text="Uninstall", command=uninstall_script)


    # Pack widgets inside the content frame
    main_radio.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    host_radio.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    client_radio.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    client_label.grid(row=3, column=1, padx=5, pady=5) #, sticky="e") 
    client_entry.grid(row=3, column=2, padx=5, pady=5 , sticky="w") 
    button_frame.grid(row=4, column=0, padx=5, pady=5, columnspan=3, sticky="nsw")

    launch_button.grid(row=4, column=0, padx=5, pady=10, columnspan=1, sticky="w")
    uninstall_button.grid(row=4, column=1, padx=5, pady=10, columnspan=1, sticky="s")
    safety_button.grid(row=4, column=2, padx=5, pady=10, columnspan=1, sticky="e")

    root.bind("<Return>", on_enter_key)
    root.mainloop()
    
    
