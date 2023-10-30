# README

This repository contains all code installed on the Raspberry Pi in the current shipbox version. 

## Contents

1. Logging.py: this python 2 script logs the data from
    + the external BME280 temperature and pressure sensors
    + the internal temperature and humidity sensor
    + the GPS receiver
2. SpecOn.py: this script switches the EM27 on using a relay.
3. SpecOff.py: this script switches the EM27 off using a relay.
4. SpecOn_Autostart.py: this is a derivative of SpecOn.py that can be used for the autostart. It switches the EM27 and the DOAS on and writes an entry into a relay log file. It also switches the DOAS off again after 3 minutes, if the DOAS fitlet has not started.
5. Trigger_Serial.py: this code triggers the Arduino to reset a relay. Command: python3 Trigger_Serial.py <letter for relais>. The following letters do exist: 
    +  z -> DOAS computer
    +  x -> Tracker computer
    +  y -> OPUS computer
    +  q -> Raspberry Pi
6. Check_device_status.py: this code checks every 30 minutes whether the three fitlets are running. If not, it triggers the relais and restarts the respective computer by switching the power off and on. 
7. DOASOff.py: this script switches the DOAS spectrometer off. 
8. DOASOn.py: this script switches the DOAS spectrometer on. 
9. Reset_RTC.py: this code resets the RTC of the reset Arduino to the current time. 

## Prerequisites

1. Logging.py:
    + Python 2.7 (this code does NOT work with python 3)
    + smbus2 package
    + RPi.bme280 package
    + pyserial package
    + Adafruit_DHT package (python 2 only!)
    + Log-file can be found in '/home/shippi/Documents/Measurements/'. This directory needs to exist.
    + GPS needs to be found at '/dev/ttyAMA0'. Change otherwise.
    + GPS needs to be GPS-receiver and not a GNSS-receiver. 
    + Internal temperature sensor: default is pin 4. Change otherwise.
    + BME280 sensors: default port is 1 and addresses are 0x76 and 0x77. Change otherwise. 
2. SpecOn.py:
    + Python 3
    + RPi.GPIO package
    + Relais connected to pin 17
3. SpecOff.py:
    + Python 3
    + RPi.GPIO package
    + Relais connected to pin 17
4. SpecOn_Autostart.py:
    + Python 3
    + RPi.GPIO package
    + ping3 package
    + Relais connected to pin 17 for the EM27 and pin 18 for the DOAS
    + Relais log can be found in '/home/shippi/Documents/Relais_log.txt'. This folder needs to exist. 
5. Trigger_Serial.py:
    + Python 3
    + pyserial package
    + Arduino connected via USB
    + Serial port needs to be defined. Default: '/dev/ttyUSB0'. Change if other port is used.
    + Baudrate of serial: 9600. 
6. Check_device_status.py: 
    + Python 3
    + ping3 package
7. DOASOff.py:
    + Python 3
    + RPi.GPIO package 
    + Relais connected to pin 18
8. DOASOn.py:
    + Python 3
    + RPi.GPIO package 
    + Relais connected to pin 18
9. Reset_RTC.py:
    + Python 3
    + pyserial package

## Acknowledgement

1. Logging.py:
    + The GPS part of this code is a python 2 derivative of pyGPS. See pyGPS documentation for more information.
    + The general structure of this code is based on the old Raspberry Pi repository from Marvin Knapp. However, all modules used have been changed since the old BME280 package and the old DHT package as well as the old GPSD package were not compatible anymore with the new Raspberry Pi generation.
2. SpecOn.py: written by Marvin Knapp.
3. SpecOff.py: written by Marvin Knapp.
4. SpecOn_Autostart.py: partly based on SpecOn.py written by Marvin Knapp.
5. Trigger_Serial.py: None. 
6. Check_device_status.py: None. 
7. DOASOff.py: based on SpecOff.py by Marvin Knapp.
8. DOASOn.py: based on SpecOn.py by Marvin Knapp.
9. Reset_RTC.py: None. 
