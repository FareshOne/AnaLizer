import tkinter as tk
from tkinter import Canvas
import numpy as np

def draw_waveform(canvas, audio, sr, width, height, theme):
    canvas.delete("all")
    waveform = audio / np.max(np.abs(audio))  # Normalize

    step = max(1, len(waveform) // width)
    half_height = height // 2

    for i in range(width - 1):
        index = i * step
        y1 = half_height - int(waveform[index] * half_height)
        y2 = half_height - int(waveform[min(index + step, len(waveform) - 1)] * half_height)
        
        freq_color = theme["waveform_color"]
        canvas.create_line(i, y1, i + 1, y2, fill=freq_color, width=1)

def draw_spectrum(canvas, spectrum, sr, width, height, theme):
    canvas.delete("spectrum")
    max_amp = np.max(spectrum)
    
    for i in range(width):
        frequency = i * (sr / 2) / width
        amplitude = spectrum[i] / max_amp
        height_bar = int(amplitude * height)
        color = calculate_color(frequency, theme)
        canvas.create_line(i, height, i, height - height_bar, fill=color, tags="spectrum")

def draw_velocity_curve(canvas, velocities, width, height, theme):
    canvas.delete("velocity_curve")
    max_velocity = max(velocities) if velocities else 1

    for i in range(len(velocities) - 1):
        x1 = int((i / len(velocities)) * width)
        y1 = height - int((velocities[i] / max_velocity) * height)
        x2 = int(((i + 1) / len(velocities)) * width)
        y2 = height - int((velocities[i + 1] / max_velocity) * height)

        canvas.create_line(x1, y1, x2, y2, fill=theme["velocity_curve_color"], width=2, tags="velocity_curve")

def draw_piano_roll(canvas, notes, width, height, zoom_level, scroll_y, theme, cursor_position=None):
    canvas.delete("all")
    note_height = 10
    total_keys = 88
    key_height = height // total_keys
    visible_notes = [note for note in notes if scroll_y <= note['pitch'] < scroll_y + total_keys]
    
    # Draw grid lines
    for i in range(total_keys):
        y = height - (i * key_height)
        canvas.create_line(0, y, width, y, fill=theme["grid_color"])

    # Draw notes
    for note in visible_notes:
        y = height - ((note['pitch'] - scroll_y) * key_height)
        x = int(note['start'] * zoom_level)
        note_width = max(int(note['duration'] * zoom_level), 1)
        
        canvas.create_rectangle(
            x, y - key_height, x + note_width, y,
            fill=theme["note_color"], outline=theme["note_border_color"]
        )

    # Draw velocity curve below notes
    velocities = [note['velocity'] for note in visible_notes]
    draw_velocity_curve(canvas, velocities, width, int(height * 0.2), theme)

    # Draw cursor if active
    if cursor_position is not None:
        cursor_x = int(cursor_position * zoom_level)
        canvas.create_line(cursor_x, 0, cursor_x, height, fill=theme["cursor_color"], width=2)

def calculate_color(frequency, theme):
    low, mid, high = theme["gradient_low"], theme["gradient_mid"], theme["gradient_high"]
    if frequency < 200:
        return low
    elif frequency < 2000:
        return mid
    else:
        return high

def apply_theme(canvas, theme):
    canvas.configure(bg=theme["background_color"])
