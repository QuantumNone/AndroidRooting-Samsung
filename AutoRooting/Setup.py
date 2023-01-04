import Scripts.AutoRootUtilities as rutil

#We start by checking everything is configured correctly OK

mode = rutil.getPlatform()

if mode == 1:
    print("Detected a Windows system")
elif mode == 2:
    print("Detected a Linux system")

if not rutil.getDiskSpace() > 8589934592:
    raise SystemExit("Less than 8GiB of disk space is available, setup cannot continue.")

if not rutil.isElevated():
    raise SystemExit("This Script requires elevated Priviledges, Execution cannot continue.")

if not rutil.isConnected():
    raise SystemExit("Could not connect to the Internet, or could not resolve DNS. Check your Internet.")

resumeSetup = False

if not rutil.isSetup():
    if mode == 1:
        if not rutil.checkTool("wsl"):
            raise SystemExit("This tool requires WSL2 to be installed in order to patch magisk boot images with docker. WSL2 can be installed on all versions of Windows starting with Windows 10 2004 and all releases of Windows 11. For more information, see https://aka.ms/wsl")
        if rutil.os.path.isfile("Tools\\inprogress.cfg"):
            print("Resuming setup")
            resumeSetup = True
        if rutil.checkTool("adb") or rutil.checkTool("fastboot"):
            raise SystemExit("ADB or Fastboot are already in Path. This will conflict with the installed version, which will install the latest version of platform-tools into path. Please remove the offending programs and re-run Setup.")
        if not resumeSetup:
            print("Checks Complete, Detected first run or configuration removed.")
            print("Welcome to Setup.py, this setup file will install google's platform-tools and docker, then will spawn a docker container to patch boot images for magisk.")
            if (not rutil.askUser("Is this alright?")):
                raise SystemExit("User refused setup, exiting.")
            else:
                print("Preparing File Structure.")
                try: 
                    rutil.os.mkdir("Tools")
                except FileExistsError:
                    pass
                try: 
                    rutil.os.mkdir("Tools\\magiskDocker")
                except FileExistsError:
                    pass 
                try: 
                    rutil.os.mkdir("Downloads")
                except FileExistsError:
                    pass
                print("Prepared - Downloading platform-tools")
                rutil.download("https://dl.google.com/android/repository/platform-tools-latest-windows.zip", "plattools.zip")
                print("Download Complete - Extracting")
                rutil.extractZip("Downloads\\plattools.zip", "Tools")
                rutil.os.system("setx PATH \"" + rutil.os.getcwd() +"\\Tools\platform-tools;%PATH%\"")
                print("Platform Tools Installed and added to PATH - Cleaning up")
                rutil.os.remove("Downloads\\plattools.zip")
                #Docker installer will be run with `"Docker Desktop Installer.exe" install --accept-license`
                if not rutil.checkTool("docker"):
                    print("Downloading Docker for Windows installer")
                    rutil.download("https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe", "docker-inst.exe")
                    print("Download Complete - Preparing to Install")
                    print("The Docker Installer will now run. please follow its process to completion with the default install location. Do not log out of Windows. Instead, return here and report when it has succeeded.")
                    rutil.os.system("Downloads\\docker-inst.exe --accept-license")
                    rutil.askUser()
                    rutil.os.remove("Downloads\\docker-inst.exe")
                    rutil.os.create()
                    with open('Tools\\inprogress.cfg', 'w') as fp:
                        pass
                    raise SystemExit("Phase 1 of Setup is complete. Please Reboot your computer and re-run this program to continue setup.")
                else: 
                    print("Docker already installed - Skipping")
            if resumeSetup or rutil.checkTool("docker"):
                print("Resuming setup - Preparing Magisk - Docker Desktop will start, this is currently required in order to start the Docker Daemon. Please confirm when it finishes loading")
                rutil.os.system("start /w \"\" \"C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe\"")
                rutil.askUser()
                #Docker is a pain in the ass. I'm going to leave it here until I can figure out how to make Magisk-In-A-Box work properly.
    elif mode == 2:
        print("Linux System Setup is currently not implemented. Sorry!")
    #TODO: Do more setup
    print("To configure device specific options, install drivers, or update any of the installed utilities, run this program again.")
else:
    print("Setup has already been completed - Opening configuration menu")
    #TODO: Configuration Menu