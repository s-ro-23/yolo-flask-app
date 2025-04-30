import cv2
from ultralytics import YOLO
from utils.tracking import Tracker
from utils.analytics import draw_statistics

model = YOLO("models/yolov8n.pt")
tracker = Tracker()

def gen_frames(source='uploads/MOT20-07-raw.mp4'):
    """
    Generate frames from a video file or a camera feed for MJPEG streaming.
    If 'source' is 0, it reads from the webcam, otherwise from a video file.
    """
    # Open the video source (webcam or video file)
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"[ERROR] Failed to open video source: {source}")
        return

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("[ERROR] Failed to read frame.")
            break

        # Perform object detection and tracking on the frame
        results = model.track(frame, persist=True)
        frame, track_ids = tracker.update(frame, results)
        draw_statistics(frame, track_ids)  # Add statistics (e.g., total count) to frame

        # Encode the frame as JPEG for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("[ERROR] Failed to encode frame.")
            continue

        # Yield the frame in MJPEG format for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    # Release the video capture object when done
    cap.release()
