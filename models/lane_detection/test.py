import cv2
import numpy as np
import os
import keras
from keras.models import load_model

if __name__ == '__main__':
    model = load_model('8-13-59-3.h5')

    img = cv2.imread('dataset/1/image424.jpg')
    img = cv2.Canny(img, 20, 50)
    img = cv2.resize(img, (128,128))
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    print(img.shape)
    print(np.argmax(model.predict(img.reshape(1,128,128,3))))
