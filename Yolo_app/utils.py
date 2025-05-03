import cv2
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO('yolov8n.pt')  # You can change to yolov8s.pt, yolov8m.pt if you want bigger models

def detect_objects(frame):
    # Convert frame to RGB for YOLO
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Perform detection
    results = model.predict(source=rgb_frame, save=False, imgsz=640, verbose=False)
    
    # Results is a list (even for one image)
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # (x1, y1, x2, y2)
        confidences = result.boxes.conf.cpu().numpy()  # confidence scores
        classes = result.boxes.cls.cpu().numpy()  # class IDs
        
        for box, conf, cls in zip(boxes, confidences, classes):
            x1, y1, x2, y2 = map(int, box)
            label = model.names[int(cls)]
            confidence = conf * 100

            # Draw rectangle and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.1f}%", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame
