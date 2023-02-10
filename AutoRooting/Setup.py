#Copyright (C) <2023> by <Quantum>

import Scripts.Utilities as rutil
 
# Colors for String formatting :
Colors = rutil.Colors
# Usage Example : print(Colors["Red"] + 'Color that string' + Colors["Reset"])


# We start by checking everything is configured correctly OK

Platform = rutil.getPlatform()

if not rutil.getDiskSpace() > 21474836480:
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



try:
    rutil.os.mkdir("Tools")
except FileExistsError:
    pass
try:
    rutil.os.mkdir("Downloads")
except FileExistsError:
    pass
try:
    rutil.os.mkdir(f'{rutil.DownloadsFolder}Temp')
except FileExistsError:
    pass
try:
    rutil.os.mkdir(f'Logs')
except FileExistsError:
    pass

rutil.Pip_Installer(Package = 'tqdm')
rutil.Pip_Installer(Package = 'bs4')


rutil.AddToEnvironmentPath(Directory = rutil.DownloadsFolder)
rutil.AddToEnvironmentPath(Directory = rutil.ToolsFolder)

