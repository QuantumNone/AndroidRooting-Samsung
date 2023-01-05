

# [Main.py] will contain the instructions to follow inside functions to make the code more clear.
# Each device model (For now only Samsung) will require a personal function with it's own instructions to follow in order to root the device

import Scripts.AutoRootUtilities as rutil
Colors = rutil.Colors
sleep = rutil.sleep
sleepDelay = 0



# The user has to follow these steps in order to be able to use Adb
def SetupDeviceForUSBCommunication():
    """User has to MANUALLY setup his device to start USB communication"""
    print(f'\n\n1. Open your device {Colors["Green"]}settings{Colors["Reset"]} and navigate into "About my phone" option.')
    sleep(sleepDelay)
    print(f'2. Search for "{Colors["Red"]}Build number{Colors["Reset"]}" option inside these settings (if you cannot find it try in "{Colors["Green"]}Software Information{Colors["Reset"]}" option).')
    sleep(sleepDelay)
    print(f'3. Tap 7 times on "Build number" option to enable {Colors["Red"]}Developer Options{Colors["Reset"]}.')
    sleep(sleepDelay)
    print(f'4. Go back to settings and {Colors["Red"]}search{Colors["Reset"]} for Developer Options.')
    sleep(sleepDelay)
    print(f'5. Search for "{Colors["Red"]}USB debugging{Colors["Reset"]}" option and {Colors["Green"]}enable{Colors["Reset"]} it.')
    sleep(sleepDelay)
    print(f'6. {Colors["Green"]}Connect{Colors["Reset"]} now your device to your computer trough USB cable and check your device screen.')
    sleep(sleepDelay)
    print(f'7. {Colors["Green"]}Allow{Colors["Reset"]} the pop-up asking for computer permissions.')
    sleep(sleepDelay)
    print(f'8. Now search inside Developer Options for "{Colors["Red"]}Select USB configuration{Colors["Reset"]}".')
    sleep(sleepDelay)
    print(f'9. Click it and select "{Colors["Green"]}MTP File transfer{Colors["Reset"]}" protocol.')
    sleep(sleepDelay)

    input(f'\n\t=> Press {Colors["Green"]}Enter{Colors["Reset"]} key to continue : ')

    print(f'\n10. Now search for "{Colors["Red"]}OEM Unlocking{Colors["Reset"]}" option in Developer options and {Colors["Green"]}ENABLE{Colors["Reset"]} it!')
    sleep(sleepDelay)
    print(
        f'''
        {Colors["Red"]}IF{Colors["Reset"]} YOU CANNOT FIND THAT OPTION THEN LOOK AT THESE DOCUMENTATION :
        \t1. "{Colors["Blue"]}https://krispitech.com/fix-the-missing-oem-unlock-in-developer-options/{Colors["Reset"]}"
        \t2. "{Colors["Blue"]}https://www.quora.com/Why-do-some-mobile-companies-refuse-to-unlock-bootloaders-like-Huawei-and-Realme{Colors["Reset"]}"
        '''
        )
    sleep(sleepDelay)

    input(f'\n\t=> Press {Colors["Green"]}Enter{Colors["Reset"]} key to continue : ')
    print()


# SetupDeviceForUSBCommunication()


#Once the Developer options have been enabled the program will check the USB connection trough ADB
#If the connection cannot be enstablished the problems could be:
#   - User unplugged USB Cable (Or not, in that case ask user to re-plug in the cable)
#   - USB Drivers don't work (Need to install them first), so try to re-install them

#Else, use ADB to get device informations. This function is an example on how it should work (The dict should be a class)

# def GetPhoneInformations():
#     PhoneInformations = {
#         'Model': 'ro.product.model',
#         'Build Number': 'ro.build.display.id',
#         'Android Version': 'ro.build.version.release',
#         'PDA': 'ro.build.PDA' #SAMSUNG FIRMWARES NEED PDA and CSS
#     }
#     subprocess.call('cls', shell=True)

#     for Info in PhoneInformations:
#         try:
#                                                                                                                                                 #Need to format this : b'[ro.build.display.id]: [KTU84P.J100HXCS0AQC2]\r\r\n'   to  "KTU84P.J100HXCS0AQC2"
#             PhoneInformations[Info] = str(subprocess.check_output(f'adb shell getprop | find "{PhoneInformations[Info]}"', stderr=subprocess.STDOUT, shell = True)).split(': ')[1].split(']')[0][1:]
#             print(f'Got device {Info} : {PhoneInformations[Info]}')
#         except:
#             print(f'Could not get device {Info} information!')
#             PhoneInformations[Info] = False
#     return PhoneInformations


#
# class Phone:
#     def __init__(self):
#         self.Model = PhoneInformations['Model']
#         self.BuildNumber = PhoneInformations['Build Number']
#         self.AndroidVersion = PhoneInformations['Android Version']
#         self.PDA = PhoneInformations['PDA']

# device = Phone(PhoneInformations)



# TODO: Create a function to check ADB (and/or Fastboot) connection

