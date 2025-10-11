# Project Roadmap

> **Current Focus**: Phase 1 (Proof of Concept) + Phase 2 (Data Pipeline) running in parallel

---

## Phase 1: Proof of Concept (2-4 weeks)

**Goal**: Get the hardware working and collecting basic heart rate data.

### Hardware Tasks (When device arrives)

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

---

## Phase 2: Data Pipeline (2-3 weeks) **← CURRENT PRIORITY**

**Goal**: Send data from watch to server and store it.

### Backend Tasks (Work on these now!)

- [x] Set up Python FastAPI backend
- [x] Create API endpoint to receive sensor readings
- [ ] Set up database (SQLite for dev, PostgreSQL for production)
- [ ] Design database schema
  - `readings` table: timestamp, user_id, heart_rate, spo2, raw_ppg
  - `anomalies` table: timestamp, type, severity
- [ ] Create data validation & error handling
- [ ] Build mock data generator for testing

### Frontend Tasks

- [ ] Create simple web page to view data
- [ ] Display real-time readings (WebSocket or polling)
- [ ] Show historical data (charts/graphs using Chart.js)
- [ ] Build alert notification UI

### Firmware Tasks (When hardware arrives)

- [ ] Set up WiFi connection on T-Watch
- [ ] Send heart rate data via HTTP POST
- [ ] Implement retry logic for failed transmissions

### Success Criteria
✅ Backend API successfully receives and stores mock data  
✅ Watch successfully connects to WiFi (when ready)  
✅ Data appears in database within 1 second  
✅ Web dashboard shows live heart rate  
✅ Can view last 24 hours of data

---

## Phase 3: Intelligence Layer (4-6 weeks)

**Goal**: Add smart detection of abnormal patterns.

### Proposed Tasks

- [ ] Research normal vs abnormal heart patterns
- [ ] Implement Heart Rate Variability (HRV) analysis
- [ ] Create rule-based anomaly detection
  - Tachycardia (HR > 120)
  - Bradycardia (HR < 50)
  - Sudden changes (±30 BPM in short time)
  - Irregular patterns (potential arrhythmia)
- [ ] Add alert notifications (email/push/SMS)
- [ ] Research ML models for arrhythmia detection
- [ ] Train basic ML model on cardiac datasets
- [ ] Test with real cardiac event data (if available)

### Success Criteria
✅ System detects when HR is abnormally high/low  
✅ Alert sent within 10 seconds of detection  
✅ False positive rate < 5%

### Resources Needed
- Medical literature on cardiac patterns
- Labeled cardiac datasets (PhysioNet, MIMIC)
- scikit-learn or TensorFlow

---

## Phase 4: Validation & Testing (2-3 weeks)

**Goal**: Validate accuracy and get real-world feedback.

### Proposed Tasks

- [ ] Compare readings with medical-grade pulse oximeter
- [ ] Test on multiple people (different ages, conditions)
- [ ] Document accuracy statistics
- [ ] Calculate sensitivity and specificity
- [ ] Get feedback from healthcare professionals (if possible)
- [ ] Consider pilot study with willing participants
- [ ] Improve based on feedback
- [ ] Write final documentation

### Success Criteria
✅ Readings within acceptable medical tolerance  
✅ Positive feedback from test users  
✅ No false alarms that cause panic  
✅ System stable for 24+ hour continuous monitoring
