import pygame
from tower import tower_menu_info, UPGRADES # Import UPGRADES for upgrade info

class Menu:
    def __init__(self, screen, money):
        self.screen = screen
        self.money = money
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.current_wave = 1  # Initialize the current wave number
        self.selected_placed_tower = None  # Initialize selected placed tower
        self.towers_to_buy = [
            {
                "name": tower_name,
                "price": tower_data["price"],
                "color": tower_data["color"],
                "x": 50 + index * 100,
                "y": 800,
            }
            for index, (tower_name, tower_data) in enumerate(tower_menu_info.items())
        ]
        self.selected_tower_to_buy = None
        self.preview_tower = None

    def draw_menu(self):
        # Draw the main menu background (for buying new towers)
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 750, 900, 150))

        # Draw each tower to buy and its price
        for tower in self.towers_to_buy:
            pygame.draw.rect(self.screen, tower["color"], (tower["x"], tower["y"], 50, 50))
            price_text = self.font.render(f"${tower['price']}", True, (0, 0, 0))
            self.screen.blit(price_text, (tower["x"], tower["y"] + 60))

        # Draw the current wave number
        wave_text = self.font.render(f"Wave: {self.current_wave}", True, (0, 0, 0))
        self.screen.blit(wave_text, (400, 10))  # Display wave number at the top center

    def increment_wave(self):
        """Increment the current wave number."""
        self.current_wave += 1


    def draw_upgrade_menu(self):
        self.upgrade_buttons = [] # Clear previous buttons

        if self.selected_placed_tower:
            # Draw a background for the upgrade menu
            upgrade_menu_rect = pygame.Rect(self.screen.get_width() - 250, 0, 250, self.screen.get_height() - 150)
            pygame.draw.rect(self.screen, (180, 180, 180), upgrade_menu_rect)
            pygame.draw.rect(self.screen, (100, 100, 100), upgrade_menu_rect, 3) # Border

            tower_name_text = self.font.render(f"{self.selected_placed_tower.__class__.__name__}", True, (0, 0, 0))
            self.screen.blit(tower_name_text, (upgrade_menu_rect.x + 10, upgrade_menu_rect.y + 10))

            y_offset = 50
            for path in range(1, 4): # Loop through paths 1, 2, 3
                current_tier = self.selected_placed_tower.upgrades.get(path, 0)
                next_tier = current_tier + 1
                upgrade_info = self.selected_placed_tower.get_upgrade_info(path, next_tier)
                
                button_x = upgrade_menu_rect.x + 10
                button_y = upgrade_menu_rect.y + y_offset
                button_width = 230
                button_height = 50
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

                button_color = (100, 100, 200) # Default button color
                text_color = (255, 255, 255)
                button_text = f"Path {path}: "

                can_afford = False
                if upgrade_info:
                    can_afford = self.money >= upgrade_info['price']

                if self.selected_placed_tower.upgrades_locked_path == path:
                    button_text += "LOCKED"
                    button_color = (50, 50, 50) # Dark gray for locked
                elif current_tier == 3:
                    button_text += "MAXED"
                    button_color = (50, 150, 50) # Green for maxed
                elif upgrade_info:
                    button_text += f"{upgrade_info['name']} (${upgrade_info['price']})"
                    if not can_afford:
                        button_color = (150, 100, 100) # Reddish if not enough money
                    else:
                        button_color = (100, 100, 200) # Default blue if affordable
                else: # Should not happen if UPGRADES dict is complete, but for safety
                    button_text += "N/A"
                    button_color = (70, 70, 70)

                pygame.draw.rect(self.screen, button_color, button_rect, border_radius=5)
                pygame.draw.rect(self.screen, (50, 50, 50), button_rect, 2, border_radius=5) # Border

                text_surface = self.small_font.render(button_text, True, text_color)
                self.screen.blit(text_surface, (button_x + 5, button_y + 5))
                
                # Display current tier
                tier_text = self.small_font.render(f"Tier: {current_tier}", True, (0, 0, 0))
                self.screen.blit(tier_text, (button_x + 5, button_y + 30))

                self.upgrade_buttons.append({
                    "rect": button_rect,
                    "path": path,
                    "tier": next_tier,
                    "upgrade_info": upgrade_info # Store the info for click handling
                })
                y_offset += 60

    def handle_click(self, mouse_pos: tuple, placed_towers: list):
        # Flag to track if any interactive UI element was clicked
        handled_ui_click = False

        # 1. Check for clicks on upgrade buttons (only if a tower is already selected for upgrades)
        if self.selected_placed_tower:
            for button in self.upgrade_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    self.handle_upgrade_button_click(button)
                    handled_ui_click = True
                    break # Handled click on an upgrade button, stop checking

        if handled_ui_click:
            return # Exit if an upgrade button was clicked

        # 2. Check for clicks on placed towers to select/deselect them for upgrades
        for tower in placed_towers:
            tower_rect = pygame.Rect(tower.x - tower.radius, tower.y - tower.radius, tower.radius * 2, tower.radius * 2)
            if tower_rect.collidepoint(mouse_pos):
                if self.selected_placed_tower == tower:
                    # Clicking on the same tower deselects it
                    self.selected_placed_tower = None
                    print(f"Deselected placed tower: {tower.__class__.__name__}")
                else:
                    # Clicking on a new tower selects it
                    self.selected_placed_tower = tower
                    self.selected_tower_to_buy = None # Deselect buy menu if a placed tower is selected
                    self.preview_tower = None
                    print(f"Selected placed tower: {tower.__class__.__name__} at ({tower.x}, {tower.y})")
                handled_ui_click = True
                break # Found a tower, stop checking

        if handled_ui_click:
            return # Exit if a placed tower was clicked

        # 3. Check for clicks on the tower buying menu (bottom bar)
        for tower_data in self.towers_to_buy:
            tower_rect = pygame.Rect(tower_data["x"], tower_data["y"], 50, 50)
            if tower_rect.collidepoint(mouse_pos):
                if self.money >= tower_data["price"]:
                    self.selected_tower_to_buy = tower_data
                    self.preview_tower = tower_data  # Set the preview tower
                    self.selected_placed_tower = None # Deselect any placed tower if a buy tower is selected
                    print(f"Selected {tower_data['name']} for ${tower_data['price']}")
                else:
                    print(f"Not enough money for {tower_data['name']}")
                handled_ui_click = True
                break # Handled click on a buy tower, stop checking

        if handled_ui_click:
            return # Exit if a buy menu tower was clicked

        # If we reached here, no specific UI element (upgrade button, placed tower, buy tower) was clicked.
        # If a tower is currently selected for buying, this click must be an attempt to place it on the map.
        # In this scenario, we DO NOT deselect selected_tower_to_buy, as test.py needs it to be active for placement.
        # If no tower is selected for buying, AND no other UI element was clicked, then clicking
        # on an empty space (either on the map or in the menu) should deselect any active placed tower.
        if not self.selected_tower_to_buy:
            self.selected_placed_tower = None
            self.preview_tower = None # Clear preview if no tower is selected for buying
            print("DEBUG: Clicked empty space. Deselecting active placed tower (if any) and preview.")


    def handle_upgrade_button_click(self, button_data: dict):
        if not self.selected_placed_tower:
            return

        path_to_upgrade = button_data["path"]
        tier_to_upgrade = button_data["tier"]
        upgrade_info = button_data["upgrade_info"]

        if upgrade_info is None:
            print("Invalid upgrade selected.")
            return

        upgrade_price = upgrade_info["price"]

        if self.money >= upgrade_price:
            if self.selected_placed_tower.can_upgrade(path_to_upgrade, tier_to_upgrade):
                self.money -= upgrade_price
                self.selected_placed_tower.apply_upgrade(path_to_upgrade, tier_to_upgrade)
                print(f"Upgraded {self.selected_placed_tower.__class__.__name__} to {upgrade_info['name']}")
            else:
                print(f"Cannot upgrade {self.selected_placed_tower.__class__.__name__} path {path_to_upgrade} to tier {tier_to_upgrade}.")
                if self.selected_placed_tower.upgrades_locked_path == path_to_upgrade:
                    print(f"Path {path_to_upgrade} is locked!")
                elif self.selected_placed_tower.upgrades.get(path_to_upgrade, 0) == 3:
                    print(f"Path {path_to_upgrade} is already maxed!")
                else:
                    print(f"Must upgrade path {path_to_upgrade} sequentially (current: {self.selected_placed_tower.upgrades.get(path_to_upgrade, 0)}, target: {tier_to_upgrade}).")
        else:
            print(f"Not enough money for {upgrade_info['name']}. Need ${upgrade_price - self.money} more.")

    def draw_money(self):
        # Draw the user's money on the top-right corner of the screen
        money_text = self.font.render(f"Money: ${int(self.money)}", True, (0, 0, 0)) # Cast to int for display
        self.screen.blit(money_text, (700, 10))

    def draw_preview(self, mouse_pos):
        # Draw a transparent preview of the selected tower for placement
        if self.preview_tower:
            preview_color = (*self.preview_tower["color"], 100)  # Add transparency
            preview_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(preview_surface, preview_color, (25, 25), 25) # Draw a transparent circle
            self.screen.blit(preview_surface, (mouse_pos[0] - 25, mouse_pos[1] - 25))