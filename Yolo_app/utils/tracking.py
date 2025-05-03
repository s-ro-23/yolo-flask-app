import cv2
import numpy as np

class Tracker:
    def __init__(self):
        self.next_id = 1

    def update(self, frame, results):
        boxes = results[0].boxes.xyxy.cpu().numpy() if results and results[0].boxes else []
        tracked_ids = []

        for box in boxes:
            x1, y1, x2, y2 = map(int, box[:4])
            obj_id = self.next_id
            self.next_id += 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'ID: {obj_id}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            tracked_ids.append(obj_id)

        return frame, tracked_ids
