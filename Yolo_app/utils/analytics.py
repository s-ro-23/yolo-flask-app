import cv2

def draw_statistics(frame, tracked_ids):
    count = len(tracked_ids)
    cv2.putText(frame, f'Total Objects: {count}', (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
