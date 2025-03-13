import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bard")

# Load background image
bg_image = pygame.image.load("./assets/hd_ Angry.jpeg")  # Replace with your image path
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)

# Font
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def game_loop():
    bird_x, bird_y = 100, HEIGHT // 2
    bird_radius = 20
    grav = 0.5
    velocity = 0
    jump_strength = -8

    pipes = []
    pipe_width = 60
    pipe_gap = 150
    pipe_speed = 3
    pipe_spawn_timer = 90
    score = 0
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.blit(bg_image, (0, 0))
        draw_text(f"Score: {score}", 20, 20)
        
        # Bird physics
        velocity += grav
        bird_y += velocity
        pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)
        
        # Pipe generation
        pipe_spawn_timer -= 1
        if pipe_spawn_timer <= 0:
            pipe_spawn_timer = 90
            pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
            pipes.append([WIDTH, pipe_height])
        
        # Move and draw pipes
        for pipe in pipes[:]:
            pipe[0] -= pipe_speed
            pygame.draw.rect(screen, GREEN, (pipe[0], 0, pipe_width, pipe[1]))
            pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap))
            if pipe[0] + pipe_width < 0:
                pipes.remove(pipe)
                score += 1
        
        # Collision detection
        for pipe in pipes:
            if (bird_x + bird_radius > pipe[0] and bird_x - bird_radius < pipe[0] + pipe_width):
                if bird_y - bird_radius < pipe[1] or bird_y + bird_radius > pipe[1] + pipe_gap:
                    running = False
        if bird_y + bird_radius > HEIGHT or bird_y - bird_radius < 0:
            running = False
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = jump_strength
        
        pygame.display.update()
        clock.tick(30)
    
    # Game over screen
    screen.fill(WHITE)
    draw_text("Game Over! Press R to Restart", WIDTH // 4, HEIGHT // 2, RED)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                    return

game_loop()
