from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import os
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}
MAX_FILE_SIZE = 100 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'error':
        'File too large',
        'message':
        f'Maximum file size is {MAX_FILE_SIZE / (1024 * 1024):.0f}MB'
    }), 413


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Flask Video Processing API',
        'version': '1.0.0'
    }), 200


@app.route('/render', methods=['POST'])
def render_video():
    data = request.json
    heygen = data['heygen']
    pantalla = data['pantalla']
    pecho = data['pecho']
    return jsonify({"status": "received", "videos": [heygen, pantalla, pecho]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
