from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import edge_tts
import asyncio
import os
import tempfile
import subprocess
import json

app = Flask(__name__)
CORS(app)

# Configuration
VOICE = "en-US-ChristopherNeural"
TEMP_DIR = tempfile.gettempdir()
AUDIO_FILE = os.path.join(TEMP_DIR, "generated_audio.mp3")
WAV_FILE = os.path.join(TEMP_DIR, "generated_audio.wav")
LIP_SYNC_FILE = os.path.join(TEMP_DIR, "lip_sync.json")
# Assuming 'bin/rhubarb' is relative to where server.py is run (backend dir)
RHUBARB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "rhubarb")

import time

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    print(f"🎤 Generating Audio for: {text}")
    start_time = time.time()

    try:
        # Run Edge-TTS
        t0 = time.time()
        asyncio.run(generate_audio(text))
        t1 = time.time()
        print(f"⏱️ TTS Generation: {t1 - t0:.3f}s")
        
        # Generate Lip Sync Data
        t2 = time.time()
        lip_sync_data = generate_lip_sync()
        t3 = time.time()
        print(f"⏱️ Lip Sync Generation: {t3 - t2:.3f}s")
        
        total_time = time.time() - start_time
        print(f"✅ Total Request Time: {total_time:.3f}s")

        # Return URL to frontend
        # We add a random query parameter (?t=...) so the browser doesn't cache the old audio
        return jsonify({
            "audio_url": f"http://127.0.0.1:5000/get_audio?t={os.urandom(4).hex()}",
            "lip_sync": lip_sync_data
        })
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_audio')
def get_audio():
    try:
        return send_file(AUDIO_FILE, mimetype="audio/mpeg")
    except FileNotFoundError:
        return "Audio not found", 404

async def generate_audio(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(AUDIO_FILE)

def generate_lip_sync():
    print("👄 Generating Lip Sync Data...")
    
    # 1. Convert MP3 to WAV (Rhubarb needs WAV)
    # Using afconvert (macOS built-in) as seen in lip_sync.py
    try:
        if os.path.exists(WAV_FILE):
            os.remove(WAV_FILE)
            
        subprocess.run(
            ["afconvert", "-f", "WAVE", "-d", "LEI16", AUDIO_FILE, WAV_FILE], 
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"⚠️ Audio conversion failed: {e}")
        return None

    # 2. Run Rhubarb
    if not os.path.exists(RHUBARB_PATH):
        print(f"⚠️ Rhubarb executable not found at: {RHUBARB_PATH}")
        return None

    try:
        command = [RHUBARB_PATH, "-f", "json", "-o", LIP_SYNC_FILE, WAV_FILE]
        subprocess.run(
            command, 
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # 3. Read and Return JSON
        with open(LIP_SYNC_FILE, 'r') as f:
            return json.load(f)
            
    except Exception as e:
        print(f"⚠️ Rhubarb processing failed: {e}")
        return None

if __name__ == '__main__':
    print("🚀 TTS Server running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)