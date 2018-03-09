
import os

os.system("sudo apt-get update -y")
os.system("sudo apt-get upgrade -y")
os.system("sudo apt-get autoremove -y")

os.system("sudo apt-get install python-dev libbluetooth-dev -y")

f = open("/lib/systemd/system/bluetooth.service", "r")
lines = f.readlines()
f.close()

f = open("/lib/systemd/system/bluetooth.service", "w")
for line in lines:
        if line != "ExecStart=/usr/lib/bluetooth/bluetoothd" + "\n":
                f.write(line)
        else:
                f.write('ExecStart=/usr/lib/bluetooth/bluetoothd -C' + '\n')

f.close()

os.system("sudo reboot")
