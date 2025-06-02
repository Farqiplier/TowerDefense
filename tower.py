# tower.py
from projectiles import Projectile, CannonProjectile, LaserBeam
import pygame
import math


tower_menu_info = {
    "Arrow Tower": {
        "color": (255, 0, 0),  # Red color
        "price": 75
    },
    "Laser Tower": {
        "color": (0, 0, 255),  # Blue color
        "price": 150
    },
    "Cannon Tower": {
        "color": (0, 255, 0),  # Green color
        "price": 200
    },
    "Ice Tower": {
        "color": (0, 200, 255),  # Light Blue color
        "price": 200
    }
}

class Tower:
    PROJECTILE_CONFIG = {
        'damage': 1,
        'speed': 5,
        'pierce': 1,
        'lifespan': 2.0,
        'can_pop_lead': False,
        'can_pop_camo': False,
        'homing': False,
        'aoe_radius': 0
    }
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.range = 200
        self.fire_rate = 1.0  # shots per second
        self.last_shot = 0
        self.projectiles = []
        self.projectile_type = Projectile
        self.projectile_config = self.PROJECTILE_CONFIG.copy()
        
        # Visuals
        self.radius = 25
        self.color = (255, 0, 0)
        
    def find_target(self, enemies):
        """Find first enemy in range (override for different targeting)"""
        for enemy in enemies:
            dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if dist <= self.range:
                return enemy
        return None
    
    def fire(self, enemies: list, current_time: float):
        """Create projectiles if ready to fire"""
        if current_time - self.last_shot < 1.0 / self.fire_rate:
            return
            
        target = self.find_target(enemies)
        if target:
            self.create_projectile(target)
            self.last_shot = current_time
    
    def create_projectile(self, target):
        """Instantiate configured projectile type"""
        projectile = self.projectile_type(
            self.x, self.y, 
            target,
            **self.projectile_config
        )
        self.projectiles.append(projectile)
    
    def update_projectiles(self, screen, enemies: list, dt: float):
        """Update all active projectiles"""
        for proj in self.projectiles[:]:
            proj.move(dt)
            
            if proj.has_hit_target() or proj.should_expire():
                self.handle_projectile_impact(proj, enemies)
                self.projectiles.remove(proj)
            else:
                proj.draw(screen)
    
    def handle_projectile_impact(self, projectile, enemies):
        """Handle projectile hitting target or expiring"""
        if projectile.target and projectile.has_hit_target():
            projectile.target.take_damage(projectile.damage)
            projectile.apply_effects(projectile.target)
            
            # Handle AOE damage if configured
            if projectile.aoe_radius > 0 and isinstance(projectile, CannonProjectile):
                projectile.explode(None, enemies)  # Screen would be passed here
            
            # Handle pierce
            projectile.pierce -= 1
    
    def draw(self, screen, enemies: list):
        """Draw tower and range (for debugging)"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Optional: Draw range circle
        # pygame.draw.circle(screen, (100, 100, 100, 50), (int(self.x), int(self.y)), self.range, 1)

class ArrowTower(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.color = (255, 0, 0)
        self.projectile_config.update({
            'damage': 1,
            'speed': 8,
            'pierce': 3,
            'trail_length': 5
        })

class CannonTower(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.color = (0, 255, 0)
        self.fire_rate = 0.5  # Slower firing
        self.projectile_type = CannonProjectile
        self.projectile_config.update({
            'damage': 5,
            'speed': 4,
            'aoe_radius': 60,
            'explosion_radius': 80,
            'arc_height': 40,
            'trail_length': 10
        })

class LaserTower(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.color = (0, 0, 255)
        self.fire_rate = 10  # High for continuous damage
        self.damage_per_sec = 3
        self.active_laser = None
    
    def fire(self, enemies: list, current_time: float):
        target = self.find_target(enemies)
        
        if target:
            if not self.active_laser:
                self.active_laser = LaserBeam(self, target, self.damage_per_sec)
            else:
                self.active_laser.target = target
                self.active_laser.damage_per_sec = self.damage_per_sec
        else:
            self.active_laser = None
    
    def update_projectiles(self, screen, enemies: list, dt: float):
        if self.active_laser:
            self.active_laser.update(dt)
            self.active_laser.draw(screen)
            if not self.active_laser.active:
                self.active_laser = None

class IceTower(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.color = (0, 200, 255)
        self.projectile_config.update({
            'damage': 0,
            'on_hit_effects': ['slow'],
            'aoe_radius': 40,
            'color': (100, 200, 255)
        })
