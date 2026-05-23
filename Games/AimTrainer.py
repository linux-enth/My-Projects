import pygame
import sys
import random
import math
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Aim Trainer")

pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
# Colors
BACKGROUND = (15, 15, 25)
TEXT_COLOR = (220, 220, 255)
TARGET_COLOR = (255, 50, 50)
TARGET_HIGHLIGHT = (255, 150, 150)
HIT_COLOR = (50, 200, 50)
MISS_COLOR = (255, 100, 100)
UI_BG = (30, 30, 45)
UI_BORDER = (60, 60, 90)

# Game variables
score = 0
targets_hit = 0
targets_missed = 0
accuracy = 100.0
game_time = 60  # seconds
start_time = time.time()
time_left = game_time
game_active = True
targets = []
target_radius = 30
spawn_rate = 0.5  # seconds between spawns
last_spawn_time = 0

# Fonts
font_large = pygame.font.SysFont("Arial", 36, bold=True)
font_medium = pygame.font.SysFont("Arial", 24)
font_small = pygame.font.SysFont("Arial", 18)

class Target:
    def __init__(self):
        self.radius = target_radius
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.spawn_time = time.time()
        self.lifetime = 3.0  # seconds
        self.active = True
        self.color = TARGET_COLOR
        
    def update(self):
        # Check if target has expired
        if time.time() - self.spawn_time > self.lifetime:
            self.active = False
            return False
        return True
    
    def draw(self):
        # Draw target with pulsing effect
        time_alive = time.time() - self.spawn_time
        pulse = 0.8 + 0.2 * math.sin(time_alive * 10)
        current_radius = int(self.radius * pulse)
        
        # Draw outer circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), current_radius)
        
        # Draw inner circle
        pygame.draw.circle(screen, TARGET_HIGHLIGHT, (self.x, self.y), current_radius // 2)
        
        # Draw center dot
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), current_radius // 4)
    
    def is_clicked(self, pos):
        distance = math.sqrt((self.x - pos[0])**2 + (self.y - pos[1])**2)
        return distance <= self.radius

def draw_ui():
    # Draw background for UI
    pygame.draw.rect(screen, UI_BG, (0, 0, WIDTH, 80))
    pygame.draw.line(screen, UI_BORDER, (0, 80), (WIDTH, 80), 2)
    
    # Draw score
    score_text = font_large.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 20))
    
    # Draw time
    time_text = font_medium.render(f"Time: {int(time_left)}s", True, TEXT_COLOR)
    screen.blit(time_text, (WIDTH - 150, 20))
    
    # Draw accuracy
    accuracy_text = font_medium.render(f"Accuracy: {accuracy:.1f}%", True, TEXT_COLOR)
    screen.blit(accuracy_text, (WIDTH - 150, 50))
    
    # Draw targets hit/missed
    targets_text = font_small.render(f"Hit: {targets_hit} | Missed: {targets_missed}", True, TEXT_COLOR)
    screen.blit(targets_text, (WIDTH // 2 - 80, 50))

def draw_game_over():
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Draw game over text
    game_over_text = font_large.render("GAME OVER", True, TEXT_COLOR)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    
    # Draw final score
    final_score_text = font_medium.render(f"Final Score: {score}", True, TEXT_COLOR)
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
    
    # Draw final accuracy
    final_accuracy_text = font_medium.render(f"Final Accuracy: {accuracy:.1f}%", True, TEXT_COLOR)
    screen.blit(final_accuracy_text, (WIDTH // 2 - final_accuracy_text.get_width() // 2, HEIGHT // 2 + 40))
    
    # Draw restart instruction
    restart_text = font_small.render("Press R to restart or ESC to quit", True, TEXT_COLOR)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

def reset_game():
    global score, targets_hit, targets_missed, accuracy, start_time, time_left, game_active, targets, last_spawn_time
    score = 0
    targets_hit = 0
    targets_missed = 0
    accuracy = 100.0
    start_time = time.time()
    time_left = game_time
    game_active = True
    targets = []
    last_spawn_time = time.time()

# Main game loop
clock = pygame.time.Clock()
while True:
    current_time = time.time()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r and not game_active:
                reset_game()
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_active:
            if event.button == 1:  # Left mouse button
                clicked = False
                for target in targets[:]:
                    if target.active and target.is_clicked(event.pos):
                        # Hit target
                        targets.remove(target)
                        score += 10
                        targets_hit += 1
                        accuracy = (targets_hit / (targets_hit + targets_missed)) * 100 if (targets_hit + targets_missed) > 0 else 100
                        clicked = True
                        
                        # Visual feedback for hit
                        pygame.draw.circle(screen, HIT_COLOR, event.pos, 40, 5)
                        pygame.display.flip()
                        pygame.time.delay(50)
                        break
                
                if not clicked:
                    # Missed all targets
                    targets_missed += 1
                    accuracy = (targets_hit / (targets_hit + targets_missed)) * 100 if (targets_hit + targets_missed) > 0 else 100
                    
                    # Visual feedback for miss
                    pygame.draw.circle(screen, MISS_COLOR, event.pos, 30, 3)
                    pygame.display.flip()
                    pygame.time.delay(50)
    
    # Game logic
    if game_active:
        # Update time
        time_left = game_time - (current_time - start_time)
        
        # Check if game is over
        if time_left <= 0:
            game_active = False
            time_left = 0
        
        # Spawn new targets
        if current_time - last_spawn_time > spawn_rate and time_left > 0:
            targets.append(Target())
            last_spawn_time = current_time
        
        # Update targets
        for target in targets[:]:
            if not target.update():
                targets.remove(target)
                targets_missed += 1
                accuracy = (targets_hit / (targets_hit + targets_missed)) * 100 if (targets_hit + targets_missed) > 0 else 100
    
    # Drawing
    screen.fill(BACKGROUND)
    
    # Draw targets
    for target in targets:
        target.draw()
    
    # Draw UI
    draw_ui()
    
    # Draw game over screen if game is over
    if not game_active:
        draw_game_over()
    
    pygame.display.flip()
    clock.tick(60)



