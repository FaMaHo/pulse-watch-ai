# Project Roadmap: Early Detection of Cardiosclerosis

> **Current Focus**: Parallel execution of Phase 1 (Hardware Setup) and Phase 2 (Data Pipeline/AI Pre-training).

---

## Phase 1: Hardware Proof of Concept (2-4 weeks)

**Goal**: Get the custom device working, collecting **PPG and Accelerometer** data.

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
✅ PPG waveform visible and shows clear peaks

---

## Phase 2: Data Pipeline & Pre-training (2-3 weeks) **← CURRENT PRIORITY**

**Goal**: Establish a robust real-time data pipeline and build the foundational AI model.

### Backend/Database Tasks
- [x] Set up Python FastAPI backend
- [x] Create API endpoint to receive sensor readings
- [x] [cite_start]Set up **PostgreSQL** database (using SQLite for local dev) [cite: 46]
- [x] Design multi-table database schema (`Users`, `Raw_Sensor_Data`, `Aggregated_Metrics`)
- [ ] Implement robust data validation & error handling
- [ ] [cite_start]Build mock data generator for pipeline stress testing [cite: 56]

### AI/ML Foundation Tasks (New Priority)
- [ ] **Data Acquisition:** Secure and load pre-training datasets (e.g., **PulseDB**, **PPG-DaLiA**, **BIDMC CHF**) for initial model development.
- [ ] **Feature Extraction Pipeline:** Develop Python scripts to reliably extract:
    * **HRV features** (Time/Frequency domain) from IBI/RR-intervals.
    * [cite_start]**Pulse Waveform Morphology features** (e.g., dicrotic notch, crest time)[cite: 13].
    * [cite_start]**Activity/HR Recovery metrics** (from Accelerometer)[cite: 20].
- [ ] **Model Pre-training (Stage 1):** Train a **1D CNN model** on PPG-DaLiA/BUT PPG to learn robust PPG peak detection and noise filtering in motion.

### Success Criteria
✅ Backend API successfully receives and stores mock data into **PostgreSQL** schema.
✅ **Pre-trained AI model** can reliably extract **HRV and morphology features** from public PPG data.
✅ **Full data pipeline** passes a 24-hour stability and latency test.

---

## Phase 3: Intelligence Layer - Cardiosclerosis Detection (4-6 weeks)

**Goal**: Train the final multi-modal model to detect patterns indicative of myocardial fibrosis.

### Proposed Tasks
- [ ] [cite_start]**Model Refinement (Stage 2):** Fine-tune the pre-trained model using clinical datasets (e.g., BIDMC CHF, PulseDB) to classify "Compromised Heart Function" (proxy for Cardiosclerosis) vs. "Healthy"[cite: 14].
- [ ] [cite_start]**Multi-modal Integration:** Combine features from HRV, Morphology (CNN output), and Activity (ACC) into a final **LSTM/DNN** for anomaly scoring[cite: 13].
- [ ] [cite_start]Implement **Symptom-Sensor Correlation Logic** (e.g., Resting HR elevation + Dyspnea correlation)[cite: 20].
- [ ] Create **Unsupervised Anomaly Detector** (e.g., Autoencoder) for flagging novel, subtle patterns.
- [ ] Build the Alerting Service (email/push/SMS).

### Success Criteria
✅ Model exhibits high **Sensitivity** (correctly flagging compromised hearts) on the validation set.
✅ System successfully flags anomalies based on combined **HRV/Morphology/Activity** signals.
✅ Alert sent within acceptable time limit (e.g., < 10 seconds).

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
