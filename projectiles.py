# projectiles.py
import pygame
import math
import random
from typing import List, Optional, Dict, Any, Tuple
from enemy import Lead # Ensure Lead is imported if needed for specific checks

class Projectile:
    def __init__(self, source_tower: Any, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """
        Base projectile class with BTD6-like properties

        Args:
            source_tower: The tower instance that fired the projectile.
            x, y: Starting position
            target_pos: Position target was at when fired (static target)
            kwargs: Any projectile property like speed, damage, pierce etc.
        """
        # Core properties
        self.source_tower = source_tower # MODIFIED: Keep track of the tower that fired this
        self.x = x
        self.y = y
        self.start_pos = (x, y) 
        self.target_pos = target_pos
        self.speed = kwargs.get('speed', 5)
        self.damage = kwargs.get('damage', 1)
        self.pierce = kwargs.get('pierce', 1)
        self.max_pierce = self.pierce
        self.lifespan = kwargs.get('lifespan', 2.0)
        self.age = 0.0
        self.distance_traveled = 0.0
        self.max_distance = kwargs.get('max_distance', float('inf'))

        # Bloon properties affecting what it can pop
        self.can_pop_lead = kwargs.get('can_pop_lead', False)
        self.can_pop_camo = kwargs.get('can_pop_camo', False)

        # Behavior flags
        self.homing = kwargs.get('homing', False)
        self.aoe_radius = kwargs.get('aoe_radius', 0)
        self.turn_rate = kwargs.get('turn_rate', 0.1) if self.homing else 0.0

        # Visuals
        self.color = kwargs.get('color', (255, 0, 0))
        self.radius = kwargs.get('radius', 5)
        self.trail_length = kwargs.get('trail_length', 0)
        self.trail_points = []

        # Special effects to apply on hit
        self.on_hit_effects = kwargs.get('on_hit_effects', [])
        
        # MODIFIED: Get shrapnel properties from kwargs
        self.shrapnel_on_explode = kwargs.get('shrapnel_on_explode', False)
        self.shrapnel_count = kwargs.get('shrapnel_count', 0)
        self.shrapnel_damage = kwargs.get('shrapnel_damage', 0)
        self.shrapnel_pierce = kwargs.get('shrapnel_pierce', 0)
        
        # Movement: Initial velocity vector
        self.velocity = self._calculate_initial_velocity()
        self.direction = math.atan2(self.velocity[1], self.velocity[0])

    def _calculate_initial_velocity(self):
        """Calculate initial direction vector towards the target position."""
        dx = self.target_pos[0] - self.x
        dy = self.target_pos[1] - self.y
        dist = max(1.0, math.sqrt(dx*dx + dy*dy))
        return [dx/dist * self.speed, dy/dist * self.speed]

    def move(self, dt: float):
        """
        Update projectile's position based on its velocity and delta time (dt in seconds).
        """
        self.age += dt
        self.start_pos = (self.x, self.y) 
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.distance_traveled += self.speed * dt
        if self.trail_length > 0:
            self.trail_points.append((self.x, self.y))
            if len(self.trail_points) > self.trail_length:
                self.trail_points.pop(0)

    def check_collision(self, enemies: List[Any]) -> Optional[Any]:
        """
        Check for collision with any enemy in the provided list.
        """
        line_start = self.start_pos
        line_end = (self.x, self.y)
        if line_start == line_end:
            return None
        line_vec = (line_end[0] - line_start[0], line_end[1] - line_start[1])
        line_len_sq = line_vec[0]**2 + line_vec[1]**2
        if line_len_sq == 0:
            return None

        for enemy in enemies:
            if (isinstance(enemy, Lead) and not self.can_pop_lead) or \
               (enemy.is_camo and not self.can_pop_camo):
                continue
            enemy_vec = (enemy.x - line_start[0], enemy.y - line_start[1])
            t = (enemy_vec[0] * line_vec[0] + enemy_vec[1] * line_vec[1]) / line_len_sq
            t = max(0.0, min(1.0, t))
            closest_point_x = line_start[0] + t * line_vec[0]
            closest_point_y = line_start[1] + t * line_vec[1]
            dist_sq = (enemy.x - closest_point_x)**2 + (enemy.y - closest_point_y)**2
            combined_radius = enemy.radius + self.radius
            if dist_sq <= combined_radius**2:
                return enemy
        return None

    def should_expire(self) -> bool:
        """
        Check if the projectile should be removed from the game.
        """
        return self.pierce <= 0 or self.age >= self.lifespan or self.distance_traveled >= self.max_distance

    def draw(self, screen):
        """
        Draw the projectile on the screen.
        """
        if self.trail_length > 0 and len(self.trail_points) > 1:
            pygame.draw.lines(screen, self.color, False, self.trail_points, 1)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def apply_effects(self, enemy):
        """
        Apply any configured on-hit effects to the enemy.
        """
        for effect in self.on_hit_effects:
            if effect == 'slow':
                if not hasattr(enemy, 'original_speed'):
                    enemy.original_speed = enemy.speed
                enemy.speed = enemy.original_speed * 0.5
            elif effect == 'stun':
                enemy.stun_duration = 1.0

# --- NEW PROJECTILE CLASS ---
class ShrapnelProjectile(Projectile):
    def __init__(self, source_tower: Any, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        """ A small fragment that flies out from an impact. """
        super().__init__(source_tower, x, y, target_pos, **kwargs)
        self.rotation_angle = random.randint(0, 359)
        self.rotation_speed = random.randint(-180, 180)
        # Randomize the shape and color slightly for a "broken parts" look
        self.w = random.randint(3, 6)
        self.h = random.randint(3, 6)
        c = random.randint(80, 120)
        self.color = (c, c, c)

    def move(self, dt: float):
        super().move(dt)
        self.rotation_angle = (self.rotation_angle + self.rotation_speed * dt) % 360

    def draw(self, screen):
        """ Draws a small, rotating grey square/rectangle. """
        frag_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        frag_surface.fill(self.color)
        rotated_surface = pygame.transform.rotate(frag_surface, self.rotation_angle)
        new_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_surface, new_rect)

class DartProjectile(Projectile):
    def __init__(self, source_tower: Any, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        super().__init__(source_tower, x, y, target_pos, **kwargs)

class TackProjectile(Projectile):
    def __init__(self, source_tower: Any, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        super().__init__(source_tower, x, y, target_pos, **kwargs)

class CannonProjectile(Projectile):
    def __init__(self, source_tower: Any, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        super().__init__(source_tower, x, y, target_pos, **kwargs)
        self.explosion_radius = kwargs.get('explosion_radius', 80)

    def move(self, dt: float):
        super().move(dt)

    def explode(self, screen, enemies: List[Any]):
        """ Handles the AOE explosion and now also spawns shrapnel if upgraded. """
        if self.aoe_radius > 0:
            pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.explosion_radius, 2)
            for enemy in enemies:
                dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if dist <= self.aoe_radius:
                    if enemy.is_camo and not self.can_pop_camo:
                        continue
                    enemy.take_damage(self.damage)
                    self.apply_effects(enemy)
        
        # --- FIXED: Spawn shrapnel from explosion ---
        if self.shrapnel_on_explode and self.shrapnel_count > 0:
            for _ in range(self.shrapnel_count):
                angle = random.uniform(0, 2 * math.pi)
                # Define a target point for the shrapnel to fly towards
                shrapnel_target_x = self.x + math.cos(angle) * 100
                shrapnel_target_y = self.y + math.sin(angle) * 100
                
                shrapnel = ShrapnelProjectile(
                    self.source_tower,
                    self.x, self.y,
                    (shrapnel_target_x, shrapnel_target_y),
                    damage=self.shrapnel_damage,
                    pierce=self.shrapnel_pierce,
                    speed=250, # Shrapnel has its own speed
                    lifespan=0.5 # And lifespan
                )
                self.source_tower.projectiles.append(shrapnel)

class HitscanProjectile:
    def __init__(self, source: Any, target: Any, **kwargs):
        self.source = source
        self.target = target
        self.damage = kwargs.get('damage', 1)
        self.can_pop_lead = kwargs.get('can_pop_lead', False)
        self.can_pop_camo = kwargs.get('can_pop_camo', False)
        self.on_hit_effects = kwargs.get('on_hit_effects', [])
        self.hit_line_color = kwargs.get('hit_line_color', (200,200,200))
        # MODIFIED: Get shrapnel properties from kwargs
        self.shrapnel_count = kwargs.get('shrapnel_count', 0)
        self.shrapnel_damage = kwargs.get('shrapnel_damage', 0)
        self.shrapnel_pierce = kwargs.get('shrapnel_pierce', 0)

    def apply_hit(self, screen: pygame.Surface, effects_list: list):
        """ Immediately apply damage, effects, and now SPAWNS SHRAPNEL. """
        if self.target:
            can_damage_target = True
            if (isinstance(self.target, Lead) and not self.can_pop_lead) or \
               (self.target.is_camo and not self.can_pop_camo):
                can_damage_target = False

            if can_damage_target:
                self.target.take_damage(self.damage)
                for effect in self.on_hit_effects:
                    # (effect logic remains the same)
                    pass
                
                effects_list.append({
                    'type': 'hit_marker',
                    'pos': (self.target.x, self.target.y),
                    'color': (255, 255, 0),
                    'radius': 3,
                    'creation_time': pygame.time.get_ticks() / 1000.0,
                    'duration': 0.15
                })

                # --- FIXED: Spawn shrapnel on hit ---
                if self.shrapnel_count > 0:
                    for _ in range(self.shrapnel_count):
                        angle = random.uniform(0, 2 * math.pi)
                        shrapnel_target_x = self.target.x + math.cos(angle) * 100
                        shrapnel_target_y = self.target.y + math.sin(angle) * 100
                        
                        shrapnel = ShrapnelProjectile(
                            self.source, # The source tower
                            self.target.x, self.target.y, # Start from the hit bloon
                            (shrapnel_target_x, shrapnel_target_y),
                            damage=self.shrapnel_damage,
                            pierce=self.shrapnel_pierce,
                            speed=250,
                            lifespan=0.5
                        )
                        # Add shrapnel to its tower's main projectile list to be updated and drawn
                        self.source.projectiles.append(shrapnel)

class SpikeProjectile(Projectile):
    def __init__(self, source_tower: Any, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        super().__init__(source_tower, x, y, target_pos, **kwargs)
        self.radius = kwargs.get('radius', 15)
        self.color = kwargs.get('color', (100, 50, 0))
        self.pierce = kwargs.get('pierce', 22)
        self.rotation_angle = 0
        self.rotation_speed = 180

    def move(self, dt: float):
        super().move(dt)
        self.rotation_angle = (self.rotation_angle + self.rotation_speed * dt) % 360

    def draw(self, screen):
        size = self.radius * 2
        spike_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (self.radius, self.radius)
        pygame.draw.circle(spike_surface, (128, 128, 128), center, self.radius * 0.7)
        pygame.draw.circle(spike_surface, (80, 80, 80), center, self.radius * 0.7, 1)
        num_spikes = 8
        for i in range(num_spikes):
            angle = (i / num_spikes) * 2 * math.pi
            outer_point = (center[0] + self.radius * math.cos(angle), center[1] + self.radius * math.sin(angle))
            angle_left, angle_right = angle - 0.2, angle + 0.2
            inner_base_l = (center[0] + self.radius * 0.6 * math.cos(angle_left), center[1] + self.radius * 0.6 * math.sin(angle_left))
            inner_base_r = (center[0] + self.radius * 0.6 * math.cos(angle_right), center[1] + self.radius * 0.6 * math.sin(angle_right))
            pygame.draw.polygon(spike_surface, (128, 128, 128), [outer_point, inner_base_l, inner_base_r])
            pygame.draw.polygon(spike_surface, (80, 80, 80), [outer_point, inner_base_l, inner_base_r], 1)
        rotated_surface = pygame.transform.rotate(spike_surface, self.rotation_angle)
        new_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_surface, new_rect)

class CrossbowProjectile(Projectile):
    def __init__(self, source_tower: Any, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        super().__init__(source_tower, x, y, target_pos, **kwargs)
        self.speed = kwargs.get('speed', 400)
        self.damage = kwargs.get('damage', 3)
        self.pierce = kwargs.get('pierce', 4)
        self.lifespan = kwargs.get('lifespan', 3.0)
        self.max_distance = kwargs.get('max_distance', float('inf'))
        self.color = kwargs.get('color', (50, 50, 50))
        self.radius = kwargs.get('radius', 6)

    def draw(self, screen):
        bolt_len, bolt_width, center_y = 20, 4, 10
        bolt_surface = pygame.Surface((bolt_len, bolt_len), pygame.SRCALPHA)
        shaft_color = (80, 54, 41)
        pygame.draw.line(bolt_surface, shaft_color, (0, center_y), (bolt_len - 4, center_y), bolt_width)
        head_color = (100, 100, 100)
        head_points = [(bolt_len - 5, center_y - 4), (bolt_len, center_y), (bolt_len - 5, center_y + 4)]
        pygame.draw.polygon(bolt_surface, head_color, head_points)
        pygame.draw.line(bolt_surface, shaft_color, (0, center_y-2), (4, center_y-4), 2)
        pygame.draw.line(bolt_surface, shaft_color, (0, center_y+2), (4, center_y+4), 2)
        angle = -math.degrees(self.direction)
        rotated_surface = pygame.transform.rotate(bolt_surface, angle)
        new_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_surface, new_rect)

class BladeProjectile(Projectile):
    def __init__(self, source_tower: Any, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        super().__init__(source_tower, x, y, target_pos, **kwargs)
        self.radius = kwargs.get('radius', 8)
        self.color = kwargs.get('color', (150, 150, 150))
        self.pierce = kwargs.get('pierce', 6)
        self.rotation_angle = 0
        self.rotation_speed = 360

    def move(self, dt: float):
        super().move(dt)
        self.rotation_angle = (self.rotation_angle + self.rotation_speed * dt) % 360

    def draw(self, screen):
        size, center = self.radius * 2.5, self.radius * 1.25
        blade_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        blade_color, blade_outline = (192, 192, 192), (105, 105, 105)
        blade1_rect, blade2_rect = pygame.Rect(0, center - 2, size, 4), pygame.Rect(center - 2, 0, 4, size)
        pygame.draw.rect(blade_surface, blade_color, blade1_rect)
        pygame.draw.rect(blade_surface, blade_color, blade2_rect)
        pygame.draw.rect(blade_surface, blade_outline, blade1_rect, 1)
        pygame.draw.rect(blade_surface, blade_outline, blade2_rect, 1)
        rotated_surface = pygame.transform.rotate(blade_surface, self.rotation_angle)
        new_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_surface, new_rect)

class RocketProjectile(Projectile):
    def __init__(self, source_tower: Any, x: float, y: float, target_pos: Tuple[float, float], **kwargs):
        super().__init__(source_tower, x, y, target_pos, **kwargs)
        self.aoe_radius = kwargs.get('aoe_radius', 25)
        self.damage = kwargs.get('damage', 2)
        self.color = kwargs.get('color', (200, 50, 0))
        self.radius = kwargs.get('radius', 8)
        self.trail_length = kwargs.get('trail_length', 10)

    def draw(self, screen):
        acid_green, black = (124, 252, 0), (0, 0, 0)
        rocket_len, rocket_h = 20, 12
        rocket_surface = pygame.Surface((rocket_len, rocket_h), pygame.SRCALPHA)
        body_rect = pygame.Rect(0, 3, 14, 6)
        pygame.draw.rect(rocket_surface, black, body_rect)
        nose_points = [(13, 0), (rocket_len, rocket_h / 2), (13, rocket_h)]
        pygame.draw.polygon(rocket_surface, acid_green, nose_points)
        pygame.draw.polygon(rocket_surface, black, nose_points, 1)
        pygame.draw.line(rocket_surface, acid_green, (0, 3), (4, 0), 2)
        pygame.draw.line(rocket_surface, acid_green, (0, 9), (4, 12), 2)
        pygame.draw.line(rocket_surface, black, (0, 3), (4, 0), 1)
        pygame.draw.line(rocket_surface, black, (0, 9), (4, 12), 1)
        angle = -math.degrees(self.direction)
        rotated_surface = pygame.transform.rotate(rocket_surface, angle)
        new_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_surface, new_rect)

    def check_collision(self, enemies: List[Any]) -> Optional[Any]:
        hit_enemy = super().check_collision(enemies)
        if hit_enemy:
            self.explode(pygame.display.get_surface(), enemies)
        return hit_enemy
    
    def explode(self, screen, enemies: List[Any]):
        if self.aoe_radius > 0:
            pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y)), self.aoe_radius, 2)
            for enemy in enemies:
                dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if dist <= self.aoe_radius:
                    if enemy.is_camo and not self.can_pop_camo:
                        continue
                    enemy.take_damage(self.damage)
                    self.apply_effects(enemy)