import librosa
import numpy as np

def analyze_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    midi_notes = []

    # Note Detection
    for frame in range(pitches.shape[1]):
        pitch_values = pitches[:, frame]
        magnitudes_values = magnitudes[:, frame]

        for i, pitch in enumerate(pitch_values):
            if pitch > 0 and magnitudes_values[i] > 0.05:
                midi_notes.append({
                    'pitch': int(librosa.hz_to_midi(pitch)),
                    'velocity': int(min(max(magnitudes_values[i] * 127, 0), 127)),
                    'start_time': frame / sr,
                    'duration': 0.1  # Default (will be adjusted later)
                })

    # Generate Clean Spectrum (FFT)
    spectrum = np.abs(np.fft.fft(y))[:len(y) // 2]
    spectrum = np.interp(spectrum, (spectrum.min(), spectrum.max()), (0, 100))

    return y, sr, midi_notes, spectrum
