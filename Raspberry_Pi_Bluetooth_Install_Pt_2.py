import os

Is_Mac_Address = False

os.system("sudo bluetoothctl")
os.system("power on")
os.system("pairable on")
os.system("agent on")
os.system("default-agent")

os.system("yes")
os.system("yes")

with open('MacAddress.txt', 'r') as file:
    Mac_Address = file.read()

if(Mac_Address == "None"):
    os.system("sudo python Raspberry_Pi_Mac_Address_Find.py")
    if(Mac_Address == "None"):
        print("Error Could not find device")
    else:
        Is_Mac_Address = True
else:
    Is_Mac_Address = True

if(Is_Mac_Address):
    os.system("trust " + Mac_Address)
    os.system("exit")
    os.system("wget https://bootstrap.pypa.io/get-pip.py")
    os.system("sudo python get-pip.py")
    os.system("git clone https://github.com/karulis/pybluez.git")
    os.system("sudo python setup.py install")
    with open('bluetooth_adv', 'w') as file:
        file.write('sudo hciconfig hci0 piscan \nsudo sdptool add SP')
    os.system("sudo chmod +x bluetooth_adv")
    os.system("sudo ./bluetooth_adv")
    os.system("sudo python pybluez/examples/simple/rfcomm-server.py")

print("Program Finnished: Exiting")
    
    

        
        
