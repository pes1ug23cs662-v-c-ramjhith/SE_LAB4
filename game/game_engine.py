import pygame
import sys
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # --- NEW FOR TASK 4 ---
        # Initialize the sound mixer
        pygame.mixer.init()
        # Load sound effects (ensure you have an 'assets' folder with these files)
        try:
            self.paddle_hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
            self.wall_bounce_sound = pygame.mixer.Sound("assets/wall_bounce.wav")
            self.score_sound = pygame.mixer.Sound("assets/score.wav")
        except pygame.error as e:
            print(f"Error loading sound file: {e}")
            print("Please ensure you have an 'assets' folder with the required .wav files.")
            # Create dummy sound objects so the game doesn't crash
            self.paddle_hit_sound = pygame.mixer.Sound(buffer=b'')
            self.wall_bounce_sound = pygame.mixer.Sound(buffer=b'')
            self.score_sound = pygame.mixer.Sound(buffer=b'')
        # --------------------
        
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)
        
        self.font = pygame.font.SysFont("Arial", 30)
        self.reset_game(5)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.winner:
            if keys[pygame.K_3]:
                self.reset_game(3)
            elif keys[pygame.K_5]:
                self.reset_game(5)
            elif keys[pygame.K_7]:
                self.reset_game(7)
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        else:
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def reset_game(self, winning_score):
        self.winning_score = winning_score
        self.player_score = 0
        self.ai_score = 0
        self.winner = None
        self.ball.reset()
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50

    def update(self):
        if self.winner is None:
            # --- MODIFIED FOR TASK 4 ---
            # Store old velocities to detect if a bounce/hit occurred
            old_vx = self.ball.velocity_x
            old_vy = self.ball.velocity_y

            self.ball.move()
            self.ball.check_collision(self.player, self.ai)

            # Check if velocities changed to play sounds
            if self.ball.velocity_x != old_vx:
                self.paddle_hit_sound.play()
            if self.ball.velocity_y != old_vy:
                self.wall_bounce_sound.play()
            # -------------------------

            if self.ball.x <= 0:
                self.ai_score += 1
                self.score_sound.play() # --- NEW FOR TASK 4 ---
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.score_sound.play() # --- NEW FOR TASK 4 ---
                self.ball.reset()

            self.ai.auto_track(self.ball, self.height)

            if self.player_score >= self.winning_score:
                self.winner = "Player Wins!"
            elif self.ai_score >= self.winning_score:
                self.winner = "AI Wins!"

    def render(self, screen):
        if self.winner:
            winner_text = self.font.render(self.winner, True, WHITE)
            text_rect = winner_text.get_rect(center=(self.width//2, self.height//2 - 40))
            screen.blit(winner_text, text_rect)

            replay_text = self.font.render("Play Again: Best of 3, 5, or 7 | ESC to Exit", True, WHITE)
            replay_rect = replay_text.get_rect(center=(self.width//2, self.height//2 + 20))
            screen.blit(replay_text, replay_rect)
        else:
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width * 3//4, 20))