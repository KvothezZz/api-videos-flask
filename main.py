from flask import Flask, request, jsonify, send_file
from moviepy.editor import VideoFileClip, CompositeVideoClip
import tempfile
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'Flask Video Processing API', 'version': '1.0.0'}), 200

@app.route('/render', methods=['POST'])
def render_video():
    try:
        face = request.files.get('face')
        screen = request.files.get('screen')
        pecho = request.files.get('pecho')
        
        if not all([face, screen, pecho]):
            return jsonify({'error': 'Missing files. Required: face, screen, pecho'}), 400
        
        with tempfile.TemporaryDirectory() as tmpdir:
            face_path = os.path.join(tmpdir, 'face.mp4')
            screen_path = os.path.join(tmpdir, 'screen.mp4')
            pecho_path = os.path.join(tmpdir, 'pecho.mp4')
            output_path = os.path.join(tmpdir, 'final.mp4')
            
            face.save(face_path)
            screen.save(screen_path)
            pecho.save(pecho_path)
            
            screen_clip = VideoFileClip(screen_path).resize((1080, 1920))
            face_clip = VideoFileClip(face_path).resize(height=710)
            pecho_clip = VideoFileClip(pecho_path).resize((1080, 1920))
            
            final = CompositeVideoClip([
                screen_clip,
                face_clip.set_position(('center', 80)),
                pecho_clip.set_start(0).set_duration(screen_clip.duration)
            ])
            
            final.write_videofile(output_path, codec='libx264', audio_codec='aac', preset='fast')
            
            return send_file(output_path, mimetype='video/mp4', as_attachment=True, download_name='video_final.mp4')
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
