import cv2
import logging

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
                logging.info("No more frames to read from camera.")
                break
            yield frame
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
                logging.info("No more frames to read from file.")
                break
            yield frame
        self.cap.release()
