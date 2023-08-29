import serial
import sys
import time

# get first input argument -> number of relais
command = sys.argv[1]

#port number
port = '/dev/ttyACM1'

#open serial
print('Open serial')
ser = serial.Serial(port, 9600, timeout=1)

#write command
print('Reset relay number '+str(command))
ser.write(str(command))
print('Reset in progress. Please wait...')
time.sleep(300)
print('Resetting relay finished')

#close serial
ser.close()
print('Serial closed')

