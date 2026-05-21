from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
from waitress import serve
import os
import time

#
# This server is intended to be hosted on some online hosting solution like https://render.com/.
# Buzz should be configured to upload transcripts and translations to this server
# during live recording sessions.
#
# To prevent unauthorized upload of entries you can set a password for uploads
# Set password in the environment variable UPLOAD_PASSWORD. f.e. UPLOAD_PASSWORD="topSecret"
# Then add it to the upload URL. f.e. http://localhost:5000/upload?password=topSecret
#

# Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PORT = int(os.environ.get('PORT', 5000))
UPLOAD_PASSWORD = os.environ.get('UPLOAD_PASSWORD', '')
UPLOAD_DEBUG = os.environ.get('UPLOAD_DEBUG', '')
SITE_TITLE = os.environ.get('SITE_TITLE', 'Buzz transcription server')
TALK_TITLE = os.environ.get('TALK_TITLE', 'Powered by Mozilla Common Voice data')
SHOW_TRANSLATION = os.environ.get('SHOW_TRANSLATION', '').lower() in ('1', 'true', 'yes', 'on')
TRAFFIC_COUNTER_CODE = os.environ.get('TRAFFIC_COUNTER_CODE', '')

entries = []

@app.route('/')
def serve_client():
    with open('client.html', 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('{{SITE_TITLE}}', SITE_TITLE).replace('{{TALK_TITLE}}', TALK_TITLE)
    html = html.replace('{{TRANSLATION_DISPLAY}}', 'block' if SHOW_TRANSLATION else 'none')
    html = html.replace('{{TRANSLATION_CHECKED}}', 'checked' if SHOW_TRANSLATION else '')
    html = html.replace('{{TRAFFIC_COUNTER_CODE}}', TRAFFIC_COUNTER_CODE)
    return html

@app.route('/NoSleep.min.js')
def serve_nosleep_js():
    return send_file('NoSleep.min.js')

@app.route('/entries')
def serve_entries():
    timestamp = request.args.get('timestamp', type=float)
    if timestamp:  # Treat None and 0 the same — return the tail
        filtered_entries = [entry for entry in entries if entry['timestamp'] > timestamp]
        if filtered_entries:
            return jsonify(filtered_entries)
        return jsonify([]), 200
    if entries:
        return jsonify(entries[-6:])
    return jsonify({"error": "No entries found"}), 404


@app.route('/upload', methods=['POST'])
def upload_entries():
    if UPLOAD_PASSWORD:
        password_in_url = request.args.get('password')

        password_in_body = None
        if request.json:
            if isinstance(request.json, dict):
                password_in_body = request.json.get('password')

        if password_in_body != UPLOAD_PASSWORD and password_in_url != UPLOAD_PASSWORD:
            return jsonify({"error": "Invalid or missing password"}), 401

    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400

    # Handle both single entry or list of entries
    new_entries = request.json
    if not isinstance(new_entries, list):
        new_entries = [new_entries]

    for entry in new_entries:
        if not isinstance(entry, dict):
            return jsonify({"error": "Each entry must be an object"}), 400

        if 'kind' not in entry:
            return jsonify({"error": "Each entry must have a 'kind' property"}), 400

        if entry['kind'] not in ['transcript', 'translation', 'clear']:
            return jsonify({"error": "The 'kind' property must be 'transcript', 'translation' or 'clear'"}), 400

        if 'text' not in entry:
            return jsonify({"error": "Each entry must have a 'text' property"}), 400

        if 'mode' in entry and entry['mode'] not in ['append', 'replace']:
            return jsonify({"error": "The 'mode' property must be 'append' or 'replace'"}), 400

        entry['timestamp'] = time.time()

    for entry in new_entries:
        if entry['kind'] == 'clear':
            entries.clear()

        entries.append(entry)

    if UPLOAD_DEBUG:
        print(f"Uploaded: {new_entries}")

    return jsonify({
        "message": f"Successfully added {len(new_entries)} entries",
        "total_entries": len(entries)
    }), 201

@app.route('/health-check')
def health_check():
    return jsonify({
        "status": "ok",
        "timestamp": time.time(),
        "entries_count": len(entries)
    }), 200

def start_server():
    print(f"Server running on port {PORT}")
    serve(
        app,
        host='0.0.0.0',
        port=PORT,
        connection_limit=300,
        channel_timeout=30,  # Cleanup inactive channels after 30 seconds
        threads=4,  # Number of threads to handle requests, default is 4
    )

if __name__ == "__main__":
    start_server()