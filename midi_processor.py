import pretty_midi
import numpy as np

def generate_midi(notes, save_path, mode="normal"):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=73)  # Flute default

    for note in notes:
        start = note["start"]
        duration = note["duration"]

        if mode == "legato":
            duration += duration * 0.15  # 15% overlap for Legato

        velocity = calculate_velocity(note["amplitude"])
        midi_note = pretty_midi.Note(
            velocity=velocity,
            pitch=note["pitch"],
            start=start,
            end=start + duration
        )
        instrument.notes.append(midi_note)

    midi.instruments.append(instrument)
    midi.write(save_path)

def process_pitches_to_midi(pitches, amplitudes, sr, min_duration=0.05):
    notes = []
    current_note = None

    for i, pitch in enumerate(pitches):
        if pitch > 0:
            if current_note is None:
                current_note = {
                    "pitch": int(librosa.hz_to_midi(pitch)),
                    "start": i / sr,
                    "amplitude": amplitudes[i],
                    "duration": 0
                }
            else:
                current_note["duration"] += 1 / sr
                current_note["amplitude"] = max(current_note["amplitude"], amplitudes[i])
        else:
            if current_note and current_note["duration"] >= min_duration:
                notes.append(current_note)
            current_note = None

    if current_note and current_note["duration"] >= min_duration:
        notes.append(current_note)

    return notes

def calculate_velocity(amplitude):
    # Logarithmic velocity scaling
    scaled_amplitude = max(0.001, amplitude)  # Prevent log(0)
    velocity = int(np.clip(127 * np.log10(scaled_amplitude + 1), 0, 127))
    return velocity
