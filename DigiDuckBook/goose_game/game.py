import random
import os
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame  # подключение библиотеки
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT  # константы кнопок
# G:\go_it\training\GitHub\repositories\DigiDuckBook\DigiDuckBook\goose_game\image


def main_game() -> None:

    pygame.init()  # инициация библиотеки

    FPS = pygame.time.Clock()  # класс Clock для скорости отображения окна

    HEIGHT = 800  # высота и ширина поля игры
    WIDTH = 1200

    FONT = pygame.font.SysFont("Verdana", 20)

    COLOR_WHITE = (255, 255, 255)  # цвет игрока в ргб формате const
    COLOR_BLACK = (0, 0, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_GREEN = (0, 255, 0)

    main_display = pygame.display.set_mode((WIDTH, HEIGHT))  # обьявление дисплея

    bg = pygame.transform.scale(
        pygame.image.load("DigiDuckBook\\goose_game\\image\\background.png"), (WIDTH, HEIGHT)
    )
    bg_X1 = 0
    bg_X2 = bg.get_width()
    bg_move = 3

    IMAGES_PATH = "DigiDuckBook\\goose_game\\image\\Goose"  # папка с картинками анимации # TODO обережно зі шляхами
    PLAYER_IMAGES = os.listdir(IMAGES_PATH)

    player_size = (20, 20)  # обьявление модели игрока 20на20 п.
    player = pygame.image.load("DigiDuckBook\\goose_game\\image\\player.png").convert_alpha()  # =pygame.Surface(player_size)  #модель игрока
    # player.fill(COLOR_BLACK) #цвет игрока
    player_rect = player.get_rect().move(150, (HEIGHT - player_size[0]) / 2)  # обьявление координат player (х,y)
    # player_speed = [1, 1] #координаты игрока
    player_move_down = [0, 4]
    player_move_right = [4, 0]
    player_move_up = [0, -4]
    player_move_left = [-4, 0]


    def create_enemy():  # цикл врагов
        enemy_size = (30, 30)
        enemy = pygame.Surface(enemy_size)  # модель врага
        # enemy.fill(COLOR_BLUE)
        enemy = pygame.image.load("DigiDuckBook\\goose_game\\image\\enemy.png").convert_alpha()
        enemy_rect = pygame.Rect(
            WIDTH, random.randint(100, HEIGHT - 100), *enemy_size
        )  # спавн
        enemy_move = [random.randint(-8, -4), 0]  # тражктория
        return [enemy, enemy_rect, enemy_move]  # возвращаем enemy[0] enemy[1] enemy[2]


    def create_bonus():
        bonus_size = (40, 40)
        bonus = pygame.Surface(bonus_size)
        # bonus.fill(COLOR_GREEN)
        bonus = pygame.image.load("DigiDuckBook\\goose_game\\image\\bonus.png").convert_alpha()
        bonus_rect = pygame.Rect(random.randint(200, WIDTH - 200), 0, *bonus_size)
        bonus_move = [0, random.randint(3, 8)]
        return [bonus, bonus_rect, bonus_move]


    CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_ENEMY, 1500)
    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 2000)
    CHANG_IMAGE = pygame.USEREVENT + 3
    pygame.time.set_timer(CHANG_IMAGE, 200)


    bonuses = []
    enemies = []

    score = 0

    image_index = 0

    playing = True  # переменная работы окна


    # TODO in func розбити всередені на логичні функції іх викликати у нашій функції
    # и так шоб ничого не зламалося)
    def pop_enemy(l_enemies):
        for l_enemy in l_enemies:  # функция удаления врагов за экраном
            if l_enemy[1].left < 0:
                l_enemies.pop(l_enemies.index(l_enemy))
        return l_enemies


    def pop_bonuses(l_bonuses):
        for l_bonus in l_bonuses:
            if l_bonus[1].bottom > HEIGHT:
                l_bonuses.pop(l_bonuses.index(l_bonus))
        return l_bonuses


    def bonus_move(l_bonuses):
        for l_bonus in l_bonuses:
            l_bonus[1] = l_bonus[1].move(
                l_bonus[2]
            )  # enemy_rect = enemy_rect.move(enemy_move)но через return функции
        return l_bonuses


    # def bottom_down(bottom):
    #     if keys[K_DOWN] and player_rect.bottom < HEIGHT:  # keys[K_DOWN]возвращает тру/фолс
    #         player_rect = player_rect.move(player_move_down)
    #     return player_rect


    while playing:  # цикл окна
        FPS.tick(120)

        for event in pygame.event.get():  # цикл event button exit???
            if event.type == QUIT:
                playing = False  # типа break если нажали віход
            if event.type == CREATE_ENEMY:  # заполнение списка
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == (CHANG_IMAGE):
                player = pygame.image.load(
                    os.path.join(IMAGES_PATH, PLAYER_IMAGES[image_index])
                )
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0
        # main_display.fill(COLOR_BLACK)  # закрашивание поле окна после движения моделей(игрока)

        bg_X1 -= bg_move
        bg_X2 -= bg_move

        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()

        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()

        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))

        keys = pygame.key.get_pressed()  # возвращает список тру/фолс??

        # bottom_down(keys[K_DOWN])

        if keys[K_DOWN] and player_rect.bottom < HEIGHT:  # keys[K_DOWN]возвращает тру/фолс
            player_rect = player_rect.move(player_move_down)

        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)

        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)

        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])

            if player_rect.colliderect(enemy[1]):
                playing = False

        bonus_move(bonuses)
        for bonus in bonuses:
            main_display.blit(bonus[0], bonus[1])

        # for bonus in bonuses:
        #     bonus[1] = bonus[1].move(bonus[2])  # enemy_rect = enemy_rect.move(enemy_move)но через return функции
        #     main_display.blit(bonus[0], bonus[1])

        for bonus in bonuses:
            if player_rect.colliderect(bonus[1]):
                score += 1
                bonuses.pop(bonuses.index(bonus))

        main_display.blit(
            FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20)
        )  # вывод score на єкран
        main_display.blit(
            player, player_rect
        )  # размещение player в окне метод blit (x,y) или переменная

        # main_display.blit(enemy,enemy_rect)
        # player_rect = player_rect.move(player_speed) #итерация координат move=+[1,1]???

        pygame.display.flip()  # постоянное обновление окна

        pop_enemy(enemies)
        pop_bonuses(bonuses)


if __name__ == "__main__":
    pass