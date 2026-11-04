from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
import secrets
import string
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip', 'mp4', 'mp3'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# In-memory storage for file metadata (use database in production)
file_storage = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_code(length=6):
    """Generate a random alphanumeric code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Generate unique code
        code = generate_code()
        while code in file_storage:
            code = generate_code()
        
        # Save file with code as prefix
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{code}_{filename}")
        file.save(file_path)
        
        # Store metadata
        file_storage[code] = {
            'filename': filename,
            'original_filename': file.filename,
            'file_path': file_path,
            'upload_time': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(hours=24)).isoformat(),
            'downloads': 0
        }
        
        return jsonify({
            'success': True,
            'code': code,
            'filename': filename,
            'message': 'File uploaded successfully!'
        }), 200
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/download/<code>', methods=['GET'])
def download_file(code):
    if code not in file_storage:
        return jsonify({'error': 'Invalid code or file expired'}), 404
    
    file_info = file_storage[code]
    
    # Check if file expired
    if datetime.now() > datetime.fromisoformat(file_info['expires']):
        # Clean up expired file
        if os.path.exists(file_info['file_path']):
            os.remove(file_info['file_path'])
        del file_storage[code]
        return jsonify({'error': 'File has expired'}), 404
    
    # Increment download count
    file_storage[code]['downloads'] += 1
    
    # Send file
    try:
        return send_file(
            file_info['file_path'],
            as_attachment=True,
            download_name=file_info['original_filename']
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check/<code>', methods=['GET'])
def check_file(code):
    """Check if a file exists and get its info"""
    if code not in file_storage:
        return jsonify({'error': 'Invalid code or file not found'}), 404
    
    file_info = file_storage[code]
    
    # Check if expired
    if datetime.now() > datetime.fromisoformat(file_info['expires']):
        if os.path.exists(file_info['file_path']):
            os.remove(file_info['file_path'])
        del file_storage[code]
        return jsonify({'error': 'File has expired'}), 404
    
    return jsonify({
        'filename': file_info['original_filename'],
        'upload_time': file_info['upload_time'],
        'expires': file_info['expires'],
        'downloads': file_info['downloads']
    }), 200

@app.route('/files', methods=['GET'])
def list_files():
    """List all active files (for admin/debugging)"""
    active_files = []
    for code, info in file_storage.items():
        if datetime.now() < datetime.fromisoformat(info['expires']):
            active_files.append({
                'code': code,
                'filename': info['original_filename'],
                'downloads': info['downloads']
            })
    return jsonify(active_files)

# Clean up expired files periodically (basic implementation)
@app.before_request
def cleanup_expired_files():
    """Remove expired files"""
    expired_codes = []
    for code, info in file_storage.items():
        if datetime.now() > datetime.fromisoformat(info['expires']):
            if os.path.exists(info['file_path']):
                try:
                    os.remove(info['file_path'])
                except:
                    pass
            expired_codes.append(code)
    
    for code in expired_codes:
        del file_storage[code]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)