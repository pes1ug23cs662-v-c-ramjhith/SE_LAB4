import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    # --- UPDATED METHOD FOR TASK 1 ---
    def check_collision(self, player, ai):
        # Check for collision with the player's paddle
        # Only check if the ball is moving left (velocity_x < 0)
        if self.velocity_x < 0:
            if self.rect().colliderect(player.rect()):
                self.velocity_x *= -1

        # Check for collision with the AI's paddle
        # Only check if the ball is moving right (velocity_x > 0)
        if self.velocity_x > 0:
            if self.rect().colliderect(ai.rect()):
                self.velocity_x *= -1
    # ---------------------------------

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)