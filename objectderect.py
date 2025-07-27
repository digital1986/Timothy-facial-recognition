import cv2
import numpy as np

# Load the pre-trained model and configuration file
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')

# Define the list of class labels MobileNet SSD was trained to detect
CLASSES = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 
           'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 
           'tvmonitor']

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Get the frame dimensions
    (h, w) = frame.shape[:2]

    # Prepare the frame for the model
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # Loop over the detections and draw bounding boxes
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        # Filter weak detections
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])

            # Get bounding box coordinates
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw the bounding box and label
            label = f"{CLASSES[idx]}: {confidence:.2f}"
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with detections
    cv2.imshow("Object Detection", frame)

    # Exit loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
