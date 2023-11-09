import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import configparser
import os
import sys
import requests
import zipfile
import psutil
import shutil
import ctypes
import webbrowser
import time
import json

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if sys.platform != 'win32':
        return

    try:
        ASADMIN = 'asadmin'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ASADMIN, None, 1)
    except Exception as e:
        print("Failed to run as admin:", e)
        sys.exit(1)

if not is_admin():
    run_as_admin()
    sys.exit(0)


running = True
running2 = True

current_version = 0 
latest_version = 0 


def update_version():
    global latest_version
    global running

    while running:
        # Make a request to the API to check for a new release
        url = "https://api.steamcmd.net/v1/info/2662210"
        response = requests.get(url)
        data = response.json()

        # Get the latest version
        latest_version = data["data"]["2662210"]["_change_number"]
        latest_version_label.config(text=str(latest_version))

        # Wait for 300 seconds before making the next request
        time.sleep(300)

def check_version():
    global running2
    while running2:
    # Check if the latest version is different from the current version
        if str(latest_version) != str(current_version):
            status_label.config(text="New version available.", fg="red")
        else:
            status_label.config(text="No new version available.", fg="black")
        root.update()
    # Wait for 1 second before checking again
    time.sleep(2)



def start_updating():
    global running
    running = True
    global running2
    running2 = True
    update_thread = threading.Thread(target=update_version, daemon=True)
    check_thread = threading.Thread(target=check_version, daemon=True)
    update_thread.start()
    check_thread.start()

def stop_updating():
    global running
    running = False
    global running2
    running2 = False	


def update_vs():
    global current_version

    try:
        config = configparser.ConfigParser()
        config.read('conf.ini')


        config.set('Server', 'latest_version', str(latest_version))
        

        with open('conf.ini', 'w') as configfile:
            config.write(configfile)

        current_version = latest_version
        current_version_label.config(text=str(current_version))

    except Exception as e:
        current_version = 0
        current_version_label.config(text=str(current_version))



def download_steamcmd():

    nssm_url = 'https://nssm.cc/release/nssm-2.24.zip'
    r = requests.get(nssm_url)
    with open("nssm-2.24.zip", "wb") as code:
        code.write(r.content)

    fantasy_zip = zipfile.ZipFile('nssm-2.24.zip')
    fantasy_zip.extractall('')
    fantasy_zip.close()
    shutil.copy('nssm-2.24/win64/nssm.exe', '.')
    if os.path.exists('nssm-2.24.zip'):
        os.remove('nssm-2.24.zip')
    if os.path.exists('nssm-2.24'):
        shutil.rmtree('nssm-2.24')

        
    steamcmd_url = 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip'
    r = requests.get(steamcmd_url)
    with open("steamcmd.zip", "wb") as code:
        code.write(r.content)
    fantasy_zip = zipfile.ZipFile('steamcmd.zip')
    fantasy_zip.extractall('steamcmd')
    fantasy_zip.close()
    os.remove("steamcmd.zip")

    command = 'steamcmd/steamcmd.exe'
    args = [
        '+login', 'anonymous',
        '+force_install_dir', '..\\Astro_Colony',  
        '+app_update', '2662210', 'validate', '+quit'  
    ]
    subprocess.Popen([command] + args, cwd='steamcmd')
    update_vs()


def download_astro_colony():

    command = 'steamcmd/steamcmd.exe'
    args = [
        '+login', 'anonymous',
        '+force_install_dir', '..\\Astro_Colony',  
        '+app_update', '2662210', 'validate', '+quit'  
    ]
    subprocess.Popen([command] + args, cwd='steamcmd')
    update_vs()


def kill_server_process():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if 'AstroColonyServer.exe' in process.info['name']:
            try:
                psutil.Process(process.info['pid']).terminate()
            except psutil.NoSuchProcess:
                pass

def open_ports(query_port):
    cmd_command = f'powershell.exe New-NetFirewallRule -DisplayName "Allow-AstroColony-UDP-Port" -Direction Inbound -Action Allow -EdgeTraversalPolicy Allow -Protocol UDP -LocalPort {query_port},7777'
    os.system(f'cmd /C "{cmd_command} & timeout 5 & exit"')




def on_install_service(server_name, query_port):
    cmd_command = f'nssm.exe install AstroColonyServerService %CD%\\Astro_Colony\\AstroColonyServer.exe -SteamServerName={server_name} -QueryPort={query_port}'
    os.system(f'cmd /C "{cmd_command} & timeout 3"')
    save_configs()




def on_start_service():
    cmd_command = 'nssm.exe start AstroColonyServerService'
    os.system(f'cmd /C "{cmd_command} & timeout 3"')


def on_stop_service():
    cmd_command = 'nssm.exe stop AstroColonyServerService'
    os.system(f'cmd /C "{cmd_command} & timeout 3"')

def on_delete_service():
    cmd_command = 'nssm.exe remove AstroColonyServerService'
    os.system(f'cmd /C "{cmd_command} & timeout 3"')

def on_open_guide():
    url = "https://bit.ly/AstroColonyDedicatedDoc"
    webbrowser.open(url)

def save_configs():
    server_name = server_name_entry.get()
    query_port = query_port_entry.get()
    log_enabled = log_var.get()
    server_password = server_password_entry.get()
    seed = seed_entry.get()
    map_name = map_name_entry.get()
    max_players = max_players_entry.get()
    savegame_name = savegame_name_entry.get()
    should_load_latest_savegame = load_latest_savegame_var.get()
    admin_list = admin_list_entry.get()
    shared_technologies = shared_technologies_var.get()
    oxygen_consumption = oxygen_consumption_var.get()
    free_construction = free_construction_var.get()

    config = configparser.ConfigParser()
    config.read('conf.ini')

    try:
        config['Server']['SteamServerName'] = server_name
        config['Server']['QueryPort'] = query_port
        config['Server']['LogEnabled'] = str(log_enabled)


        with open('conf.ini', 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        pass

    with open('Astro_Colony/AstroColony/Saved/Config/WindowsServer/ServerSettings.ini', 'w') as server_settings_file:
        server_settings_file.write('[/Script/AstroColony.EHServerSubsystem]\n')
        server_settings_file.write(f'ServerPassword={server_password}\n')
        server_settings_file.write(f'Seed={seed}\n')
        server_settings_file.write(f'MapName={map_name}\n')
        server_settings_file.write(f'MaxPlayers={max_players}\n')
        server_settings_file.write(f'SavegameName={savegame_name}\n')
        server_settings_file.write(f'ShouldLoadLatestSavegame={should_load_latest_savegame}\n')
        server_settings_file.write(f'AdminList={admin_list}\n')
        server_settings_file.write(f'SharedTechnologies={shared_technologies}\n')
        server_settings_file.write(f'OxygenConsumption={oxygen_consumption}\n')
        server_settings_file.write(f'FreeConstruction={free_construction}\n')


def create_server():
    server_name = server_name_entry.get()
    query_port = query_port_entry.get()
    server_command = f'Astro_Colony\\AstroColonyServer.exe -SteamServerName={server_name} -QueryPort={query_port}'
    if log_var.get():
        server_command += ' -log'
    subprocess.Popen(server_command, shell=True, close_fds=True)
    save_configs()



def load_server_settings():
    server_settings = configparser.ConfigParser()

    server_settings_file_path = 'Astro_Colony/AstroColony/Saved/Config/WindowsServer/ServerSettings.ini'

    if not os.path.exists(server_settings_file_path):
        os.makedirs("Astro_Colony/AstroColony/Saved/Config/WindowsServer/")
        with open(server_settings_file_path, 'w') as server_settings_file:
            server_settings_file.write('[/Script/AstroColony.EHServerSubsystem]\n')
            server_settings_file.write('ServerPassword=\n')
            server_settings_file.write('Seed=\n')
            server_settings_file.write('MapName=SuperName\n')
            server_settings_file.write('MaxPlayers=5\n')
            server_settings_file.write('SavegameName=\n')
            server_settings_file.write('ShouldLoadLatestSavegame=False\n')
            server_settings_file.write('AdminList=\n')
            server_settings_file.write('SharedTechnologies=False\n')
            server_settings_file.write('OxygenConsumption=False\n')
            server_settings_file.write('FreeConstruction=False\n')

    server_settings.read('Astro_Colony/AstroColony/Saved/Config/WindowsServer/ServerSettings.ini')

    return server_settings

def load_settings_into_fields():
    server_settings = load_server_settings()

    server_password_entry.insert(0, server_settings.get('/Script/AstroColony.EHServerSubsystem', 'ServerPassword'))
    seed_entry.insert(0, server_settings.get('/Script/AstroColony.EHServerSubsystem', 'Seed'))
    map_name_entry.insert(0, server_settings.get('/Script/AstroColony.EHServerSubsystem', 'MapName'))
    max_players_entry.insert(0, server_settings.get('/Script/AstroColony.EHServerSubsystem', 'MaxPlayers'))
    savegame_name_entry.insert(0, server_settings.get('/Script/AstroColony.EHServerSubsystem', 'SavegameName'))
    load_latest_savegame_var.set(server_settings.getboolean('/Script/AstroColony.EHServerSubsystem', 'ShouldLoadLatestSavegame'))
    admin_list_entry.insert(0, server_settings.get('/Script/AstroColony.EHServerSubsystem', 'AdminList'))
    shared_technologies_var.set(server_settings.getboolean('/Script/AstroColony.EHServerSubsystem', 'SharedTechnologies'))
    oxygen_consumption_var.set(server_settings.getboolean('/Script/AstroColony.EHServerSubsystem', 'OxygenConsumption'))
    free_construction_var.set(server_settings.getboolean('/Script/AstroColony.EHServerSubsystem', 'FreeConstruction'))





root = tk.Tk()
root.title("Astro Colony Server Manager")
root.geometry("550x490")
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=(35, 30), pady=5)



server_name_label = tk.Label(left_frame, text="Server Name:")
server_name_label.pack()
server_name_entry = tk.Entry(left_frame)
server_name_entry.pack()



query_port_label = tk.Label(left_frame, text="Query Port:")
query_port_label.pack()
config = configparser.ConfigParser()
if config.read('conf.ini'):
    query_port = ()
else:
    query_port = 27015 

query_port_entry = tk.Entry(left_frame)
query_port_entry.insert(0, query_port)
query_port_entry.pack()




log_var = tk.BooleanVar()
log_checkbutton = tk.Checkbutton(left_frame, text="Enable Logging and Console", variable=log_var)
log_checkbutton.pack()
log_checkbutton.config(variable=log_var)

download_steamcmd_button = tk.Button(left_frame, text="Download SteamCMD & Install", command=download_steamcmd)
download_steamcmd_button.pack()

download_astro_colony_button = tk.Button(left_frame, text="Download Astro Colony and Update", command=download_astro_colony)
download_astro_colony_button.pack()

create_server_button = tk.Button(left_frame, text="Start Server", command=create_server)
create_server_button.pack()

kill_server_button = tk.Button(left_frame, text="Close process AstroColonyServer", command=kill_server_process)
kill_server_button.pack()

Install_service_button = tk.Button(left_frame, text="Install Service", command=lambda: on_install_service(server_name_entry.get(), query_port_entry.get()))
Install_service_button.pack()
start_service_button = tk.Button(left_frame, text="Start Service", command=on_start_service)
start_service_button.pack()
stop_server_button = tk.Button(left_frame, text="Stop Service", command=on_stop_service)
stop_server_button.pack()
delete_server_button = tk.Button(left_frame, text="Delete Service", command=on_delete_service)
delete_server_button.pack()



open_ports_button = tk.Button(left_frame, text="Open UDP Ports", command=lambda: open_ports(int(query_port_entry.get())))
open_ports_button.pack()


on_open_guide = tk.Button(left_frame, text="Open Guide page", command=on_open_guide)
on_open_guide.pack()

try:
    config = configparser.ConfigParser()
    config.read('conf.ini')
    current_version = int(config.get('Server', 'latest_version'))
except Exception as e:
    current_version = "0"
    print(e)


currentt_version_label = tk.Label(left_frame, text="Current version")
currentt_version_label.pack()
# Create labels to display the current version and the latest version
current_version_label = tk.Label(left_frame, text=current_version)
current_version_label.pack()

latestt_version_label = tk.Label(left_frame, text="Latest version")
latestt_version_label.pack()
latest_version_label = tk.Label(left_frame, text="Checking for updates...")
latest_version_label.pack()

# Create a label to display the status of the update
status_label = tk.Label(left_frame, text="")
status_label.pack()


right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=5)
separator = tk.Frame(root, width=2, bd=1, relief=tk.SUNKEN)
separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)

windos2_label = tk.Label(right_frame, text="Config ServerSettings.ini", font=("Helvetica", 12, "bold"), foreground="gray")
windos2_label.pack(pady=10)




server_password_label = tk.Label(right_frame, text="Server Password:")
server_password_label.pack()
server_password_entry = tk.Entry(right_frame)
server_password_entry.pack()

seed_label = tk.Label(right_frame, text="Seed:")
seed_label.pack()
seed_entry = tk.Entry(right_frame)
seed_entry.pack()

map_name_label = tk.Label(right_frame, text="Map Name:")
map_name_label.pack()
map_name_entry = tk.Entry(right_frame)
map_name_entry.pack()

max_players_label = tk.Label(right_frame, text="Max Players:")
max_players_label.pack()
max_players_entry = tk.Entry(right_frame)
max_players_entry.pack()

savegame_name_label = tk.Label(right_frame, text="Savegame Name:")
savegame_name_label.pack()
savegame_name_entry = tk.Entry(right_frame)
savegame_name_entry.pack()

load_latest_savegame_var = tk.BooleanVar()
load_latest_savegame_checkbutton = tk.Checkbutton(right_frame, text="Should Load Latest Savegame", variable=load_latest_savegame_var)
load_latest_savegame_checkbutton.pack()

admin_list_label = tk.Label(right_frame, text="Admin List (Steam PlayerIDs, comma separated):")
admin_list_label.pack()
admin_list_entry = tk.Entry(right_frame)
admin_list_entry.pack()

shared_technologies_var = tk.BooleanVar()
shared_technologies_checkbutton = tk.Checkbutton(right_frame, text="Shared Technologies", variable=shared_technologies_var)
shared_technologies_checkbutton.pack()

oxygen_consumption_var = tk.BooleanVar()
oxygen_consumption_checkbutton = tk.Checkbutton(right_frame, text="Oxygen Consumption", variable=oxygen_consumption_var)
oxygen_consumption_checkbutton.pack()

free_construction_var = tk.BooleanVar()
free_construction_checkbutton = tk.Checkbutton(right_frame, text="Free Construction", variable=free_construction_var)
free_construction_checkbutton.pack()







config = configparser.ConfigParser()
if not config.read('conf.ini'):
    config['Server'] = {
        'SteamServerName': '',
        'QueryPort': '',
        'LogEnabled': False,
        'latest_version': 0,
    }

    with open('conf.ini', 'w') as configfile:
        config.write(configfile)

server_name_entry.insert(0, config.get('Server', 'SteamServerName'))
query_port_entry.insert(0, config.get('Server', 'QueryPort'))
log_var.set(config.getboolean('Server', 'LogEnabled'))


    
start_updating()

load_settings_into_fields()
root.protocol("WM_DELETE_WINDOW", lambda: (stop_updating(), root.destroy()))

root.mainloop()
