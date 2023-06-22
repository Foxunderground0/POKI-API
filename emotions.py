import numpy as np
import time
import argparse
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import face_recognition
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# command line argument
ap = argparse.ArgumentParser()
ap.add_argument("--mode", help="train/display")
mode = ap.parse_args().mode

# plots accuracy and loss curves


def plot_model_history(model_history):
    """
    Plot Accuracy and Loss curves given the model_history
    """
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    # summarize history for accuracy
    axs[0].plot(range(1, len(model_history.history['accuracy'])+1),
                model_history.history['accuracy'])
    axs[0].plot(range(1, len(model_history.history['val_accuracy'])+1),
                model_history.history['val_accuracy'])
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1, len(model_history.history['accuracy'])+1),
                      len(model_history.history['accuracy'])/10)
    axs[0].legend(['train', 'val'], loc='best')
    # summarize history for loss
    axs[1].plot(range(1, len(model_history.history['loss'])+1),
                model_history.history['loss'])
    axs[1].plot(range(1, len(model_history.history['val_loss'])+1),
                model_history.history['val_loss'])
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(
        1, len(model_history.history['loss'])+1), len(model_history.history['loss'])/10)
    axs[1].legend(['train', 'val'], loc='best')
    fig.savefig('plot.png')
    plt.show()


num_train = 28709
num_val = 7178
batch_size = 64
num_epoch = 50

train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)


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

# If you want to train the same model or try other models, go for this
if mode == "train":
    model.compile(loss='categorical_crossentropy', optimizer=Adam(
        lr=0.0001, decay=1e-6), metrics=['accuracy'])
    model_info = model.fit_generator(
        train_generator,
        steps_per_epoch=num_train // batch_size,
        epochs=num_epoch,
        validation_data=validation_generator,
        validation_steps=num_val // batch_size)
    plot_model_history(model_info)
    model.save_weights('model.h5')

# emotions will be displayed on your face from the webcam feed
elif mode == "display":
    model.load_weights('model.h5')

    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    # start the webcam feed
    cap = cv2.VideoCapture("a.mp4")
    while True:
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        frame = cv2.imread("e.jpg")
        # frame = cv2.resize(frame, (640, 360))
        if not ret:
            break
        # facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # faces = facecasc.detectMultiScale(
        #    gray, scaleFactor=1.3, minNeighbors=12)
        faces = face_recognition.face_locations(frame, model="cnn")

        for (y1, x1, y2, x2) in faces:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            roi_gray = gray[y1:y2, x2:x1]
            print(f'{x1} {x2} {y1} {y2} {roi_gray}')
            cv2.imshow('roi', roi_gray)
            cropped_img = np.expand_dims(np.expand_dims(
                cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x2, y2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# emotions will be displayed on your face from the webcam feed
elif mode == "directory":
    model.load_weights('model.h5')

    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    # start the webcam feed
    inputPath = r"D:\Programing\Projects\Emotion-detection\src\to_sort"
    filesArray = []
    for path, subdirs, files in os.walk(inputPath):
        for name in files:
            filesArray.append(os.path.join(path + "\\", name))
    print(filesArray)
    print(len(filesArray))
    for file in filesArray:
        print(file)
        frame = cv2.imread(file)
        cv2.imshow('Initial', frame)
        # Find haar cascade to draw bounding box around face
        frame = cv2.imread(file)
        cv2.imshow('Initial', frame)

        # frame = cv2.resize(frame, (640, 360))
        # facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_recognition.face_locations(frame, model="hog")

        for (y1, x1, y2, x2) in faces:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            roi_gray = gray[y1:y2, x2:x1]
            print(f'{x1} {x2} {y1} {y2}')

            cv2.imshow('roi', roi_gray)

            cropped_img = np.expand_dims(np.expand_dims(
                cv2.resize(roi_gray, (48, 48)), -1), 0)

            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x2, y2),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Video', frame)

        cv2.waitKey()

    cv2.destroyAllWindows()
