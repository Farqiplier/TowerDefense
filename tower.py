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
        if current_time - self.last_shot_time >= 1 / self.fire_rate:
            for enemy in enemies:
                distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
                if distance <= self.range:
                    projectile = Projectile(self.x, self.y, enemy, speed=5, damage=1, color=self.color)
                    self.projectiles.append(projectile)
                    self.last_shot_time = current_time
                    break

    def draw(self, screen, enemies):
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw(screen)

    def update_projectiles(self, screen, enemies):
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.has_hit_target():
                is_dead = projectile.target.take_damage(projectile.damage)
                if is_dead and projectile.target in enemies:
                    enemies.remove(projectile.target)
                self.projectiles.remove(projectile)
            else:
                projectile.draw(screen)

class ArrowTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 0, 0)  # Red color for arrow
        self.price = 75
        self.fire_rate = 0.5  # 1 shot per second
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
        self.color = (0, 0, 255)  # Blue color for laser
        self.price = 150
        self.fire_rate = 100  # Continuous damage (10 times per second)
        self.damage_per_tick = 0.1  # Damage applied per tick

    def fire(self, enemies, current_time):
        # Apply continuous damage to the first enemy in range
        for enemy in enemies:
            distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
            if distance <= self.range:
                if current_time - self.last_shot_time >= 1 / self.fire_rate:
                    is_dead = enemy.take_damage(self.damage_per_tick)
                    if is_dead and enemy in enemies:
                        enemies.remove(enemy)
                    self.last_shot_time = current_time
                break

    def draw(self, screen, enemies):
        super().draw(screen, enemies)
        # Draw a laser beam to the first enemy in range
        for enemy in enemies:
            distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
            if distance <= self.range:
                pygame.draw.line(screen, self.color, (self.x, self.y), (enemy.x, enemy.y), 2)
                break

class CannonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 255, 0)  # Green color for cannon
        self.price = 200
        self.fire_rate = 0.50  # 1 shot every 4 seconds
        self.projectile_speed = 4
        self.projectile_damage = 5
        self.explosion_radius = 100  # Radius of the explosion

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
                # Let the explosion handle enemy removal
                projectile.explode(screen, enemies)
                self.projectiles.remove(projectile)
            elif projectile.has_hit_target():
                is_dead = projectile.target.take_damage(projectile.damage)
                if is_dead and projectile.target in enemies:
                    enemies.remove(projectile.target)
                self.projectiles.remove(projectile)
            else:
                projectile.draw(screen)