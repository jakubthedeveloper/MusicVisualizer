import librosa
import pygame
import sys
from src.analyser import Analyser
from src.modifier import Modifier
from src.renderer import Renderer

test_x = 0
test_y = 0
test_z = 0
test_r = 0

if len(sys.argv) != 2:
    print("Usage: python3 main.py <wave file>")
    quit()

filename = sys.argv[1]
try:
    timeSeries, sampleRate = librosa.load(filename)  # getting information from the file
except FileNotFoundError:
    print("Unable to load file ", filename)
    quit()

analyser = Analyser(timeSeries, sampleRate)
modifier = Modifier(analyser)
renderer = Renderer(modifier)

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
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                test_y += 1
            elif event.key == pygame.K_s:
                test_y -= 1
            elif event.key == pygame.K_a:
                test_x -= 1
            elif event.key == pygame.K_d:
                test_x += 1
            elif event.key == pygame.K_q:
                test_z -= 0.5
            elif event.key == pygame.K_e:
                test_z += 0.5
            elif event.key == pygame.K_z:
                test_r -= 0.5
            elif event.key == pygame.K_x:
                test_r += 0.5

            print (test_x, test_y, test_z, test_r)

    modifier.update(pygame.mixer.music.get_pos() / 1000.0)
    renderer.render(deltaTime)

pygame.quit()
