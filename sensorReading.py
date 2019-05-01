import RPi.GPIO as GPIO
import time, configparser

config = configparser.ConfigParser()
config.read('setupcar.ini')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

echo = int(config['hc-sensor']['echo'])
trigger = int(config['hc-sensor']['trigger'])

GPIO.setup(echo,GPIO.IN)
GPIO.setup(trigger,GPIO.OUT)
GPIO.output(trigger,False)

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