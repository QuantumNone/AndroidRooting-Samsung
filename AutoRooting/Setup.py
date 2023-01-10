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



if Platform == "Windows":
    #These Tools are general tools, means that we are working with samsung for now and so if a device brand requires specified tool, then it will be installed inside the device brand's function's setup
    print(
        f"""All the {Colors['Red']}requirements{Colors['Reset']} have been configured correctly!
        [{Colors['Red']}Setup.py{Colors['Reset']}] will perform an installation of :
        {Colors['Green']}SDK Platform Tools{Colors['Reset']} : includes tools that interface with the Android platform trough USB Communication [{Colors['Green']}adb&fastboot{Colors['Reset']}]
        """
    )
    with open("Tools\\config.cfg", "w") as fp:
        fp.write(
            "This file exists to validate that setup has been completed - Do not move or delete it."
        )

elif Platform == "Linux":
    print("Linux System Setup is currently not implemented. Sorry!")
# TODO: Do more setup
elif Platform == "Darwin":
    print("MacOS System Setup is currently not implemented. Sorry!")

