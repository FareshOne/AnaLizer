# Advanced MIDI Sequencer (Piano Roll)
def update_midi_display():
    midi_canvas.delete("all")
    if not current_midi_notes:
        return

    width = midi_canvas.winfo_width()
    height = midi_canvas.winfo_height()
    note_height = 10  # Height of each note block

    # Draw MIDI Notes on Piano Roll
    for note in current_midi_notes:
        x = note['start'] * width
        y = height - ((note['note'] - 21) / 88) * height  # MIDI range (21 - 108)
        note_length = note['duration'] * width
        velocity = note.get('velocity', 100)

        color = f"#{int(255 * (velocity / 127)):02x}00{int(255 * (1 - (velocity / 127))):02x}"  # Red-Green gradient
        midi_canvas.create_rectangle(x, y, x + note_length, y + note_height, fill=color, outline="white")

# Velocity and Duration Adjustments (Sliders)
def adjust_velocity(value):
    for note in current_midi_notes:
        note['velocity'] = int(value)
    update_midi_display()

def adjust_duration(value):
    for note in current_midi_notes:
        note['duration'] = float(value)
    update_midi_display()

# Velocity and Duration Sliders (MIDI Tab)
velocity_slider = tk.Scale(tab_midi, from_=0, to=127, orient="horizontal", label="Velocity", command=adjust_velocity)
velocity_slider.pack(fill="x", padx=10)

duration_slider = tk.Scale(tab_midi, from_=0.1, to=5.0, resolution=0.1, orient="horizontal", label="Duration (s)", command=adjust_duration)
duration_slider.pack(fill="x", padx=10)

# Legato Mode Toggle (Checkbox)
legato_var = tk.BooleanVar()
def toggle_legato():
    if legato_var.get():
        apply_legato()

def apply_legato():
    if not current_midi_notes:
        return

    for i in range(1, len(current_midi_notes)):
        previous_note = current_midi_notes[i - 1]
        current_note = current_midi_notes[i]

        # Apply overlap (15% of note duration)
        overlap = previous_note['duration'] * 0.15
        current_note['start'] = max(current_note['start'], previous_note['start'] + previous_note['duration'] - overlap)

    update_midi_display()

legato_checkbox = tk.Checkbutton(tab_midi, text="Legato Mode", variable=legato_var, command=toggle_legato)
legato_checkbox.pack(side="left", padx=5)

# Quantize Button (Align Notes)
def quantize_notes():
    if not current_midi_notes:
        return

    for note in current_midi_notes:
        note['start'] = round(note['start'] * 4) / 4  # Quantize to nearest 1/4 beat

    update_midi_display()

quantize_button = tk.Button(tab_midi, text="Quantize", command=quantize_notes, bg="#333333", fg="white")
quantize_button.pack(side="left", padx=5)
