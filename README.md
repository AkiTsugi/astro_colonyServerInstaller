# astro_colonyServerInstaller

**Here's what it can do for the user:**

`Download SteamCMD:` Allows the user to download SteamCMD, a command-line tool used to download and update the Astro Colony server files.

`Download Astro Colony:` Downloads and updates the Astro Colony server files using SteamCMD.

`Start Server:` Initiates the Astro Colony server with the specified configuration settings.

`Close Server Process:` Terminates the Astro Colony server process to stop the server.

`Install Service:` Installs Astro Colony as a Windows service for easier management (with the specified configuration settings).

`Start Service:` Starts the installed Astro Colony server service (If you have modified server settings such as its name and port, you need to recreate the service and start the server using [Start Server] in order for all the settings to be saved.).

`Stop Service:` Stops the running Astro Colony server service.

`Delete Service:` Removes the Astro Colony server service.

`Open UDP Ports:` Opens the required UDP ports for the server to function correctly.

`Open Guide Page:` Opens a web page with a guide for setting up and configuring the dedicated Astro Colony server.

`Configure Server Settings:` Allows the user to configure various server settings, including server name, query port, server password, seed, map name, max players, savegame name, and gameplay options like shared technologies, oxygen consumption, and free construction.

The program provides a convenient way for users to manage and configure their Astro Colony servers with minimal manual command-line interaction. It simplifies the process of setting up and running a dedicated server for the game.




---
After clicking on (Start server), the data (Server name) and (Query Port), the state of the Logging checkbox and others are saved in the conf.ini & ServerSettings.ini files, and then it is stored for future launches.

![image](https://github.com/asidsx/astro_colonyServerInstaller/assets/106923482/90e60f6a-58db-4540-8a2c-250fd6a6f1ea)





```
pip install requests
pip install psutil
pip install pyinstaller
```
```
pyinstaller astroserverinstaller.py --onefile --noconsole
```

Or simply take the already compiled program https://github.com/asidsx/astro_colonyServerInstaller/releases.

all files

![image](https://github.com/asidsx/astro_colonyServerInstaller/assets/106923482/f261d868-b55b-4311-96aa-11575cb2dc3b)
