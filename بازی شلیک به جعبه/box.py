import pygame
import random
import sys
import arabic_reshaper
from bidi.algorithm import get_display
import time

pygame.init()

gold_color = (255, 215, 0)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("بازی شلیک به جعبه‌ها")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

farsi_font_path = r"G:\python\بازی شلیک به جعبه\Vazirmatn-Medium.ttf"
font = pygame.font.Font(farsi_font_path, 50)
small_font = pygame.font.Font(farsi_font_path, 36)

# تصاویر
player_img = pygame.transform.scale(
    pygame.image.load(r"G:\python\بازی شلیک به جعبه\سفینه.png").convert_alpha(), (100, 100)
)
box_img = pygame.transform.scale(
    pygame.image.load(r"G:\python\بازی شلیک به جعبه\box.png").convert_alpha(), (50, 50)
)
bullet_img = pygame.image.load(r"G:\python\بازی شلیک به جعبه\ابی.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (15, 20))

menu_background_img = pygame.transform.scale(
    pygame.image.load(r"G:\python\بازی شلیک به جعبه\صفحه اول.png").convert(), (WIDTH, HEIGHT)
)
game_over_background_img = pygame.transform.scale(
    pygame.image.load(r"G:\python\بازی شلیک به جعبه\صفحه ی اخر.png").convert(), (WIDTH, HEIGHT)
)
game_background_img = pygame.transform.scale(
    pygame.image.load(r"G:\python\بازی شلیک به جعبه\فضا.png").convert(), (WIDTH, HEIGHT)
)
instructions_background_img = pygame.transform.scale(
    pygame.image.load(r"G:\python\بازی شلیک به جعبه\توضیحات.png").convert(), (WIDTH, HEIGHT)
)

# بونوس‌ها
bonus_green_img = pygame.transform.scale(
    pygame.image.load(r"G:\python\بازی شلیک به جعبه\سبز1.png").convert_alpha(), (40, 40)
)
bonus_gold_img = pygame.transform.scale(
    pygame.image.load(r"G:\python\بازی شلیک به جعبه\طلایی.png").convert_alpha(), (40, 40)
)
bonus_red_img = pygame.transform.scale(
    pygame.image.load(r"G:\python\بازی شلیک به جعبه\قرمز.png").convert_alpha(), (40, 40)
)

def render_farsi_text(text, font, color):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return font.render(bidi_text, True, color)

def draw_centered_text(text_surface, y):
    rect = text_surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surface, rect)

class Player:
    def __init__(self):
        self.image = player_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 7
        self.bullets = []  # هر تیر: [x, y, dx, dy]
        self.triple_shot = False
        self.auto_fire = False
        self.weak_shot = False
        self.last_auto_shot_time = 0
        self.bullet_speed = 10

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            screen.blit(bullet_img, (bullet[0], bullet[1]))

    def move(self, dx):
        self.x += dx * self.speed
        self.x = max(0, min(WIDTH - self.width, self.x))

    def shoot(self):
        """
        تیرها را به صورت [x, y, dx, dy] اضافه می‌کنیم.
        dx مقدار تغییر افقی در هر فریم است (برای زاویه).
        dy سرعت عمودی تیر است (مقداری که y با آن کاهش می‌یابد).
        """
        speed = self.bullet_speed if not self.weak_shot else max(1, self.bullet_speed // 2)
        if self.triple_shot:
            # سه تیر: چپ، وسط، راست
            center_x = self.x + self.width // 2 - bullet_img.get_width() // 2
            # مقادیر dx را می‌توانی بسته به زاویه دلخواه تنظیم کنی
            left_dx = -3
            mid_dx = 0
            right_dx = 3
            self.bullets.append([center_x, self.y, left_dx, speed])
            self.bullets.append([center_x, self.y, mid_dx, speed])
            self.bullets.append([center_x, self.y, right_dx, speed])
        else:
            center_x = self.x + self.width // 2 - bullet_img.get_width() // 2
            self.bullets.append([center_x, self.y, 0, speed])

    def update_bullets(self):
        for bullet in self.bullets[:]:
            # حرکت عمودی و افقی تیر
            bullet[1] -= bullet[3]  # y -= dy
            bullet[0] += bullet[2]  # x += dx
            # حذف تیر‌هایی که از صفحه خارج شدند
            if bullet[1] < -20 or bullet[0] < -50 or bullet[0] > WIDTH + 50:
                try:
                    self.bullets.remove(bullet)
                except ValueError:
                    pass

class Box:
    def __init__(self):
        self.image = box_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.reset()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def reset(self):
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(-200, -50)
        self.speed = random.randint(3, 6)
        self.hp = 1

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.reset()

class BonusBox(Box):
    def __init__(self, bonus_type):
        super().__init__()
        self.bonus_type = bonus_type
        if bonus_type == "triple":
            self.image = bonus_green_img
        elif bonus_type == "auto":
            self.image = bonus_gold_img
        elif bonus_type == "weak":
            self.image = bonus_red_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()

STATE_MENU = 0
STATE_INSTRUCTIONS = 3
STATE_PLAYING = 1
STATE_GAME_OVER = 2

best_score = 0

def game_loop():
    global best_score
    game_state = STATE_MENU
    player = Player()
    boxes = [Box() for _ in range(5)]
    bonus_boxes = []
    score = 0

    triple_shot_end_time = 0
    auto_fire_end_time = 0
    weak_shot_end_time = 0

    clock = pygame.time.Clock()
    current_time = 0

    start_text = render_farsi_text("برای شروع Enter را فشار دهید", small_font, GREEN)
    instructions_text = render_farsi_text("برای دیدن توضیحات Alt را فشار دهید", small_font, RED)
    move_text = render_farsi_text("حرکت با: چپ , راست", small_font, WHITE)
    shoot_text = render_farsi_text("تیر زدن با: Space", small_font, WHITE)
    back_to_menu_text = render_farsi_text("برای برگشت به منو Enter یا ESC را بزنید", small_font, GREEN)
    retry_text = render_farsi_text("برای شروع دوباره Enter را فشار دهید", small_font, GREEN)
    esc_text = render_farsi_text("برای رفتن به منو ESC را بزنید", small_font, RED)

    while True:
        screen.fill((0, 0, 0))
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_state == STATE_MENU:
                    if event.key == pygame.K_RETURN:
                        game_state = STATE_PLAYING
                        player = Player()
                        boxes = [Box() for _ in range(5)]
                        bonus_boxes.clear()
                        score = 0
                    elif event.key in (pygame.K_LALT, pygame.K_RALT):
                        game_state = STATE_INSTRUCTIONS

                elif game_state == STATE_INSTRUCTIONS:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        game_state = STATE_MENU

                elif game_state == STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        player.shoot()

                elif game_state == STATE_GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        game_state = STATE_PLAYING
                        player = Player()
                        boxes = [Box() for _ in range(5)]
                        bonus_boxes.clear()
                        score = 0
                    elif event.key == pygame.K_ESCAPE:
                        game_state = STATE_MENU

        keys = pygame.key.get_pressed()

        if game_state == STATE_MENU:
            screen.blit(menu_background_img, (0, 0))
            draw_centered_text(start_text, HEIGHT - 80)
            draw_centered_text(instructions_text, HEIGHT - 40)
            best_score_text = render_farsi_text(f"بهترین امتیاز: {best_score}", small_font, gold_color)
            draw_centered_text(best_score_text, HEIGHT // 2 - 50)

        elif game_state == STATE_INSTRUCTIONS:
            screen.blit(instructions_background_img, (0, 0))
            screen.blit(move_text, (WIDTH - move_text.get_width() - 10, 10))
            screen.blit(shoot_text, (10, 10))
            draw_centered_text(back_to_menu_text, HEIGHT - 60)

        elif game_state == STATE_PLAYING:
            screen.blit(game_background_img, (0, 0))

            if keys[pygame.K_LEFT]:
                player.move(-1)
            if keys[pygame.K_RIGHT]:
                player.move(1)

            if player.auto_fire and current_time - player.last_auto_shot_time > 0.2:
                player.shoot()
                player.last_auto_shot_time = current_time

            player.update_bullets()
            for box in boxes:
                box.update()
            for b in bonus_boxes:
                b.update()

            # برخورد تیر با جعبه‌ها و بونوس‌ها
            for bullet in player.bullets[:]:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_img.get_width(), bullet_img.get_height())
                hit = False
                for box in boxes[:]:
                    if bullet_rect.colliderect(box.rect()):
                        boxes.remove(box)
                        boxes.append(Box())
                        score += 1
                        hit = True
                        break
                for b in bonus_boxes[:]:
                    if bullet_rect.colliderect(b.rect()):
                        # فقط حذف بونوس، فعال نشود
                        bonus_boxes.remove(b)
                        hit = True
                        break
                if hit:
                    try:
                        player.bullets.remove(bullet)
                    except ValueError:
                        pass

            # برخورد پلیر با BonusBox
            for b in bonus_boxes[:]:
                if b.rect().colliderect(player.rect()):
                    if b.bonus_type == "triple":
                        player.triple_shot = True
                        triple_shot_end_time = current_time + 10
                    elif b.bonus_type == "auto":
                        player.auto_fire = True
                        auto_fire_end_time = current_time + 10
                    elif b.bonus_type == "weak":
                        player.weak_shot = True
                        weak_shot_end_time = current_time + 10
                    bonus_boxes.remove(b)

            # غیرفعال کردن بونوس‌ها بعد از زمان
            if player.triple_shot and current_time > triple_shot_end_time:
                player.triple_shot = False
            if player.auto_fire and current_time > auto_fire_end_time:
                player.auto_fire = False
            if player.weak_shot and current_time > weak_shot_end_time:
                player.weak_shot = False

            # شانس تولید بونوس
            if random.randint(1, 500) == 1:
                bonus_type = random.choice(["triple", "auto", "weak"])
                bonus_boxes.append(BonusBox(bonus_type))

            player.draw()
            for box in boxes:
                box.draw()
            for b in bonus_boxes:
                b.draw()

            score_text = render_farsi_text(f"امتیاز: {score}", small_font, WHITE)
            screen.blit(score_text, (10, 10))

            for box in boxes:
                if box.rect().colliderect(player.rect()):
                    game_state = STATE_GAME_OVER
                    if score > best_score:
                        best_score = score

        elif game_state == STATE_GAME_OVER:
            screen.blit(game_over_background_img, (0, 0))
            draw_centered_text(retry_text, HEIGHT - 80)
            draw_centered_text(esc_text, HEIGHT - 40)
            score_text = render_farsi_text(f"امتیاز: {score}", font, RED)
            draw_centered_text(score_text, HEIGHT // 2 - 50)
            best_score_text = render_farsi_text(f"بهترین امتیاز: {best_score}", small_font, gold_color)
            draw_centered_text(best_score_text, HEIGHT // 2 + 10)

        pygame.display.flip()
        clock.tick(60)

game_loop()
