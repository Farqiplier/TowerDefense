import pygame

class Enemy:
    def __init__(self, path, health, speed, money):
        self.path = path
        self.health = health
        self.speed = speed
        self.money = money  # Money earned when this enemy is killed
        self.current_path_index = 0
        self.x, self.y = self.path[self.current_path_index]
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)  # Default color for enemies
        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def move(self):
        if self.current_path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.current_path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            distance = (dx**2 + dy**2)**0.5

            if distance <= self.speed:
                self.x, self.y = target_x, target_y
                self.current_path_index += 1
            else:
                self.x += self.speed * dx / distance
                self.y += self.speed * dy / distance

            self.update_rect()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0  # This returns True if enemy should die
class Red(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1, money=10, )
        self.color = (255, 0, 0)


class Blue(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.4, money=20)
        self.color = (0, 0, 255)


class Green(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.8, money=30)
        self.color = (0, 255, 0)


class Yellow(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=3.2, money=50)
        self.color = (255, 255, 0)

class Pink(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=3.5, money=60)
        self.color = (255, 192, 203)

class Black(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.8, money=60)
        self.color = (5, 5, 5)

class White(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=2.0, money=60)
        self.color = (250, 250, 250)

class Purple(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=3.0, money=60)
        self.color = (160, 32, 240)

class Lead(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.0, money=60)
        self.color = (128, 128, 128)

class Zebra(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.8, money=60)

    def draw(self, screen):
        part_width = self.width // 7
        for i in range(7):
            part_color = (0, 0, 0) if i % 2 == 0 else (255, 255, 255)
            part_rect = pygame.Rect(
                self.rect.x + i * part_width,
                self.rect.y,
                part_width,
                self.height
            )
            pygame.draw.rect(screen, part_color, part_rect)
        
class Rainbow(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=2.2, money=60)
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
        part_width = self.width // 7
        for i in range(7):
            part_color = self.colors[i]
            part_rect = pygame.Rect(
                self.rect.x + i * part_width,
                self.rect.y,
                part_width,
                self.height
            )
            pygame.draw.rect(screen, part_color, part_rect)

class Ceramic(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=2.5, money=60)
        self.color = (138, 102, 66)

class MOAB(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.0, money=60)
        self.color = (12, 23, 255)
        
bloon_layer_map = {
    "Red": [],
    "Blue": ["Red"],
    "Green": ["Blue"],
    "Yellow": ["Green"],
    "Pink": ["Yellow"],
    "Black": ["Yellow", "Yellow"],           # Pops into 2 Yellows
    "White": ["Yellow", "Yellow"],           # Pops into 2 Yellows
    "Purple": ["Pink"],                      # Pops into 1 Pink
    "Lead": ["Black", "Black"],              # Pops into 2 Blacks
    "Zebra": ["Black", "White"],             # Pops into 1 Black, 1 White
    "Rainbow": ["Zebra", "Zebra"],           # Pops into 2 Zebras
    "Ceramic": ["Rainbow", "Rainbow"],       # Pops into 2 Rainbows
    "MOAB": ["Ceramic", "Ceramic", "Ceramic", "Ceramic"],  # Pops into 4 Ceramics
} 