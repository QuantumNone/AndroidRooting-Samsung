import Scripts.AutoRootUtilities as rutil

#We start by checking everything is configured correctly OK

mode = rutil.getPlatform()



if not rutil.isSetup():
    #TODO: Do setup
    print("To configure device specific options and drivers, or to update any of the installed utilities, run this program again.")
else:
    print("Setup has been completed - Opening configuration menu")
    #TODO: Configuration Menu