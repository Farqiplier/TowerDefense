import pygame
import sys
from tower import tower
from enemy import Enemy

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1000, 800

# Colors
white = (10, 255, 10)
black = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Line Drawing Example")

# Create a tower instance at (400, 400)
tower_instance = tower(800, 800)

# Define the path
path = ((0, 100), (200, 100), (200, 400), (600, 400), (600, 100), (600, 0))
path_line_amount = len(path) - 1
path_thickness = 5

# Create an enemy instance at the starting position of the path
enemy_instance = Enemy(path)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(white)

    # Draw the path
    for i in range(path_line_amount):
        pygame.draw.line(screen, black, path[i], path[i + 1], path_thickness)

    # Draw the tower
    pygame.draw.rect(screen, tower_instance.color, tower_instance.rect)

    # Move and draw the enemy
    enemy_instance.move()
    enemy_instance.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()