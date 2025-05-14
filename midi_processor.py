import pretty_midi

def generate_midi(midi_notes, save_path, mode="normal"):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)
    
    for note in midi_notes:
        end_time = note['start_time'] + note['duration']
        if mode == "legato":
            end_time += 0.05  # Slight overlap for legato effect

        instrument.notes.append(pretty_midi.Note(
            velocity=note['velocity'],
            pitch=note['pitch'],
            start=note['start_time'],
            end=end_time
        ))

    midi.instruments.append(instrument)
    midi.write(save_path)
