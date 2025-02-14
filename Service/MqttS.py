import paho.mqtt.client as mqtt, time, json
from Tubbercar.MovingS import MovingService
from ..Controller.SensorController import SensorController


class MqttService:
    client = mqtt.Client()

    broker_address = "10.0.0.113"

    sensors = SensorController()
    drive = MovingService()

    domoticzTopic = "domoticz/in"
    sensorUltraTopic = "home/vehicle/tubbercar/sensor"

    def __init__(self):
        print("MQTT initializing")

    def connectandsubscribe(self, subscribeTopic, vehicle):
        try:
            self.client.connect(self.broker_address)
            self.client.subscribe(subscribeTopic)

            if (vehicle == "TubberCar"):
                self.client.on_message = self.on_message_tc
            elif (vehicle == "Hexapod"):
                self.client.on_message = self.on_message_hp
            time.sleep(2)
            print("MQTT is ready.")
            self.client.loop_forever()
        except:
            print("ERROR! Cannot connect to the Mqtt broker! ")

    def sendmqttmsg(self, topic, payload):
        self.client.connect(self.broker_address)
        self.client.publish(topic, json.dumps(payload))

    def on_message_tc(self, mosq, obj, msg):
        try:
            print(msg.topic)
            print(str(msg.payload))

            data = json.loads(msg.payload.decode())
            value = str(data["Value"])

            if (value == "Up"):
                self.drive.forward()
            elif (value == "Down"):
                self.drive.backward()
            elif (value == "Left"):
                self.drive.turn_left()
            elif (value == "Right"):
                self.drive.turn_right()
            elif (str(data["Value"]) == 'MeasureUltra'):
                measuring = self.sensors.measureultra()
                self.sendmqttmsg(self.domoticzTopic, measuring)
                self.sendmqttmsg(self.sensorUltraTopic, measuring)
        except:
            print("ERROR! Cannot handle mqtt msg...")

    def on_message_hp(self, mosq, obj, msg):
        print(msg.topic)
        print(str(msg.payload))

        data = json.loads(msg.payload.decode())
        value = str(data["Value"])
