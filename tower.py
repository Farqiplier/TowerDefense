from projectiles import Projectile, DartProjectile, CannonProjectile, TackProjectile, HitscanProjectile, SpikeProjectile, CrossbowProjectile, BladeProjectile, RocketProjectile
import pygame
import math
import random

tower_menu_info = {
    "Dart Monkey": {
        "color": (255, 0, 0),
        "price": 200
    },
    "Tack Shooter": {
        "color": (255, 100, 100),
        "price": 350
    },
    "Sniper Monkey": {
        "color": (100, 100, 100),
        "price": 400
    },
    "Dartling Gunner": {
        "color": (150, 75, 0),
        "price": 850,
        "radius": 35  # Visual radius in menu, potentially larger than default tower radius
    },
    "Ice Tower": {
        "color": (100, 200, 255),
        "price": 300
    },
    "Banana Farm": {
        "color": (150, 100, 0),
        "price": 1000
    },
    "Cannon Tower": {
        "color": (0, 255, 0), # This color is for the menu, actual tower is black.
        "price": 450
    }
}

# Define upgrade data for each tower
# This dictionary stores all upgrade information for each path and tier.
# Each upgrade dictionary includes a 'name', 'price', and a 'stats_effect' dictionary
# for direct attribute changes. Special effects are handled within apply_upgrade.
# Note on fire_rate_multiplier: Code applies this to 'fire_rate' (shots/sec).
# A multiplier > 1 increases fire rate (decreases cooldown).
# A multiplier < 1 decreases fire rate (increases cooldown).
# Cooldown_new = Cooldown_old / fire_rate_multiplier.
# Comments below reflect this code behavior.
UPGRADES = {
    "DartMonkey": { # Base Cooldown: 0.95s. Base Pierce: 1. Base Damage: 1.
        # Path 1: Sharp Shots / Razor Sharp Shots / Spike-o-pult
        1: {
            1: {"name": "Sharp Shots", "price": 100, "stats_effect": {'pierce': 1}}, # pierce +1
            2: {"name": "Razor Sharp Shots", "price": 150, "stats_effect": {'pierce': 2}}, # pierce +2
            3: {"name": "Spike-o-pult", "price": 400, "stats_effect": {'pierce': 22, 'fire_rate_multiplier': 1.25, 'projectile_radius': 15, 'damage': 1, 'projectile_type': 'SpikeProjectile'}}, # New projectile type, pierce +22, fire_rate x1.25 (cooldown 0.95s -> 0.76s if no other P1/P2 speed upgrades), projectile_radius set to 15, damage +1
        },
        # Path 2: Quick Shots / Very Quick Shots / Triple Shots
        2: {
            1: {"name": "Quick Shots", "price": 120, "stats_effect": {'fire_rate_multiplier': 0.85}}, # Fire_rate x0.85 (cooldown 0.95s -> 1.118s)
            2: {"name": "Very Quick Shots", "price": 180, "stats_effect": {'fire_rate_multiplier': 0.67}}, # Fire_rate x0.67 (cooldown 1.118s -> 1.668s if P2T1 taken)
            3: {"name": "Triple Shot", "price": 800, "stats_effect": {'num_projectiles': 2, 'fire_rate_multiplier': 0.75}}, # Fires 1+2=3 darts, fire_rate x0.75 (cooldown 1.668s -> 2.224s if P2T1&T2 taken)
        },
        # Path 3: Long Range Darts / Enhanced Eyesight / Crossbow
        3: {
            1: {"name": "Long Range Darts", "price": 80, "stats_effect": {'range': 8, 'projectile_lifespan_multiplier': 1.15}}, # Range +8, projectile lifespan x1.15
            2: {"name": "Enhanced Eyesight", "price": 150, "stats_effect": {'range': 8, 'projectile_speed_multiplier': 1.1, 'can_pop_camo': True}}, # Range +8, projectile speed x1.1, can_pop_camo = True
            3: {"name": "Crossbow", "price": 600, "stats_effect": {'damage': 2, 'pierce': 3, 'projectile_speed_multiplier': 1.2, 'range': 8, 'projectile_lifespan_multiplier': 1.2, 'projectile_type': 'CrossbowProjectile'}}, # Damage +2, pierce +3, projectile speed x1.2, range +8, projectile lifespan x1.2, new projectile type
        },
    },
    "TackShooter": { # Base Cooldown: 1/1.5 = 0.667s. Base Pierce: 1. Base Damage: 1. Base num_projectiles: 8.
        # Path 1: Faster Shooting / Even Faster Shooting / Tack Sprayer
        1: {
            1: {"name": "Faster Shooting", "price": 150, "stats_effect": {'fire_rate_multiplier': 0.75}}, # Fire_rate x0.75 (cooldown 0.667s -> 0.889s)
            2: {"name": "Even Faster Shooting", "price": 200, "stats_effect": {'fire_rate_multiplier': 0.5}}, # Fire_rate x0.5 (cooldown 0.889s -> 1.778s if P1T1 taken)
            3: {"name": "Tack Sprayer", "price": 800, "stats_effect": {'num_projectiles': 5, 'fire_rate_multiplier': 0.5}}, # Fires 8+5=13 tacks, fire_rate x0.5 (cooldown 1.778s -> 3.556s if P1T1&T2 taken)
        },
        # Path 2: Super Range Tacks / Even More Range Tacks / Hot Shots
        2: {
            1: {"name": "Super Range Tacks", "price": 100, "stats_effect": {'range': 20, 'projectile_lifespan_multiplier': 1.25, 'projectile_max_distance_multiplier': 1.25}}, # Range +20, lifespan x1.25, max_distance x1.25
            2: {"name": "Even More Range Tacks", "price": 150, "stats_effect": {'range': 20, 'projectile_lifespan_multiplier': 1.25, 'projectile_max_distance_multiplier': 1.25}}, # Range +20, lifespan x1.25, max_distance x1.25
            3: {"name": "Hot Shots", "price": 700, "stats_effect": {'can_pop_lead': True, 'damage': 1, 'projectile_color': (255, 100, 0)}}, # can_pop_lead = True, damage +1, projectile_color set to orange
        },
        # Path 3: Extra Pierce / More Extra Pierce / Blade Shooter
        3: {
            1: {"name": "Extra Pierce", "price": 100, "stats_effect": {'pierce': 1}}, # pierce +1
            2: {"name": "More Extra Pierce", "price": 150, "stats_effect": {'pierce': 1}}, # pierce +1
            3: {"name": "Blade Shooter", "price": 600, "stats_effect": {'pierce': 6, 'projectile_type': 'BladeProjectile', 'projectile_radius': 8, 'projectile_color': (150, 150, 150)}}, # pierce +6, new projectile type, projectile_radius set to 8, projectile_color set to grey
        },
    },
    "SniperMonkey": { # Base Cooldown: 1.2s. Base Damage: 2. Base Pierce: Assumed 1 (Hitscan).
        # Path 1: Full Metal Jacket / Deadly Precision / Maim MOAB
        1: {
            1: {"name": "Full Metal Jacket", "price": 300, "stats_effect": {'can_pop_lead': True, 'pierce': 2}}, # can_pop_lead = True, pierce +2
            2: {"name": "Deadly Precision", "price": 700, "stats_effect": {'damage': 1, 'pierce': 1, 'fire_rate_multiplier': 0.75}}, # Damage +1, pierce +1, fire_rate x0.75 (cooldown 1.2s -> 1.6s if no other P1/P2 speed upgrades)
            3: {"name": "Maim MOAB", "price": 4000, "stats_effect": {'damage': 5, 'moab_stun_duration': 2.0}}, # Damage +5, sets MOAB stun duration to 2.0s
        },
        # Path 2: Faster Firing / Even Faster Firing / Supply Drop
        2: {
            1: {"name": "Faster Firing", "price": 250, "stats_effect": {'fire_rate_multiplier': 0.8}}, # Fire_rate x0.8 (cooldown 1.2s -> 1.5s)
            2: {"name": "Even Faster Firing", "price": 400, "stats_effect": {'fire_rate_multiplier': 0.8}}, # Fire_rate x0.8 (cooldown 1.5s -> 1.875s if P2T1 taken)
            3: {"name": "Supply Drop", "price": 4000, "stats_effect": {'income_ability': 2500, 'ability_cooldown': 60}}, # Adds income ability (2500 cash) with 60s cooldown
        },
        # Path 3: Night Vision Goggles / Shrapnel Shot / Bouncing Bullet
        3: {
            1: {"name": "Night Vision Goggles", "price": 200, "stats_effect": {'can_pop_camo': True}}, # can_pop_camo = True
            2: {"name": "Shrapnel Shot", "price": 300, "stats_effect": {'shrapnel_count': 3, 'shrapnel_damage': 1, 'shrapnel_pierce': 2}}, # Adds shrapnel (3 count, 1 damage, 2 pierce)
            3: {"name": "Bouncing Bullet", "price": 1200, "stats_effect": {'bounces': 3, 'pierce': 2}}, # Adds 3 bounces, pierce +2 (to main projectile)
        },
    },
    "DartlingGunner": { # Base Cooldown: 1/4.0 = 0.25s. Base Pierce: 1. Base Damage: 1. Base num_projectiles: 1.
        # Path 1: Focused Firing / Laser Cannon / Plasma Accelerator
        1: {
            1: {"name": "Focused Firing", "price": 325, "stats_effect": {'accuracy': 0.05}}, # Accuracy set to 0.05 (lower is better)
            2: {"name": "Laser Shock", "price": 970, "stats_effect": {'damage': 1, 'pierce': 2, 'can_pop_lead': True, 'projectile_color': (255, 0, 255)}}, # Damage +1, pierce +2, can_pop_lead = True, projectile_color set to purple
            3: {"name": "Laser Cannon", "price": 3240, "stats_effect": {'damage': 2, 'pierce': 5, 'fire_rate_multiplier': 0.9}}, # Damage +2, pierce +5, fire_rate x0.9 (cooldown 0.25s -> 0.278s if no other P1/P2 speed upgrades)
        },
        # Path 2: Faster Barrel Spin / Hydra Rocket Pods / Bloon Area Denial System
        2: {
            1: {"name": "Advanced Targeting", "price": 270, "stats_effect": {'can_pop_camo': True}}, # can_pop_camo = True
            2: {"name": "Faster Barrel Spin", "price": 1025, "stats_effect": {'fire_rate_multiplier': 0.8}}, # Fire_rate x0.8 (cooldown 0.25s -> 0.313s)
            3: {"name": "Hydra Rocket Pods", "price": 5185, "stats_effect": {'num_projectiles': 1, 'aoe_radius': 25, 'damage': 2, 'projectile_type': 'RocketProjectile', 'fire_rate_multiplier': 0.7}}, # Fires 1+1=2 rockets, AOE radius +25, damage +2, new projectile type, fire_rate x0.7 (cooldown 0.313s -> 0.447s if P2T2 taken)
        },
        # Path 3: Powerful Darts / Buckshot / M.A.D
        3: {
            1: {"name": "Faster Darts", "price": 200, "stats_effect": {'projectile_speed_multiplier': 1.5}}, # Projectile speed x1.5
            2: {"name": "Powerful Darts", "price": 1295, "stats_effect": {'damage': 1, 'pierce': 1}}, # Damage +1, pierce +1
            3: {"name": "Buckshot", "price": 3670, "stats_effect": {'num_projectiles': 5, 'damage': 0.5, 'pierce': 1}}, # Fires 1+5=6 pellets, damage +0.5, pierce +1
        },
    },
    "IceTower": { # Base Cooldown: 2.5s. Base blast_damage: 1. Base range: 75.
        # Path 1: Enhanced Freeze / Permafrost / Arctic Wind
        1: {
            1: {"name": "Enhanced Freeze", "price": 150, "stats_effect": {'freeze_duration': 0.5, 'slow_factor': 0.0}}, # freeze_duration set to 0.5s, slow_factor set to 0.0 (no post-freeze slow from this)
            2: {"name": "Permafrost", "price": 250, "stats_effect": {'slow_factor': 0.4}}, # slow_factor set to 0.4 (bloons remain slowed by 40% after freeze)
            3: {"name": "Arctic Wind", "price": 2000, "stats_effect": {'range': 50, 'blast_damage': 2, 'attack_cooldown': 1.0, 'area_slow': True}}, # Range +50, blast_damage +2, attack_cooldown set to 1.0s (from 2.5s), area_slow = True
        },
        # Path 2: Cold Snap / Icicle Impale / Super Brittle
        2: {
            1: {"name": "Cold Snap", "price": 100, "stats_effect": {'can_pop_white_zebra_lead': True}}, # can_pop_white_zebra_lead = True
            2: {"name": "Icicle Impale", "price": 500, "stats_effect": {'blast_damage': 2, 'freeze_duration': 1.0, 'moab_stun_duration': 0.5}}, # blast_damage +2, freeze_duration set to 1.0s, moab_stun_duration set to 0.5s
            3: {"name": "Super Brittle", "price": 5000, "stats_effect": {'damage_vulnerable_modifier': 5}}, # Bloons take +5 damage from all sources when affected
        },
        # Path 3: Embrittlement / Absolute Zero / Snowstorm
        3: {
            1: {"name": "Embrittlement", "price": 200, "stats_effect": {'can_pop_frozen_bloons': True}}, # can_pop_frozen_bloons = True (allows sharp/shrapnel to damage frozen)
            2: {"name": "Absolute Zero", "price": 1000, "stats_effect": {'global_freeze_ability': True, 'ability_cooldown': 60, 'freeze_duration': 3.0}}, # Adds global freeze ability (60s cooldown, 3.0s freeze)
            3: {"name": "Snowstorm", "price": 3000, "stats_effect": {'attack_cooldown': 0.75, 'blast_damage': 3, 'range': 100}}, # attack_cooldown set to 0.75s, blast_damage +3, range +100
        },
    },
    "BananaFarm": { # Base banana_rate (interval): 15.0s. Base banana_value: 20.
        # Path 1: Increased Production / Greater Production / Banana Plantation
        1: {
            1: {"name": "Increased Production", "price": 300, "stats_effect": {'banana_rate': 12.0}}, # Banana interval set to 12.0s (from 15.0s)
            2: {"name": "Greater Production", "price": 400, "stats_effect": {'banana_rate': 10.0}}, # Banana interval set to 10.0s (from 12.0s)
            3: {"name": "Banana Plantation", "price": 1500, "stats_effect": {'banana_rate': 6.0, 'banana_value': 30}}, # Banana interval set to 6.0s, banana_value set to 30
        },
        # Path 2: Long Life Bananas / Banana Bank / IMF Loan
        2: {
            1: {"name": "Long Life Bananas", "price": 200, "stats_effect": {'banana_lifespan': 5.0}}, # banana_lifespan set to 5.0s (from default, likely an increase)
            2: {"name": "Banana Bank", "price": 1500, "stats_effect": {'bank_capacity': 7000, 'interest_rate': 0.1}}, # bank_capacity set to 7000, interest_rate set to 0.1 (10%)
            3: {"name": "IMF Loan", "price": 5000, "stats_effect": {'loan_ability': True, 'ability_cooldown': 60, 'loan_amount': 10000}}, # Adds loan ability (10000 cash) with 60s cooldown
        },
        # Path 3: Valuable Bananas / Central Market / Monkey Wall Street
        3: {
            1: {"name": "Valuable Bananas", "price": 200, "stats_effect": {'banana_value': 5}}, # banana_value set to 5 (Note: code sets, not adds. This is a decrease from 20)
            2: {"name": "Central Market", "price": 2000, "stats_effect": {'income_per_round': 200, 'range': 50}}, # income_per_round set to 200, range +50 (for auto-collect visualization/effect)
            3: {"name": "Monkey Wall Street", "price": 15000, "stats_effect": {'auto_collect': True, 'income_per_round': 500}}, # auto_collect = True, income_per_round set to 500
        },
    },
    "CannonTower": { # Base Cooldown: 1.4s. Base Pierce: 1. Base Damage: 1. Base AOE Radius: 75.
        # Path 1: Bigger Bombs / Heavy Bombs / Bloon Impact
        1: {
            1: {"name": "Bigger Bombs", "price": 300, "stats_effect": {'aoe_radius': 50, 'explosion_radius': 50, 'pierce': 5}}, # aoe_radius +50, explosion_radius +50, pierce +5
            2: {"name": "Heavy Bombs", "price": 400, "stats_effect": {'damage': 1, 'pierce': 10}}, # Damage +1, pierce +10
            3: {"name": "Bloon Impact", "price": 2000, "stats_effect": {'stun_duration': 1.0, 'pierce': 5}}, # stun_duration set to 1.0s, pierce +5
        },
        # Path 2: Faster Reload / Even Faster Reload / MOAB Mauler
        2: {
            1: {"name": "Faster Reload", "price": 250, "stats_effect": {'fire_rate_multiplier': 0.8}}, # Fire_rate x0.8 (cooldown 1.4s -> 1.75s)
            2: {"name": "Even Faster Reload", "price": 350, "stats_effect": {'fire_rate_multiplier': 0.8}}, # Fire_rate x0.8 (cooldown 1.75s -> 2.188s if P2T1 taken)
            3: {"name": "MOAB Mauler", "price": 2500, "stats_effect": {'damage_moab': 18, 'damage': 0}}, # damage_moab set to 18, damage +0 (no change to normal damage)
        },
        # Path 3: Missile Launcher / Mortar Monkey / Pop and Awe
        3: {
            1: {"name": "Missile Launcher", "price": 200, "stats_effect": {'projectile_speed_multiplier': 1.5, 'range': 50}}, # Projectile speed x1.5, range +50
            2: {"name": "Shattering Shells", "price": 700, "stats_effect": {'pierce_fortified': 2, 'damage_fortified': 1}}, # pierce_fortified set to 2, damage_fortified set to 1 (extra effects vs fortified)
            3: {"name": "The Big One", "price": 3000, "stats_effect": {'aoe_radius': 30, 'damage': 5, 'pierce': 10}}, # aoe_radius +30, damage +5, pierce +10
        },
    },
}

class Tower:
    PROJECTILE_CONFIG = {
        'damage': 1,
        'speed': 5,
        'pierce': 1,
        'lifespan': 2.0, # In seconds
        'can_pop_lead': False,
        'can_pop_camo': False, # Default: Cannot pop camo
        'homing': False,
        'aoe_radius': 0, # Area of Effect radius for explosive projectiles
        'radius': 5 # Default projectile visual radius
    }

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.range = 200 # Attack range of the tower
        self.base_fire_rate = 1.0 # Base shots per second, used for reference
        self.fire_rate = 1.0  # Current shots per second (attacks per second)
        self.last_shot = 0 # Time of the last shot, for cooldown calculation
        self.projectiles = [] # List of active projectiles fired by this tower
        self.projectile_type = Projectile # Class of projectile this tower fires
        self.projectile_config = self.PROJECTILE_CONFIG.copy() # Current configuration for projectiles

        # Visuals
        self.radius = 25 # Tower visual radius (size on screen)
        self.color = (255, 0, 0) # Default tower color

        # Upgrade system attributes
        self.upgrades = {1: 0, 2: 0, 3: 0} # Tracks current tier (0-3) for each path
        self.upgrades_locked_path = None # Stores which path (1, 2, or 3) is locked out after two paths are upgraded
        self.price = 0 # Base price, will be set by specific tower subclass

    def find_target(self, enemies):
        """
        Find the furthest enemy in range that the tower can pop.
        Prioritizes enemies deeper into the track (higher current_path_index).
        If multiple enemies are on the same path segment, prioritizes the one further along that segment.
        """
        furthest_enemy = None
        max_path_index = -1 # Tracks the highest path index seen so far
        max_distance_on_segment = -1.0 # Tracks progress along the current furthest segment

        for enemy in enemies:
            dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if dist <= self.range: # Check if enemy is within tower's attack range
                # Check for camo immunity: if enemy is camo and tower cannot pop camo, skip
                if enemy.is_camo and not self.projectile_config.get('can_pop_camo', False):
                    continue

                # Prioritize based on path index first (further along the track)
                if enemy.current_path_index > max_path_index:
                    furthest_enemy = enemy
                    max_path_index = enemy.current_path_index
                    # Calculate distance along the current segment for the new furthest enemy
                    if enemy.current_path_index < len(enemy.path) - 1:
                        p1 = enemy.path[enemy.current_path_index]
                        p2 = enemy.path[enemy.current_path_index + 1]
                        segment_length_sq = (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2
                        if segment_length_sq > 0: # Avoid division by zero if segment is a point
                            # Project enemy's position onto the segment to get normalized distance (0 to 1)
                            t = ((enemy.x - p1[0]) * (p2[0] - p1[0]) + (enemy.y - p1[1]) * (p2[1] - p1[1])) / segment_length_sq
                            max_distance_on_segment = t
                        else:
                            max_distance_on_segment = 0.0 # At the start of a zero-length segment
                    else: # Enemy is at the very end of the path
                        max_distance_on_segment = 1.0 # Max progress value
                elif enemy.current_path_index == max_path_index:
                    # If on the same path segment, check which is further along that segment
                    if enemy.current_path_index < len(enemy.path) - 1:
                        p1 = enemy.path[enemy.current_path_index]
                        p2 = enemy.path[enemy.current_path_index + 1]
                        segment_length_sq = (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2
                        if segment_length_sq > 0:
                            t = ((enemy.x - p1[0]) * (p2[0] - p1[0]) + (enemy.y - p1[1]) * (p2[1] - p1[1])) / segment_length_sq
                            if t > max_distance_on_segment: # If this enemy is further along the same segment
                                furthest_enemy = enemy
                                max_distance_on_segment = t
                        # else: Segment is a point, keep current furthest_enemy
                    # else: Both are at the very end, keep the first one found (or current)
        return furthest_enemy

    def fire(self, enemies: list, current_time: float):
        """
        Creates projectiles if the tower is ready to fire (cooldown passed) and a target is found.
        Passes the target's position (x, y) to the projectile.
        """
        # Fire rate is attacks per second, so cooldown is 1.0 / fire_rate
        if current_time - self.last_shot < (1.0 / self.fire_rate): # Check if cooldown has passed
            return

        target = self.find_target(enemies)
        if target:
            # Pass target's position at time of firing, not the enemy object itself (target might move)
            self.create_projectile((target.x, target.y))
            self.last_shot = current_time # Reset cooldown timer

    def create_projectile(self, target_pos: tuple):
        """
        Instantiates configured projectile type with given target position and tower's projectile_config.
        Adds the new projectile to the tower's list of active projectiles.
        """
        projectile = self.projectile_type(
            self.x, self.y, # Origin of projectile (tower's position)
            target_pos, # Target's static position at time of firing
            **self.projectile_config # Pass all projectile attributes (damage, speed, etc.)
        )
        self.projectiles.append(projectile)

    def update_projectiles(self, screen, enemies: list, dt: float):
        """
        Updates the position of all active projectiles, handles collisions,
        applies damage and effects, and removes expired projectiles.
        """
        # Iterate over a copy of the list (self.projectiles[:]) to safely remove elements during iteration
        for proj in self.projectiles[:]:
            proj.move(dt) # Update projectile's position based on delta time

            # Check for collisions with any enemy along its path
            hit_enemy = proj.check_collision(enemies)

            if hit_enemy:
                # Apply damage and effects to the hit enemy
                if hasattr(hit_enemy, 'take_damage'): # Check if enemy can take damage
                    hit_enemy.take_damage(proj.damage)
                    proj.apply_effects(hit_enemy) # Apply any special projectile effects (e.g., slow)
                proj.pierce -= 1 # Reduce pierce count after hitting an enemy

                # If it's a CannonProjectile or RocketProjectile and has an AOE radius, trigger its explosion
                if (isinstance(proj, CannonProjectile) or isinstance(proj, RocketProjectile)) and proj.aoe_radius > 0:
                    # Pass the current enemy list to the explosion to potentially damage multiple enemies
                    proj.explode(screen, enemies)

            # Remove the projectile if it has no pierce left or has expired (e.g., reached max distance/lifespan)
            if proj.should_expire():
                self.projectiles.remove(proj)
            else:
                proj.draw(screen) # Draw the projectile if it's still active

    def draw(self, screen, enemies: list): # enemies list currently unused here, but kept for consistency
        """
        Draws the tower itself on the screen.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # Optional: Draw range circle for debugging/visualisation
        # pygame.draw.circle(screen, (100, 100, 100, 50), (int(self.x), int(self.y)), self.range, 1) # 4th arg is alpha, 5th is width

    def get_upgrade_info(self, path: int, tier: int):
        """Returns the upgrade data (name, price, stats_effect) for a specific path and tier."""
        tower_upgrades = UPGRADES.get(self.__class__.__name__) # Get upgrades for this tower type
        if tower_upgrades and path in tower_upgrades and tier in tower_upgrades[path]:
            return tower_upgrades[path][tier]
        return None # Upgrade not found

    def can_upgrade(self, path: int, tier: int) -> bool:
        """
        Checks if a specific upgrade can be purchased based on game rules:
        - Tier must be valid (1, 2, or 3).
        - Path must not be locked.
        - Upgrades must be sequential (tier N requires tier N-1).
        - Path must not be at max tier (3).
        - Cannot upgrade a third path if two paths already have upgrades.
        """
        # Check if the upgrade tier is valid (1, 2, or 3)
        if not (1 <= tier <= 3):
            return False

        # Check if this path is locked due to upgrades in other paths (e.g., 5-X-X locks path 2 and 3)
        # This rule (max one path to T5, one to T2, third locked) is more complex.
        # Current rule: max two paths can have any upgrades, third is locked.
        if self.upgrades_locked_path is not None and self.upgrades_locked_path == path:
            return False # This specific path is locked

        # Check if the desired tier is exactly one level higher than the current tier on this path
        if self.upgrades[path] != tier - 1:
            return False # Must upgrade sequentially (e.g., cannot go from tier 0 to tier 2)

        # Check if the current tier is already maxed for this path
        if self.upgrades[path] == 3: # Max tier is 3 per path in this system
            return False

        # Check if any two paths already have upgrades, which would lock the third
        active_paths = [p for p, t in self.upgrades.items() if t > 0]
        if len(active_paths) == 2 and path not in active_paths:
            # If two paths are active, and the requested path is not one of them, it's locked.
            return False

        return True

    def apply_upgrade(self, path: int, tier: int):
        """
        Applies the effects of an upgrade to the tower's stats and properties.
        Also handles locking out the third path if two paths reach any upgrade tier.
        """
        upgrade_data = self.get_upgrade_info(path, tier)
        if not upgrade_data:
            print(f"Error: Upgrade data not found for {self.__class__.__name__}, path {path}, tier {tier}")
            return

        # Apply stat effects
        if "stats_effect" in upgrade_data:
            for stat, value in upgrade_data["stats_effect"].items():
                # Multiplicative fire rate changes: value > 1 means faster, value < 1 means slower.
                if stat == 'fire_rate_multiplier':
                    self.fire_rate *= value # Apply multiplier directly to current fire rate
                # Multiplicative projectile stat changes:
                # If value is 0.X (e.g., 0.1 for +10%), it's treated as (1+0.X).
                # If value is >=1.X (e.g., 1.1 for x1.1), it's treated as X.
                elif stat == 'projectile_speed_multiplier':
                    self.projectile_config['speed'] *= (1 + value) if value > 0 and value < 1 else value
                elif stat == 'projectile_lifespan_multiplier':
                    self.projectile_config['lifespan'] *= (1 + value) if value > 0 and value < 1 else value
                elif stat == 'projectile_max_distance_multiplier':
                    # Assuming 'max_distance' is a key in projectile_config if used by this upgrade
                    self.projectile_config['max_distance'] = self.projectile_config.get('max_distance', 0) * ((1 + value) if value > 0 and value < 1 else value)
                elif stat == 'banana_rate': # Banana farm specific. Value is the new interval in seconds.
                    self.banana_rate = value # Set directly
                elif stat == 'attack_cooldown': # Ice Tower specific, direct value for cooldown in seconds.
                    self.attack_cooldown = value
                # Direct additions/sets for other stats
                elif stat == 'range':
                    self.range += value
                elif stat == 'damage':
                    self.projectile_config['damage'] += value
                elif stat == 'blast_damage': # For Ice Tower's direct damage
                    self.blast_damage = getattr(self, 'blast_damage', 0) + value # Ensure blast_damage exists
                elif stat == 'pierce':
                    self.projectile_config['pierce'] += value
                elif stat == 'aoe_radius':
                    self.projectile_config['aoe_radius'] += value
                elif stat == 'explosion_radius': # Typically visual, might be same as aoe_radius
                    self.projectile_config['explosion_radius'] = self.projectile_config.get('explosion_radius', 0) + value
                elif stat == 'radius': # Tower visual radius
                    self.radius += value
                elif stat == 'projectile_radius': # Projectile visual/hitbox radius, sets the value
                    self.projectile_config['radius'] = value
                elif stat == 'color': # Tower color (for cosmetic upgrades)
                    self.color = value
                elif stat == 'projectile_color': # Projectile color
                    self.projectile_config['color'] = value # Assumes 'color' key exists or is added
                elif stat == 'can_pop_lead':
                    self.projectile_config['can_pop_lead'] = value
                elif stat == 'can_pop_camo':
                    self.projectile_config['can_pop_camo'] = value
                elif stat == 'homing':
                    self.projectile_config['homing'] = value
                elif stat == 'num_projectiles': # Adds to existing number of projectiles
                    self.num_projectiles = getattr(self, 'num_projectiles', 1) + value
                elif stat == 'accuracy': # Dartling specific, lower value means more accurate (less deviation)
                    self.accuracy = value
                elif stat == 'moab_stun_duration': # Sniper/Ice Tower specific for MOABs
                    self.moab_stun_duration = value
                elif stat == 'shrapnel_count': # Sniper specific
                    self.shrapnel_count = value
                elif stat == 'shrapnel_damage': # Sniper specific
                    self.shrapnel_damage = value
                elif stat == 'shrapnel_pierce': # Sniper specific
                    self.shrapnel_pierce = value
                elif stat == 'bounces': # Sniper specific
                    self.bounces = value
                elif stat == 'stun_duration': # Cannon/Dartling general stun
                    self.stun_duration = value
                elif stat == 'damage_moab': # Cannon/Dartling MOAB-specific damage
                    self.damage_moab = value
                elif stat == 'pierce_fortified': # Cannon, extra pierce vs fortified
                    self.pierce_fortified = value
                elif stat == 'damage_fortified': # Cannon, extra damage vs fortified
                    self.damage_fortified = value
                elif stat == 'can_pop_white_zebra_lead': # Ice Tower specific
                    self.can_pop_white_zebra_lead = value
                elif stat == 'can_pop_frozen_bloons': # Ice Tower specific
                    self.can_pop_frozen_bloons = value
                elif stat == 'freeze_duration': # Ice Tower specific, duration of freeze effect
                    self.freeze_duration = value
                elif stat == 'slow_factor': # Ice Tower specific, multiplier for speed (e.g., 0.5 for 50% speed)
                    self.slow_factor = value
                elif stat == 'damage_vulnerable_modifier': # Ice Tower, makes bloons take extra damage
                    self.damage_vulnerable_modifier = value
                elif stat == 'area_slow': # Ice Tower (Arctic Wind), continuous slow aura
                    self.area_slow = value
                elif stat == 'global_freeze_ability': # Ice Tower (Absolute Zero) ability flag
                    self.global_freeze_ability = value
                elif stat == 'ability_cooldown': # For abilities (Sniper, Ice Tower, Banana Farm)
                    self.ability_cooldown = value
                elif stat == 'income_ability': # Sniper Supply Drop, amount of income
                    self.income_ability = value
                    self.last_ability_time = pygame.time.get_ticks() / 1000.0 # Start cooldown timer
                elif stat == 'banana_value': # Banana Farm, value per banana/bundle
                    self.banana_value = value # Sets the value
                elif stat == 'banana_lifespan': # Banana Farm, how long bananas stay on screen
                    self.banana_lifespan = value
                elif stat == 'bank_capacity': # Banana Farm Bank
                    self.bank_capacity = value
                    self.current_bank_amount = 0 # Initialize bank amount when capacity is gained
                elif stat == 'interest_rate': # Banana Farm Bank interest rate
                    self.interest_rate = value
                    self.last_interest_time = pygame.time.get_ticks() / 1000.0 # Start interest timer
                elif stat == 'loan_ability': # Banana Farm IMF Loan ability flag
                    self.loan_ability = value
                    self.last_loan_time = 0 # Initialize loan cooldown
                elif stat == 'loan_amount': # Banana Farm IMF Loan amount
                    self.loan_amount = value
                elif stat == 'income_per_round': # Banana Farm Central Market/Wall Street passive income
                    self.income_per_round = value
                elif stat == 'auto_collect': # Banana Farm Monkey Wall Street auto-collection flag
                    self.auto_collect = value
                elif stat == 'projectile_type': # Change projectile class type
                    # Dynamically select projectile class based on string name
                    projectile_class_map = {
                        'SpikeProjectile': SpikeProjectile,
                        'CrossbowProjectile': CrossbowProjectile,
                        'BladeProjectile': BladeProjectile,
                        'RocketProjectile': RocketProjectile,
                        # Add other projectile types here if needed
                    }
                    self.projectile_type = projectile_class_map.get(value, self.projectile_type) # Default to current if not found
                # Add more special stat handling as needed for specific towers/upgrades

        # Increment the tier for the applied path
        self.upgrades[path] = tier

        # Check for locking of the third path: if two paths have any upgrades, the third is locked.
        active_paths = [p for p, t in self.upgrades.items() if t > 0]
        if len(active_paths) == 2 and self.upgrades_locked_path is None:
            # Find the path that is not one of the active paths
            for p_num in [1, 2, 3]: # Iterate through possible path numbers
                if p_num not in active_paths:
                    self.upgrades_locked_path = p_num
                    print(f"Path {p_num} locked for {self.__class__.__name__}") # Debug message
                    break


class CannonTower(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Cannon Tower"]["price"]
        self.color = (0, 0, 0) # Black color for cannon tower appearance
        self.range = 200 # Default attack range for bombs
        self.base_fire_rate = 1.0 / 1.4 # BTD6 base: 1.4 seconds attack cooldown (approx 0.71 shots/sec)
        self.fire_rate = self.base_fire_rate
        self.projectile_type = CannonProjectile # Uses the specialized CannonProjectile
        self.projectile_config.update({
            'damage': 1, # Base damage per explosion
            'speed': 200, # Projectile travel speed (pixels/second)
            'aoe_radius': 75, # Base Area of Effect radius for damage
            'explosion_radius': 75, # Visual explosion radius, matches AOE radius here
            'can_pop_lead': True, # Base cannon can pop lead bloons
            'radius': 8, # Visual radius of the cannonball projectile
            'pierce': 1 # Base pierce of the explosion (how many bloons it can hit)
        })
        self.num_projectiles = 1 # Base number of projectiles fired per shot (usually 1)
        # Upgrade-specific attributes, initialized to neutral values
        self.stun_duration = 0 # Duration of stun effect from upgrades
        self.damage_moab = 0 # Extra damage to MOAB-class bloons from upgrades
        self.pierce_fortified = 0 # Extra pierce against fortified bloons
        self.damage_fortified = 0 # Extra damage to fortified bloons


class DartMonkey(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Dart Monkey"]["price"]
        self.color = (255, 0, 0) # Red color for Dart Monkey appearance
        self.range = 100 # Approx range for 32 game units in BTD6
        self.base_fire_rate = 1.0 / 0.95 # BTD6 base: 0.95 seconds attack cooldown (approx 1.05 shots/sec)
        self.fire_rate = self.base_fire_rate
        self.projectile_type = DartProjectile # Uses the DartProjectile class
        self.projectile_config.update({
            'damage': 1, # Base damage per dart
            'speed': 300, # Increased speed for better visibility/effectiveness
            'pierce': 1, # Base pierce (1 bloon per dart)
            'trail_length': 0, # Dart Monkey does not have a visual trail by default
            'can_pop_lead': False, # Base Dart Monkey cannot pop lead
            'can_pop_camo': False, # Base Dart Monkey cannot pop camo
        })
        self.num_projectiles = 1 # Base number of darts fired per shot

class TackShooter(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Tack Shooter"]["price"]
        self.color = (255, 100, 100) # Pinkish color for Tack Shooter
        self.base_fire_rate = 1 # BTD6 base: 1.5 shots per second (cooldown 1/1.5 = 0.667s)
        self.fire_rate = self.base_fire_rate
        self.range = 90  # BTD6 base: 80 units (effective radius for tacks)
        self.projectile_type = TackProjectile # Uses the specialized TackProjectile
        self.projectile_config.update({
            'damage': 1, # Base damage per tack
            'speed': 300, # Speed of tacks
            'lifespan': 0.4,  # Very short lifespan for tacks in seconds
            'pierce': 1, # Base pierce per tack
            'max_distance': 80, # Very short max travel distance for tacks
            'radius': 3, # Small visual radius for tack projectile
            'can_pop_lead': False, # Base Tack Shooter cannot pop lead
            'can_pop_camo': False, # Base Tack Shooter cannot pop camo
        })
        self.num_projectiles = 8 # Base Tack Shooter fires 8 tacks in a circle

    def fire(self, enemies: list, current_time: float):
        """
        Overrides the base fire method to shoot tacks in multiple radial directions.
        Fires if any valid target (non-immune) is in range to avoid wasting shots.
        """
        if current_time - self.last_shot < (1.0 / self.fire_rate): # Check cooldown
            return

        has_valid_target = False # Flag to check if there's at least one poppable bloon in range
        for enemy in enemies:
            dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if dist <= self.range: # Check if enemy is within nominal range
                # Check if this enemy can be popped by current projectile config (e.g., camo)
                if not (enemy.is_camo and not self.projectile_config.get('can_pop_camo', False)):
                    has_valid_target = True
                    break # Found at least one valid target, no need to check further

        if has_valid_target:
            # Fire self.num_projectiles (e.g., 8 tacks) in radial directions
            for i in range(self.num_projectiles):
                angle = (360 / self.num_projectiles) * i # Calculate angle for each tack
                rad = math.radians(angle)
                # Calculate a distant target position to define the tack's direction
                target_x = self.x + math.cos(rad) * 1000 # Large distance ensures direction vector
                target_y = self.y + math.sin(rad) * 1000
                self.create_projectile((target_x, target_y)) # Create tack with this direction
            self.last_shot = current_time # Reset cooldown

class SniperMonkey(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Sniper Monkey"]["price"]
        self.color = (100, 100, 100) # Grey color for Sniper Monkey
        self.range = float('inf') # Effectively infinite range for sniper targeting
        self.base_fire_rate = 1.0 / 1.2 # BTD6 base: 1.2 seconds attack cooldown (approx 0.83 shots/sec)
        self.fire_rate = self.base_fire_rate
        self.projectile_type = HitscanProjectile # Uses the specialized HitscanProjectile (instant hit)
        self.projectile_config.update({
            'damage': 2, # BTD6 Base damage is 2
            'can_pop_lead': False, # Base sniper cannot pop lead
            'can_pop_camo': False, # Base sniper cannot pop camo
            # Hitscan projectiles don't use speed, lifespan, pierce from Tower.PROJECTILE_CONFIG in the same way
        })
        # Sniper specific upgrade attributes
        self.moab_stun_duration = 0 # Duration of MOAB stun from Maim MOAB upgrade
        self.shrapnel_count = 0 # Number of shrapnel pieces from Shrapnel Shot
        self.shrapnel_damage = 0 # Damage of shrapnel pieces
        self.shrapnel_pierce = 0 # Pierce of shrapnel pieces
        self.bounces = 0 # Number of bounces for Bouncing Bullet upgrade
        self.income_ability = 0 # Income generated by Supply Drop ability
        self.last_ability_time = 0 # Timestamp of last Supply Drop activation
        self.ability_cooldown = 0 # Cooldown for Supply Drop ability


    def find_target(self, enemies):
        """
        Finds the enemy farthest along the path, prioritizing enemies deeper into the track.
        Sniper Monkey has global range, so no distance check to self.range is needed.
        Handles camo immunity based on upgrades.
        """
        if not enemies: # No enemies to target
            return None

        furthest_enemy = None
        max_path_index = -1
        max_distance_on_segment = -1.0

        for enemy in enemies:
            # Sniper has infinite range, so no dist <= self.range check.
            # Check for camo immunity
            if enemy.is_camo and not self.projectile_config.get('can_pop_camo', False):
                continue # Skip camo enemy if sniper cannot pop camo

            # Prioritize based on path index first (further along the track)
            if enemy.current_path_index > max_path_index:
                furthest_enemy = enemy
                max_path_index = enemy.current_path_index
                # Calculate distance along the current segment for the new furthest enemy
                if enemy.current_path_index < len(enemy.path) - 1:
                    p1 = enemy.path[enemy.current_path_index]
                    p2 = enemy.path[enemy.current_path_index + 1]
                    segment_length_sq = (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2
                    if segment_length_sq > 0:
                        t = ((enemy.x - p1[0]) * (p2[0] - p1[0]) + (enemy.y - p1[1]) * (p2[1] - p1[1])) / segment_length_sq
                        max_distance_on_segment = t
                    else:
                        max_distance_on_segment = 0.0
                else: # Enemy is at the very end of the path
                    max_distance_on_segment = 1.0
            elif enemy.current_path_index == max_path_index:
                # If on the same path segment, check which is further along that segment
                if enemy.current_path_index < len(enemy.path) - 1:
                    p1 = enemy.path[enemy.current_path_index]
                    p2 = enemy.path[enemy.current_path_index + 1]
                    segment_length_sq = (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2
                    if segment_length_sq > 0:
                        t = ((enemy.x - p1[0]) * (p2[0] - p1[0]) + (enemy.y - p1[1]) * (p2[1] - p1[1])) / segment_length_sq
                        if t > max_distance_on_segment:
                            furthest_enemy = enemy
                            max_distance_on_segment = t
                    # else: Segment is a point
                # else: Both are at the very end
        return furthest_enemy


    def fire(self, enemies: list, current_time: float, screen: pygame.Surface, effects_list: list):
        """
        Overrides the fire method for instant (hitscan) damage.
        Sniper projectiles do not travel; they hit the target instantly.
        """
        if current_time - self.last_shot < (1.0 / self.fire_rate): # Check cooldown
            return

        target = self.find_target(enemies)
        if target:
            # Create a HitscanProjectile and immediately apply its hit effect
            hitscan_projectile = HitscanProjectile(self, target, **self.projectile_config) # Pass tower (self) and target
            hitscan_projectile.apply_hit(screen, effects_list) # Method to apply damage, effects, shrapnel, and add hit marker
            self.last_shot = current_time # Reset cooldown

    def update(self, enemies: list, current_time: float): # enemies list currently unused here
        """
        Handles Sniper Monkey specific updates, like the Supply Drop ability.
        Returns any income generated by abilities this frame.
        """
        income_generated = 0
        # Handle Supply Drop ability
        if self.income_ability > 0 and self.ability_cooldown > 0 and \
           current_time - getattr(self, 'last_ability_time', 0) >= self.ability_cooldown:
            # For now, just print income. In a full game, this would add to player's money.
            print(f"Sniper Supply Drop: +${self.income_ability}")
            self.last_ability_time = current_time # Reset ability cooldown timer
            income_generated = self.income_ability # Store income for game logic to handle

        # Other Sniper update logic if any (e.g., tracking debuffs on bloons) could go here.
        return income_generated # Return income for game's economy manager

    def update_projectiles(self, screen, enemies: list, dt: float):
        """
        Sniper Monkey's projectiles are hitscan (instant). They don't need continuous
        position updates or drawing like traditional projectiles. This method is empty.
        """
        pass # No projectiles to update or draw in the traditional sense

class DartlingGunner(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Dartling Gunner"]["price"]
        self.color = (150, 75, 0)  # Brown color for Dartling Gunner
        self.base_fire_rate = 4.0  # BTD6 Base: 4.0 shots per second (cooldown 0.25s)
        self.fire_rate = self.base_fire_rate
        self.range = 250 # Visual/nominal range, but aims at mouse globally
        self.projectile_type = Projectile  # Uses standard projectiles by default
        self.projectile_config.update({
            'damage': 1, # Base damage per dart
            'speed': 300, # Faster speed for dartling gunner projectiles
            'pierce': 1, # Base pierce per dart
            'aoe_radius': 0, # No AOE by default
            'radius': 4, # Smaller visual radius for darts
            'can_pop_lead': False, # Base Dartling cannot pop lead
            'can_pop_camo': False, # Base Dartling cannot pop camo (unless upgraded)
        })
        self.num_projectiles = 1 # Base number of projectiles per shot
        self.accuracy = 0.0 # 0.0 means perfect accuracy; higher means more deviation (range 0.0 to 1.0)
        # Upgrade-specific attributes
        self.stun_duration = 0 # Stun duration from upgrades
        self.damage_moab = 0 # Extra MOAB damage from upgrades

    def fire(self, mouse_pos: tuple, current_time: float): # Modified to take mouse_pos directly
        """
        Fires projectiles towards the current mouse position, with accuracy deviation.
        Dartling Gunner fires continuously as long as cooldown allows, regardless of targets under mouse.
        Projectile camo/lead popping rules still apply.
        """
        if current_time - self.last_shot < (1.0 / self.fire_rate): # Check cooldown
            return

        # Dartling Gunner fires at the mouse position
        # Apply accuracy modification (deviation from mouse pointer)
        if self.accuracy > 0:
            # Calculate random deviation based on accuracy stat
            # Deviation is scaled; accuracy 0.05 might mean up to 5 pixels deviation if 100 is the scale.
            deviation_x = self.accuracy * 100 * (2 * random.random() - 1) # Random value between -accuracy*100 and +accuracy*100
            deviation_y = self.accuracy * 100 * (2 * random.random() - 1)
            target_x = mouse_pos[0] + deviation_x
            target_y = mouse_pos[1] + deviation_y
            self.create_projectile((target_x, target_y))
        else: # Perfect accuracy if self.accuracy is 0 or less
            self.create_projectile(mouse_pos)

        self.last_shot = current_time # Reset cooldown

    # No need for find_target for Dartling Gunner as it aims at the mouse cursor.
    def find_target(self, enemies): # enemies parameter kept for polymorphism if base class expects it
        return None # Dartling Gunner does not use traditional targeting

class IceTower(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Ice Tower"]["price"]
        self.color = (100, 200, 255) # Light blue color for Ice Tower
        self.range = 75 # Approx. 40 game units in BTD6, effective radius of freeze/damage
        self.slow_factor = 0.67  # Default: slows bloons to 67% of their speed (33% slow)
        self.slow_duration = 2.0  # Default: duration of slow effect in seconds
        self.blast_damage = 1 # Initial damage for its freezing blast/aura
        self.last_attack_time = 0 # Timestamp of last attack/effect application
        self.attack_cooldown = 2.5 # Cooldown in seconds for momentary blast (base tower)

        # Ice Tower doesn't fire projectiles in the traditional sense; its effects are area-based.
        self.projectile_type = None # No projectile class used
        self.projectile_config = {} # Clear projectile config
        self.projectiles = [] # Ensure no projectiles are stored or updated

        # Ice Tower specific upgrade attributes
        self.can_pop_white_zebra_lead = False # Ability to affect normally immune bloon types
        self.can_pop_frozen_bloons = False # Ability for sharp projectiles to damage frozen bloons
        self.global_freeze_ability = False # Flag for Absolute Zero ability
        self.ability_cooldown = 0 # Cooldown for Absolute Zero
        self.last_ability_time = 0 # Timestamp of last Absolute Zero activation
        self.moab_stun_duration = 0 # Duration of stun effect on MOABs (Icicle Impale)
        self.damage_vulnerable_modifier = 0 # Extra damage taken by bloons (Super Brittle)
        self.area_slow = False # Flag for Arctic Wind continuous slow/damage aura
        self.freeze_duration = 0 # Duration of freeze effect (can be 0 if only slowing)
        self.show_blast_aura = False # Flag to draw a momentary visual for the blast effect

    def update(self, enemies: list, current_time: float, screen): # screen needed for drawing aura
        """
        Applies freezing/slowing effects and damage to enemies within its range.
        Handles Absolute Zero ability, Arctic Wind continuous effect, and
        base Ice Tower's momentary blast.
        """
        # Handle Absolute Zero ability (if active and cooldown passed)
        if self.global_freeze_ability and self.ability_cooldown > 0 and \
           current_time - getattr(self, 'last_ability_time', 0) >= self.ability_cooldown:
            print("Absolute Zero activated! Global Freeze!") # Debug message
            for enemy in enemies: # Affect all enemies on screen
                # Camo check for Absolute Zero might be desired but currently affects all.
                if not hasattr(enemy, 'original_speed'): # Store original speed if not already stored
                    enemy.original_speed = enemy.speed
                enemy.speed = 0 # Fully stop bloons
                enemy.frozen = True # Mark as frozen
                enemy.freeze_expire_time = current_time + self.freeze_duration # Set freeze expiration
                # Note: Actual damage from Absolute Zero is not implemented here, only freeze.
            self.last_ability_time = current_time # Reset ability cooldown

        # Arctic Wind - continuous effect (Tier 3 Path 1)
        if self.area_slow:
            # Damage periodically within the constant aura
            if current_time - self.last_attack_time >= self.attack_cooldown: # Cooldown for damage pulse
                for enemy in enemies:
                    dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                    if dist <= self.range: # If enemy in range
                        # Ice tower cannot pop camo by default; Arctic Wind needs to respect this too.
                        # (Assuming projectile_config['can_pop_camo'] is updated by upgrades)
                        if enemy.is_camo and not self.projectile_config.get('can_pop_camo', False):
                            continue # Skip camo bloon if not poppable
                        enemy.take_damage(self.blast_damage) # Apply damage
                self.last_attack_time = current_time # Reset damage pulse cooldown

            # Apply slow/freeze continuously for bloons inside the aura
            for enemy in enemies:
                # Handle expiration of a global freeze (like Absolute Zero) if enemy is still in Arctic Wind aura
                if hasattr(enemy, 'frozen_by_ice_tower') and enemy.frozen_by_ice_tower and current_time > getattr(enemy, 'freeze_expire_time', 0):
                    enemy.frozen = False
                    del enemy.frozen_by_ice_tower
                    if hasattr(enemy, 'freeze_expire_time'): del enemy.freeze_expire_time
                    # Reapply Arctic Wind's own slow/freeze if applicable

                dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if dist <= self.range: # If enemy in range
                    if enemy.is_camo and not self.projectile_config.get('can_pop_camo', False):
                        continue # Skip camo bloon if not poppable

                    # Apply continuous slow if not already slowed by this tower, or re-apply freeze
                    if not hasattr(enemy, 'ice_slow_active') or not enemy.ice_slow_active or enemy.ice_slow_source != self:
                        if not hasattr(enemy, 'original_speed'):
                            enemy.original_speed = enemy.speed
                        enemy.speed = enemy.original_speed * self.slow_factor # Apply slow
                        enemy.ice_slow_active = True # Mark as slowed by an ice tower
                        enemy.ice_slow_source = self # Mark which ice tower slowed it
                    # If freeze_duration is set (e.g., from Arctic Wind itself or other upgrades), apply/extend freeze
                    if self.freeze_duration > 0:
                         enemy.frozen = True
                         enemy.frozen_by_ice_tower = True # Mark that this tower is freezing it
                         enemy.freeze_expire_time = current_time + self.freeze_duration # (Re)set freeze timer
                # else: Enemy is outside the aura (handled below)

            # Clean up speeds and effects for bloons leaving the Arctic Wind aura
            for enemy in enemies:
                if hasattr(enemy, 'ice_slow_active') and enemy.ice_slow_active and enemy.ice_slow_source == self:
                    dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                    if dist > self.range: # If enemy left the aura
                        if hasattr(enemy, 'original_speed'):
                            enemy.speed = enemy.original_speed # Restore original speed
                            del enemy.original_speed
                        enemy.ice_slow_active = False
                        del enemy.ice_slow_source
                        enemy.frozen = False # Unfreeze if leaving aura
                        if hasattr(enemy, 'frozen_by_ice_tower'): del enemy.frozen_by_ice_tower
                        if hasattr(enemy, 'freeze_expire_time'): del enemy.freeze_expire_time
        else: # Momentary blast logic (base Ice Tower and upgrades that don't grant continuous aura)
            if current_time - self.last_attack_time >= self.attack_cooldown: # Check attack cooldown
                self.show_blast_aura = True # Set flag to draw aura for this frame (visual only)

                for enemy in enemies:
                    dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                    if dist <= self.range: # If enemy in range of blast
                        if enemy.is_camo and not self.projectile_config.get('can_pop_camo', False):
                            continue # Skip camo bloon if not poppable

                        enemy.take_damage(self.blast_damage) # Apply damage

                        # Apply slow effect (non-stackable by this specific tower instance for momentary blast)
                        if not hasattr(enemy, 'ice_slow_active') or not enemy.ice_slow_active: # Apply if not already slowed
                            if not hasattr(enemy, 'original_speed'):
                                enemy.original_speed = enemy.speed
                            enemy.speed = enemy.original_speed * self.slow_factor
                            enemy.ice_slow_expire_time = current_time + self.slow_duration # Set slow expiration
                            enemy.ice_slow_active = True
                            enemy.ice_slow_source = self
                        # If freeze_duration is set by upgrades, apply initial freeze
                        if self.freeze_duration > 0:
                            enemy.frozen = True
                            enemy.freeze_expire_time = current_time + self.freeze_duration # Set freeze expiration
                self.last_attack_time = current_time # Reset attack cooldown

            # Check and remove expired slow/freeze effects from momentary blasts
            for enemy in enemies:
                if hasattr(enemy, 'ice_slow_active') and enemy.ice_slow_active and enemy.ice_slow_source == self and \
                   current_time > getattr(enemy, 'ice_slow_expire_time', float('inf')): # Check slow expiration
                    if hasattr(enemy, 'original_speed'):
                        enemy.speed = enemy.original_speed # Reset speed
                        del enemy.original_speed
                    enemy.ice_slow_active = False
                    del enemy.ice_slow_source
                    # Also unfreeze if the slow duration was tied to the freeze from this momentary blast
                    if hasattr(enemy, 'freeze_expire_time') and current_time > enemy.freeze_expire_time:
                        enemy.frozen = False
                        if hasattr(enemy, 'freeze_expire_time'): del enemy.freeze_expire_time


    def draw(self, screen, enemies: list): # enemies list currently unused here
        """
        Draws the Ice Tower. If Arctic Wind is active, draw its persistent aura.
        If a momentary blast just occurred, draw a temporary blast aura.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius) # Draw tower body

        # Draw persistent aura for Arctic Wind
        if self.area_slow:
            aura_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA) # Create transparent surface
            pygame.draw.circle(aura_surface, (100, 200, 255, 50), (self.range, self.range), self.range) # Draw semi-transparent blue circle
            screen.blit(aura_surface, (int(self.x - self.range), int(self.y - self.range))) # Blit onto screen
        # Draw momentary blast aura if triggered
        elif self.show_blast_aura:
            aura_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, (100, 200, 255, 70), (self.range, self.range), self.range) # Slightly more opaque for momentary
            screen.blit(aura_surface, (int(self.x - self.range), int(self.y - self.range)))
            self.show_blast_aura = False # Reset flag after drawing for one frame


class BananaFarm(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Banana Farm"]["price"]
        self.color = (150, 100, 0) # Brown color for banana farm
        self.bananas = [] # List to store active banana objects/dictionaries
        self.last_banana_time = 0 # Timestamp of last banana generation
        self.banana_rate = 15.0  # BTD6 base: produces 4 bananas every ~15 seconds (interval in seconds)
        self.banana_value = 20 # BTD6 base: 20 money per banana (so 4 bananas = 80 money per interval)

        # Banana Farm doesn't fire projectiles, so remove/clear related configs
        self.projectile_type = None
        self.projectile_config = {}
        self.projectiles = [] # Ensure no projectiles are stored or updated

        # Banana Farm specific upgrade attributes
        self.banana_lifespan = 5.0 # How long bananas stay on screen before expiring (default)
        self.bank_capacity = 0 # Max capacity for Banana Bank
        self.current_bank_amount = 0 # Current amount stored in Banana Bank
        self.interest_rate = 0 # Interest rate for Banana Bank
        self.last_interest_time = 0 # Timestamp for last interest calculation
        self.loan_ability = False # Flag for IMF Loan ability
        self.last_loan_time = 0 # Cooldown timer for IMF Loan
        self.loan_amount = 0 # Amount of money from IMF Loan
        self.income_per_round = 0 # Passive income for Central Market/Monkey Wall Street (per second in this model)
        self.auto_collect = False # Flag for Monkey Wall Street auto-collection

    def update(self, current_time: float, mouse_pos): # mouse_pos for manual collection
        """
        Generates bananas, handles their collection (manual or auto), and manages bank/passive income.
        Returns any money earned this frame from collected bananas or passive income.
        """
        money_earned = 0

        # Handle passive income from Central Market / Monkey Wall Street (simplified to per-second)
        # This logic triggers roughly once per second if update is called frequently (e.g., 60 FPS)
        if self.income_per_round > 0 and int(current_time) > int(current_time - (1.0/60.0)): # Check if second changed
             # This is a simplified per-second income. A per-round system would be more complex.
             # For simplicity, let's assume income_per_round is actually income_per_second here.
             # A more robust way: store last_passive_income_time.
             # if current_time - self.last_passive_income_time >= 1.0:
             #    money_earned += self.income_per_round
             #    self.last_passive_income_time = current_time
             pass # Actual passive income logic might be handled at round end or differently.

        # Generate bananas if enough time has passed (based on banana_rate interval)
        if current_time - self.last_banana_time >= self.banana_rate:
            # Generate 4 bananas at/near the farm's location
            for _ in range(4): # BTD6 typically produces multiple bananas per cycle
                self.bananas.append({
                    'x': self.x + random.randint(-20, 20), # Slight random offset for visual spread
                    'y': self.y + random.randint(-20, 20),
                    'collected': False, # Flag indicating if collected
                    'spawn_time': current_time # Timestamp of spawn for lifespan check
                })
            self.last_banana_time = current_time # Reset banana generation timer

        # Update banana positions (attraction to mouse) and check for collection/expiration
        for banana in self.bananas[:]: # Iterate over a copy to allow safe removal
            if banana['collected'] or (current_time - banana['spawn_time'] > self.banana_lifespan):
                if banana['collected']:
                    money_earned += self.banana_value # Add money for collected banana
                self.bananas.remove(banana) # Remove collected or expired banana
                continue

            # Auto-collect for Monkey Wall Street upgrade
            if self.auto_collect:
                banana['collected'] = True # Mark as collected, will be processed above in next iteration/frame
                continue

            # Manual collection: Calculate distance to mouse for attraction and collection
            dx = mouse_pos[0] - banana['x']
            dy = mouse_pos[1] - banana['y']
            dist_sq = dx**2 + dy**2 # Use squared distance for efficiency

            # Attraction range: bananas move towards mouse if within this range
            # Note: 150*150 = 22500. Using squared distances avoids sqrt.
            if dist_sq < 150**2:
                dist = math.sqrt(dist_sq) # Calculate actual distance only if needed
                # Move banana towards mouse; 0.1 is attraction speed factor
                banana['x'] += dx/dist * (dist * 0.1) # Proportional move
                banana['y'] += dy/dist * (dist * 0.1)

                # Collection range: if mouse is very close, banana is collected
                if dist < 15:  # Small radius for collection
                    banana['collected'] = True
        return money_earned # Return total money earned this frame

    def draw(self, screen, enemies: list): # enemies list currently unused here
        """
        Draws the Banana Farm building and any uncollected bananas on the screen.
        """
        super().draw(screen, enemies) # Draw the base tower (farm building)
        # Draw bananas that haven't been collected
        for banana in self.bananas:
            if not banana['collected']:
                pygame.draw.circle(screen, (255, 255, 0), (int(banana['x']), int(banana['y'])), 8) # Yellow circle for banana

