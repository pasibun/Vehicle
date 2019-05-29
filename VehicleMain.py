from multiprocessing import Process
from .Service.MqttS import *
from .Service.PlaystationS import *

domoticzTopic = "domoticz/in"
msgValueDriving = "Value"


class TubberCar:
    subscribeTB = "home/vehicle/tubbercar"

    def __init__(self):
        print("Making TubberCar ready, please wait..")
        try:
            mqtt = MqttService()
            p1 = Process(target=mqtt.connectandsubscribe, args=(self.subscribeTB, 'TubberCar',))
            p1.deamon = True
            p1.start()
            time.sleep(5)

            ps3 = PlaystationService()
            if (ps3.ps3Connected):
                p2 = Process(target=ps3.joystickcontrole)
                p2.deamon = True
                p2.start()
            time.sleep(2)
        except KeyboardInterrupt:
            print("Exiting program.")
            p1.stop()


class Hexapod:
    def initialize(self):
        print("Making Hexapod ready, please wait..")
        ps3 = PlaystationService()
        if (ps3.ps3Connected):
            p2 = Process(target=ps3.joystickcontrole)
            p2.deamon = True
            p2.start()

        time.sleep(2)
        print("Hexapod is ready to go.")


if __name__ == "__main__":
    try:
        print("Welcome to the vehicle controller.")
        print("Before you can start, please select a vehicle.")
        firstRun = True
        while firstRun:
            print("Press 1 for TubberCar and press 2 for Hexapod.")
            choose = input('Enter the number:')
            print("")
            if (choose.isdigit() and len(choose) == 1):
                print("TubberCar it is..")
                firstRun = False
                tc = TubberCar()
            elif (choose.isdigit() and len(choose) == 2):
                print("Hexapod it is..")
                firstRun = False
                hp = Hexapod()
            else:
                print("Common.. You can do it!")
    except KeyboardInterrupt:
        print("Exiting program.")
