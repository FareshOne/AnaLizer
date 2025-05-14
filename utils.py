def filter_notes(midi_notes, velocity_threshold=10, min_duration=0.05):
    """
    Filters notes by velocity and duration thresholds.
    """
    return [
        note for note in midi_notes 
        if note['velocity'] >= velocity_threshold and note['duration'] >= min_duration
    ]

def frequency_to_color(frequency, max_freq):
    """
    Returns a color gradient (Red to Blue) based on frequency.
    """
    ratio = min(max(frequency / max_freq, 0), 1)
    red = int(255 * (1 - ratio))
    blue = int(255 * ratio)
    return f"#{red:02x}00{blue:02x}"
