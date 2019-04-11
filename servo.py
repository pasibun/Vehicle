import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)
# Zet de GPIO pin als uitgang.
GPIO.setup(12, GPIO.OUT)
# Configureer de pin voor PWM met een frequentie van 50Hz.
p = GPIO.PWM(12, 50)
# Start PWM op de GPIO pin met een duty-cycle van 6%
p.start(6)
 
try:
   while True:
    # 0 graden (neutraal)
    p.ChangeDutyCycle(6)
    sleep(1)
 
    # -90 graden (rechts)
   # p.ChangeDutyCycle(4)
    sleep(1)
 
    # 0 graden (neutraal)
    #p.ChangeDutyCycle(6)
    sleep(1)
 
    # 90 graden (links)
   # p.ChangeDutyCycle(8.5)
    sleep(1)

    # 0 graden (neutraal)
    #p.ChangeDutyCycle(6)
    sleep(1)
 
except KeyboardInterrupt:  
  # Stop PWM op GPIO.
  p.stop()
  # GPIO netjes afsluiten
  GPIO.cleanup()
