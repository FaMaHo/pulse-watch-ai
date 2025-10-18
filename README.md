# Pulse Watch AI: AI Bracelet for Heart Monitoring

A smart bracelet system for **continuous, non-invasive physiological monitoring** to detect early indicators of serious cardiovascular conditions, primarily focusing on patterns associated with **Myocardial Fibrosis (Cardiosclerosis)**. 

## 🎯 Core Objective

To develop an AI-powered system that analyzes patterns in Heart Rate Variability (**HRV**), **Pulse Waveform Morphology**, and **activity levels** (biosignals) collected from a wrist-worn device to identify anomalies associated with early-stage **Heart Sclerosis (Cardiosclerosis)**.

[cite_start]This approach focuses on **early detection** and **preventive healthcare** for at-risk populations (e.g., post-MI patients, elderly) by non-invasively detecting the scarring of healthy heart muscle (myocardium)[cite: 1, 5, 23, 24, 25].

## 📊 Current Status

- ✅ **Hardware Confirmed:** MAX30102 PPG sensor received; [cite_start]LILYGO T-Watch S3 Plus ordered[cite: 29, 30].
- ✅ **System Architecture Planned:** Full stack defined from sensor to cloud.
- 🔄 **AI Pre-training in Progress:** Utilizing public cardiac datasets to build a foundational model while awaiting custom hardware.
- 📝 **PostgreSQL Schema Designed:** Database architecture ready for real-time sensor data ingestion.

## 🛠 Technical Stack

| Layer | Component | Details |
| :--- | :--- | :--- |
| **Hardware** | LILYGO T-Watch S3 Plus + MAX30102 PPG | Collects **raw PPG and Accelerometer** data. [cite_start]Uses **I²C** connection. [cite: 17, 29, 30] |
| **Firmware** | C++ / Arduino (PlatformIO) | [cite_start]Filters noise on-device to conserve power; transmits cleaned data (HR/HRV) via Wi-Fi/Bluetooth[cite: 40, 42, 43]. |
| **Backend/DB** | **FastAPI (Python)** + **PostgreSQL** | [cite_start]Ingests real-time JSON data; stores high-volume sensor streams and extracted metrics[cite: 45, 46]. |
| **AI/ML** | Python (TensorFlow/scikit-learn) | **1D CNNs** for morphology analysis; **LSTMs** for long-term HRV trend detection; [cite_start]**Anomaly Detection** for alerting[cite: 47]. |
| **Frontend** | Web Dashboard (React or HTML+JS) | [cite_start]Real-time data visualization and anomaly alerting[cite: 48, 49]. |

## 🚀 Immediate Next Steps

1.  [cite_start]Set up **PlatformIO/Arduino IDE** for T-Watch development[cite: 53].
2.  [cite_start]Test MAX30102 sensor communication (with Arduino Uno/breadboard)[cite: 54].
3.  [cite_start]**Implement Mock Data Generator** to stress-test the full `Watch -> FastAPI -> PostgreSQL` pipeline[cite: 56].
4.  Begin **AI Model Pre-training** using public cardiac datasets (e.g., PulseDB, PPG-DaLiA).

---

## Setup (Backend)

1. Clone the repository and navigate to the backend directory:
```bash
git clone [https://github.com/FaMaHo/pulse-watch-ai.git](https://github.com/FaMaHo/pulse-watch-ai.git)
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
