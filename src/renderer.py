from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

class Renderer:
    def __init__(self, modifier):
        self.modifier = modifier

        pygame.init()
        pygame.display.set_caption('Music visualizer')

        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        gluPerspective(60, (display[0]/display[1]), 0.1, 100.0)
        glTranslatef(0.0, 0.0, -5)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, [0.5, 0.5, 0.5, 1.0])
        glFogi(GL_FOG_MODE, GL_EXP)
        glFogfv(GL_FOG_START, 0.5)
        glFogfv(GL_FOG_END, 10)
        glFogf(GL_FOG_DENSITY, 0.35)
        glClearColor(0.5, 0.5, 0.5, 1.0)

    def wire_cube(self, modifier):
        cube_vertices = (
            (1 + modifier.values[0], 1, 1),
            (1 + modifier.values[0], 1, -1),
            (1 + modifier.values[1], -1, -1),
            (1 + modifier.values[1], -1, 1),
            (-1 - modifier.values[2], 1, 1),
            (-1 - modifier.values[3], -1, -1),
            (-1 - modifier.values[3], -1, 1),
            (-1 - modifier.values[2], 1, -1)
        )
        cube_edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))

        glLineWidth(2.0)

        glBegin(GL_LINES)
        for cubeEdge in cube_edges:
            for cubeVertex in cubeEdge:
                glVertex3fv(cube_vertices[cubeVertex])
        glEnd()

    def render(self, dt):
        glRotatef(10 * dt, 1, 0.5, 0.3)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.wire_cube(self.modifier)
        pygame.display.flip()
        pygame.time.wait(10)