# Resources & References

---

## 🎯 Clinical & Medical References

* **Heart Sclerosis Definition**: Pathological replacement of healthy heart muscle (myocardium) with fibrous/scar tissue, leading to impaired function.
* **Causes**: Myocardial infarction, chronic ischemia, myocarditis, and degenerative aging.
* **Symptom-Sensor Correlation**: Detailed table mapping clinical manifestations (e.g., Arrhythmias, Fatigue, Dyspnea) to measurable wearable signals (HRV, Activity, HR Trends).

---

## 💾 AI/ML Datasets (Pre-training)

### Foundation Datasets (PPG + ECG Morphology)
* **MIMIC-III Waveform Database**: Hospital-grade PPG, ECG, ABP from ~30,000 ICU patients. Industry standard for cardiovascular ML research. Includes heart failure cases. Requires credentialed access via PhysioNet.
* **PulseDB (MIMIC-III/VitalDB Derivative)**: 5.2M cleaned PPG + ECG segments from 5,361 subjects with beat-to-beat annotations. Pre-processed and ML-ready. https://github.com/pulselabteam/PulseDB

### Motion Artifact Training (PPG + Accelerometer)
* **PPG-DaLiA**: 15 subjects, wrist PPG + 3-axis ACC during daily activities (cycling, walking, working). Essential for motion artifact handling.
* **WESAD**: 15 subjects, wrist BVP + ACC during stress/baseline conditions. Multimodal wearable data.
* **WildPPG**: 16 subjects, 216 hours of real-world outdoor PPG + ACC (hiking, traveling). High motion artifact diversity.
* **GalaxyPPG**: 24 subjects with consumer-grade Galaxy Watch PPG + ACC. Validates commercial wearable performance.

### Disease Labels (Heart Failure / Compromised Function)
* **BIDMC Congestive Heart Failure Database**: 15 subjects with severe CHF, 20-hour ECG recordings. Provides ground truth for compromised heart function. PhysioNet
* **MIMIC-III Clinical Database**: 682 heart failure patients + 954 controls with structured clinical data. Used for disease classification validation.

---

## 🛠 Signal Processing & Data Analysis Tools

* **Python Libraries for PPG/HRV Analysis**:
    * **WFDB (WaveForm DataBase)**: Toolset for reading and processing standard PhysioNet data formats.
    * **hrv-analysis**: Dedicated Python package for extracting Time, Frequency, and Non-Linear HRV features.
    * **SciPy/NumPy**: Used for signal filtering (e.g., Butterworth bandpass filter) and general signal processing.

---

## 💻 Hardware & Software Documentation

* **LILYGO T-Watch S3 Official GitHub**: https://github.com/Xinyuan-LilyGO/TTGO_TWatch_Library
* **MAX30102 Datasheet**: https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf
* **Backend Framework**: FastAPI Documentation: https://fastapi.tiangolo.com/
* **ORM**: SQLAlchemy ORM Quick Start: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
* **PostgreSQL Best Practices**: For high-volume time-series data storage and query optimization (e.g., partitioning, indexing on timestamps).
