import os
import numpy as np
import pandas as pd
import h5py
from scipy.signal import find_peaks
from google.colab import drive

# PATH MANAGEMENT
def setup_paths():
    """Mount drive and return project paths"""
    if not os.path.exists('/content/drive'):
        drive.mount('/content/drive')
    
    paths = {
        'base': '/content/drive/MyDrive/PulseWatch-AI',
        'raw': '/content/drive/MyDrive/PulseWatch-AI/datasets/raw/pulsedb',
        'processed': '/content/drive/MyDrive/PulseWatch-AI/datasets/processed',
        'mimic': '/content/drive/MyDrive/PulseWatch-AI/datasets/raw/pulsedb/Segment_Files/PulseDB_MIMIC',
        'vitaldb': '/content/drive/MyDrive/PulseWatch-AI/datasets/raw/pulsedb/Segment_Files/PulseDB_Vital'
    }
    
    # Create processed folder if it doesn't exist
    os.makedirs(paths['processed'], exist_ok=True)
    
    return paths

# DATA LOADING
def load_signal_from_mat(file_path, signal_type='PPG'):
    """
    Load PPG or ECG signal from .mat file
    
    Parameters:
    -----------
    file_path : str
        Path to .mat file
    signal_type : str
        'PPG' or 'ECG'
    
    Returns:
    --------
    signal : numpy array or None
    """
    try:
        with h5py.File(file_path, 'r') as mat_data:
            if 'Subj_Wins' not in mat_data:
                return None
            
            data_group = mat_data['Subj_Wins']
            signal_key = f'{signal_type}_Record_F'
            
            if signal_key in data_group:
                ref = data_group[signal_key][0, 0]
                signal = np.squeeze(mat_data[ref][:])
                return signal
    except:
        return None
    
    return None

# SIGNAL PROCESSING
def detect_r_peaks(ecg_signal, fs=125):
    """Detect R-peaks in ECG signal"""
    peaks, _ = find_peaks(ecg_signal, distance=75, prominence=0.3)
    return peaks

def detect_ppg_peaks(ppg_signal, fs=125):
    """Detect systolic peaks in PPG signal"""
    peaks, _ = find_peaks(ppg_signal, distance=75, prominence=0.05)
    return peaks

# FEATURE EXTRACTION
def calculate_hrv_features(rr_intervals):
    """Calculate time-domain HRV features"""
    if len(rr_intervals) < 2:
        return None
    
    features = {
        'mean_hr': 60000 / np.mean(rr_intervals),
        'sdnn': np.std(rr_intervals),
        'rmssd': np.sqrt(np.mean(np.diff(rr_intervals) ** 2)),
        'pnn50': (np.sum(np.abs(np.diff(rr_intervals)) > 50) / len(rr_intervals)) * 100,
        'mean_rr': np.mean(rr_intervals),
        'min_rr': np.min(rr_intervals),
        'max_rr': np.max(rr_intervals)
    }
    
    return features

def extract_ppg_features(ppg_signal, ppg_peaks):
    """Extract morphological features from PPG waveform"""
    if len(ppg_peaks) < 2:
        return None
    
    pp_intervals = np.diff(ppg_peaks) * (1000/125)
    peak_amplitudes = ppg_signal[ppg_peaks]
    
    features = {
        'mean_pp': np.mean(pp_intervals),
        'std_pp': np.std(pp_intervals),
        'mean_amplitude': np.mean(peak_amplitudes),
        'std_amplitude': np.std(peak_amplitudes)
    }
    
    return features

# Add this to your utils.py file

def decode_ascii_field(mat_data, field_ref):
    """Helper to decode ASCII-encoded fields"""
    try:
        ascii_array = mat_data[field_ref][:]
        return ''.join([chr(int(x)) for x in ascii_array.flatten()])
    except:
        return None

def extract_metadata(mat_data, data_group, segment_idx=0):
    """
    Extract metadata (Age, Gender, BP, SubjectID) from a segment
    
    Parameters:
    -----------
    mat_data : h5py.File
        Opened .mat file
    data_group : h5py.Group
        The 'Subj_Wins' group
    segment_idx : int
        Which segment to extract (default: 0 = first segment)
    
    Returns:
    --------
    dict with metadata or None if extraction fails
    """
    metadata = {}
    
    try:
        # Age
        if 'Age' in data_group:
            age_ref = data_group['Age'][segment_idx, 0]
            metadata['age'] = float(np.squeeze(mat_data[age_ref][:]))
        else:
            metadata['age'] = None
        
        # Gender (decode from ASCII: 'M' or 'F')
        if 'Gender' in data_group:
            gender_ref = data_group['Gender'][segment_idx, 0]
            gender_str = decode_ascii_field(mat_data, gender_ref)
            metadata['gender'] = gender_str
        else:
            metadata['gender'] = None
        
        # Systolic BP
        if 'SegSBP' in data_group:
            sbp_ref = data_group['SegSBP'][segment_idx, 0]
            metadata['systolic_bp'] = float(np.squeeze(mat_data[sbp_ref][:]))
        else:
            metadata['systolic_bp'] = None
        
        # Diastolic BP
        if 'SegDBP' in data_group:
            dbp_ref = data_group['SegDBP'][segment_idx, 0]
            metadata['diastolic_bp'] = float(np.squeeze(mat_data[dbp_ref][:]))
        else:
            metadata['diastolic_bp'] = None
        
        # Subject ID (decode from ASCII)
        if 'SubjectID' in data_group:
            subj_ref = data_group['SubjectID'][segment_idx, 0]
            metadata['subject_id'] = decode_ascii_field(mat_data, subj_ref)
        else:
            metadata['subject_id'] = None
        
        return metadata
    
    except Exception as e:
        return None

def create_health_label(age, systolic_bp, diastolic_bp):
    """
    Create health risk label based on age and blood pressure
    
    Classification:
    - 0: Low risk (healthy)
    - 1: Moderate risk
    - 2: High risk (likely cardiac issues)
    
    Returns:
    --------
    int: 0, 1, or 2 (or None if data missing)
    """
    if age is None or systolic_bp is None or diastolic_bp is None:
        return None
    
    # Blood pressure risk assessment
    if systolic_bp >= 140 or diastolic_bp >= 90:
        bp_risk = 2  # Stage 2 Hypertension
    elif 130 <= systolic_bp < 140 or 80 <= diastolic_bp < 90:
        bp_risk = 1  # Stage 1 Hypertension
    elif 120 <= systolic_bp < 130 and diastolic_bp < 80:
        bp_risk = 1  # Elevated
    elif systolic_bp < 90:
        bp_risk = 1  # Hypotension (also concerning)
    else:
        bp_risk = 0  # Normal
    
    # Age risk factor
    age_risk = 1 if age >= 65 else 0
    
    # Combined risk score (0-2)
    total_risk = min(bp_risk + age_risk, 2)
    
    return total_risk

def extract_features_with_labels(file_path):
    """Extract features AND labels from .mat file"""
    try:
        with h5py.File(file_path, 'r') as mat_data:
            if 'Subj_Wins' not in mat_data:
                return None
            
            data_group = mat_data['Subj_Wins']
            
            # Load signals
            ecg_ref = data_group['ECG_Record_F'][0, 0]
            ppg_ref = data_group['PPG_Record_F'][0, 0]
            
            ecg = np.squeeze(mat_data[ecg_ref][:])
            ppg = np.squeeze(mat_data[ppg_ref][:])
            
            # Detect peaks
            r_peaks = detect_r_peaks(ecg)
            if len(r_peaks) < 2:
                return None
            
            ppg_peaks = detect_ppg_peaks(ppg)
            
            # Extract features
            rr_intervals = np.diff(r_peaks) * (1000/125)
            hrv_feats = calculate_hrv_features(rr_intervals)
            ppg_feats = extract_ppg_features(ppg, ppg_peaks)
            
            if not hrv_feats or not ppg_feats:
                return None
            
            # Extract metadata
            metadata = extract_metadata(mat_data, data_group, segment_idx=0)
            
            if metadata is None:
                return None
            
            # Create health label
            label = create_health_label(
                metadata['age'],
                metadata['systolic_bp'],
                metadata['diastolic_bp']
            )
            
            # Combine everything
            record = {
                'file_name': os.path.basename(file_path),
                'dataset': 'MIMIC' if 'MIMIC' in file_path else 'VitalDB',
                'subject_id': metadata['subject_id'],
                'num_beats': len(r_peaks),
                **hrv_feats,
                **ppg_feats,
                **metadata,
                'health_label': label  # Our target variable
            }
            
            return record
            
    except Exception as e:
        return None