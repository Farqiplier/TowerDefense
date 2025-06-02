from projectiles import Projectile, CannonProjectile
import pygame

# Base class for all towers
class Tower:
    def __init__(self, x, y):
        # Initialize tower position, dimensions, and attributes
        self.x = x
        self.y = y
        self.width = 50  # Width of the tower
        self.height = 50  # Height of the tower
        self.color = (255, 0, 0)  # Default color (red)
        self.range = 200  # Range within which the tower can attack enemies
        self.price = 100  # Cost of the tower
        self.projectiles = []  # List to store projectiles fired by the tower
        self.fire_rate = 1  # Default fire rate (1 shot per second)
        self.last_shot_time = 0  # Time of the last shot fired

    # Method to fire projectiles at enemies within range
    def fire(self, enemies, current_time):
        # Check if enough time has passed since the last shot
        if current_time - self.last_shot_time >= 1 / self.fire_rate:
            for enemy in enemies:
                # Calculate distance to the enemy
                distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
                # If the enemy is within range, fire a projectile
                if distance <= self.range:
                    projectile = Projectile(self.x, self.y, enemy, speed=5, damage=1, color=self.color)
                    self.projectiles.append(projectile)  # Add projectile to the list
                    self.last_shot_time = current_time  # Update the last shot time
                    break  # Fire at only one enemy per shot

    # Method to draw the tower and its projectiles on the screen
    def draw(self, screen, enemies):
        # Draw the tower as a rectangle
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
        # Draw all projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)

    # Method to update the state of projectiles (movement, collision, etc.)
    def update_projectiles(self, screen, enemies):
        for projectile in self.projectiles[:]:  # Iterate over a copy of the list
            projectile.move()  # Move the projectile
            if projectile.has_hit_target():  # Check if the projectile hit its target
                is_dead = projectile.target.take_damage(projectile.damage)  # Apply damage to the target
                if is_dead and projectile.target in enemies:
                    enemies.remove(projectile.target)  # Remove the enemy if it is dead
                self.projectiles.remove(projectile)  # Remove the projectile after it hits
            else:
                projectile.draw(screen)  # Draw the projectile if it hasn't hit yet

# Subclass for an Arrow Tower
class ArrowTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize base tower attributes
        self.color = (255, 0, 0)  # Red color for arrow tower
        self.price = 75  # Cost of the arrow tower
        self.fire_rate = 0.5  # Fire rate (2 shots per second)
        self.projectile_speed = 7  # Speed of the arrow projectiles
        self.projectile_damage = 1  # Damage dealt by each arrow projectile

    # Override the fire method to customize projectile attributes
    def fire(self, enemies, current_time):
        if current_time - self.last_shot_time >= 1 / self.fire_rate:
            for enemy in enemies:
                distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
                if distance <= self.range:
                    projectile = Projectile(self.x, self.y, enemy, speed=self.projectile_speed, damage=self.projectile_damage, color=self.color)
                    self.projectiles.append(projectile)
                    self.last_shot_time = current_time
                    break

# Subclass for a Laser Tower
class LaserTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize base tower attributes
        self.color = (0, 0, 255)  # Blue color for laser tower
        self.price = 150  # Cost of the laser tower
        self.fire_rate = 100  # Continuous damage (10 times per second)
        self.damage_per_tick = 0.1  # Damage applied per tick

    # Override the fire method to apply continuous damage
    def fire(self, enemies, current_time):
        for enemy in enemies:
            distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
            if distance <= self.range:
                # Apply damage continuously to the first enemy in range
                if current_time - self.last_shot_time >= 1 / self.fire_rate:
                    is_dead = enemy.take_damage(self.damage_per_tick)
                    if is_dead and enemy in enemies:
                        enemies.remove(enemy)  # Remove the enemy if it is dead
                    self.last_shot_time = current_time
                break

    # Override the draw method to include a laser beam
    def draw(self, screen, enemies):
        super().draw(screen, enemies)  # Draw the tower and projectiles
        for enemy in enemies:
            distance = ((enemy.x - self.x)**2 + (enemy.y - self.y)**2)**0.5
            if distance <= self.range:
                # Draw a laser beam to the first enemy in range
                pygame.draw.line(screen, self.color, (self.x, self.y), (enemy.x, enemy.y), 2)
                break

# Subclass for a Cannon Tower
class CannonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize base tower attributes
        self.color = (0, 255, 0)  # Green color for cannon tower
        self.price = 200  # Cost of the cannon tower
        self.fire_rate = 0.50  # Fire rate (1 shot every 2 seconds)
        self.projectile_speed = 4  # Speed of the cannon projectiles
        self.projectile_damage = 5  # Damage dealt by each cannon projectile
        self.explosion_radius = 100  # Radius of the explosion caused by cannon projectiles

    # Override the fire method to customize projectile attributes
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

    # Override the update_projectiles method to handle explosions
    def update_projectiles(self, screen, enemies):
        for projectile in self.projectiles[:]:  # Iterate over a copy of the list
            projectile.move()  # Move the projectile
            if isinstance(projectile, CannonProjectile) and projectile.has_hit_target():
                # Handle explosion and enemy removal
                projectile.explode(screen, enemies)
                self.projectiles.remove(projectile)  # Remove the projectile after explosion
            elif projectile.has_hit_target():
                is_dead = projectile.target.take_damage(projectile.damage)  # Apply damage to the target
                if is_dead and projectile.target in enemies:
                    enemies.remove(projectile.target)  # Remove the enemy if it is dead
                self.projectiles.remove(projectile)  # Remove the projectile after it hits
            else:
                projectile.draw(screen)  # Draw the projectile if it hasn't hit yet