#Copyright (C) <2023> by <Quantum>

#TODO: Check which samsung cannot be unlocked, such as US version.
#US and Canada
# Factory unlocked ones should also be affected
#Before starting make sure any google account has been removeds

from Scripts.Utilities import *

def Samsung_Requirements(Device: object, Phone: classmethod):
    def Install_SamsungUSBDrivers(InstallationStatus: bool = True) -> None:
        Download(
            URLink = "https://developer.samsung.com/sdp/file/2ad30860-0932-44e3-bf63-765a5cfa1010",
            FileName = "SamsungUSB-installer.exe"
        )

        #Let's not reboot the computer and try to check if the USB Communication works, if not then the pc will require reboot (Or Windows Driver signature offline)
        print(
            f'Please, follow the instructions that the installer shows!'
        )
        os.startfile(f'{DownloadsFolder}SamsungUSB-installer.exe')
        print('Installation Completed!')

        #HAVE TO WORK ON THAT
        if not InstallationStatus: #This can be converted into a function like : checkAdbConnection() (If not connected, check USB drivers) 
            print(
                f'''
                The USB communication cannot be enstablished!
                Try to reboot your computer or try to {Colors["Red"]}disable{Colors["Reset"]} Windows Driver Signature Verification : 
                \t[{Colors["Blue"]}https://answers.microsoft.com/en-us/windows/forum/all/permanent-disable-driver-signature-verification/009c3498-bef8-4564-bb52-1d05812506e0{Colors["Reset"]}]'''
            )
            
            Quit(
                ExceptionName = SystemExit(),
                Message = f'{Colors["Red"]}Cannot Install Correctly{Colors["Reset"]} USB Drivers!'
            )

    def Unlock_Bootloader() -> None: #SHOULD RETURN AN AVAILABLE USB CONNECTION
        print(f'''\n
        [{Colors["Red"]}Bootloader unlock{Colors["Reset"]} Step]\t[{Colors["Green"]}Advance Download Mode{Colors["Reset"]}]
        \t\t[{Colors["Red"]}All phone data will be erased{Colors["Reset"]}!]
        1. {Colors["Red"]}Unplug{Colors["Reset"]} phone cable from pc and {Colors["Red"]}power off{Colors["Reset"]} your phone.
        2. Press and hold {Colors["Red"]}volume up{Colors["Reset"]} and {Colors["Red"]}volume down{Colors["Reset"]} buttons {Colors["Green"]}and{Colors["Reset"]} (while holding) connect the USB cable to the computer.
        \t[{Colors["Red"]}IF{Colors["Reset"]} your phone has {Colors["Red"]}BIXBI button{Colors["Reset"]} then press and hold it too!]
        3. You can release buttons once a {Colors["Blue"]}blue screen{Colors["Reset"]} appears.
        
        You should now see a screen like this :
            {Colors["Green_Highlight"]}A custom OS can cause critical problems{Colors["Reset"]} 
            {Colors["Green_Highlight"]}in phone and installed applications.{Colors["Reset"]} 
        
            {Colors["Green_Highlight"]}if you want to download a custom OS,{Colors["Reset"]} 
            {Colors["Green_Highlight"]}press the volume up key.{Colors["Reset"]} 
            {Colors["Green_Highlight"]}Otherwise, press the volume down key to cancel.{Colors["Reset"]} 

          ---------------------------------------------------

            {Colors["Green_Highlight"]}Volume up: Continue{Colors["Reset"]} 
            {Colors["Green_Highlight"]}Volume up long press: Device unlock mode{Colors["Reset"]} 
            {Colors["Green_Highlight"]}Volume down: Cancel (restart phone){Colors["Reset"]} 

        4. Press and hold volume up button until see {Colors["Red"]}bootloader unlock menu{Colors["Reset"]}.
        5. Press again the volume up button to {Colors["Green"]}confirm{Colors["Reset"]} the bootloader unlock process.

        The phone will now reboot.
        ''')
        
        input(f'Press {Colors["Green"]}ENTER{Colors["Reset"]} {Colors["Red"]}if{Colors["Reset"]} the phone has been rebooted : ')

        print(f'''
        Your phone has now been rebooted into {Colors["Blue"]}Welcome Screen{Colors["Reset"]}.
        Configure all you need to finish the Welcome Screen's setup.     [You can also skip this configuration, just click on "Next"]
        Open your system settings and {Colors["Red"]}configure{Colors["Reset"]} WI-FI network.      [{Colors["Red"]}Important{Colors["Reset"]}!]

        Once done enable again developer options.
        ''')
        if askUser('Need help on how to enable Developer options?'):
            SetupDeviceForUSBCommunication()
        
        if askUser(f'Is "OEM Unlocking" option "{Colors["Grey"]}greyed out{Colors["Reset"]}"?'):
                print(f'[{Colors["Red"]}Great{Colors["Reset"]}!]\nYour phone\'s bootloader has been {Colors["Green"]}unlocked correctly{Colors["Reset"]}!') 
        else:
            print("This means your phone's bootloader hasn't been unlocked correctly!")
            if askUser('Wanna continue anyway?'):
                print(f"[{Colors['Green']}Ok!{Colors['Reset']}]")       #If unlocking bootloader instructions were followed rightly (phone formatted) some devices (like huawei) might not have "OEM Unlocking" greyed out...
            else:
                input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to exit : ")
                raise SystemExit()

    def Install_Heimdall() -> None: #The phone has to be in download mode
        
            
        Download(
            URLink = "https://download1076.mediafire.com/ha3x6kwdi36g/zyge4l2ifk9nxk6/Heimdall.zip",
            FileName = "Heimdall.zip"
        )
        
        ExtractZip(
            Zip_Path = DownloadsFolder + 'Heimdall.zip',
            DestinationPath = ToolsFolder,
            HasFolderInside = False
        )

        os.rename(ToolsFolder + 'Heimdall\\zadig-2.4.exe', ToolsFolder + 'Heimdall\\zadig.exe')

        #This might be a 'USBDriver installation' function
        #TODO : In order to stop doing things multiple times (like drivers installation), create a config file where to store informations about what this program did.
        print(f'{Colors["Green"]}In order to{Colors["Reset"]} setup USB communication, you need to install Samsung drivers {Colors["Green"]}manually{Colors["Reset"]}...')
        print(f'{Colors["Green"]}Rebooting{Colors["Reset"]} Samsung to {Colors["Blue"]}Download Mode{Colors["Reset"]}...')
        os.system('adb reboot download')
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} if the device is in Download Mode : ")
        print(f'{Colors["Green"]}zadig.exe{Colors["Reset"]} (a Driver installer application) will be executed!')    #TODO : check if zadig reboots pc once driver is installed
        os.startfile(ToolsFolder + 'Heimdall\\zadig.exe')

        print(f'''
Now follow these {Colors["Red"]}instructions{Colors["Reset"]} : 
    1. From the menu chose Options -> {Colors["Green"]}List All Devices{Colors["Reset"]}.

    2. From the USB Device list chose "{Colors["Green"]}Samsung USB Composite Device{Colors["Reset"]}" or "{Colors["Green"]}Gadget Serial{Colors["Reset"]}".

    3. Press "{Colors["Green"]}Install Driver{Colors["Reset"]}", click "{Colors["Green"]}Yes{Colors["Reset"]}" to the prompt and if you receive
    a message about being unable to verify the publisher of the driver
    click "Install this driver software anyway".

        {Colors["Red"]}NOTE{Colors["Reset"]}:    [IF YOU DON'T SEE YOUR DEVICE IN 'Device list' then your device might be unsupported!]

    4. Done!

    5. Close zadig application.
        ''')

        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to continue : ")

    def Download_Firmware() -> None: #Returns "Firmware" folder inside Downloads folder. Inside it there are all .md5 files
        def Download_Status(Status: str):
            #This dict contains all supported firmware regions, there could be a better way to implement this...
            Samsung_Regions: dict(str, list[str]) = {
                'Algeria': ['ALG', 'ALR'],
                'Argentina': ['ANC', 'ARO', 'CTI', 'UFN', 'PSN'],
                'Aruba': ['ARU'],
                'Australia': ['OPP', 'OPS', 'VAU', 'XSA', 'TEL', 'HUT'],
                'Austria': ['AOM', 'DRE', 'MAX', 'MOB', 'MOK', 'ONE', 'TRG', 'ATO'],       
                'Baltic': ['SEB'],
                'Belarus': ['MTB', 'VEL'],
                'Belgium': ['BAE', 'BSE', 'PRO', 'XEB'],
                'Bosnia-Herzegovina': ['BHO', 'BHT', 'TEB'],
                'Brazil': ['BTA', 'BTM', 'TMR', 'ZTA', 'ZVV', 'ZTO', 'ZTM'],
                'Bulgaria': ['CMF', 'GBL', 'MTE', 'MTL', 'OMX', 'PLX', 'VVT'],
                'Cambodia': ['RCG'],
                'Canada': ['RGS', 'BMC', 'TLS'],
                'Chile': ['CHB', 'CHE', 'CHL', 'CHT'],
                'China': ['CUH', 'INT', 'TEC', 'TIY', 'CMC', 'CHN', 'M00'],
                'Colombia': ['COB', 'COL', 'COM', 'CGU'],
                'Costa Rica': ['ICE'],
                'Croatia': ['CRO', 'TRA', 'TWO', 'VIP'],
                'Cyprus': ['CYV'],
                'Czech': ['ETL', 'KBN', 'OSK', 'VDC', 'XCS', 'XEZ', 'TMZ', 'O2C'],
                'Denmark': ['DTL'],
                'Dominica': ['CST', 'DCN', 'DOR'],
                'Dominican Rep': ['CDR', 'TDR'],
                'Ecuador': ['BBE'],
                'Egypt': ['EGY'],
                'El Salvador': ['DGC', 'TBS'],
                'Finland': ['ELS', 'SAU'],
                'France': ['OFR', 'AUC', 'BOG', 'COR', 'DIX', 'FTM', 'NRJ', 'ORC', 'ORF', 'SFR', 'UNI', 'VGF', 'XEF'],
                'Germany': ['DBT', 'DTM', 'DUT', 'EPL', 'MAN', 'MBC', 'VD2', 'VIA', 'XEG'],
                'Ghana': ['SPN'],
                'Greece': ['AOC', 'COS', 'EUR', 'GER', 'TGR', 'VGR', 'CYO'],
                'Guatemala': ['PCS'],
                'Hong Kong': ['TGY'],
                'Hungary': ['PAN', 'VDH', 'WST', 'TMO', 'XEH', 'TMH'],
                'India': ['HFC', 'HYA', 'INA', 'IND', 'INU', 'IMS', 'REL', 'TAT', 'INS'],
                'Indonesia': ['AXI', 'SAR', 'XSE'],
                'Iran': ['THR'],
                'Ireland': ['3IE', 'VDI'],
                'Israel': ['CEL', 'PCL', 'PTR'],
                'Italy': ['GOM', 'HUI', 'ITV', 'OMN', 'TIM', 'VOM', 'WIN', 'XET', 'FWB'],
                'Ivory Coast': ['IRS', 'SIE'],
                'Jamaica': ['JBS', 'JCN', 'JCW'],
                'Japan': ['DCM', 'SBM', 'VFK'],
                'Jordan': ['LEV'],
                'Kazakhstan': ['EST', 'KCL', 'KMB', 'KZK', 'SKZ'],
                'Kenya': ['KEL', 'KEN'],
                'Korea': ['SKT'],
                'Libyan Arab Rep': ['MMC'],
                'Lithuania': ['TLT'],
                'Luxemburg': ['LUX'],
                'Macao': ['VTN'],
                'Macedonia': ['TMC', 'MBM'],
                'Malaysia': ['CCM', 'MXS', 'FMG', 'FME', 'XME'],
                'Mexico': ['SEM', 'TCE', 'TMM', 'UNE'],
                'Mongolia': ['MPC'],
                'Morocco': ['WAN', 'FWD', 'MAT', 'MED', 'SNI', 'MWD'],
                'Netherlands': ['BEN', 'MMO', 'ONL', 'QIC', 'TFT', 'TNL', 'VDF', 'VDP', 'XEN', 'KPN'],
                'New Zealand': ['VNZ'],
                'Nigeria': ['ECT', 'GCR', 'MML'],
                'Norway': ['TEN'],
                'Pakistan': ['WDC', 'PAK'],
                'Panama': ['BPC', 'PCW', 'PBS'],
                'Peru': ['PEB', 'PET', 'SAM'],
                'Philippines': ['FAM', 'XTC', 'GLB', 'XTE', 'SMA'],
                'Poland': ['ERA', 'IDE', 'PLS', 'PRT', 'XEO'],
                'Portugal': ['OPT', 'TMN', 'TPH', 'XEP', 'TCL'],
                'Puerto Rico': ['CEN', 'PCI', 'TPR'],
                'Romania': ['CNX', 'HAT', 'ORO', 'COA'],
                'Russia': ['AZC', 'BLN', 'EMT', 'ERS', 'GEO', 'MTV', 'SER', 'SNT'],
                'Saudi Arabi': ['JED'],
                'Serbia Montenegro': ['MSR', 'PMN', 'SMO', 'TSR', 'TOP'],
                'Singapore': ['BGD', 'XSO', 'XSP'],
                'Slovakia': ['GTL', 'IRD', 'TMS', 'ORS'],
                'Slovenia': ['MOT', 'SIM'],
                'South Africa': ['XFA', 'XFC', 'XFM', 'XFV', 'XFE'],
                'South West Asia': ['SWA'],
                'Spain': ['AMN', 'EUS', 'FOP', 'XEC', 'ATL'],
                'Sweden': ['BAU', 'BCN', 'BME', 'BSG', 'BTH', 'COV', 'HTS', 'SEN', 'TET', 'TLA', 'XEE', 'VDS', 'TNO'],
                'Switzerland': ['AUT', 'ORG', 'MOZ', 'SUN', 'SWC'],
                'Taiwan': ['TWM', 'BRI', 'TCC', 'TCI', 'CWT'],
                'Tanzania': ['SOL'],
                'Temporary': ['TEM'],
                'Thailand': ['CAT', 'THE', 'THL', 'THO', 'THS'],
                'The UAE': ['MID', 'ARB', 'XSG', 'AFR', 'ITO'],
                'The UK': ['BTC', 'O2I', 'O2U', 'ORA', 'TMU', 'TSC', 'VOD', 'XEU', 'VIR', 'H3G', 'CPW'],
                'The USA': ['AWS', 'DOB', 'TMB', 'CLW'],
                'Tunisia': ['ABS', 'RNG'],
                'Turkey': ['BAS', 'KVK', 'TUR', 'TLP', 'TRC'],
                'Ukraine': ['KVR', 'SEK', 'UMC'],
                'Uzbekistan': ['UZB'],
                'Venezuela': ['VMT'],
                'Vietnam': ['XXV', 'PHU', 'XEV', 'DNA', 'FPT', 'SPT', 'TLC', 'VTC', 'VTL']
            }

            def Get_WorkingVersion():   #If the user's phone's region cannot be found inside Samsung Firmware server then we get any available ("wrong" region won't cause any brick)
                for country in Samsung_Regions: #country = 'Algeria'
                    for region in Samsung_Regions[country]: #region = 'ALG' then region = 'ALR'...
                        try: #If the region is found then we get it's version
                            versions = str(
                                subprocess.check_output(
                                    f'samloader -m {Device.Model} -r {region} checkupdate', 
                                    stderr = subprocess.STDOUT, 
                                    shell = True), 
                                encoding = 'utf-8')[:-2]

                            print(f'Found a downloadable firmware region ["{Colors["Green"]}{country}{Colors["Reset"]}" : {region}]!')
                            Device.Region = region #Important : change user's phone's region information because this firmware will be flashed on the device...
                            return versions
                        except:
                            print(f'Trying with "{Colors["Grey"]}{region}{Colors["Reset"]}"...'.ljust(150), f'[{Colors["Red"]}Not worked{Colors["Reset"]}!]')
                            pass

                #This is raised if no region has been found, because if found then the execution of this function terminates with the return statement 'return versions'
                Quit(ExceptionName = SystemExit(), Message = f'Cannot find any {Device.Model} firmware version!') 

            def GetFirmwareVersion() -> str:
                try: #This is the first check : if the region given from adb is not found then samloader raises an Exception, so we check if there is any region available for this device
                    versions = str(
                        subprocess.check_output(
                            f'samloader -m {Device.Model} -r {Device.Region} checkupdate', 
                            stderr = subprocess.STDOUT, 
                            shell = True), 
                        encoding = 'utf-8')[:-2]

                except Exception:
                        print(f'{Colors["Red"]}Cannot{Colors["Reset"]} find any version on "{Colors["Green"]}{Device.Region}{Colors["Reset"]}" Region!')
                        if askUser(f'Do you want to download any other firmware version [{Colors["Green"]}Recommended{Colors["Reset"]}] ?'):
                            versions = Get_WorkingVersion()
                        else:
                            raise SystemExit()
                return versions
            versions = GetFirmwareVersion() if versions not in locals() else versions #This is because Dowload_Status() can be called more times

            if Status == 'New Download':
                try:    #Need to check if some firmwares have .enc2 extension, because if so then samloader will raise an error during decrypting       #Maybe samloader manages it automatically, so no need
                    os.system(f'samloader --dev-model {Device.Model} --dev-region {Device.Region} download --fw-ver {versions} --do-decrypt --out-file {DownloadsFolder + "Firmware.zip.enc4"}')
                
                except ConnectionAbortedError:
                    print(f'Your {Colors["Red"]}internet connection{Colors["Reset"]} has been stopped or aborted!\nPlease {Colors["Green"]}check{Colors["Reset"]} your internet connection!')
                    input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to confirm if your internet connection works : ")
                    
                    if isConnected():
                        Download_Status(Status = 'Resume Downlad')
                    else:
                        raise SystemExit()
                
                except Exception as ex:
                    Quit(ExceptionName = ex(), Message = f'Cannot start or continue {Device.Model} firmware\'s download for an unknown error!')

            elif Status == 'Resume Download': #This is helpfull when the user gets its firmware file corrupted or stopped cause of internet or keyboard issue
                print(f'{Colors["Green"]}Resuming{Colors["Reset"]} the download...')
                try: #There could be an error here : if the download stops during 'download process' then it will run without issues BUT 
                    #if samloader was decrypting the file and something happens and we resume download then the file extension changes from .zip (changed from .enc4 by samloader during decrypting) then the decryption won't work...
                    os.system(f'samloader --dev-model {Device.Model} --dev-region {Device.Region} download --resume --fw-ver {versions} --do-decrypt --out-file {DownloadsFolder + "Firmware.zip.enc4"}')

                except ConnectionAbortedError:
                    print(f'Your internet connection has been stopped or aborted!\nPlease check your internet connection!')
                    input(f"\tPress {Colors['Green']}ENTER{Colors['Reset']} to confirm if your internet connection works : ")
                    
                    if isConnected():
                        Download_Status(Status = 'Resume Downlad') 
                    else:
                        raise SystemExit()

                except Exception as ex:
                    Quit(ExceptionName = ex(), Message = f'Cannot start or continue {Device.Model} firmware\'s download for an unknown error!')
        
        print(f'''
                    [Firmware Downloader] by (@Samloader)
        ''')
        Pip_Installer(Package = 'git+https://github.com/samloader/samloader.git', Package_Name = 'samloader')

        print(f'Your device ({Device.Model}) is currently running on Android V{Device.AndroidVersion} and {Device.PDA} version.\t[Region : {Device.Region}]\n')
        
        Download_Status('New Download')
        print(f'Firmware has been downloaded correctly!')
        sleep(1)
        
        ExtractZip(
            Zip_FileName = 'Firmware.zip',
            DestinationPath = DownloadsFolder,
            HasFolderInside = False
        )

        if askUser(f'Do you want to delete Firmware.zip to free up disk space in your pc [{Colors["Green"]}Recommended{Colors["Reset"]}] ?'):
            os.remove(f'{DownloadsFolder}Firmware.zip')

    def Firmware_Unpacking() -> None: #Returns a created folder "Extracted_Files" -> Downloads/Firmware/Extracted_Files
        print(f'\n{Colors["Green"]}Unpacking{Colors["Reset"]} Firmware files...')
        def lz4_Extractor(Files_Path: str) -> None:
            #Once the extraction is completed then the file will be in the same directory where it was
            for File in os.listdir(Files_Path):
                if File.endswith('.lz4'):
                    print(f'{Colors["Green"]}Extracting{Colors["Reset"]} {File}')
                    os.system(f'{ToolsFolder}lz4\\lz4.exe f"{Files_Path}\\{File}" -f')
                    os.remove(Files_Path + '\\' + File)

        
        Download(
            URLink = 'https://github.com/lz4/lz4/releases/download/v1.9.4/lz4_win64_v1_9_4.zip', 
            FileName = 'lz4.zip'
        )
        ExtractZip(
            Zip_FileName = 'lz4.zip',
            DestinationPath = ToolsFolder,
            HasFolderInside = True
        )

        for md5 in os.listdir(DownloadsFolder + 'Firmware\\'):
            Extract_tar(
                file_path = DownloadsFolder + 'Firmware\\' + md5, 
                extract_path = DownloadsFolder + f'Firmware\\Extracted_Files\\'
            )

        lz4_Extractor(Files_Path = DownloadsFolder + 'Firmware\\Extracted_Files\\')

    def Firmware_Flashing() -> None: #Need to fix heimdall : Need to know how it actually works : --resume and when --no-reboot...
        def CreateFlashingCommand(ExtractedFirmFiles_Path: str) -> str:
            #How's the pit file : 
            # --- Entry #0 ---
            # Binary Type: 0 (AP)
            # Device Type: 8 (Unknown)
            # Identifier: 80
            # Attributes: 2 (STL Read-Only)
            # Update Attributes: 1 (FOTA)
            # Partition Block Size/Offset: 0
            # Partition Block Count: 1204
            # File Size (Obsolete): 0
            # Partition Name: BOOTLOADER
            # Flash Filename: sboot.bin

            while True:
                Connection = subprocess.check_output('heimdall detect', stderr = True, shell = True)
                if Connection:
                    break
                print(f'{Colors["Red"]}Cannot{Colors["Reset"]} detect device...\nAre you sure that your device is in download mode or is connected to computer?')
                input(f"Press {Colors['Green']}ENTER{Colors['Reset']} to try again the connection : ")

            class Partition:
                def __init__(self, PartitionName, FileName) -> None:
                    self.PartitionName = PartitionName
                    self.FileName = FileName

            PitOutput = subprocess.check_output('heimdall print-pit --no-reboot', cwd = ToolsFolder + 'Heimdall\\', stderr = subprocess.STDOUT, shell = True) #encoding might be needed
            lines = [[line.rstrip() for line in PitOutput]]

            Partitions = list()

            for line in lines:
                if 'Partition Name' in PreviousLine:
                    PartitionName = line.split(': ')[1] #Partition Name: BOOTLOADER

                if 'Flash Filename' in line: #Flash Flename: sboot.bin
                    Partitions.append(Partition(PartitionName, FileName = line.split(': ')[1]))
                PreviousLine = line

            FilesInDirectory = [f for f in os.listdir(ExtractedFirmFiles_Path) if os.path.isfile(os.join(ExtractedFirmFiles_Path, f))]

            for Part in Partitions:
                if Part.FileName not in FilesInDirectory: #Checking whatever device's partition's file exists
                    Partitions.remove(Part)

            Command = 'heimdall flash --resume '
            for Part in Partitions:
                Command += f' --{Part.PartitionName} {Part.FileName}'

            return Command


        Check_AdbConnection(AdbOrFastboot='Adb', DriversInstaller=Install_SamsungUSBDrivers)
        os.system('adb reboot download')
        input(f"Press {Colors['Green']}ENTER{Colors['Reset']} if your phone is in {Colors['Blue']}Download Mode{Colors['Reset']} : ")
        #Need to use heimdall detect        #TODO: Check heimdall commands' output
        Heimdall_Command = CreateFlashingCommand(ExtractedFirmFiles_Path = DownloadsFolder + 'Firmware\\Extracted_Files')
        print(f'\n\n{Colors["Green"]}Starting{Colors["Reset"]} Flashing process...')
        os.system(Heimdall_Command)
        #Check if need to reboot or not!
        print(f'\n\n[{Colors["Green"]}Finished Flashing{Colors["Reset"]}!]')

        #TODO: Setup again and then call 'Device = Phone()' to refresh device informations.

    

    def Setup_MagiskManager() -> None:
        pass


    print(
        f'{Colors["Green"]}Installing{Colors["Reset"]} Samsung requirements...'
    )

#Maybe patch the image first, then flash stock firmware and then the patched imagie instead of let the user set up the device to then flash the patched image and to so format again the phone

    Install_AdbFastboot()
    SetupDeviceForUSBCommunication()
    Check_AdbConnection(AdbOrFastboot='Adb', DriversInstaller=Install_SamsungUSBDrivers)
    Unlock_Bootloader()
    Check_AdbConnection(AdbOrFastboot='Adb', DriversInstaller=Install_SamsungUSBDrivers)
    Download_Firmware()
    Firmware_Unpacking()
    Install_Heimdall()
    Firmware_Flashing()
    SetupDeviceForUSBCommunication()
    Check_AdbConnection(AdbOrFastboot='Adb', DriversInstaller=Install_SamsungUSBDrivers)
    Patch_Image_File(Device, BootImage_Name = 'boot.img') #Need to re-packthe archive to a tar file and then flash it.
    os.system(f'adb reboot download')
    Firmware_Flashing()
    SetupDeviceForUSBCommunication()
    Setup_MagiskManager()

