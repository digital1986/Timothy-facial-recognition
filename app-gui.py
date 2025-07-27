import tkinter as tk
from tkinter import filedialog, messagebox
import face_recognition
import cv2
import os
from PIL import Image, ImageTk

# Load known faces
known_faces_dir = "known_faces"
known_encodings = []
known_names = []

for name in os.listdir(known_faces_dir):
    person_dir = os.path.join(known_faces_dir, name)
    for filename in os.listdir(person_dir):
        image_path = os.path.join(person_dir, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)

# GUI application
class FaceRecognitionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Recognition App")
        self.master.geometry("600x400")

        self.label = tk.Label(master, text="Choose an image to recognize faces", font=("Arial", 14))
        self.label.pack(pady=10)

        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.button = tk.Button(master, text="Select Image", command=self.select_image)
        self.button.pack(pady=20)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.recognize_faces(file_path)

    def recognize_faces(self, image_path):
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        image_cv = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]

            cv2.rectangle(image_cv, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(image_cv, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Show result image
        image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil.thumbnail((500, 300))
        photo = ImageTk.PhotoImage(image_pil)

        self.image_label.configure(image=photo)
        self.image_label.image = photo

# Create the GUI window
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
