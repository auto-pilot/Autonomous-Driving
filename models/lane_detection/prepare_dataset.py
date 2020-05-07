import os
import cv2
import pandas as pd
import numpy as np
import uuid

# roots definition
ROOT_DIR = os.getcwd()
DATASET_DIR = os.path.join(ROOT_DIR, "DATASET")
DATASET_DIR = os.path.join(DATASET_DIR, "18")
LABELS_DIR = os.path.join(DATASET_DIR, "imagelabels.csv")
NEW_DATA_DIR = os.path.join(ROOT_DIR, "DATASET_CANNY")

# rotations
STRAIGHT = 1230
NORMAL = 1169
HARD = 960

def angle_labeling(x_coordinate):
    label = ''
    if x_coordinate >= STRAIGHT:
        label = "STRAIGHT"
    elif HARD <= x_coordinate <= STRAIGHT-1:
        label = "NORMAL"
    elif x_coordinate <= HARD:
        label = "HARD"

    return label

def prepare():
    # read the defined CSV file
    labels = pd.read_csv(LABELS_DIR)
    labelFile = open(str(NEW_DATA_DIR + '/labels.txt'), 'a')

    for index, item in labels.iterrows():

        img = cv2.imread(os.path.join(DATASET_DIR, item['name']))
        # we are convert image canny format because
        # int this way lines looks more obvious
        img = cv2.Canny(img, 50, 20)
        #image = np.zeros((200,200))

        cv2.putText(img,"angle:" + str(item['x']), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img,"speed:" + str(item['y']), (10, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('img', img)
        #cv2.imshow('image', image)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            newName = str(uuid.uuid4())

            cv2.imwrite(NEW_DATA_DIR + '/' + newName + '.jpg', img)

            labelFile.write(newName + '.jpg,' + str(angle_labeling(float(item['x']))) + '\n')

    labelFile.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    prepare()
