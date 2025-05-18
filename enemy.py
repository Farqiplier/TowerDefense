import pygame

class Enemy:
    def __init__(self, path):
        self.path = path  # List of (x, y) tuples representing the path
        self.x, self.y = self.path[0]  # Start at the first point in the path (centered)
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)  # Red color for the enemy
        self.speed = 0.2  # Reduced speed to make the enemy slower
        self.health = 3
        self.current_path_index = 0
        self.reward = 10
        self.update_rect()

    def update_rect(self):
        # Update the rect to ensure the position is centered
        self.rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )

    def move(self):
        if self.current_path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.current_path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            distance = (dx**2 + dy**2)**0.5

            if distance <= self.speed:
                # Move to the next point in the path
                self.x, self.y = target_x, target_y
                self.current_path_index += 1
            else:
                # Move toward the next point
                self.x += self.speed * dx / distance
                self.y += self.speed * dy / distance

            self.update_rect()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True  # Enemy is dead
        return False


class RedEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.color = (255, 0, 0)  # Red color for the enemy
        self.health = 1  # Health of the red enemy
        self.speed = 1  # Speed of the red enemy
        self.money = 2  # Money given when the red enemy is killed


class BlueEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.color = (0, 0, 255)  # Blue color for the enemy
        self.health = 2  # Health of the blue enemy
        self.speed = 0.8  # Speed of the blue enemy
        self.money = 4  # Money given when the red enemy is killed

class GreenEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.color = (0, 255, 0)  # Green color for the enemy
        self.health = 3  # Health of the green enemy
        self.speed = 0.6  # Speed of the green enemy
        self.money = 6  # Money given when the red enemy is killed


class YellowEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.color = (255, 255, 0)  # Yellow color for the enemy
        self.health = 4  # Health of the yellow enemy
        self.speed = 0.4  # Speed of the yellow enemy
        self.money = 8  # Money given when the red enemy is killed