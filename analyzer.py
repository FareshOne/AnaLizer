import numpy as np
import librosa

# Audio Analysis (Pitch, Amplitude, Denoising)
def analyze_audio(file_path, pitch_threshold=0.1, velocity_sensitivity=0.5, amplitude_threshold=0.1, legato=0.1):
    audio, sr = librosa.load(file_path, sr=None)
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)

    midi_notes = []

    for t in range(pitches.shape[1]):
        pitch_col = pitches[:, t]
        mag_col = magnitudes[:, t]

        if mag_col.max() > amplitude_threshold:
            pitch = pitch_col[mag_col.argmax()]
            if pitch > pitch_threshold:
                midi_notes.append(librosa.hz_to_midi(pitch))

    return audio, sr, midi_notes, np.array(magnitudes)

# Denoising Function
def denoise_audio(audio, sr, noise_threshold=0.01):
    return librosa.effects.preemphasis(audio, coef=noise_threshold)
