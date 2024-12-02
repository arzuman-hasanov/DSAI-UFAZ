from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def display():
    """Display callback function."""
    glClear(GL_COLOR_BUFFER_BIT)

    render_scene()

    glutSwapBuffers()

def render_scene():
    """Scene render function."""

    # Draw first triangle (red) at the bottom
    glColor3f(1.0, 0.0, 0.0)  # Red
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.3, -0.7, -0.8)  # Adjust y-coordinate for bottom position
    glVertex3f(0.3, -0.7, -1)
    glVertex3f(0, -0.1, -0.9)  # Adjust y-coordinate
    glEnd()

    # Draw second triangle (yellow) at the top
    glPushMatrix()  # Push the current matrix stack

    # Translate the second triangle to the top
    glTranslatef(0.0, 0.8, 0.0)  # Adjust y-coordinate for top position

    glColor3f(1.0, 1.0, 0.0)  # Yellow
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.3, 0.2, 0.0)
    glVertex3f(-0.7, 0.5, 0.0)
    glVertex3f(-0.5, 0.7, 0.0)
    glEnd()

    glPopMatrix()  # Pop the matrix stack

# Initialize GLUT
glutInit()

# Initialize the window with double buffering and RGB colors
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

# Set the window size to 500x500 pixels
glutInitWindowSize(500, 500)

# Create the window and give it a title
glutCreateWindow("Two Triangles: Red at Bottom, Yellow at Top")

# Set the initial window position to (50, 50)
glutInitWindowPosition(50, 50)

# Define display callback
glutDisplayFunc(display)

# Begin event loop
glutMainLoop()