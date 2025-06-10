import pygame
import os
import math

class Enemy:
    # We will now load _camo_image within __init__ after pygame.display is initialized.
    # So, we remove the class-level loading.
    _camo_image = None 

    def __init__(self, path, health, speed, money, bloon_type, contains, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        self.path = path
        self.health = health
        self.max_health = health
        self.speed = speed
        self.money = money
        self.bloon_type = bloon_type
        self.is_regrowth = is_regrowth
        self.is_camo = is_camo
        
        # Initialize current_path_index, x, and y based on arguments
        self.current_path_index = start_pos_index
        if start_x is not None and start_y is not None:
            self.x = start_x
            self.y = start_y
        else:
            # If no starting position is provided, use the beginning of the path
            self.x, self.y = self.path[self.current_path_index]
        
        # Set default dimensions for most bloons (Normal Bloon Size)
        self.width = 30
        self.height = 40

        # Adjust size specifically for Regrowth bloons
        if self.is_regrowth:
            self.width = 45
            self.height = 60
        
        # MOABs have their own specific dimensions, overriding others
        if self.bloon_type == "MOAB":
            self.width = 120
            self.height = 80


        self.contains = contains # List of Enemy classes this bloon spawns when popped
        self.radius = self.width // 2 # Radius should be based on the determined width for collisions

        # Load the image for the enemy from the 'bloons' folder
        image_path = os.path.join("bloons", f"{self.bloon_type}.png")
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except pygame.error as e:
            print(f"Warning: Could not load bloon image {image_path} - {e}")
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA) # Create a blank surface
            pygame.draw.circle(self.image, (255, 0, 255), (self.width // 2, self.height // 2), self.width // 2) # Magenta placeholder


        # Load camo image here if it hasn't been loaded yet and this is a camo bloon
        if self.is_camo and Enemy._camo_image is None:
            camo_image_path = os.path.join("bloons", "Camo.png")
            if os.path.exists(camo_image_path): # Check if the file exists
                try:
                    Enemy._camo_image = pygame.image.load(camo_image_path).convert_alpha()
                except pygame.error as e:
                    print(f"Warning: Could not load Camo.png - {e}")
                    Enemy._camo_image = None # Ensure it remains None if loading fails
            else:
                print(f"Warning: Camo.png not found at {camo_image_path}, no overlay drawn.")
                Enemy._camo_image = None # Ensure it remains None if file not found


        # IMPORTANT: Call update_rect immediately after setting x, y, width, height
        # to ensure the rect is correct for the first draw/move.
        self.update_rect()

        # Attributes for status effects (e.g., from Ice Tower)
        self.original_speed = speed # Store original speed for debuffs
        self.ice_slow_active = False
        self.ice_slow_expire_time = 0
        self.ice_slow_source = None # To track which Ice Tower applied the slow
        self.frozen = False
        self.freeze_expire_time = 0
        self.frozen_by_ice_tower = False # Flag to prevent continuous re-freezing

    def update_rect(self):
        """Updates the pygame.Rect object for collision detection and drawing."""
        self.rect = self.image.get_rect(center=(self.x, self.y)) # Center the rect at (self.x, self.y)

    def move(self):
        """Moves the enemy along its predefined path."""
        if self.frozen: # If bloon is frozen, it does not move
            return

        if self.current_path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.current_path_index + 1]
            
            # Calculate direction vector
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.sqrt(dx**2 + dy**2)

            # Check if bloon is effectively at the target point
            if dist < self.speed: # If very close to target, jump to next point
                self.x, self.y = target_x, target_y
                self.current_path_index += 1
                # If moved to a new path index, immediately update rect
                self.update_rect() 
            else: # Move towards the target
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
                self.update_rect() # Update rect after every movement

    def take_damage(self, damage_amount):
        """Reduces the enemy's health by the given amount."""
        self.health -= damage_amount

    def draw(self, screen):
        """Draws the enemy on the screen."""
        screen.blit(self.image, self.rect)

        # Draw Camo overlay if it's a camo bloon
        if self.is_camo and Enemy._camo_image:
            # Scale camo image to fit the current bloon's size
            camo_scaled_image = pygame.transform.scale(Enemy._camo_image, (self.width, self.height))
            camo_rect = camo_scaled_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(camo_scaled_image, camo_rect)
        elif self.is_camo and not Enemy._camo_image:
            # This print will now only occur if the file wasn't found or loading failed
            # after the file existence check.
            print("Warning: Camo bloon present but Camo.png failed to load, no overlay drawn.")


        # Draw health bar (optional, for visual feedback)
        health_bar_width = self.width
        health_bar_height = 5
        # Center health bar above the bloon's image
        health_bar_x = self.x - self.width // 2
        health_bar_y = self.y - self.height // 2 - 10
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height)) # Red background
        current_health_width = (self.health / self.max_health) * health_bar_width
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height)) # Green health

    def destroyed(self, enemy_list: list):
        """
        Handles the logic when an enemy is destroyed.
        Spawns child bloons at the parent's current position and path progress.
        """
        for BloonType in self.contains:
            # Pass the current x, y, path index, and also the regrowth/camo properties to the child bloons
            child_bloon = BloonType(
                self.path, 
                start_pos_index=self.current_path_index, 
                start_x=self.x, 
                start_y=self.y,
                is_regrowth=self.is_regrowth, # Pass parent's regrowth status
                is_camo=self.is_camo # Pass parent's camo status
            )
            enemy_list.append(child_bloon)

# Define specific enemy types inheriting from Enemy
# (Health, Speed, Money, BloonType, Contains)

class Red(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=1, speed=1.0, money=10, bloon_type="Red", contains=[], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo)


class Blue(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=1, speed=1.2, money=15, bloon_type="Blue", contains=[Red], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo)


class Green(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=1, speed=1.5, money=20, bloon_type="Green", contains=[Blue], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo)


class Yellow(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=1, speed=1.8, money=25, bloon_type="Yellow", contains=[Green], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo)


class Pink(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=1, speed=2.2, money=30, bloon_type="Pink", contains=[Yellow], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo)


class Black(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=2, speed=1.4, money=40, bloon_type="Black", contains=[Pink, Pink], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo) # Immune to explosion


class White(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=2, speed=1.6, money=40, bloon_type="White", contains=[Pink, Pink], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo) # Immune to freeze


class Purple(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=1, speed=2.0, money=50, bloon_type="Purple", contains=[Pink], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo) # Immune to energy, plasma, fire


class Lead(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=2, speed=0.8, money=50, bloon_type="Lead", contains=[Red, Red], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo) # Immune to sharp


class Zebra(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=1, speed=1.8, money=60, bloon_type="Zebra", contains=[Black, White], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo)


class Rainbow(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=1, speed=2.2, money=60, bloon_type="Rainbow", contains=[Zebra, Zebra], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo)


class Ceramic(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        super().__init__(path, health=10, speed=2.5, money=100, bloon_type="Ceramic", contains=[Rainbow, Rainbow], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo)


class MOAB(Enemy):
    def __init__(self, path, start_pos_index=0, start_x=None, start_y=None, is_regrowth=False, is_camo=False):
        # MOABs typically don't have regrowth/camo properties in BTD6, but the base class
        # handles the parameters. We'll set its specific size here.
        super().__init__(path, health=200, speed=1.0, money=500, bloon_type="MOAB", contains=[Ceramic, Ceramic, Ceramic, Ceramic], start_pos_index=start_pos_index, start_x=start_x, start_y=start_y, is_regrowth=is_regrowth, is_camo=is_camo)
        self.width = 120 # MOAB's explicit width
        self.height = 80 # MOAB's explicit height
        self.image = pygame.image.load(os.path.join("bloons", "MOAB.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.update_rect() # Ensure rect is updated after scaling the image
        
    def draw(self, screen):
        # MOAB's draw method has specific rotation logic
        if self.current_path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.current_path_index + 1]
            # Calculate angle to rotate MOAB image
            dx = target_x - self.x
            dy = target_y - self.y
            angle = math.degrees(math.atan2(-dy, dx)) # Pygame angles are often inverse y
        else:
            angle = 0 # No rotation if at the end of the path

        rotated_image = pygame.transform.rotate(self.image, angle)
        # Get a new rect for the rotated image, centered at the bloon's position
        new_rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_image, new_rect)

        # Draw Camo overlay if it's a camo MOAB (if MOABs can be camo)
        if self.is_camo and Enemy._camo_image:
            camo_scaled_image = pygame.transform.scale(Enemy._camo_image, (self.width, self.height))
            camo_rect = camo_scaled_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(camo_scaled_image, camo_rect)
        elif self.is_camo and not Enemy._camo_image:
            print("Warning: Camo MOAB present but Camo.png failed to load, no overlay drawn.")


        # Draw health bar (optional, for visual feedback)
        health_bar_width = self.width
        health_bar_height = 10
        health_bar_x = self.x - self.width // 2
        health_bar_y = self.y - self.height // 2 - 20 # Position above MOAB
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height)) # Red background
        current_health_width = (self.health / self.max_health) * health_bar_width
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height)) # Green health