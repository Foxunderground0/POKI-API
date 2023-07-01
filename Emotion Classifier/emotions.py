import numpy as np
import argparse
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import face_recognition
from datetime import datetime
import subprocess

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Create the model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
          activation='relu', input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

model.load_weights('Emotion Classifier\\model.h5')

cv2.ocl.setUseOpenCL(False)
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
inputPath = r"Immages\\to_sort\\"
filesArray = []

for path, subdirs, files in os.walk(inputPath):
    for name in files:
        filesArray.append(os.path.join(path, name))

for file in filesArray:
    f = open(file, "rb")
    immage = cv2.imread(file)
    f.close()
    if immage is None:
        os.remove(file)

filesArray = []

for path, subdirs, files in os.walk(inputPath):
    for name in files:
        filesArray.append(os.path.join(path, name))


print(filesArray)
print(len(filesArray))
# a = os.system("face_detection.exe --cpus 12 --model hog " + inputPath)
'''
command = ['face_detection.exe', '--cpus',
           '12', '--model', 'cnn', inputPath]

try:
    output = subprocess.check_output(command, universal_newlines=True)
    print(output)
except subprocess.CalledProcessError as e:
    print(f"Command execution failed with error code {e.returncode}")
    print(e.output)
'''

for file in filesArray:
    emotions_array = [0, 0, 0, 0, 0, 0, 0]
    print(file)
    frame = cv2.imread(file)
    try:
        real_frame = frame.copy()
    except:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_recognition.face_locations(frame, 1, model="cnn")
    print(faces)
    for (y1, x1, y2, x2) in faces:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        roi_gray = gray[y1:y2, x2:x1]
        cropped_img = np.expand_dims(np.expand_dims(
            cv2.resize(roi_gray, (48, 48)), -1), 0)
        prediction = model.predict(cropped_img)
        maxindex = int(np.argmax(prediction))
        emotions_array[maxindex] = emotions_array[maxindex] + 1
        cv2.putText(frame, emotion_dict[maxindex], (x2, y2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    if (faces == []):
        cv2.imwrite("Immages\\sorted\\"+"None_" +
                    file.split("\\")[-1], frame)
    else:
        cv2.imwrite(
            "Immages\\sorted\\"+emotion_dict[np.argmax(emotions_array)]+"_"+file.split("\\")[-1], frame)

cv2.destroyAllWindows()
