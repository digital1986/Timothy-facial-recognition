import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import face_recognition
import cv2
import os
import numpy as np
import uuid

# Load known faces
def load_known_faces(known_faces_dir="known_faces"):
    known_encodings = []
    known_names = []
    if not os.path.exists(known_faces_dir):
        os.makedirs(known_faces_dir)

    for name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, name)
        if not os.path.isdir(person_dir):
            continue
        for filename in os.listdir(person_dir):
            filepath = os.path.join(person_dir, filename)
            image = face_recognition.load_image_file(filepath)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(name)
    return known_encodings, known_names

# Save face from webcam to known_faces
def save_face_image(name):
    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Capture", "Press 's' to save a face or 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Capture Face - Press 's' to Save", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                top, right, bottom, left = face_locations[0]
                face_image = frame[top:bottom, left:right]
                person_dir = os.path.join("known_faces", name)
                os.makedirs(person_dir, exist_ok=True)
                filename = os.path.join(person_dir, f"{uuid.uuid4()}.jpg")
                cv2.imwrite(filename, face_image)
                break
            else:
                messagebox.showwarning("No Face", "No face detected, try again.")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

class FaceRecognitionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Recognition App")
        self.master.geometry("800x600")

        self.known_encodings, self.known_names = load_known_faces()

        self.title_label = tk.Label(master, text="Face Recognition GUI", font=("Arial", 20))
        self.title_label.pack(pady=10)

        self.image_label = tk.Label(master)
        self.image_label.pack()

        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Select Image", command=self.select_image).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Live Recognition", command=self.live_recognition).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Add New Face", command=self.add_new_face).grid(row=0, column=2, padx=10)

    def refresh_known_faces(self):
        self.known_encodings, self.known_names = load_known_faces()

    def select_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if filepath:
            image = face_recognition.load_image_file(filepath)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_encodings, encoding)
                name = "Unknown"
                if True in matches:
                    index = matches.index(True)
                    name = self.known_names[index]

                cv2.rectangle(image_bgr, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(image_bgr, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            img.thumbnail((700, 500))
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

    def live_recognition(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small)
            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

            for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_encodings, encoding)
                name = "Unknown"
                if True in matches:
                    index = matches.index(True)
                    name = self.known_names[index]

                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2.imshow("Live Recognition - Press 'q' to quit", frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def add_new_face(self):
        name = simpledialog.askstring("New Face", "Enter name of the person:")
        if name:
            save_face_image(name)
            self.refresh_known_faces()
            messagebox.showinfo("Success", f"Face for '{name}' added!")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
