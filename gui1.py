import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import face_recognition
import cv2
import os

# Load known faces from 'known_faces' folder
def load_known_faces():
    known_encodings = []
    known_names = []
    known_faces_dir = "known_faces"

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

class FaceRecognitionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Recognition App")
        self.master.geometry("800x600")
        self.master.configure(bg="#f0f0f0")

        self.known_encodings, self.known_names = load_known_faces()

        self.title_label = tk.Label(master, text="Face Recognition GUI", font=("Arial", 20, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select Image", command=self.select_image, font=("Arial", 14))
        self.select_button.pack(pady=10)

        self.image_label = tk.Label(master, bg="#f0f0f0")
        self.image_label.pack(pady=10)

    def select_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if filepath:
            self.recognize_faces(filepath)

    def recognize_faces(self, image_path):
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = self.known_names[match_index]

            cv2.rectangle(image_bgr, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(image_bgr, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        pil_image.thumbnail((700, 500))  # Resize for display
        photo = ImageTk.PhotoImage(pil_image)

        self.image_label.configure(image=photo)
        self.image_label.image = photo

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
