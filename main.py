import librosa
import numpy as np
import pygame
import sys
from enum import Enum

class Analyser:
    def __init__(self, timeSeries, sampleRate):
        hopLength=512
        nFft=2048*4
        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = np.abs(librosa.stft(timeSeries, hop_length=512, n_fft=nFft))
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
        self.weights = [0.8, 1.5, 1, 1.2]
        self.analyser = analyser

    def update(self, pos):
        for i, frequency in enumerate(self.frequencies):
            decibel = self.analyser.get_decibel(pos, frequency)
            self.values[i] = abs(decibel) * self.weights[i]

class DanceType(Enum):
    EDGES = "edges"
    CORNERS = "corners"

class Dancer:
    def __init__(self, x, y, color, w, h, type):
        if not isinstance(type, DanceType):
            raise TypeError('Dance type must be an instance of DanceType enum.')

        self.x, self.y = x, y
        self.color = color
        self.w, self.h = w, h
        self.polygonPoints = None
        self.type = type

    def update(self, dt, values):
        # TODO: use dt

        if self.type == DanceType.EDGES:
            # first freq moves top edge
            # second freq moves bottom edge
            # third freq moves left edge
            # fourth freq moves right edge

            self.polygonPoints = [
                (int(self.x - values[2]), int(self.y - values[0])), # top left
                (int(self.x + values[3]) + self.w, int(self.y - values[0])), # top right
                (int(self.x + self.w + values[3]), int(self.y + self.h + values[1])), # bottom right
                (int(self.x - values[2]), int(self.y + self.h + values[1])) # bottom left
            ];

        elif self.type == DanceType.CORNERS:
            self.polygonPoints = [
                (int(self.x - values[0]),          int(self.y - values[0])),
                (int(self.x + self.w - values[1]), int(self.y - values[1])),
                (int(self.x + self.w - values[2]), int(self.y + self.h - values[2])),
                (int(self.x - values[3]),          int(self.y + self.h - values[3]))
            ]

    def render(self, screen):
        if self.polygonPoints != None:
            pygame.draw.polygon(screen, self.color, self.polygonPoints)

if len(sys.argv) != 2:
    print("Usage: python3 main.py <wave file>")
    quit()

filename = sys.argv[1]
try:
    timeSeries, sampleRate = librosa.load(filename)  # getting information from the file
except FileNotFoundError:
    print("Unable to open", filename)
    quit()

analyser = Analyser(timeSeries, sampleRate)

pygame.init()
pygame.display.set_caption('Music visualizer')

screen_w = 800
screen_h = 600
screen = pygame.display.set_mode([screen_w, screen_h])

modifier = Modifier(analyser)
dancer1 = Dancer(200, 200, (0, 255, 0), 200, 200, DanceType.CORNERS)
dancer2 = Dancer(500, 200, (0, 255, 0), 100, 100, DanceType.EDGES)
t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(filename)
pygame.mixer.music.play(0)

running = True
while running:
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((100, 100, 100))

    modifier.update(pygame.mixer.music.get_pos()/1000.0)

    dancer1.update(deltaTime, modifier.values)
    dancer2.update(deltaTime, modifier.values)

    dancer1.render(screen)
    dancer2.render(screen)

    pygame.display.flip()

pygame.quit()
