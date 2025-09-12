import pygame
import random

pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

snake_pos = [100, 50]
snake_body = [[100,50], [90,50], [80,50]]
food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
food_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

font = pygame.font.SysFont('Arial', 24)

def draw_snake(surface, body):
    for i, pos in enumerate(body):
        x, y = pos
        rect = pygame.Rect(x, y, 10, 10)
        # رنگ مار: سر روشن‌تر، بدن کمی تیره‌تر
        if i == 0:
            pygame.draw.rect(surface, (0, 255, 0), rect)  # سر مار سبز روشن
            pygame.draw.rect(surface, (0, 200, 0), rect.inflate(-4, -4))  # سایه سر
        else:
            pygame.draw.rect(surface, (0, 180, 0), rect)  # بدن سبز تیره‌تر
            pygame.draw.rect(surface, (0, 130, 0), rect.inflate(-4, -4))  # سایه بدن

def draw_food(surface, pos):
    x, y = pos
    center = (x + 5, y + 5)
    pygame.draw.circle(surface, (255, 0, 0), center, 6)  # دایره قرمز بزرگتر
    pygame.draw.circle(surface, (255, 100, 100), center, 4)  # دایره کوچک‌تر برای افکت

def game_over():
    game_over_surface = font.render('Game Over!', True, (255, 0, 0))
    game_over_rect = game_over_surface.get_rect(center=(width//2, height//2))
    screen.fill((0,0,0))
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
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//100)) * 10]
        food_spawn = True

    screen.fill((20, 20, 20))  # پس‌زمینه خاکستری خیلی تیره
    draw_snake(screen, snake_body)
    draw_food(screen, food_pos)

    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    # برخورد با دیوار
    if snake_pos[0] < 0 or snake_pos[0] > width-10 or snake_pos[1] < 0 or snake_pos[1] > height-10:
        game_over()
    # برخورد با خودش
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    pygame.display.set_caption(f'مار بازی ,امتیاز: {score}')
    pygame.display.update()
    clock.tick(15)
