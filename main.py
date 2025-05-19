import tkinter as tk
from tkinter import ttk, filedialog
from settings import load_settings, save_settings
from display import draw_waveform, draw_midi
from shader_renderer import start_shader_renderer
from audio_processor import analyze_audio
from midi_processor import generate_midi

# Initialize Main Window
root = tk.Tk()
root.title("ANALizer")
root.geometry("1200x800")
root.configure(bg="#1e1e1e")

# Shader Canvas (Background)
shader_canvas = tk.Canvas(root, bg="#000000", highlightthickness=0)
shader_canvas.pack(fill=tk.BOTH, expand=True)
shader_canvas.lower()
start_shader_renderer(shader_canvas)

# Tab Control
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Tabs Setup
tab_audio = tk.Frame(notebook, bg="#1e1e1e")
tab_midi = tk.Frame(notebook, bg="#1e1e1e")
tab_settings = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tab_audio, text="Audio Analysis")
notebook.add(tab_midi, text="MIDI Keys [Piano Roll]")
notebook.add(tab_settings, text="Settings")

# Audio Canvas (Tab 1)
audio_canvas = tk.Canvas(tab_audio, bg="#2e2e2e", highlightthickness=0)
audio_canvas.pack(fill=tk.BOTH, expand=True)

# MIDI Canvas (Tab 2)
midi_canvas = tk.Canvas(tab_midi, bg="#2e2e2e", highlightthickness=0)
midi_canvas.pack(fill=tk.BOTH, expand=True)

# Settings (Tab 3)
settings_label = tk.Label(tab_settings, text="Settings", bg="#1e1e1e", fg="white", font=("Arial", 14))
settings_label.pack(pady=10)

# Global State Variables
current_audio = None
current_midi_notes = []

root.mainloop()
