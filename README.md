# Smart Face & Sensor System

This project integrates face recognition, sensor monitoring (distance, temperature, humidity), and a GUI dashboard using Raspberry Pi.

## Features

- Face Recognition using OpenCV and face_recognition
- Real-time Distance Measurement with Ultrasonic Sensor
- DHT22 Temperature & Humidity Sensing
- Object Detection Tracker
- GPIO Buzzer Alert
- Tkinter GUI Dashboard

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
sudo apt-get install libatlas-base-dev
```

### 2. Hardware Required

- Raspberry Pi
- Ultrasonic Sensor (HC-SR04)
- DHT22 Sensor
- IR Object Tracker
- Buzzer
- Camera Module or USB Webcam

### 3. Directory Setup

Ensure the following folders exist:

```bash
mkdir -p dataset known_faces trainer
```

- `dataset/` — for face images (named like `User.1.jpg`)
- `known_faces/` — subfolders for each person's images
- `trainer/` — stores the trained face model

### 4. Train Face Recognition Model

Run:
```bash
python3 02_face_training.py
```

### 5. Run the GUI System

Run:
```bash
python3 all.py
```

## Example

![GUI Screenshot](assets/screenshot.png)

## Notes

- Face recognition requires good lighting and clear frontal images.
- Make sure all sensors are wired correctly to the designated GPIO pins.

## Credits

Based on code by:
- Anirban Kar: [GitHub](https://github.com/thecodacus/Face-Recognition)
- Marcelo Rovai (MJRoBot.org)
