import subprocess
import re
from time import sleep
time = 0.5
print("\nStarting scan...")
output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
names = (re.findall("All User Profile     : (.*)\r", output))
networks = list()
if len(names) > 0 :
    for name in names:
        profile = dict()
        info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Security key           : Absent", info):
            continue
        else:
            profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            # print(profile_info_pass)
            if password == None:
                profile["password"] = None
            else:
                profile["password"] = password[1]
            networks.append(profile)
    for network in networks:
        print()
        print("SSID Name : '", network["ssid"], "', Key Content : '",  network["password"], "'")
        sleep(time)
    print("\nCompleted...")
    sleep(time)