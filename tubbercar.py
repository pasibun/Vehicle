import configparser
from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('setupcar.ini')

m1e = int(config['motor-a']['motorAEnable'])
m1a = int(config['motor-a']['motorA1'])
m1b = int(config['motor-a']['motorA2'])

m2e = int(config['motor-b']['motorBEnable'])
m2a = int(config['motor-b']['motorB1'])
m2b = int(config['motor-b']['motorB2'])

Trigger = int(config['hc-sensor']['trigger'])
Echo = int(config['hc-sensor']['echo'])

ServoA = int(config['servos']['servoA'])
ServoB = int(config['servos']['servoB'])

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(m1a,GPIO.OUT)
GPIO.setup(m1b,GPIO.OUT)
GPIO.setup(m1e,GPIO.OUT)
GPIO.setup(m2a,GPIO.OUT)
GPIO.setup(m2b,GPIO.OUT)
GPIO.setup(m2e,GPIO.OUT)
GPIO.setup(Trigger,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)
GPIO.setup(ServoA,GPIO.OUT)
GPIO.setup(ServoB,GPIO.OUT)

GPIO.output(m1a,GPIO.LOW)
GPIO.output(m1b,GPIO.LOW)
GPIO.output(m2a,GPIO.LOW)
GPIO.output(m2b,GPIO.LOW)
GPIO.output(Trigger,False)

p1=GPIO.PWM(m1e,1000)
p1.start(75)

p2=GPIO.PWM(m2e,1000)
p2.start(75)

pwmA = GPIO.PWM(ServoA,50)
#pwmA.start(5)
pwmB = GPIO.PWM(ServoB,50)
#pwmB.start(5)

print "DOne"

@app.route("/")
def index():
    return render_template('robot.html')

@app.route('/left_side')
def left_side():
    data1="LEFT"
    GPIO.output(m1a, 0)
    GPIO.output(m1b, 0)
    GPIO.output(m2a, 1)
    GPIO.output(m2b, 0)
    return 'true'

@app.route('/right_side')
def right_side():
   data1="RIGHT"
   GPIO.output(m1a, 1)
   GPIO.output(m1b, 0)
   GPIO.output(m2a, 0)
   GPIO.output(m2b, 0)
   return 'true'

@app.route('/up_side')
def up_side():
   data1="FORWARD"
   GPIO.output(m1a, 0)
   GPIO.output(m1b, 1)
   GPIO.output(m2a, 0)
   GPIO.output(m2b, 1)
   return 'true'

@app.route('/down_side')
def down_side():
   data1="BACK"
   GPIO.output(m1a, 1)
   GPIO.output(m1b, 0)
   GPIO.output(m2a, 1)
   GPIO.output(m2b, 0)
   return 'true'

@app.route('/stop')
def stop():
   data1="STOP"
   GPIO.output(m1a, 0)
   GPIO.output(m1b, 0)
   GPIO.output(m2a, 0)
   GPIO.output(m2b, 0)
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

if __name__ == "__main__":
   print "Start"
   app.run(host='10.0.0.82',port=5010,debug=True)
