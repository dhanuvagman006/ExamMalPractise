from flask import Flask, render_template, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DETECTION_FOLDER=SCRIPT_DIR+"/batch/"

@app.route('/')
def index():
    images = []
    for root, _, files in os.walk(DETECTION_FOLDER):
        for f in files:
            if f.lower().endswith(('.jpg','.png','.jpeg')):
                rel_path = os.path.relpath(os.path.join(root, f), DETECTION_FOLDER)
                images.append(rel_path)
    return render_template('index.html', images=images)

@app.route('/detections/<path:filename>')
def serve_image(filename):
    return send_from_directory(DETECTION_FOLDER, filename)
@app.route('/api/stats')
def get_stats():
    count = 0
    for root, _, files in os.walk(DETECTION_FOLDER):
        count += len([f for f in files if f.lower().endswith(('.jpg','.png','.jpeg'))])
        
    return {'total_detections': count, 'folder': DETECTION_FOLDER}
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)