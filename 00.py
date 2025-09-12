import pygame
import random

pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# اندازه‌ها
HEAD_SIZE = 30
BODY_SIZE = 30
FOOD_SIZE = 25

# بارگذاری عکس‌ها
try:
    snake_head_img = pygame.image.load('IMG_20190714_180128.jpg')
    snake_head_img = pygame.transform.scale(snake_head_img, (HEAD_SIZE, HEAD_SIZE))
except:
    print("خطا در بارگذاری عکس سر مار!")

try:
    food_img = pygame.image.load('IMG_20210319_111637.jpg')
    food_img = pygame.transform.scale(food_img, (FOOD_SIZE, FOOD_SIZE))
except:
    print("خطا در بارگذاری عکس غذا!")

snake_pos = [100, 50]
snake_body = [[100, 50], [100 - BODY_SIZE, 50], [100 - 2 * BODY_SIZE, 50]]
food_pos = [random.randrange(0, (width // FOOD_SIZE)) * FOOD_SIZE,
            random.randrange(0, (height // FOOD_SIZE)) * FOOD_SIZE]
food_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

font = pygame.font.SysFont('Arial', 24)


def draw_snake(surface, body):
    for i, pos in enumerate(body):
        x, y = pos
        rect = pygame.Rect(x, y, BODY_SIZE, BODY_SIZE)
        if i == 0:
            surface.blit(snake_head_img, (x, y))
        else:
            pygame.draw.rect(surface, (0, 180, 0), rect)
            pygame.draw.rect(surface, (0, 130, 0), rect.inflate(-8, -8))


def draw_food(surface, pos):
    surface.blit(food_img, (pos[0], pos[1]))


def game_over():
    game_over_surface = font.render('Game Over! Press any key to exit.', True, (255, 0, 0))
    game_over_rect = game_over_surface.get_rect(center=(width // 2, height // 2))
    screen.fill((0, 0, 0))
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting = False
    pygame.quit()
    quit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_pos[1] -= BODY_SIZE
    if direction == 'DOWN':
        snake_pos[1] += BODY_SIZE
    if direction == 'LEFT':
        snake_pos[0] -= BODY_SIZE
    if direction == 'RIGHT':
        snake_pos[0] += BODY_SIZE

    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(0, (width // FOOD_SIZE)) * FOOD_SIZE,
                    random.randrange(0, (height // FOOD_SIZE)) * FOOD_SIZE]
        food_spawn = True

    screen.fill((20, 20, 20))
    draw_snake(screen, snake_body)
    draw_food(screen, food_pos)

    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    if (snake_pos[0] < 0 or snake_pos[0] > width - BODY_SIZE or
            snake_pos[1] < 0 or snake_pos[1] > height - BODY_SIZE):
        game_over()

    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    pygame.display.set_caption(f'Snake Game | Score: {score}')
    pygame.display.update()
    clock.tick(10)
