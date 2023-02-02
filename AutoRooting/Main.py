#Copyright (C) <2023> by <Quantum>

# [Main.py] will contain the instructions to follow inside functions to make the code more clear.
# Each device model (For now only Samsung) will require a personal function with it's own instructions to follow in order to root the device

from Scripts.Utilities import subprocess, Colors, Check_AdbConnection, SetupDeviceForUSBCommunication, Quit
import Samsung

def Welcome_Screen():
    print(
    f'''



                                                            [{Colors["Green"]}Description{Colors["Reset"]}]:                                                    
    {Colors["White"]}    .▄▄▄  ▄• ▄▌ ▄▄▄·  ▐ ▄ ▄▄▄▄▄▄• ▄▌• ▌ ▄ ·.  {Colors["Reset"]}                This "{Colors["Underline"]}AutoRooting{Colors["Reset"]}" script is a sophisticated system that incorporates a highly {Colors["Underline"]}advanced device status identification algorithm{Colors["Reset"]}. 
    {Colors["White"]}    ▐▀•▀█ █▪██▌▐█ ▀█ •█▌▐█•██  █▪██▌·██ ▐███▪ {Colors["Reset"]}                This allows for the determination of the current situation of the Android device and the selection of the {Colors["Underline"]}optimal solution for rooting{Colors["Reset"]}. 
    {Colors["White"]}    █▌·.█▌█▌▐█▌▄█▀▀█ ▐█▐▐▌ ▐█.▪█▌▐█▌▐█ ▌▐▌▐█· {Colors["Reset"]}                The script employs cutting-edge technologies to ensure a safe and reliable rooting process, preventing possible damage to the device. 
    {Colors["White"]}    ▐█▪▄█·▐█▄█▌▐█ ▪▐▌██▐█▌ ▐█▌·▐█▄█▌██ ██▌▐█▌ {Colors["Reset"]}                Furthermore, this script is subject to {Colors["Underline"]}constant updates{Colors["Reset"]} to ensure compatibility with the latest Android devices.
    {Colors["White"]}    ·▀▀█.  ▀▀▀  ▀  ▀ ▀▀ █▪ ▀▀▀  ▀▀▀ ▀▀  █▪▀▀▀ {Colors["Reset"]}           
    {Colors["White"]}            ▄▄▄              ▄▄▄▄▄            {Colors["Reset"]}                                    
    {Colors["White"]}            ▀▄ █·▪     ▪     •██              {Colors["Reset"]}           [{Colors["Green"]}License{Colors["Reset"]}]:                                                                                                   [{Colors["Green"]}Contributors{Colors["Reset"]}]:
    {Colors["White"]}            ▐▀▀▄  ▄█▀▄  ▄█▀▄  ▐█.▪            {Colors["Reset"]}           [{Colors["Red"]}GNU General Public License v3.0{Colors["Reset"]}]:       
    {Colors["White"]}            ▐█•█▌▐█▌.▐▌▐█▌.▐▌ ▐█▌·            {Colors["Reset"]}                This program is free software: you can redistribute it and/or modify                                  
    {Colors["White"]}            .▀  ▀ ▀█▄▀▪ ▀█▄▀▪ ▀▀▀             {Colors["Reset"]}                it under the terms of the GNU General Public License as published by  
                                                                  the Free Software Foundation, either version 3 of the License, or                         
          [Automating Android Rooting process]                    (at your option) any later version.                                                         
           {Colors["Red"]}Copyright{Colors["Reset"]} (C) <2023> by <Quantum>                                                                                             
                                                                  This program is distributed in the hope that it will be useful,       
                                                                  {Colors["Underline"]}but WITHOUT ANY WARRANTY{Colors["Reset"]}; without even the implied warranty of     
                                                                  {Colors["Underline"]}MERCHANTABILITY{Colors["Reset"]} or FITNESS FOR A PARTICULAR PURPOSE.  See the    
                                                                  GNU General Public License for more details.                          
            
    [{Colors["Green"]}Terms of Use{Colors["Reset"]}]:
        {Colors["Underline"]}Note{Colors["Reset"]} that rooting your device carries a risk of damaging your device. 
        {Colors["Underline"]}The author{Colors["Reset"]} of this script {Colors["Underline"]}assumes no responsibility{Colors["Reset"]} for any potential harm to your device. 
        If you choose to use this script, {Colors["Underline"]}you assume full responsibility{Colors["Reset"]} for the outcome on your device. 
        {Colors["Underline"]}You can open any support request on GitHub{Colors["Reset"]}.


    [{Colors["Green"]}GitHub{Colors["Reset"]}]: [{Colors["Blue"]}https://github.com/QuantumNone/AndroidRooting-Samsung{Colors["Reset"]}]
    
    ''')    #Check if any tool need to share license, for example heimdall or magisk...

    input(f'\t[{Colors["Red"]}Continue{Colors["Reset"]}]: press {Colors["Green"]}ENTER{Colors["Reset"]} in order to continue the execution of this program: ')

#Once the Developer options have been enabled the program will check the USB connection trough ADB
#If the connection cannot be enstablished the problems could be:
#   - User unplugged USB Cable (Or not, in that case ask user to re-plug in the cable)
#   - USB Drivers don't work (Need to install them first), so try to re-install them

#Else, use ADB to get device informations. This function is an example on how it should work (The dict should be a class)

def GetPhoneInformations() -> dict[str, str]:
    print(f'{Colors["Green"]}Getting{Colors["Reset"]} device informations...')
    PhoneInformations = {
        'Model': 'ro.product.model',
        'Brand': 'ro.product.brand', #Check if the brand is Verizon, if so root probably cannot be executed because bootloader cannot be unlocked.
        'Build Number': 'ro.build.display.id',
        'Android Version': 'ro.build.version.release',
        'PDA': 'ro.build.PDA', #SAMSUNG FIRMWARES NEED PDA and CSS
        'CSC': 'ro.csc.country_code',
        'Region': 'ro.build.version.codename', #[REL, TIM] italy,
        'IsEncrypted': 'ro.crypto.state',
        'CPU_Architecture': 'ro.product.cpu.abi'
    }

    for Info in PhoneInformations: #Info = 'Model', PhoneInformations[Info] = 'ro.prduct.model'
        print(f'\t{Colors["Green"]}Detecting{Colors["Reset"]} device {Colors["Green"]}{Info}{Colors["Reset"]}...'.ljust(150), end = '')
        try:
                                                                                                                                                #Need to format this : b'[ro.build.display.id]: [KTU84P.J100HXCS0AQC2]\r\r\n'   to  "KTU84P.J100HXCS0AQC2"
            PhoneInformations[Info] = str(subprocess.check_output(f'adb shell getprop | findstr "{PhoneInformations[Info]}"', stderr = subprocess.STDOUT, shell = True), encoding = 'utf-8').split(': [')[1].split(']')[0].upper()
            print(f'[{Colors["Green"]}Got{Colors["Reset"]}!]')
        except:
            print(f'\b\b[{Colors["Red"]}Not Found{Colors["Reset"]}!]')
            PhoneInformations[Info] = None

    return PhoneInformations



SetupDeviceForUSBCommunication()

print(GetPhoneInformations())


class Phone:
    def __init__(self):
        Check_AdbConnection()
        PhoneInformations = GetPhoneInformations()
        self.Model = PhoneInformations['Model']
        self.Brand = PhoneInformations['Brand']
        self.BuildNumber = PhoneInformations['Build Number']
        self.AndroidVersion = PhoneInformations['Android Version']
        self.PDA = PhoneInformations['PDA']
        self.CSC = PhoneInformations['CSC']
        self.Region = PhoneInformations['Region']
        self.CPU_Architecture = PhoneInformations['CPU_Architecture']
        self.BatteryLevel = str(subprocess.check_output(f'adb shell dumpsys battery | findstr "level"', stderr = subprocess.STDOUT, shell = True), encoding = 'utf-8').strip().split(': ')[1].strip()
        self.IsEncrypted = PhoneInformations['IsEncrypted']

        if self.Brand == 'Verizon':
            Quit(
                ExceptionName = SystemExit(),
                Message = f'This device is branded with Verizon!\nThis device\'s bootloader cannot be unlocked : {Colors["Blue"]}https://community.verizon.com/t5/Other-Phones/Why-does-Verizon-not-allow-unlock-bootloaders/m-p/319200#:~:text=Verizon%20keeps%20bootloaders%20locked%20(most,for%20something%20the%20user%20caused.{Colors["Reset"]}'
            )

        if int(self.BatteryLevel) < 30:
            print(f'{Colors["Red"]}Attention{Colors["Reset"]} : Your phone battery level is under 30%!\nCurrent battery level : {self.BatteryLevel}')
            Quit(
                ExceptionName = SystemExit(),
                Message = 'Phone\'s battery level too low.\nCharge it up to 30% !'
            )

        if int(Device.AndroidVersion[0]) < 9:
            Quit(
                ExceptionName = SystemExit(),
                Message = f'Your device is running on Android V{Device.AndroidVersion}, which is unsupported!\n{Colors["Green"]}Only{Colors["Reset"]} Android Version >= 9 is supported!'
            )

        # VBMeta_output = str(subprocess.check_output(f'adb shell ls -l /dev/block/by-name | findstr "level"', stderr = subprocess.STDOUT, shell = True), encoding = 'utf-8').split('\n')
        # for line in VBMeta_output:
        #     line = line.strip().split(' -> ')
        #     if line[0][-6:] == 'vbmeta':
        #         self.HasVBMeta = True
        #         break
        # else:
        #     self.HasVBMeta = False
        

Device = Phone()

if Device.Model == 'Samsung':
    Samsung.Samsung_Requirements(Device, Phone)

else:
    print(f'''
    Sorry!
    This device is unsupported...
    Cannot root {Device.Model}
    ''')
    input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
    raise SystemExit()



# TODO: Create a function to check ADB (and/or Fastboot) connection

