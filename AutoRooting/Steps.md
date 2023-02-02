
#Need to do some setups before starting the program :
#In case the phone needs to be fixed, in which way did it got break? OTA updates?
#Computer RAM > 2 Gb

#NOT ALL DEVICES CAN BE ROOTED EVEN IF OEM UNLOCKING IS AVAILABLE
#Make a list of known not rootable devices
#Oppo F19 CPH2219


#The program should be built by defining functions inside the Main.py file because if we create modules to there create functions (like Download_and_Extract.py) could give logical issues or pc performance issues.
#The program should be built with a Main Class as we need to call some functions many times, like :
#Func1 : check if device rebooted into fastbootMode, if not then call again Func1

#First step :
    #Get all device informations to then download the correct device firmware
    #These informations can be found on your phone manually in settings > about my phone
    #Every phone has different informations but the ones that every device has are :
        #Full device model name : "Huawei Mate 10 Pro"
        #Name of the model : "BLA-L09"
        #Build Number : "9.1.0.342(C55E7R1P12)"
        #Android Version : "Android 9"
        #IMEI : "866347812340982"

    #From this step we'll have to figure out what is the device the program is going to root.
    #We need to know if the phone can be "unlocked" by checking if the option "OEM unlocking" in developer options in settings is available.
    #If yes then the phone can be unlocked and so allows flashing unofficial files, else the phone cannot be rooted.


#Second Step :
    #Since we know from First step the device model name, we have to download the device firmware and every brand has it's own website.
    #For some models like samsung there are already programs that automatically downloads firmware from the website by giving them the device informations.
    #The problem is how we are going to work with them and if APIs exists...
    #As the firmware is normally of the size of 4-8 Gb then there could be issues with downloading like missing internet etc...

    #Examples of models firmware :
        #Samsung : https://www.sammobile.com/samsung/galaxy-a21/firmware/SM-A215U/USC/download/A215USQS7BVE1/1651607/
        #Xioami : https://xiaomifirmwareupdater.com/miui/mojito/stable/V13.0.6.0.SKGEUXM/
        #Oneplus : https://www.oneplus.com/it/support/softwareupgrade/details?code=PM1605596915581
        #Huawei : http://huawei-update.com/device-list/bla-l29


    #The firmwares are needed to flash them (will erase phone data) to then extract boot.img (Image that tells the device how to boot)
    #And every device firmware has its own firmware compression, for example Oneplus has payload.bin, Samsung has AP.MD5 or AP.tar
    #OR we can download directly the boot.img from any website but this is dangerouse because the image could be too old or too new and cause device brick

#Third Step :
    #Download Softwares needed to communicate with android (Flash files or get device infos)
    #Main program is ADB&Fastboot   (Terminal GUI)
    #Others like Odin for samsung that allows flashing
    #The problem on the comunication with device are USB drivers and all models have their own drivers...


# Download_and_Extract("https://dl.google.com/android/repository/platform-tools-latest-windows.zip", "%USERPROFILE%\Downloads")


#Fourth step
    #Unlock device bootloader to allow file flashing :
    #Every device model has its own way to unlock bootloader but the most ones uses Adb&Fastboot
        #Xioami : https://en.miui.com/unlock/download_en.html
        #Samsung : https://www.youtube.com/watch?v=cMN0WWtu-zo
        #Oneplus : Fastboot
        #Oppo : Fastboot
    
    #Some deivces need an unlock code to unlock bootlader. This code can be get by model website or by payment services (we will not working with these devices or at least we can check if bootlaoder is already unlocked (as we suggest the user a guide to unlock manually) and then continue with rooting
    #Huawei : Most hard to unlock : need to pay third part software to crack unlock code
    #Oneplus : too

#Fifth step 
    #Install magisk manager (the app that will patch boot.img to boot itself on phone boots and gets device full control (root))
    #Patch the file image automatically or give to user some informations to user on how to patch
    #transfer patched image to computer
    #With the tool used from the model to flash files, flash patched image "fastboot flash {boot or boot_Ramdisk} Magisk-Patched.img"

#Final setup and all is done...
