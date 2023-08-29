import RPi.GPIO as GPIO
import time
import datetime

time.sleep(60) #start EM27 only 1 minute after boot

# GPIO number instead of Board number
GPIO.setmode(GPIO.BCM)

Pin = 17

GPIO.setup(Pin, GPIO.OUT) # set pin to output
GPIO.output(Pin, GPIO.HIGH) # set pin to high -> switch relais on

# get current computer time
computer_time = datetime.datetime.now()
computer_time = computer_time.strftime('%d%m%y %H%M%S')

# write to relais log
filename = '/home/shippi/Documents/Relais_log.txt'
file = open(filename, 'a+')
string = computer_time + ': ' + 'EM27 relais on \n'
file.write(string)
file.close()

