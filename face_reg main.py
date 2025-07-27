'''
Real Time Face Recognition

Each face stored in dataset/ directory should have a unique numeric ID (e.g., 1, 2, 3...).
Trained model is saved in trainer/trainer.yml.
Face recognition is based on LBPH using OpenCV.

Original code by Anirban Kar, modified by Marcelo Rovai, further improved below.
'''

import cv2
import numpy as np
import os

# Load LBPH trained recognizer and face cascade
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

# List of known names (id=0 is reserved as 'unknown' placeholder)
names = ['unknown', 'timothy', 'paula', 'ilza', 'z', 'w']

# Initialize camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # width
cam.set(4, 480)  # height

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    img = cv2.flip(img, -1)  # vertically flip

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id_predicted, confidence = recognizer.predict(roi_gray)

        # Lower confidence means better match
        if confidence < 60:
            if 0 < id_predicted < len(names):
                name = names[id_predicted]
            else:
                name = "unknown"
        else:
            name = "unknown"

        confidence_text = f"  {round(100 - confidence)}%"

        # Draw rectangle and labels
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, confidence_text, (x+5, y+h-5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff
    if k == 27:  # ESC to quit
        break

# Cleanup
print("\n[INFO] Exiting Program and cleaning up...")
cam.release()
cv2.destroyAllWindows()
