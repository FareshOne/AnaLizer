import numpy as np
from utils import frequency_to_color

def draw_waveform(canvas, audio, sr, width, height):
    """
    Draws the audio waveform with a vertically mirrored gradient (Red-Yellow-Green).
    """
    canvas.delete("all")
    step = max(1, len(audio) // width)
    max_amplitude = max(abs(audio)) if len(audio) > 0 else 1

    for i in range(width - 1):
        # Calculate waveform amplitude for vertical gradient
        amplitude = abs(audio[i * step]) / max_amplitude
        
        # Top Half Gradient (Red → Yellow → Green)
        if amplitude <= 0.5:
            red = int(255 * (1 - 2 * amplitude))
            green = int(255 * (2 * amplitude))
            blue = 0
        # Bottom Half Gradient (Green → Yellow → Red)
        else:
            amplitude = amplitude - 0.5
            red = int(255 * (2 * amplitude))
            green = int(255 * (1 - 2 * amplitude))
            blue = 0

        color = f"#{red:02x}{green:02x}{blue:02x}"

        # Draw the waveform
        y1 = height // 2 - int((audio[i * step] / max_amplitude) * (height // 2))
        y2 = height // 2 - int((audio[(i + 1) * step] / max_amplitude) * (height // 2))
        canvas.create_line(i, y1, i + 1, y2, fill=color, width=1)

def draw_spectrum(canvas, spectrum, sr, width, height):
    """
    Draws the frequency spectrum on the given canvas.
    """
    for i in range(width - 1):
        spectrum_value = spectrum[i] if i < len(spectrum) else 0
        color = frequency_to_color(i * sr / (2 * width), sr // 2)
        canvas.create_line(
            i, height, i, height - int(spectrum_value * height // 2), 
            fill=color, width=1
        )

def draw_midi(canvas, midi_notes, width, height):
    """
    Draws MIDI notes on the given canvas (Piano Roll Style).
    """
    canvas.delete("all")
    if len(midi_notes) == 0:
        return

    note_height = height // 88  # 88 Piano Keys (A0 to C8)
    for note in midi_notes:
        x = int(note['start_time'] * 500)
        y = height - ((note['pitch'] - 21) * note_height)
        velocity = min(max(note['velocity'], 0), 127)
        color = f"#{int(0):02x}{int(200 - velocity):02x}{int(50 + velocity):02x}"
        canvas.create_rectangle(
            x, y, x + int(note['duration'] * 500), y + note_height, fill=color, outline="#333333"
        )
