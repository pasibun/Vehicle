import RPi.GPIO as GPIO
import time
from Objects import VehicleO


class SensorController:
    echo = None
    trigger = None

    def __init__(self):
        us = VehicleO.UltraSonicTC()
        self.echo = us.echo
        self.trigger = us.trigger

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.output(self.trigger, False)

    def measureultra(self):
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()

        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return "{ \"SensorName\" : \"UltraSonig""\"\"Value\" : \"" + str(distance) + "\""
