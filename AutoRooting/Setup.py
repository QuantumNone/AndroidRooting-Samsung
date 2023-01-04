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

if not rutil.isSetup():
    if mode == 1:
        if not rutil.checkTool("wsl"):
            raise SystemExit("This tool requires WSL2 to be installed in order to patch magisk boot images with docker. WSL2 can be installed on all versions of Windows starting with Windows 10 2004 and all releases of Windows 11. For more information, see https://aka.ms/wsl")
        if rutil.checkTool("adb") or rutil.checkTool("fastboot"):
            raise SystemExit("ADB or Fastboot are already in Path. This will conflict with the installed version, which will install the latest version of platform-tools into path. Please remove the offending programs and re-run Setup.")
        print("Checks Complete, Detected first run or configuration removed.")
        print("Welcome to Setup.py, this setup file will install google's platform-tools and docker, then will spawn a docker container to patch boot images for magisk.")
        if not rutil.askUser("Is this alright?"):
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
            rutil.download("https://dl.google.com/android/repository/platform-tools-latest-windows.zip", "plattools.zip")
            rutil.extractZip("Downloads\\plattools.zip", "Tools")
            rutil.os.remove("Downloads\\plattools.zip")
            print(rutil.os.system("setx PATH \"" + rutil.os.getcwd() +"\\Tools\platform-tools;%PATH%\""))
    #TODO: Do more setup
    print("To configure device specific options and drivers, or to update any of the installed utilities, run this program again.")
else:
    print("Setup has been completed - Opening configuration menu")
    #TODO: Configuration Menu