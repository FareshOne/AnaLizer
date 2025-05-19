import pretty_midi
import numpy as np

# MIDI Settings (Default)
midi_settings = {
    "velocity_threshold": 30,   # Minimum velocity for note detection
    "min_duration": 0.05,       # Minimum duration (seconds) for a note
    "legato_mode": False,       # Legato (note overlap) mode
    "bpm": 120                  # Default BPM
}

def generate_midi(notes, save_path, legato=False):
    """
    Generates a MIDI file from a list of notes.

    :param notes: List of dicts with 'note', 'start', 'duration', 'velocity'.
    :param save_path: Path to save the generated MIDI file.
    :param legato: If True, applies note overlap for legato.
    """
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    for note in notes:
        start = note['start']
        duration = note['duration']
        velocity = note['velocity']
        pitch = note['note']

        # Apply Legato if enabled
        if legato:
            duration += duration * 0.15  # 15% overlap for legato

        midi_note = pretty_midi.Note(
            velocity=int(velocity),
            pitch=int(pitch),
            start=start,
            end=start + duration
        )
        instrument.notes.append(midi_note)

    midi.instruments.append(instrument)
    midi.write(save_path)


def process_audio_to_midi(audio_data, sr, pitch_values, amplitude_values):
    """
    Converts audio analysis data to MIDI notes.

    :param audio_data: Audio waveform data (array).
    :param sr: Sample rate of the audio.
    :param pitch_values: Detected pitch values (Hz).
    :param amplitude_values: Detected amplitude values.
    :return: List of MIDI notes (note, velocity, start, duration).
    """
    midi_notes = []
    current_note = None
    start_time = 0

    for i, pitch in enumerate(pitch_values):
        if pitch > 0:  # Detected pitch
            midi_pitch = librosa.hz_to_midi(pitch)
            velocity = min(127, max(0, int(amplitude_values[i] * 127)))

            if velocity < midi_settings["velocity_threshold"]:
                continue

            if current_note is None:
                current_note = {
                    "note": midi_pitch,
                    "velocity": velocity,
                    "start": i / sr,
                    "duration": 0
                }
                start_time = i / sr
            else:
                current_note['duration'] = (i / sr) - start_time

        elif current_note:
            if current_note['duration'] >= midi_settings["min_duration"]:
                midi_notes.append(current_note)
            current_note = None

    # Finalize last note
    if current_note and current_note['duration'] >= midi_settings["min_duration"]:
        midi_notes.append(current_note)

    return midi_notes


def apply_legato(midi_notes):
    """
    Applies legato (overlap) to MIDI notes.

    :param midi_notes: List of MIDI notes (dict).
    """
    for i in range(1, len(midi_notes)):
        if midi_notes[i - 1]['note'] == midi_notes[i]['note']:
            midi_notes[i - 1]['duration'] *= 1.15  # 15% overlap

    return midi_notes


def filter_midi_notes(midi_notes):
    """
    Filters MIDI notes based on velocity and duration thresholds.

    :param midi_notes: List of MIDI notes (dict).
    :return: Filtered list of MIDI notes.
    """
    filtered_notes = [
        note for note in midi_notes
        if note['velocity'] >= midi_settings["velocity_threshold"]
        and note['duration'] >= midi_settings["min_duration"]
    ]
    return filtered_notes


def set_midi_bpm(bpm):
    """
    Sets the BPM for the generated MIDI file.

    :param bpm: Beats per minute.
    """
    midi_settings["bpm"] = bpm
