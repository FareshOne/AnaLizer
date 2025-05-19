import json

SETTINGS_FILE = "settings.json"

# Load Settings
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return default_settings()

# Save Settings
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

# Default Settings
def default_settings():
    return {
        "theme": "dark",
        "shader_opacity": 0.8,
        "audio_threshold": 0.1,
        "midi_velocity": 100,
        "shader_type": "random",
        "bpm": 120
    }
