import pygame
import random
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bard Extreme")

# Load assets
bg_image = pygame.image.load("./assets/hd_ Angry.jpeg").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
bird_imgs = [
    pygame.transform.scale(pygame.image.load("./assets/bird1.png").convert_alpha(), (40, 40)),
    pygame.transform.scale(pygame.image.load("./assets/bird2.png").convert_alpha(), (40, 40))
]
pipe_img = pygame.transform.scale(pygame.image.load("./assets/pipe.png").convert_alpha(), (80, 400))
ground_img = pygame.transform.scale(pygame.image.load("./assets/ground.png").convert_alpha(), (WIDTH, 60))

# Sounds
jump_sound = pygame.mixer.Sound("./assets/jump.mp3")
score_sound = pygame.mixer.Sound("./assets/score.mp3")
hit_sound = pygame.mixer.Sound("./assets/hit.mp3")

# Colors
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# Font
font = pygame.font.Font("./assets/flappy-font.ttf", 36)
game_over_font = pygame.font.Font("./assets/flappy-font.ttf", 48)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-5, -1)
        self.life = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 2

    def draw(self):
        if self.life > 0:
            alpha = min(255, self.life * 8)
            pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), 3)

def draw_text(text, x, y, color=GOLD, font=font):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def game_loop():
    bird_rect = pygame.Rect(100, HEIGHT//2, 40, 40)
    bird_anim = 0
    bird_angle = 0
    gravity = 0.5
    velocity = 0
    jump = -8

    pipes = []
    pipe_gap = 150
    pipe_speed = 3
    pipe_timer = 90
    score = 0
    ground_scroll = 0
    particles = []

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(bg_image, (0, 0))

        # Ground scrolling
        ground_scroll = (ground_scroll - pipe_speed) % -WIDTH
        screen.blit(ground_img, (ground_scroll, HEIGHT-60))
        screen.blit(ground_img, (ground_scroll + WIDTH, HEIGHT-60))

        # Bird animation
        bird_anim = (bird_anim + 0.2) % 2
        rotated_bird = pygame.transform.rotate(bird_imgs[int(bird_anim)], bird_angle)
        bird_rect = rotated_bird.get_rect(center=(100, bird_rect.centery))
        screen.blit(rotated_bird, bird_rect)

        # Bird physics
        velocity += gravity
        bird_rect.centery += velocity
        bird_angle = max(-30, min(velocity * -5, 30))

        # Pipes
        pipe_timer -= 1
        if pipe_timer <= 0:
            pipe_timer = 90
            gap_y = random.randint(100, HEIGHT - pipe_gap - 100)
            pipes.extend([
                {"x": WIDTH, "y": gap_y - 400, "scored": False},
                {"x": WIDTH, "y": gap_y + pipe_gap, "scored": False}
            ])

        for pipe in pipes[:]:
            pipe["x"] -= pipe_speed
            screen.blit(pipe_img, (pipe["x"], pipe["y"]))
            
            # Collision
            pipe_rect = pygame.Rect(pipe["x"], pipe["y"], 80, 400)
            if bird_rect.colliderect(pipe_rect):
                hit_sound.play()
                running = False

            if pipe["x"] < -80:
                pipes.remove(pipe)
                if pipe["y"] > HEIGHT//2 and not pipe["scored"]:
                    score += 0.5
                    pipe["scored"] = True
                    score_sound.play()

        # Score display
        draw_text(f"{int(score)}", WIDTH//2 - 20, 50)

        # Particles
        for p in particles[:]:
            p.update()
            p.draw()
            if p.life <= 0:
                particles.remove(p)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = jump
                    jump_sound.play()
                    particles.extend([Particle(bird_rect.centerx, bird_rect.centery) for _ in range(8)])

        pygame.display.update()
        clock.tick(30)

    # Game Over
    screen.fill((0, 0, 0))
    draw_text("Game Over!", WIDTH//4, HEIGHT//3, font=game_over_font)
    draw_text(f"Score: {int(score)}", WIDTH//3, HEIGHT//2)
    draw_text("Press R to Restart", WIDTH//6, HEIGHT*2//3)
    pygame.display.update()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_loop()
            return

game_loop()