import wave
import math
import struct
import os

# Configuration
FILENAME = "test_audio.wav"
DURATION = 3.0  # Seconds
FREQUENCY = 440.0  # Hz (A4)
FRAMERATE = 44100

def generate_clean_audio():
    print(f"Generating clean audio file: {FILENAME}...")
    
    # Generate 3 seconds of audio data
    audio_data = []
    num_samples = int(DURATION * FRAMERATE)
    
    for i in range(num_samples):
        # Generate sine wave
        value = int(32767.0 * math.cos(FREQUENCY * math.pi * float(i) / float(FRAMERATE)))
        # Pack as 16-bit little-endian
        data = struct.pack('<h', value)
        audio_data.append(data)

    # Write to WAV file
    with wave.open(FILENAME, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes (16-bit)
        wav_file.setframerate(FRAMERATE)
        wav_file.writeframes(b''.join(audio_data))

    print(f"✅ Success! {FILENAME} created.")
    print(f"📂 File size: {os.path.getsize(FILENAME)} bytes")

if __name__ == "__main__":
    generate_clean_audio()