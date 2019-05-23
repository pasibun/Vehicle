import paho.mqtt.client as mqtt
import json, multiprocessing, time, playstationController
from driving import MovingController
from sensorReading import SensorController
from multiprocessing import Process

client = mqtt.Client()

broker_address="10.0.0.113"
subscribe = "home/vehicle/tubbercar"
domoticzTopic = "domoticz/in"
sensorUltraTopic="home/vehicle/tubbercar/sensor"

msgValueDriving="Value"

class TubberCar:
    sensors = SensorController.initializeTC()
    drive = MovingController.initizlizeTC()
    def initialize:
        print("Making TubberCar ready..."
        try:
            p1 = multiprocessing.Process(target=connectAndSubscribe)
            p1.deamon = True
            p1.start()            
            
            ps3 = PlaystationControl        
            if(ps3.initializeControler):
                p2 = multiprocessing.Process(target=ps3.controlingJoystick)
                p2.deamon = True
                p2.start()
            
            print('Proces Mqtt is running.')
        except KeyboardInterrupt:
            print("Exiting program.")
            client.end()
            p1.stop()
            
    def on_message(mosq, obj, msg):
        print(msg.topic)
        print(str(msg.payload))
        
        data = json.loads(msg.payload.decode())    
        value = str(data[msgValueDriving])
        
        if(value == "Up"):
            drive.forward()
        elif(value == "Down"):
            drive.backward()
        elif(value == "Left"):
            drive.turnLeft()
        elif(value == "Right"):
            drive.turnRight()
        elif(str(data[msgValueSensor]) == 'MeasureUltra'):
            measuring = sensors.measureUltra()
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

class Hexapod:
    def initialize:
        print("Ready to walk bitches")      
      
if __name__ == "__main__":
    try:
        print("Welcome to the vehicle controller.")
        print("Before you can start, please select a vehicle.")
        while True:
            print("Press 1 for TubberCar and press 2 for Hexapod.")
            choose = input('Enter the number:') 
            if(choose.isdigit() and len(choose) == 1):
                print("TubberCar it is..")
                TubberCar.initialize()
            elif(choose.isdigit() and len(choose) == 2):                
                print("Hexapod it is..")
                Hexapod.initialize()
            else:
                print("Common.. You can do it!")
     except KeyboardInterrupt:
            print("Exiting program.")
