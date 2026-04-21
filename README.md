# AI-Physio: Real-Time Rehabilitation Pose Assessment System

AI-Physio is a high-performance, edge-based physiotherapy assistant designed to provide real-time assessment of exercise form using computer vision. The system tracks 33 body landmarks to calculate joint angles, count repetitions via a state-machine logic, and provide immediate audio-visual feedback to the user. All processing is done locally to ensure data privacy and low-latency performance.

## Core Features

- Real-Time Pose Tracking: Utilizes MediaPipe BlazePose for accurate 33-landmark skeleton detection.
- Biomechanical Evaluation: Supports 24 specific exercises across four categories (Core, Lower Body, Upper Body, and Mobility).
- Automated Repetition Counting: Employs a hysteresis-based state machine for robust movement detection.
- Intelligent Feedback System: Provides corrective audio cues and visual indicators for form deviations.
- Local Analytics Dashboard: Stores session data in a local SQLite database for historical progress tracking.
- Fully Offline Operation: Requires no cloud APIs or external processing, running efficiently on standard CPU hardware.

## System Architecture

The application is built on a modular backend using Python and Flask, integrated with SocketIO for real-time data streaming.

1. Capture Layer: OpenCV handles video stream acquisition from local hardware.
2. Inference Layer: MediaPipe processes frames to extract skeletal landmarks.
3. Logic Layer: Custom services calculate joint angles and manage exercise state transitions.
4. Persistence Layer: SQLite manages user profiles, session aggregates, and rep-by-rep event logs.
5. Presentation Layer: A responsive web interface built with vanilla JavaScript and Chart.js.

## Project Structure

- app.py: Main entry point for the Flask-SocketIO server.
- config.py: Centralized application settings and hardware indices.
- database/: Contains the SQLite database helpers and SQL schema definitions.
- services/: Core logic including pose estimation, angle math, and exercise tracking.
- templates/: HTML5 UI components for the live sessions and analytics dashboard.
- static/: CSS and JS assets for the frontend.
- docs/: Detailed technical documentation and evaluation papers.
- utils/: Common utility functions and logging setup.

## Exercise Categories

| Core & Back | Lower Body | Upper Body | Mobility |
|---|---|---|---|
| Glute Bridge | Squats | Wall Push-ups | Cat-Cow |
| Plank | Wall Sit | Shoulder Rolls | Heel Slides |
| Bird Dog | Clamshells | Chin Tucks | Ankle Circles |
| Superman | Leg Raises | Wall Slides | Child's Pose |

## Installation and Setup

### 1. Environment Preparation
It is recommended to use a virtual environment with Python 3.10 or later.

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Dependency Installation
Install the necessary libraries via pip:

```powershell
pip install -r requirements.txt
```

### 3. Execution
Launch the local development server:

```powershell
python app.py
```
Access the application at http://localhost:5000 in your preferred browser.

## Technical Details

For detailed information regarding joint angle calculations, state machine thresholds, and the biomechanical engineering principles behind the platform, refer to the documentation in the docs/TECHNICAL_DOCS.md file.

## License

This project is released under the MIT License.
