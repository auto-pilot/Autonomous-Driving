import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev

in3 = 22
in4 = 24
ena = 23
temp1=1

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
q=GPIO.PWM(ena,1000)
q.start(25)

GPIO.setup(17,GPIO.OUT)
p = GPIO.PWM(17,50)

p.start(7.5)

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio2 = NRF24(GPIO, spidev.SpiDev())
radio2.begin(0, 25)

radio2.setRetries(15,15)

radio2.setPayloadSize(32)
radio2.setChannel(0x60)
radio2.setDataRate(NRF24.BR_1MBPS)
radio2.setPALevel(NRF24.PA_MAX)

radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio2.openWritingPipe(pipes[0])
radio2.openReadingPipe(1, pipes[1])
#radio2.setCRCLength(2)
radio2.startListening()
radio2.stopListening()

radio2.printDetails()

radio2.startListening()

def to_angle(x):
    return 2.5 + (7 / 255) * x

while True:
    pipe = [0]
    
    while not radio2.available(pipe):
        time.sleep(10000/1000000.0)

    coordinates = [120,121]
    radio2.read(coordinates, radio2.getDynamicPayloadSize())
    
    
    if coordinates[0] >= 135:
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
    elif coordinates[0] <= 115:
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
    else :
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
            
    if coordinates[1] == 121 or coordinates[1] == 122:
        p.ChangeDutyCycle(to_angle(160))
    else:
        p.ChangeDutyCycle(to_angle(coordinates[1]))

    
