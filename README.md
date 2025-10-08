# Pulse Watch AI

A smart bracelet for continuous heart monitoring using LILYGO T-Watch S3 and MAX30102 PPG sensor, with AI-powered cardiac anomaly detection.

## 🎯 Project Goal

We’re creating a smart bracelet that continuously monitors heart data (via PPG sensor) and uses AI to detect early signs of potential cardiac issues - especially for patients with conditions like heart scoliosis - to enable proactive care.


## 🛠 Hardware

- **LILYGO T-Watch S3 Plus** - ESP32-S3 smartwatch with display
- **MAX30102 Sensor** - PPG heart rate and SpO2 sensor
- **Connection**: I²C interface between watch and sensor

## 📐 Technical Plan

### Firmware (C++ / Arduino)
- Read raw PPG/heart-rate data from MAX30102
- Preprocess signals (filtering, averaging)
- Send data via Wi-Fi/Bluetooth to server

### Backend (Python)
- Flask or FastAPI server
- Store data in SQLite/PostgreSQL
- Run AI/ML models to flag abnormal patterns

### Visualization
- Web dashboard (React or HTML+JS)
- Live data visualization
- Alert system for anomalies

## 🚀 Getting Started

### Hardware Setup
1. Order LILYGO T-Watch S3 Plus
2. Connect MAX30102 to watch via I²C
3. Install Arduino IDE with ESP32 support

### Software Setup
```bash
# Clone the repository
git clone https://github.com/FaMaHo/pulse-watch-ai.git
cd pulse-watch-ai

```

## 📁 Project Structure

```
pulse-watch-ai/
└── docs/              # Documentation
```