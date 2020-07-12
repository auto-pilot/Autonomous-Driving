import numpy as np
import cv2
import keras
from keras.models import load_model
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time
import spidev
import pigpio

# pinout
in3 = 22
in4 = 24
ena = 23

# gpio configuration
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
q=GPIO.PWM(ena,1000)
q.start(25)

pi = pigpio.pi()
pi.set_mode(17, pigpio.OUTPUT)


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


if __name__ == '__main__':
    model = load_model('26-20-39-50.h5')
    
    # resizing video
    cap = cv2.VideoCapture(0);
    cap.set(3, 480)
    cap.set(4, 480)
    
    while True:
        start_time = time.time()
        
        ret, frame = cap.read()
	
	# taking edges from frame
        frame = cv2.flip(frame, -1)
        frame = cv2.Canny(frame, 20, 50)
        frame = cv2.resize(frame, (128,128))
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
	# model prediction
        estimate = np.argmax(model.predict(frame.reshape(1, 128, 128, 3)))
        
	
        print(estimate)
        if estimate == 0:
            pi.set_servo_pulsewidth(17, 1500)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            q.ChangeDutyCycle(45)
            time.sleep(0.1)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
        elif estimate == 1:
            pi.set_servo_pulsewidth(17, 1045)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            q.ChangeDutyCycle(65)
            time.sleep(0.125)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
        elif estimate == 2:
            pi.set_servo_pulsewidth(17, 900)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            q.ChangeDutyCycle(80)
            time.sleep(0.125)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
        
        print("FPS: ", 1.0 / (time.time() - start_time))
