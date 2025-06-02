import pygame
import os

class Enemy:
    def __init__(self, path, health, speed, money, bloon_type, contains):
        self.path = path
        self.health = health
        self.max_health = health
        self.speed = speed
        self.money = money
        self.bloon_type = bloon_type
        self.current_path_index = 0
        self.x, self.y = self.path[self.current_path_index]
        self.width = 40
        self.height = 50
        self.contains = contains

        # Load the image for the enemy from the 'bloons' folder
        image_path = os.path.join("bloons", f"{bloon_type}.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def move(self):
        if self.current_path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.current_path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            distance = (dx**2 + dy**2)**0.5

            if distance <= self.speed:
                self.x, self.y = target_x, target_y
                self.current_path_index += 1
            else:
                self.x += self.speed * dx / distance
                self.y += self.speed * dy / distance

            self.update_rect()

    def draw(self, screen):
        # Draw the enemy using its image
        screen.blit(self.image, self.rect)

        # Draw the health bar
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        health_bar_width = self.width
        health_bar_height = 5
        health_bar_x = self.rect.x
        health_bar_y = self.rect.y + self.height + 2

        current_health_width = int(health_bar_width * (self.health / self.max_health))

        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height))

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

    def destroyed(self, enemy_list):
        for Balloon in self.contains:
            new_balloon = Balloon(self.path)
            new_balloon.x = self.x
            new_balloon.y = self.y
            new_balloon.current_path_index = self.current_path_index
            enemy_list.append(new_balloon)


class Red(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1, money=10, bloon_type="Red", contains=[])


class Blue(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.4, money=20, bloon_type="Blue", contains=[Red])


class Green(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.8, money=30, bloon_type="Green", contains=[Blue])


class Yellow(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=3.2, money=50, bloon_type="Yellow", contains=[Green])


class Pink(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=3.5, money=60, bloon_type="Pink", contains=[Yellow])


class Black(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.8, money=60, bloon_type="Black", contains=[Yellow, Yellow])


class White(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=2.0, money=60, bloon_type="White", contains=[Yellow, Yellow])


class Purple(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=3.0, money=60, bloon_type="Purple", contains=[Pink])


class Lead(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.0, money=60, bloon_type="Lead", contains=[Black, Black])


class Zebra(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=1.8, money=60, bloon_type="Zebra", contains=[Black, White])


class Rainbow(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1, speed=2.2, money=60, bloon_type="Rainbow", contains=[Zebra, Zebra])


class Ceramic(Enemy):
    def __init__(self, path):
        super().__init__(path, health=10, speed=2.5, money=100, bloon_type="Ceramic", contains=[Rainbow, Rainbow])


class MOAB(Enemy):
    def __init__(self, path):
        super().__init__(path, health=200, speed=1.0, money=500, bloon_type="MOAB", contains=[Ceramic, Ceramic, Ceramic, Ceramic])
        self.width = 120
        self.height = 80
        self.image = pygame.image.load(os.path.join("bloons", "MOAB.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen):
        if self.current_path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.current_path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            angle = pygame.math.Vector2(dx, dy).angle_to((1, 0))  # Calculate the angle to rotate

            rotated_image = pygame.transform.rotate(self.image, angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, rotated_rect)

        # Draw the health bar
        self.draw_health_bar(screen)