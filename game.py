import random
import pygame
import sys
from random import *

# 기본 초기화
pygame.init()

# 화면 크기 설정
screen_width = 950  # 가로크기
screen_height = 440  # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("학점게임")

music = pygame.mixer.music.load('TN.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

score = 0
A_crush = 0
B_crush = 0
C_crush = 0
F_crush = 0
start_ticks = pygame.time.get_ticks()

# FPS
clock = pygame.time.Clock()
############################################################
# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

#배경화면
background = pygame.image.load("SB1.png")
background2 = pygame.image.load("AF.jpg")
background3 = pygame.image.load("AR.jpg")
background4 = pygame.image.load("BM.png")
background5 = pygame.image.load("congrat.jpg")

#캐릭터 정보
character = pygame.image.load("maple_leaf.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) / 2 - 250
character_y_pos = screen_height - character_height - 37

char_to_x = 0
char_to_y = 0
char_speed = 15

A = pygame.image.load("A+.png")
A_size = A.get_rect().size
A_width = A_size[0]
A_height = A_size[1]
A_x_pos = screen_width - A_width
A_y_pos = randint(0, screen_height - A_height)
A_speed = 3

B = pygame.image.load("B.png")
B_size = B.get_rect().size
B_width = B_size[0]
B_height = B_size[1]
B_x_pos = screen_width - B_width
B_y_pos = randint(0, screen_height - B_height)
B_speed = 5

C = pygame.image.load("C.png")
C_size = A.get_rect().size
C_width = C_size[0]
C_height = C_size[1]
C_x_pos = randint(0, screen_width - C_width)
C_y_pos = 0
C_speed = 7

F = pygame.image.load("F.png")
F_size = F.get_rect().size
F_width = F_size[0]
F_height = F_size[1]
F_x_pos = randint(0, screen_width - F_width)
F_y_pos = screen_height
F_speed = 10

font = pygame.font.SysFont('comicsans', 30, True)
running = True  # 게임이 진행중인가?
while running:

    dt = clock.tick(30)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 게임이 진행중이 아님

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                char_to_x -= char_speed

            elif event.key == pygame.K_RIGHT:
                char_to_x += char_speed

            elif event.key == pygame.K_UP:
                char_to_y -= char_speed

            elif event.key == pygame.K_DOWN:
                char_to_y += char_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                char_to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                char_to_y = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += char_to_x
    character_y_pos += char_to_y

    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height
        A_x_pos += 0.2 * dt

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        A_x_pos += 0.2 * dt

    A_x_pos -= A_speed
    B_x_pos += B_speed
    C_y_pos += C_speed
    F_y_pos -= F_speed

    if A_x_pos < 0:
        A_x_pos = screen_width - A_width
        A_y_pos = randint(0, screen_height - A_height)

    if B_x_pos > screen_width - B_width:
        B_x_pos = 0
        B_y_pos = randint(0, screen_height - B_height)

    if C_y_pos > screen_height:
        C_x_pos = randint(0, screen_width - C_width)
        C_y_pos = 0

    if F_y_pos < 0:
        F_x_pos = randint(0, screen_width)
        F_y_pos = screen_height - F_height

    # 4. 충돌 처리
    char_rect = character.get_rect()
    char_rect.left = character_x_pos
    char_rect.top = character_y_pos

    A_rect = A.get_rect()
    A_rect.left = A_x_pos
    A_rect.top = A_y_pos

    B_rect = B.get_rect()
    B_rect.left = B_x_pos
    B_rect.top = B_y_pos

    C_rect = C.get_rect()
    C_rect.left = C_x_pos
    C_rect.top = C_y_pos

    F_rect = F.get_rect()
    F_rect.left = F_x_pos
    F_rect.top = F_y_pos

    score = int(elapsed_time) + A_crush * 10 + B_crush * 4 + C_crush * 2 - F_crush * 30

    if char_rect.colliderect(A_rect):
        A_crush += 1
        A_x_pos = screen_width - A_width
        A_y_pos = randint(0, screen_height - A_height)

    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(A, (A_x_pos, A_y_pos))
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render('time: ' + str(int(elapsed_time)), 1, (255, 255, 255))
    screen.blit(text, (10, 40))
    text = font.render('A+:10p', 1, (255, 255, 255))
    screen.blit(text, (300, 10))
    text = font.render('1000p', 1, (255, 255, 255))
    screen.blit(text, (300, 40))

    if (score > 1000):
        if char_rect.colliderect(B_rect):
            B_crush += 1
            B_x_pos = screen_width - B_width
            B_y_pos = randint(0, screen_height - B_height)

        # A_y_pos = randint(0, -screen_height + A_height)
        screen.blit(background2, (0, 0))
        screen.blit(character, (character_x_pos, character_y_pos))
        screen.blit(A, (A_x_pos, A_y_pos))
        screen.blit(B, (B_x_pos, B_y_pos))
        text = font.render('Score: ' + str(score), 1, (255, 255, 255))
        screen.blit(text, (10, 10))
        text = font.render('time: ' + str(int(elapsed_time)), 1, (255, 255, 255))
        screen.blit(text, (10, 40))
        text = font.render('B:4p', 1, (255, 255, 255))
        screen.blit(text, (300, 10))
        text = font.render('1500p, 100s', 1, (255, 255, 255))
        screen.blit(text, (300, 40))
        if (elapsed_time > 100):
            running = False

    if (score > 1500):
        if char_rect.colliderect(C_rect):
            C_crush += 1
            C_x_pos = screen_width - C_width
            C_y_pos = randint(0, screen_height - C_height)
        screen.blit(background3, (0, 0))
        screen.blit(character, (character_x_pos, character_y_pos))
        screen.blit(A, (A_x_pos, A_y_pos))
        screen.blit(B, (B_x_pos, B_y_pos))
        screen.blit(C, (C_x_pos, C_y_pos))
        text = font.render('Score: ' + str(score), 1, (255, 255, 255))
        screen.blit(text, (10, 10))
        text = font.render('time: ' + str(int(elapsed_time)), 1, (255, 255, 255))
        screen.blit(text, (10, 40))
        text = font.render('C:2p', 1, (255, 255, 255))
        screen.blit(text, (300, 10))
        text = font.render('2000p, 120s', 1, (255, 255, 255))
        screen.blit(text, (300, 40))
        if (elapsed_time > 120):
            running = False

    if (score > 2000):
        if char_rect.colliderect(F_rect):
            F_crush += 1
            F_x_pos = screen_width - F_width
            F_y_pos = randint(0, screen_height - F_height)
        char_speed = 1
        screen.blit(background4, (0, 0))
        screen.blit(character, (character_x_pos, character_y_pos))
        screen.blit(A, (A_x_pos, A_y_pos))
        screen.blit(B, (B_x_pos, B_y_pos))
        screen.blit(C, (C_x_pos, C_y_pos))
        screen.blit(F, (F_x_pos, F_y_pos))
        text = font.render('Score: ' + str(score), 1, (255, 255, 255))
        screen.blit(text, (10, 10))
        text = font.render('time: ' + str(int(elapsed_time)), 1, (255, 255, 255))
        screen.blit(text, (10, 40))
        text = font.render('F:-30p, key change', 1, (255, 255, 255))
        screen.blit(text, (300, 10))
        text = font.render('5000p, 240s', 1, (255, 255, 255))
        screen.blit(text, (300, 40))
        if (elapsed_time > 240):
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                char_to_x += char_speed

            elif event.key == pygame.K_RIGHT:
                char_to_x -= char_speed

            elif event.key == pygame.K_UP:
                char_to_y += char_speed

            elif event.key == pygame.K_DOWN:
                char_to_y -= char_speed

    if score > 5000:
        screen.blit(background5, (0, 0))
        text = font.render('Good bye', 1, (255, 255, 255))
        screen.blit(text, (300, 40))
        if elapsed_time > 240:
            running = False

    pygame.display.update()

pygame.quit()