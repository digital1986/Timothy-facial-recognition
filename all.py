import RPi.GPIO as GPIO
import time
import threading
import tkinter as tk
from tkinter import ttk
import Adafruit_DHT
import math
import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageTk
import os

# GPIO Setup
GPIO.setmode(GPIO.BCM)
TRIG, ECHO, BUZZER, TRACKER_PIN, DHT_PIN = 23, 24, 21, 2, 22
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(TRACKER_PIN, GPIO.IN)

running = True

# Load known faces
known_face_encodings = []
known_face_names = []

def load_known_faces():
    for person_name in os.listdir("known_faces"):
        person_folder = os.path.join("known_faces", person_name)
        if os.path.isdir(person_folder):
            for img_name in os.listdir(person_folder):
                img_path = os.path.join(person_folder, img_name)
                image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(person_name)

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    duration = pulse_end - pulse_start
    return round(duration * 17150, 2)

def detect_object():
    return GPIO.input(TRACKER_PIN) == 1

def read_dht():
    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT_PIN)

# GUI App
class SensorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Sensor Dashboard")
        self.root.geometry("600x500")
        self.root.configure(bg="#121212")

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TLabel", background="#121212", foreground="white", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TProgressbar", troughcolor="#333", background="#00bfff", thickness=20)

        self.build_ui()
        self.angle = 0
        self.face_running = False

        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.animate()

    def build_ui(self):
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="#121212", highlightthickness=0)
        self.canvas.place(x=20, y=20)
        self.sonar = self.canvas.create_oval(90, 90, 110, 110, outline="cyan")

        frame = ttk.Frame(self.root, padding=10)
        frame.place(x=250, y=20)

        self.distance_label = ttk.Label(frame, text="Distance: -- cm")
        self.distance_label.pack(anchor="w", pady=5)

        self.object_label = ttk.Label(frame, text="Object: Not Detected", foreground="green")
        self.object_label.pack(anchor="w", pady=5)

        self.temp_label = ttk.Label(frame, text="Temp: -- °C | Humidity: -- %")
        self.temp_label.pack(anchor="w", pady=10)

        self.temp_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
        self.temp_bar.pack(pady=5)

        self.toggle_button = ttk.Button(self.root, text="Stop Monitoring", command=self.toggle_monitoring)
        self.toggle_button.place(x=250, y=150)

        self.face_toggle = ttk.Button(self.root, text="Start Face Recognition", command=self.toggle_face_recognition)
        self.face_toggle.place(x=400, y=150)

        self.video_label = tk.Label(self.root, bg="#1e1e1e")
        self.video_label.place(x=250, y=200, width=320, height=240)

    def toggle_monitoring(self):
        global running
        running = not running
        self.toggle_button.config(text="Start Monitoring" if not running else "Stop Monitoring")

    def toggle_face_recognition(self):
        if not self.face_running:
            self.face_running = True
            self.face_toggle.config(text="Stop Face Recognition")
            self.face_thread = threading.Thread(target=self.face_loop)
            self.face_thread.daemon = True
            self.face_thread.start()
        else:
            self.face_running = False
            self.face_toggle.config(text="Start Face Recognition")

    def update_loop(self):
        while True:
            if running:
                try:
                    dist = measure_distance()
                    self.distance_label.config(text=f"Distance: {dist} cm")

                    object_detected = dist < 10 or detect_object()
                    GPIO.output(BUZZER, GPIO.HIGH if object_detected else GPIO.LOW)
                    self.object_label.config(
                        text="Object: Detected" if object_detected else "Object: Not Detected",
                        foreground="red" if object_detected else "green"
                    )

                    temp, hum = read_dht()
                    if temp and hum:
                        self.temp_bar["value"] = min(temp, 50)
                        self.temp_label.config(text=f"Temp: {temp:.1f} °C | Humidity: {hum:.1f} %")
                except:
                    pass
            time.sleep(1)

    def face_loop(self):
        cap = cv2.VideoCapture(0)
        while self.face_running:
            ret, frame = cap.read()
            if not ret:
                continue

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small)
            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

            names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances =_
