import RPi.GPIO as GPIO
import time
import datetime
import ping3

time.sleep(60) #start EM27 only 1 minute after boot

DOAS_IP = '10.10.0.220' #IP of DOAS control computer

# GPIO number instead of Board number
GPIO.setmode(GPIO.BCM)

Pin = 17 #relais pin for EM27
Pin_DOAS = 18 #relais pin for DOAS

GPIO.setup(Pin, GPIO.OUT) # set pin to output
GPIO.output(Pin, GPIO.HIGH) # set pin to high -> switch relais on

GPIO.setup(Pin_DOAS, GPIO.OUT) # set pin to output
GPIO.output(Pin_DOAS, GPIO.LOW)

# get current computer time
computer_time = datetime.datetime.now()
computer_time = computer_time.strftime('%d%m%y %H%M%S')

# write to relais log
filename = '/home/shippi/Documents/Relais_log.txt'
file = open(filename, 'a+')
string = computer_time + ': ' + 'EM27 relais on, DOAS relais on \n'
file.write(string)
file.close()

time.sleep(120) #wait for 120 seconds to have enough time for DOAS computer to boot

return_ping = ping3.ping(DOAS_IP) # ping DOAS computer

# switch DOAS relais off if DOAS computer does not respond
# result from ping is delay if computer responds or either False or None
if return_ping == False:
    GPIO.output(Pin_DOAS, GPIO.HIGH)
    file = open(filename, 'a+')
    string = computer_time + ': DOAS computer not responding, switch DOAS off \n'
    file.write(string)
    file.close()
try:
    float(return_ping)
except:
    GPIO.output(Pin_DOAS, GPIO.HIGH)
    file = open(filename, 'a+')
    string = computer_time + ': DOAS computer not responding, switch DOAS off \n'
    file.write(string)
    file.close()




