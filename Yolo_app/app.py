from flask import Flask, render_template, request, Response, redirect, url_for
import os
from utils.detection import gen_frames

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    if file:
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        return redirect(url_for('video_feed', source=file.filename))
    return redirect(url_for('index'))

@app.route('/video_feed/<source>')
def video_feed(source):
    path = os.path.join(app.config['UPLOAD_FOLDER'], source)
    return Response(gen_frames(path), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera_feed')
def camera_feed():
    return Response(gen_frames(0), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
