import librosa
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from enum import Enum

class Analyser:
    def __init__(self, timeSeries, sampleRate):
        hopLength=512
        nFft=2048*4
        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = np.abs(librosa.stft(timeSeries, hop_length=hopLength, n_fft=nFft))
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix
        frequencies = librosa.core.fft_frequencies(nFft)  # getting an array of frequencies

        # getting an array of time periodic
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sampleRate, hop_length=512, n_fft=nFft)

        self.timeIndexRatio = len(times)/times[len(times) - 1]
        self.frequenciesIndexRatio = len(frequencies)/frequencies[len(frequencies)-1]

    def get_decibel(self, targetTime, frequency):
        return self.spectrogram[int(frequency * self.frequenciesIndexRatio)][int(targetTime * self.timeIndexRatio)]


class Modifier:
    def __init__(self, analyser):
        self.frequencies = [100, 800, 2000, 8000]
        self.values = [0, 0, 0, 0]
        self.weights = [0.01, 0.01, 0.01, 0.01]
        self.analyser = analyser

    def update(self, pos):
        for i, frequency in enumerate(self.frequencies):
            decibel = self.analyser.get_decibel(pos, frequency)
            self.values[i] = abs(decibel) * self.weights[i]

def wireCube(modifier):
    cubeVertices = (
        (1 + modifier.values[0], 1, 1),
        (1 + modifier.values[0], 1, -1),
        (1 + modifier.values[1], -1, -1),
        (1 + modifier.values[1], -1, 1),
        (-1 - modifier.values[2], 1, 1),
        (-1 - modifier.values[3], -1, -1),
        (-1 - modifier.values[3], -1, 1),
        (-1 - modifier.values[2], 1, -1)
    )
    cubeEdges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))

    glLineWidth(2.0)

    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

if len(sys.argv) != 2:
    print("Usage: python3 main.py <wave file>")
    quit()

filename = sys.argv[1]
try:
    timeSeries, sampleRate = librosa.load(filename)  # getting information from the file
except FileNotFoundError:
    print("Unable to open", filename)
    quit()

pygame.init()
pygame.display.set_caption('Music visualizer')

display = (800, 600)
screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

gluPerspective(60, (display[0]/display[1]), 0.1, 100.0)
glTranslatef(0.0, 0.0, -5)

analyser = Analyser(timeSeries, sampleRate)
modifier = Modifier(analyser)
t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(filename)
pygame.mixer.music.play(0)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glEnable(GL_FOG)
glFogfv(GL_FOG_COLOR, [0.5, 0.5, 0.5, 1.0])
glFogi(GL_FOG_MODE, GL_EXP)
glFogfv(GL_FOG_START, 0.5)
glFogfv(GL_FOG_END, 10)
glFogf(GL_FOG_DENSITY, 0.35)
glClearColor(0.5, 0.5, 0.5, 1.0)

running = True
while running:
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    modifier.update(pygame.mixer.music.get_pos()/1000.0)

    glRotatef(0.1, 1, 0.5, 0.3)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    wireCube(modifier)
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
