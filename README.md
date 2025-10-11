# Pulse Watch AI

A smart bracelet for continuous heart monitoring using LILYGO T-Watch S3 and MAX30102 PPG sensor, with AI-powered cardiac anomaly detection.

## 🎯 Project Goal

We're creating a smart bracelet that continuously monitors heart data (via PPG sensor) and uses AI to detect early signs of potential cardiac issues - especially cardiovascular irregularities like heart sclerosis - to enable proactive care.

## 📊 Current Status

- ✅ MAX30102 sensor received 
- ✅ T-Watch S3 Plus ordered
- 🔄 Backend development in progress
- 📝 System architecture planned

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
- PostgreSQL database (SQLite for development)
- REST API for data ingestion
- AI/ML models to flag abnormal patterns

### Visualization
- Web dashboard (React or HTML+JS)
- Live data visualization
- Alert system for anomalies


## Setup
1. Clone the repository
```bash
git clone https://github.com/FaMaHo/pulse-watch-ai.git
cd pulse-watch-ai/backend
```
2. Create virtual environment
```bash
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
bashpip install -r requirements.txt
```

4. Run the server
```bash
bashuvicorn main:app --reload
```

5. Test with mock data
```bash
bashpython mock_data_generator.py
```

6. View API documentation
Open your browser: http://localhost:8000/docs

## 📁 Project Structure

```
pulse-watch-ai/
├── backend/           # FastAPI server
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── anomaly_detector.py
│   └── mock_data_generator.py
├── firmware/          # Arduino/ESP32 code (coming soon)
├── frontend/          # Web dashboard (coming soon)
└── docs/              # Documentation
```
