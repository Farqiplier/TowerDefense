from projectiles import Projectile, CannonProjectile
import pygame

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = (255, 0, 0)
        self.range = 200
        self.price = 100
        self.projectiles = []
        self.fire_rate = 1  # Default fire rate (1 shot per second)
        self.last_shot_time = 0  # Time of the last shot

    def fire(self, enemies, current_time):
        # Fire at the first enemy in range if enough time has passed since the last shot
        if current_time - self.last_shot_time >= 1 / self.fire_rate:
            for enemy in enemies:
                distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
                if distance <= self.range:
                    projectile = Projectile(self.x, self.y, enemy, speed=5, damage=1, color=self.color)
                    self.projectiles.append(projectile)
                    self.last_shot_time = current_time  # Update the last shot time
                    break

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw(screen)

    def update_projectiles(self, screen, enemies):
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.has_hit_target():
                projectile.target.health -= projectile.damage
                if projectile.target.health <= 0 and projectile.target in enemies:
                    enemies.remove(projectile.target)
                self.projectiles.remove(projectile)
            else:
                projectile.draw(screen)

class ArrowTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 0, 0)
        self.price = 75
        self.fire_rate = 1  # 1 shot per second
        self.projectile_speed = 7
        self.projectile_damage = 1

    def fire(self, enemies, current_time):
        if current_time - self.last_shot_time >= 1 / self.fire_rate:
            for enemy in enemies:
                distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
                if distance <= self.range:
                    projectile = Projectile(self.x, self.y, enemy, speed=self.projectile_speed, damage=self.projectile_damage, color=self.color)
                    self.projectiles.append(projectile)
                    self.last_shot_time = current_time
                    break

class LaserTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 0, 255)
        self.price = 150
        self.fire_rate = 0.5  # 1 shot every 2 seconds
        self.projectile_speed = 10
        self.projectile_damage = 2

class CannonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 255, 0)
        self.price = 200
        self.fire_rate = 0.25  # 1 shot every 4 seconds
        self.projectile_speed = 4
        self.projectile_damage = 5
        self.explosion_radius = 300  # Radius of the explosion

    def fire(self, enemies, current_time):
        if current_time - self.last_shot_time >= 1 / self.fire_rate:
            for enemy in enemies:
                distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
                if distance <= self.range:
                    projectile = CannonProjectile(
                        self.x, self.y, enemy, speed=self.projectile_speed,
                        damage=self.projectile_damage, color=self.color,
                        explosion_radius=self.explosion_radius
                    )
                    self.projectiles.append(projectile)
                    self.last_shot_time = current_time
                    break

    def update_projectiles(self, screen, enemies):
        for projectile in self.projectiles[:]:
            projectile.move()
            if isinstance(projectile, CannonProjectile) and projectile.has_hit_target():
                projectile.explode(screen, enemies)  # Apply AoE damage and show explosion
                self.projectiles.remove(projectile)
            elif projectile.has_hit_target():
                projectile.target.health -= projectile.damage
                if projectile.target.health <= 0 and projectile.target in enemies:
                    enemies.remove(projectile.target)
                self.projectiles.remove(projectile)
            else:
                projectile.draw(screen)