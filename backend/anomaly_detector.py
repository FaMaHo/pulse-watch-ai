def detect_anomaly(heart_rate: int, spo2: float) -> dict | None:
    """
    Detect if heart rate or SpO2 values are abnormal.
    Returns anomaly info or None if normal.
    """
    
    # Tachycardia (high heart rate)
    if heart_rate > 120:
        severity = "high" if heart_rate > 150 else "medium"
        return {
            "anomaly_type": "tachycardia",
            "severity": severity,
            "description": f"Heart rate abnormally high: {heart_rate} BPM"
        }
    
    # Bradycardia (low heart rate)
    if heart_rate < 50:
        severity = "high" if heart_rate < 40 else "medium"
        return {
            "anomaly_type": "bradycardia",
            "severity": severity,
            "description": f"Heart rate abnormally low: {heart_rate} BPM"
        }
    
    # Low oxygen
    if spo2 < 90:
        severity = "critical" if spo2 < 85 else "high"
        return {
            "anomaly_type": "hypoxemia",
            "severity": severity,
            "description": f"Blood oxygen level low: {spo2}%"
        }
    
    return None  # No anomaly detected