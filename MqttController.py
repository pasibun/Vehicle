import paho.mqtt.client as mqtt

client = mqtt.Client()

broker_address="10.0.0.113"

sensors = SensorController.initializeTC()
drive = MovingController.initizlizeTC()
    
def connectAndSubscribe(subscribeTopic, vehicle):
    print("Making MQTT ready.")
    client.connect(broker_address)
    client.subscribe(subscribeTopic)
    if(vehicle == "TubberCar"):
        client.on_message = on_messageTC
    elif(vehicle == "Hexapod"):
        client.on_message = on_messageHP
    time.sleep(2)
    print("MQTT is ready.")
    client.loop_forever()
    
def sendMqttMsg(topic, payload):
    client.connect(broker_address)
    client.publish(topic, json.dumps(payload))
    
def on_messageTC(mosq, obj, msg):
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
        
def on_messageHP(mosq, obj, msg):
    print(msg.topic)
    print(str(msg.payload))
    
    data = json.loads(msg.payload.decode())    
    value = str(data[msgValueDriving])