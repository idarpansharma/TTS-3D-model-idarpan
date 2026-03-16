import subprocess
import json
import os

# Configuration
RHUBARB_PATH = os.path.join("bin", "rhubarb")  # Path to the tool
AUDIO_FILE = "test_audio.mp3"                  # The audio we made in Phase 1
OUTPUT_JSON = "../frontend/lip_sync.json"      # Where to save the mouth data

def generate_lip_sync():
    print(f"Analyzing {AUDIO_FILE} for mouth shapes...")

    # Check if files exist
    if not os.path.exists(RHUBARB_PATH):
        print(f"ERROR: Rhubarb tool not found at {RHUBARB_PATH}")
        return
    if not os.path.exists(AUDIO_FILE):
        print(f"ERROR: Audio file not found at {AUDIO_FILE}")
        return

    # Convert MP3 to WAV if needed (Rhubarb only supports WAV/OGG)
    current_audio_file = AUDIO_FILE
    if AUDIO_FILE.lower().endswith(".mp3"):
        wav_file = AUDIO_FILE.rsplit(".", 1)[0] + ".wav"
        print(f"Converting {AUDIO_FILE} to {wav_file}...")
        try:
            subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", AUDIO_FILE, wav_file], check=True)
            current_audio_file = wav_file
        except subprocess.CalledProcessError:
            print("ERROR: Failed to convert audio file using afconvert.")
            return

    command = [RHUBARB_PATH, "-f", "json", "-o", OUTPUT_JSON, current_audio_file]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Success! Lip sync data saved to: {OUTPUT_JSON}")
        else:
            print("Error running Rhubarb:")
            print(result.stderr)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_lip_sync()