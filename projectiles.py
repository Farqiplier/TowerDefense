# projectiles.py
import pygame
import math
from typing import List, Optional, Dict, Any, Tuple
from enemy import Lead # Ensure Lead is imported if needed for specific checks

class Projectile:
    def __init__(self, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """
        Base projectile class with BTD6-like properties

        Args:
            x, y: Starting position
            target_pos: Position target was at when fired (static target)
            kwargs: Any projectile property like speed, damage, pierce etc.
        """
        # Core properties
        self.x = x
        self.y = y
        # Initial start_pos is set when projectile is created
        self.start_pos = (x, y) 
        self.target_pos = target_pos  # Stores position target was at when fired
        self.speed = kwargs.get('speed', 5) # Speed in pixels per second
        self.damage = kwargs.get('damage', 1)
        self.pierce = kwargs.get('pierce', 1)
        self.max_pierce = self.pierce # Keep original pierce count
        self.lifespan = kwargs.get('lifespan', 2.0)  # seconds
        self.age = 0.0 # Current age of the projectile in seconds
        self.distance_traveled = 0.0 # Total distance moved
        self.max_distance = kwargs.get('max_distance', float('inf')) # Max distance before expiring

        # Bloon properties affecting what it can pop
        self.can_pop_lead = kwargs.get('can_pop_lead', False)
        self.can_pop_camo = kwargs.get('can_pop_camo', False)

        # Behavior flags
        self.homing = kwargs.get('homing', False) # True if projectile tracks moving targets
        self.aoe_radius = kwargs.get('aoe_radius', 0) # Area of Effect radius
        self.turn_rate = kwargs.get('turn_rate', 0.1) if self.homing else 0.0 # How fast homing projectiles can turn

        # Visuals
        self.color = kwargs.get('color', (255, 0, 0)) # Default red color
        self.radius = kwargs.get('radius', 5) # Visual radius for drawing
        self.trail_length = kwargs.get('trail_length', 0) # Number of past positions to store for a trail
        self.trail_points = [] # List to store trail coordinates

        # Special effects to apply on hit
        self.on_hit_effects = kwargs.get('on_hit_effects', [])
        # Projectiles to spawn on hit (e.g., sticky bomb)
        self.spawn_on_hit = kwargs.get('spawn_on_hit', [])
        # Projectiles/effects to spawn when projectile expires/dies
        self.spawn_on_death = kwargs.get('spawn_on_death', [])

        # Movement: Initial velocity vector
        self.velocity = self._calculate_initial_velocity()
        self.direction = math.atan2(self.velocity[1], self.velocity[0]) # Angle of movement

    def _calculate_initial_velocity(self):
        """Calculate initial direction vector towards the target position."""
        dx = self.target_pos[0] - self.x
        dy = self.target_pos[1] - self.y
        dist = max(1.0, math.sqrt(dx*dx + dy*dy)) # Avoid division by zero
        return [dx/dist * self.speed, dy/dist * self.speed] # velocity components (pixels per second)

    def move(self, dt: float):
        """
        Update projectile's position based on its velocity and delta time (dt in seconds).
        If homing, adjust velocity towards the current target.
        """
        self.age += dt # Increase age
        
        # Store current position as the start of the segment for collision detection in this frame
        self.start_pos = (self.x, self.y) 

        # Update position based on velocity (pixels/second) and dt (seconds)
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

        # Update distance traveled
        self.distance_traveled += self.speed * dt # Distance is speed * time

        # Update trail points if trail_length is configured
        if self.trail_length > 0:
            self.trail_points.append((self.x, self.y))
            if len(self.trail_points) > self.trail_length:
                self.trail_points.pop(0) # Remove oldest point if trail is too long

    def check_collision(self, enemies: List[Any]) -> Optional[Any]:
        """
        Check for collision with any enemy in the provided list.
        Uses line-circle intersection for accurate path collision.
        Returns the first enemy hit (and valid) or None.
        """
        # Define the line segment for collision check
        line_start = self.start_pos # Projectile's starting point for this frame's movement
        line_end = (self.x, self.y) # Projectile's current (end) point for this frame's movement

        # If the projectile hasn't moved yet in this frame, no line segment exists for collision
        if line_start == line_end:
            return None

        # Calculate vector for the line segment
        line_vec = (line_end[0] - line_start[0], line_end[1] - line_start[1])
        line_len_sq = line_vec[0]**2 + line_vec[1]**2
        if line_len_sq == 0: # Line has zero length, no collision possible (should be caught by line_start == line_end)
            return None

        for enemy in enemies:
            # Skip if the enemy cannot be popped by this projectile type
            # Check enemy.is_camo directly from the enemy object
            if (isinstance(enemy, Lead) and not self.can_pop_lead) or \
               (enemy.is_camo and not self.can_pop_camo): # Use enemy.is_camo directly
                continue

            # Vector from line start to enemy center
            enemy_vec = (enemy.x - line_start[0], enemy.y - line_start[1])

            # Calculate the projection of enemy_vec onto line_vec
            t = (enemy_vec[0] * line_vec[0] + enemy_vec[1] * line_vec[1]) / line_len_sq

            # Clamp t to [0, 1] to ensure the closest point is within the line segment
            t = max(0.0, min(1.0, t))

            # Find the closest point on the line segment to the enemy center
            closest_point_x = line_start[0] + t * line_vec[0]
            closest_point_y = line_start[1] + t * line_vec[1]

            # Calculate distance from the closest point to the enemy center
            dist_sq = (enemy.x - closest_point_x)**2 + (enemy.y - closest_point_y)**2
            combined_radius = enemy.radius + self.radius

            # If distance is within combined radii, a collision occurred
            if dist_sq <= combined_radius**2:
                return enemy # Return the enemy that was hit
        return None # No collision found

    def should_expire(self) -> bool:
        """
        Check if the projectile should be removed from the game (e.g., out of pierce,
        reached max age, or traveled max distance).
        """
        return self.pierce <= 0 or self.age >= self.lifespan or self.distance_traveled >= self.max_distance

    def draw(self, screen):
        """
        Draw the projectile on the screen, including its trail if configured.
        """
        # Draw projectile trail
        if self.trail_length > 0 and len(self.trail_points) > 1:
            pygame.draw.lines(screen, self.color, False, self.trail_points, 1)

        # Draw the projectile itself
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def apply_effects(self, enemy):
        """
        Apply any configured on-hit effects to the enemy.
        """
        for effect in self.on_hit_effects:
            if effect == 'slow':
                # Apply slow effect, store original speed if not already done
                if not hasattr(enemy, 'original_speed'):
                    enemy.original_speed = enemy.speed
                enemy.speed = enemy.original_speed * 0.5 # Halve speed
            elif effect == 'stun':
                # Apply stun effect (e.g., set a stun duration)
                enemy.stun_duration = 1.0 # Stun for 1 second

class DartProjectile(Projectile):
    def __init__(self, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """
        A basic dart projectile, fast and single target.
        """
        super().__init__(x, y, target_pos, **kwargs) # Pass all kwargs to super

class TackProjectile(Projectile):
    # Constructor updated to match the base Projectile signature
    def __init__(self, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """
        A short-range projectile for the Tack Shooter, fired in radial patterns.
        The target_pos is calculated by the TackShooter itself to determine direction.
        """
        # Pass all kwargs to the superclass. Specific properties are set in tower.py's config.
        super().__init__(x, y, target_pos, **kwargs)

class CannonProjectile(Projectile):
    # Constructor updated to correctly handle kwargs without conflicts and simplify behavior
    def __init__(self, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """
        A large, black projectile that deals AOE damage upon impact.
        Simplified to move in a straight line, without arcing.
        """
        # Pass all properties via kwargs to the superclass.
        super().__init__(x, y, target_pos, **kwargs)
        # Ensure specific properties are retrieved from kwargs, or use default if not provided
        self.explosion_radius = kwargs.get('explosion_radius', 80)
        self.aoe_radius = kwargs.get('aoe_radius', 0) 

    def move(self, dt: float):
        """
        Cannon projectile now moves in a straight line, like a regular projectile.
        No custom arc trajectory.
        """
        super().move(dt) # Call the base Projectile's move method

    def explode(self, screen, enemies: List[Any]):
        """
        Handles the Area of Effect (AOE) explosion damage for the cannon projectile.
        """
        print(f"CannonProjectile.explode() called at ({self.x}, {self.y}) with AOE Radius: {self.aoe_radius}, Damage: {self.damage}")
        if self.aoe_radius > 0:
            # Draw a visual representation of the explosion
            pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.explosion_radius, 2) # Orange outline

            # Damage all enemies within the explosion radius
            for enemy in enemies:
                dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if dist <= self.aoe_radius: # Use aoe_radius for damage application
                    # Check camo immunity for explosion damage as well
                    if enemy.is_camo and not self.can_pop_camo:
                        print(f"  Skipping camo enemy {enemy.bloon_type} (ID: {id(enemy)}) in explosion.")
                        continue # Skip camo bloon if projectile can't pop camo

                    print(f"  Enemy {enemy.bloon_type} (ID: {id(enemy)}) in range, health before: {enemy.health}")
                    enemy.take_damage(self.damage)
                    self.apply_effects(enemy) # Apply effects from the cannon shot
                    print(f"  Enemy {enemy.bloon_type} (ID: {id(enemy)}) health after: {enemy.health}")

class HitscanProjectile:
    """
    Special projectile type for instant hits (e.g., Sniper Monkey).
    It does not move; it applies damage immediately upon creation.
    """
    def __init__(self, source: Any, target: Any, **kwargs):
        self.source = source # The tower that fired it
        self.target = target # The enemy hit
        self.damage = kwargs.get('damage', 1)
        self.can_pop_lead = kwargs.get('can_pop_lead', False)
        self.can_pop_camo = kwargs.get('can_pop_camo', False)
        self.on_hit_effects = kwargs.get('on_hit_effects', [])

    def apply_hit(self):
        """
        Immediately apply damage and effects to the target.
        This is called directly by the tower, not in a projectile update loop.
        """
        if self.target:
            # Check if the target can be popped by this hitscan type
            if (isinstance(self.target, Lead) and not self.can_pop_lead) or \
               (self.target.is_camo and not self.can_pop_camo): # Use self.target.is_camo directly
                # If target can't be popped, no damage/effects are applied
                return

            self.target.take_damage(self.damage)
            for effect in self.on_hit_effects:
                if effect == 'slow':
                    if not hasattr(self.target, 'original_speed'):
                        self.target.original_speed = self.target.speed
                    self.target.speed = self.target.original_speed * 0.5
                elif effect == 'stun':
                    self.target.stun_duration = 1.0

class SpikeProjectile(Projectile):
    def __init__(self, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """
        A large, sharp spike projectile fired by the Spike-o-pult.
        Has high pierce and can pop multiple bloons.
        """
        super().__init__(x, y, target_pos, **kwargs)
        self.radius = kwargs.get('radius', 15) # Larger radius for visual representation
        self.color = kwargs.get('color', (100, 50, 0)) # Brownish color for spike
        self.pierce = kwargs.get('pierce', 22) # Base pierce for Spike-o-pult (22 with upgrades)

class CrossbowProjectile(Projectile):
    def __init__(self, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """
        A fast, long-range, high-damage projectile fired by the Crossbow.
        """
        super().__init__(x, y, target_pos, **kwargs)
        self.speed = kwargs.get('speed', 400) # Faster speed
        self.damage = kwargs.get('damage', 3) # Higher damage (1 base + 2 from upgrade)
        self.pierce = kwargs.get('pierce', 4) # Higher pierce (1 base + 3 from upgrade)
        self.lifespan = kwargs.get('lifespan', 3.0) # Longer lifespan
        self.max_distance = kwargs.get('max_distance', float('inf')) # Effectively infinite range
        self.color = kwargs.get('color', (50, 50, 50)) # Dark color for crossbow bolt
        self.radius = kwargs.get('radius', 6) # Moderate radius

class BladeProjectile(Projectile):
    def __init__(self, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """
        A blade projectile fired by the Tack Shooter (Blade Shooter upgrade).
        Rotates and has high pierce.
        """
        super().__init__(x, y, target_pos, **kwargs)
        self.radius = kwargs.get('radius', 8) # Visual radius
        self.color = kwargs.get('color', (150, 150, 150)) # Grayish color
        self.pierce = kwargs.get('pierce', 6) # High pierce
        self.rotation_angle = 0
        self.rotation_speed = 360 # degrees per second

    def move(self, dt: float):
        super().move(dt)
        self.rotation_angle = (self.rotation_angle + self.rotation_speed * dt) % 360

    def draw(self, screen):
        # Draw a simple rotating cross or square to represent the blade
        temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, self.color, (self.radius, self.radius), self.radius) # Base circle
        pygame.draw.line(temp_surface, (0, 0, 0), (self.radius, 0), (self.radius, self.radius * 2), 2) # Cross
        pygame.draw.line(temp_surface, (0, 0, 0), (0, self.radius), (self.radius * 2, self.radius), 2)

        rotated_surface = pygame.transform.rotate(temp_surface, self.rotation_angle)
        new_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_surface, new_rect)


class RocketProjectile(Projectile):
    def __init__(self, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """
        A rocket projectile fired by the Dartling Gunner (Hydra Rocket Pods upgrade).
        Has AOE damage.
        """
        super().__init__(x, y, target_pos, **kwargs)
        self.aoe_radius = kwargs.get('aoe_radius', 25) # AOE radius
        self.damage = kwargs.get('damage', 2) # Higher damage (base 1 + 2 from upgrade)
        self.color = kwargs.get('color', (200, 50, 0)) # Orangish-red for rocket
        self.radius = kwargs.get('radius', 8) # Larger visual
        self.trail_length = kwargs.get('trail_length', 10) # Visible trail for rockets

    def check_collision(self, enemies: List[Any]) -> Optional[Any]:
        """
        For rockets, collision acts like a CannonProjectile's explosion on first hit.
        It hits one, then explodes to damage others.
        """
        hit_enemy = super().check_collision(enemies)
        if hit_enemy:
            # When a rocket hits, it "explodes" in a small AOE
            self.explode(pygame.display.get_surface(), enemies) # Get current screen surface
        return hit_enemy
    
    def explode(self, screen, enemies: List[Any]):
        """
        Handles the Area of Effect (AOE) explosion damage for the rocket projectile.
        """
        if self.aoe_radius > 0:
            # Draw a visual representation of the explosion (small burst)
            pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y)), self.aoe_radius, 2) # Yellow outline

            # Damage all enemies within the explosion radius
            for enemy in enemies:
                dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if dist <= self.aoe_radius:
                    if enemy.is_camo and not self.can_pop_camo:
                        continue # Skip camo bloon if projectile can't pop camo
                    
                    enemy.take_damage(self.damage)
                    self.apply_effects(enemy) # Apply effects from the rocket hit
