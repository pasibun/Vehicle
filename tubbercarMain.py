import paho.mqtt.client as mqtt
import json, multiprocessing, time, configparser, driving, sensorReading
from multiprocessing import Process

client = mqtt.Client()

broker_address="10.0.0.113"
subscribe = "home/vehicle/tubbercar"
domoticzTopic = "domoticz/in"
sensorUltraTopic="home/vehicle/tubbercar/sensor"

msgValueDriving="Value"

def on_message(mosq, obj, msg):
    print(msg.topic)
    print(str(msg.payload))
    
    data = json.loads(msg.payload.decode())    
    value = str(data[msgValueDriving])
    
    if(value == "Up"):
        driving.forward()
    elif(value == "Down"):
        driving.backward()
    elif(value == "Left"):
        driving.turnLeft()
    elif(value == "Right"):
        driving.turnRight()
    elif(str(data[msgValueSensor]) == 'MeasureUltra'):
        measuring = sensorReading.measureUltra()
        sendMqttMsg(domoticzTopic, measuring)
        sendMqttMsg(sensorUltraTopic, measuring)

def connectAndSubscribe():
    client.connect(broker_address)
    client.subscribe(subscribe)
    client.on_message = on_message
    client.loop_forever()
    
def sendMqttMsg(topic, payload):
    client.connect(broker_address)
    client.publish(topic, json.dumps(payload))
  
if __name__ == "__main__":
    try:
        p1 = multiprocessing.Process(target=connectAndSubscribe)
        p1.deamon = True
        p1.start()
        print('Proces Mqtt is running.')
    except KeyboardInterrupt:
        print("Exiting program.")
        client.end()
        p1.stop()
