import pygame
from tower import tower_menu_info

class Menu:
    def __init__(self, screen, money):
        self.screen = screen
        self.money = money
        self.font = pygame.font.Font(None, 36)
        self.towers = [
            {
            "name": tower_name,
            "price": tower_data["price"],
            "color": tower_data["color"],
            "x": 50 + index * 100,
            "y": 800,
            }
            for index, (tower_name, tower_data) in enumerate(tower_menu_info.items())
        ]
        self.selected_tower = None
        self.preview_tower = None  # Holds the preview tower's data
        
    def draw_menu(self):
        # Draw the menu background
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 750, 900, 150))

        # Draw each tower and its price
        for tower in self.towers:
            pygame.draw.rect(self.screen, tower["color"], (tower["x"], tower["y"], 50, 50))
            price_text = self.font.render(f"${tower['price']}", True, (0, 0, 0))
            self.screen.blit(price_text, (tower["x"], tower["y"] + 60))

    def handle_click(self, mouse_pos):
        # Check if the user clicked on a tower in the menu
        for tower in self.towers:
            tower_rect = pygame.Rect(tower["x"], tower["y"], 50, 50)
            if tower_rect.collidepoint(mouse_pos):
                if self.money >= tower["price"]:
                    self.selected_tower = tower
                    self.preview_tower = tower  # Set the preview tower
                    print(f"Selected {tower['name']} for ${tower['price']}")
                else:
                    print(f"Not enough money for {tower['name']}")

    def draw_money(self):
        # Draw the user's money on the top-right corner of the screen
        money_text = self.font.render(f"Money: ${self.money}", True, (0, 0, 0))
        self.screen.blit(money_text, (700, 10))

    def draw_preview(self, mouse_pos):
        # Draw a transparent preview of the selected tower
        if self.preview_tower:
            preview_color = (*self.preview_tower["color"], 100)  # Add transparency
            preview_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            preview_surface.fill(preview_color)
            self.screen.blit(preview_surface, (mouse_pos[0] - 25, mouse_pos[1] - 25))