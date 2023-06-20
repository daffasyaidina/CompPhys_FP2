import math
import random
import pygame
from functions import *  

# Initializing pygame
pygame.init()

# Setting up the screen
SCREEN = WIDTH, HEIGHT = 800, 600

# Adjusting the window size based on the screen orientation
info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
    win = pygame.display.set_mode(SCREEN)
else:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

# Clock and frame rate
clock = pygame.time.Clock()
FPS = 60

# Color definitions
BLACK = (18, 18, 18)
WHITE = (217, 217, 217)
RED = (252, 91, 122)
GREEN = (29, 161, 16)
BLUE = (78, 193, 246)
ORANGE = (252, 76, 2)
YELLOW = (254, 221, 0)
PURPLE = (155, 38, 182)
AQUA = (0, 249, 182)

COLORS = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]

# Font and text rendering
font = pygame.font.SysFont('verdana', 12)

# Origin and radius of the circular path
origin = (20, 400)
radius = 800

# Default values for velocity and gravity
u = 50
g = 9.8

# Textboxes for input
u_textbox = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 50, 140, 32)
g_textbox = pygame.Rect(WIDTH // 2 + 10, HEIGHT - 50, 140, 32)
active = False
active_box = None
u_text = ''
g_text = ''
u_text_surface = font.render(u_text, True, WHITE)
g_text_surface = font.render(g_text, True, WHITE)

# Labels for the textboxes
u_label = font.render('Velocity (m/s)', True, WHITE)
g_label = font.render('Gravity (m/s^2)', True, WHITE)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, u, theta):
        super(Projectile, self).__init__()

        self.u = u
        self.theta = toRadian(abs(theta))
        self.x, self.y = origin
        self.color = random.choice(COLORS)

        self.ch = 0
        self.dx = 2

        # Variables for trajectory calculation
        self.f = self.getTrajectory()
        self.range = self.x + abs(self.getRange())

        self.path = []

    # Calculates the time of flight for the projectile.
    # Formula: (2 * u * sin(theta)) / g
    def timeOfFlight(self):
        return round((2 * self.u * math.sin(self.theta)) / g, 2)

    # Calculates the range of the projectile.
    # Formula: (u^2 * 2 * sin(theta) * cos(theta)) / g
    def getRange(self):
        range_ = ((self.u ** 2) * 2 * math.sin(self.theta) * math.cos(self.theta)) / g
        return round(range_, 2)
    
    # Calculates the maximum height of the projectile.
    # Formula: (u^2 * sin(theta)^2) / (2 * g)
    def getMaxHeight(self):
        h = ((self.u ** 2) * (math.sin(self.theta)) ** 2) / (2 * g)
        return round(h, 2)
    
    # Calculates the trajectory constant of the projectile.
    # Formula: g / (2 * u^2 * cos(theta)^2)
    def getTrajectory(self):
        return round(g / (2 * (self.u ** 2) * (math.cos(self.theta) ** 2)), 4)

    # Calculates the vertical position of the projectile at a given horizontal position.
    # Formula: x * tan(theta) - f * x^2
    def getProjectilePos(self, x):
        return x * math.tan(self.theta) - self.f * x ** 2

    # Updates the position of the projectile.
    def update(self):
        if self.x >= self.range:
            self.dx = 0
        self.x += self.dx
        self.ch = self.getProjectilePos(self.x - origin[0])

        self.path.append((self.x, self.y - abs(self.ch)))
        self.path = self.path[-50:]

        # Drawing the projectile path
        max_path_length = 200
        if len(self.path) > max_path_length:
            self.path = self.path[-max_path_length:]
        
        pygame.draw.circle(win, self.color, self.path[-1], 5)
        pygame.draw.circle(win, WHITE, self.path[-1], 5, 1)
        for pos in self.path[:-1:5]:
            pygame.draw.circle(win, WHITE, pos, 1)

# Group to hold projectiles
projectile_group = pygame.sprite.Group()

# Variables for user interaction
clicked = False
currentp = None

# Initial theta and line end point
theta = -30
end = getPosOnCircumeference(theta, origin)
arct = toRadian(theta)
arcrect = pygame.Rect(origin[0] - 30, origin[1] - 30, 60, 60)

running = True
while running:
    win.fill(BLACK)  # Clear the screen
    
    # Quit event detected, exit the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Exit the game loop when Esc or Q key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
        
        # Reset the projectile group and current projectile
            if event.key == pygame.K_r:
                projectile_group.empty()
                currentp = None

        # Reset the velocity and gravity values
            if event.key == pygame.K_g:
                active = True
                active_box = 'g'

        # Activate the gravity input textbox
            if event.key == pygame.K_h:
                active = True
                active_box = 'u'

        
            if active:
                if active_box == 'u':
                    if event.key == pygame.K_RETURN:
                        try:                                # Parse the velocity input and update the textbox surface
                            u = float(u_text)
                        except ValueError:
                            print("Invalid input for velocity!")
                            u_text = ''
                        u_text_surface = font.render(u_text, True, WHITE)
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        u_text = u_text[:-1]                 # Remove the last character from the velocity input
                    else:
                        u_text += event.unicode              # Append the pressed key to the velocity input
                    u_text_surface = font.render(u_text, True, WHITE)
                elif active_box == 'g':
                    if event.key == pygame.K_RETURN:         # Parse the gravity input and update the textbox surface
                        try:
                            g = float(g_text)
                        except ValueError:
                            print("Invalid input for gravity!")
                            g_text = ''
                        g_text_surface = font.render(g_text, True, WHITE)
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        g_text = g_text[:-1]                # Remove the last character from the gravity input
                    else:
                        g_text += event.unicode              # Append the pressed key to the gravity input
                    g_text_surface = font.render(g_text, True, WHITE)

        # Create a new projectile and add it to the group
        if event.type == pygame.MOUSEBUTTONUP:
            pos = event.pos
            theta = getAngle(pos, origin)
            if -90 < theta <= 0:
                projectile = Projectile(u, theta)
                projectile_group.add(projectile)
                currentp = projectile

        # Update the line end point and arc angle indicator
            pos = pygame.mouse.get_pos()
            theta = getAngle(pos, origin)
            if -90 < theta <= 0:
                end = getPosOnCircumeference(theta, origin)
                arct = toRadian(theta)
       
        if event.type == pygame.MOUSEMOTION:
            if clicked:
                pos = event.pos
                theta = getAngle(pos, origin)
                if -90 < theta <= 0:
                    end = getPosOnCircumeference(theta, origin)
                    arct = toRadian(theta)

    # Draw UI elements
    pygame.draw.rect(win, WHITE, u_textbox, 2)
    win.blit(u_text_surface, (u_textbox.x + 5, u_textbox.y + 5))

    pygame.draw.rect(win, WHITE, g_textbox, 2)
    win.blit(g_text_surface, (g_textbox.x + 5, g_textbox.y + 5))

    pygame.draw.line(win, WHITE, origin, (origin[0] + radius, origin[1]), 2)
    pygame.draw.line(win, WHITE, origin, (origin[0], origin[1] - radius), 2)
    pygame.draw.line(win, AQUA, origin, end, 2)
    pygame.draw.circle(win, WHITE, origin, 3)
    pygame.draw.arc(win, AQUA, arcrect, 0, -arct, 2)

    # Update and draw projectiles
    projectile_group.update()

    # Display information and labels
    title = font.render("GolfDriveSim", True, WHITE)
    fpstext = font.render(f"FPS : {int(clock.get_fps())}", True, WHITE)
    thetatext = font.render(f"Angle : {int(abs(theta))}", True, WHITE)
    degreetext = font.render(f"{int(abs(theta))}°", True, YELLOW)
    win.blit(title, (400, 30))
    win.blit(fpstext, (20, 420))
    win.blit(thetatext, (20, 440))
    win.blit(degreetext, (origin[0] + 38, origin[1] - 20))

    if currentp:
        gravitytext = font.render(f"Gravity : {g}m/s^2", True, WHITE)
        veltext = font.render(f"Velocity : {currentp.u}m/s", True, WHITE)
        timetext = font.render(f"Time : {currentp.timeOfFlight()}s", True, WHITE)
        rangetext = font.render(f"Range : {currentp.getRange()}m", True, WHITE)
        heighttext = font.render(f"Max Height : {currentp.getMaxHeight()}m", True, WHITE)
        win.blit(gravitytext, (WIDTH - 150, 410))
        win.blit(veltext, (WIDTH - 150, 430))
        win.blit(timetext, (WIDTH - 150, 450))
        win.blit(rangetext, (WIDTH - 150, 470))
        win.blit(heighttext, (WIDTH - 150, 490))
        win.blit(u_label, (u_textbox.x, u_textbox.y - 25))
        win.blit(g_label, (g_textbox.x, g_textbox.y - 25))
        win.blit(u_text_surface, (u_textbox.x + 5, u_textbox.y + 5))
        win.blit(g_text_surface, (g_textbox.x + 5, g_textbox.y + 5))

    pygame.draw.rect(win, WHITE, u_textbox, 2)
    pygame.draw.rect(win, WHITE, g_textbox, 2)
    pygame.draw.rect(win, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 5)

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
