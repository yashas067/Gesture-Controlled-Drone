# 🚁 Gesture-Controlled Drone using Computer Vision

An AI-powered autonomous drone control system that allows a user to control a drone using hand gestures instead of a traditional remote controller. The system also performs real-time face detection and tracking using computer vision techniques.

---

## 📌 Project Overview

This project integrates **Computer Vision**, **MediaPipe**, **OpenCV**, **MAVSDK**, **PX4 Autopilot**, **Gazebo Simulation**, and **QGroundControl** to create an intelligent drone control system.

The webcam captures live video, detects hand gestures and faces, converts them into drone movement commands, and sends those commands to the PX4 flight controller through MAVSDK.

---

## ✨ Features

- ✋ Real-time Hand Gesture Recognition
- 😊 Real-time Face Detection
- 🎯 Face Tracking
- 🚁 Gesture-Based Drone Navigation
- 📡 MAVSDK Communication
- 🛰 PX4 SITL Simulation
- 🌍 Gazebo Drone Simulation
- 🎮 QGroundControl Monitoring
- 💻 Fully Software-Based Prototype

---

# 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python 3.10 |
| Computer Vision | OpenCV |
| AI Framework | MediaPipe |
| Face Detection Model | BlazeFace |
| Hand Detection Model | MediaPipe Hands |
| Drone SDK | MAVSDK |
| Flight Controller | PX4 Autopilot |
| Drone Simulator | Gazebo Sim |
| Ground Control Station | QGroundControl |
| Communication Protocol | MAVLink |
| Operating System | Windows + WSL Ubuntu |

---

# 🏗 System Architecture

```
                  Webcam
                     │
                     ▼
            OpenCV Video Capture
                     │
                     ▼
     MediaPipe Face & Hand Detection
                     │
                     ▼
       Gesture Recognition Logic
                     │
                     ▼
      Python Drone Control Program
                     │
                     ▼
                MAVSDK API
                     │
                     ▼
             MAVLink Protocol
                     │
                     ▼
            PX4 Autopilot (SITL)
                     │
                     ▼
            Gazebo Drone Simulator
                     │
                     ▼
            QGroundControl GUI
```

---

# 📂 Project Structure

```
Gesture-Controlled-Drone
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── src
│   ├── drone_brain.py
│   ├── drone_tracker.py
│   ├── gesture_drone_control.py
│   ├── gesture_recognition.py
│   ├── keyboard_drone.py
│   ├── realtime_face.py
│   └── tests
│       ├── drone_test.py
│       ├── face_test.py
│       ├── gesture_test.py
│       └── test_movement.py
│
├── docs
├── images
├── videos
├── models
└── assets
```

---

# 🤖 Models Used

## Face Detection

- BlazeFace
- Developed by Google
- Optimized for real-time detection
- Used through MediaPipe

### Why BlazeFace?

- Lightweight
- High speed
- Low latency
- Works well on CPU
- Suitable for drones

---

## Hand Detection

MediaPipe Hands

Features

- Detects 21 Hand Landmarks
- Real-time tracking
- Works without GPU
- Accurate fingertip detection

---

# 📷 Images

## Gazebo Simulation

> Add image here

```
images/gazebo_simulation.png
```

---

## QGroundControl

> Add image here

```
images/qgroundcontrol_interface.png
```

---

## System Architecture

> Add image here

```
images/project_architecture.png
```

---

# 🚀 Installation

Clone Repository

```bash
git clone https://github.com/yashas067/Gesture-Controlled-Drone.git
```

Go inside project

```bash
cd Gesture-Controlled-Drone
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Project

Start PX4 Simulation

```bash
start_px4.bat
```

Start MAVSDK Server

```bash
mavsdk_server.exe -p 50051
```

Run Gesture Controller

```bash
python src/gesture_drone_control.py
```

---

# 📈 Workflow

1. Webcam captures live video.
2. OpenCV reads video frames.
3. MediaPipe detects hands and face.
4. Gesture Recognition module identifies gestures.
5. Python converts gesture into movement commands.
6. MAVSDK sends commands using MAVLink.
7. PX4 receives commands.
8. Gazebo simulates drone movement.
9. QGroundControl displays drone telemetry.

---

# 🎯 Future Scope

- Voice Control
- Obstacle Avoidance
- Object Detection
- Autonomous Navigation
- GPS Waypoint Missions
- Mobile App Integration
- Multi-Drone Control
- AI-based Gesture Learning

---

# 👨‍💻 Author

**S Yashas**

Artificial Intelligence & Data Science

SJC Institute of Technology

GitHub

https://github.com/yashas067

LinkedIn

https://www.linkedin.com/in/s-yashas-312536389

---

# ⭐ If you like this project

Please consider giving it a ⭐ on GitHub.