import tkinter as tk
from tkinter import Canvas
import numpy as np

# Display Settings
display_settings = {
    "waveform_color": "#00FF00",  # Green
    "spectrum_color": "#FF0000",  # Red
    "slice_color": "#FFD700",     # Gold
    "background_color": "#1e1e1e" # Dark background
}

def draw_waveform(canvas, audio, sr, width, height):
    """
    Draws the audio waveform on the canvas.

    :param canvas: Tkinter canvas to draw on.
    :param audio: Audio waveform (numpy array).
    :param sr: Sample rate.
    :param width: Canvas width.
    :param height: Canvas height.
    """
    canvas.delete("all")  # Clear previous waveform

    # Normalize audio for display
    audio = audio / np.max(np.abs(audio))
    step = max(1, len(audio) // width)

    for x in range(width):
        i = int(x * step)
        y = int((1 - (audio[i] + 1) / 2) * height)
        canvas.create_line(x, height // 2, x, y, fill=display_settings["waveform_color"], width=1)

def draw_spectrum(canvas, audio, sr, width, height):
    """
    Draws the audio spectrum on the canvas.

    :param canvas: Tkinter canvas to draw on.
    :param audio: Audio waveform (numpy array).
    :param sr: Sample rate.
    :param width: Canvas width.
    :param height: Canvas height.
    """
    canvas.delete("spectrum")  # Clear spectrum only

    # FFT Spectrum
    spectrum = np.abs(np.fft.rfft(audio))
    spectrum = spectrum / np.max(spectrum)  # Normalize

    for x in range(width):
        freq = int((x / width) * (sr / 2))
        y = int((1 - spectrum[min(len(spectrum) - 1, int(len(spectrum) * (x / width)))]) * height)
        color = display_settings["spectrum_color"]
        canvas.create_line(x, height, x, y, fill=color, width=1, tags="spectrum")

def draw_midi(canvas, midi_notes, width, height):
    """
    Draws the MIDI notes (piano roll) on the canvas.

    :param canvas: Tkinter canvas to draw on.
    :param midi_notes: List of MIDI notes (dicts).
    :param width: Canvas width.
    :param height: Canvas height.
    """
    canvas.delete("all")  # Clear previous notes
    note_height = height // 88  # Piano roll (88 keys)

    for note in midi_notes:
        note_y = height - (note['note'] - 21) * note_height  # Note position
        note_x = int(note['start'] * width)
        note_width = int(note['duration'] * width)
        canvas.create_rectangle(
            note_x, note_y, 
            note_x + note_width, note_y + note_height, 
            fill="white", outline="black"
        )

def draw_slice_selection(canvas, start_x, end_x, height):
    """
    Draws a translucent selection area for audio slicing.

    :param canvas: Tkinter canvas to draw on.
    :param start_x: Starting X coordinate of the selection.
    :param end_x: Ending X coordinate of the selection.
    :param height: Canvas height.
    """
    canvas.create_rectangle(
        start_x, 0, end_x, height,
        fill=display_settings["slice_color"],
        stipple="gray25", outline=""
    )

def attach_slicing_controls(canvas, audio, sr, on_slice_update):
    """
    Adds slicing controls to the waveform canvas.

    :param canvas: Tkinter canvas.
    :param audio: Audio waveform.
    :param sr: Sample rate.
    :param on_slice_update: Function to call when slice is adjusted.
    """
    start_x = None
    end_x = None

    def start_slice(event):
        nonlocal start_x, end_x
        start_x = event.x
        end_x = start_x
        draw_slice_selection(canvas, start_x, end_x, canvas.winfo_height())

    def update_slice(event):
        nonlocal start_x, end_x
        if start_x is not None:
            end_x = event.x
            canvas.delete("slice")
            draw_slice_selection(canvas, start_x, end_x, canvas.winfo_height())
            on_slice_update(min(start_x, end_x), max(start_x, end_x))

    def end_slice(event):
        nonlocal start_x, end_x
        if start_x is not None and end_x is not None:
            canvas.delete("slice")
            draw_slice_selection(canvas, start_x, end_x, canvas.winfo_height())
            on_slice_update(min(start_x, end_x), max(start_x, end_x))
            start_x = None
            end_x = None

    canvas.bind("<Button-1>", start_slice)
    canvas.bind("<B1-Motion>", update_slice)
    canvas.bind("<ButtonRelease-1>", end_slice)
