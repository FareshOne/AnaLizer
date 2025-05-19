# Main Application Code
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from audio_processor import analyze_audio
from display import draw_waveform, draw_midi
from shader_renderer import start_shader_renderer
from midi_processor import generate_midi
from settings import load_settings, save_settings

root = tk.Tk()
root.title("ANALizer")
root.geometry("1200x700")

# Start Shader Background
shader_canvas = tk.Canvas(root, bg="#000000")
shader_canvas.pack(fill=tk.BOTH, expand=True)
shader_canvas.lower()  # Send shader to background
start_shader_renderer(shader_canvas)

# Tab Control
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Tab 1: Audio Analysis
tab_audio = tk.Frame(notebook)
audio_canvas = tk.Canvas(tab_audio, bg="#1e1e1e", highlightthickness=0)
audio_canvas.pack(fill=tk.BOTH, expand=True)
notebook.add(tab_audio, text="Audio Analysis")

# Tab 2: MIDI Keys (Piano Roll)
tab_midi = tk.Frame(notebook)
midi_canvas = tk.Canvas(tab_midi, bg="#1e1e1e", highlightthickness=0)
midi_canvas.pack(fill=tk.BOTH, expand=True)
notebook.add(tab_midi, text="MIDI Keys [Piano Roll]")

# Tab 3: Settings
tab_settings = tk.Frame(notebook)
notebook.add(tab_settings, text="Settings")

current_audio = None
current_midi_notes = []

# Load Audio File
def load_audio():
    global current_audio, current_midi_notes
    file_path = filedialog.askopenfilename()
    if file_path:
        audio, _, midi_notes, _ = analyze_audio(file_path)
        current_audio = audio
        current_midi_notes = [{'note': int(note), 'start': i / 100, 'duration': 0.1} for i, note in enumerate(midi_notes)]

        draw_waveform(audio_canvas, audio, 44100, 900, 400)
        draw_midi(midi_canvas, current_midi_notes, 900, 400)

# Load Button
load_button = tk.Button(root, text="Load Audio", command=load_audio)
load_button.pack(pady=5)

root.mainloop()
