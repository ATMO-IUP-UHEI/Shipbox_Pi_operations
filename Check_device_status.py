import ping3
import time
import os
import datetime

# IP addresses of all devices 
DOAS_IP = '10.10.0.220' #DOAS fitlet
Tracker_IP = '10.10.0.200' #tracker fitlet
OPUS_IP = '10.10.0.4' #OPUS/EM27 fitlet

# name of the file, where the error log is written
filename = 'Ping_Relais_Log.txt'

# wait a few minutes in order to let the computers boot first
time.sleep(180)

while True:
    # get current computer time
    computer_time = datetime.datetime.now()
    computer_time = computer_time.strftime('%d%m%y %H%M%S')

    # general remark: ping3 can return either a float with the number of successfull pings or "False" or "None" in case of an error

    # check whether DOAS fitlet is working
    print('Check DOAS')
    return_ping = ping3.ping(DOAS_IP) # ping DOAS computer
    if return_ping == False:
        # if "False": DOAS computer is not working -> trigger relais to restart it
        print('DOAS not found')
        # write entry into error log
        file = open(filename, 'a+')
        string = computer_time + ': DOAS computer not responding, trigger relais \n'
        file.write(string)
        file.close()
        # trigger relais
        os.system('python3 /home/shippi/Trigger_Serial.py z')
    try:
        # if pinging returns something that cannot be converted into a float: DOAS computer not working -> trigger relais to restart it
        float(return_ping)
    except:
        print('DOAS not found')
        # write entry into error log
        file = open(filename, 'a+')
        string = computer_time + ': DOAS computer not responding, trigger relais \n'
        file.write(string)
        file.close()
        # trigger relais
        os.system('python3 /home/shippi/Trigger_Serial.py z')

    # check whether the tracker computer is working
    print('Check tracker')
    return_ping = ping3.ping(Tracker_IP) # ping tracker computer
    if return_ping == False:
        # if "False": tracker computer not working -> trigger relais to restart it
        print('Tracker not found')
        # write entry into error log
        file = open(filename, 'a+')
        string = computer_time + ': Tracker computer not responding, trigger relais \n'
        file.write(string)
        file.close()
        # trigger the relais
        os.system('python3 /home/shippi/Trigger_Serial.py x')
    try:
        # if ping returns something that cannot be converted to a float: tracker computer not working -> trigger relais to restart it
        float(return_ping)
    except:
        print('Tracker not found')
        # write entry into error log
        file = open(filename, 'a+')
        string = computer_time + ': Tracker computer not responding, trigger relais \n'
        file.write(string)
        file.close()
        # trigger relais
        os.system('python3 /home/shippi/Trigger_Serial.py x')

    # check whether the OPUS fitlet is working
    print('Check OPUS')
    return_ping = ping3.ping(OPUS_IP) # ping OPUS computer
    if return_ping == False:
        # if "False": OPUS computer not working -> trigger relais
        print('OPUS not found')
        # write entry into error log
        file = open(filename, 'a+')
        string = computer_time + ': OPUS computer not responding, trigger relais \n'
        file.write(string)
        file.close()
        # trigger relais
        os.system('python3 /home/shippi/Trigger_Serial.py y')
    try:
        # if not a float: OPUS computer not working -> trigger relais
        float(return_ping)
    except:
        print('OPUS not found')
        # write entry into error log
        file = open(filename, 'a+')
        string = computer_time + ': OPUS computer not responding, trigger relais \n'
        file.write(string)
        file.close()
        # trigger relais
        os.system('python3 /home/shippi/Trigger_Serial.py y')

    # wait for 30 minutes before checking again
    time.sleep(1800)


    


