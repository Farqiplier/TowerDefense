# projectiles.py
import pygame
import math
from typing import List, Optional, Dict, Any

class Projectile:
    def __init__(self, x: float, y: float, target: Any, **kwargs):
        """
        Base projectile class with all BTD6-like properties
        
        Args:
            x, y: Starting position
            target: Target enemy
            kwargs: Any projectile property (see below)
        """
        # Core properties
        self.x = x
        self.y = y
        self.target = target
        self.speed = kwargs.get('speed', 5)
        self.damage = kwargs.get('damage', 1)
        self.pierce = kwargs.get('pierce', 1)
        self.lifespan = kwargs.get('lifespan', 2.0)  # seconds
        self.age = 0
        
        # Bloon properties
        self.can_pop_lead = kwargs.get('can_pop_lead', False)
        self.can_pop_camo = kwargs.get('can_pop_camo', False)
        
        # Behavior flags
        self.homing = kwargs.get('homing', False)
        self.aoe_radius = kwargs.get('aoe_radius', 0)
        self.turn_rate = kwargs.get('turn_rate', 0.1) if self.homing else 0
        
        # Visuals
        self.color = kwargs.get('color', (255, 0, 0))
        self.radius = kwargs.get('radius', 5)
        self.trail_length = kwargs.get('trail_length', 0)
        self.trail_points = []
        
        # Special effects
        self.on_hit_effects = kwargs.get('on_hit_effects', [])
        self.spawn_on_hit = kwargs.get('spawn_on_hit', [])
        self.spawn_on_death = kwargs.get('spawn_on_death', [])
        
        # Movement
        self.velocity = self._calculate_initial_velocity()
        
    def _calculate_initial_velocity(self):
        """Calculate direction toward target"""
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = max(1, math.sqrt(dx*dx + dy*dy))
            return [dx/dist * self.speed, dy/dist * self.speed]
        return [0, 0]
    
    def move(self, dt: float):
        """Update position with optional homing behavior"""
        self.age += dt
        
        if self.homing and self.target:
            # Adjust direction toward target
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = max(1, math.sqrt(dx*dx + dy*dy))
            
            target_vx = dx/dist * self.speed
            target_vy = dy/dist * self.speed
            
            self.velocity[0] += (target_vx - self.velocity[0]) * self.turn_rate
            self.velocity[1] += (target_vy - self.velocity[1]) * self.turn_rate
            
            # Normalize
            vel_mag = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
            if vel_mag > 0:
                self.velocity[0] = self.velocity[0]/vel_mag * self.speed
                self.velocity[1] = self.velocity[1]/vel_mag * self.speed
        
        self.x += self.velocity[0] * dt * 60  # dt is in seconds, convert to frames
        self.y += self.velocity[1] * dt * 60
        
        if self.trail_length > 0:
            self.trail_points.append((self.x, self.y))
            if len(self.trail_points) > self.trail_length:
                self.trail_points.pop(0)
    
    def has_hit_target(self) -> bool:
        """Check if projectile reached target"""
        if not self.target:
            return True
            
        distance = math.sqrt((self.target.x - self.x)**2 + (self.target.y - self.y)**2)
        return distance < max(10, self.target.radius)
    
    def should_expire(self) -> bool:
        """Check if projectile should be removed"""
        return self.age >= self.lifespan or self.pierce <= 0
    
    def draw(self, screen):
        """Draw projectile with optional trail"""
        if self.trail_length > 0 and len(self.trail_points) > 1:
            pygame.draw.lines(screen, self.color, False, self.trail_points, 1)
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def apply_effects(self, enemy):
        """Apply any on-hit effects to enemy"""
        for effect in self.on_hit_effects:
            if effect == 'slow':
                enemy.speed *= 0.5  # Slow by 50%
            elif effect == 'stun':
                enemy.stun_duration = 1.0
            # Add more effects as needed

class CannonProjectile(Projectile):
    def __init__(self, x: float, y: float, target: Any, **kwargs):
        super().__init__(x, y, target, **kwargs)
        self.explosion_radius = kwargs.get('explosion_radius', 100)
        self.arc_height = kwargs.get('arc_height', 50)
        self.gravity = kwargs.get('gravity', 0.5)
        self.initial_y = y
        self.vertical_velocity = -self.arc_height  # Initial upward velocity
        
    def move(self, dt: float):
        """Arcing movement with gravity"""
        self.age += dt
        
        # Horizontal movement (same as base)
        self.x += self.velocity[0] * dt * 60
        
        # Vertical movement with gravity
        self.vertical_velocity += self.gravity
        self.y += self.vertical_velocity * dt * 60
        
        # Trail for arcing projectiles
        if self.trail_length > 0:
            self.trail_points.append((self.x, self.y))
            if len(self.trail_points) > self.trail_length:
                self.trail_points.pop(0)
    
    def explode(self, screen, enemies: List):
        """Handle AOE explosion damage"""
        if self.aoe_radius > 0:
            # Draw explosion
            pygame.draw.circle(screen, (255, 165, 0), (int(self.x), int(self.y)), self.explosion_radius, 1)
            
            # Damage all enemies in radius
            for enemy in enemies[:]:
                dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if dist <= self.explosion_radius:
                    enemy.take_damage(self.damage)
                    self.apply_effects(enemy)
        
        # Spawn sub-projectiles if configured
        for proj_config in self.spawn_on_death:
            # Implementation would create new projectiles here
            pass

class LaserBeam:
    """Special continuous damage projectile"""
    def __init__(self, source, target, damage_per_sec: float):
        self.source = source
        self.target = target
        self.damage_per_sec = damage_per_sec
        self.active = True
        self.color = (0, 0, 255)
        
    def update(self, dt: float):
        """Apply damage over time"""
        if self.target:
            self.target.take_damage(self.damage_per_sec * dt)
        else:
            self.active = False
    
    def draw(self, screen):
        if self.target:
            pygame.draw.line(screen, self.color, 
                           (self.source.x, self.source.y),
                           (self.target.x, self.target.y), 2)