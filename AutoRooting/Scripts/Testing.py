import subprocess

def Check_AdbConnection() -> bool:
    try:
        AdbDevices_output = subprocess.check_output("adb devices", stderr = subprocess.STDOUT, shell = True).strip()
        print(AdbDevices_output[-6:])
        if AdbDevices_output[-6:] == b'device':
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        pass

print(Check_AdbConnection())
