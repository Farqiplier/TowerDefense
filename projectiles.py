import pygame
import math

class Projectile:
    def __init__(self, x, y, target, speed, damage, color):
        self.x = x
        self.y = y
        self.target = target
        self.speed = speed
        self.damage = damage
        self.color = color
        self.radius = 5

    def move(self):
        dx, dy = self.target.x - self.x, self.target.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def has_hit_target(self):
        return math.hypot(self.target.x - self.x, self.target.y - self.y) < self.radius + self.target.width // 2

class CannonProjectile(Projectile):
    def __init__(self, x, y, target, speed, damage, color, explosion_radius):
        super().__init__(x, y, target, speed, damage, color)
        self.explosion_radius = explosion_radius  # Radius of the explosion

    def explode(self, screen, enemies):
        # Draw explosion effect
        pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.explosion_radius, 2)
        
        # Deal AoE damage
        for enemy in enemies[:]:  # Make a copy to iterate over
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.explosion_radius:
                if enemy.take_damage(self.damage):  # Returns True if enemy dies
                    enemies.remove(enemy)

    def has_hit_target(self):
        
        return super().has_hit_target()