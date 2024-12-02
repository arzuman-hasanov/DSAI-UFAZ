#------------------------------------------------------#
#--------------------- Exercise 1 ---------------------#
#------------------------------------------------------#

#Change the background color of the window(black by default) and set it to white(or any other color).

# Importing the necessary Modules
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Display callback function
def display():
    
    # we use glClearColor(red, green, blue, alpha) to set the background color. Alpha represents opacity. For green color we set (0.0, 1.0, 0.0, 1.0).
    glClearColor(0.0, 1.0, 0.0, 1.0)

    glClear(GL_COLOR_BUFFER_BIT)

    # Render scene
    render_Scene()

    # Swap buffers
    glutSwapBuffers()

# Scene render function
def render_Scene():
    # Set current color to red
    glColor3f(1.0, 0.0, 0.0)

    # Draw a square
    glBegin(GL_POLYGON)
    glVertex2f(-0.5, -0.5)
    glVertex2f(-0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glEnd()

# Initialize GLUT
glutInit()

# Initialize the window with double buffering and RGB colors
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

# Set the window size to 500x500 pixels
glutInitWindowSize(500, 500)

# Create the window and give it a title
glutCreateWindow("My First OpenGL Window")

# Set the initial window position to (50, 50)
glutInitWindowPosition(50, 50)

# Define callbacks
glutDisplayFunc(display)

# Begin event loop
glutMainLoop()





#------------------------------------------------------#
#--------------------- Exercise 2 ---------------------#
#------------------------------------------------------#
#Draw the previous window in the middle of the screen (horizontally and vertically) with dimensions (width and height) equal to 500x500.

# Importing the necessary Modules
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pyautogui

# Display callback function
def display():
    # Set background color to white
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Render scene
    render_Scene()

    # Swap buffers
    glutSwapBuffers()

# Scene render function
def render_Scene():
    # Set current color to red
    glColor3f(1.0, 0.0, 0.0)

    # Draw a square
    glBegin(GL_POLYGON)
    glVertex2f(-0.5, -0.5)
    glVertex2f(-0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glEnd()

# Initialize GLUT
glutInit()

# Initialize the window with double buffering and RGB colors
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

# Set the window size to 500x500 pixels
window_width = 500
window_height = 500
glutInitWindowSize(window_width, window_height) #We use this function to set the dimensions of OpenGL window.

# Using pyautogui we get screen resolution
screen_width, screen_height = pyautogui.size()

# Calculating position of the center. We subtract the window size from the screen size and divide by 2.
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

# Setting the window position to the center of the screen
glutInitWindowPosition(window_x, window_y)

# Create the window and give it a title
glutCreateWindow("Centered Window")

# Define callbacks
glutDisplayFunc(display)

# Begin event loop
glutMainLoop()





#------------------------------------------------------#
#--------------------- Exercise 3 ---------------------#
#------------------------------------------------------#
# Add the code allowing to display the size and the position of the current OpenGL window and update this display every time the window is moved or resized.

# Importing the necessary Modules
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pyautogui

# Display callback function
def display():
    # Set background color to white
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Render scene
    render_Scene()

    # Displaying window information
    displayWindowInfo()

    # Swap buffers
    glutSwapBuffers()

# Scene render function
def render_Scene():
    # Set current color to red
    glColor3f(1.0, 0.0, 0.0)

    # Draw a square
    glBegin(GL_POLYGON)
    glVertex2f(-0.5, -0.5)
    glVertex2f(-0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glEnd()

# Function to display the window size and position
def displayWindowInfo():
    # Getting the current window's width, height, x and y position
    window_width = glutGet(GLUT_WINDOW_WIDTH)
    window_height = glutGet(GLUT_WINDOW_HEIGHT)
    window_x = glutGet(GLUT_WINDOW_X)
    window_y = glutGet(GLUT_WINDOW_Y)

    # Printing the information
    print(f"Window Size: {window_width}x{window_height}, Position: ({window_x}, {window_y})")

# Reshape callback function to update window info on resize
def reshape(width, height):
    glViewport(0, 0, width, height)
    # Update window info on reshape
    displayWindowInfo()

# Initialize GLUT
glutInit()

# Initialize the window with double buffering and RGB colors
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

# Set the window size to 500x500 pixels
window_width = 500
window_height = 500
glutInitWindowSize(window_width, window_height)

# Getting screen resolution using pyautogui
screen_width, screen_height = pyautogui.size()

# Calculating center position
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

# Creating the window and giving it a title
glutCreateWindow("OpenGL Window with Info Display")

# Setting the window position to the center of the screen
glutInitWindowPosition(window_x, window_y)

# Define callbacks
glutDisplayFunc(display)
glutReshapeFunc(reshape)  # Set the reshape callback to update window info

# Begin event loop
glutMainLoop()
