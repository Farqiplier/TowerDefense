import pygame  # Import the pygame library for game development
import sys  # Import sys for system-specific parameters and functions
import math # Import math for distance calculations
import random # For Dartling Gunner accuracy

from tower import CannonTower, DartMonkey, TackShooter, SniperMonkey, DartlingGunner, IceTower, BananaFarm, UPGRADES # Import tower classes and UPGRADES
from enemy import Red, Blue, Green, Yellow, Pink, Black, White, Purple, Lead, Zebra, Rainbow, Ceramic, MOAB  # Import enemy classes
from enemy_info import wave_1, path  # Import predefined enemy waves and path
from menu import Menu  # Import the menu class for handling UI

# --- Helper Functions for Collision ---
def dist_point_to_segment(px, py, x1, y1, x2, y2):
    """Calculates the shortest distance from a point to a line segment."""
    line_vec_x, line_vec_y = x2 - x1, y2 - y1
    line_len_sq = line_vec_x**2 + line_vec_y**2
    if line_len_sq == 0: # Segment is a point
        return math.sqrt((px - x1)**2 + (py - y1)**2)

    # Project point onto the line defined by the segment
    t = ((px - x1) * line_vec_x + (py - y1) * line_vec_y) / line_len_sq
    t = max(0.0, min(1.0, t)) # Clamp t to [0, 1] to stay within the segment

    closest_x = x1 + t * line_vec_x
    closest_y = y1 + t * line_vec_y
    return math.sqrt((px - closest_x)**2 + (py - closest_y)**2)

def is_on_path(x, y, path_points, path_thickness):
    """Checks if a point is within the path's thickness."""
    for i in range(len(path_points) - 1):
        p1 = path_points[i]
        p2 = path_points[i+1]
        if dist_point_to_segment(x, y, p1[0], p1[1], p2[0], p2[1]) <= path_thickness / 2:
            return True
    return False

def is_overlapping_tower(new_x, new_y, new_radius, existing_towers):
    """Checks if a proposed tower placement overlaps with any existing tower."""
    for tower in existing_towers:
        # Calculate distance between centers
        dist = math.sqrt((new_x - tower.x)**2 + (new_y - tower.y)**2)
        # Check if their circles overlap (add a small buffer if needed for visual spacing)
        # Assuming tower.radius exists and is roughly consistent with its visual size.
        if dist < (new_radius + tower.radius):
            return True
    return False
# --- End Helper Functions ---


# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 900, 900  # Define the width and height of the game window

# Colors
WHITE = (255, 255, 255)  # RGB value for WHITE color
DARK_GREEN = (0, 200, 0)  # RGB value for dark green color (background)
BLACK = (0, 0, 0)  # RGB value for BLACK color
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

# Initialize the menu
menu = Menu(screen, money=30000)  # Create the menu object with starting money

# Towers list
towers = []  # List to store placed towers

# Initialize clock for managing frame rate
clock = pygame.time.Clock()  # Create a clock object to control frame rate

# Main game loop
running = True

while running:
    # --- Game Loop Timing & Input ---
    # Limit the frame rate to 60 FPS and calculate delta_time
    time_started = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
    current_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds
    mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Handle window close event
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse button click
            # Handle clicks on menu items (buy towers) and upgrade buttons
            menu.handle_click(event.pos, towers) 

            # If a tower is selected for placement (from the buy menu)
            # and no existing tower is currently selected for upgrades
            if menu.selected_tower_to_buy and not menu.selected_placed_tower:
                placement_x, placement_y = event.pos[0], event.pos[1]
                # Use a default radius for placement collision checks
                tower_radius_for_placement = 25 

                if placement_y < 750:  # Ensure the tower is placed outside the menu area
                    # Check for collision with path
                    if is_on_path(placement_x, placement_y, path, path_thickness):
                        print("Cannot place tower on the path!")
                        continue # Skip placement
                    
                    # Check for collision with other towers
                    if is_overlapping_tower(placement_x, placement_y, tower_radius_for_placement, towers):
                        print("Cannot place tower on another tower!")
                        continue # Skip placement

                    tower_type = menu.selected_tower_to_buy["name"]  # Get the type of the tower
                    if menu.money >= menu.selected_tower_to_buy["price"]:  # Check if player has enough money
                        # Create and place the new tower based on its type
                        new_tower = None
                        if tower_type == "Cannon Tower":
                            new_tower = CannonTower(placement_x, placement_y)
                        elif tower_type == "Dart Monkey":
                            new_tower = DartMonkey(placement_x, placement_y)
                        elif tower_type == "Tack Shooter":
                            new_tower = TackShooter(placement_x, placement_y)
                        elif tower_type == "Sniper Monkey":
                            new_tower = SniperMonkey(placement_x, placement_y)
                        elif tower_type == "Dartling Gunner":
                            new_tower = DartlingGunner(placement_x, placement_y)
                        elif tower_type == "Ice Tower":
                            new_tower = IceTower(placement_x, placement_y)
                        elif tower_type == "Banana Farm":
                            new_tower = BananaFarm(placement_x, placement_y)
                        
                        if new_tower: # If tower was successfully created
                            towers.append(new_tower)
                            menu.money -= new_tower.price  # Deduct cost
                            menu.selected_tower_to_buy = None  # Clear selected tower for buying
                            menu.preview_tower = None  # Clear placement preview

    # --- Game State Updates ---
    # Spawn enemies based on the current wave configuration
    if wave_index < len(wave_1):
        wave = wave_1[wave_index]
        if current_time >= wave["delay_from_start"] + wave_start_time:
            if enemy_spawn_timer <= 0 and len(enemy_list) < wave["amount"]:
                enemy_type = wave["type"]
                # Create enemy instance based on type
                if enemy_type == "Red": enemy_list.append(Red(path))
                elif enemy_type == "Blue": enemy_list.append(Blue(path))
                elif enemy_type == "Green": enemy_list.append(Green(path))
                elif enemy_type == "Yellow": enemy_list.append(Yellow(path))
                elif enemy_type == "Pink": enemy_list.append(Pink(path))
                elif enemy_type == "Black": enemy_list.append(Black(path))
                elif enemy_type == "White": enemy_list.append(White(path))
                elif enemy_type == "Purple": enemy_list.append(Purple(path))
                elif enemy_type == "Lead": enemy_list.append(Lead(path))
                elif enemy_type == "Zebra": enemy_list.append(Zebra(path))
                elif enemy_type == "Rainbow": enemy_list.append(Rainbow(path))
                elif enemy_type == "Ceramic": enemy_list.append(Ceramic(path))
                elif enemy_type == "MOAB": enemy_list.append(MOAB(path))
                enemy_spawn_timer = wave["spawn_delay"]
            elif len(enemy_list) >= wave["amount"]: # All enemies for this wave spawned
                wave_index += 1
                wave_start_time = current_time
            else:
                enemy_spawn_timer -= time_started # Countdown to next enemy spawn

    # Move enemies and handle those reaching the end
    for enemy in enemy_list[:]: # Iterate over a copy to allow modification
        enemy.move()
        if enemy.current_path_index == len(path) - 1: # Enemy reached end of path
            player_health -= enemy.health
            menu.money += enemy.money # Player gets money for bloons that leak
            enemy_list.remove(enemy)

    # Update towers (firing, abilities, etc.)
    for tower in towers:
        if isinstance(tower, DartlingGunner):
            tower.fire(mouse_pos, current_time) # Dartling aims at mouse
        elif isinstance(tower, SniperMonkey):
            income = tower.update(enemy_list, current_time) # Sniper may generate income
            if income and income > 0:
                menu.money += income
            tower.fire(enemy_list, current_time) # Sniper also fires
        elif isinstance(tower, IceTower):
            tower.update(enemy_list, current_time, screen) # Ice Tower has its own update for aura
        elif isinstance(tower, BananaFarm):
            money_earned = tower.update(current_time, mouse_pos) # Banana Farm generates money
            if money_earned > 0:
                menu.money += money_earned
        else: # All other shooting towers
            tower.fire(enemy_list, current_time)
        
    # Clean up dead enemies and spawn children bloons
    for enemy in enemy_list[:]:
        if enemy.health <= 0:
            menu.money += enemy.money
            enemy.destroyed(enemy_list) # Spawn child bloons if applicable
            enemy_list.remove(enemy)

    # --- Drawing ---
    screen.fill(DARK_GREEN) # Background

    # Draw the path
    for i in range(path_line_amount):
        pygame.draw.line(screen, Path_color, path[i], path[i + 1], path_thickness)

    # Draw enemies
    for enemy in enemy_list:
        enemy.draw(screen)

    # Draw towers
    for tower in towers:
        tower.draw(screen, enemy_list) # enemy_list is passed for potential range drawing

        # Update and draw projectiles for towers that manage them (MOVED HERE)
        if hasattr(tower, 'projectiles') and tower.projectiles is not None and tower.projectile_type is not None:
             tower.update_projectiles(screen, enemy_list, time_started)  

    # Display player health and money
    health_text = font.render(f"Health: {player_health}", True, BLACK)
    screen.blit(health_text, (50, 10))
    menu.draw_money()

    # Draw menu elements (buy menu, upgrade menu, preview)
    menu.draw_menu()
    menu.draw_upgrade_menu() # Draw upgrade menu if a tower is selected
    menu.draw_preview(mouse_pos) # Draw placement preview

    # Update the display
    pygame.display.flip()

    # --- Game Over Condition ---
    if player_health <= 0:
        print("Game Over!")
        running = False

# --- Game Exit ---
pygame.quit()
sys.exit()
