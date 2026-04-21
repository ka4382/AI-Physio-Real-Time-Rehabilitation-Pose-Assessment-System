# AI-Physio: Technical Documentation

This document provides a deep dive into the engineering principles, mathematical logic, and architecture of the AI-Physio platform.

## 1. Pose Estimation Engine
The system utilizes **MediaPipe BlazePose** as its core vision engine. BlazePose provides 33 3D landmarks for the human body at high frame rates (20-30 FPS on typical CPUs).

### Model Configuration
- **Complexity**: 1 (Balanced for real-time performance)
- **Landmarks**: 33 keypoints (mapped to standard COCO/MediaPipe indices)
- **Smoothing**: Adaptive filters enable smooth skeleton visualization even with minor occlusion.

## 2. Biomechanical Math: Joint Angle Calculation
The core of exercise evaluation is the calculation of angles between body segments. We compute the angle at a specific joint (e.g., knee) using the three landmarks forming that joint (e.g., hip, knee, ankle).

### The Formula
Given three points $A$ (Hip), $B$ (Knee), and $C$ (Ankle), we calculate the vectors $\vec{BA}$ and $\vec{BC}$:
1. $\vec{u} = A - B$
2. $\vec{v} = C - B$
3. Angle $\theta = \arccos\left(\frac{\vec{u} \cdot \vec{v}}{|\vec{u}| |\vec{v}|}\right)$

The result is converted from radians to degrees for intuitive feedback.

## 3. Repetition Counting State Machine
To ensure accurate counting and prevent "cheating," the system uses a **Hysteresis-based State Machine**.

### States:
- **`UP`**: User is in the starting position (e.g., standing for a squat).
- **`DOWN`**: User has reached the target depth.

### Transition Logic (Squat Example):
- **UP -> DOWN**: Occurs when the knee angle drops below $95^\circ$.
- **DOWN -> UP**: Occurs when the knee angle rises above $150^\circ$.
- **Rep Completion**: A rep is counted only when the user returns to the `UP` state after transitioning through `DOWN`.

## 4. Exercise Evaluation Logic
Each of the 24 supported exercises has a specific configuration in `exercise_service.py`.

### Threshold Categories:
- **Static Holds**: (e.g., Plank, Wall Sit) Measures time duration while maintaining an angle within a specific tolerance.
- **Dynamic Reps**: (e.g., Bicep Curls, Squats) Measures the range of motion and ensures the "peak" angle hits the target depth.

### Correctness Criteria:
- **Perfect Rep**: Peak angle falls within `(correct_min, correct_max)`.
- **Too Shallow**: User returned to `UP` without reaching the required depth.
- **Form Error**: Secondary joints (e.g., back leaning during a squat) moved outside the allowed range.

## 5. Data Architecture
The platform uses **SQLite** for lightweight, local-first persistence.

- **`users`**: Authentication and anthropometric data (height, weight).
- **`sessions`**: Aggregate data per exercise set (reps, accuracy, duration).
- **`rep_events`**: High-resolution data for every single repetition, storing the peak angle for accuracy analysis.
- **`feedback_log`**: Temporal record of all real-time corrections provided to the user.

## 6. Feedback Engine
- **Visual**: Real-time skeleton overlay with per-joint color coding (Green = Correct, Red = Error).
- **Audio**: Multi-threaded TTS (pyttsx3) providing clinical-grade cues based on error codes.
