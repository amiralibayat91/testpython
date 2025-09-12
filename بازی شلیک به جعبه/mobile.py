from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
import random
import time
import arabic_reshaper
from bidi.algorithm import get_display

Window.size = (800, 600)

# مسیر تصاویر
player_img = r"G:\python\بازی شلیک به جعبه\سفینه.png"
box_img = r"G:\python\بازی شلیک به جعبه\box.png"
bullet_img = r"G:\python\بازی شلیک به جعبه\ابی.png"
bonus_green_img = r"G:\python\بازی شلیک به جعبه\سبز1.png"
bonus_red_img = r"G:\python\بازی شلیک به جعبه\قرمز.png"

# تابع برای رندر متن فارسی
def render_farsi_text(text, font_size=36, color=(1,1,1,1)):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return Label(text=bidi_text, font_size=font_size, color=color)

class Bullet(Image):
    dx = NumericProperty(0)
    dy = NumericProperty(10)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = bullet_img
        self.size = (15, 20)

class Box(Image):
    speed = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = box_img
        self.size = (50, 50)
        self.reset()

    def reset(self):
        self.pos = (random.randint(0, int(Window.width - self.width)),
                    Window.height + random.randint(50, 200))
        self.speed = random.randint(3, 6)

class BonusBox(Image):
    bonus_type = ''

    def __init__(self, bonus_type, **kwargs):
        super().__init__(**kwargs)
        self.bonus_type = bonus_type
        self.size = (40, 40)
        if bonus_type == 'triple':
            self.source = bonus_green_img
        elif bonus_type == 'weak':
            self.source = bonus_red_img
        self.reset()

    def reset(self):
        self.pos = (random.randint(0, int(Window.width - self.width)),
                    Window.height + random.randint(50, 200))
        self.speed = random.randint(2, 5)

class Player(Image):
    auto_fire_active = BooleanProperty(False)
    bullet_speed = NumericProperty(10)
    triple_shot = BooleanProperty(False)
    weak_shot = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = player_img
        self.size = (100, 100)
        self.pos = (Window.width/2 - 50, 50)

class Game(Widget):
    player = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = 'menu'  # حالت بازی: menu, playing, gameover
        self.player = Player()
        self.add_widget(self.player)

        self.boxes = []
        self.bonus_boxes = []
        self.bullets = []
        self.score = 0
        self.best_score = 0

        # اضافه کردن جعبه‌ها
        for _ in range(5):
            box = Box()
            self.boxes.append(box)
            self.add_widget(box)

        self.last_auto_shot_time = 0
        self.triple_shot_end_time = 0
        self.weak_shot_end_time = 0

        # متن‌ها
        self.start_label = render_farsi_text('برای شروع لمس کنید', 36, (0,1,0,1))
        self.start_label.pos = (Window.width/2 - 150, Window.height/2)
        self.add_widget(self.start_label)

        Clock.schedule_interval(self.update, 1/60.)

    def on_touch_down(self, touch):
        if self.state == 'menu':
            self.state = 'playing'
            self.remove_widget(self.start_label)
            return True

        if self.state == 'playing':
            self.player.auto_fire_active = True
            self.player.center_x = touch.x
            return True

    def on_touch_move(self, touch):
        if self.state == 'playing':
            self.player.center_x = touch.x
            return True

    def on_touch_up(self, touch):
        if self.state == 'playing':
            self.player.auto_fire_active = False
            return True

    def shoot(self):
        speed = self.player.bullet_speed
        if self.player.weak_shot:
            speed = max(1, speed // 2)
        if self.player.triple_shot:
            offsets = [-20, 0, 20]
            for dx in offsets:
                bullet = Bullet(pos=(self.player.center_x + dx, self.player.top))
                bullet.dy = speed
                self.bullets.append(bullet)
                self.add_widget(bullet)
        else:
            bullet = Bullet(pos=(self.player.center_x, self.player.top))
            bullet.dy = speed
            self.bullets.append(bullet)
            self.add_widget(bullet)

    def update(self, dt):
        current_time = time.time()

        if self.state == 'playing':
            if self.player.auto_fire_active and current_time - self.last_auto_shot_time > 0.2:
                self.shoot()
                self.last_auto_shot_time = current_time

            for bullet in self.bullets[:]:
                bullet.y += bullet.dy
                bullet.x += bullet.dx
                if bullet.y > Window.height:
                    self.bullets.remove(bullet)
                    self.remove_widget(bullet)
                    continue
                for box in self.boxes[:]:
                    if bullet.collide_widget(box):
                        self.score += 1
                        box.reset()
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                            self.remove_widget(bullet)
                        break
                for b in self.bonus_boxes[:]:
                    if bullet.collide_widget(b):
                        if b.bonus_type == 'triple':
                            self.player.triple_shot = True
                            self.triple_shot_end_time = current_time + 10
                        elif b.bonus_type == 'weak':
                            self.player.weak_shot = True
                            self.weak_shot_end_time = current_time + 10
                        self.bonus_boxes.remove(b)
                        self.remove_widget(b)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                            self.remove_widget(bullet)

            if self.player.triple_shot and current_time > self.triple_shot_end_time:
                self.player.triple_shot = False
            if self.player.weak_shot and current_time > self.weak_shot_end_time:
                self.player.weak_shot = False

            if random.randint(1, 500) == 1:
                bonus_type = random.choice(['triple', 'weak'])
                b = BonusBox(bonus_type)
                self.bonus_boxes.append(b)
                self.add_widget(b)

            for box in self.boxes:
                box.y -= box.speed
                if box.y < -box.height:
                    box.reset()

            for b in self.bonus_boxes:
                b.y -= b.speed
                if b.y < -b.height:
                    self.bonus_boxes.remove(b)
                    self.remove_widget(b)

            # بررسی برخورد پلیر با جعبه‌ها
            for box in self.boxes:
                if box.collide_widget(self.player):
                    self.state = 'gameover'
                    if self.score > self.best_score:
                        self.best_score = self.score
                    self.show_gameover()

    def show_gameover(self):
        self.gameover_label = render_farsi_text(f'بازی تمام شد! امتیاز: {self.score}', 36, (1,0,0,1))
        self.gameover_label.pos = (Window.width/2 - 200, Window.height/2)
        self.add_widget(self.gameover_label)

class ShooterApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    ShooterApp().run()
