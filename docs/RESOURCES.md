# Resources & References

---

## 🎯 Clinical & Medical References

* **Heart Sclerosis Definition**: Pathological replacement of healthy heart muscle (myocardium) with fibrous/scar tissue, leading to impaired function.
* **Causes**: Myocardial infarction, chronic ischemia, myocarditis, and degenerative aging.
* **Symptom-Sensor Correlation**: Detailed table mapping clinical manifestations (e.g., Arrhythmias, Fatigue, Dyspnea) to measurable wearable signals (HRV, Activity, HR Trends).

---

## 💾 AI/ML Datasets (Pre-training)

These datasets are crucial for pre-training our models on signal quality and clinical conditions:

* **PulseDB (MIMIC-III / VitalDB Derivative)**: High-quality, cleaned **PPG, ECG** segments with extracted **beat-to-beat points**. Excellent for training on **PPG Morphology** and precise HRV extraction.
* **PPG-DaLiA (PPG + Accelerometer during Daily Activities)**: Contains wrist-worn **PPG and Accelerometer (ACC)** data from daily life. **Essential for training motion artifact reduction** and activity-level correlation.
* **BIDMC Congestive Heart Failure Database (CHFDB)**: Long-term **ECG recordings** from subjects with severe CHF (a condition resulting from myocardial fibrosis). **Crucial for providing the clinical label** (Compromised Heart Function) for the AI model.

---

## 🛠 Signal Processing & Data Analysis Tools

* **Python Libraries for PPG/HRV Analysis**:
    * **WFDB (WaveForm DataBase)**: Toolset for reading and processing standard PhysioNet data formats.
    * **hrv-analysis**: Dedicated Python package for extracting Time, Frequency, and Non-Linear HRV features.
    * **SciPy/NumPy**: Used for signal filtering (e.g., Butterworth bandpass filter) and general signal processing.

---

## 💻 Hardware & Software Documentation

* **LILYGO T-Watch S3 Official GitHub**: `https://github.com/Xinyuan-LilyGO/TTGO_TWatch_Library`
* **MAX30102 Datasheet**: `https://www.analog.com/media/en/technical-documentation/data-sheets/max30102.pdf`
* **Backend Framework**: FastAPI Documentation: `https://fastapi.tiangolo.com/`
* **ORM**: SQLAlchemy ORM Quick Start: `https://docs.sqlalchemy.org/en/20/orm/quickstart.html`
* **PostgreSQL Best Practices**: For high-volume time-series data storage and query optimization (e.g., partitioning, indexing on timestamps).
