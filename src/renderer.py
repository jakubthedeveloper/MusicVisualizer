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

    def wire_cube(self, x, y, z, scale_x, scale_y, scale_z):
        cube_vertices = (
            (1 + self.modifier.values[0], 1, 1),
            (1 + self.modifier.values[0], 1, -1),
            (1 + self.modifier.values[1], -1, -1),
            (1 + self.modifier.values[1], -1, 1),
            (-1 - self.modifier.values[2], 1, 1),
            (-1 - self.modifier.values[3], -1, -1),
            (-1 - self.modifier.values[3], -1, 1),
            (-1 - self.modifier.values[2], 1, -1)
        )
        cube_edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))

        glLineWidth(2.0)

        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(scale_x, scale_y, scale_z);
        glBegin(GL_LINES)
        for cubeEdge in cube_edges:
            for cubeVertex in cubeEdge:
                glVertex3fv(cube_vertices[cubeVertex])
        glEnd()
        glPopMatrix()

    def sphere(self):
        glPushMatrix()
        glTranslatef(0, 0, 0)
        quadric = gluNewQuadric()  # TODO: move to class property
        gluSphere(quadric, 0.5, int(20 * self.modifier.values[1]), 10)
        gluDeleteQuadric(quadric)
        glPopMatrix()


    def render(self, dt, test_x, test_y, test_z, test_r):
        glRotatef(10 * dt, 1, 0.5, 0.3)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.wire_cube(-1.8, 0, 0, 0.5, 0.5, 0.5)
        self.wire_cube(0, 0, 0, -0.5, -0.5, 0.5)
        self.wire_cube(0, -1.2, 0, -0.5, -0.5, 0.5)
        self.wire_cube(0, 1.2, 0, -0.5, -0.5, 0.5)
        self.wire_cube(0, 0, -1.5, -0.5, -0.5, 0.5)
        self.wire_cube(0, 0, 1.5, -0.5, -0.5, 0.5)
        self.wire_cube(2, 0, 0, 0.5, 0.5, 0.5)
        #self.sphere()

        pygame.display.flip()
        pygame.time.wait(10)