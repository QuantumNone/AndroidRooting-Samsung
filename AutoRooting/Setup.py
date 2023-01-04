import Scripts.AutoRootUtilities as rutil

# Colors for String formatting :
Colors = {
    "Reset": "\033[0m",
    "Grey": "\033[1;30m",
    "Red": "\033[1;31m",
    "Green": "\033[1;32m",
    "Yellow": "\033[1;33m",
    "Blue": "\033[1;34m",
    "Magenta": "\033[1;35m",
    "Cyan": "\033[1;36m",
    "White": "\033[1;37m",
}
# Usage Example : print(Colors["Red"] + 'Color that string' + Colors["Reset"])


# We start by checking everything is configured correctly OK

Platform = rutil.getPlatform()

if not rutil.getDiskSpace() > 17179869184:
    print(f"Less than {Colors['Red']}16 Gigabytes{Colors['Reset']} of disk space is available, setup cannot continue.")
    input(f"\nPress {Colors['Red']}ENTER{Colors['Reset']} to exit : ")

    raise SystemExit()

if not rutil.isElevated():
    print(f"This Script requires {Colors['Red']}Elevated Priviledges{Colors['Reset']}, Execution cannot continue.")
    input(f"\nPress {Colors['Red']}ENTER{Colors['Reset']} to exit : ")

    raise SystemExit()

if not rutil.isConnected():
    print(f"Could not connect to the Internet, or could not resolve DNS. {Colors['Red']}Check your Internet Connetion{Colors['Reset']}!")
    input(f"\nPress {Colors['Red']}ENTER{Colors['Reset']} to exit : ")

    raise SystemExit()

# Checks if the installation has been marked as in progress, and redirects the installer to docker
#(Docker's first install requires a reboot so that flag serves to not redo the entire installer)
resumeSetup = False
if rutil.os.path.isfile("Tools\\inprogress.cfg"):
    print("Resuming setup")
    resumeSetup = True

if not rutil.isSetup():
    if (Platform == "Windows") and (not resumeSetup):
        if not rutil.checkTool("wsl"):
            print(f"[{Colors['Green']}AutoRooting{Colors['Reset']}] requires {Colors['Red']}WSL2{Colors['Reset']} (Windows Subsystem for Linux) to be installed.")
            print(f"For more information, see {Colors['Blue']}https://aka.ms/wsl{Colors['Reset']}")
            input(f"\nPress {Colors['Red']}ENTER{Colors['Reset']} to exit : ")

            raise SystemExit()

        if rutil.checkTool("adb") or rutil.checkTool("fastboot"): #Need to create a function that removes these tools from the Environment Path and that removes C:/platform-tools folder
            raise SystemExit()

        # TODO: replace this check with a WSL check that will determinate if the app present is installer or installed
        if not resumeSetup:
            print(
                f"""All the {Colors['Red']}requirements{Colors['Reset']} have been configured correctly!
                [{Colors['Red']}Setup.py{Colors['Reset']}] will perform an installation of :
                {Colors['Green']}SDK Platform Tools{Colors['Reset']} : includes tools that interface with the Android platform trough USB Communication [{Colors['Green']}adb&fastboot{Colors['Reset']}]
                {Colors['Green']}Docker Software{Colors['Reset']} : a {Colors['Green']}virtual machine{Colors['Reset']} that helps on patching Android images with {Colors['Green']}Magisk{Colors['Reset']}
                """
            )
            print(f"Preparing {Colors['Red']}File Structure{Colors['Reset']}...")
            print(
                f"""
                ├───{Colors['Green']}Devices{Colors['Reset']}
                ├───{Colors['Red']}Downloads{Colors['Reset']}
                ├───Scripts
                │   └───__pycache__
                └───{Colors['Green']}Tools{Colors['Reset']}
                    ├───magiskDocker
                    └───platform-tools
                """)

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


            rutil.download(
                "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
                "plattools.zip",
            )
            
            rutil.extractZip(
                "Downloads\\plattools.zip", 
                "Tools"
            )

            #Adding platform-tools folder to the Environment PATH to be able to access to adb.exe and fastboot.exe anywhere in terminal
            rutil.os.system(
                'setx PATH "' + rutil.os.getcwd() + '\\Tools\platform-tools;%PATH%"'
            )

            print(f"{Colors['Green']}Cleaning Up{Colors['Reset']}...")
            rutil.os.remove("Downloads\\plattools.zip")

            # Docker installer will be run with `"Docker Desktop Installer.exe" install --accept-license`
            if not rutil.checkTool("docker"):
                rutil.download(
                    "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
                    "docker-inst.exe",
                )
                print(
                    f"""
                    [{Colors['Red']}Attention{Colors['Reset']}] : 
                    {Colors['Red']}Docker installer{Colors['Reset']} will now be executed!
                    Please, continue with the {Colors['Green']}default settings{Colors['Reset']} installation.
                    Do not change any configuration, just click '{Colors['Green']}Next{Colors['Reset']}'.
                    """
                )

                # TODO: Automate Docker installation

                rutil.os.system("Downloads\\docker-inst.exe --accept-license")
                input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to continue ({Colors['Red']}Docker installation has to be finished!{Colors['Reset']})")
                rutil.os.remove("Downloads\\docker-inst.exe")
                
                with open("Tools\\inprogress.cfg", "w") as fp:
                    pass

                print(f"Please, {Colors['Red']}reboot{Colors['Reset']} your computer and then {Colors['Green']}Execute again{Colors['Reset']} Setup.py file from a terminal!")
                raise SystemExit()
            else:
                print("Docker already installed!")

    if resumeSetup or rutil.checkTool("docker"):
        print(
            f"""[{Colors['Red']}Resuming setup{Colors['Reset']}]
            [{Colors['Red']}Preparing Magisk{Colors['Reset']}] : Docker Desktop will start.
            """
        )

        rutil.os.system(
            'start /w "" "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"'
        )
        input(f"Press {Colors['Red']}Enter{Colors['Reset']} key once Docker Desktop is opened : ")
        
        rutil.download(
            "https://raw.githubusercontent.com/xclusivor/magisk-in-a-box/main/Dockerfile",
            "Dockerfile",
        )
        rutil.download(
            "https://raw.githubusercontent.com/xclusivor/magisk-in-a-box/main/miab.sh",
            "miab.sh",
        )
        rutil.os.replace("Downloads\\Dockerfile", "Tools\\magiskDocker\\Dockerfile")
        rutil.os.replace("Downloads\\miab.sh", "Tools\\magiskDocker\\miab.sh")
        print(
            "Docker will now attempt to build the magisk image. Be patient, this may take up to an hour or as little as 5 minutes, depending on your System specs"
        )
        rutil.os.system("docker build .\\Tools\\magiskDocker -t miab")
        if rutil.askUser(
            "Did Docker build the image successfully? (All output is not red, and no Errors present)"
        ):
            with open("Tools\\config.cfg", "w") as fp:
                fp.write(
                    "This file exists to validate that setup has been completed - Do not move or delete it."
                )
            rutil.os.remove("Tools\\inprogress.cfg")
            print("Setup is now complete!")
        else:
            with open("Tools\\inprogress.cfg", "w") as fp:
                pass
            raise SystemExit(
                "Docker failed to compile - setup cannot continue. Please resolve the above errors and re-run setup."
            )

    elif Platform == 2:
        print("Linux System Setup is currently not implemented. Sorry!")
    # TODO: Do more setup
    print(
        "To configure device specific options, install drivers, or update any of the installed utilities, run this program again."
    )
else:
    print("Setup has already been completed - Opening configuration menu")
    # TODO: Configuration Menu
