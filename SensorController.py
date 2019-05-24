import RPi.GPIO as GPIO
import time, VehicleObjects
from VehicleObjects import *

class SensorController:
    echo = None
    trigger = None
    def __init__(self):
        us = VehicleObjects.UltraSonicTC()
        self.echo = us.echo
        self.trigger = us.trigger
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.setup(self.trigger,GPIO.OUT)
        GPIO.output(self.trigger,False)
        
    def measureUltra():
        GPIO.output(Trigger,True)
        time.sleep(0.00001)
        GPIO.output(Trigger,False)
        
        while GPIO.input(Echo)==0:
            pulse_start = time.time()
        
        while GPIO.input(Echo)==1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return returnSensorInformation(distance, "UltraSonic")
        
        
    def returnSensorInformation(value, name):
         "{ \"SensorName\" : \""+name+ "\"\"Value\" : \""+ distance+"\""