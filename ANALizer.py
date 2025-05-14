
import tkinter as tk
from tkinter import filedialog, messagebox
from analyzer import analyze_audio, generate_midi, render_analysis
import os

current_midi_notes = []

def process_audio():
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("WAV Files", "*.wav")])
    if not file_path:
        return

    audio_data = analyze_audio(file_path, pitch_threshold.get(), velocity_sensitivity.get(), amplitude_threshold.get(), legato.get())
    render_analysis(*audio_data)
    global current_midi_notes
    current_midi_notes = audio_data[1]

    save_path = os.path.join(os.path.dirname(file_path), "output_flute_midi.mid")
    generate_midi(current_midi_notes, save_path)

root = tk.Tk()
root.title("ANALizer - Real-Time Audio to MIDI")
root.geometry("450x300")

tk.Label(root, text="ANALizer - Real-Time Audio to MIDI", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Select Audio File", command=process_audio).pack(pady=5)

pitch_threshold = tk.Scale(root, from_=20, to=2000, orient="horizontal", label="Pitch Threshold (Hz)")
pitch_threshold.set(50)
pitch_threshold.pack()

velocity_sensitivity = tk.Scale(root, from_=0, to=127, orient="horizontal", label="Velocity Sensitivity")
velocity_sensitivity.set(100)
velocity_sensitivity.pack()

amplitude_threshold = tk.Scale(root, from_=0, to=1, orient="horizontal", label="Amplitude Threshold")
amplitude_threshold.set(0.01)
amplitude_threshold.pack()

legato = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Legato (%)")
legato.set(0)
legato.pack()

root.mainloop()
