
# heavily based and inspired by ClearCode Channel videos on youtube - https://youtu.be/oOqdHBkA4rc

import random
import pygame
from pygame.locals import *
import sys

###


class Block(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, x_pos, y_pos) -> None:
        super().__init__()
        #self.image = pygame.image.load(path).convert()
        self.image = surface
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    speed: int
    movement: int

    def __init__(self, x_pos, y_pos, speed) -> None:
        ps = pygame.Surface(((10, 140)))
        ps.set_colorkey((0, 0, 0))
        pygame.draw.rect(ps, line_color, (0, 0, 10, 140))
        super().__init__(ps, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_contrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_contrain()


class Ball(Block):
    def __init__(self, x_pos, y_pos, speed_x, speed_y, paddles) -> None:
        ps = pygame.Surface((30, 30)).convert()
        ps.set_colorkey((0, 0, 0))
        pygame.draw.ellipse(ps, line_color, (0, 0, 30, 30))
        super().__init__(ps, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            collision_paddle = pygame.sprite.spritecollide(
                self, self.paddles, False)[0].rect

            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1

            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width * 0.5, screen_height * 0.5)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = game_font.render(
            str(countdown_number), True, font_color)
        time_counter_rect = time_counter.get_rect(
            center=(screen_width * 0.5, screen_height * 0.5 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)


class Opponent(Block):
    def __init__(self, x_pos, y_pos, speed) -> None:
        ps = pygame.Surface((10, 140))
        ps.set_colorkey((0, 0, 0))
        pygame.draw.rect(ps, line_color, (0, 0, 10, 140))
        super().__init__(ps, x_pos, y_pos)
        self.speed = speed

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height


class GameManager:
    player_score: int
    opponent_score: int
    ball_group: pygame.sprite.GroupSingle
    paddle_group: pygame.sprite.Group

    def __init__(self, ball_group, paddle_group) -> None:
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = game_font.render(
            str(self.player_score), True, font_color)
        opponent_score = game_font.render(
            str(self.opponent_score), True, font_color)

        player_score_rect = player_score.get_rect(
            midleft=(screen_width * 0.5 + 30, screen_height * 0.5))
        opponent_score_rect = opponent_score.get_rect(
            midleft=(screen_width * 0.5 - 40, screen_height * 0.5))

        screen.blits([
            (player_score, player_score_rect),
            (opponent_score, opponent_score_rect)
        ])

###


pygame.init()

clock = pygame.time.Clock()

screen_width = 1280
screen_height = 960
flags = DOUBLEBUF
screen = pygame.display.set_mode(
    (screen_width, screen_height), flags, 16, vsync=0)
pygame.display.set_caption('Pong')

middle_strip = pygame.Rect(screen_width * 0.5 - 2, 0, 4, screen_height)

bg_color = pygame.Color('grey12')
line_color = pygame.Color(240, 240, 240)

game_font = pygame.font.Font(None, 32)
font_color = pygame.Color(128, 128, 128)

player = Player(screen_width - 20, screen_height * 0.5, 5)
opponent = Opponent(20, screen_width * 0.5, 5)
paddle_group = pygame.sprite.Group([player, opponent])
ball = Ball(screen_width * 0.5, screen_height * 0.5, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle(ball)
game_manager = GameManager(ball_sprite, paddle_group)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.movement += player.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.movement += player.speed
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.movement -= player.speed

            if event.key == pygame.K_9:
                player.speed -= 1
            if event.key == pygame.K_0:
                player.speed += 1

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill(bg_color)
    pygame.draw.rect(screen, line_color, middle_strip)

    game_manager.run_game()

    pygame.display.flip()
    clock.tick(60)
