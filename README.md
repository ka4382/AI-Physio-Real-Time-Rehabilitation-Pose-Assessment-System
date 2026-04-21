# ⚡ AI-Physio — Real-Time Rehabilitation Pose Assessment System

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/framework-Flask-red.svg)](https://flask.palletsprojects.com/)
[![MediaPipe](https://img.shields.io/badge/vision-MediaPipe-green.svg)](https://google.github.io/mediapipe/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready, edge-based physiotherapy assistant that uses computer vision to assess exercise form, count repetitions, and provide real-time audio+visual feedback — all running locally on your machine.

---

## 🎯 Key Features

- **24+ Supported Exercises** — From orthopaedic recovery (Heel Slides, Clamshells) to core strength (Plank, Bird Dog).
- **Real-Time Pose Detection** — Powered by MediaPipe BlazePose for clinical-grade landmark tracking.
- **Biomechanical Logic** — Real-time joint angle calculation and state-machine based rep counting.
- **Intelligent Feedback** — 
  - **Visual Interventions**: Red/Green joint indicators and form overlays.
  - **Audio Coaching**: Offline TTS providing immediate corrective cues.
- **Comprehensive Analytics** — Dashboard featuring Chart.js visualizations for accuracy, volume, and progress tracking.
- **Secure Data Persistence** — Local SQLite storage for session history and user profiles.

---

## 📁 Project Structure

```text
├── app.py                  # Flask + SocketIO Entry Point
├── config.py               # Application Configuration
├── requirements.txt        # Dependencies
├── database/               # SQLite Helpers and Schema
├── services/               # Core Logic (Pose, Angle, Exercise, Feedback)
├── templates/              # Modern UI (HTML)
├── static/                 # Stylesheets and Javascript
├── docs/                   # Detailed Technical Documentation
└── utils/                  # Helper Functions
```

---

## 🚀 Quick Start (Windows)

### 1. Environment Setup
```powershell
# Clone the repository
git clone https://github.com/ka4382/AI-Physio-Real-Time-Rehabilitation-Pose-Assessment-System.git
cd AI-Physio-Real-Time-Rehabilitation-Pose-Assessment-System

# Create & Activate Virtual Environment
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Launch Application
```powershell
python app.py
```
👉 Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 🔬 How it Works

1. **Capture**: The system accesses your webcam via OpenCV.
2. **Detection**: MediaPipe identifies 33 3D landmarks on your body.
3. **Mathematics**: The `AngleService` computes vectors and joint angles using trigonometric dot products.
4. **Assessment**: The `ExerciseTracker` runs a state machine to validate each repetition against clinical thresholds.
5. **Instruction**: Real-time feedback is pushed via WebSockets to the UI and Audio service.

For a deeper dive into the math and algorithms, see **[TECHNICAL_DOCS.md](docs/TECHNICAL_DOCS.md)**.

---

## 🏋️ Exercise Categories

| Core & Back | Lower Body | Upper Body | Mobility |
|---|---|---|---|
| Glute Bridge | Squats | Wall Push-ups | Cat-Cow |
| Plank | Wall Sit | Shoulder Rolls | Heel Slides |
| Bird Dog | Clamshells | Chin Tucks | Ankle Circles |
| Superman | Leg Raises | Wall Slides | Child's Pose |

---

## 🛠️ Tech Stack

*   **Backend**: Python, Flask, Flask-SocketIO
*   **Computer Vision**: OpenCV, MediaPipe
*   **Database**: SQLite
*   **Frontend**: Tailwind CSS, Vanilla JS, Chart.js
*   **Audio**: pyttsx3

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
