import RPi.GPIO as GPIO

# GPIO number instead of Board number
GPIO.setmode(GPIO.BCM)

Pin = 17

GPIO.setup(Pin, GPIO.OUT) # set pin to be output
GPIO.output(Pin, GPIO.HIGH) # set pin to high -> switch relais on
