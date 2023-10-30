import serial
import sys
import time

#port number
port = '/dev/ttyUSB0'

#open serial
print('Open serial')
ser = serial.Serial(port,9600,timeout=1)
time.sleep(5)

# Get the current time and format it as a string
current_time = time.strftime("%Y-%m-%d %H:%M:%S")

#write command to serial
print('Reset RTC')
ser.write(b'+')
ser.write(current_time.encode('utf-8') + b'\n')
print('Reset in progress. Please wait...')
time.sleep(10)
print('Resetting RTC finished')

#close serial
ser.close()
print('Serial closed')
