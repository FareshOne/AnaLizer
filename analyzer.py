import numpy as np
import librosa
from scipy.ndimage import median_filter

def analyze_audio(file_path, noise_reduction=True, harmonic_enhancement=False, low_cut=50, high_cut=15000, sr=44100):
    # Load Audio
    audio, sr = librosa.load(file_path, sr=sr)
    original_audio = np.copy(audio)

    # Noise Reduction (Adaptive)
    if noise_reduction:
        noise_profile = detect_noise_profile(audio)
        audio = audio - noise_profile
        audio = np.clip(audio, -1, 1)

    # Apply Band-Pass Filter
    audio = apply_bandpass_filter(audio, sr, low_cut, high_cut)

    # Harmonic Enhancement
    if harmonic_enhancement:
        audio = enhance_harmonics(audio, sr)

    # Spectrum Analysis
    spectrum = np.abs(np.fft.rfft(audio))
    spectrum = median_filter(spectrum, size=3)  # Smooth spectrum for better clarity

    # Pitch Detection
    pitches, magnitudes = librosa.piptrack(audio, sr=sr)
    detected_pitches = []
    for i in range(pitches.shape[1]):
        index = np.argmax(magnitudes[:, i])
        pitch = pitches[index, i]
        if pitch > 0:
            detected_pitches.append(pitch)

    return audio, spectrum, detected_pitches, original_audio

def detect_noise_profile(audio, noise_threshold=0.02):
    # Detect silent sections (assumed as noise)
    silent_mask = np.abs(audio) < noise_threshold
    noise_profile = np.mean(audio[silent_mask]) if np.any(silent_mask) else 0
    return noise_profile

def apply_bandpass_filter(audio, sr, low_cut, high_cut):
    fft_spectrum = np.fft.rfft(audio)
    frequencies = np.fft.rfftfreq(len(audio), 1 / sr)

    # Apply band-pass filter
    fft_spectrum[(frequencies < low_cut) | (frequencies > high_cut)] = 0
    filtered_audio = np.fft.irfft(fft_spectrum)
    return filtered_audio

def enhance_harmonics(audio, sr, harmonic_strength=1.5):
    # Perform a basic harmonic boost
    spectrum = np.fft.rfft(audio)
    frequencies = np.fft.rfftfreq(len(audio), 1 / sr)

    for i, freq in enumerate(frequencies):
        if freq > 0 and freq * 2 < len(spectrum):
            spectrum[i] += harmonic_strength * spectrum[i // 2]  # Boost harmonics

    enhanced_audio = np.fft.irfft(spectrum)
    return enhanced_audio
