from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import RPi.GPIO as GPIO
import dht11
import time
import datetime

# 初期化
myMQTTClient = AWSIoTMQTTClient("raspi")

# MQTTクライアントの設定
myMQTTClient.configureEndpoint("endpoint_URL", 443)
myMQTTClient.configureCredentials("/xxx/xxx/certs/AmazonRootCA1.pem", "/xxx/xxx/certs/xxx-private.pem.key", "/xxx/xxx/certs/xxx-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

# Connect to AWS IoT endpoint and publish a message
myMQTTClient.connect()
print ("Connected to AWS IoT")


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
	        myMQTTClient.publish("awsiot/test", json.dumps({"Temperature":result.temperature, "Humidity":result.humidity}), 0)

	    time.sleep(10)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
    myMQTTClient.disconnect()