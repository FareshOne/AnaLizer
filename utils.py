import os

# Utility: Ensure Directory Exists
def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Utility: Clamp Value (Range)
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

# Utility: Map Value (Range)
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
