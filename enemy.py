import pygame

class Enemy:
    def __init__(self, path):
        self.path = path  # List of (x, y) tuples representing the path
        self.true_x, self.true_y = self.path[0]  # Start at the first point in the path
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)  # Red color for the enemy
        self.speed = 0.2  # Reduced speed to make the enemy slower
        self.health = 100
        self.current_path_index = 0
        self.update_position()
        self.update_rect()

    def update_position(self):
        # Update self.x and self.y to represent the center of the enemy
        self.x = self.true_x + self.width // 2
        self.y = self.true_y + self.height // 2

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
            dx, dy = target_x - self.true_x, target_y - self.true_y
            distance = (dx**2 + dy**2)**0.5

            if distance <= self.speed:
                # Move to the next point in the path
                self.true_x, self.true_y = target_x, target_y
                self.current_path_index += 1
            else:
                # Move toward the next point
                self.true_x += self.speed * dx / distance
                self.true_y += self.speed * dy / distance

            self.update_position()
            self.update_rect()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True  # Enemy is dead
        return False