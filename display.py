import tkinter as tk
import numpy as np

def draw_waveform(canvas, audio, sr=44100):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    waveform = (audio / np.max(np.abs(audio))) * (height // 2)
    for x in range(1, width):
        try:
            y1 = height // 2 - waveform[int(len(waveform) * (x - 1) / width)]
            y2 = height // 2 - waveform[int(len(waveform) * x / width)]
            canvas.create_line(x - 1, y1, x, y2, fill="#00FF00")
        except:
            continue

def draw_midi(canvas, notes):
    canvas.delete("all")
    height = canvas.winfo_height()

    for note in notes:
        y = height - (note['note'] * 3)
        canvas.create_rectangle(note['start'] * 100, y, note['start'] * 100 + 10, y + 10, fill="#FFFFFF")
