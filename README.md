# VHS Redirector Scripts
_Scripts and GUIs to automate VHS Alternative Server. Needs Admin Privileges to run All scripts._

Download the most up to date scripts here: [Download Now](https://github.com/SkelXton/VHS-Redirector-Scripts/releases/download/v1.1/VHS_Server_Coordinator.exe)

**VHS Server Coordinator GUI:**
-------------------------------
A GUI interface to modify the hosts file quickly and efficiently when switching server settings. Select Main to launch from the main private server, Self-Host to connect to a server on the local network, and Remote Server to connect to a IP address you provide.

![Example GUI](https://github.com/SkelXton/VHS-Redirector-Scripts/assets/57548041/96478f3e-1c4b-48bc-a95b-fda5e5fcca94)


**Installer/Uninstaller for VHS Redirector:**
-------------------------------
Included are .bat scripts which will install and uninstall the certificate as needed automatically. In addition, the install script also sets up the hosts file to run a server locally on the system.
The install script must be run in the same directory as the certificate in order to work.

**Requirements for VHS Server Coordinator GUI:**
-------------------------------
The GUI was built on python 3.10.10, using the tkinter 8.6.12 and pillow 9.5.0 packages, and compiled into an executable using PyInstaller.
