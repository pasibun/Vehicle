import multiprocessing, time, PlaystationController
from multiprocessing import Process

domoticzTopic = "domoticz/in"
msgValueDriving="Value"

class TubberCar:
    subscribeTB = "home/vehicle/tubbercar"
    domoticzTopic = "domoticz/in"
    sensorUltraTopic="home/vehicle/tubbercar/sensor"
    
    def initialize:
        print("Making TubberCar ready, please wait..")
        try:
            p1 = multiprocessing.Process(target=connectAndSubscribe args=(subscribeTB,'TubberCar',))
            p1.deamon = True
            p1.start()            
            print('Proces Mqtt is running.')
            
            ps3 = PlaystationControl        
            if(ps3.initializeControler):
                p2 = multiprocessing.Process(target=ps3.controlingJoystick)
                p2.deamon = True
                p2.start()            
           
        except KeyboardInterrupt:
            print("Exiting program.")
            client.end()
            p1.stop()      
            
class Hexapod:
    def initialize:
        print("Making Hexapod ready, please wait..")
        ps3 = PlaystationControl        
            if(ps3.initializeControler):
                p2 = multiprocessing.Process(target=ps3.controlingJoystick)
                p2.deamon = True
                p2.start()
      
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
