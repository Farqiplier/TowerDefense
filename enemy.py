import pygame

# Bloon layer map defining what each bloon spawns into when popped
bloon_layer_map = {
    "Red": [],  # Red bloon doesn't spawn any children
    "Blue": ["Red"],  # Blue bloon spawns into 1 Red bloon
    "Green": ["Blue"],  # Green bloon spawns into 1 Blue bloon
    "Yellow": ["Green"],  # Yellow bloon spawns into 1 Green bloon
    "Pink": ["Yellow"],  # Pink bloon spawns into 1 Yellow bloon
    "Black": ["Yellow", "Yellow"],  # Black bloon spawns into 2 Yellow bloons
    "White": ["Yellow", "Yellow"],  # White bloon spawns into 2 Yellow bloons
    "Purple": ["Pink"],  # Purple bloon spawns into 1 Pink bloon
    "Lead": ["Black", "Black"],  # Lead bloon spawns into 2 Black bloons
    "Zebra": ["Black", "White"],  # Zebra bloon spawns into 1 Black and 1 White bloon
    "Rainbow": ["Zebra", "Zebra"],  # Rainbow bloon spawns into 2 Zebra bloons
    "Ceramic": ["Rainbow", "Rainbow"],  # Ceramic bloon spawns into 2 Rainbow bloons
    "MOAB": ["Ceramic", "Ceramic", "Ceramic", "Ceramic"],  # MOAB spawns into 4 Ceramic bloons
}

class Enemy:
    def __init__(self, path, health, speed, money, bloon_type):
        # Initialize the enemy with its path, health, speed, reward money, and bloon type
        self.path = path  # Path the enemy follows
        self.health = health  # Current health of the enemy
        self.max_health = health  # Maximum health of the enemy
        self.speed = speed  # Movement speed of the enemy
        self.money = money  # Money rewarded when the enemy is defeated
        self.bloon_type = bloon_type  # Type of the bloon (e.g., "Red", "Blue")
        self.current_path_index = 0  # Index of the current path point
        self.x, self.y = self.path[self.current_path_index]  # Initial position of the enemy
        self.width = 40  # Width of the enemy's rectangle
        self.height = 40  # Height of the enemy's rectangle
        self.color = (255, 0, 0)  # Default color for enemies (red)
        self.update_rect()  # Update the rectangle representing the enemy

    def update_rect(self):
        # Update the rectangle representing the enemy's position and size
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def move(self):
        # Move the enemy along its path
        if self.current_path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.current_path_index + 1]  # Next target position
            dx, dy = target_x - self.x, target_y - self.y  # Distance to the target
            distance = (dx**2 + dy**2)**0.5  # Euclidean distance to the target

            if distance <= self.speed:
                # If the enemy can reach the target in one step, move directly to it
                self.x, self.y = target_x, target_y
                self.current_path_index += 1
            else:
                # Otherwise, move proportionally towards the target
                self.x += self.speed * dx / distance
                self.y += self.speed * dy / distance

            self.update_rect()  # Update the rectangle after moving

    def draw(self, screen):
        # Draw the enemy on the screen
        pygame.draw.rect(screen, self.color, self.rect)  # Draw the enemy's rectangle
        self.draw_health_bar(screen)  # Draw the health bar

    def draw_health_bar(self, screen):
        # Draw the health bar below the enemy
        health_bar_width = self.width  # Width of the health bar
        health_bar_height = 5  # Height of the health bar
        health_bar_x = self.rect.x  # X-coordinate of the health bar
        health_bar_y = self.rect.y + self.height + 2  # Y-coordinate of the health bar

        current_health_width = int(health_bar_width * (self.health / self.max_health))  # Width of the current health

        # Draw the background (red) and current health (green) portions of the health bar
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

    def take_damage(self, damage):
        # Reduce the enemy's health by the given damage amount
        self.health -= damage
        return self.health <= 0  # Return True if the enemy's health drops to 0 or below

    def pop(self):
        """Spawn new bloons based on the bloon_layer_map."""
        children = []  # List to store spawned bloons
        if self.bloon_type in bloon_layer_map:
            child_types = bloon_layer_map[self.bloon_type]  # Get the types of bloons to spawn
            for i, child_type in enumerate(child_types):
                # Spawn each child with a 30-pixel offset
                offset_x = (i - len(child_types) // 2) * 30  # Horizontal offset for child bloons
                child_x = self.x + offset_x  # X-coordinate of the child bloon
                child_y = self.y  # Y-coordinate of the child bloon
                child_class = globals()[child_type]  # Dynamically get the class by name
                children.append(child_class(self.path))  # Create and add the child bloon to the list
        return children  # Return the list of spawned bloons

# Define specific bloon classes with unique attributes and colors
class Red(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1, money=10, bloon_type="Red")
        self.color = (255, 0, 0)  # Red color

class Blue(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.4, money=20, bloon_type="Blue")
        self.color = (0, 0, 255)  # Blue color

class Green(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.8, money=30, bloon_type="Green")
        self.color = (0, 255, 0)  # Green color

class Yellow(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=3.2, money=50, bloon_type="Yellow")
        self.color = (255, 255, 0)  # Yellow color

class Pink(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=3.5, money=60, bloon_type="Pink")
        self.color = (255, 192, 203)  # Pink color

class Black(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.8, money=60, bloon_type="Black")
        self.color = (5, 5, 5)  # Black color

class White(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=2.0, money=60, bloon_type="White")
        self.color = (250, 250, 250)  # White color

class Purple(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=3.0, money=60, bloon_type="Purple")
        self.color = (160, 32, 240)  # Purple color

class Lead(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.0, money=60, bloon_type="Lead")
        self.color = (128, 128, 128)  # Lead color

class Zebra(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.8, money=60, bloon_type="Zebra")

    def draw(self, screen):
        # Draw the Zebra bloon with alternating black and white stripes
        part_width = self.width // 7  # Width of each stripe
        for i in range(7):
            part_color = (0, 0, 0) if i % 2 == 0 else (255, 255, 255)  # Alternate colors
            part_rect = pygame.Rect(
                self.rect.x + i * part_width,
                self.rect.y,
                part_width,
                self.height
            )
            pygame.draw.rect(screen, part_color, part_rect)  # Draw each stripe
        self.draw_health_bar(screen)  # Draw the health bar

class Rainbow(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=2.2, money=60, bloon_type="Rainbow")
        self.colors = [
            (148, 0, 211),  # Violet
            (75, 0, 130),   # Indigo
            (0, 0, 255),    # Blue
            (0, 255, 0),    # Green
            (255, 255, 0),  # Yellow
            (255, 127, 0),  # Orange
            (255, 0, 0)     # Red
        ]

    def draw(self, screen):
        # Draw the Rainbow bloon with a gradient of rainbow colors
        part_width = self.width // 7  # Width of each color segment
        for i in range(7):
            part_color = self.colors[i]  # Get the color for the segment
            part_rect = pygame.Rect(
                self.rect.x + i * part_width,
                self.rect.y,
                part_width,
                self.height
            )
            pygame.draw.rect(screen, part_color, part_rect)  # Draw each color segment
        self.draw_health_bar(screen)  # Draw the health bar

class Ceramic(Enemy):
    def __init__(self, path):
        super().__init__(path, health=10, speed=2.5, money=100, bloon_type="Ceramic")
        self.color = (138, 102, 66)  # Ceramic color

class MOAB(Enemy):
    def __init__(self, path):
        super().__init__(path, health=200, speed=1.0, money=500, bloon_type="MOAB")
        self.color = (12, 23, 255)  # MOAB color
