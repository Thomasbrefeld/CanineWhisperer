import os, struct, math, smtplib
import RPi.GPIO as GPIO
from time import *

food_motor = 40
water_pump = 38
water_sensor = 36
critical_error_exit = 0

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(food_motor, GPIO.OUT)
GPIO.setup(water_pump, GPIO.OUT)
GPIO.setup(water_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(food_motor, False)
GPIO.output(water_pump, False)

def Read_Scale():
        fd = os.open("/dev/usb/hiddev0", os.O_RDONLY)
        hiddev_event_fmt = "Ii"
        list = []
        for i in range(4):
                list.append(struct.unpack(hiddev_event_fmt, os.read(fd,struct.calcsize(hiddev_event_fmt))))
        global scale_input
        if (scale_input > 100):
                email('ERROR: Scale input undefined. System need manual reboot.')
                global critical_error_exit = 1
        scale_input = ((list[3][1]) % 256)

def Current_Time():
        global Stime
        Stime = int(strftime("%S"))
        global Mtime
        Mtime = int(strftime("%M"))
        global Htime
        Htime = int(strftime("%H"))

def Feed():
        Read_Scale()
        starting_amount = scale_input
        start_time = int(time())
        email("feeding initialized")
        GPIO.output(food_motor, True)
        while ((scale_input < 35) and (int(time()) - start_time < 15)):
                Read_Scale()
        GPIO.output(food_motor, False)
        amount_added = int(scale_input - starting_amount)
        if (int(time()) - start_time > 15):
                email("ERROR: Feeding exited based on allotted time. System needs manual reboot.")
        else:
                email("Feeding exited normally")
        Current_Time()

def Water():
        water_level = GPIO.input(water_sensor)
        sleep(.1)
        Current_Time()
        email("watering")
        GPIO.output(water_pump, True)
        start_time = int(time())
        while ((water_level != 1) and (int(time()) - start_time < 6)):
                water_level = GPIO.input(water_sensor)
        GPIO.output(water_pump, False)
        if(int(time()) - start_time > 6):
                email('CRITICAL ERROR: Watering exited based on allotted time. System needs a immediate reboot.')
                #global critical_error_exit = 1
        else:
                email('Watering exited at')
        Current_Time()

def email(sel_file):
        mail = smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        mail.login('sciencefair930@gmail.com','Buckwheat2016')
        mail.sendmail('sciencefair930@gmail.com','3133007575@vtext.com',sel_file)
        mail.close()

try:
        Current_Time()
        water_level = GPIO.input(water_sensor)
        if (water_level != 1):
                Water()
        water_mark = Htime
        Feed()
        food_mark = Htime
        while (critical_error_exit == 0):
                Current_Time()
                water_level = GPIO.input(water_sensor)
                if ((water_level != 1) and (water_mark != Htime)):
                        water_mark = Htime
                        Water()
                if ((Htime == 22) and (food_mark != 22)):
                        Feed()
                        food_mark = 22
                if ((Htime == 11) and (food_mark != 11)):
                        Feed()
                        food_mark = 11
                if (Htime == 8):
                        Read_Scale()
                        if (scale_input <= 2):
                                email('updating/rebooting')
                                os.system('sudo reboot')
                sleep(1)

except Exception as e:
        email('error')
        print(e)
        GPIO.output(food_motor, False)
        GPIO.output(water_pump, False)
email("Program exited")
GPIO.cleanup()
os.system('sudo reboot')
