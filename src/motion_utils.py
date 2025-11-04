"""
Motion-Robust Feature Extraction for PPG-DaLiA Dataset
Phase 2: Motion Artifact Handling

This module extends Phase 1 (utils.py) with motion-aware processing:
- Activity detection from accelerometer
- Signal quality assessment  
- Motion-robust HRV features
- Adaptive filtering based on activity type
"""

import numpy as np
from scipy import signal
from scipy.signal import find_peaks, butter, filtfilt, welch
import pandas as pd


# ========== MOTION DETECTION ==========

def calculate_accelerometer_magnitude(acc_data):
    """
    Calculate magnitude of 3-axis accelerometer
    
    Parameters:
    -----------
    acc_data : numpy array
        Shape (n_samples, 3) for [x, y, z]
    
    Returns:
    --------
    acc_mag : numpy array
        Magnitude signal
    """
    return np.sqrt(np.sum(acc_data**2, axis=1))


def extract_motion_features(acc_data, fs=32, window_sec=5):
    """
    Extract motion intensity features from accelerometer
    
    Features capture:
    - Overall motion level (mean, std)
    - Motion intensity (range)
    - Rhythmic motion (dominant frequency for walking)
    
    Parameters:
    -----------
    acc_data : numpy array
        3-axis accelerometer (n_samples, 3)
    fs : int
        Sampling frequency (Hz)
    window_sec : int
        Analysis window (seconds)
    
    Returns:
    --------
    dict with motion features
    """
    acc_mag = calculate_accelerometer_magnitude(acc_data)
    
    # Time-domain features
    features = {
        'acc_mean': np.mean(acc_mag),
        'acc_std': np.std(acc_mag),
        'acc_range': np.max(acc_mag) - np.min(acc_mag),
        'acc_median': np.median(acc_mag)
    }
    
    # Frequency-domain: Detect rhythmic motion (walking = ~1-2 Hz)
    try:
        freqs, psd = welch(acc_mag, fs=fs, nperseg=min(256, len(acc_mag)))
        dominant_freq = freqs[np.argmax(psd[1:]) + 1]  # Skip DC
        features['dominant_freq'] = dominant_freq
        features['psd_peak'] = np.max(psd[1:])
    except:
        features['dominant_freq'] = 0
        features['psd_peak'] = 0
    
    return features


def classify_activity_intensity(motion_features):
    """
    Classify motion intensity: stationary, light, moderate, vigorous
    
    Based on accelerometer STD thresholds from literature:
    - Stationary: STD < 0.1 g (sitting, lying)
    - Light: 0.1-0.3 g (slow walking, desk work)
    - Moderate: 0.3-0.6 g (brisk walking, stairs)
    - Vigorous: > 0.6 g (running, sports)
    
    Parameters:
    -----------
    motion_features : dict
        Output from extract_motion_features()
    
    Returns:
    --------
    str : 'stationary', 'light', 'moderate', 'vigorous'
    int : intensity_code (0, 1, 2, 3)
    """
    acc_std = motion_features['acc_std']
    
    if acc_std < 0.1:
        return 'stationary', 0
    elif acc_std < 0.3:
        return 'light', 1
    elif acc_std < 0.6:
        return 'moderate', 2
    else:
        return 'vigorous', 3


# ========== SIGNAL QUALITY ASSESSMENT ==========

def calculate_signal_quality_index(ppg_signal, acc_data=None, fs_ppg=64, fs_acc=32):
    """
    Calculate PPG signal quality index (0-1 scale)
    
    Quality indicators:
    1. Peak detectability (can we find consistent peaks?)
    2. Signal-to-noise ratio
    3. Motion correlation (if accelerometer available)
    
    Parameters:
    -----------
    ppg_signal : numpy array
        PPG waveform
    acc_data : numpy array, optional
        3-axis accelerometer
    fs_ppg : int
        PPG sampling rate
    fs_acc : int
        Accelerometer sampling rate
    
    Returns:
    --------
    float : quality index (0 = poor, 1 = excellent)
    """
    quality_score = 0
    weight_total = 0
    
    # 1. Peak detectability (40% weight)
    try:
        peaks, properties = find_peaks(
            ppg_signal, 
            distance=int(0.5 * fs_ppg),  # Min 0.5s between peaks
            prominence=0.05
        )
        
        if len(peaks) >= 3:
            # Check peak regularity
            peak_intervals = np.diff(peaks) / fs_ppg
            cv = np.std(peak_intervals) / np.mean(peak_intervals)  # Coefficient of variation
            
            # Lower CV = more regular = better quality
            peak_quality = np.clip(1 - cv, 0, 1)
            quality_score += 0.4 * peak_quality
        else:
            quality_score += 0  # Too few peaks
        
        weight_total += 0.4
        
    except:
        weight_total += 0.4
    
    # 2. Signal-to-noise ratio (30% weight)
    try:
        # Use wavelet decomposition or simple smoothing
        # High-frequency noise vs. signal power
        from scipy.signal import savgol_filter
        
        smoothed = savgol_filter(ppg_signal, window_length=min(51, len(ppg_signal)//2*2+1), polyorder=3)
        noise = ppg_signal - smoothed
        
        signal_power = np.var(smoothed)
        noise_power = np.var(noise)
        
        if noise_power > 0:
            snr = 10 * np.log10(signal_power / noise_power)
            snr_quality = np.clip(snr / 20, 0, 1)  # Normalize to 0-1
            quality_score += 0.3 * snr_quality
        
        weight_total += 0.3
        
    except:
        weight_total += 0.3
    
    # 3. Motion correlation (30% weight, if available)
    if acc_data is not None:
        try:
            acc_mag = calculate_accelerometer_magnitude(acc_data)
            
            # Resample accelerometer to match PPG
            if len(acc_mag) != len(ppg_signal):
                from scipy.interpolate import interp1d
                t_acc = np.linspace(0, len(acc_mag)/fs_acc, len(acc_mag))
                t_ppg = np.linspace(0, len(ppg_signal)/fs_ppg, len(ppg_signal))
                f_interp = interp1d(t_acc, acc_mag, kind='linear', fill_value='extrapolate')
                acc_mag = f_interp(t_ppg)
            
            # High motion = low quality
            motion_std = np.std(acc_mag)
            motion_quality = np.exp(-motion_std * 2)  # Exponential decay
            
            quality_score += 0.3 * motion_quality
            weight_total += 0.3
            
        except:
            weight_total += 0.3
    
    # Normalize by total weight
    if weight_total > 0:
        return quality_score / weight_total
    else:
        return 0.5  # Uncertain


def should_process_segment(quality_index, activity_intensity, threshold=0.5):
    """
    Decide whether to extract HRV from a segment
    
    Decision logic:
    - Stationary/Light motion: Use if quality > 0.4
    - Moderate motion: Use if quality > 0.6
    - Vigorous motion: Skip (quality unreliable)
    
    Parameters:
    -----------
    quality_index : float
        Signal quality (0-1)
    activity_intensity : int
        0=stationary, 1=light, 2=moderate, 3=vigorous
    threshold : float
        Base quality threshold
    
    Returns:
    --------
    bool : True if segment is processable
    """
    # Adjust threshold based on activity
    adjusted_threshold = threshold + (activity_intensity * 0.15)
    
    # Always skip vigorous motion
    if activity_intensity >= 3:
        return False
    
    return quality_index >= adjusted_threshold


# ========== MOTION-ROBUST PPG PROCESSING ==========

def adaptive_bandpass_filter(ppg_signal, fs, activity_intensity):
    """
    Apply activity-specific bandpass filter to PPG
    
    Frequencies of interest (Hz):
    - Stationary: 0.5-4 Hz (heart rate 30-240 bpm)
    - Light/Moderate: 0.7-3.5 Hz (narrow to reduce motion)
    - Vigorous: 1-3 Hz (very narrow, but still likely corrupted)
    
    Parameters:
    -----------
    ppg_signal : numpy array
    fs : int
        Sampling frequency
    activity_intensity : int
        0=stationary, 1=light, 2=moderate, 3=vigorous
    
    Returns:
    --------
    filtered_signal : numpy array
    """
    if activity_intensity == 0:
        lowcut, highcut = 0.5, 4.0
    elif activity_intensity == 1:
        lowcut, highcut = 0.7, 3.5
    elif activity_intensity == 2:
        lowcut, highcut = 0.8, 3.0
    else:  # vigorous
        lowcut, highcut = 1.0, 2.8
    
    # Design Butterworth filter
    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist
    
    b, a = butter(N=4, Wn=[low, high], btype='band')
    filtered = filtfilt(b, a, ppg_signal)
    
    return filtered


def detect_ppg_peaks_robust(ppg_signal, fs=64, activity_intensity=0):
    """
    Detect PPG peaks with activity-aware parameters
    
    Adjusts:
    - Minimum peak distance based on expected heart rate
    - Prominence threshold based on expected noise level
    
    Parameters:
    -----------
    ppg_signal : numpy array
    fs : int
    activity_intensity : int
        0=stationary, 1=light, 2=moderate, 3=vigorous
    
    Returns:
    --------
    peaks : numpy array of peak indices
    """
    # Adjust distance (min time between peaks)
    # More conservative during motion
    base_distance = int(0.4 * fs)  # Min 0.4s = 150 bpm max
    distance = base_distance + (activity_intensity * int(0.1 * fs))
    
    # Adjust prominence
    # Higher threshold during motion to reject artifacts
    base_prominence = 0.05
    prominence = base_prominence * (1 + activity_intensity * 0.5)
    
    peaks, _ = find_peaks(
        ppg_signal,
        distance=distance,
        prominence=prominence,
        height=np.percentile(ppg_signal, 20)  # Above 20th percentile
    )
    
    return peaks


# ========== FREQUENCY-DOMAIN HRV (MOTION-ROBUST) ==========

def calculate_hrv_frequency_features(rr_intervals, method='welch'):
    """
    Calculate frequency-domain HRV features
    
    These are MORE ROBUST to motion artifacts than time-domain SDNN/RMSSD
    because they capture oscillatory patterns that motion doesn't affect.
    
    Features:
    - VLF power: 0.003-0.04 Hz (long-term regulation)
    - LF power: 0.04-0.15 Hz (sympathetic + parasympathetic)
    - HF power: 0.15-0.4 Hz (parasympathetic, respiratory)
    - LF/HF ratio: Autonomic balance
    
    Parameters:
    -----------
    rr_intervals : numpy array
        RR intervals in milliseconds
    method : str
        'welch' or 'ar' (autoregressive)
    
    Returns:
    --------
    dict with frequency features (or None if insufficient data)
    """
    if len(rr_intervals) < 10:
        return None
    
    # Convert RR intervals to evenly sampled signal (4 Hz)
    # This is necessary for FFT
    rr_times = np.cumsum(rr_intervals) / 1000  # Convert to seconds
    rr_times = np.insert(rr_times, 0, 0)
    
    # Interpolate to 4 Hz
    fs_interp = 4
    t_interp = np.arange(0, rr_times[-1], 1/fs_interp)
    
    from scipy.interpolate import interp1d
    f_interp = interp1d(rr_times[:-1], rr_intervals, kind='cubic', fill_value='extrapolate')
    rr_interp = f_interp(t_interp)
    
    # Power spectral density
    freqs, psd = welch(rr_interp, fs=fs_interp, nperseg=min(256, len(rr_interp)))
    
    # Frequency band power
    vlf_band = (freqs >= 0.003) & (freqs < 0.04)
    lf_band = (freqs >= 0.04) & (freqs < 0.15)
    hf_band = (freqs >= 0.15) & (freqs < 0.4)
    
    vlf_power = np.trapz(psd[vlf_band], freqs[vlf_band])
    lf_power = np.trapz(psd[lf_band], freqs[lf_band])
    hf_power = np.trapz(psd[hf_band], freqs[hf_band])
    
    total_power = vlf_power + lf_power + hf_power
    
    features = {
        'vlf_power': vlf_power,
        'lf_power': lf_power,
        'hf_power': hf_power,
        'total_power': total_power,
        'lf_hf_ratio': lf_power / hf_power if hf_power > 0 else 0,
        'lf_norm': lf_power / (lf_power + hf_power) if (lf_power + hf_power) > 0 else 0,
        'hf_norm': hf_power / (lf_power + hf_power) if (lf_power + hf_power) > 0 else 0
    }
    
    return features


# ========== COMPLETE PIPELINE ==========

def extract_motion_robust_features(ppg_signal, acc_data, fs_ppg=64, fs_acc=32):
    """
    Complete pipeline: Motion detection → Quality check → Feature extraction
    
    This is the MAIN function for Phase 2.
    
    Parameters:
    -----------
    ppg_signal : numpy array
    acc_data : numpy array
        3-axis accelerometer
    fs_ppg : int
    fs_acc : int
    
    Returns:
    --------
    dict with features (or None if segment should be rejected)
    """
    # Step 1: Motion detection
    motion_features = extract_motion_features(acc_data, fs_acc)
    activity_name, activity_intensity = classify_activity_intensity(motion_features)
    
    # Step 2: Signal quality
    quality_index = calculate_signal_quality_index(ppg_signal, acc_data, fs_ppg, fs_acc)
    
    # Step 3: Decision - should we process?
    if not should_process_segment(quality_index, activity_intensity):
        return None  # Reject segment
    
    # Step 4: Adaptive filtering
    ppg_filtered = adaptive_bandpass_filter(ppg_signal, fs_ppg, activity_intensity)
    
    # Step 5: Peak detection
    peaks = detect_ppg_peaks_robust(ppg_filtered, fs_ppg, activity_intensity)
    
    if len(peaks) < 3:
        return None  # Not enough beats
    
    # Step 6: Feature extraction
    pp_intervals = np.diff(peaks) * (1000 / fs_ppg)  # Convert to ms
    
    # Time-domain HRV (from Phase 1 utils.py)
    time_features = {
        'mean_hr': 60000 / np.mean(pp_intervals),
        'sdnn': np.std(pp_intervals),
        'rmssd': np.sqrt(np.mean(np.diff(pp_intervals) ** 2)),
        'pnn50': (np.sum(np.abs(np.diff(pp_intervals)) > 50) / len(pp_intervals)) * 100,
    }
    
    # Frequency-domain HRV (motion-robust)
    freq_features = calculate_hrv_frequency_features(pp_intervals)
    
    # Combine all features
    features = {
        'activity': activity_name,
        'activity_intensity': activity_intensity,
        'signal_quality': quality_index,
        'num_beats': len(peaks),
        **motion_features,
        **time_features,
        **(freq_features if freq_features else {})
    }
    
    return features


# ========== UTILITY: BATCH PROCESSING ==========

def process_subject_file(ppg_signal, acc_data, fs_ppg=64, fs_acc=32, window_sec=30, overlap=0.5):
    """
    Process entire recording in sliding windows
    
    Parameters:
    -----------
    ppg_signal : numpy array
    acc_data : numpy array
    fs_ppg, fs_acc : int
    window_sec : int
        Window size in seconds
    overlap : float
        Overlap fraction (0-1)
    
    Returns:
    --------
    list of feature dicts (one per valid window)
    """
    window_samples_ppg = int(window_sec * fs_ppg)
    window_samples_acc = int(window_sec * fs_acc)
    
    step_ppg = int(window_samples_ppg * (1 - overlap))
    step_acc = int(window_samples_acc * (1 - overlap))
    
    results = []
    
    for start_ppg in range(0, len(ppg_signal) - window_samples_ppg, step_ppg):
        end_ppg = start_ppg + window_samples_ppg
        
        # Corresponding accelerometer window
        start_acc = int(start_ppg * fs_acc / fs_ppg)
        end_acc = start_acc + window_samples_acc
        
        if end_acc > len(acc_data):
            break
        
        ppg_window = ppg_signal[start_ppg:end_ppg]
        acc_window = acc_data[start_acc:end_acc]
        
        features = extract_motion_robust_features(ppg_window, acc_window, fs_ppg, fs_acc)
        
        if features is not None:
            features['window_start_sec'] = start_ppg / fs_ppg
            results.append(features)
    
    return results
