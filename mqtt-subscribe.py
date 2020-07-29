import paho.mqtt.client as mqtt #import the client1
import time
############
def on_connect(client, userdata, flags, rc):
    print("Connected with code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
    client.subscribe("#")

def on_message(client, userdata, message):
    print("\n")
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("\n")
########################################
broker_address="34.72.249.18"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()