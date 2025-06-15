import os
import pygame
import sys
import random
from pygame.locals import *
import math


def main():
    global WIDTH, HEIGHT, screen, clock
    global bird_x, bird_y, bird_z, bird_radius, bird_vel
    global bird_gravity, bird_jump
    global pipe_width, pipe_gap, pipe_depth, pipes, pipe_speed
    global pipe_interval, last_pipe, score, font

    # Initialize Pygame
    pygame.init()
    WIDTH, HEIGHT = 600, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Flopping Bird")
    clock = pygame.time.Clock()

    # Bird properties
    bird_x, bird_y = WIDTH // 3, HEIGHT // 2
    bird_z = 0
    bird_radius = 30
    bird_vel = 0
    bird_gravity = 0.7
    bird_jump = -10


    # Pipe properties
    pipe_width = 100
    pipe_gap = 220
    pipe_depth = 200
    pipes = []
    pipe_speed = 5
    pipe_interval = 1500
    last_pipe = pygame.time.get_ticks()

    score = 0
    font = pygame.font.SysFont(None, 48)

def draw_bird(x, y, z):
    scale = 1 + z / 400
    r = int(bird_radius * scale)
    pygame.draw.ellipse(screen, (255, 255, 0), (x - r, y - r, r * 2, r * 2))
    pygame.draw.circle(screen, (0, 0, 0), (x + r//2, y - r//2), r//5)

def draw_pipe(pipe):
    x, y, z, gap = pipe
    scale = 1 + z / 400
    w = int(pipe_width * scale)
    # Top pipe
    pygame.draw.rect(screen, (0, 200, 0), (x - w//2, 0, w, y - gap//2))
    # Bottom pipe
    pygame.draw.rect(screen, (0, 200, 0), (x - w//2, y + gap//2, w, HEIGHT - (y + gap//2)))

def check_collision(bird_x, bird_y, bird_z, pipes):
    scale = 1 + bird_z / 400
    r = int(bird_radius * scale)
    for pipe in pipes:
        x, y, z, gap = pipe
        p_scale = 1 + z / 400
        w = int(pipe_width * p_scale)
        # Remove z-axis check for collision
        if (bird_x + r > x - w//2 and bird_x - r < x + w//2):
            if bird_y - r < y - gap//2 or bird_y + r > y + gap//2:
                return True
    if bird_y - r < 0 or bird_y + r > HEIGHT:
        return True
    return False

    running = True
    while running:
        clock.tick(60)
        screen.fill((135, 206, 235))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird_vel = bird_jump

        # Bird physics
        bird_vel += bird_gravity
        bird_y += bird_vel

        # Pipes logic
        now = pygame.time.get_ticks()
        if now - last_pipe > pipe_interval:
            pipe_y = random.randint(200, HEIGHT - 200)
            pipe_z = random.randint(-100, 100)
            pipes.append([WIDTH + pipe_width, pipe_y, pipe_z, pipe_gap])
            last_pipe = now

        for pipe in pipes:
            pipe[0] -= pipe_speed

        # Remove off-screen pipes
        pipes = [p for p in pipes if p[0] > -pipe_width]

        # Draw pipes
        for pipe in pipes:
            draw_pipe(pipe)

        # Draw bird
        draw_bird(bird_x, bird_y, bird_z)

        # Collision
        if check_collision(bird_x, bird_y, bird_z, pipes):
            running = False

        # Score
        for pipe in pipes:
            if 'scored' not in pipe and pipe[0] + pipe_width//2 < bird_x:
                score += 1
                pipe.append('scored')

        score_surf = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()



# Game over - display final score and quit Pygame
pygame.quit()
print(f"Final Score: {score}")

# Simple restart option using command line
try:
    restart = input("Play again? (y/n): ").strip().lower()
    if restart == 'y':
        os.execl(sys.executable, sys.executable, *sys.argv)
except EOFError:
    pass

