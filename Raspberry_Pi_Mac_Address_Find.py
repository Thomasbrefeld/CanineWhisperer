
import bluetooth

devices = False
i = 0

while (not(devices)) and (i < 5) :
        devices = bluetooth.discover_devices(duration = 8, lookup_names = True,$
        i = i + 1
        print(i)

with open('MacAddress.txt', 'w') as file:
        if(devices):
                file.write(devices[0][0])
        else:
                file.write('None')
