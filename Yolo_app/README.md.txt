# YOLOv8 Flask Video Detection App 🎥🧠

## 📌 Features

- 🔍 YOLOv8-based object detection
- 🎯 Real-time video stream or uploaded file
- 🧮 Region-wise object counting
- 🚗 Speed estimation per object
- 📊 Live statistics display

---

## 🚀 Run with Docker (Recommended)

```bash
docker build -t flask-yolo-app .
docker run -d -p 5000:5000 --name yolo-app flask-yolo-app
