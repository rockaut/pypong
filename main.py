import random
import pygame
from pygame.locals import *
import sys

pygame.init()

clock = pygame.time.Clock()

screen_width = 1280
screen_height = 960
flags = DOUBLEBUF
screen = pygame.display.set_mode((screen_width, screen_height), flags, 16, vsync=1)
pygame.display.set_caption('Pong')

ball = pygame.Rect(screen_width/2-15, screen_height/2-15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2-70, 10, 140)

bg_color = pygame.Color('grey12')
line_color = pygame.Color(240, 240, 240)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7


player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None, 32)
font_color = pygame.Color(128, 128, 128)
font_color.a = 128

current_time: int = 0
last_frametime: int = 0
score_time: int = 1
show_frames: bool = False


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()
    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 10:
            ball_speed_y *= -1


def ball_start():
    global ball_speed_x, ball_speed_y, score_time, current_time

    ball.center = (screen_width * 0.5, screen_height * 0.5)

    if current_time - score_time < 700:
        number_three = game_font.render("3", True, font_color)
        screen.blit(number_three, (screen_width * 0.5 - 10, screen_height * 0.5 + 20))
    if current_time - score_time < 1400:
        number_two = game_font.render("2", True, font_color)
        screen.blit(number_two, (screen_width * 0.5 - 10, screen_height * 0.5 + 20))
    if current_time - score_time < 2100:
        number_one = game_font.render("1", True, font_color)
        screen.blit(number_one, (screen_width * 0.5 - 10, screen_height * 0.5 + 20))

    if current_time - score_time < 2100:
        ball_speed_x = 0
        ball_speed_y = 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

while True:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_speed += 7
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_speed -= 7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_speed -= 7
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_speed += 7
            
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_F1:
                show_frames = not show_frames

    screen.fill(bg_color)
    pygame.draw.rect(screen, line_color, player)
    pygame.draw.rect(screen, line_color, opponent)
    pygame.draw.ellipse(screen, line_color, ball)
    pygame.draw.aaline(screen, line_color, (screen_width/2,
                       0), (screen_width/2, screen_height))

    if score_time:
        ball_start()

    player_text = game_font.render(f"{player_score}", True, font_color)
    screen.blit(player_text, (660, 50))

    opponent_text = game_font.render(f"{opponent_score}", True, font_color)
    screen.blit(opponent_text, (610, 50))

    a = current_time - last_frametime
    last_frametime = current_time
    if show_frames:
        frame_text = game_font.render(str(a), True, font_color)
        screen.blit(frame_text, (10, 10))

    ball_animation()
    opponent_animation()
    player_animation()

    pygame.display.flip()
    clock.tick(60)
