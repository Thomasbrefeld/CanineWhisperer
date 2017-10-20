import os, struct, math, smtplib
import RPi.GPIO as GPIO
from time import *

food_motor = 40
water_pump = 38
water_sensor = 36

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
        scale_input = ((list[3][1]) % 256)

def Current_Time():
        global Stime
        Stime = int(strftime("%S"))
        global Mtime
        Mtime = int(strftime("%M"))
        global Htime
        Htime = int(strftime("%H"))
        print(Htime, ':', Mtime, '.', Stime)

def Feed():
        Read_Scale()
        starting_amount = scale_input
        start_time = int(time())
        email("feeding")
        print('starting scale amount:', starting_amount, ' --- Htime:', Htime, ' --- start time:', start_time)
        GPIO.output(food_motor, True)
        while ((scale_input < 35) and (int(time()) - start_time < 15)):
                Read_Scale()
        GPIO.output(food_motor, False)
        amount_added = int(scale_input - starting_amount)
        print('scale amount:', scale_input, ' --- Htime:', Htime, ' --- time():', int(time()))
        if (int(time()) - start_time > 15):
                email("feeding-time")
        else:
                email("feeding ending")
        Current_Time()

def Water():
        water_level = GPIO.input(water_sensor)
        sleep(.1)
        Current_Time()
        email("watering")
        GPIO.output(water_pump, True)
        start_time = int(time())
        print('Water sensor level:', water_level, ' --- Htime:', Htime, ' --- start time:', start_time)
        while ((water_level != 1) and (int(time()) - start_time < 6)):
                water_level = GPIO.input(water_sensor)
        GPIO.output(water_pump, False)
        email("water ending")
        Current_Time()
        print('Water sensor level:', water_level, ' --- Htime:', Htime, ' --- time():', int(time()))

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
        while True:
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
                        if (scale_input < 35):
                                email('updating/rebooting')
                                os.system('sudo reboot -r now')
                sleep(1)

except Exception as e:
        email('error')
        print(e)
        GPIO.output(food_motor, False)
        GPIO.output(water_pump, False)
        GPIO.cleanup()
email("Program exited")
GPIO.cleanup()
