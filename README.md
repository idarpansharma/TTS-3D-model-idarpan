# TTS-3D: Text-to-Speech Driven 3D Avatar System

## 🚀 Project Overview

TTS-3D is an open source, cross-platform project that combines text-to-speech (TTS), real-time audio analysis, and 3D avatar lip-syncing. It integrates Python backend tools with a WebGL/VRM frontend to animate humanoid avatars based on spoken text input, enabling interactive virtual presenters, game NPCs, accessibility characters, and multimedia demos.

Key features:
- Python-based TTS/audio pipeline in `backend/`
- Lip sync audio-to-viseme mapping using Rhubarb (included)
- Support for VRM avatars in `frontend/`
- Modular architecture for easy adaptation to other renderers

## 📁 Repository Structure

- `backend/`
  - `server.py` – HTTP server for generating audio and lip-sync data
  - `generate_beep.py` – test utility to generate waveforms (beeps)
  - `lip_sync.py` – core viseme parsing and timing logic
  - `inspect_avatar.py` – helper for VRM avatar shape key inspection
  - `bin/rhubarb` – lip sync engine binary (bundled)

- `frontend/`
  - `index.html` – demo UI and 3D rendering harness
  - `*.vrm` – sample avatars (e.g., `avatar6.vrm`, `model-1.vrm`)
  - HDR textures for lighting presets
  - Animation presets in `expression/`, `idle/`, `locomotion/`

## 🧩 How It Works

1. User enters text in frontend (or API request) and submits.
2. Backend generates TTS audio and stores a `.wav` output.
3. `lip_sync.py` calls Rhubarb on generated audio and returns viseme timing JSON.
4. Frontend reads viseme frames and animates avatar blend shapes in sync with speech.

## ⚙️ Requirements

### Python (backend)
- Python 3.10+ (3.11 recommended)
- pip dependencies:
  - `numpy`
  - `soundfile`
  - `scipy`
  - `pyttsx3` (if local TTS)
  - `flask` (if `server.py` uses it)

### Frontend
- Modern web browser with WebGL 2
- No additional build step required for static demo

### Optional tools
- `ffmpeg` (for audio conversions)
- `rhubarb` is included under `backend/bin/rhubarb`

## 🛠️ Setup and Run

### Backend (local)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # create this if missing
python server.py
```

### Frontend

Open `frontend/index.html` in a browser or run a local server:

```bash
cd frontend
python3 -m http.server 8000
# then open http://localhost:8000
```

### Using the demo
- Load a VRM avatar file
- Enter text to speak
- Press play to see lips and face animate in sync

## 🧪 Testing

- `backend/test_lip_sync.py` covers lip-sync timing conversion logic.

```bash
cd backend
pytest test_lip_sync.py
```

## 💡 Customization Guide

- Swap the VRM model in `frontend/`
- Tune viseme blending by editing `frontend/index.html` animation curves
- Replace TTS engine in `backend` with cloud engine (e.g., Azure, Google, OpenAI) by modifying server endpoints and audio output format

## 💬 Notes

- `backend/bin/rhubarb` is the default articulator. If you want `rhubarb` from system path, adjust `lip_sync.py` to call the system binary.
- Frontend-core uses procedural animation data in `lip_sync.json` and can be integrated with any Three.js or Babylon.js avatar runtime.

## 📄 License

Add your preferred license (MIT, Apache 2.0, etc.).

## 🙌 Contributing

1. Fork repo
2. Create feature branch `feature/your-update`
3. Add tests and documentation
4. Open a pull request

---
### 3-D Model ui
![App ui](screenshots/app-ui.png)

### 3-D Model ui
![App ui](screenshots/app-ui2.png)

> This `README` is generated to make the repo approachable for new collaborators, and to give a strong baseline for expanding to monetized avatars, virtual presenters, or telepresence applications.
