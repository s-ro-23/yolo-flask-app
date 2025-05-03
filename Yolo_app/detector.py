import cv2
import logging
from ultralytics import YOLO

# Load YOLOv8 model (make sure this file exists or provide the correct path)
model = YOLO('yolov8n.pt')  # or your custom weights file

class VideoStream:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            logging.error(f"Cannot open camera {source}")
            raise ValueError("Cannot open camera.")

    def read_frames(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            results = model.predict(frame, conf=0.4, stream=False)
            for r in results:
                annotated_frame = r.plot()
                yield annotated_frame

        self.cap.release()

class UploadedVideo:
    def __init__(self, file_path):
        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            logging.error(f"Cannot open video file {file_path}")
            raise ValueError("Cannot open video file.")

    def read_frames(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            results = model.predict(frame, conf=0.4, stream=False)
            for r in results:
                annotated_frame = r.plot()
                yield annotated_frame

        self.cap.release()
