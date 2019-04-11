import configparser
from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('setupcar.ini')

Motor1Enable = 14
Motor1A= 15
Motor1B= 18

Motor2Enable = 25
Motor2A= 7
Motor2B= 8

Trigger = 4
Echo = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1Enable,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2Enable,GPIO.OUT)
GPIO.setup(Trigger,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)

GPIO.output(Motor1A,GPIO.LOW)
GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor2A,GPIO.LOW)
GPIO.output(Motor2B,GPIO.LOW)
GPIO.output(Trigger,False)

p1=GPIO.PWM(Motor1Enable,1000)
p1.start(75)

p2=GPIO.PWM(Motor2Enable,1000)
p2.start(75)


print "DOne"

a=1
@app.route("/")
def index():
    return render_template('robot.html')

@app.route('/left_side')
def left_side():
    data1="LEFT"
    GPIO.output(Motor1A, 0)
    GPIO.output(Motor1B, 0)
    GPIO.output(Motor2A, 1)
    GPIO.output(Motor2B, 0)
    return 'true'

@app.route('/right_side')
def right_side():
   data1="RIGHT"
   GPIO.output(Motor1A, 1)
   GPIO.output(Motor1B, 0)
   GPIO.output(Motor2A, 0)
   GPIO.output(Motor2B, 0)
   return 'true'

@app.route('/up_side')
def up_side():
   data1="FORWARD"
   GPIO.output(Motor1A, 1)
   GPIO.output(Motor1B, 0)
   GPIO.output(Motor2A, 1)
   GPIO.output(Motor2B, 0)
   return 'true'

@app.route('/down_side')
def down_side():
   data1="BACK"
   GPIO.output(Motor1A, 0)
   GPIO.output(Motor1B, 1)
   GPIO.output(Motor2A, 0)
   GPIO.output(Motor2B, 1)
   return 'true'

@app.route('/stop')
def stop():
   data1="STOP"
   GPIO.output(Motor1A, 0)
   GPIO.output(Motor1B, 0)
   GPIO.output(Motor2A, 0)
   GPIO.output(Motor2B, 0)
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
