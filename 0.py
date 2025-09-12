import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot the Boxes - Restartable")

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

player_size = 50
player_speed = 7

bullets = []
bullet_speed = 10

box_size = 50
box_speed = 1.5
num_boxes_per_row = 10
num_rows = 2

# بارگذاری تصاویر (باید این فایل‌ها رو داشته باشی)
box_img = pygame.image.load("box.png")
box_img = pygame.transform.scale(box_img, (box_size, box_size))

bullet_img = pygame.image.load("bullet.png")
bullet_width = bullet_img.get_width()
bullet_height = bullet_img.get_height()

clock = pygame.time.Clock()

font_big = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

def spawn_boxes():
    boxes = []
    x_margin = (WIDTH - (box_size * num_boxes_per_row)) // (num_boxes_per_row + 1)
    y_start = 20
    for row in range(num_rows):
        for col in range(num_boxes_per_row):
            x = x_margin + col * (box_size + x_margin)
            y = y_start + row * (box_size + 10)
            boxes.append([x, y])
    return boxes

def reset_game():
    global player_x, player_y, bullets, boxes, game_over
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    bullets = []
    boxes = spawn_boxes()
    game_over = False

reset_game()

running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + player_size // 2 - bullet_width // 2, player_y])
        elif game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # وقتی اینتر فشار داده شد
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # حرکت گلوله‌ها
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] + bullet_height < 0:
                bullets.remove(bullet)

        # حرکت جعبه‌ها
        for box in boxes:
            box[1] += box_speed
            if box[1] > HEIGHT:
                box[1] = -box_size

        # برخورد گلوله با جعبه
        for bullet in bullets[:]:
            for box in boxes[:]:
                bx, by = box
                if (bx < bullet[0] < bx + box_size) and (by < bullet[1] < by + box_size):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    boxes.remove(box)
                    boxes.append([random.randint(0, WIDTH - box_size), -box_size])
                    break

        # برخورد بازیکن با جعبه
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for box in boxes:
            box_rect = pygame.Rect(box[0], box[1], box_size, box_size)
            if player_rect.colliderect(box_rect):
                game_over = True

    # رسم بازیکن
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

    # رسم گلوله‌ها
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))

    # رسم جعبه‌ها
    for box in boxes:
        screen.blit(box_img, (box[0], box[1]))

    # نمایش Game Over و گزینه شروع مجدد
    if game_over:
        text_game_over = font_big.render("GAME OVER", True, WHITE)
        screen.blit(text_game_over, (WIDTH//2 - text_game_over.get_width()//2, HEIGHT//2 - text_game_over.get_height()))
        
        text_restart = font_small.render("Press ENTER to Restart", True, WHITE)
        screen.blit(text_restart, (WIDTH//2 - text_restart.get_width()//2, HEIGHT//2 + 40))

    pygame.display.update()

pygame.quit()