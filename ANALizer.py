import tkinter as tk
from tkinter import ttk, filedialog
from analyzer import analyze_audio
from midi_processor import generate_midi
from utils import filter_notes
from display import draw_waveform, draw_spectrum, draw_midi
import numpy as np

current_midi_notes = []
audio_data = []
bpm = 120
zoom_level = 1.0
scroll_y = 0

# Filter Controls
velocity_threshold = 10
min_duration = 0.05
denoise_threshold = 0.01
low_cut = 20
high_cut = 20000
controls_visible = True
filtered_waveform = True

def toggle_controls():
    global controls_visible
    controls_visible = not controls_visible
    control_panel.pack_forget() if not controls_visible else control_panel.pack(side="left", fill="y")

def toggle_waveform():
    global filtered_waveform
    filtered_waveform = not filtered_waveform
    update_audio_analysis()

def process_audio():
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("WAV Files", "*.wav")])
    if not file_path:
        return

    global audio_data, current_midi_notes
    audio_data = analyze_audio(file_path)
    update_audio_analysis()
    update_midi_conversion()

def update_audio_analysis():
    audio_canvas.delete("all")
    if len(audio_data) > 0:
        audio, sr, _, spectrum = audio_data

        # Denoising
        audio = np.where(np.abs(audio) < denoise_threshold, 0, audio)
        
        # Band-Pass Filtering (applied to waveform)
        freqs = np.fft.rfftfreq(len(audio), 1 / sr)
        spectrum = np.fft.rfft(audio)
        if filtered_waveform:
            spectrum = np.where((freqs < low_cut) | (freqs > high_cut), 0, spectrum)
        filtered_audio = np.fft.irfft(spectrum)[:len(audio)]

        width = audio_canvas.winfo_width()
        height = audio_canvas.winfo_height()

        # Draw the appropriate waveform
        draw_waveform(audio_canvas, filtered_audio if filtered_waveform else audio, sr, width, height)
        draw_spectrum(audio_canvas, np.abs(spectrum), sr, width, height)

def update_midi_conversion():
    midi_canvas.delete("all")
    global current_midi_notes
    if len(audio_data) > 0:
        current_midi_notes = filter_notes(audio_data[2], velocity_threshold, min_duration)
    draw_midi(midi_canvas, current_midi_notes, midi_canvas.winfo_width(), midi_canvas.winfo_height(), zoom_level, scroll_y)

def adjust_denoise(value):
    global denoise_threshold
    denoise_threshold = float(value)
    update_audio_analysis()

def adjust_low_cut(value):
    global low_cut
    low_cut = int(value)
    update_audio_analysis()

def adjust_high_cut(value):
    global high_cut
    high_cut = int(value)
    update_audio_analysis()

def adjust_velocity(value):
    global velocity_threshold
    velocity_threshold = int(value)
    update_midi_conversion()

def adjust_duration(value):
    global min_duration
    min_duration = float(value)
    update_midi_conversion()

def set_bpm(value):
    global bpm
    bpm = int(value)

def quantize_bpm():
    update_midi_conversion()

def zoom_midi(value):
    global zoom_level
    zoom_level = float(value)
    update_midi_conversion()

def scroll_midi(event):
    global scroll_y
    scroll_y = max(-0.5, min(0.5, scroll_y - event.delta / 1000))
    update_midi_conversion()

# GUI Setup
root = tk.Tk()
root.title("ANALizer - Real-Time Audio to MIDI")
root.geometry("1000x600")
root.minsize(900, 500)

# Control Panel (Collapsible)
control_panel = tk.Frame(root, width=200, bg="#34495e")
control_panel.pack(side="left", fill="y")
toggle_button = tk.Button(root, text="☰ Controls", command=toggle_controls)
toggle_button.pack(side="left")

# AA Controls (Denoising + Band-Pass Filter)
aa_controls = tk.LabelFrame(control_panel, text="Audio Analysis Controls", bg="#34495e", fg="white")
aa_controls.pack(fill="x", pady=5)

tk.Button(aa_controls, text="Toggle Waveform (Filtered/Raw)", command=toggle_waveform).pack(fill="x")

tk.Label(aa_controls, text="Denoise Threshold").pack()
denoise_slider = tk.Scale(aa_controls, from_=0.001, to=0.1, resolution=0.001, orient="horizontal", command=adjust_denoise)
denoise_slider.set(0.01)
denoise_slider.pack(fill="x")

tk.Label(aa_controls, text="Low Cut (Hz)").pack()
low_cut_slider = tk.Scale(aa_controls, from_=20, to=1000, orient="horizontal", command=adjust_low_cut)
low_cut_slider.set(20)
low_cut_slider.pack(fill="x")

tk.Label(aa_controls, text="High Cut (Hz)").pack()
high_cut_slider = tk.Scale(aa_controls, from_=1000, to=20000, orient="horizontal", command=adjust_high_cut)
high_cut_slider.set(20000)
high_cut_slider.pack(fill="x")

# MIDI Conversion Controls (Tab 2)
midi_controls = tk.LabelFrame(control_panel, text="MIDI Controls", bg="#34495e", fg="white")
midi_controls.pack(fill="x", pady=5)

tk.Label(midi_controls, text="Velocity Threshold").pack()
velocity_slider = tk.Scale(midi_controls, from_=0, to=127, orient="horizontal", command=adjust_velocity)
velocity_slider.set(10)
velocity_slider.pack(fill="x")

tk.Label(midi_controls, text="Min Duration (s)").pack()
duration_slider = tk.Scale(midi_controls, from_=0.01, to=0.5, resolution=0.01, orient="horizontal", command=adjust_duration)
duration_slider.set(0.05)
duration_slider.pack(fill="x")

tk.Label(midi_controls, text="BPM").pack()
bpm_input = tk.Entry(midi_controls)
bpm_input.insert(0, "120")
bpm_input.pack(fill="x")
tk.Button(midi_controls, text="Quantize BPM", command=quantize_bpm).pack(fill="x")

# Tabs (AA + MIDI)
notebook = ttk.Notebook(root)
tab_audio = tk.Frame(notebook)
tab_midi = tk.Frame(notebook)
notebook.add(tab_audio, text="Audio Analysis")
notebook.add(tab_midi, text="MIDI Conversion")
notebook.pack(fill="both", expand=True, side="right")

# Audio Analysis Tab (AA Tab)
audio_canvas = tk.Canvas(tab_audio, width=800, height=250, bg="#2c3e50")
audio_canvas.pack(pady=5, fill="x")

tk.Button(tab_audio, text="Load Audio", command=process_audio, bg="#3498db", fg="#ffffff").pack()

# MIDI Conversion Tab (MIDI Tab)
midi_canvas = tk.Canvas(tab_midi, width=800, height=250, bg="#ffffff")
midi_canvas.pack(pady=5, fill="x")
midi_canvas.bind("<MouseWheel>", scroll_midi)

root.mainloop()
