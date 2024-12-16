from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import random

# Window dimensions
width, height = 800, 600

# Texture IDs
ground_texture_id = None
sky_texture_id = None
volcano_texture_id = None
lava_texture_id = None
sun_texture_id = None
moon_texture_id = None

# Camera position
camera_x = 0.0
camera_y = 45.0
camera_z = 50.0

blade_rotation_angle = 0.0

# Eruption state
is_erupting = False
particles = []
particle_lifetime = 100

# Raining state
is_raining = False
raindrops = []

# Day-night mode
is_night = False  # Starts in day mode

# Sunlight properties
sun_light_position = [30.0, 30.0, -50.0, 0.0]  # Directional light
sun_light_ambient = [0.2, 0.2, 0.2, 1.0]      # Ambient light intensity
sun_light_diffuse = [1.0, 1.0, 0.8, 1.0]      # Diffuse light intensity
sun_light_specular = [1.0, 1.0, 1.0, 1.0]     # Specular light intensity

class Particle:
    """Class to define a particle in the volcanic eruption."""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = random.uniform(-0.5, 0.5) # Horizontal velocity component
        self.vy = random.uniform(1.0, 2.0) # Vertical velocity component
        self.vz = random.uniform(-0.5, 0.5) # Depth velocity component
        self.life = particle_lifetime # Remaining life of the particle

    def update(self):
        """Update the particle position and life."""
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.vy -= 0.05  # Simulate gravity
        self.life -= 2 # Decrease the particle's life

    def is_alive(self):
        """Check if the particle is still alive."""
        return self.life > 0

class Raindrop:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z # Initial position
        self.vy = random.uniform(-0.5, -1.5) # Downward velocity

    def update(self):
        self.y += self.vy
        if self.y < 0: # Reset raindrop position if it falls out of view
            self.y = 35.0 # Reset height
            self.x = random.uniform(-10.0, 10.0) # Randomize horizontal position
            self.z = random.uniform(-35.0, -25.0) # Randomize depth position

def load_texture(image_path):
    """Loading texture"""
    image = Image.open(image_path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM) # Flip image for correct orientation
    image_data = np.array(image, dtype=np.uint8)

    # Generate a texture ID and configure its properties
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # Horizontal wrapping
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # Vertical wrapping
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # Minification filter
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # Magnification filter
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    glBindTexture(GL_TEXTURE_2D, 0) # Unbind the texture

    return texture_id

def generate_height(x, z):
    """Generate procedural terrain height."""
    scale1 = 0.1 # Large-scale frequency
    amplitude1 = 3.0 # Large-scale amplitude
    scale2 = 0.05 # Small-scale frequency
    amplitude2 = 1.5 # Small-scale amplitude
    return (amplitude1 * np.sin(scale1 * x) * np.cos(scale1 * z) +
            amplitude2 * np.sin(scale2 * x + scale2 * z))

def draw_surface():
    """Draw the ground surface."""
    global ground_texture_id
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ground_texture_id)

    grid_size = 100 # Number of grid cells along each dimension
    spacing = 1.0 # Distance between adjacent grid vertices

    glBegin(GL_QUADS)
    for i in range(grid_size):
        for j in range(grid_size):
            # Define grid vertices
            x1, z1 = i * spacing - 50.0, j * spacing - 50.0
            x2, z2 = x1 + spacing, z1 + spacing

            # Compute height values at grid vertices
            y1 = generate_height(x1, z1)
            y2 = generate_height(x2, z1)
            y3 = generate_height(x2, z2)
            y4 = generate_height(x1, z2)

            # Compute texture coordinates
            t1, t2 = i / grid_size * 5.0, j / grid_size * 5.0
            t3, t4 = t1 + 5.0 / grid_size, t2 + 5.0 / grid_size

            # Map vertices and texture coordinates
            glTexCoord2f(t1, t2)
            glVertex3f(x1, y1, z1)

            glTexCoord2f(t3, t2)
            glVertex3f(x2, y2, z1)

            glTexCoord2f(t3, t4)
            glVertex3f(x2, y3, z2)

            glTexCoord2f(t1, t4)
            glVertex3f(x1, y4, z2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0) # Unbind texture
    glDisable(GL_TEXTURE_2D)

num_segments = 72 # Number of segments in a circular structure
perturbations = [0.05 * np.sin(4 * (2 * np.pi * i / num_segments)) + random.uniform(-0.02, 0.02)
                 for i in range(num_segments + 1)] # Add randomness for a natural look

def setup_lava_light():
    """Setup a bright light source for the lava."""
    lava_light_position = [-15.0, 20.0, -30.0, 1.0]  # Position at crater
    lava_light_diffuse = [1.0, 0.5, 0.0, 1.0]        # Diffuse light with bright orange glow
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, lava_light_position)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lava_light_diffuse)
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.3, 0.1, 0.0, 1.0])  # Dim ambient

def set_emissive_material():
    """Set the material to emit light."""
    glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 0.2, 0.0, 1.0])  # Glowing orange

def draw_volcano():
    """Draw the volcano with a crater and lava."""
    global volcano_texture_id, lava_texture_id
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, volcano_texture_id)

    glPushMatrix()
    glTranslatef(-15.0, 0.0, -30.0) # Position the volcano
    glScalef(10.0, 20.0, 10.0) # Scale the volcano dimensions

    base_radius = 1.0 # Base radius of the volcano
    crater_radius_outer = 0.4 # Outer radius of the crater
    crater_radius_inner = 0.2 # Inner radius of the lava pool
    crater_depth = 0.1 # Depth of the crater
    lava_height = 0.95 * (1.0 - crater_depth) # Height of the lava within the crater

    # Draw the outer structure of the volcano
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(num_segments + 1):
        angle = 2 * np.pi * i / num_segments
        perturbation = perturbations[i] # Add random variations
        adjusted_height = 1.0 - crater_depth + perturbation

        x_base = base_radius * np.cos(angle)
        z_base = base_radius * np.sin(angle)

        x_crater = crater_radius_outer * np.cos(angle)
        z_crater = crater_radius_outer * np.sin(angle)

        glTexCoord2f(0.5 + 0.5 * np.cos(angle), 0.5 + 0.5 * np.sin(angle))
        glVertex3f(x_base, perturbation, z_base)

        glTexCoord2f(0.5 + 0.5 * x_crater, 0.5 + 0.5 * z_crater)
        glVertex3f(x_crater, adjusted_height, z_crater)
    glEnd()

    # Draw the lava
    glBindTexture(GL_TEXTURE_2D, lava_texture_id)
    setup_lava_light()       # Set lava-specific lighting
    set_emissive_material()  # Make lava glow
    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0.5, 0.5) # Center of the lava pool
    glVertex3f(0.0, lava_height, 0.0)
    for i in range(num_segments + 1):
        angle = 2 * np.pi * i / num_segments
        x_crater_inner = crater_radius_inner * np.cos(angle)
        z_crater_inner = crater_radius_inner * np.sin(angle)

        glTexCoord2f(0.5 + 0.5 * x_crater_inner, 0.5 + 0.5 * z_crater_inner)
        glVertex3f(x_crater_inner, lava_height, z_crater_inner)
    glEnd()

    # Reset emissive and light settings
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
    glDisable(GL_LIGHT1)

    glPopMatrix()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

def draw_particles():
    """Draw the particles for the volcanic eruption."""
    global particles
    glDisable(GL_LIGHTING)  # Disable lighting for particles
    glPointSize(5.0)
    glBegin(GL_POINTS)
    for particle in particles:
        glColor3f(1.0, random.uniform(0.3, 0.5), 0.0)  # Particle color
        glVertex3f(particle.x, particle.y, particle.z)
    glEnd()
    glEnable(GL_LIGHTING)  # Re-enable lighting
    glColor3f(1.0, 1.0, 1.0)  # Reset color to white

def update_particles():
    """Update the particle positions."""
    global particles
    for particle in particles:
        particle.update()
    # Keep only particles that are still alive
    particles = [p for p in particles if p.is_alive()]

    # Generate new particles if the volcano is erupting
    if is_erupting:
        for _ in range(10):
            particles.append(Particle(-15.0, 20.0, -30.0))
            
sun_rotation_angle = 0.0  # Global rotation angle for the sun

def draw_sun():
    """Draw the sun in the sky."""
    global sun_texture_id, is_night, sun_rotation_angle
    if is_night:
        return  # Do not render the sun during the night

    glDisable(GL_LIGHTING)  # Disable lighting for the sun texture
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, sun_texture_id)

    glPushMatrix()
    glTranslatef(30.0, 30.0, -50.0)  # Position the sun in the sky
    glRotatef(sun_rotation_angle, 0.0, 1.0, 0.0)  # Rotate the sun on its Y-axis
    glColor3f(1.0, 1.0, 1.0)  # Reset color for texture

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, 5.0, 36, 18)  # Sun as a sphere with radius 5
    gluDeleteQuadric(quadric)

    glPopMatrix()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)  # Re-enable lighting


def draw_moon():
    """Draw the moon in the night sky."""
    global moon_texture_id, is_night
    if not is_night:
        return  # Do not render the moon during the day

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, moon_texture_id)

    glPushMatrix()
    glTranslatef(30.0, 30.0, -50.0)  # Position the moon in the sky
    glColor3f(1.0, 1.0, 1.0)  # Reset color for texture

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, 5.0, 36, 18)  # Moon as a sphere with radius 5
    gluDeleteQuadric(quadric)

    glPopMatrix()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

    
def draw_circle(x, y, radius):
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 1.0, 1.0)  # Set color to white (for clouds)
    glVertex2f(x, y)  # Center of the circle
    for angle in range(0, 361, 1):  # 0 to 360 degrees
        theta = math.radians(angle)
        x_pos = x + radius * math.cos(theta) # Calculate x position
        y_pos = y + radius * math.sin(theta) # Calculate y position
        glVertex2f(x_pos, y_pos)
    glEnd()

blade_rotation_speed = 1.0  # Speed of blade rotation
blade_rotation_angle = 0.0 # Current rotation angle of the blades

def draw_windmill():
    """Draw a windmill with a base and blades."""
    global blade_rotation_angle

    # Draw the base of the windmill 
    glPushMatrix()
    glTranslatef(20.0, 0.0, -20.0)  # Position the windmill base
    glColor3f(0.6, 0.6, 0.6)  # Gray color for the base
    glRotatef(-90, 1.0, 0.0, 0.0)  # Rotate cylinder to make it vertical
    gluCylinder(gluNewQuadric(), 1.0, 1.0, 17.0, 32, 32)  # Render the cylindrical base
    glPopMatrix()

    # Draw the top of the windmill
    glPushMatrix()
    glTranslatef(20.0, 17.0, -20.0)  # Position at the top of the base
    glColor3f(0.8, 0.8, 0.8)  # Light gray for the top
    glutSolidCube(2.0)  # Render a solid cube
    glPopMatrix()

    # Draw and rotate the blades around their axis
    glPushMatrix()
    glTranslatef(20.0, 17.0, -19.5)  # Position blades slightly forward from the top
    glRotatef(blade_rotation_angle, 0.0, 0.0, 1.0)  # Rotate the blades

    glColor3f(0.9, 0.9, 0.9)  # Set blade color to light gray
    for i in range(3):
        glPushMatrix()
        glRotatef(120 * i, 0.0, 0.0, 1.0)  # Rotate each blade by 120 degrees
        glTranslatef(0.0, 6.0, 0.0)  # Offset each blade from the center

        draw_blade()  # Call to draw the blade
        glPopMatrix()

    glPopMatrix()

    
    blade_rotation_angle += blade_rotation_speed
    if blade_rotation_angle >= 360.0:
        blade_rotation_angle -= 360.0  # Reset to prevent overflow


def draw_blade():
    """Render a single windmill blade."""
    glPushMatrix()
    

    glColor3f(0.9, 0.9, 0.9)  # Light gray for the blade
    glScalef(1.0, 8.0, 0.25)  # Scale blade
    gluCylinder(gluNewQuadric(), 0.3, 0.8, 8.0, 32, 32)  # Create a tapered cylinder for the blade

    glPopMatrix()


def draw_cloud(x, y, z, size):
    """Render a cloud using multiple spheres to create a puffed appearance."""
    glPushMatrix()
    glTranslatef(x, y, z) # Position the cloud in 3D space

    # Base sphere (center)
    glColor3f(1.0, 1.0, 1.0)
    glutSolidSphere(size, 12, 12)  # Main central sphere

    # Additional spheres to form the cloud shape
    offsets = [
        (-size * 0.8,  size * 0.2,  0),   # Left-top
        ( size * 0.8,  size * 0.2,  0),   # Right-top
        (-size * 0.4, -size * 0.4,  0),   # Left-bottom
        ( size * 0.4, -size * 0.4,  0),   # Right-bottom
        ( 0,           size * 0.6, -size * 0.3),  # Top
        ( 0,          -size * 0.6,  size * 0.3),  # Bottom
    ]

    # Render each additional sphere based on its offset
    for offset in offsets:
        glPushMatrix()
        glTranslatef(*offset) # Apply offset for sphere position
        glutSolidSphere(size * 0.6, 16, 16)
        glPopMatrix()

    glPopMatrix()

def generate_raindrops():
    """Generate multiple raindrops at random positions."""
    global raindrops
    num_raindrops = 200  # Define the number of raindrops to generate
    raindrops = [
        Raindrop(random.uniform(-50.0, 50.0), random.uniform(20.0, 40.0), random.uniform(-50.0, 50.0))
        for _ in range(num_raindrops)
    ]


def update_raindrops():
    """Update raindrop positions."""
    global raindrops
    for drop in raindrops:
        drop.update() # Update each raindrop's position


def draw_raindrops():
    """Render all raindrops."""
    global raindrops
    glDisable(GL_LIGHTING)  # Disable lighting for a flat rain effect
    glColor3f(0.5, 0.5, 1.0) # Set rain color to a soft blue
    glBegin(GL_LINES)
    for drop in raindrops:
        glVertex3f(drop.x, drop.y, drop.z) # Start of the raindrop line
        glVertex3f(drop.x, drop.y - 0.5, drop.z)  # End of the raindrop line
    glEnd()
    glEnable(GL_LIGHTING) # Re-enable lighting after rendering



def display():
    """Main display function."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(camera_x, camera_y, camera_z, camera_x, camera_y - 0.5, camera_z - 1.0, 0, 1, 0)

    # Draw the main scene elements
    draw_surface() # Render the surface
    draw_windmill() # Render the windmill
    draw_volcano() # Render the volcano
    draw_cloud(0.0, 35.0, -30.0, 4.0)  # Render a cloud at the specified position

    # Render the sun or moon based on day/night mode
    if is_night:
        draw_moon() # Render the moon for night mode
    else:
        draw_sun() # Render the sun for day mode

    # Render eruption particles if the volcano is erupting
    if is_erupting:
        draw_particles()

    # Render raindrops if raining mode is active
    if is_raining:
        update_raindrops() # Update the position of raindrops
        draw_raindrops() # Render the raindrops

    glutSwapBuffers()
    
def reshape(w, h):
    """Handle window resizing."""
    glViewport(0, 0, w, h) # Set the viewport
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 500) # Set perspective projection with a 45-degree field of view
    glMatrixMode(GL_MODELVIEW) # Switch back to the modelview matrix

def keyboard_special(key, x, y):
    """Handle special keyboard keys for camera movement."""
    global camera_x, camera_z
    move_speed = 5 # Speed of movement
    if key == GLUT_KEY_UP: # Move camera forward
        camera_z -= move_speed
    elif key == GLUT_KEY_DOWN: # Move camera backward
        camera_z += move_speed
    elif key == GLUT_KEY_LEFT: # Move camera left
        camera_x -= move_speed
    elif key == GLUT_KEY_RIGHT: # Move camera right
        camera_x += move_speed
    glutPostRedisplay() # Update the display


vertical_move_speed = 2.0 # Speed for vertical camera movement

def keyboard(key, x, y):
    """Handle keyboard inputs."""
    global is_erupting, particles, is_night, camera_y, is_raining
    if key == b'f' or key == b'F':  # Toggle eruption
        is_erupting = not is_erupting
        if is_erupting:
            particles = []  # Clear existing particles when eruption starts
    elif key == b'n' or key == b'N':  # Toggle day-night mode
        is_night = not is_night
        if is_night:
            glClearColor(6 / 255.0, 17 / 255.0, 37 / 255.0, 1.0)  # Night color
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.2, 0.2, 0.5, 1.0])  # Dim diffuse light
            glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.2, 1.0]) # Dim ambient light
        else:
            glClearColor(128 / 255.0, 196 / 255.0, 233 / 255.0, 1.0)  # Day color
            glLightfv(GL_LIGHT0, GL_DIFFUSE, sun_light_diffuse)  # Restore bright diffuse light
            glLightfv(GL_LIGHT0, GL_AMBIENT, sun_light_ambient) # Restore bright ambient light
    elif key == b' ':  # Move camera up
        camera_y += vertical_move_speed
    elif key == b'h' or key == b'H':  # Move camera down
        camera_y -= vertical_move_speed
    elif key == b'r' or key == b'R':  # Toggle raining mode
        is_raining = not is_raining
        if is_raining:
            generate_raindrops()  # Generate raindrops when rain is enabled
    glutPostRedisplay() # Update the display to reflect changes


def timer(value):
    """Timer function for periodic updates and animations."""
    global sun_rotation_angle
    update_particles() # Update the state of particles for animations

    sun_rotation_angle += 1.2 # Increment the sun's rotation angle
    if sun_rotation_angle >= 360.0:
        sun_rotation_angle -= 360.0  # Reset to prevent overflow

    glutPostRedisplay() # Request a redraw of the scene
    glutTimerFunc(16, timer, 0)


def main():
    """Main function to initialize OpenGL and run the application."""
    global ground_texture_id, volcano_texture_id, lava_texture_id, sun_texture_id, moon_texture_id
    
    # Initialize GLUT
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) # Enable double buffering and depth testing
    glutInitWindowSize(width, height) # Set the initial window size
    glutCreateWindow("OpenGL Mini-Project")

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    glClearColor(128/255.0, 196/255.0, 233/255.0, 1.0)

    # Load textures
    ground_texture_id = load_texture("images/ground.jpg")
    volcano_texture_id = load_texture("images/volcano.jpg")
    lava_texture_id = load_texture("images/lava.jpg")
    sun_texture_id = load_texture("images/sun.jpg")
    moon_texture_id = load_texture("images/moon.jpg")

    
    # Setup lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, sun_light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, sun_light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, sun_light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, sun_light_specular)

    # Enable color-based material settings
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Register GLUT callback functions
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard_special)
    glutTimerFunc(16, timer, 0) # Set the timer function for periodic updates

    glutMainLoop()

if __name__ == "__main__":
    main()