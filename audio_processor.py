import numpy as np
import soundfile as sf
import librosa
import tkinter as tk

# Global Variables
current_audio = None
current_filtered_audio = None
current_selection = None

# Load Audio File
def load_audio():
    global current_audio, current_filtered_audio
    file_path = filedialog.askopenfilename()
    if file_path:
        current_audio, sr = librosa.load(file_path, sr=44100)
        current_filtered_audio = np.copy(current_audio)
        draw_waveform(audio_canvas, current_audio, sr)
        denoise_audio()

# Draw Waveform (AA Tab)
def draw_waveform(canvas, audio, sr):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    step = max(1, len(audio) // width)
    for i in range(0, len(audio), step):
        x = (i // step)
        y = int((audio[i] + 1) * (height // 2))
        color = "#00ff00"  # Green waveform
        canvas.create_line(x, height // 2, x, y, fill=color)

# Apply Denoising (Default On)
def denoise_audio():
    global current_filtered_audio
    if current_audio is None:
        return

    noise_profile = np.percentile(current_audio, 25)  # Noise threshold
    current_filtered_audio = np.where(np.abs(current_audio) > noise_profile, current_audio, 0)
    draw_waveform(audio_canvas, current_filtered_audio, 44100)

# Slicing Controls (Selection)
def start_selection(event):
    global current_selection
    current_selection = [event.x, event.x]

def update_selection(event):
    global current_selection
    if current_selection:
        current_selection[1] = event.x
        draw_waveform(audio_canvas, current_filtered_audio, 44100)
        audio_canvas.create_rectangle(current_selection[0], 0, current_selection[1], audio_canvas.winfo_height(), outline="#ff8800", width=2)

def end_selection(event):
    global current_selection
    if current_selection and current_selection[0] != current_selection[1]:
        crop_audio()
        current_selection = None

# Crop Audio (to Selection)
def crop_audio():
    global current_filtered_audio
    if not current_selection:
        return

    width = audio_canvas.winfo_width()
    start = int((current_selection[0] / width) * len(current_filtered_audio))
    end = int((current_selection[1] / width) * len(current_filtered_audio))
    current_filtered_audio = current_filtered_audio[start:end]
    draw_waveform(audio_canvas, current_filtered_audio, 44100)

# Export Filtered Audio
def export_filtered_audio():
    if current_filtered_audio is None:
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV file", "*.wav"), ("MP3 file", "*.mp3")])
    if file_path:
        sf.write(file_path, current_filtered_audio, 44100)

# UI - Audio Analysis Tab
audio_canvas = tk.Canvas(tab_audio, bg="#1e1e1e", highlightthickness=0)
audio_canvas.pack(fill=tk.BOTH, expand=True)
audio_canvas.bind("<Button-1>", start_selection)
audio_canvas.bind("<B1-Motion>", update_selection)
audio_canvas.bind("<ButtonRelease-1>", end_selection)

denoise_button = tk.Button(tab_audio, text="Denoise", command=denoise_audio, bg="#333333", fg="white")
denoise_button.pack(side="left", padx=5)

export_button = tk.Button(tab_audio, text="Export Filtered Audio", command=export_filtered_audio, bg="#333333", fg="white")
export_button.pack(side="left", padx=5)
