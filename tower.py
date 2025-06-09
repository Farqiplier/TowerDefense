from projectiles import Projectile, DartProjectile, CannonProjectile, TackProjectile, HitscanProjectile
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
        "price": 500,
        "radius": 35  # Bigger than normal
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
        "color": (0, 255, 0),
        "price": 450
    }
}

# Define upgrade data for each tower
# This dictionary stores all upgrade information for each path and tier.
# Each upgrade dictionary includes a 'name', 'price', and a 'stats_effect' dictionary
# for direct attribute changes. Special effects are handled within apply_upgrade.
UPGRADES = {
    "Dart Monkey": {
        # Path 1: Sharp Shots / Razor Sharp Shots / Spike-o-pult
        1: {
            1: {"name": "Sharp Shots", "price": 100, "stats_effect": {'pierce': 1}}, # Total pierce 2 -> 3
            2: {"name": "Razor Sharp Shots", "price": 150, "stats_effect": {'pierce': 2}}, # Total pierce 3 -> 5
            3: {"name": "Spike-o-pult", "price": 400, "stats_effect": {'pierce': 17, 'fire_rate_multiplier': 1.15, 'projectile_radius': 15, 'damage': 1, 'projectile_type': 'SpikeProjectile'}}, # New projectile type, total pierce 5 -> 22, attack speed 0.95s -> 1.15s, +1 damage
        },
        # Path 2: Quick Shots / Very Quick Shots / Triple Shots
        2: {
            1: {"name": "Quick Shots", "price": 120, "stats_effect": {'fire_rate_multiplier': 0.85}}, # 15% faster (0.95 -> 0.8075)
            2: {"name": "Very Quick Shots", "price": 180, "stats_effect": {'fire_rate_multiplier': 0.67}}, # 33% faster (0.8075 -> 0.456)
            3: {"name": "Triple Shot", "price": 800, "stats_effect": {'num_projectiles': 3, 'fire_rate_multiplier': 0.75}}, # Fires 3 darts, attack speed 0.456 -> 0.606
        },
        # Path 3: Long Range Darts / Enhanced Eyesight / Crossbow
        3: {
            1: {"name": "Long Range Darts", "price": 80, "stats_effect": {'range': 8, 'projectile_lifespan_multiplier': 1.15}}, # Increased range by 8 units, lifespan 15%
            2: {"name": "Enhanced Eyesight", "price": 150, "stats_effect": {'range': 8, 'projectile_speed_multiplier': 1.1, 'can_pop_camo': True}}, # Increased range by 8 units, speed 10%, camo
            3: {"name": "Crossbow", "price": 600, "stats_effect": {'damage': 2, 'pierce': 3, 'projectile_speed_multiplier': 1.2, 'range': 8, 'projectile_lifespan_multiplier': 1.2, 'projectile_type': 'CrossbowProjectile'}}, # Damage +2, pierce +3, speed +20%, range +8, lifespan +20%
        },
    },
    "Tack Shooter": {
        # Path 1: Faster Shooting / Even Faster Shooting / Tack Sprayer
        1: {
            1: {"name": "Faster Shooting", "price": 150, "stats_effect": {'fire_rate_multiplier': 0.75}}, # Faster
            2: {"name": "Even Faster Shooting", "price": 200, "stats_effect": {'fire_rate_multiplier': 0.5}}, # Even faster (relative to base)
            3: {"name": "Tack Sprayer", "price": 800, "stats_effect": {'num_projectiles': 5, 'fire_rate_multiplier': 0.5}}, # Fires 8+5=13 tacks, faster attack (relative to base)
        },
        # Path 2: Super Range Tacks / Even More Range Tacks / Hot Shots
        2: {
            1: {"name": "Super Range Tacks", "price": 100, "stats_effect": {'range': 20, 'projectile_lifespan_multiplier': 1.25, 'projectile_max_distance_multiplier': 1.25}},
            2: {"name": "Even More Range Tacks", "price": 150, "stats_effect": {'range': 20, 'projectile_lifespan_multiplier': 1.25, 'projectile_max_distance_multiplier': 1.25}},
            3: {"name": "Hot Shots", "price": 700, "stats_effect": {'can_pop_lead': True, 'damage': 1, 'projectile_color': (255, 100, 0)}}, # Adds lead popping, +1 damage, orange color
        },
        # Path 3: Extra Pierce / More Extra Pierce / Blade Shooter
        3: {
            1: {"name": "Extra Pierce", "price": 100, "stats_effect": {'pierce': 1}},
            2: {"name": "More Extra Pierce", "price": 150, "stats_effect": {'pierce': 1}},
            3: {"name": "Blade Shooter", "price": 600, "stats_effect": {'pierce': 4, 'projectile_type': 'BladeProjectile', 'projectile_radius': 8, 'projectile_color': (150, 150, 150)}}, # Tack pierce becomes 6, new blade projectile
        },
    },
    "Sniper Monkey": {
        # Path 1: Full Metal Jacket / Deadly Precision / Maim MOAB
        1: {
            1: {"name": "Full Metal Jacket", "price": 300, "stats_effect": {'can_pop_lead': True, 'pierce': 2}}, # Enables lead, pierce +2
            2: {"name": "Deadly Precision", "price": 700, "stats_effect": {'damage': 1, 'pierce': 1, 'fire_rate_multiplier': 0.75}}, # Damage +1, pierce +1, faster attack (1.2s -> 0.9s)
            3: {"name": "Maim MOAB", "price": 4000, "stats_effect": {'damage': 5, 'moab_stun_duration': 2.0}}, # Stuns MOAB-class bloons for 2s, +5 damage
        },
        # Path 2: Faster Firing / Even Faster Firing / Supply Drop
        2: {
            1: {"name": "Faster Firing", "price": 250, "stats_effect": {'fire_rate_multiplier': 0.8}}, # 20% faster
            2: {"name": "Even Faster Firing", "price": 400, "stats_effect": {'fire_rate_multiplier': 0.8}}, # Further 20% faster
            3: {"name": "Supply Drop", "price": 4000, "stats_effect": {'income_ability': 2500, 'ability_cooldown': 60}}, # Income ability every 60s
        },
        # Path 3: Night Vision Goggles / Shrapnel Shot / Bouncing Bullet
        3: {
            1: {"name": "Night Vision Goggles", "price": 200, "stats_effect": {'can_pop_camo': True}}, # Enables camo
            2: {"name": "Shrapnel Shot", "price": 300, "stats_effect": {'shrapnel_count': 3, 'shrapnel_damage': 1, 'shrapnel_pierce': 2}}, # Spawns 3 shrapnel on hit
            3: {"name": "Bouncing Bullet", "price": 1200, "stats_effect": {'bounces': 3, 'pierce': 2}}, # Bounces to up to 3 more bloons
        },
    },
    "Dartling Gunner": {
        # Path 1: Focused Firing / Laser Cannon / Plasma Accelerator
        1: {
            1: {"name": "Focused Firing", "price": 300, "stats_effect": {'accuracy': 0.05}}, # Makes shots more accurate (0.05 deviation)
            2: {"name": "Laser Cannon", "price": 800, "stats_effect": {'damage': 1, 'pierce': 2, 'can_pop_lead': True, 'projectile_color': (255, 0, 255)}}, # Damage +1, pierce +2, pops lead, purple color
            3: {"name": "Plasma Accelerator", "price": 3000, "stats_effect": {'damage': 2, 'pierce': 5, 'fire_rate_multiplier': 0.9}}, # Damage +2, pierce +5, faster (7.0 -> 7.7)
        },
        # Path 2: Faster Barrel Spin / Hydra Rocket Pods / Bloon Area Denial System
        2: {
            1: {"name": "Faster Barrel Spin", "price": 250, "stats_effect": {'fire_rate_multiplier': 0.8}}, # Faster attack speed (7.0 -> 8.75)
            2: {"name": "Hydra Rocket Pods", "price": 1000, "stats_effect": {'num_projectiles': 3, 'aoe_radius': 25, 'damage': 2, 'projectile_type': 'RocketProjectile'}}, # Fires rockets, AOE, damage +2
            3: {"name": "Bloon Area Denial System", "price": 4500, "stats_effect": {'aoe_radius': 50, 'damage': 3, 'stun_duration': 1.0}}, # Larger AOE, more damage, stun
        },
        # Path 3: Powerful Darts / Buckshot / M.A.D
        3: {
            1: {"name": "Powerful Darts", "price": 200, "stats_effect": {'damage': 1, 'pierce': 1}}, # Damage +1, pierce +1
            2: {"name": "Buckshot", "price": 700, "stats_effect": {'num_projectiles': 5, 'damage': 0.5, 'pierce': 1}}, # Fires 5 pellets, 0.5 damage each, 1 pierce
            3: {"name": "M.A.D", "price": 6000, "stats_effect": {'damage_moab': 10, 'fire_rate_multiplier': 0.9}}, # Huge MOAB damage, faster (8.75 -> 9.7)
        },
    },
    "Ice Tower": {
        # Path 1: Enhanced Freeze / Permafrost / Arctic Wind
        1: {
            1: {"name": "Enhanced Freeze", "price": 150, "stats_effect": {'freeze_duration': 0.5, 'slow_factor': 0.0}}, # Freeze duration +0.5s, no slow
            2: {"name": "Permafrost", "price": 250, "stats_effect": {'slow_factor': 0.4}}, # Bloons remain slowed by 40% after freeze
            3: {"name": "Arctic Wind", "price": 2000, "stats_effect": {'range': 50, 'damage': 2, 'attack_cooldown': 1.0, 'area_slow': True}}, # Large range, 2 damage, faster attack (2.5 -> 1.5s), constant area slow
        },
        # Path 2: Cold Snap / Icicle Impale / Super Brittle
        2: {
            1: {"name": "Cold Snap", "price": 100, "stats_effect": {'can_pop_white_zebra_lead': True}}, # Pops White/Zebra/Lead
            2: {"name": "Icicle Impale", "price": 500, "stats_effect": {'damage': 2, 'freeze_duration': 1.0, 'moab_stun_duration': 0.5}}, # Damage +2, longer freeze, stun MOABs
            3: {"name": "Super Brittle", "price": 5000, "stats_effect": {'damage_vulnerable_modifier': 5}}, # Bloons take +5 damage from all sources
        },
        # Path 3: Embrittlement / Absolute Zero / Snowstorm
        3: {
            1: {"name": "Embrittlement", "price": 200, "stats_effect": {'can_pop_frozen_bloons': True}}, # Bloons hit are vulnerable to sharp/shrapnel
            2: {"name": "Absolute Zero", "price": 1000, "stats_effect": {'global_freeze_ability': True, 'ability_cooldown': 60, 'freeze_duration': 3.0}}, # Global freeze ability
            3: {"name": "Snowstorm", "price": 3000, "stats_effect": {'attack_cooldown': 0.75, 'damage': 3, 'range': 100}}, # Much faster, more damage, larger range
        },
    },
    "Banana Farm": {
        # Path 1: Increased Production / Greater Production / Banana Plantation
        1: {
            1: {"name": "Increased Production", "price": 300, "stats_effect": {'banana_rate': 12.0}}, # Bananas every 15s -> 12s
            2: {"name": "Greater Production", "price": 400, "stats_effect": {'banana_rate': 10.0}}, # Bananas every 12s -> 10s
            3: {"name": "Banana Plantation", "price": 1500, "stats_effect": {'banana_rate': 6.0, 'banana_value': 30}}, # Bananas every 10s -> 6s, 20 -> 30 value
        },
        # Path 2: Long Life Bananas / Banana Bank / IMF Loan
        2: {
            1: {"name": "Long Life Bananas", "price": 200, "stats_effect": {'banana_lifespan': 5.0}}, # Bananas stay longer (e.g., 5 seconds additional)
            2: {"name": "Banana Bank", "price": 1500, "stats_effect": {'bank_capacity': 7000, 'interest_rate': 0.1}}, # Creates a bank
            3: {"name": "IMF Loan", "price": 5000, "stats_effect": {'loan_ability': True, 'ability_cooldown': 60, 'loan_amount': 10000}}, # Ability to get loan
        },
        # Path 3: Valuable Bananas / Central Market / Monkey Wall Street
        3: {
            1: {"name": "Valuable Bananas", "price": 200, "stats_effect": {'banana_value': 5}}, # +5 value per banana
            2: {"name": "Central Market", "price": 2000, "stats_effect": {'income_per_round': 200, 'range': 50}}, # Generates money passively + more range for auto-collect
            3: {"name": "Monkey Wall Street", "price": 15000, "stats_effect": {'auto_collect': True, 'income_per_round': 500}}, # Autocollects all bananas
        },
    },
    "Cannon Tower": {
        # Path 1: Bigger Bombs / Heavy Bombs / Bloon Impact
        1: {
            1: {"name": "Bigger Bombs", "price": 300, "stats_effect": {'aoe_radius': 10, 'explosion_radius': 15, 'pierce': 5}}, # Radius +10, pierce +5
            2: {"name": "Heavy Bombs", "price": 400, "stats_effect": {'damage': 1, 'pierce': 10}}, # Damage +1, pierce +10
            3: {"name": "Bloon Impact", "price": 2000, "stats_effect": {'stun_duration': 1.0, 'pierce': 5}}, # Stuns bloons for 1s, pierce +5
        },
        # Path 2: Faster Reload / Even Faster Reload / MOAB Mauler
        2: {
            1: {"name": "Faster Reload", "price": 250, "stats_effect": {'fire_rate_multiplier': 0.8}}, # Faster attack speed (1.4 -> 1.12s)
            2: {"name": "Even Faster Reload", "price": 350, "stats_effect": {'fire_rate_multiplier': 0.8}}, # Even faster attack speed (1.12 -> 0.896s)
            3: {"name": "MOAB Mauler", "price": 2500, "stats_effect": {'damage_moab': 18, 'damage': 0}}, # Deals 18 damage to MOABs
        },
        # Path 3: Missile Launcher / Mortar Monkey / Pop and Awe
        3: {
            1: {"name": "Missile Launcher", "price": 200, "stats_effect": {'projectile_speed_multiplier': 1.5, 'range': 50}}, # Faster projectile, longer range
            2: {"name": "Shattering Shells", "price": 700, "stats_effect": {'pierce_fortified': 2, 'damage_fortified': 1}}, # Deals extra damage to fortified
            3: {"name": "The Big One", "price": 3000, "stats_effect": {'aoe_radius': 30, 'damage': 5, 'pierce': 10}}, # Huge explosion radius and damage
        },
    },
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
        'aoe_radius': 0,
        'radius': 5 # Default projectile radius
    }

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.range = 200
        self.base_fire_rate = 1.0 # Store base for multiplicative upgrades
        self.fire_rate = 1.0  # shots per second (attacks per second)
        self.last_shot = 0
        self.projectiles = []
        self.projectile_type = Projectile
        self.projectile_config = self.PROJECTILE_CONFIG.copy() # Make sure to copy

        # Visuals
        self.radius = 25 # Tower visual radius
        self.color = (255, 0, 0)

        # Upgrade system attributes
        self.upgrades = {1: 0, 2: 0, 3: 0} # Tracks current tier for each path
        self.upgrades_locked_path = None # The path that got locked out (1, 2, or 3)
        self.price = 0 # Base price, will be set by specific tower class

    def find_target(self, enemies):
        """
        Find the first enemy in range.
        This can be overridden in subclasses for different targeting modes (e.g., last, close, strong).
        """
        for enemy in enemies:
            dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if dist <= self.range:
                return enemy
        return None

    def fire(self, enemies: list, current_time: float):
        """
        Creates projectiles if the tower is ready to fire and a target is found.
        Passes the target's position (x, y) to the projectile.
        """
        # Fire rate is attacks per second, so cooldown is 1.0 / fire_rate
        if current_time - self.last_shot < (1.0 / self.fire_rate):
            return

        target = self.find_target(enemies)
        if target:
            # Pass target's position at time of firing, not the enemy object itself
            self.create_projectile((target.x, target.y))
            self.last_shot = current_time

    def create_projectile(self, target_pos: tuple):
        """
        Instantiates configured projectile type with given target position and tower's projectile_config.
        """
        projectile = self.projectile_type(
            self.x, self.y,
            target_pos, # Pass the target's static position at time of firing
            **self.projectile_config
        )
        self.projectiles.append(projectile)

    def update_projectiles(self, screen, enemies: list, dt: float):
        """
        Updates the position of all active projectiles, handles collisions,
        applies damage and effects, and removes expired projectiles.
        """
        # Iterate over a copy of the list to safely remove elements during iteration
        for proj in self.projectiles[:]:
            proj.move(dt) # Update projectile's position

            # Check for collisions with any enemy along its path
            hit_enemy = proj.check_collision(enemies)

            if hit_enemy:
                # Apply damage and effects to the hit enemy
                if hasattr(hit_enemy, 'take_damage'):
                    hit_enemy.take_damage(proj.damage)
                    proj.apply_effects(hit_enemy)
                proj.pierce -= 1 # Reduce pierce count after hitting an enemy

                # If it's a CannonProjectile and has an AOE radius, trigger its explosion
                if isinstance(proj, CannonProjectile) and proj.aoe_radius > 0:
                    proj.explode(screen, enemies) # Cannon explosion affects nearby enemies

            # Remove the projectile if it has no pierce left or has expired (e.g., reached max distance/lifespan)
            if proj.should_expire():
                self.projectiles.remove(proj)
            else:
                proj.draw(screen) # Draw the projectile if it's still active


    def draw(self, screen, enemies: list):
        """
        Draws the tower itself.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        # Optional: Draw range circle for debugging/visualisation
        # pygame.draw.circle(screen, (100, 100, 100, 50), (int(self.x), int(self.y)), self.range, 1)

    def get_upgrade_info(self, path: int, tier: int):
        """Returns the upgrade data (name, price) for a specific path and tier."""
        tower_upgrades = UPGRADES.get(self.__class__.__name__)
        if tower_upgrades and path in tower_upgrades and tier in tower_upgrades[path]:
            return tower_upgrades[path][tier]
        return None

    def can_upgrade(self, path: int, tier: int) -> bool:
        """
        Checks if a specific upgrade can be purchased based on game rules (max tier,
        locked path, and sequential upgrades).
        """
        # Check if the upgrade tier is valid (1, 2, or 3)
        if not (1 <= tier <= 3):
            return False

        # Check if this path is locked due to upgrades in other paths
        if self.upgrades_locked_path is not None and self.upgrades_locked_path == path:
            return False

        # Check if the desired tier is exactly one level higher than the current tier on this path
        if self.upgrades[path] != tier - 1:
            return False # Must upgrade sequentially (e.g., cannot go from tier 0 to tier 2)

        # Check if the current tier is already maxed for this path
        if self.upgrades[path] == 3:
            return False

        # Check if any two paths already have upgrades, which would lock the third
        active_paths = [p for p, t in self.upgrades.items() if t > 0]
        if len(active_paths) == 2 and path not in active_paths:
            return False # Cannot upgrade if two other paths already have upgrades

        return True


    def apply_upgrade(self, path: int, tier: int):
        """
        Applies the effects of an upgrade to the tower's stats and properties.
        Also handles locking out the third path.
        """
        upgrade_data = self.get_upgrade_info(path, tier)
        if not upgrade_data:
            print(f"Error: Upgrade data not found for {self.__class__.__name__}, path {path}, tier {tier}")
            return

        # Apply stat effects
        if "stats_effect" in upgrade_data:
            for stat, value in upgrade_data["stats_effect"].items():
                # Multiplicative speed/rate changes
                if stat == 'fire_rate_multiplier':
                    self.fire_rate *= value # Apply multiplier directly
                elif stat == 'projectile_speed_multiplier':
                    self.projectile_config['speed'] *= (1 + value) if value > 0 and value < 1 else value
                elif stat == 'projectile_lifespan_multiplier':
                    self.projectile_config['lifespan'] *= (1 + value) if value > 0 and value < 1 else value
                elif stat == 'projectile_max_distance_multiplier':
                    self.projectile_config['max_distance'] *= (1 + value) if value > 0 and value < 1 else value
                elif stat == 'banana_rate': # Banana farm specific. Higher value means slower rate.
                    self.banana_rate = value # Set directly
                elif stat == 'attack_cooldown': # Ice Tower specific, direct value
                    self.attack_cooldown = value
                # Direct additions/sets
                elif stat == 'range':
                    self.range += value
                elif stat == 'damage':
                    self.projectile_config['damage'] += value
                elif stat == 'pierce':
                    self.projectile_config['pierce'] += value
                elif stat == 'aoe_radius':
                    self.projectile_config['aoe_radius'] += value
                elif stat == 'explosion_radius':
                    self.projectile_config['explosion_radius'] += value
                elif stat == 'radius': # Projectile radius
                    self.projectile_config['radius'] += value
                elif stat == 'projectile_radius': # Specific projectile radius for new types
                    self.projectile_config['radius'] = value
                elif stat == 'color': # Tower color (for cosmetic upgrades)
                    self.color = value
                elif stat == 'projectile_color': # Projectile color
                    self.projectile_config['color'] = value
                elif stat == 'can_pop_lead':
                    self.projectile_config['can_pop_lead'] = value
                elif stat == 'can_pop_camo':
                    self.projectile_config['can_pop_camo'] = value
                elif stat == 'homing':
                    self.projectile_config['homing'] = value
                elif stat == 'num_projectiles':
                    self.num_projectiles += value
                elif stat == 'accuracy': # Dartling specific, lower value means more accurate (less deviation)
                    self.accuracy = value
                elif stat == 'moab_stun_duration': # Sniper specific
                    self.moab_stun_duration = value
                elif stat == 'shrapnel_count': # Sniper specific
                    self.shrapnel_count = value
                elif stat == 'shrapnel_damage': # Sniper specific
                    self.shrapnel_damage = value
                elif stat == 'shrapnel_pierce': # Sniper specific
                    self.shrapnel_pierce = value
                elif stat == 'bounces': # Sniper specific
                    self.bounces = value
                elif stat == 'stun_duration': # Cannon/Dartling
                    self.stun_duration = value
                elif stat == 'damage_moab': # Cannon/Dartling
                    self.damage_moab = value
                elif stat == 'pierce_fortified': # Cannon
                    self.pierce_fortified = value
                elif stat == 'damage_fortified': # Cannon
                    self.damage_fortified = value
                elif stat == 'can_pop_white_zebra_lead': # Ice Tower
                    self.can_pop_white_zebra_lead = value
                elif stat == 'can_pop_frozen_bloons': # Ice Tower
                    self.can_pop_frozen_bloons = value
                elif stat == 'freeze_duration': # Ice Tower
                    self.freeze_duration = value
                elif stat == 'slow_factor': # Ice Tower
                    self.slow_factor = value
                elif stat == 'damage_vulnerable_modifier': # Ice Tower
                    self.damage_vulnerable_modifier = value
                elif stat == 'area_slow': # Ice Tower (Arctic Wind)
                    self.area_slow = value
                elif stat == 'global_freeze_ability': # Ice Tower (Absolute Zero)
                    self.global_freeze_ability = value
                elif stat == 'ability_cooldown': # For abilities
                    self.ability_cooldown = value
                elif stat == 'income_ability': # Sniper Supply Drop
                    self.income_ability = value
                    self.last_ability_time = pygame.time.get_ticks() / 1000.0
                elif stat == 'banana_value': # Banana Farm
                    self.banana_value = value
                elif stat == 'banana_lifespan': # Banana Farm
                    self.banana_lifespan = value
                elif stat == 'bank_capacity': # Banana Farm
                    self.bank_capacity = value
                    self.current_bank_amount = 0 # Initialize bank amount
                elif stat == 'interest_rate': # Banana Farm
                    self.interest_rate = value
                    self.last_interest_time = pygame.time.get_ticks() / 1000.0
                elif stat == 'loan_ability': # Banana Farm
                    self.loan_ability = value
                    self.last_loan_time = 0
                elif stat == 'loan_amount':
                    self.loan_amount = value
                elif stat == 'income_per_round': # Banana Farm Central Market/Wall Street
                    self.income_per_round = value
                elif stat == 'auto_collect': # Banana Farm Monkey Wall Street
                    self.auto_collect = value
                elif stat == 'projectile_type': # Change projectile class type
                    if value == 'SpikeProjectile':
                        self.projectile_type = DartProjectile # Placeholder, ideally a new class
                    elif value == 'CrossbowProjectile':
                        self.projectile_type = DartProjectile # Placeholder, ideally a new class
                    elif value == 'BladeProjectile':
                        self.projectile_type = TackProjectile # Placeholder, ideally a new class
                    elif value == 'RocketProjectile':
                        self.projectile_type = Projectile # Placeholder, ideally a new class
                    # Add more projectile type changes here
                # Add more special stat handling as needed for specific towers/upgrades

        # Increment the tier for the applied path
        self.upgrades[path] = tier

        # Check for locking of the third path
        active_paths = [p for p, t in self.upgrades.items() if t > 0]
        if len(active_paths) == 2 and self.upgrades_locked_path is None:
            # Find the path that is not one of the active paths
            for p_num in [1, 2, 3]:
                if p_num not in active_paths:
                    self.upgrades_locked_path = p_num
                    print(f"Path {p_num} locked for {self.__class__.__name__}")
                    break


class CannonTower(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Cannon Tower"]["price"]
        self.color = (0, 0, 0) # Black color for cannon tower
        self.range = 200 # Default range for bombs
        self.base_fire_rate = 1.0 / 1.4 # BTD6 base: 1.4 seconds attack speed
        self.fire_rate = self.base_fire_rate
        self.projectile_type = CannonProjectile # Uses the specialized CannonProjectile
        self.projectile_config.update({
            'damage': 1, # Base damage
            'speed': 10, # Projectile speed
            'aoe_radius': 20, # Base AOE radius
            'explosion_radius': 30, # Visual explosion radius
            'can_pop_lead': True, # Base cannon can pop lead bloons
            'radius': 8 # Projectile radius
        })
        self.num_projectiles = 1 # Used for upgrades that increase projectile count
        self.stun_duration = 0 # From upgrades
        self.damage_moab = 0 # From upgrades
        self.pierce_fortified = 0 # From upgrades
        self.damage_fortified = 0 # From upgrades


class DartMonkey(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Dart Monkey"]["price"]
        self.color = (255, 0, 0)
        self.range = 100 # Approx for 32 game units
        self.base_fire_rate = 1.0 / 0.95 # BTD6 base: 0.95 seconds attack speed
        self.fire_rate = self.base_fire_rate
        self.projectile_type = Projectile # Uses the base Projectile class
        self.projectile_config.update({
            'damage': 1,
            'speed': 10,
            'pierce': 2, # Base pierce 2
            'trail_length': 0, # Dart Monkey does not have visual trail
            'can_pop_lead': False,
            'can_pop_camo': False,
        })
        self.num_projectiles = 1 # Used for upgrades like Triple Shot

class TackShooter(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Tack Shooter"]["price"]
        self.color = (255, 100, 100)
        self.base_fire_rate = 1.5 # BTD6 base: 1.5 shots per second
        self.fire_rate = self.base_fire_rate
        self.range = 80  # BTD6 base: 80 units
        self.projectile_type = TackProjectile # Uses the specialized TackProjectile
        self.projectile_config.update({
            'damage': 1,
            'speed': 8,
            'lifespan': 0.2,  # Very short lifespan for tacks
            'pierce': 1,
            'max_distance': 50, # Very short max distance for tacks
            'radius': 3, # Small radius for tack projectile
            'can_pop_lead': False,
            'can_pop_camo': False,
        })
        self.num_projectiles = 8 # Base 8 tacks

    def fire(self, enemies: list, current_time: float):
        """
        Overrides the base fire method to shoot tacks in 8 radial directions.
        """
        if current_time - self.last_shot < (1.0 / self.fire_rate):
            return

        # Check if any enemy is in range to trigger firing
        in_range = any(math.sqrt((e.x - self.x)**2 + (e.y - self.y)**2) <= self.range for e in enemies)

        if in_range:
            # Fire self.num_projectiles in radial directions
            for i in range(self.num_projectiles):
                angle = (360 / self.num_projectiles) * i
                rad = math.radians(angle)
                # Calculate a target position based on the direction for each tack
                target_x = self.x + math.cos(rad) * 1000 # Large distance to ensure direction
                target_y = self.y + math.sin(rad) * 1000 # Large distance to ensure direction
                self.create_projectile((target_x, target_y)) # Pass calculated position
            self.last_shot = current_time

class SniperMonkey(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Sniper Monkey"]["price"]
        self.color = (100, 100, 100)
        self.range = float('inf') # Effectively infinite range for sniper
        self.base_fire_rate = 1.0 / 1.2 # BTD6 base: 1.2 seconds attack speed
        self.fire_rate = self.base_fire_rate
        self.projectile_type = HitscanProjectile # Uses the specialized HitscanProjectile
        self.projectile_config.update({
            'damage': 2, # BTD6 Base damage is 2
            'can_pop_lead': False, # Base sniper cannot pop lead
            'can_pop_camo': False, # Base sniper cannot pop camo
        })
        # Sniper specific upgrade attributes
        self.moab_stun_duration = 0
        self.shrapnel_count = 0
        self.shrapnel_damage = 0
        self.shrapnel_pierce = 0
        self.bounces = 0
        self.income_ability = 0
        self.last_ability_time = 0
        self.ability_cooldown = 0


    def find_target(self, enemies):
        """
        Finds the enemy farthest along the path, prioritizing enemies deeper into the track.
        """
        if not enemies:
            return None

        farthest_enemy = None
        max_path_index = -1
        for enemy in enemies:
            if enemy.current_path_index > max_path_index:
                farthest_enemy = enemy
                max_path_index = enemy.current_path_index
        return farthest_enemy

    def fire(self, enemies: list, current_time: float):
        """
        Overrides the fire method for instant (hitscan) damage.
        Sniper projectiles do not move, they hit instantly.
        """
        if current_time - self.last_shot < (1.0 / self.fire_rate):
            return

        target = self.find_target(enemies)
        if target:
            # Create a HitscanProjectile and immediately apply its hit
            hitscan_projectile = HitscanProjectile(self, target, **self.projectile_config)
            hitscan_projectile.apply_hit()
            self.last_shot = current_time

    def update(self, enemies: list, current_time: float):
        # Handle Supply Drop ability
        if self.income_ability > 0 and current_time - self.last_ability_time >= self.ability_cooldown:
            # For now, just print income. In game, add to player's money.
            print(f"Sniper Supply Drop: +${self.income_ability}")
            self.last_ability_time = current_time
            return self.income_ability # Return income for test.py to add to menu.money

        # Other Sniper update logic if any, e.g., tracking debuffs on bloons
        pass

    def update_projectiles(self, screen, enemies: list, dt: float):
        """
        Sniper Monkey's projectiles are hitscan, so they don't need continuous updates
        or drawing. This method is empty for Sniper Monkey.
        """
        pass

class DartlingGunner(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Dartling Gunner"]["price"]
        self.color = (150, 75, 0)  # Brown color for Dartling Gunner
        self.base_fire_rate = 7.0  # BTD6 Base: 7.0 shots per second
        self.fire_rate = self.base_fire_rate
        self.range = 250 # Approximation of its targeting range
        self.projectile_type = Projectile  # Uses standard projectiles
        self.projectile_config.update({
            'damage': 1,
            'speed': 15, # Faster speed for dartling gunner projectiles
            'pierce': 2,
            'aoe_radius': 0,
            'radius': 4, # Smaller radius
            'can_pop_lead': False,
            'can_pop_camo': False,
        })
        self.num_projectiles = 1
        self.accuracy = 0.0 # 0.0 means perfect accuracy, higher means more deviation (0.0 to 1.0)
        self.stun_duration = 0 # From upgrades
        self.damage_moab = 0 # From upgrades

    def fire(self, mouse_pos: tuple, current_time: float): # Modified to take mouse_pos directly
        """
        Fires projectiles at the current mouse position, with accuracy deviation.
        """
        if current_time - self.last_shot < (1.0 / self.fire_rate):
            return
        
        # Dartling Gunner fires at the mouse position
        # Apply accuracy modification (deviation)
        if self.accuracy > 0:
            deviation_x = self.accuracy * 100 * (2 * random.random() - 1) # Scale deviation by accuracy
            deviation_y = self.accuracy * 100 * (2 * random.random() - 1)
            target_x = mouse_pos[0] + deviation_x
            target_y = mouse_pos[1] + deviation_y
            self.create_projectile((target_x, target_y))
        else: # Perfect accuracy if self.accuracy is 0
            self.create_projectile(mouse_pos) 

        self.last_shot = current_time

    # No need for find_target for Dartling Gunner as it aims at mouse
    def find_target(self, enemies):
        return None

class IceTower(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Ice Tower"]["price"]
        self.color = (100, 200, 255)
        self.range = 75 # Approx. 40 game units BTD6
        self.slow_factor = 0.67  # 33% slow
        self.slow_duration = 2.0  # seconds
        self.slow_damage = 1 # 1 damage per blast
        self.last_attack_time = 0
        self.attack_cooldown = 2.5 # seconds (every 2.5 seconds, fits 2-3 sec user request)
        
        # Ice Tower doesn't fire projectiles, so remove related configs
        self.projectile_type = None 
        self.projectile_config = {}
        self.projectiles = [] # Ensure no projectiles are stored

        # Ice Tower specific upgrade attributes
        self.can_pop_white_zebra_lead = False # From upgrades
        self.can_pop_frozen_bloons = False # From upgrades
        self.global_freeze_ability = False # From upgrades
        self.moab_stun_duration = 0 # From upgrades
        self.damage_vulnerable_modifier = 0 # From upgrades
        self.area_slow = False # For Arctic Wind, means constant slow

    def update(self, enemies: list, current_time: float, screen): # Added screen to draw momentary aura
        """
        Applies a momentary slow aura to enemies within its range and deals damage.
        If Arctic Wind (area_slow) is active, it's a constant effect.
        """
        # Arctic Wind (constant aura) vs. momentary blast
        if self.area_slow:
            # Constant aura logic (simplified for now as drawing happens in draw method)
            for enemy in enemies:
                dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if dist <= self.range:
                    if not hasattr(enemy, 'ice_slow_active') or not enemy.ice_slow_active:
                        if not hasattr(enemy, 'original_speed'):
                            enemy.original_speed = enemy.speed
                        enemy.speed = enemy.original_speed * self.slow_factor
                        enemy.ice_slow_active = True # Mark as slowed by ice tower
                        enemy.ice_slow_source = self # Mark which tower slowed it

            # Clean up speeds for bloons leaving the aura
            for enemy in enemies:
                if hasattr(enemy, 'ice_slow_active') and enemy.ice_slow_active and enemy.ice_slow_source == self:
                    dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                    if dist > self.range:
                        enemy.speed = enemy.original_speed
                        del enemy.original_speed
                        enemy.ice_slow_active = False
                        del enemy.ice_slow_source
            
            # Damage periodically within constant aura (e.g., every 0.5s if not already handled by attack_cooldown)
            if current_time - self.last_attack_time >= self.attack_cooldown:
                for enemy in enemies:
                    dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                    if dist <= self.range:
                        enemy.take_damage(self.slow_damage) # Use slow_damage as base damage
                self.last_attack_time = current_time

        else: # Momentary blast logic (base Ice Tower)
            if current_time - self.last_attack_time >= self.attack_cooldown:
                # Draw momentary aura visual for a single frame
                aura_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
                pygame.draw.circle(aura_surface, (100, 200, 255, 70), (self.range, self.range), self.range) # Semi-transparent blue
                screen.blit(aura_surface, (self.x - self.range, self.y - self.range))

                for enemy in enemies:
                    dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                    if dist <= self.range:
                        # Apply damage
                        enemy.take_damage(self.slow_damage)

                        # Apply slow effect (non-stackable by this specific tower instance)
                        if not hasattr(enemy, 'ice_slow_active') or not enemy.ice_slow_active:
                            if not hasattr(enemy, 'original_speed'):
                                enemy.original_speed = enemy.speed
                            enemy.speed = enemy.original_speed * self.slow_factor
                            enemy.ice_slow_expire_time = current_time + self.slow_duration
                            enemy.ice_slow_active = True # Mark as slowed by ice tower
                            enemy.ice_slow_source = self # Mark which tower slowed it
                self.last_attack_time = current_time
            
            # Check and remove expired slow effects for momentary blasts
            for enemy in enemies:
                if hasattr(enemy, 'ice_slow_active') and enemy.ice_slow_active and enemy.ice_slow_source == self and current_time > enemy.ice_slow_expire_time:
                    enemy.speed = enemy.original_speed # Reset speed
                    del enemy.original_speed # Clean up
                    enemy.ice_slow_active = False
                    del enemy.ice_slow_source


    def draw(self, screen, enemies: list):
        """
        Draws the Ice Tower. If Arctic Wind is active, draw its persistent aura.
        """
        super().draw(screen, enemies)
        if self.area_slow: # Draw persistent aura for Arctic Wind
            aura_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, (100, 200, 255, 50), (self.range, self.range), self.range) # Semi-transparent blue
            screen.blit(aura_surface, (int(self.x - self.range), int(self.y - self.range)))


class BananaFarm(Tower):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.price = tower_menu_info["Banana Farm"]["price"]
        self.color = (150, 100, 0) # Brown for banana farm
        self.bananas = []
        self.last_banana_time = 0
        self.banana_rate = 15.0  # BTD6 base: produces 4 bananas every ~15 seconds (approximation)
        self.banana_value = 20 # BTD6 base: 20 money per banana (4 bananas * 20 = 80 per interval)

        # Banana Farm doesn't fire projectiles, so remove related configs
        self.projectile_type = None
        self.projectile_config = {}
        self.projectiles = [] # Ensure no projectiles are stored

        # Banana Farm specific upgrade attributes
        self.banana_lifespan = 5.0 # How long bananas stay on screen (default)
        self.bank_capacity = 0
        self.current_bank_amount = 0
        self.interest_rate = 0
        self.last_interest_time = 0
        self.loan_ability = False
        self.last_loan_time = 0 # Cooldown for loan ability
        self.loan_amount = 0
        self.income_per_round = 0 # Passive income for Central Market/Monkey Wall Street
        self.auto_collect = False # For Monkey Wall Street

    def update(self, current_time: float, mouse_pos):
        """
        Generates bananas and handles their collection by the mouse.
        Also handles passive income from Central Market/Monkey Wall Street.
        """
        money_earned = 0

        # Handle passive income from Central Market / Monkey Wall Street
        if self.income_per_round > 0 and current_time % 1.0 < (current_time - (1.0/60)) % 1.0: # Roughly once per second
            money_earned += self.income_per_round

        # Generate bananas if enough time has passed
        if current_time - self.last_banana_time > self.banana_rate:
            # Generate 4 bananas at the farm's location
            for _ in range(4): # Generate 4 bananas per interval
                self.bananas.append({
                    'x': self.x + random.randint(-20, 20), # Slight offset for visual spread
                    'y': self.y + random.randint(-20, 20),
                    'collected': False,
                    'spawn_time': current_time
                })
            self.last_banana_time = current_time

        # Update banana positions and check for collection
        for banana in self.bananas[:]: # Iterate over a copy to allow safe removal
            if banana['collected'] or current_time - banana['spawn_time'] > self.banana_lifespan:
                if banana['collected']:
                    money_earned += self.banana_value # Add money for collected banana
                self.bananas.remove(banana)
                continue

            # Auto-collect for Monkey Wall Street
            if self.auto_collect:
                banana['collected'] = True
                continue # Will be removed in the next iteration

            # Manual collection: Calculate distance to mouse
            dx = mouse_pos[0] - banana['x']
            dy = mouse_pos[1] - banana['y']
            dist = math.sqrt(dx**2 + dy**2)

            if dist < 150:  # Attraction range: bananas move towards mouse
                # Adjust speed of attraction
                banana['x'] += dx * 0.1
                banana['y'] += dy * 0.1

                if dist < 15:  # Collection range: banana is collected
                    banana['collected'] = True
        return money_earned

    def draw(self, screen, enemies: list):
        """
        Draws the Banana Farm and any generated bananas.
        """
        super().draw(screen, enemies)
        # Draw bananas that haven't been collected
        for banana in self.bananas:
            if not banana['collected']:
                pygame.draw.circle(screen, (255, 255, 0), (int(banana['x']), int(banana['y'])), 8) # Yellow for bananas

