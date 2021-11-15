import pygame
import sys
from random import *

############################################################
# 기본 초기화 (반드시 해야하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 950  # 가로크기
screen_height = 440  # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height))  # (()) 2개씩 필요, 튜플 형식으로 저장하는 것임

# 화면 타이틀 설정
pygame.display.set_caption("학점게임")

music = pygame.mixer.music.load('HB-S.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

score = 0
A_crush = 0
start_ticks = pygame.time.get_ticks()

# FPS
clock = pygame.time.Clock()
############################################################
# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

#배경화면
background = pygame.image.load("SB1.png")

#캐릭터 정보
character = pygame.image.load("standing.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) / 2 - 250
character_y_pos = screen_height - character_height - 37

char_to_x = 0
char_to_y = 0
char_speed = 1

A = pygame.image.load("A+.png")
A_size = A.get_rect().size
A_width = A_size[0]
A_height = A_size[1]
A_x_pos = screen_width - 50
A_y_pos = randint(0, screen_height - A_height)

font = pygame.font.SysFont('comicsans', 30, True)
running = True  # 게임이 진행중인가?
while running:

    dt = clock.tick(30)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가 / 대문자로 QUIT
            running = False  # 게임이 진행중이 아님

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                char_to_y -= char_speed
            elif event.key == pygame.K_UP:
                char_to_y += char_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                char_to_y = 0


    # 3. 게임 캐릭터 위치 정의
    character_x_pos += char_to_x * dt

    if character_x_pos < 0:
        character_x_pos = 0

    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
        A_y_pos += 0.2 * dt

    if A_y_pos > screen_height:
        A_x_pos = randint(0, screen_width - A_width)
        A_y_pos = 0


    # 4. 충돌 처리
    char_rect = character.get_rect()
    char_rect.left = character_x_pos
    char_rect.top = character_y_pos

    A_rect = A.get_rect()
    A_rect.left = A_x_pos
    A_rect.top = A_y_pos

    if char_rect.colliderect(A_rect):
        A_crush += 1

    # 5. 화면에 그리기
    score = elapsed_time + A_crush * 3
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(A, (A_x_pos, A_y_pos))
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.update()

pygame.quit()