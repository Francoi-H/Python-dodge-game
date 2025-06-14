import pygame
import sys
from game_logic import Player, Block, check_collision
import random
from utils import init_log, log_event

pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DodgeMaster")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player = Player(WIDTH // 2, HEIGHT - 50)
blocks = []
score = 0
spawn_timer = 0

init_log()
running = True
while running:
    CLOCK.tick(60)
    SCREEN.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.move(-5)
    if keys[pygame.K_RIGHT]: player.move(5)

    spawn_timer += 1
    if spawn_timer >= 30:
        blocks.append(Block(random.randint(0, WIDTH-50), 0))
        spawn_timer = 0

    for block in blocks[:]:
        block.move()
        if block.y > HEIGHT:
            blocks.remove(block)
            score += 1
            log_event("missed", player.rect.x, block.rect.y, score)
        elif check_collision(player, block):
            log_event("hit", player.rect.x, block.rect.y, score)
            print("GAME OVER")
            running = False

    player.draw(SCREEN)
    for block in blocks:
        block.draw(SCREEN)
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
