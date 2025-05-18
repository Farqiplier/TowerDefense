import pygame
import sys
from tower import ArrowTower, LaserTower, CannonTower
from enemy import RedEnemy, BlueEnemy, GreenEnemy, YellowEnemy
from enemy_list import wave_1, path
from menu import Menu

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 900, 900

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tower Defense")

# Define the path
path_line_amount = len(path) - 1
path_thickness = 8

# Player health and money
player_health = 100

# Font for displaying health and money
font = pygame.font.Font(None, 36)

# Enemy spawning variables
enemy_list = []
wave_index = 0
enemy_spawn_timer = 0
wave_start_time = pygame.time.get_ticks() / 1000  # Start time in seconds

# Initialize the menu with $300 starting money
menu = Menu(screen, money=300)

# Towers list
towers = []

# Initialize clock for managing frame rate
clock = pygame.time.Clock()

running = True
while running:
    # Limit the frame rate to 60 FPS and calculate delta_time
    delta_time = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
    current_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle clicks for the menu
            menu.handle_click(event.pos)

            # Handle tower placement
            if menu.preview_tower:
                # Ensure the tower is placed outside the menu area
                if event.pos[1] < 750:
                    tower_type = menu.preview_tower["name"]
                    if menu.money >= menu.preview_tower["price"]:
                        if tower_type == "Arrow Tower":
                            towers.append(ArrowTower(event.pos[0], event.pos[1]))
                        elif tower_type == "Laser Tower":
                            towers.append(LaserTower(event.pos[0], event.pos[1]))
                        elif tower_type == "Cannon Tower":
                            towers.append(CannonTower(event.pos[0], event.pos[1]))
                        menu.money -= menu.preview_tower["price"]
                        menu.preview_tower = None  # Clear the preview

    # Fill the screen with white
    screen.fill(white)

    # Draw the path
    for i in range(path_line_amount):
        pygame.draw.line(screen, black, path[i], path[i + 1], path_thickness)

    # Spawn enemies based on wave_1
    if wave_index < len(wave_1):
        wave = wave_1[wave_index]
        if current_time >= wave["delay_from_start"] + wave_start_time:
            if enemy_spawn_timer <= 0 and len(enemy_list) < wave["amount"]:
                # Spawn an enemy
                enemy_type = wave["type"]
                if enemy_type == "RedEnemy":
                    enemy_list.append(RedEnemy(path))
                elif enemy_type == "BlueEnemy":
                    enemy_list.append(BlueEnemy(path))
                elif enemy_type == "GreenEnemy":
                    enemy_list.append(GreenEnemy(path))
                elif enemy_type == "YellowEnemy":
                    enemy_list.append(YellowEnemy(path))
                enemy_spawn_timer = wave["spawn_delay"]
            elif len(enemy_list) >= wave["amount"]:
                # Move to the next wave
                wave_index += 1
                wave_start_time = current_time
            else:
                enemy_spawn_timer -= delta_time  # Decrease timer using delta_time

    # Move and draw enemies
    for enemy in enemy_list[:]:
        enemy.move()
        enemy.draw(screen)

        # Check if the enemy has reached the end of the path
        if enemy.current_path_index == len(path) - 1:
            player_health -= enemy.health
            enemy_list.remove(enemy)  # Remove the enemy

    # Update and draw towers
    for tower in towers:
        tower.fire(enemy_list, current_time)  # Pass current_time to respect fire rate
        tower.update_projectiles(screen, enemy_list)
        tower.draw(screen)

    # Display player health
    health_text = font.render(f"Health: {player_health}", True, black)
    screen.blit(health_text, (50, 10))

    # Draw the menu and the player's money
    menu.draw_menu()
    menu.draw_money()

    # Draw the preview tower
    menu.draw_preview(mouse_pos)

    # Update the display
    pygame.display.flip()

    # End the game if the player's health reaches 0
    if player_health <= 0:
        print("Game Over!")
        running = False

# Quit pygame
pygame.quit()
sys.exit()