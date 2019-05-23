import RPi.GPIO as GPIO
import time, configparser

class MovingController:
    steering = GPIO.PWM(servoSteering,50)
    msStep = None
    msDir = None
    CW = 1     # Clockwise Rotation
    CCW = 0    # Counterclockwise Rotation
    delay = 0.001 
    step_count = 48*2 # Steps per Revolution (360 / 7.5)
    
    def initizlizeTC():
        motor = objects.MotorTC
        msStep = motor.msStep
        msDir = motor.msDir
        
        servo = objects.ServoTC
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(motor.ms1,GPIO.OUT)
        GPIO.setup(motor.ms2,GPIO.OUT)
        GPIO.setup(motor.ms3,GPIO.OUT)
        GPIO.output(motor.ms1,GPIO.HIGH)
        GPIO.output(motor.ms2,GPIO.LOW)
        GPIO.output(motor.ms3,GPIO.LOW)

        GPIO.setup(msStep,GPIO.OUT)
        GPIO.setup(msDir,GPIO.OUT)
        GPIO.output(msDir,CW)

        GPIO.setup(servo.servoSteering,GPIO.OUT)
        
    def turnLeft():
        steering.ChangeDutyCycle(8.5)

    def turnRight():
        steering.ChangeDutyCycle(4)

    def forward():
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