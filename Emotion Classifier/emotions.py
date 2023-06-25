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

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Command line argument
ap = argparse.ArgumentParser()
ap.add_argument("--mode", help="train/display")
mode = ap.parse_args().mode
mode = "directory"  # Default mode

num_train = 28709
num_val = 7178
batch_size = 64
num_epoch = 50

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

if mode == "train":
    print("Not Available")
elif mode == "video":
    model.load_weights('model.h5')
    cv2.ocl.setUseOpenCL(False)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    cap = cv2.VideoCapture("e.mp4")
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_recognition.face_locations(frame, model="hog")
        for (y1, x1, y2, x2) in faces:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            roi_gray = gray[y1:y2, x2:x1]
            cropped_img = np.expand_dims(np.expand_dims(
                cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x2, y2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Video', cv2.resize(frame, (1280, 720)))
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f") + ".jpg"
        cv2.imwrite(timestamp, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
elif mode == "video_whole":
    model.load_weights('model.h5')
    emotions_array = [0, 0, 0, 0, 0, 0, 0]
    cv2.ocl.setUseOpenCL(False)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    cap = cv2.VideoCapture("c.mp4")
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_recognition.face_locations(frame, model="hog")
        for (y1, x1, y2, x2) in faces:
            roi_gray = gray[y1:y2, x2:x1]
            cropped_img = np.expand_dims(np.expand_dims(
                cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            emotions_array[maxindex] = emotions_array[maxindex] + 1
        print(emotions_array)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(emotions_array)
    cap.release()
    cv2.destroyAllWindows()
elif mode == "directory":
    model.load_weights('model.h5')
    cv2.ocl.setUseOpenCL(False)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    inputPath = r"to_sort"
    filesArray = []
    for path, subdirs, files in os.walk(inputPath):
        for name in files:
            filesArray.append(os.path.join(path + "\\", name))
    print(filesArray)
    print(len(filesArray))
    for file in filesArray:
        emotions_array = [0, 0, 0, 0, 0, 0, 0]
        print(file)
        frame = cv2.imread(file)
        try:
            real_frame = frame.copy()
        except:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_recognition.face_locations(frame, model="hog")
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
            cv2.imwrite("sorted\\"+"None_"+file.split("\\")[-1], frame)
        else:
            cv2.imwrite(
                "sorted\\"+emotion_dict[np.argmax(emotions_array)]+"_"+file.split("\\")[-1], frame)
    cv2.destroyAllWindows()
