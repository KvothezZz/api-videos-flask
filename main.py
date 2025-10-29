from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import os
import tempfile

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}
MAX_FILE_SIZE = 100 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Flask Video Processing API',
        'version': '1.0.0'
    }), 200

@app.route('/render', methods=['POST'])
def render():
    if 'video' not in request.files:
        return jsonify({
            'error': 'No video file provided',
            'message': 'Please upload a video file with the key "video"'
        }), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({
            'error': 'No file selected',
            'message': 'Please select a video file to upload'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'error': 'Invalid file type',
            'message': f'Allowed file types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        filename = secure_filename(file.filename)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_input:
            file.save(temp_input.name)
            input_path = temp_input.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='_processed.mp4') as temp_output:
            output_path = temp_output.name
        
        try:
            video = VideoFileClip(input_path)
            
            duration = video.duration
            fps = video.fps
            size = video.size
            
            processed_video = video.subclip(0, min(5, duration))
            processed_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            video.close()
            processed_video.close()
            
            output_size = os.path.getsize(output_path)
            
            os.unlink(input_path)
            os.unlink(output_path)
            
            return jsonify({
                'success': True,
                'message': 'Video processed successfully',
                'original': {
                    'filename': filename,
                    'duration': duration,
                    'fps': fps,
                    'resolution': f'{size[0]}x{size[1]}'
                },
                'processed': {
                    'duration': min(5, duration),
                    'size_bytes': output_size,
                    'note': 'This is a demo that processes the first 5 seconds of the video'
                }
            }), 200
            
        except Exception as e:
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
            raise e
            
    except Exception as e:
        return jsonify({
            'error': 'Video processing failed',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
