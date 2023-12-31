import os
import sys
import ctypes
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import subprocess
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from certgen import genCert

MAIN_IP = "173.249.51.206"

CERTIFICATE_SERIAL = "454e1e3b62e6c326"
CERTIFICATE_DATA = """\
-----BEGIN CERTIFICATE-----
MIIERTCCAy2gAwIBAgIIRU4eO2LmwyYwDQYJKoZIhvcNAQELBQAwgZcxCzAJBgNV
BAYTAkVTMQswCQYDVQQIEwJFUzEPMA0GA1UEBxMGTUFMQUdBMREwDwYDVQQKEwhM
dWlnaURldjERMA8GA1UECxMITHVpZ2lEZXYxGDAWBgNVBAMTD0x1aWdpRGV2VkhT
Q0F2MjEqMCgGCSqGSIb3DQEJARYbbHVpc21heW92YWxidWVuYUBvdXRsb29rLmVz
MB4XDTIzMDgwMjEwNTgwMFoXDTMzMDgwMjEwNTgwMFowgZcxCzAJBgNVBAYTAkVT
MQswCQYDVQQIEwJFUzEPMA0GA1UEBxMGTUFMQUdBMREwDwYDVQQKEwhMdWlnaURl
djERMA8GA1UECxMITHVpZ2lEZXYxGDAWBgNVBAMTD0x1aWdpRGV2VkhTQ0F2MjEq
MCgGCSqGSIb3DQEJARYbbHVpc21heW92YWxidWVuYUBvdXRsb29rLmVzMIIBIjAN
BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1sEt+Q53gVvCDkKGexClF1B8Kc8k
JR9G4onIsoHJBGKk72HaC9YTzXPyX9cjBSuftIdFOQijERzQVlWoqkdShs1DmPfV
I2QqhyyBozV9sFOZ3gGVhE+POZ1YUIDl8OL8SdVhlMQyGh78n/BRKkZ/P+jACH7+
XRpRahGsMIIsRLkP6q3tN1NeW+gGWurja6C/edrKxQz64gBU7QVpmwoS3vK60gQk
AnMO6AOcIv/tnI3KXnRb2R/uBAUg20CcxjtmQ6jqV77TWby40jRmT8H1s2HoENF6
ZwLZFzGQnajtMwCURYWU2wjQ6zNnPjqtNQAGsZ87XUTmXxjBEjbBmJhQQwIDAQAB
o4GSMIGPMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFF2V6FUwNWjn3AYIWig5
ahcyFf0hMAsGA1UdDwQEAwIBBjAdBgNVHR4BAf8EEzARoA8wDYILdmhzZ2FtZS5j
b20wEQYJYIZIAYb4QgEBBAQDAgAHMB4GCWCGSAGG+EIBDQQRFg94Y2EgY2VydGlm
aWNhdGUwDQYJKoZIhvcNAQELBQADggEBALRdSIQmuI+e2sF9JuFyoaawkaMS6ukc
wP19qDJY2T2N56PYXfd8wBNJzRgW/Mu0NzQUEOx+ETY21wkAFbNYU2pdeKUY5N6X
f3jNBkrw9O7kYbwFPHHwD/AmAZ83m2rZABRSRVur+lNLFU/I5TSjWsazR+T8vgyO
Qox4UNjExwiOh6oWgGquyTDSKWNIRx1LJrrWCctVZ/WL0s0LSKmkZZCXffBrS3yp
eikakSOtIy5IxufBiZHjRVHNixXeIkSdR9cArPwzkAD8wB/p2dIiCMRIcVlDPJow
FeWkBlpUfYAkt7oEQd93O2mLRcSDkAMqA2QbTT2puv7T//JSvyBlXz8=
-----END CERTIFICATE-----
"""

# This is definitely bad practice, but Python was
# having some trouble reading a separate file for some reason.
# This is just a temporary solution :).
SAFETY_SCRIPT = """Although the risk of using this server is infintessimally small (>0.01%), we know that safety online is a top priority.

In an effort to make people both feel and be safer while using the server, we've compiled important tips for folks to know about, alongside official recommendations:

1. Uninstall the server as soon as you log off.
2. Play only with people you know and trust.
3. Raise any security concerns with the developers of this tool via the Discord server.

The private server is made more secure by the private key (the server uses to confirm legitimacy via decrypting data encrypted from a public key) being stored in an offline storage medium. 
This means it cannot be compromised via the internet.

Security is a top priority for us. If you have any additional concerns, feel free to raise them in the Discord!

- The VHS: END Team"""

# Bad practice continued lol
ADMIN_MESSAGE = """In order to setup the server, you will need to run this program as administrator to make the needed changes. 

If you have any concerns with this program, please refer to the GitHub repo which can be found in the discord server or below.

https://github.com/SkelXton/VHS-Redirector-Scripts
"""

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

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

        # Doesn't work for the time being...
        # # Run the Server Executable
        # try:
        #     if sys.platform == "win32":
        #         # Windows-specific code
        #         subprocess.run("vhs-server-win.exe", shell=True)
        #     elif sys.platform == "linux" or sys.platform == "linux2":
        #         # Linux-specific code
        #         subprocess.run("./vhs-server-linux", shell=True)
        #     else:
        #         print("Unsupported platform")
        # except Exception as e:
        #     messagebox.showinfo("An error occurred:", str(e))
        #     is_error_free = False
    
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
    if is_admin():
        WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
        root = tk.Tk()
        root.title("VHS Server Coordinator")
        try:
            root.iconbitmap(os.path.join(WORKING_DIR, r"END_ICON.ico"))
        except Exception as e:
            print("Exception: ", e)
            print("Issues using icon, so skipped...")
            pass
        
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
        # TBA on Host once tutorial for setting up server tutorial is done
        # host_radio = tk.Radiobutton(content_frame, text="Self-Host", variable=selected_option, value="Host", command=on_radio_selected)
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
        # TBA on Host once tutorial for setting up server tutorial is done
        # host_radio.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        client_radio.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        client_label.grid(row=3, column=1, padx=5, pady=5) #, sticky="e") 
        client_entry.grid(row=3, column=2, padx=5, pady=5 , sticky="w") 
        button_frame.grid(row=4, column=0, padx=5, pady=5, columnspan=3, sticky="nsw")
    
        launch_button.grid(row=4, column=0, padx=5, pady=10, columnspan=1, sticky="w")
        uninstall_button.grid(row=4, column=1, padx=5, pady=10, columnspan=1, sticky="s")
        safety_button.grid(row=4, column=2, padx=5, pady=10, columnspan=1, sticky="e")
    
        root.bind("<Return>", on_enter_key)
        root.mainloop()
    else:
        ctypes.windll.user32.MessageBoxW(0, ADMIN_MESSAGE, "Admin Privileges Required", 0x30)
        run_as_admin()

