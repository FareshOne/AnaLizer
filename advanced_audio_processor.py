import librosa
import numpy as np
import sounddevice as sd
from scipy.ndimage import median_filter

# Audio Settings (Default)
audio_settings = {
    "noise_reduction": True,
    "denoise_strength": 0.5,       # Denoising strength (0 = none, 1 = full)
    "low_cut": 20,                 # Low cut filter (Hz)
    "high_cut": 20000,             # High cut filter (Hz)
    "slice_fade": 0.01,            # Fade in/out duration for sliced audio
    "real_time_denoising": False   # Realtime denoising (requires fast CPU)
}

def load_audio(file_path):
    """
    Loads audio file and applies noise reduction (optional).
    """
    audio, sr = librosa.load(file_path, sr=None)
    if audio_settings["noise_reduction"]:
        audio = denoise_audio(audio, sr)
    return audio, sr

def denoise_audio(audio, sr):
    """
    Applies denoising (median filtering) to audio.

    :param audio: Audio waveform (array).
    :param sr: Sample rate of the audio.
    :return: Denoised audio waveform.
    """
    if not audio_settings["noise_reduction"]:
        return audio
    
    # Apply median filter for noise reduction
    filtered_audio = median_filter(audio, size=int(audio_settings["denoise_strength"] * sr))
    return filtered_audio

def apply_filters(audio, sr):
    """
    Applies high and low cut filters to the audio.

    :param audio: Audio waveform (array).
    :param sr: Sample rate.
    :return: Filtered audio.
    """
    # Fourier Transform
    spectrum = np.fft.rfft(audio)
    freqs = np.fft.rfftfreq(len(audio), 1 / sr)

    # Apply bandpass filter
    spectrum[(freqs < audio_settings["low_cut"]) | (freqs > audio_settings["high_cut"])] = 0

    # Inverse Fourier Transform
    filtered_audio = np.fft.irfft(spectrum)
    return filtered_audio

def real_time_denoising_callback(indata, frames, time, status):
    """
    Callback function for real-time denoising (if enabled).
    """
    if audio_settings["real_time_denoising"]:
        return denoise_audio(indata[:, 0], sr)

def record_audio(duration=5, sr=44100):
    """
    Records audio using sounddevice (WASAPI or default device).

    :param duration: Duration in seconds.
    :param sr: Sample rate.
    :return: Recorded audio waveform.
    """
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()
    
    if audio_settings["noise_reduction"]:
        audio = denoise_audio(audio.flatten(), sr)
    
    return audio.flatten(), sr

def slice_audio(audio, sr, start_time, end_time):
    """
    Slices a section of the audio and applies fade in/out.

    :param audio: Audio waveform (array).
    :param sr: Sample rate.
    :param start_time: Start time (seconds).
    :param end_time: End time (seconds).
    :return: Sliced audio waveform.
    """
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)
    
    sliced_audio = audio[start_sample:end_sample]
    
    # Apply fade in/out
    fade_len = int(sr * audio_settings["slice_fade"])
    sliced_audio[:fade_len] *= np.linspace(0, 1, fade_len)
    sliced_audio[-fade_len:] *= np.linspace(1, 0, fade_len)
    
    return sliced_audio

def play_audio(audio, sr):
    """
    Plays the audio using sounddevice.
    """
    sd.play(audio, samplerate=sr)
    sd.wait()

def export_audio(audio, sr, file_path):
    """
    Exports audio to WAV file.
    """
    librosa.output.write_wav(file_path, audio, sr)

def set_audio_settings(noise_reduction=None, denoise_strength=None, low_cut=None, high_cut=None):
    """
    Sets the audio processing settings.

    :param noise_reduction: Enable/disable noise reduction.
    :param denoise_strength: Strength of denoising (0-1).
    :param low_cut: Low cut filter frequency.
    :param high_cut: High cut filter frequency.
    """
    if noise_reduction is not None:
        audio_settings["noise_reduction"] = noise_reduction
    if denoise_strength is not None:
        audio_settings["denoise_strength"] = denoise_strength
    if low_cut is not None:
        audio_settings["low_cut"] = low_cut
    if high_cut is not None:
        audio_settings["high_cut"] = high_cut

