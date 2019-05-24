import paho.mqtt.client as mqtt, time, json
from MovingS import MovingService
from SensorController import SensorController


class MqttService:
    client = mqtt.Client()

    broker_address = "10.0.0.113"

    sensors = SensorController()
    drive = MovingService()

    def __init__(self):
        print("Mqqt..")

    def connectAndSubscribe(self, subscribeTopic, vehicle):
        print("Making MQTT ready.")
        self.client.connect(self.broker_address)
        self.client.subscribe(subscribeTopic)

        if (vehicle == "TubberCar"):
            self.client.on_message = self.on_messageTC
        elif (vehicle == "Hexapod"):
            self.client.on_message = self.on_messageHP
        time.sleep(2)
        print("MQTT is ready.")
        self.client.loop_forever()

    def sendMqttMsg(self, topic, payload):
        self.client.connect(self.broker_address)
        self.client.publish(topic, json.dumps(payload))

    def on_messageTC(self, mosq, obj, msg):
        print(msg.topic)
        print(str(msg.payload))

        data = json.loads(msg.payload.decode())
        value = str(data[self.msgValueDriving])

        if (value == "Up"):
            self.drive.forward()
        elif (value == "Down"):
            self.drive.backward()
        elif (value == "Left"):
            self.drive.turnLeft()
        elif (value == "Right"):
            self.drive.turnRight()
        elif (str(data[self.msgValueSensor]) == 'MeasureUltra'):
            measuring = self.sensors.measureUltra()
            self.sendMqttMsg(self.domoticzTopic, measuring)
            self.sendMqttMsg(self.sensorUltraTopic, measuring)

    def on_messageHP(self, mosq, obj, msg):
        print(msg.topic)
        print(str(msg.payload))

        data = json.loads(msg.payload.decode())
        value = str(data[self.msgValueDriving])
