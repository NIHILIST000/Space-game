import pygame
import random
import sys
import os

# --- НАСТРОЙКИ ---
WIDTH, HEIGHT = 950, 750
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 8
ENEMY_SPEED = 3
ASTEROID_SPEED = 2
SHIELD_DURATION = 120  # кадров (~2 сек)
MUSIC_VOLUME = 0.5

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Space Shooter")
clock = pygame.time.Clock()

# --- МУЗЫКА ---
music_path = "music"
if not os.path.exists(music_path):
    os.makedirs(music_path)

# Если есть музыка — включаем
music_files = [f for f in os.listdir(music_path) if f.endswith((".mp3", ".ogg", ".wav"))]
if music_files:
    pygame.mixer.music.load(os.path.join(music_path, random.choice(music_files)))
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)

# --- ШРИФТ ---
font = pygame.font.Font(None, 24)
medium_font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# --- ЦВЕТА ---
BLACK = (5, 5, 20)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 60, 60)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 100)
BLUE = (0, 150, 255)
GRAY = (180, 180, 180)
PURPLE = (180, 60, 220)

# --- УЛУЧШЕННЫЕ ПИКСЕЛЬНЫЕ МОДЕЛИ ---
def draw_player(surface, x, y):
    # Основной корпус
    pygame.draw.polygon(surface, CYAN, [(x, y - 12), (x - 8, y + 8), (x + 8, y + 8)])
    # Детализация
    pygame.draw.polygon(surface, BLUE, [(x, y - 8), (x - 4, y + 4), (x + 4, y + 4)])
    # Двигатели
    pygame.draw.rect(surface, YELLOW, (x - 3, y + 8, 2, 4))
    pygame.draw.rect(surface, YELLOW, (x + 1, y + 8, 2, 4))

def draw_enemy(surface, x, y):
    # Основной корпус
    pygame.draw.polygon(surface, RED, [(x, y + 12), (x - 10, y - 8), (x + 10, y - 8)])
    # Детализация
    pygame.draw.polygon(surface, PURPLE, [(x, y + 6), (x - 6, y - 4), (x + 6, y - 4)])
    # Оружие
    pygame.draw.rect(surface, YELLOW, (x - 8, y - 8, 3, 6))
    pygame.draw.rect(surface, YELLOW, (x + 5, y - 8, 3, 6))

def draw_asteroid(surface, x, y):
    # Неровная форма астероида
    points = []
    for i in range(8):
        angle = 2 * 3.14159 * i / 8
        radius = random.randint(8, 14)
        px = x + radius * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x
        py = y + radius * pygame.math.Vector2(1, 0).rotate(angle * 57.3).y
        points.append((px, py))
    pygame.draw.polygon(surface, GRAY, points)
    # Кратеры
    pygame.draw.circle(surface, (120, 120, 120), (x-4, y-3), 3)
    pygame.draw.circle(surface, (120, 120, 120), (x+5, y+2), 2)

def draw_bullet(surface, x, y):
    # Плазменный снаряд
    pygame.draw.rect(surface, YELLOW, (x - 2, y - 10, 4, 10))
    pygame.draw.rect(surface, (255, 200, 0), (x - 1, y - 9, 2, 8))
    # Эффект свечения
    pygame.draw.circle(surface, (255, 255, 200, 100), (x, y - 5), 3)

def draw_shield(surface, x, y):
    # Анимированный щит
    radius = 20 + abs(pygame.time.get_ticks() % 10 - 5) / 2
    pygame.draw.circle(surface, BLUE, (x, y), int(radius), 2)
    pygame.draw.circle(surface, (100, 200, 255, 100), (x, y), int(radius) - 2, 1)

# --- КЛАССЫ ---
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.shield_timer = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 20:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 20:
            self.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.y > 20:
            self.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 20:
            self.y += PLAYER_SPEED

    def draw(self):
        draw_player(screen, self.x, self.y)
        if self.shield_timer > 0:
            draw_shield(screen, self.x, self.y)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y -= BULLET_SPEED

    def draw(self):
        draw_bullet(screen, self.x, self.y)

class Enemy:
    def __init__(self):
        self.x = random.randint(20, WIDTH - 20)
        self.y = -20

    def update(self):
        self.y += ENEMY_SPEED

    def draw(self):
        draw_enemy(screen, self.x, self.y)

class Asteroid:
    def __init__(self):
        self.x = random.randint(20, WIDTH - 20)
        self.y = -20

    def update(self):
        self.y += ASTEROID_SPEED

    def draw(self):
        draw_asteroid(screen, self.x, self.y)

# --- УЛУЧШЕННОЕ МЕНЮ ---
def draw_menu(selected_option):
    screen.fill(BLACK)
    
    # Звездный фон
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(120, 225)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
    
    # Заголовок с эффектом свечения
    title = big_font.render("PIXEL SPACE SHOOTER", True, CYAN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4 - 50))
    
    # Подзаголовок
    subtitle = font.render("Борись!", True, YELLOW)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 4 + 20))

    # Опции меню
    options = ["Играть", "Руководство", "Выход"]
    for i, option in enumerate(options):
        color = WHITE if i != selected_option else GREEN
        text = medium_font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 50))
        
        # Индикатор выбора
        if i == selected_option:
            pygame.draw.polygon(screen, GREEN, [
                (WIDTH // 2 - text.get_width() // 2 - 20, HEIGHT // 2 + i * 50 + text.get_height() // 2),
                (WIDTH // 2 - text.get_width() // 2 - 10, HEIGHT // 2 + i * 50 + text.get_height() // 2 - 5),
                (WIDTH // 2 - text.get_width() // 2 - 10, HEIGHT // 2 + i * 50 + text.get_height() // 2 + 5)
            ])
            pygame.draw.polygon(screen, GREEN, [
                (WIDTH // 2 + text.get_width() // 2 + 20, HEIGHT // 2 + i * 50 + text.get_height() // 2),
                (WIDTH // 2 + text.get_width() // 2 + 10, HEIGHT // 2 + i * 50 + text.get_height() // 2 - 5),
                (WIDTH // 2 + text.get_width() // 2 + 10, HEIGHT // 2 + i * 50 + text.get_height() // 2 + 5)
            ])
    
    # Отрисовка регулятора громкости
    vol_text = font.render(f"Громкость: {int(MUSIC_VOLUME * 100)}%", True, YELLOW)
    screen.blit(vol_text, (WIDTH // 2 - vol_text.get_width() // 2, HEIGHT // 2 + 180))
    
    # Подсказки управления
    controls = font.render("Используйте left right для изменения громкости, up down для выбора, ENTER для подтверждения", True, (150, 150, 150))
    screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

# --- РУКОВОДСТВО ---
def draw_manual():
    screen.fill(BLACK)
    
    # Звездный фон
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(120, 225)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
    
    title = medium_font.render("РУКОВОДСТВО ПО ИГРЕ", True, CYAN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    
    instructions = [
        "УПРАВЛЕНИЕ:",
        "left right up down - Движение корабля",
        "ПРОБЕЛ - Стрельба",
        "S - Активировать щит (перезарядка)",
        "ESC - Выйти в меню",
        "",
        "ЦЕЛЬ ИГРЫ:",
        "Уничтожайте вражеские корабли и астероиды",
        "Набирайте как можно больше очков",
        "Избегайте столкновений с врагами",
        "",
        "СИСТЕМА ОЧКОВ:",
        "Вражеский корабль: 10 очков",
        "Астероид: 5 очков",
        "",
        "ЩИТ:",
        "Защищает от всех повреждений",
        "Имеет ограниченную продолжительность",
        "Перезаряжается после использования"
    ]
    
    for i, line in enumerate(instructions):
        color = YELLOW if ":" in line else WHITE
        text = font.render(line, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100 + i * 30))
    
    back_text = medium_font.render("Нажмите ESC для возврата в меню", True, GREEN)
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 50))
    
    pygame.display.flip()

# --- ИГРОВОЙ ЦИКЛ ---
def game_loop():
    global MUSIC_VOLUME

    player = Player()
    bullets = []
    enemies = []
    asteroids = []
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x, player.y - 10))
                if event.key == pygame.K_s and player.shield_timer <= 0:
                    player.shield_timer = SHIELD_DURATION
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- ОБНОВЛЕНИЕ ---
        player.move(keys)
        for b in bullets:
            b.update()
        for e in enemies:
            e.update()
        for a in asteroids:
            a.update()

        bullets = [b for b in bullets if b.y > -10]
        enemies = [e for e in enemies if e.y < HEIGHT + 20]
        asteroids = [a for a in asteroids if a.y < HEIGHT + 20]

        # Спавн врагов и астероидов
        if random.random() < 0.03:
            enemies.append(Enemy())
        if random.random() < 0.02:
            asteroids.append(Asteroid())

        # Проверка столкновений
        for e in enemies[:]:
            for b in bullets[:]:
                if abs(e.x - b.x) < 15 and abs(e.y - b.y) < 15:
                    enemies.remove(e)
                    bullets.remove(b)
                    score += 10
                    break

        for a in asteroids[:]:
            for b in bullets[:]:
                if abs(a.x - b.x) < 15 and abs(a.y - b.y) < 15:
                    asteroids.remove(a)
                    bullets.remove(b)
                    score += 5
                    break

        # Столкновение с игроком
        if player.shield_timer <= 0:
            for e in enemies:
                if abs(e.x - player.x) < 20 and abs(e.y - player.y) < 20:
                    running = False
            for a in asteroids:
                if abs(a.x - player.x) < 20 and abs(a.y - player.y) < 20:
                    running = False

        # --- ОТРИСОВКА ---
        screen.fill(BLACK)
        
        # Звездный фон
        for _ in range(30):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 2)
            brightness = random.randint(100, 200)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
        
        # Отрисовка игровых объектов
        for a in asteroids:
            a.draw()
        for e in enemies:
            e.draw()
        for b in bullets:
            b.draw()
        player.draw()

        # Улучшенный интерфейс
        score_text = medium_font.render(f"Очки: {score}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        
        # Индикатор щита
        if player.shield_timer > 0:
            shield_text = font.render(f"Щит: {player.shield_timer // FPS + 1}с", True, BLUE)
            screen.blit(shield_text, (10, 50))
        else:
            shield_text = font.render("Щит: готов", True, GREEN)
            screen.blit(shield_text, (10, 50))
        
        # Подсказки управления
        controls_text = font.render("Управление: left right up down двигаться, ПРОБЕЛ стрелять, S щит, ESC меню", True, (150, 150, 150))
        screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT - 30))

        # уменьшение таймера щита
        if player.shield_timer > 0:
            player.shield_timer -= 1

        pygame.display.flip()

    return score

# --- ГЛАВНОЕ МЕНЮ ---
def main_menu():
    global MUSIC_VOLUME
    selected_option = 0
    in_manual = False
    
    while True:
        if in_manual:
            draw_manual()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    in_manual = False
        else:
            draw_menu(selected_option)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            score = game_loop()
                            print("Ваш счёт:", score)
                        elif selected_option == 1:
                            in_manual = True
                        elif selected_option == 2:
                            pygame.quit()
                            sys.exit()
                    elif event.key == pygame.K_LEFT:
                        MUSIC_VOLUME = max(0.0, MUSIC_VOLUME - 0.1)
                        pygame.mixer.music.set_volume(MUSIC_VOLUME)
                    elif event.key == pygame.K_RIGHT:
                        MUSIC_VOLUME = min(1.0, MUSIC_VOLUME + 0.1)
                        pygame.mixer.music.set_volume(MUSIC_VOLUME)

# --- ЗАПУСК ---
if __name__ == "__main__":
    main_menu()