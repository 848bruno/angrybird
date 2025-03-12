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
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)

# Load assets
background = pygame.image.load("./assets/hd_Angry.jpeg")  # Add a medieval background
bard_image = pygame.image.load("./assets/Birds.png")
note_image = pygame.image.load("note.png")
knight_image = pygame.image.load("./assets/night.png")

# Scale images
bard_image = pygame.transform.scale(bard_image, (80, 80))
note_image = pygame.transform.scale(note_image, (20, 20))
knight_image = pygame.transform.scale(knight_image, (50, 50))

# Bard position
bard_x, bard_y = 100, HEIGHT - 120

# Enemy knights
knights = [(random.randint(500, WIDTH - 50), HEIGHT - 80) for _ in range(3)]

# Notes (projectiles)
notes = []

# Fonts and text
font = pygame.font.Font(None, 36)
score = 0

def draw_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Game loop variables
running = True
clock = pygame.time.Clock()
grav = 0.5

while running:
    screen.blit(background, (0, 0))
    screen.blit(bard_image, (bard_x, bard_y))
    draw_text(f"Score: {score}", 20, 20)
    
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
                score += 10
                break
    
    # Check for win condition
    if not knights:
        draw_text("You Win!", WIDTH//2 - 50, HEIGHT//2, RED)
    
    # Update display
    pygame.display.update()
    clock.tick(30)

pygame.quit()
