#!/usr/bin/env python 

import paho.mqtt.client as mqtt 
import pylog 
import time
import random
import json

pylog.setLogger('virtual-device.log', pylog.DEBUG, 102400, 2)
log = pylog.Log("virtual-device")

class EdgexMqttDevice:
    def __init__(self, server="localhost", port=1883, name="my-custom-device"):
        self._server = server 
        self._port = port 
        self._client_id = name 
        self._device_name = name
        self._client = mqtt.Client(self._client_id)
        self._commandTopic = "command/" + self._device_name + "/#"
        self._reportTopicPrefix = "incoming/data/" + self._device_name + "/"
        self._responseTopicPrefix = "command/response/"
        self._subscribe_topis = [self._commandTopic]
    
    def is_connected(self):
        return self._client.is_connected()
    
    def _on_connect(self, client, userdata, flags, rc):
        log.i("Connected to %s:%d success" % (self._server, self._port))

        for t in self._subscribe_topis:
            self._client.subscribe(t)
            log.i("Subscribe topic:%s" % t)


    def _on_disconnect(self, userdata, rc):
        log.w("Disconnected with result code " + str(rc))

    def _on_message(self, client, userdata, msg):
        log.d("Receive message: (" + msg.topic + ") " + str(msg.payload))
        # command/my-custom-device/ping/get/ab196da3-429d-427f-89fd-5cae53a5e061
        items = msg.topic.split('/')
        if len(items) != 5:
            log.w("Receive invalid topic: %s" % msg.topic)
            return 
        resource = items[2]
        command = items[3]
        uuid = items[4]
        if command == 'get':
            self._handle_read_resource(uuid, resource)
        elif command == 'set':
            data = json.loads(msg.payload)                        
            for (k, v) in data.items():
                self._handle_write_resource(uuid, k, v)
        else :
            log.w("Unsupport command:%s" % command)


    def _handle_read_resource(self, uuid:str, resource:str):
        v = random.randint(25, 30)        
        ack = {}
        ack[resource] = v 
        msg = json.dumps(ack)
        log.i("resource read:  %s = %s" % (resource, msg))
        self.publish(self._responseTopicPrefix + uuid, msg)

    def _handle_write_resource(self, uuid:str, resource:str, value):
        log.i("resource write: %s = %s" % (resource, str(value)))
        self.publish(self._responseTopicPrefix + uuid, "")

    def stop(self):
        self._client.loop_stop()

    def start(self):
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

        # TODO: try to use password or ssl options
        log.i("Connecting to server(%s:%d)" % (self._server, self._port))
        try:
            self._client.connect(self._server, self._port, 30)
        except Exception as e:
            log.w("Connected failed:", e)
            return 
        self._client.loop_start() 

    def publish(self, topic:str, msg:str)->bool:
        if not self.is_connected():
            return False
        msgInfo = self._client.publish(topic, msg)
        # if not msgInfo.is_published():
        #     log.d("publish waiting...")
        #     msgInfo.wait_for_publish(timeout=0.2)
        log.w("Publish topic:%s, msg:%s, result:%s" % (topic, msg, str(msgInfo.rc)))
        return True 

    def report(self, resource:str, value):
        self.publish(self._reportTopicPrefix + resource, str(value))


dev = EdgexMqttDevice()
dev.start()

# time.sleep(5)
# for i in range(1000):
#     dev.report("randnum", (random.randint(25, 29) * 0.75))
#     time.sleep(0.01)
#     i += 1

# time.sleep(1)

while True:
    time.sleep(10)
    dev.report("randnum", (random.randint(25, 29) * 0.75))

dev.stop()


#while True:
#    time.sleep(10)


