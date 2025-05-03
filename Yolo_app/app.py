import os
import logging
import cv2
from flask import Flask, render_template, request, Response, redirect, url_for
from detector import VideoStream, UploadedVideo

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html', video_path=None)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        video = request.files.get('video')
        if video:
            if video.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
                video.save(path)
                logging.info(f"Video saved: {path}")
                
                # Send path to template
                return render_template('index.html', video_path=path)
            else:
                logging.error("Invalid file type.")
                return "Invalid file type. Only video files are allowed.", 400
        else:
            logging.error("No video uploaded.")
            return "No video uploaded", 400
    except Exception as e:
        logging.error(f"Error during upload: {e}")
        return "An error occurred during upload.", 500

@app.route('/video_feed')
def video_feed():
    video_source = request.args.get('source', default='0')

    logging.info(f"Video source received: {video_source}")

    if video_source.isdigit():
        stream = VideoStream(source=int(video_source))
    else:
        stream = UploadedVideo(file_path=video_source)

    def generate():
        try:
            for frame in stream.read_frames():
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except Exception as e:
            logging.error(f"Error in video feed: {e}")
            yield b''

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
