import RPi.GPIO as GPIO
import time, configparser

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
delay = 0.001
SPR = 48   # Steps per Revolution (360 / 7.5)
step_count = SPR

config = configparser.ConfigParser()
config.read('setupcar.ini')

ms1 = int(config['micro-stepping']['ms1'])
ms2 = int(config['micro-stepping']['ms2'])
ms3 = int(config['micro-stepping']['ms3'])
#msEnable = int(config['motor']['motorEnable'])
msStep = int(config['motor']['motorStep'])
msDir = int(config['motor']['motorDir'])

servoSteering = int(config['servos']['servoSteering'])

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ms1,GPIO.OUT)
GPIO.setup(ms2,GPIO.OUT)
GPIO.setup(ms3,GPIO.OUT)
GPIO.output(ms1,GPIO.HIGH)
GPIO.output(ms2,GPIO.LOW)
GPIO.output(ms3,GPIO.LOW)

#GPIO.setup(msEnable,GPIO.OUT)
GPIO.setup(msStep,GPIO.OUT)
GPIO.setup(msDir,GPIO.OUT)
GPIO.output(msDir,CW)

GPIO.setup(servoSteering,GPIO.OUT)

steering = GPIO.PWM(servoSteering,50)

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