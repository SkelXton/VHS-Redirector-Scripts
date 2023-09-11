# VHS Redirector Scripts
_Scripts and GUIs to automate VHS Alternative Server. Needs Admin Privileges to run All scripts._


**VHS Server Coordinator GUI:**
-------------------------------
A GUI interface to modify the hosts file quickly and efficiently when switching server settings. Select Main to launch from the main private server, Self-Host to connect to a server on the local network, and Remote Server to connect to a IP address you provide.

All code can be found in vhs_gui.py if you are curious about how the program works. Everything else is just a wrapper or asset.

![GUI](https://github.com/SkelXton/VHS-Redirector-Scripts/assets/57548041/41dcad5b-2ee6-40f0-a2f8-7581f9559964)


**How to Install VHS Server Redirector:**
-------------------------------
Download the most up-to-date release here: [Download Now](https://github.com/SkelXton/VHS-Redirector-Scripts/releases/download/initial_release/VHS_Server_Coordinator.exe)

Functionality is built into the app, but if you want to build from source, you can do so using this command within autopy-to-exe or pyinstaller through the terminal:
```
pyinstaller --noconfirm --onefile --windowed --icon "[PATH TO BUILD FOLDER]/VHS-Redirector-Scripts-main/VHS Redirector GUI/toolbar_icon.ico" --add-data "[PATH TO BUILD FOLDER]/VHS-Redirector-Scripts-main/VHS Redirector GUI/banner.png;."  "[PATH TO BUILD FOLDER]/VHS-Redirector-Scripts-main/VHS Redirector GUI/vhs_gui.py"
```

**Requirements for Compiling VHS Server Coordinator GUI:**
-------------------------------
The GUI was built on Python 3.10.10, using the tkinter 8.6.12 and pillow 9.5.0 packages, and compiled into an executable using PyInstaller (Autopy-to-exe).
