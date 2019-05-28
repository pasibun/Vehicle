# Tubbercar
* clone this project
* 

# Hexapod instalation
* sudo pip3 install --upgrade setuptools
* sudo raspi-config
* Enable I2C
* Enable SPI
* pip3 install RPI.GPIO
* pip3 install adafruit-blinka
* sudo pip3 install adafruit-circuitpython-pca9685
* sudo pip3 install adafruit-circuitpython-servokit

## wiring adafruit servo controller to raspberry:
* Pi 3V3 to sensor VCC
* Pi GND to sensor GND
* Pi SCL to sensor SCL
* Pi SDA to sensor SDA