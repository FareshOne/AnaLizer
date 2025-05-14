
import soundfile as sf
import librosa
import matplotlib.pyplot as plt
import pretty_midi

def analyze_audio(file_path, pitch_threshold=50, velocity_sensitivity=127, amplitude_threshold=0.01, legato=0):
    audio, sr = sf.read(file_path)
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    pitches, _ = librosa.piptrack(y=audio, sr=sr)
    midi_notes = [int(librosa.hz_to_midi(p)) for p in pitches if p > pitch_threshold]
    return audio, sr, midi_notes

def render_analysis(audio, sr, midi_notes):
    plt.figure()
    plt.plot(audio, color="gray")
    plt.scatter(range(len(midi_notes)), midi_notes, color="orange")
    plt.show()

def generate_midi(midi_notes, output_file):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=73)
    time = 0
    for note in midi_notes:
        midi_note = pretty_midi.Note(velocity=80, pitch=note, start=time, end=time + 0.2)
        instrument.notes.append(midi_note)
        time += 0.2
    midi.instruments.append(instrument)
    midi.write(output_file)
