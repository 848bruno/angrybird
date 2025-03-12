import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Bard")

# Colors
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)

# Load assets (Replace with actual paths or use placeholders)
bard_image = pygame.Surface((80, 80))
bard_image.fill(RED)
note_image = pygame.Surface((20, 20))
note_image.fill(BLUE)
knight_image = pygame.Surface((50, 50))
knight_image.fill(GREEN)

# Bard position
bard_x, bard_y = 100, HEIGHT - 120

# Enemy knights
knights = [(random.randint(500, WIDTH - 50), HEIGHT - 80) for _ in range(3)]

# Notes (projectiles)
notes = []

# Game loop variables
running = True
clock = pygame.time.Clock()
grav = 0.5

while running:
    screen.fill(WHITE)
    screen.blit(bard_image, (bard_x, bard_y))
    
    # Draw knights
    for knight in knights:
        screen.blit(knight_image, knight)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - bard_y, mouse_x - bard_x)
            speed = 10
            notes.append([bard_x + 40, bard_y + 40, math.cos(angle) * speed, math.sin(angle) * speed])
    
    # Move and draw notes
    for note in notes[:]:
        note[0] += note[2]  # X movement
        note[1] += note[3]  # Y movement
        note[3] += grav  # Apply gravity
        screen.blit(note_image, (note[0], note[1]))
        if note[0] > WIDTH or note[1] > HEIGHT:
            notes.remove(note)
    
    # Collision detection
    for note in notes[:]:
        for knight in knights[:]:
            knight_rect = pygame.Rect(knight[0], knight[1], 50, 50)
            note_rect = pygame.Rect(note[0], note[1], 20, 20)
            if note_rect.colliderect(knight_rect):
                knights.remove(knight)
                notes.remove(note)
                break
    
    # Update display
    pygame.display.update()
    clock.tick(30)

pygame.quit()
