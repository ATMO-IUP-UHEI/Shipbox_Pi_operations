import smbus2
import bme280
import datetime
import time
import serial
import os
import Adafruit_DHT

# start main function
def main():
    """ USER DEFINED PARAMETERS """
    file_path_local = '/home/shippi/Documents/Measurements/' # path in which data is saved
    prefix          = 'DATA_' # prefix for the data file

    interval        = 10                # interval between measurements in seconds
    sensorpin       = 4                 # pin of inside T sensor
    port            = 1                 # port of BME280-sensors
    address1        = 0x76              # address of BME280-sensors
    address2        = 0x77
    bus             = smbus2.SMBus(port) # bus of BME280 sensor
    # get calibration parameters from the sensors
    calibration_params1 = bme280.load_calibration_params(bus,address1)
    calibration_params2 = bme280.load_calibration_params(bus,address2)

    # set default
    default         = -9999

    # port of the GPS sensor
    port_GPS = '/dev/ttyAMA0'
    GPS = False #default for GPS

    # infinite loop
    while True:
        # Find Date for filename
        today = datetime.datetime.today()
        filename = prefix + today.strftime('%F') + '.txt'
        # save to local folder; open file
        local   = open((file_path_local + filename), "a+")
        # write header if file is empty
        if os.stat((file_path_local + filename)).st_size == 0:
            header  = 'Computer time \t GPS time \t GPS \t latitude \t longitude \t horizontal dilution \t altitude \t geoid separation \t GPS quality \t Num. of Sat. \t speed \t course \t pT_76 \t T_76 \t p_76 \t pT_77 \t T_77 \t p_77 \t Hum_in \t T_in \n'
            local.write(header)
        try:
            print 'DHT'
            # get data from internal sensor
            try:
                humidity, tinside = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, sensorpin)
            except:
                print 'DHT failure'
                # use default if no data available
                humidity = default
                tinside = default

            print 'IO1'
            # get data from BME280 sensor 1
            try:
                sensor1         = bme280.sample(bus,address1,calibration_params1)
                degrees1        = sensor1.temperature
                hectopascals1   = sensor1.pressure
                IO1 = True
            except IOError:
                # use default if sensor not available
                IO1             = False
                degrees1        = default
                hectopascals1   = default

            print 'IO2'
            # get data from BME280 sensor 2
            try:
                sensor2         = bme280.sample(bus,address2,calibration_params2)
                degrees2        = sensor2.temperature
                hectopascals2   = sensor2.pressure
                IO2             = True
            except IOError:
                # use default if sensor not available
                IO2             = False
                degrees2        = default
                hectopascals2   = default

            print 'GPS'
            # get GPS data
            try:
                # open serial
                ser=serial.Serial(port_GPS,baudrate=9600,timeout=0.5)
                while True:
                    # read lines from serial until GGA line is reached
                    data = ser.readline()
                    if data[0:6] == b'$GPGGA':
                        # convert data to UTF-8
                        decoded_data = data.decode('UTF-8')
                        # get variables from NMEA-string
                        GPS_time, lat, lat_dir, lon, lon_dir, quality, num_sat, hor_dil, alt, geoid_sep = GPGGA_parser(decoded_data)
                        lat = lat + lat_dir
                        lon = lon + lon_dir
                        print 'GPS found'
                        break
                while True:
                    # read lines from serial until RMC line is reached
                    data = ser.readline()
                    if data[0:6] == b'$GPRMC':
                        # convert data to UTF-8
                        decoded_data = data.decode('UTF-8')
                        # get variables from NMEA-string
                        status, GPS_time, lat, lat_dir, lon, lon_dir, speed, course, date_GPS = GPRMC_parser(decoded_data)
                        lat = lat + lat_dir
                        lon = lon + lon_dir
                        # get GPS status from status variable in NMEA string
                        if status == 'A':
                            GPS = True
                        else:
                            GPS = False
                        break
            except:
                # use default if GPS is not working
                GPS_time = '999999.999'
                lat = default
                lon = default
                quality = default
                num_sat = default
                hor_dil = default
                alt = default
                geoid_sep = default
                speed = default
                course = default
                GPS = False
                date_GPS = '999999'
            if GPS == False:
                # use default if GPS quality is bad 
                GPS_time = '999999.999'
                lat = default
                lon = default
                alt = default
                geoid_sep = default
                speed = default
                course = default
                date_GPS = '999999'
            GPS_datetime = date_GPS + ' ' + GPS_time

            print 'get computer time'
            # get computer time
            computer_time = datetime.datetime.now()
            computer_time = computer_time.strftime('%d%m%y %H%M%S')

            print 'write entry'
            # write string with all data
            data_line = computer_time + "\t" + GPS_datetime + "\t" +  str(GPS) + "\t" + str(lat) + "\t" + str(lon) + "\t"  + str(hor_dil) + "\t" + str(alt) + "\t" + str(geoid_sep) + "\t" + str(quality) + "\t" + str(num_sat) + "\t" + str(speed) + "\t" + str(course) + "\t" + str(IO1) + "\t" + str(degrees1) + "\t" + str(hectopascals1) + "\t" + str(IO2) + "\t" + str(degrees2) + "\t" + str(hectopascals2) + "\t" + str(humidity) + "\t" + str(tinside) + "\n"
            # write string to file
            local.write(data_line)
            local.flush()
            # set GPS variable back to default
            GPS = False
            # close file 
            local.close()

            # print data string
            print data_line
            # wait for specified interval before data is read again from all sensors
            wait_time = interval
            print 'sleep'
            time.sleep(wait_time)
        except:
            # wait for 30 seconds if exception has ocurred
            print 'Exception has ocurred: sleep 30 seconds'
            time.sleep(30)
            pass

# functon to find the nth comma in a string
# the entries in the NMEA protocol are written with commas in between; the number of commas is always the same
# the parser calls this function to get the position of the element
def find_nth_comma(string, n):
    index = string.find(',')
    while index >=0 and n > 1:
        index = string.find(',', index+1)
        n -= 1
    return index

# function to convert a RMC string to the variables of interest
# based on the NMEA protocol
# the position of the comma is used to identify the elements
# input format: string in UTF-8
def GPRMC_parser(RMC_string):
    #see NMEA protocol for documentation
    index_start = find_nth_comma(RMC_string,2)
    index_stop = find_nth_comma(RMC_string,3)
    status = RMC_string[index_start+1:index_stop]
    index_start = find_nth_comma(RMC_string,1)
    index_stop = find_nth_comma(RMC_string,2)
    time_GPS = RMC_string[index_start+1:index_stop]
    index_start = find_nth_comma(RMC_string,3)
    index_stop = find_nth_comma(RMC_string,4)
    latitude = RMC_string[index_start+1:index_stop]
    index_start = find_nth_comma(RMC_string,4)
    index_stop = find_nth_comma(RMC_string,5)
    latitude_dir = RMC_string[index_start+1:index_stop]
    index_start = find_nth_comma(RMC_string,5)
    index_stop = find_nth_comma(RMC_string,6)
    longitude = RMC_string[index_start+1:index_stop]
    index_start = find_nth_comma(RMC_string,6)
    index_stop = find_nth_comma(RMC_string,7)
    longitude_dir = RMC_string[index_start+1:index_stop]
    index_start = find_nth_comma(RMC_string,7)
    index_stop = find_nth_comma(RMC_string,8)
    speed = RMC_string[index_start+1:index_stop]
    index_start = find_nth_comma(RMC_string,8)
    index_stop = find_nth_comma(RMC_string,9)
    course = RMC_string[index_start+1:index_stop]
    index_start = find_nth_comma(RMC_string,9)
    index_stop = find_nth_comma(RMC_string,10)
    date_GPS = RMC_string[index_start+1:index_stop]
    return status, time_GPS, latitude, latitude_dir, longitude, longitude_dir, speed, course, date_GPS

# function to convert a GGA string to the variables of interest
# based on the NMEA protocol
# the position of the comma is used to identify the elements
# input format: string in UTF-8
def GPGGA_parser(GGA_string):
    index_start = find_nth_comma(GGA_string,1)
    index_stop = find_nth_comma(GGA_string,2)
    time_GPS = GGA_string[index_start+1:index_stop]
    index_start = find_nth_comma(GGA_string,2)
    index_stop = find_nth_comma(GGA_string,3)
    latitude = GGA_string[index_start+1:index_stop]
    index_start = find_nth_comma(GGA_string,3)
    index_stop = find_nth_comma(GGA_string,4)
    latitude_dir = GGA_string[index_start+1:index_stop]
    index_start = find_nth_comma(GGA_string,4)
    index_stop = find_nth_comma(GGA_string,5)
    longitude = GGA_string[index_start+1:index_stop]
    index_start = find_nth_comma(GGA_string,5)
    index_stop = find_nth_comma(GGA_string,6)
    longitude_dir = GGA_string[index_start+1:index_stop]
    index_start = find_nth_comma(GGA_string,6)
    index_stop = find_nth_comma(GGA_string,7)
    pos_ind = GGA_string[index_start+1:index_stop]
    index_start = find_nth_comma(GGA_string,7)
    index_stop = find_nth_comma(GGA_string,8)
    sat_num = GGA_string[index_start+1:index_stop]
    index_start = find_nth_comma(GGA_string,8)
    index_stop = find_nth_comma(GGA_string,9)
    hdop = GGA_string[index_start+1:index_stop]
    index_start = find_nth_comma(GGA_string,9)
    index_stop = find_nth_comma(GGA_string,10)
    alt = GGA_string[index_start+1:index_stop]
    index_start = find_nth_comma(GGA_string,11)
    index_stop = find_nth_comma(GGA_string,12)
    geoid_sep = GGA_string[index_start+1:index_stop]
    return time_GPS, latitude, latitude_dir, longitude, longitude_dir, pos_ind, sat_num, hdop, alt, geoid_sep

if __name__ == "__main__": #call function main
    main()
