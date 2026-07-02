# 🧠 SpeakEasy: A Personalized Smart Home Assistant for Dysarthric Speech

> An AI-powered smart home assistant designed to help individuals with dysarthric speech interact with home appliances using voice commands.

---

## 📖 Overview

SpeakEasy is a final-year undergraduate project that enables individuals with dysarthric speech to control smart home devices through voice commands. The system leverages a fine-tuned **Wav2Vec2** speech recognition model with **LoRA (Low-Rank Adaptation)** to recognize dysarthric speech accurately and convert it into actionable smart home commands.

The application provides an intuitive web interface for recording speech, predicts the intended command, requests user confirmation to reduce incorrect actions, and then communicates with an ESP32-based smart home controller to execute the command.

---

## ✨ Features

* 🎤 Browser-based voice recording
* 🧠 AI-powered dysarthric speech recognition
* 🚀 Fine-tuned Wav2Vec2 model using LoRA
* 🌐 Flask-based web application
* 🏠 ESP32 smart home integration
* ✅ Confirmation step ("Yes" / "No") before executing commands
* ⚡ Real-time command prediction
* ♿ Designed specifically for accessibility

---

## 🏠 Supported Voice Commands

* Light On
* Light Off
* Fan On
* Fan Off
* Bright Light
* Dim Light
* LED Off
* Call Help
* Call Home
* Yes (confirmation)
* No (cancel)

---

## 🛠️ Technology Stack

| Category             | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| Deep Learning        | PyTorch               |
| Speech Model         | Wav2Vec2 MMS-1B       |
| Fine-Tuning          | LoRA                  |
| Web Framework        | Flask                 |
| Audio Processing     | Librosa               |
| Hardware             | ESP32                 |
| Frontend             | HTML, CSS, JavaScript |

---

## 🔄 System Workflow

1. User records a voice command using the web interface.
2. The audio is preprocessed and converted to the required format.
3. The fine-tuned Wav2Vec2 model predicts the spoken command.
4. The system asks the user for confirmation.
5. After confirmation, the command is sent to the ESP32.
6. The corresponding smart home appliance performs the requested action.

---

## 📂 Project Structure

```text
SpeakEasy/
│
├── app.py
├── requirements.txt
├── models/
├── Training Notebook/
├── Testing Notebook/
├── Output Images/
├── static/
└── templates/
```

---

## 🚀 Installation

1. Clone the repository.
2. Install the required dependencies.

```bash
pip install -r requirements.txt
```

3. Add the trained model to the `models` directory (not included in this repository).
4. Run the application.

```bash
python app.py
```

---

## 📸 Screenshots

Screenshots will be added soon.

---

## 🔮 Future Improvements

* Improve recognition accuracy with larger dysarthric speech datasets.
* Support additional smart home devices.
* Enable cloud deployment.
* Add multilingual support.
* Integrate voice authentication for enhanced security.

---

## 👨‍💻 Contributors

Developed as a final-year undergraduate team project by:

* **Adithyan V**
* **Anjana S**
* **Haifa Shanavas**

---

## 📄 License

This project is licensed under the MIT License.
