import RPi.GPIO as GPIO
import time, VehicleObjects
from VehicleObjects import *

class MovingController:
    steering = None
    msStep = None
    msDir = None
    CW = 1     # Clockwise Rotation
    CCW = 0    # Counterclockwise Rotation
    delay = 0.001 
    step_count = 48*2 # Steps per Revolution (360 / 7.5)
    
    def __init__(self):
        motor = VehicleObjects.MotorTC()
        self.msStep = motor.msStep
        self.msDir = motor.msDir
        
        servo = VehicleObjects.ServoTC()
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(motor.ms1,GPIO.OUT)
        GPIO.setup(motor.ms2,GPIO.OUT)
        GPIO.setup(motor.ms3,GPIO.OUT)
        GPIO.output(motor.ms1,GPIO.HIGH)
        GPIO.output(motor.ms2,GPIO.LOW)
        GPIO.output(motor.ms3,GPIO.LOW)

        GPIO.setup(self.msStep,GPIO.OUT)
        GPIO.setup(self.msDir,GPIO.OUT)
        GPIO.output(self.msDir,self.CW)

        GPIO.setup(servo.servoSteering,GPIO.OUT)
        self.steering  = GPIO.PWM(servo.servoSteering,50)
        
    def turnLeft():
        steering.ChangeDutyCycle(8.5)

    def turnRight():
        steering.ChangeDutyCycle(4)

    def forward():
        global CW
        GPIO.output(msDir,CW)
        steering.ChangeDutyCycle(6)
        driving()

    def backward():
        steering.ChangeDutyCycle(6)
        GPIO.output(msDir,CCW)
        driving()
       
    def driving():
        for x in range(step_count):
            GPIO.output(msStep, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(msStep, GPIO.LOW)
            time.sleep(delay)