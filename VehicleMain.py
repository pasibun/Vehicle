from multiprocessing import Process
from MqttS import *
from PlaystationS import *

domoticzTopic = "domoticz/in"
msgValueDriving = "Value"


class TubberCar:
    subscribeTB = "home/vehicle/tubbercar"
    domoticzTopic = "domoticz/in"
    sensorUltraTopic = "home/vehicle/tubbercar/sensor"

    def __init__(self):
        print("Making TubberCar ready, please wait..")
        try:
            mqtt = MqttService()
            p1 = Process(target=mqtt.connectAndSubscribe, args=(self.subscribeTB, 'TubberCar',))
            p1.deamon = True
            p1.start()
            print('Proces Mqtt is running.')

            ps3 = PlaystationService()
            if (ps3.ps3Connected):
                p2 = Process(target=ps3.controlingJoystick)
                p2.deamon = True
                p2.start()

        except KeyboardInterrupt:
            print("Exiting program.")
            p1.stop()


class Hexapod:
    def initialize(self):
        print("Making Hexapod ready, please wait..")
        ps3 = PlaystationService()
        if (ps3.ps3Connected):
            p2 = Process(target=ps3.controlingJoystick)
            p2.deamon = True
            p2.start()


if __name__ == "__main__":
    try:
        print("Welcome to the vehicle controller.")
        print("Before you can start, please select a vehicle.")
        while True:
            print("Press 1 for TubberCar and press 2 for Hexapod.")
            choose = input('Enter the number:')
            if (choose.isdigit() and len(choose) == 1):
                print("TubberCar it is..")
                tc = TubberCar()
            elif (choose.isdigit() and len(choose) == 2):
                print("Hexapod it is..")
                hp = Hexapod()
            else:
                print("Common.. You can do it!")
    except KeyboardInterrupt:
        print("Exiting program.")
