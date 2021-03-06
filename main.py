import pygame
from random import randint, choice
from Entities import Colors, Dimensions
import time
from PIL import Image


def game_loop():
    pygame.init()
    background = pygame.display.set_mode((Dimensions.WIDTH, Dimensions.HEIGHT))

    # a surface which represents one part of the snake
    tile = pygame.Surface((Dimensions.TILE_SIZE, Dimensions.TILE_SIZE))
    tile.fill(Colors.WHITE)

    enemy = pygame.image.load("./resources/circle5.png")

    im = Image.open("./resources/circle5.png")  # image to be displayed as the enemy
    image_width, image_height = im.size

    score = 0

    speed = 2  # initial player speed

    enemy_speed = 1

    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    # a piece to be eaten
    fruit = pygame.Surface((Dimensions.TILE_SIZE, Dimensions.TILE_SIZE))
    fruit.fill(Colors.GREEN)
    fruit_x = randint(Dimensions.TILE_SIZE, Dimensions.WIDTH - Dimensions.TILE_SIZE)
    fruit_y = randint(Dimensions.TILE_SIZE, Dimensions.HEIGHT - Dimensions.TILE_SIZE)

    x_change = 0
    y_change = 0

    # initial state of the snake
    xs = [Dimensions.WIDTH * 0.45]
    ys = [Dimensions.HEIGHT * 0.8]

    can_up = True
    can_down = True
    can_left = True
    can_right = True
    font = pygame.font.Font(None, 30)

    # scoreboard
    score_text = font.render('Score: ' + str(score), 2, Colors.YELLOW)
    box_width = score_text.get_rect()
    score_x = (Dimensions.WIDTH - box_width[2]) / 2
    background.blit(tile, (xs[0], ys[0]))
    background.blit(score_text, [score_x, 20])

    enemies = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and can_left:
                    x_change = -1 * speed
                    y_change = 0
                    can_left = False
                    can_right = False
                    can_up = True
                    can_down = True

                if event.key == pygame.K_RIGHT and can_right:
                    x_change = speed
                    y_change = 0
                    can_left = False
                    can_right = False
                    can_up = True
                    can_down = True

                if event.key == pygame.K_DOWN and can_down:
                    y_change = speed
                    x_change = 0
                    can_down = False
                    can_up = False
                    can_right = True
                    can_left = True

                if event.key == pygame.K_UP and can_up:
                    y_change = -1 * speed
                    x_change = 0
                    can_up = False
                    can_down = False
                    can_left = True
                    can_right = True

        xs[0] += x_change
        ys[0] += y_change

        # if player goes out of bounds he appears on the opposite end
        if xs[0] < 0:
            xs[0] = Dimensions.WIDTH
        if ys[0] < 0:
            ys[0] = Dimensions.HEIGHT
        if xs[0] > Dimensions.WIDTH:
            xs[0] = 0
        if ys[0] > Dimensions.HEIGHT:
            ys[0] = 0

        background.fill(Colors.BLACK)
        background.blit(score_text, [score_x, 20])
        if Dimensions.square_square_collision_detection(xs[0], ys[0], fruit_x, fruit_y):  # check if fruit was eaten
            score += 1
            fruit_x = randint(Dimensions.TILE_SIZE, Dimensions.WIDTH - Dimensions.TILE_SIZE)
            fruit_y = randint(Dimensions.TILE_SIZE, Dimensions.HEIGHT - Dimensions.TILE_SIZE)
            xs.append(700)
            ys.append(700)

            score_text = font.render('Score: ' + str(score), 2, Colors.YELLOW)
            if score // 5 > 0 and score % 5 == 0:
                speed = 1.2 * speed
                enemies.append([randint(Dimensions.TILE_SIZE, Dimensions.WIDTH - Dimensions.TILE_SIZE),
                                # appending a list which contains x, y, as well as k's which determine direction of moving
                                randint(Dimensions.TILE_SIZE, Dimensions.HEIGHT - Dimensions.TILE_SIZE),
                                choice([-1, 1]), choice([-1, 1])])
        i = len(xs) - 1
        while i >= 1:
            xs[i] = xs[i - 1]
            ys[i] = ys[i - 1]
            i -= 1
        for i in range(0, len(xs)):  # drawing player
            background.blit(tile, (xs[i], ys[i]))

        for i in range(len(enemies)):  # updating positions of enemies
            enemies[i][0] += enemies[i][2] * enemy_speed
            enemies[i][1] += enemies[i][3] * enemy_speed

            # check if enemy has reached an edge
            if enemies[i][1] < 0:
                enemies[i][3] = 1
            if enemies[i][0] < 0:
                enemies[i][2] = 1
            if enemies[i][1] + image_height > Dimensions.HEIGHT:
                enemies[i][3] = -1
            if enemies[i][0] + image_width > Dimensions.WIDTH:
                enemies[i][2] = -1

        for i in range(len(xs)):  # check if player and any of the enemies have collided
            for j in range(len(enemies)):
                if Dimensions.square_square_collision_detection(xs[i], ys[i], enemies[j][0], enemies[j][1],
                                                                Dimensions.TILE_SIZE, image_width):
                    message_display(background, "GAME OVER!", 2, True)

        if len(xs) > 43:  # check if player has collided with himself
            for k in range(len(xs) - 1, 42, -1):
                if Dimensions.square_square_collision_detection(xs[0], ys[0], xs[k], ys[k]):
                    message_display(background, "GAME OVER!", 2, True)

        for i in range(len(enemies)):  # drawing enemies
            background.blit(enemy, (enemies[i][0], enemies[i][1]))
        background.blit(fruit, (fruit_x, fruit_y))
        pygame.display.update()
        clock.tick(75)


def text_objects(text, font):
    text_surface = font.render(text, True, Colors.WHITE)
    return text_surface, text_surface.get_rect()


def message_display(game_display, text, sleep_time, game_over):
    large_text = pygame.font.Font("freesansbold.ttf", 70)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = (Dimensions.WIDTH / 2, Dimensions.HEIGHT / 2)
    game_display.blit(text_surf, text_rect)

    pygame.display.update()

    time.sleep(sleep_time)
    if game_over:
        game_loop()


if __name__ == '__main__':
    game_loop()
