import RPi.GPIO as GPIO
import time, VehicleO


class MovingService:
    steering = None
    msStep = None
    msDir = None
    CW = 1  # Clockwise Rotation
    CCW = 0  # Counterclockwise Rotation
    delay = 0.001
    step_count = 48 * 2  # Steps per Revolution (360 / 7.5)

    def __init__(self):
        motor = VehicleO.MotorTC()
        self.msStep = motor.msStep
        self.msDir = motor.msDir

        servo = VehicleO.ServoTC()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(motor.ms1, GPIO.OUT)
        GPIO.setup(motor.ms2, GPIO.OUT)
        GPIO.setup(motor.ms3, GPIO.OUT)
        GPIO.output(motor.ms1, GPIO.HIGH)
        GPIO.output(motor.ms2, GPIO.LOW)
        GPIO.output(motor.ms3, GPIO.LOW)

        GPIO.setup(self.msStep, GPIO.OUT)
        GPIO.setup(self.msDir, GPIO.OUT)
        GPIO.output(self.msDir, self.CW)

        GPIO.setup(servo.servoSteering, GPIO.OUT)
        self.steering = GPIO.PWM(servo.servoSteering, 50)

    def turn_left(self):
        self.steering.ChangeDutyCycle(8.5)

    def turn_right(self):
        self.steering.ChangeDutyCycle(4)

    def forward(self):
        GPIO.output(self.msDir, self.CW)
        self.steering.ChangeDutyCycle(6)
        self.driving()

    def backward(self):
        self.steering.ChangeDutyCycle(6)
        GPIO.output(self.msDir, self.CCW)
        self.driving()

    def driving(self):
        for x in range(self.step_count):
            GPIO.output(self.msStep, GPIO.HIGH)
            time.sleep(self.delay)
            GPIO.output(self.msStep, GPIO.LOW)
            time.sleep(self.delay)
