import tkinter as tk
import numpy as np
from tkinter import colorchooser
import math
import time

shader_canvas = None
shader_running = False
shader_params = {
    "fractal_type": "mandelbulb",  # mandelbulb, julia, koch
    "depth": 4,
    "primary_color": "#ff0000",  # Red
    "secondary_color": "#0000ff",  # Blue
    "animation_speed": 1.0,
    "audio_reactive": True,
    "color_shift": True
}

def start_shader_renderer(canvas):
    global shader_canvas, shader_running
    shader_canvas = canvas
    shader_running = True
    animate_shader()

def stop_shader_renderer():
    global shader_running
    shader_running = False

def animate_shader():
    global shader_canvas, shader_running
    if not shader_running:
        return

    width = shader_canvas.winfo_width()
    height = shader_canvas.winfo_height()
    shader_canvas.delete("all")

    # Fractal Parameters
    depth = shader_params["depth"]
    primary = shader_params["primary_color"]
    secondary = shader_params["secondary_color"]

    # Animation Time
    t = time.time() * shader_params["animation_speed"]

    for y in range(0, height, 2):  # Skipping 2 pixels for performance
        for x in range(0, width, 2):
            # Mandelbulb Pattern (adjustable)
            zx = 1.5 * (x - width / 2) / (0.5 * width)
            zy = 1.0 * (y - height / 2) / (0.5 * height)
            c = complex(zx, zy)
            z = c
            color_factor = 0

            for i in range(depth):
                z = z ** 2 + c
                if abs(z) > 2:
                    color_factor = i / depth
                    break

            # Color Calculation (Primary to Secondary Gradient)
            if shader_params["color_shift"]:
                red = int(int(primary[1:3], 16) * (1 - color_factor) + int(secondary[1:3], 16) * color_factor)
                green = int(int(primary[3:5], 16) * (1 - color_factor) + int(secondary[3:5], 16) * color_factor)
                blue = int(int(primary[5:7], 16) * (1 - color_factor) + int(secondary[5:7], 16) * color_factor)
                color = f'#{red:02x}{green:02x}{blue:02x}'
            else:
                color = primary

            # Adjust for Audio Reactivity (Wave Effect)
            if shader_params["audio_reactive"]:
                wave = math.sin(t + (x / width) * 6.28) * 20  # Sine wave effect
                y_pos = y + int(wave)
            else:
                y_pos = y

            shader_canvas.create_rectangle(x, y_pos, x + 2, y_pos + 2, outline=color, fill=color)

    shader_canvas.after(16, animate_shader)  # ~60 FPS

# UI for Shader Settings (Settings Tab)
def open_shader_settings():
    settings_window = tk.Toplevel()
    settings_window.title("Shader Settings")

    tk.Label(settings_window, text="Fractal Type:").pack()
    fractal_var = tk.StringVar(value=shader_params["fractal_type"])
    tk.OptionMenu(settings_window, fractal_var, "mandelbulb", "julia", "koch").pack()

    def save_shader_settings():
        shader_params["fractal_type"] = fractal_var.get()
        shader_params["primary_color"] = color_1.get()
        shader_params["secondary_color"] = color_2.get()
        shader_params["depth"] = depth_slider.get()
        shader_params["animation_speed"] = speed_slider.get()
        shader_params["audio_reactive"] = audio_checkbox_var.get()
        shader_params["color_shift"] = color_shift_var.get()
        settings_window.destroy()

    # Color Pickers
    tk.Label(settings_window, text="Primary Color:").pack()
    color_1 = tk.StringVar(value=shader_params["primary_color"])
    tk.Entry(settings_window, textvariable=color_1).pack()

    tk.Label(settings_window, text="Secondary Color:").pack()
    color_2 = tk.StringVar(value=shader_params["secondary_color"])
    tk.Entry(settings_window, textvariable=color_2).pack()

    # Depth Slider
    tk.Label(settings_window, text="Fractal Depth:").pack()
    depth_slider = tk.Scale(settings_window, from_=1, to=8, orient="horizontal")
    depth_slider.set(shader_params["depth"])
    depth_slider.pack()

    # Animation Speed
    tk.Label(settings_window, text="Animation Speed:").pack()
    speed_slider = tk.Scale(settings_window, from_=0.1, to=5.0, resolution=0.1, orient="horizontal")
    speed_slider.set(shader_params["animation_speed"])
    speed_slider.pack()

    # Audio Reactivity Checkbox
    audio_checkbox_var = tk.BooleanVar(value=shader_params["audio_reactive"])
    tk.Checkbutton(settings_window, text="Audio Reactive", variable=audio_checkbox_var).pack()

    # Color Shift Checkbox
    color_shift_var = tk.BooleanVar(value=shader_params["color_shift"])
    tk.Checkbutton(settings_window, text="Color Shift", variable=color_shift_var).pack()

    # Save Button
    save_button = tk.Button(settings_window, text="Save Settings", command=save_shader_settings)
    save_button.pack(pady=5)

