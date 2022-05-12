import RPi.GPIO as GPIO
import dht11
import LCD1602
import time
import datetime

def setup(upper, lower):
	LCD1602.init(0x27, 1)	# init(slave address, background light)
	LCD1602.write(0, 0, upper)
	LCD1602.write(1, 1, lower)
	time.sleep(2)

def destroy():
	LCD1602.clear()

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=4)

try:
	while True:
	    result = instance.read()
	    if result.is_valid():
	        print("Last valid input: " + str(datetime.datetime.now()))
	        print("Temperature: %-3.1f C" % result.temperature)
	        print("Humidity: %-3.1f %%" % result.humidity)
	        date = datetime.datetime.now()
	        upper = 'Date {0}/{1} {2}:{3}'.format(date.month, date.day, date.hour, date.minute)
	        lower = 'T:{0}C H:{1}%'.format(result.temperature, result.humidity)
	        setup(str(upper) ,str(lower))
	        
	    time.sleep(28)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
    destroy()