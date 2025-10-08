# Project Roadmap (Draft)

> **Note**: This is my initial suggestion for how we could approach the project. Feel free to edit, reorder, or completely change anything! Let's discuss and adjust as we go.

---

## Phase 1: Proof of Concept (2-4 weeks)

**Goal**: Get the hardware working and collecting basic heart rate data.

### Proposed Tasks

- [ ] Set up T-Watch S3 development environment
- [ ] Run basic T-Watch examples from LILYGO library
- [ ] Connect MAX30102 sensor to T-Watch via I²C
- [ ] Test sensor communication (I²C scanner)
- [ ] Read raw PPG data from MAX30102
- [ ] Preprocess signals (basic filtering, averaging)
- [ ] Visualize PPG waveforms on watch screen
- [ ] Calculate basic heart rate (BPM)
- [ ] Calculate SpO2 (blood oxygen)
- [ ] Display readings on watch display

### Success Criteria
✅ Watch consistently shows heart rate within ±5 BPM of medical device  
✅ SpO2 reading appears reasonable (95-100% for healthy person)  
✅ PPG waveform visible and shows clear peaks

### Resources Needed
- Arduino IDE installed
- SparkFun MAX3010x library
- TFT_eSPI library for display
- Patience for debugging I²C issues!

---

## Phase 2: Data Pipeline (2-3 weeks)

**Goal**: Send data from watch to server and store it.

### Proposed Tasks

- [ ] Set up WiFi/Bluetooth connection on T-Watch
- [ ] Send heart rate data via HTTP POST (or BLE if using Bluetooth)
- [ ] Create Python Flask/FastAPI backend
- [ ] Set up SQLite database  (or PostgreSQL for production later)
- [ ] Create API endpoint to receive readings
- [ ] Store readings in database
- [ ] Create simple web page to view data
- [ ] Display real-time readings
- [ ] Show historical data (charts/graphs)

### Success Criteria
✅ Watch successfully connects to WiFi/Bluetooth
✅ Data appears in database within 1 second  
✅ Web dashboard shows live heart rate  
✅ Can view last 24 hours of data

### Resources Needed
- Flask or FastAPI knowledge
- SQLite/SQLAlchemy basics
- Chart.js or similar for visualization
- React or HTML+JS for dashboard (if we decide to build it)

---

## Phase 3: Intelligence Layer

**Goal**: Add smart detection of abnormal patterns.

### Proposed Tasks
*Totally flexible on these - just some ideas:*

- [ ] Research normal vs abnormal heart patterns
- [ ] Implement Heart Rate Variability (HRV) analysis
- [ ] Create rule-based anomaly detection
  - Tachycardia (HR > 120)
  - Bradycardia (HR < 50)
  - Sudden changes (±30 BPM in short time)
- [ ] Add alert notifications
- [ ] Research ML models for arrhythmia detection
- [ ] If possible, train basic ML model *(This might be ambitious)*
- [ ] Test with real cardiac event data (if available)

### Success Criteria
✅ System detects when HR is abnormally high/low  
✅ Alert sent within 10 seconds of detection  
✅ False positive rate < 5%

### Resources Needed
- Medical literature on cardiac patterns
- Possibly labeled cardiac datasets
- scikit-learn or TensorFlow

---

## Phase 4: Validation

**Goal**: Validate accuracy and get real-world feedback.

### Proposed Tasks
*Just some suggestions - we can refine this later:*

- [ ] Compare readings with medical-grade pulse oximeter
- [ ] Test on multiple people (different ages, conditions)
- [ ] Document accuracy statistics
- [ ] Get feedback from healthcare professionals
- [ ] Consider pilot study with willing participants
- [ ] Improve based on feedback

### Success Criteria
✅ Readings within acceptable medical tolerance  
✅ Positive feedback from test users  
✅ No false alarms that cause panic