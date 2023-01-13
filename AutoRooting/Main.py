

# [Main.py] will contain the instructions to follow inside functions to make the code more clear.
# Each device model (For now only Samsung) will require a personal function with it's own instructions to follow in order to root the device

from Scripts.AutoRootUtilities import *

def Welcome_Screen():
    #...
    input('Rooting will erase all your phone data.\nContinue?')




# SetupDeviceForUSBCommunication()


#Once the Developer options have been enabled the program will check the USB connection trough ADB
#If the connection cannot be enstablished the problems could be:
#   - User unplugged USB Cable (Or not, in that case ask user to re-plug in the cable)
#   - USB Drivers don't work (Need to install them first), so try to re-install them

#Else, use ADB to get device informations. This function is an example on how it should work (The dict should be a class)

def GetPhoneInformations() -> dict[str, str]:
    PhoneInformations = {
        'Model': 'ro.product.model',
        'Build Number': 'ro.build.display.id',
        'Android Version': 'ro.build.version.release',
        'PDA': 'ro.build.PDA', #SAMSUNG FIRMWARES NEED PDA and CSS
        'CSC': 'ro.csc.country_code',
        'Region': 'ro.build.version.codename' #[REL, TIM] italy
    }
    subprocess.call('cls', shell=True)

    for Info in PhoneInformations:
        try:
                                                                                                                                                #Need to format this : b'[ro.build.display.id]: [KTU84P.J100HXCS0AQC2]\r\r\n'   to  "KTU84P.J100HXCS0AQC2"
            PhoneInformations[Info] = str(subprocess.check_output(f'adb shell getprop | findstr "{PhoneInformations[Info]}"', stderr = subprocess.STDOUT, shell = True)).split(': [')[1].split(']')[0].upper()
            print(f'{Colors["Green"]}Got{Colors["Reset"]} device {Info} : {PhoneInformations[Info]}')

        except:
            print(f'{Colors["Red"]}Could not{Colors["Reset"]} get device {Info} information!')
            PhoneInformations[Info] = None

    return PhoneInformations

print(GetPhoneInformations())


class Phone:
    def __init__(self):
        Check_AdbConnection()
        PhoneInformations = GetPhoneInformations()
        self.Model = PhoneInformations['Model']
        self.BuildNumber = PhoneInformations['Build Number']
        self.AndroidVersion = PhoneInformations['Android Version']
        self.PDA = PhoneInformations['PDA']
        self.CSC = PhoneInformations['CSC']
        self.Region = PhoneInformations['Region']

Device = Phone()

if Device.Model == 'Samsung':
    if int(Device.AndroidVersion[0]) < 9:
        print(f'Your device is running on Android V{Device.AndroidVersion}, which is unsupported!')
        print(f'{Colors["Green"]}Only{Colors["Reset"]} Android Version >= 9 is supported!')
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
        raise SystemExit()

    Samsung_Requirements(Phone())

else:
    print(f'''
    Sorry!
    This device is unsupported...
    Cannot root {Device.Model}
    ''')
    input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
    raise SystemExit()



# TODO: Create a function to check ADB (and/or Fastboot) connection

