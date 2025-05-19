import tkinter as tk
import numpy as np
import time
import threading
from PIL import Image, ImageTk
import shader_config  # Config JSON for shader settings
import sounddevice as sd

class ShaderRenderer:
    def __init__(self, canvas, width, height, bpm=120):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.bpm = bpm
        self.running = False
        self.image = None
        self.fractal_settings = shader_config.load_shader_config()
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.render_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def render_loop(self):
        while self.running:
            self.render_fractal()
            time.sleep(1 / 30)  # Target 30 FPS

    def render_fractal(self):
        # Create an image for the fractal
        image = Image.new("RGB", (self.width, self.height))
        pixels = image.load()

        for y in range(self.height):
            for x in range(self.width):
                # Calculate fractal color (Mandelbulb-like)
                zx, zy = (x - self.width / 2) / (self.width / 4), (y - self.height / 2) / (self.height / 4)
                c = complex(zx, zy)
                color = self.calculate_color(c)
                pixels[x, y] = color

        self.image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def calculate_color(self, c):
        z = c
        max_iter = self.fractal_settings.get("depth", 50)
        color_shift = self.fractal_settings.get("color_shift", 0.01)
        for i in range(max_iter):
            z = z * z + c
            if abs(z) > 4.0:
                r = int(255 * (i / max_iter) * self.fractal_settings.get("primary_color_intensity", 1))
                g = int(255 * (i / max_iter) * self.fractal_settings.get("secondary_color_intensity", 1))
                b = int(255 * (1 - (i / max_iter)))
                return (r, g, b)
        
        # Default color for stable points
        return (0, 0, 0)

    def set_bpm(self, bpm):
        self.bpm = bpm

    def apply_shader_settings(self, new_settings):
        self.fractal_settings.update(new_settings)
        shader_config.save_shader_config(self.fractal_settings)
