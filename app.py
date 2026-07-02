from flask import Flask, request, jsonify, render_template
import torch
import numpy as np
import json
import requests
from transformers import Wav2Vec2Model
import tempfile
import os
import librosa

# -------- CREATE APP --------
app = Flask(__name__)

pending_command = None   # 👈 ADD THIS LINE HERE

# -------- HOME ROUTE --------
@app.route("/")
def home():
    return render_template("index.html")

# -------- LOAD LABELS --------
with open("models/label_map.json") as f:
    label2id = json.load(f)

id2label = {v: k for k, v in label2id.items()}
NUM_LABELS = len(id2label)

# -------- MODEL --------
class Wav2Vec2Classifier(torch.nn.Module):
    def __init__(self, num_labels):
        super().__init__()
        self.encoder = Wav2Vec2Model.from_pretrained("facebook/mms-1b-all")
        self.classifier = torch.nn.Linear(
            self.encoder.config.hidden_size,
            num_labels
        )

    def forward(self, input_values):
        outputs = self.encoder(input_values)
        hidden = outputs.last_hidden_state
        pooled = hidden.mean(dim=1)
        return self.classifier(pooled)

device = "cpu"

model = Wav2Vec2Classifier(NUM_LABELS)
model.load_state_dict(torch.load("models/model_final.pt", map_location=device))
model.to(device)
model.eval()

print("✅ Model loaded")

# -------- ESP32 --------
BASE = "http://192.168.4.1"

def send_command(cmd):
    command_map = {
        "light_on": "/light/on",
        "light_off": "/light/off",
        "fan_on": "/fan/on",
        "fan_off": "/fan/off",
        "bright_light": "/led/bright",
        "dim_light": "/led/dim",
        "led_off": "/led/off",
        "call_help": "/help",
        "call_home": "/home"
    }

    if cmd in command_map:
        endpoint = command_map[cmd]
        try:
            requests.get(f"{BASE}{endpoint}", timeout=2)
            print("📡 Sent:", endpoint)
        except Exception as e:
            print("⚠️ ESP32 not reachable:", e)
    else:
        print("⚠️ Unknown command:", cmd)

# -------- PREDICT FUNCTION --------
def predict(audio):
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    if np.max(np.abs(audio)) != 0:
        audio = audio / np.max(np.abs(audio))

    x = torch.tensor(audio, dtype=torch.float32).unsqueeze(0).to(device)

    with torch.no_grad():
        out = model(x)

    pred = torch.argmax(out, dim=1).item()
    return id2label[pred]

# -------- API ROUTE --------
@app.route("/predict", methods=["POST"])
def predict_api():
    temp_path = None
    try:
        print("📥 Received request")

        file = request.files.get("audio")
        if file is None:
            return jsonify({"error": "No audio file provided"})

        audio_bytes = file.read()

        # 🔥 IMPORTANT: keep format same as frontend (webm)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(audio_bytes)
            temp_path = tmp.name

        # 🔥 Load properly
        audio, sr = librosa.load(temp_path, sr=16000, mono=True)

        if audio is None or len(audio) == 0:
            return jsonify({"error": "Empty audio"})

        print("🎧 Audio loaded:", audio.shape)

    
        global pending_command

        command = predict(audio)
        print("🔮 Predicted:", command)

        # If already waiting for confirmation
        if pending_command:
            if command == "yes":
                send_command(pending_command)
                print("✅ Confirmed:", pending_command)
                pending_command = None
                return jsonify({"status": "confirmed", "command": command})

            elif command == "no":
                print("❌ Cancelled:", pending_command)
                pending_command = None
                return jsonify({
                    "status": "retry",
                    "message": "Okay, let's try again"
                })
            
        # If new command detected
        if command in [
            "light_on",
            "light_off",
            "fan_on",
            "fan_off",
            "bright_light",
            "dim_light",
            "led_off",
            "call_help",
            "call_home"
        ]:
            pending_command = command
            print("⏳ Waiting for confirmation:", command)
            return jsonify({"status": "pending", "command": command})
        
        else:
            print("⚠️ Ignored:", command)
            return jsonify({
                "status": "retry",
                "message": "I didn't catch that"
            })



    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)})

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)