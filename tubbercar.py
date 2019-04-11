import configparser
from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
delay = .0208
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
GPIO.output(ms2,GPIO.HIGH)
GPIO.output(ms3,GPIO.HIGH)

#GPIO.setup(msEnable,GPIO.OUT)
GPIO.setup(msStep,GPIO.OUT)
GPIO.setup(msDir,GPIO.OUT)
GPIO.output(msDir,CW)

#GPIO.setup(Echo,GPIO.IN)
#GPIO.setup(Trigger,GPIO.OUT)
#GPIO.output(Trigger,False)

GPIO.setup(servoSteering,GPIO.OUT)

steering = GPIO.PWM(servoSteering,50)
steering.start(6)

print "DOne"

@app.route("/")
def index():
    return render_template('robot.html')

@app.route('/left_side')
def left_side():
    data1="LEFT"
    steering.ChangeDutyCycle(8.5)
    return 'true'

@app.route('/right_side')
def right_side():
   data1="RIGHT"
   steering.ChangeDutyCycle(4)
   return 'true'

@app.route('/up_side')
def up_side():
   data1="FORWARD"
   steering.ChangeDutyCycle(6)
   driving()
   return 'true'

@app.route('/down_side')
def down_side():
   data1="BACK"
   steering.ChangeDutyCycle(4)
   GPIO.output(msDir,CCW)
   driving()
   return 'true'

@app.route('/stop')
def stop():
   data1="STOP"
   
   return  'true'

@app.route('/measure')
def measure():
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
    print "Distance: ", distance, "cm"
    return 'true'

   
def driving():
    for x in range(step_count):
        GPIO.output(msStep, GPIO.HIGH)
        sleep(delay)
        GPIO.output(msStep, GPIO.LOW)
        sleep(delay)
        
if __name__ == "__main__":
   print "Start"
   app.run(host='10.0.0.111',port=5010,debug=True)
