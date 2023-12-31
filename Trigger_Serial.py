import serial
import sys
import time

# get first input argument -> number of relais
command = sys.argv[1]
print(command)

#port number
port = '/dev/ttyUSB0'

#open serial
print('Open serial')
ser = serial.Serial(port,9600,timeout=1)
time.sleep(5)

#write command
print('Reset relay number '+str(command))
ser.write(command.encode('utf-8'))
print('Reset in progress. Please wait...')
time.sleep(60)
print('Resetting relay finished')

#close serial
ser.close()
print('Serial closed')
