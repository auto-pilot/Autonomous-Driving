import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import pigpio
import cv2
import os

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

pi = pigpio.pi()
pi.set_mode(17, pigpio.OUTPUT)


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
    return 600 + (1400 / 255) * x #0-> 600 255->2000

def to_speed(x):
    speed = 0 + (100 / 127) * (x - 128)
    speed = abs(speed)
    if speed < 0:
        return 0
    elif speed > 100:
        return 100
    else:
        return speed
    

c=1
cap = cv2.VideoCapture(0);
cap.set(3, 480)
cap.set(4, 480)
img_counter = 0

file = open('dataset/imagelabels.txt','w')
file.write("name," + "x,"+"y" + "\n")
file.close()

while True:
    
    pipe = [0]
    ret, frame = cap.read()
    
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
    q.ChangeDutyCycle(to_speed(coordinates[0]))
    
    if coordinates[1] >= 121 and coordinates[1] < 170:
        pi.set_servo_pulsewidth(17, 1500)
    else:
        pi.set_servo_pulsewidth(17, to_angle(coordinates[1]))
    
    frame = cv2.flip(frame, -1)
    img_counter = img_counter + 1
    
    file = open('dataset/imagelabels.txt','a')
    file.write("image" + str(img_counter) + ".jpg,"+ str(round(to_angle(coordinates[1]),0)) + "," + str(round(to_speed(coordinates[0]),0)) +"\n")
    file.close() 
    
    cv2.imwrite('dataset/image' +str(img_counter) + '.jpg', frame)
    
    #cv2.imshow("frame",frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

pi.stop()
