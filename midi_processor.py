import pygame.midi

# Initialize MIDI Playback (Pygame MIDI)
pygame.midi.init()
midi_out = pygame.midi.Output(0)

# Generate MIDI from Audio Function
def generate_midi():
    global current_midi_notes
    if not current_midi_notes:
        tk.messagebox.showerror("Error", "No MIDI notes available.")
        return

    save_path = filedialog.asksaveasfilename(
        title="Save MIDI File",
        defaultextension=".mid",
        filetypes=[("MIDI Files", "*.mid")]
    )

    if save_path:
        from midi_processor import generate_midi_file  # Import directly to avoid circular dependency
        generate_midi_file(current_midi_notes, save_path)

# MIDI Play and Stop Controls
def play_midi():
    if not current_midi_notes:
        tk.messagebox.showerror("Error", "No MIDI notes to play.")
        return

    for note in current_midi_notes:
        midi_out.note_on(note['note'], note.get('velocity', 100))
        root.after(int(note['duration'] * 1000), lambda: midi_out.note_off(note['note']))

def stop_midi():
    midi_out.close()
    pygame.midi.quit()
    pygame.midi.init()  # Reset MIDI state

# MIDI Play/Stop Buttons (MIDI Tab)
play_button = tk.Button(tab_midi, text="Play MIDI", command=play_midi, bg="#333333", fg="white")
play_button.pack(side="left", padx=5)

stop_button = tk.Button(tab_midi, text="Stop MIDI", command=stop_midi, bg="#333333", fg="white")
stop_button.pack(side="left", padx=5)

# Save MIDI Button (MIDI Tab)
save_midi_button = tk.Button(tab_midi, text="Save MIDI", command=generate_midi, bg="#333333", fg="white")
save_midi_button.pack(side="left", padx=5)
