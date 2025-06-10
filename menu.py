import pygame
from tower import tower_menu_info, UPGRADES # Import UPGRADES for upgrade info

class Menu:
    """
    Manages the game's menu system, including tower purchasing,
    wave display, money display, and tower upgrade interface.
    """
    def __init__(self, screen, money):
        self.screen = screen  # Pygame screen surface for drawing
        self.money = money    # Player's current amount of money
        self.font = pygame.font.Font(None, 36)  # Standard font for text
        self.small_font = pygame.font.Font(None, 24) # Smaller font for details
        self.current_wave = 1  # Initialize the current wave number
        self.selected_placed_tower = None  # Stores the currently selected tower on the map for upgrades
        # List of dictionaries, each representing a tower available for purchase
        self.towers_to_buy = [
            {
                "name": tower_name, # Name of the tower
                "price": tower_data["price"], # Cost of the tower
                "color": tower_data["color"], # Color representation of the tower
                "x": 50 + index * 100, # X-coordinate for the tower in the buy menu
                "y": 800, # Y-coordinate for the tower in the buy menu
            }
            for index, (tower_name, tower_data) in enumerate(tower_menu_info.items())
        ]
        self.selected_tower_to_buy = None # Stores the tower type selected from the buy menu
        self.preview_tower = None # Stores data for the tower preview when placing

    def draw_menu(self):
        """Draws the main tower purchasing menu at the bottom of the screen."""
        # Draw the main menu background (for buying new towers)
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 750, 900, 150))

        # Draw each tower to buy and its price
        for tower in self.towers_to_buy:
            # Draw the colored rectangle representing the tower
            pygame.draw.rect(self.screen, tower["color"], (tower["x"], tower["y"], 50, 50))
            # Render and display the price of the tower
            price_text = self.font.render(f"${tower['price']}", True, (0, 0, 0))
            self.screen.blit(price_text, (tower["x"], tower["y"] + 60))

        # Draw the current wave number
        wave_text = self.font.render(f"Wave: {self.current_wave}", True, (0, 0, 0))
        self.screen.blit(wave_text, (400, 10))  # Display wave number at the top center

    def increment_wave(self):
        """Increment the current wave number."""
        self.current_wave += 1


    def draw_upgrade_menu(self):
        """Draws the upgrade menu for a selected placed tower on the right side of the screen."""
        self.upgrade_buttons = [] # Clear previous buttons to regenerate them

        if self.selected_placed_tower: # Only draw if a tower on the map is selected
            # Draw a background for the upgrade menu
            upgrade_menu_rect = pygame.Rect(self.screen.get_width() - 250, 0, 250, self.screen.get_height() - 150)
            pygame.draw.rect(self.screen, (180, 180, 180), upgrade_menu_rect) # Light gray background
            pygame.draw.rect(self.screen, (100, 100, 100), upgrade_menu_rect, 3) # Border for the menu

            # Display the name of the selected tower
            tower_name_text = self.font.render(f"{self.selected_placed_tower.__class__.__name__}", True, (0, 0, 0))
            self.screen.blit(tower_name_text, (upgrade_menu_rect.x + 10, upgrade_menu_rect.y + 10))

            y_offset = 50 # Initial Y offset for the first upgrade button
            for path in range(1, 4): # Loop through upgrade paths 1, 2, 3
                current_tier = self.selected_placed_tower.upgrades.get(path, 0) # Get current tier of the path
                next_tier = current_tier + 1 # Determine the next tier for potential upgrade
                # Get information for the next possible upgrade on this path
                upgrade_info = self.selected_placed_tower.get_upgrade_info(path, next_tier)
                
                # Define button dimensions and position
                button_x = upgrade_menu_rect.x + 10
                button_y = upgrade_menu_rect.y + y_offset
                button_width = 230
                button_height = 50
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

                button_color = (100, 100, 200) # Default button color (blueish)
                text_color = (255, 255, 255) # Default text color (white)
                button_text = f"Path {path}: " # Start of the button text

                can_afford = False # Flag to check if player can afford the upgrade
                if upgrade_info:
                    can_afford = self.money >= upgrade_info['price']

                # Determine button text and color based on upgrade status
                if self.selected_placed_tower.upgrades_locked_path == path:
                    button_text += "LOCKED"
                    button_color = (50, 50, 50) # Dark gray for locked path
                elif current_tier == 3: # Max tier for an upgrade path
                    button_text += "MAXED"
                    button_color = (50, 150, 50) # Green for maxed out path
                elif upgrade_info: # If upgrade exists and path is not locked or maxed
                    button_text += f"{upgrade_info['name']} (${upgrade_info['price']})"
                    if not can_afford:
                        button_color = (150, 100, 100) # Reddish if not enough money
                    else:
                        button_color = (100, 100, 200) # Default blue if affordable
                else: # Should not happen if UPGRADES dict is complete, but for safety
                    button_text += "N/A" # Not Available
                    button_color = (70, 70, 70) # Darker gray

                # Draw the upgrade button
                pygame.draw.rect(self.screen, button_color, button_rect, border_radius=5)
                pygame.draw.rect(self.screen, (50, 50, 50), button_rect, 2, border_radius=5) # Border for button

                # Render and display the button text
                text_surface = self.small_font.render(button_text, True, text_color)
                self.screen.blit(text_surface, (button_x + 5, button_y + 5))
                
                # Display current tier of the path
                tier_text = self.small_font.render(f"Tier: {current_tier}", True, (0, 0, 0))
                self.screen.blit(tier_text, (button_x + 5, button_y + 30))

                # Store button data for click handling
                self.upgrade_buttons.append({
                    "rect": button_rect, # Pygame Rect for collision detection
                    "path": path,        # Upgrade path number
                    "tier": next_tier,   # Tier this button would upgrade to
                    "upgrade_info": upgrade_info # Full upgrade details
                })
                y_offset += 60 # Increment Y offset for the next button

    def handle_click(self, mouse_pos: tuple, placed_towers: list):
        """
        Handles mouse clicks for various UI interactions:
        1. Clicking upgrade buttons.
        2. Selecting/deselecting placed towers for upgrade.
        3. Selecting towers from the buy menu.
        4. Deselecting towers by clicking empty space.
        """
        # Flag to track if any interactive UI element was clicked
        handled_ui_click = False

        # 1. Check for clicks on upgrade buttons (only if a tower is already selected for upgrades)
        if self.selected_placed_tower:
            for button in self.upgrade_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    self.handle_upgrade_button_click(button)
                    handled_ui_click = True # Mark that a UI element was clicked
                    break # Handled click on an upgrade button, stop checking other UI elements

        if handled_ui_click:
            return # Exit if an upgrade button was clicked, no further click processing needed

        # 2. Check for clicks on placed towers to select/deselect them for upgrades
        for tower in placed_towers:
            # Create a rect around the tower for click detection (assuming tower.radius exists)
            tower_rect = pygame.Rect(tower.x - tower.radius, tower.y - tower.radius, tower.radius * 2, tower.radius * 2)
            if tower_rect.collidepoint(mouse_pos):
                if self.selected_placed_tower == tower:
                    # Clicking on the same tower deselects it
                    self.selected_placed_tower = None
                    print(f"Deselected placed tower: {tower.__class__.__name__}")
                else:
                    # Clicking on a new tower selects it for upgrade
                    self.selected_placed_tower = tower
                    self.selected_tower_to_buy = None # Deselect buy menu if a placed tower is selected
                    self.preview_tower = None # Clear any placement preview
                    print(f"Selected placed tower: {tower.__class__.__name__} at ({tower.x}, {tower.y})")
                handled_ui_click = True # Mark that a UI element was clicked
                break # Found a tower, stop checking other towers or buy menu

        if handled_ui_click:
            return # Exit if a placed tower was clicked

        # 3. Check for clicks on the tower buying menu (bottom bar)
        for tower_data in self.towers_to_buy:
            tower_rect = pygame.Rect(tower_data["x"], tower_data["y"], 50, 50) # Rect for the buyable tower icon
            if tower_rect.collidepoint(mouse_pos):
                if self.money >= tower_data["price"]: # Check if player can afford the tower
                    self.selected_tower_to_buy = tower_data # Select tower for purchase
                    self.preview_tower = tower_data  # Set the preview tower for placement
                    self.selected_placed_tower = None # Deselect any placed tower if a buy tower is selected
                    print(f"Selected {tower_data['name']} for ${tower_data['price']}")
                else:
                    print(f"Not enough money for {tower_data['name']}")
                handled_ui_click = True # Mark that a UI element was clicked
                break # Handled click on a buy tower, stop checking other buy menu items

        if handled_ui_click:
            return # Exit if a buy menu tower was clicked

        # If we reached here, no specific UI element (upgrade button, placed tower, buy tower) was clicked.
        # This means the click was on an empty space (map or menu background).
        # If a tower is currently selected for buying, this click might be an attempt to place it on the map.
        # In this scenario, we DO NOT deselect selected_tower_to_buy, as the main game loop (test.py)
        # needs it to be active for placement logic.
        # If no tower is selected for buying, AND no other UI element was clicked, then clicking
        # on an empty space should deselect any active placed tower (if one was selected for upgrade).
        if not self.selected_tower_to_buy: # If not in "buying/placing" mode
            self.selected_placed_tower = None # Deselect any tower that was selected for upgrade
            self.preview_tower = None # Clear preview if no tower is selected for buying
            print("DEBUG: Clicked empty space. Deselecting active placed tower (if any) and preview.")


    def handle_upgrade_button_click(self, button_data: dict):
        """Handles the logic when an upgrade button is clicked."""
        if not self.selected_placed_tower: # Safety check, should always have a selected tower here
            return

        path_to_upgrade = button_data["path"]       # Path number of the upgrade
        tier_to_upgrade = button_data["tier"]       # Target tier of the upgrade
        upgrade_info = button_data["upgrade_info"]  # Dictionary with upgrade details (name, price, etc.)

        if upgrade_info is None: # Should not happen if button was drawn correctly
            print("Invalid upgrade selected (no upgrade info).")
            return

        upgrade_price = upgrade_info["price"]

        # Check if player has enough money and if the upgrade is valid for the tower
        if self.money >= upgrade_price:
            if self.selected_placed_tower.can_upgrade(path_to_upgrade, tier_to_upgrade):
                self.money -= upgrade_price # Deduct money
                self.selected_placed_tower.apply_upgrade(path_to_upgrade, tier_to_upgrade) # Apply the upgrade
                print(f"Upgraded {self.selected_placed_tower.__class__.__name__} to {upgrade_info['name']}")
            else:
                # Provide feedback if upgrade is not possible
                print(f"Cannot upgrade {self.selected_placed_tower.__class__.__name__} path {path_to_upgrade} to tier {tier_to_upgrade}.")
                if self.selected_placed_tower.upgrades_locked_path == path_to_upgrade:
                    print(f"Path {path_to_upgrade} is locked!")
                elif self.selected_placed_tower.upgrades.get(path_to_upgrade, 0) == 3: # Max tier is 3
                    print(f"Path {path_to_upgrade} is already maxed!")
                else:
                    # This case usually means trying to skip a tier
                    print(f"Must upgrade path {path_to_upgrade} sequentially (current: {self.selected_placed_tower.upgrades.get(path_to_upgrade, 0)}, target: {tier_to_upgrade}).")
        else:
            print(f"Not enough money for {upgrade_info['name']}. Need ${upgrade_price - self.money} more.")

    def draw_money(self):
        """Draws the player's current money on the top-right corner of the screen."""
        # Render the money text
        money_text = self.font.render(f"Money: ${int(self.money)}", True, (0, 0, 0)) # Cast to int for display
        # Blit the text to the screen
        self.screen.blit(money_text, (700, 10)) # Positioned at top-right

    def draw_preview(self, mouse_pos):
        """Draws a transparent preview of the selected tower for placement at the mouse position."""
        if self.preview_tower: # Only draw if a tower is selected from the buy menu
            # Create a color with alpha for transparency (original color + alpha value)
            preview_color = (*self.preview_tower["color"], 100)  # Add transparency (100 out of 255)
            # Create a new surface for the preview to handle transparency correctly
            preview_surface = pygame.Surface((50, 50), pygame.SRCALPHA) # SRCALPHA allows per-pixel alpha
            # Draw a transparent circle representing the tower's potential placement or range
            pygame.draw.circle(preview_surface, preview_color, (25, 25), 25) # Centered in the 50x50 surface
            # Blit the preview surface to the screen, centered at the mouse cursor
            self.screen.blit(preview_surface, (mouse_pos[0] - 25, mouse_pos[1] - 25))