import paho.mqtt.client as paho
from paho import mqtt
import time
import threading
from smartNursingBackend.post_data import postData
from smartNursingBackend.settings import logger
import datetime
class HiveMqtt():
    _mqttinstance = None
    _client = None


    def __init__(self):
        if self._client == None:
            # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
            # userdata is user defined data of any type, updated by user_data_set()
            # client_id is the given name of the client
            logger.warning("Establishing Connection to the MQTT "+str(datetime.datetime.now())+' hours!')
            try:
                self._client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
                self._client.on_connect = self.on_connect

                # enable TLS for secure connection
                self._client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
                # set username and password
                self._client.username_pw_set("iot-enabled", "sirsamyan")
                # connect to HiveMQ Cloud on port 8883 (default for MQTT)
                self._client.connect("9de0b5ebb7c94ca2b0a8babceed188fa.s2.eu.hivemq.cloud", 8883)

                # setting callbacks, use separate functions like above for better visibility
                self._client.on_subscribe = self.on_subscribe
                self._client.on_message = self.on_message

                # subscribe to all topics of encyclopedia by using the wildcard "#"
                self._client.subscribe("activityDetection", qos=1)


                # Start the MQTT loop to establish a connection and handle incoming messages

                self._client.loop_start()
                # client.loop_stop()
            except Exception as e:
                logger.warning("Error Establishing Connection to the MQTT "+str(e)+str(datetime.datetime.now())+' hours!')
    def __new__(self):
        if not self._mqttinstance:
            print("CREATING CLASS")
            self._mqttinstance = super().__new__(self)
        return self._mqttinstance

    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self,client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self,client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    # print which topic was subscribed to
    def on_subscribe(self,client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    # print message, useful for checking if it was successful
    def on_message(self,client, userdata, msg):
        data = {"activities":msg.payload.decode()}
        try:
            postThread=threading.Thread(target= postData,args=(data,))
            postThread.start()
        except Exception as e:
            print("Error sending data to db" , e)
        return

    def killClient(self):
        
        self._client.loop_stop()
        self._client.unsubscribe("activityDetection")
        self._client.disconnect()
        return self._client