import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "theme": {
        "mode": "dark",  # "dark" or "light"
        "waveform_color": "#FF5733",  # Default color for waveform (red)
        "spectrum_color": "#33C3FF",  # Default color for spectrum (blue)
        "piano_roll_color": "#FFFFFF",  # Default color for piano roll (white)
        "background_color": "#1E1E1E"  # Default background (dark)
    },
    "shader": {
        "enabled": True,
        "complexity": 5,       # Shader complexity (depth)
        "adaptive_color": True,  # Automatically adapts colors
        "animation_speed": 1.0,  # Default animation speed
        "reset_on_change": False  # Resets animation when settings change
    },
    "audio": {
        "noise_reduction": True,
        "harmonic_enhancement": False,
        "low_cut": 50,
        "high_cut": 15000
    },
    "midi": {
        "legato": False,  # Default mode (Normal)
        "bpm": 120,       # Default BPM
        "velocity_curve": "logarithmic"  # "linear" or "logarithmic"
    },
    "lock_settings": False  # Prevents accidental changes
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    else:
        return DEFAULT_SETTINGS

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

def reset_section(section):
    settings = load_settings()
    if section in DEFAULT_SETTINGS:
        settings[section] = DEFAULT_SETTINGS[section]
        save_settings(settings)
    return settings

def toggle_lock():
    settings = load_settings()
    settings["lock_settings"] = not settings.get("lock_settings", False)
    save_settings(settings)
    return settings["lock_settings"]

def reset_animation():
    settings = load_settings()
    if settings["shader"]["reset_on_change"]:
        settings["shader"]["complexity"] = DEFAULT_SETTINGS["shader"]["complexity"]
        save_settings(settings)
