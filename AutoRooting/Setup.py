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
    print(
        f"Less than {Colors['Red']}16 Gigabytes{Colors['Reset']} of disk space is available, setup cannot continue."
    )
    input(f"\nPress {Colors['Red']}ENTER{Colors['Reset']} to exit : ")

    raise SystemExit()

if not rutil.isElevated():
    print(
        f"This Script requires {Colors['Red']}Elevated Priviledges{Colors['Reset']}, Execution cannot continue."
    )
    input(f"\nPress {Colors['Red']}ENTER{Colors['Reset']} to exit : ")

    raise SystemExit()

if not rutil.isConnected():
    print(
        f"Could not connect to the Internet, or could not resolve DNS. {Colors['Red']}Check your Internet Connetion{Colors['Reset']}!"
    )
    input(f"\nPress {Colors['Red']}ENTER{Colors['Reset']} to exit : ")

    raise SystemExit()

# Checks if the installation has been marked as in progress, and redirects the installer to docker
# (Docker's first install requires a reboot so that flag serves to not redo the entire installer)
resumeSetup = False
if rutil.os.path.isfile("Tools\\inprogress.cfg"):
    print("Resuming setup")
    resumeSetup = True

if not rutil.isSetup():
    if Platform == "Windows":

        if rutil.checkTool("adb") or rutil.checkTool(
            "fastboot"
        ):  # Need to create a function that removes these tools from the Environment Path and that removes C:/platform-tools folder
            raise SystemExit()

        # TODO: replace this check with a WSL check that will determinate if the app present is installer or installed
        else:
            print(
                f"""All the {Colors['Red']}requirements{Colors['Reset']} have been configured correctly!
                [{Colors['Red']}Setup.py{Colors['Reset']}] will perform an installation of :
                {Colors['Green']}SDK Platform Tools{Colors['Reset']} : includes tools that interface with the Android platform trough USB Communication [{Colors['Green']}adb&fastboot{Colors['Reset']}]
                """
            )
            print(f"Preparing {Colors['Red']}File Structure{Colors['Reset']}...")
            try:
                rutil.os.mkdir("Tools")
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
            print("Download Complete - Extracting")
            rutil.extractZip("Downloads\\plattools.zip", "Tools")
            rutil.os.system(
                'setx PATH "' + rutil.os.getcwd() + '\\Tools\platform-tools;%PATH%"'
            )

        print(
            f"{Colors['Green']}Platform Tools Installed and added to PATH - Cleaning Up{Colors['Reset']}..."
        )
        rutil.os.remove("Downloads\\plattools.zip")
        with open("Tools\\config.cfg", "w") as fp:
            fp.write(
                "This file exists to validate that setup has been completed - Do not move or delete it."
            )

    elif Platform == "Linux":
        print("Linux System Setup is currently not implemented. Sorry!")
    # TODO: Do more setup
    print(
        "To configure device specific options, install drivers, or update any of the installed utilities, run this program again."
    )
else:
    print("Setup has already been completed - Opening configuration menu")
    # TODO: Configuration Menu
