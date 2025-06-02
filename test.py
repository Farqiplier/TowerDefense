import pygame  # Import the pygame library for game development
import sys  # Import sys for system-specific parameters and functions
from tower import ArrowTower, LaserTower, CannonTower  # Import tower classes
from enemy import Red, Blue, Green, Yellow, Pink, Black, White, Purple, Lead, Zebra, Rainbow, Ceramic, MOAB  # Import enemy classes
from enemy_list import wave_1, path  # Import predefined enemy waves and path
from menu import Menu  # Import the menu class for handling UI

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 900, 900  # Define the width and height of the game window

# Colors
White = (255, 255, 255)  # RGB value for white color
Dark_Green = (0, 200, 0)  # RGB value for dark green color (background)
black = (0, 0, 0)  # RGB value for black color
Path_color = (150, 150, 150)  # RGB value for path color

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))  # Create the game window
pygame.display.set_caption("Tower Defense")  # Set the title of the game window

# Define the path
path_line_amount = len(path) - 1  # Number of lines in the path
path_thickness = 30  # Thickness of the path lines

# Player health and money
player_health = 100  # Initialize player's health

# Font for displaying health and money
font = pygame.font.Font(None, 36)  # Define font for rendering text

# Enemy spawning variables
enemy_list = []  # List to store active enemies
wave_index = 0  # Index of the current wave
enemy_spawn_timer = 0  # Timer for spawning enemies
wave_start_time = pygame.time.get_ticks() / 1000  # Start time of the wave in seconds

# Initialize the menu with $3000 starting money
menu = Menu(screen, money=3000)  # Create the menu object

# Towers list
towers = []  # List to store placed towers

# Initialize clock for managing frame rate
clock = pygame.time.Clock()  # Create a clock object to control frame rate

# Main game loop
running = True
while running:
    # Limit the frame rate to 60 FPS and calculate delta_time
    delta_time = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
    current_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds

    mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Handle window close event
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse button click
            menu.handle_click(event.pos)  # Handle clicks for the menu

            # Handle tower placement
            if menu.preview_tower:  # Check if a tower is being previewed
                if event.pos[1] < 750:  # Ensure the tower is placed outside the menu area
                    tower_type = menu.preview_tower["name"]  # Get the type of the tower
                    if menu.money >= menu.preview_tower["price"]:  # Check if the player has enough money
                        # Place the tower based on its type
                        if tower_type == "Arrow Tower":
                            towers.append(ArrowTower(event.pos[0], event.pos[1]))
                        elif tower_type == "Laser Tower":
                            towers.append(LaserTower(event.pos[0], event.pos[1]))
                        elif tower_type == "Cannon Tower":
                            towers.append(CannonTower(event.pos[0], event.pos[1]))
                        menu.money -= menu.preview_tower["price"]  # Deduct the tower's price from the player's money
                        menu.preview_tower = None  # Clear the preview

    # Fill the screen with the background color
    screen.fill(Dark_Green)

    # Draw the path
    for i in range(path_line_amount):  # Iterate through the path points
        pygame.draw.line(screen, Path_color, path[i], path[i + 1], path_thickness)  # Draw the path lines

    # Spawn enemies based on the current wave
    if wave_index < len(wave_1):  # Check if there are more waves
        wave = wave_1[wave_index]  # Get the current wave
        if current_time >= wave["delay_from_start"] + wave_start_time:  # Check if it's time to start the wave
            if enemy_spawn_timer <= 0 and len(enemy_list) < wave["amount"]:  # Check if it's time to spawn an enemy
                enemy_type = wave["type"]  # Get the type of enemy to spawn
                # Spawn the enemy based on its type
                if enemy_type == "Red":
                    enemy_list.append(Red(path))
                elif enemy_type == "Blue":
                    enemy_list.append(Blue(path))
                elif enemy_type == "Green":
                    enemy_list.append(Green(path))
                elif enemy_type == "Yellow":
                    enemy_list.append(Yellow(path))
                elif enemy_type == "Pink":
                    enemy_list.append(Pink(path))
                elif enemy_type == "Black":
                    enemy_list.append(Black(path))
                elif enemy_type == "White":
                    enemy_list.append(White(path))
                elif enemy_type == "Purple":
                    enemy_list.append(Purple(path))
                elif enemy_type == "Lead":
                    enemy_list.append(Lead(path))
                elif enemy_type == "Zebra":
                    enemy_list.append(Zebra(path))
                elif enemy_type == "Rainbow":
                    enemy_list.append(Rainbow(path))
                elif enemy_type == "Ceramic":
                    enemy_list.append(Ceramic(path))
                elif enemy_type == "MOAB":
                    enemy_list.append(MOAB(path))
                enemy_spawn_timer = wave["spawn_delay"]  # Reset the spawn timer
            elif len(enemy_list) >= wave["amount"]:  # Check if all enemies in the wave are spawned
                wave_index += 1  # Move to the next wave
                wave_start_time = current_time  # Update the wave start time
            else:
                enemy_spawn_timer -= delta_time  # Decrease the spawn timer using delta_time

    # Move and draw enemies
    for enemy in enemy_list[:]:  # Create a copy of the enemy list for iteration
        enemy.move()  # Move the enemy along the path
        enemy.draw(screen)  # Draw the enemy on the screen

        # Check if the enemy has reached the end of the path
        if enemy.current_path_index == len(path) - 1:
            player_health -= enemy.health  # Decrease player's health based on enemy's health
            enemy_list.remove(enemy)  # Remove the enemy from the list

    # Update and draw towers
    for tower in towers:  # Iterate through all placed towers
        tower.fire(enemy_list, current_time)  # Fire projectiles at enemies
        tower.update_projectiles(screen, enemy_list)  # Update and draw projectiles
        tower.draw(screen, enemy_list)  # Draw the tower

    # Clean up dead enemies and spawn children
    for enemy in enemy_list[:]:  # Iterate through the enemy list
        if enemy.health <= 0:  # Check if the enemy is dead
            children = enemy.pop()  # Spawn children bloons
            enemy_list.extend(children)  # Add children to the enemy list
            menu.money += enemy.money  # Add money for the destroyed enemy
            enemy_list.remove(enemy)  # Remove the dead enemy

    # Display player health
    health_text = font.render(f"Health: {player_health}", True, black)  # Render the health text
    screen.blit(health_text, (50, 10))  # Draw the health text on the screen

    # Draw the menu and the player's money
    menu.draw_menu()  # Draw the menu
    menu.draw_money()  # Draw the player's money

    # Draw the preview tower
    menu.draw_preview(mouse_pos)  # Draw the preview of the tower being placed

    # Update the display
    pygame.display.flip()  # Refresh the screen

    # End the game if the player's health reaches 0
    if player_health <= 0:
        print("Game Over!")  # Print game over message
        running = False  # Exit the game loop

# Quit pygame
pygame.quit()  # Quit pygame
sys.exit()  # Exit the program
