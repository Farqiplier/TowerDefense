import pygame

class Menu:
    def __init__(self, screen, money):
        self.screen = screen
        self.money = money
        self.font = pygame.font.Font(None, 36)
        self.towers = [
            {"name": "Arrow Tower", "price": 75, "color": (255, 0, 0), "x": 50, "y": 800},
            {"name": "Laser Tower", "price": 150, "color": (0, 0, 255), "x": 150, "y": 800},
            {"name": "Cannon Tower", "price": 200, "color": (0, 255, 0), "x": 250, "y": 800},
        ]
        self.selected_tower = None

    def draw_menu(self):
        # Draw the menu background
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 750, 900, 150))

        # Draw each tower and its price
        for tower in self.towers:
            # Draw the tower as a rectangle
            pygame.draw.rect(self.screen, tower["color"], (tower["x"], tower["y"], 50, 50))
            # Draw the price below the tower
            price_text = self.font.render(f"${tower['price']}", True, (0, 0, 0))
            self.screen.blit(price_text, (tower["x"], tower["y"] + 60))

    def handle_click(self, mouse_pos):
        # Check if the user clicked on a tower
        for tower in self.towers:
            tower_rect = pygame.Rect(tower["x"], tower["y"], 50, 50)
            if tower_rect.collidepoint(mouse_pos):
                # Check if the user has enough money to select the tower
                if self.money >= tower["price"]:
                    self.selected_tower = tower
                    print(f"Selected {tower['name']} for ${tower['price']}")
                else:
                    print(f"Not enough money for {tower['name']}")

    def draw_money(self):
        # Draw the user's money on the top-right corner of the screen
        money_text = self.font.render(f"Money: ${self.money}", True, (0, 0, 0))
        self.screen.blit(money_text, (700, 10))