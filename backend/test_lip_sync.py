import requests
import json

url = "http://127.0.0.1:5000/speak"
payload = {"text": "Hello world"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Status Code: 200")
        if "audio_url" in data:
            print("✅ Audio URL present")
        else:
            print("❌ Audio URL missing")
            
        if "lip_sync" in data:
            print("✅ Lip Sync Data present")
            # print(json.dumps(data["lip_sync"], indent=2))
            if "mouthCues" in data["lip_sync"]:
                 print(f"✅ Found {len(data['lip_sync']['mouthCues'])} mouth cues")
            else:
                 print("❌ Invalid lip sync structure")
        else:
            print("❌ Lip Sync Data missing")
    else:
        print(f"❌ Status Code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")
