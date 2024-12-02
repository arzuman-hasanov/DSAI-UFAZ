from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def initialize():
    glClearColor(0.5, 0.5, 0.5, 1.0)  # Background color: gray
    glEnable(GL_DEPTH_TEST)          # Enable depth testing
    glEnable(GL_LIGHTING)            # Enable lighting
    glEnable(GL_LIGHT0)              # Enable light source 0
    glEnable(GL_LIGHT1)              # Enable light source 1
    glEnable(GL_LIGHT2)              # Enable spotlight for cone top

    # Light 0: Green ambient and general lighting
    # Setup light 0 (main light)
    glLightfv(GL_LIGHT0, GL_AMBIENT, GLfloat_4(0.7, 0.7, 0.1, 1.0))  # Slightly increased ambient light
    glLightfv(GL_LIGHT0, GL_DIFFUSE, GLfloat_4(0.7, 0.7, 0.5, 1.0))  # Slightly increased diffuse light
    glLightfv(GL_LIGHT0, GL_SPECULAR, GLfloat_4(0.5, 0.5, 0.4, 1.0))  # Slightly brighter specular light
    glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0.4, 1.5, 2.0, 1.0))  # Same position

    # Light 1: Red ambient and general lighting
    glLightfv(GL_LIGHT1, GL_AMBIENT, GLfloat_4(0.5, 0.5, 0.5, 1.0))  # Increased ambient light
    glLightfv(GL_LIGHT1, GL_DIFFUSE, GLfloat_4(0.3, 0.3, 0.4, 1.0))  # Slightly increased diffuse light
    glLightfv(GL_LIGHT1, GL_SPECULAR, GLfloat_4(0.2, 0.2, 0.3, 1.0))  # Slightly brighter specular light
    glLightfv(GL_LIGHT1, GL_POSITION, GLfloat_4(0.4, 1.5, 2.0, 1.0))  # Same position

    # Light 2: Spotlight for cone tip
    glLightfv(GL_LIGHT2, GL_POSITION, [0.0, 1.2, 0.0, 1.0])    # Positioned at the tip of the cone
    glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, [0.0, -1.0, 0.0])  # Direction pointing downwards
    glLightf(GL_LIGHT2, GL_SPOT_CUTOFF, 15.0)                  # Focused spotlight angle
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [1.0, 1.0, 0.8, 1.0])     # Bright spotlight effect
    glLightfv(GL_LIGHT2, GL_SPECULAR, [1.0, 1.0, 0.8, 1.0])    # Highlight effect
    glLightf(GL_LIGHT2, GL_SPOT_EXPONENT, 50.0)                # Concentrated spotlight

    # Global ambient light (consistent with second code)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])  # Slightly brighter ambient lighting


def setMaterial(color):
    # Material properties for both shapes
    glMaterialfv(GL_FRONT, GL_AMBIENT, [color[0] * 0.2, color[1] * 0.2, color[2] * 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color + [1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 80.0)  # Higher shininess for tighter specular highlights

def drawScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear screen and depth buffer
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40, 1.0, 1.0, 10.0)  # Perspective setup

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 6, 0, 0, 0, 0, 1, 0)  # Camera position and orientation

    # Draw the sphere
    glPushMatrix()
    setMaterial([0.9, 0.9, 0.7])  # Light yellow material
    glTranslatef(0.0, -0.5, 0.0)  # Position sphere lower
    glutSolidSphere(0.8, 50, 50)  # Sphere radius = 0.8
    glPopMatrix()

    # Draw the cone
    glPushMatrix()
    setMaterial([0.9, 0.9, 0.7])  # Same material as sphere
    glTranslatef(0.0, 0.0, 0.0)   # Position cone to align with sphere's top
    glRotatef(-90, 1, 0, 0)       # Rotate cone to point upwards
    glutSolidCone(0.8, 1.3, 50, 50)  # Cone base radius = 0.8, height = 1.3
    glPopMatrix()

    glutSwapBuffers()  # Swap buffers for double buffering

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Cone and Sphere with Lights")
    initialize()
    glutDisplayFunc(drawScene)
    glutMainLoop()

if __name__ == "__main__":
    main()