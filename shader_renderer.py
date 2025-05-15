import pygame
from pygame.locals import *
import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders
import numpy as np
import time
import threading

class ShaderRenderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.running = False
        self.shader_program = None
        self.start_time = time.time()
        self.bpm = 120
        self.pitch_intensity = 1.0
        self.speed_multiplier = 1.0
        self.transparency = 1.0
        self.resolution = (800, 600)
        self.use_vignette = True
        self.use_lut = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()

    def setup_shader(self):
        vertex_shader_code = """
        #version 330 core
        in vec2 position;
        void main() {
            gl_Position = vec4(position, 0.0, 1.0);
        }
        """
        fragment_shader_code = """
        #version 330 core
        out vec4 fragColor;
        uniform float time;
        uniform float bpm;
        uniform float pitchIntensity;
        uniform float transparency;
        uniform vec2 resolution;
        uniform bool use_vignette;
        uniform bool use_lut;

        vec3 fractal(vec2 uv) {
            float intensity = 0.5 + 0.5 * sin(time * bpm * 0.1);
            vec3 color = vec3(0.0);
            float scale = 3.0;
            uv -= 0.5;
            uv *= scale;
            for (int i = 0; i < 10; i++) {
                uv = abs(uv) / dot(uv, uv) - 1.0;
                color += vec3(0.5, 0.3, 0.2) * intensity;
            }
            return color;
        }

        void main() {
            vec2 uv = gl_FragCoord.xy / resolution;
            vec3 color = fractal(uv);

            if (use_vignette) {
                float dist = length(uv - vec2(0.5));
                color *= smoothstep(1.0, 0.0, dist);
            }

            if (use_lut) {
                color = pow(color, vec3(0.6, 0.7, 0.8));
            }

            fragColor = vec4(color * pitchIntensity, transparency);
        }
        """
        vertex_shader = shaders.compileShader(vertex_shader_code, gl.GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(fragment_shader_code, gl.GL_FRAGMENT_SHADER)
        self.shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

    def run(self):
        pygame.init()
        pygame.display.set_mode(self.resolution, DOUBLEBUF | OPENGL)
        self.setup_shader()
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            gl.glUseProgram(self.shader_program)

            time_passed = time.time() - self.start_time
            gl.glUniform1f(gl.glGetUniformLocation(self.shader_program, "time"), time_passed * self.speed_multiplier)
            gl.glUniform1f(gl.glGetUniformLocation(self.shader_program, "bpm"), self.bpm / 60.0)
            gl.glUniform1f(gl.glGetUniformLocation(self.shader_program, "pitchIntensity"), self.pitch_intensity)
            gl.glUniform1f(gl.glGetUniformLocation(self.shader_program, "transparency"), self.transparency)
            gl.glUniform2f(gl.glGetUniformLocation(self.shader_program, "resolution"), *self.resolution)
            gl.glUniform1i(gl.glGetUniformLocation(self.shader_program, "use_vignette"), int(self.use_vignette))
            gl.glUniform1i(gl.glGetUniformLocation(self.shader_program, "use_lut"), int(self.use_lut))

            gl.glBegin(gl.GL_QUADS)
            gl.glVertex2f(-1, -1)
            gl.glVertex2f(1, -1)
            gl.glVertex2f(1, 1)
            gl.glVertex2f(-1, 1)
            gl.glEnd()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def set_bpm(self, bpm):
        self.bpm = bpm

    def set_pitch_intensity(self, intensity):
        self.pitch_intensity = intensity

    def set_speed_multiplier(self, speed):
        self.speed_multiplier = speed

    def set_transparency(self, alpha):
        self.transparency = alpha

    def set_resolution(self, width, height):
        self.resolution = (width, height)

    def toggle_vignette(self, state):
        self.use_vignette = state

    def toggle_lut(self, state):
        self.use_lut = state
