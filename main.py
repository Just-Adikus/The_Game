import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра с квадратом")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Игровые переменные
player_size = 50
player_x = width // 2
player_y = height - player_size - 10
player_speed = 10
falling_objects = []
falling_speed = 5
score = 0

# Шрифт
font = pygame.font.SysFont(None, 30)


# Функция для отображения текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Функция для отображения экрана "GAME OVER"
def game_over_screen():
    draw_text("GAME OVER", font, RED, screen, width // 2 - 100, height // 3)
    draw_text(f"Ваши очки: {score}", font, BLACK, screen, width // 2 - 80, height // 2)

    # Кнопки
    restart_button = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 50)
    quit_button = pygame.Rect(width // 2 - 100, height // 2 + 120, 200, 50)

    pygame.draw.rect(screen, GREEN, restart_button)
    pygame.draw.rect(screen, GREEN, quit_button)

    draw_text("Начать заново", font, BLACK, screen, width // 2 - 75, height // 2 + 60)
    draw_text("Выход", font, BLACK, screen, width // 2 - 25, height // 2 + 130)

    pygame.display.flip()

    # Ожидание кликов на кнопки
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_x, mouse_y):
                    return True  # Перезапустить игру
                if quit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    quit()


# Основной игровой цикл
def game_loop():
    global player_x, player_y, falling_objects, score
    player_x = width // 2
    player_y = height - player_size - 10
    falling_objects = []
    score = 0

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        # Проверка на события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += player_speed

        # Падение объектов
        if random.randint(1, 20) == 1:
            falling_objects.append([random.randint(0, width - 20), -20])

        for obj in falling_objects[:]:
            obj[1] += falling_speed
            if obj[1] > height:
                falling_objects.remove(obj)
                score += 1

        # Проверка на столкновение
        for obj in falling_objects:
            if (player_x < obj[0] < player_x + player_size or player_x < obj[0] + 20 < player_x + player_size) and \
                    (player_y < obj[1] < player_y + player_size or player_y < obj[1] + 20 < player_y + player_size):
                running = False  # Столкновение с объектом

        # Отображение игрока и объектов
        pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size))
        for obj in falling_objects:
            pygame.draw.rect(screen, RED, (obj[0], obj[1], 20, 20))

        # Отображение счета
        draw_text(f"Очки: {score}", font, BLACK, screen, 10, 10)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)

        if not running:
            if game_over_screen():
                game_loop()  # Перезапустить игру
            else:
                running = False  # Закрыть игру


# Запуск игры
game_loop()
pygame.quit()
