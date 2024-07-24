import cv2
import pygame
import time
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Initialize Pygame mixer
pygame.mixer.init()

# Load the MP3 file
pygame.mixer.music.load('greet (2).mp3')

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the video capture (0 for the default camera)
cap = cv2.VideoCapture(0)

def play_greeting():
    pygame.mixer.music.play()
    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def detect_faces(frame):
    # Convert frame to grayscale for Haar Cascade
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def update_frame():
    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    # Detect faces in the current frame
    faces = detect_faces(frame)

    # Draw bounding boxes around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # If faces are detected
    if len(faces) > 0:
        # Play the greeting
        play_greeting()

    # Convert the frame to a format suitable for Tkinter
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    root.after(10, update_frame)

# Create the main window
root = tk.Tk()
root.title("Face Detector")

# Create a label to display the video feed
lmain = Label(root)
lmain.pack()

# Start updating the frame
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
