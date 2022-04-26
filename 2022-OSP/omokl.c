#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <mmsystem.h>
#pragma comment(lib, "winmm.lib")

#define Third_Run "Starbridge.wav"
#define LEFT 75
#define RIGHT 77
#define UP 72
#define DOWN 80
#define SPACE 32
#define ESC 27
#define U1 1
#define U2 2

int MAP_X, MAP_Y;
int** GMap;

typedef struct XY {
	int x;
	int y;
}xy;

gotoxy(int x, int y)
{
	COORD pos = { x, y };
	SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), pos);
}

void initGame()
{
	int i = 0, k = 0;
	for (i = 0; i < MAP_Y; i++)
	{
		for (k = 0; k < MAP_X; k++)
		{
			if (i == 0)
			{
				if (k == 0)
					printf("┌");
				else if (k + 1 == MAP_X)
					printf("┐");
				else
					printf("┬");
			}
			else if (i + 1 < MAP_Y)
			{
				if (k == 0)
					printf("├");
				else if (k + 1 == MAP_X)
					printf("┤");
				else
					printf("┼");
			}
			else
			{
				if (k == 0)
					printf("└");
				else if (k + 1 == MAP_X)
					printf("┘");
				else
					printf("┴");
			}
		}
		printf("\n");
	}
}

int searchStone(xy hd, int **GMap, int flag, int p, int sw)
{
	if (GMap[hd.y][hd.x] != flag) return 0;
	if (p == 0)
	{
		hd.y += sw;
	}

	else if (p == 1)
	{
		hd.x += sw;
	}

	else if (p == 2)
	{
		hd.x += sw;
		hd.y += sw;
	}

	else
	{
		hd.x += sw;
		hd.y -= sw;
	}
	return 1 + searchStone(hd, GMap, flag, p, sw);
}

void checkStone(xy hd, int **GMap, int turn)
{
	int i = 0, countStone = 0;
	for (i = 0; i < 4; i++)
	{
		countStone = 0;
		countStone += searchStone(hd, GMap, turn, i, 1);
		countStone += searchStone(hd, GMap, turn, i, -1);
		if (countStone == 6)
		{
			gotoxy(0, MAP_Y);
			if (turn == U1)
				printf("사용자 1");
			else
				printf("사용자 2");
			printf("님이 승리하셨습니다.!");
			getch();
			exit(1);
		}
	}
}

void startGame(int **GMap)
{
	char ip = '\0';
	int turn = U1;
	xy hd = { MAP_X / 2, MAP_Y / 2 };

	while (1)
	{
		if (kbhit()){
			ip = getch();
			switch (ip)
			{

			case LEFT:
				if (hd.x > 0)
					hd.x -= 1;
				break;

			case RIGHT:
				if (hd.x < MAP_X - 1)
					hd.x += 1;
				break;

			case UP:
				if (hd.y > 0)
					hd.y -= 1;
				break;

			case DOWN:
				if (hd.y < MAP_Y - 1)
					hd.y += 1;
				break;

			case SPACE:
				if (GMap[hd.y][hd.x] == 0)
				{
					gotoxy(hd.x * 2, hd.y);
					if (turn == U1)
					{
						GMap[hd.y][hd.x] = U1;
						printf("●");
						checkStone(hd, GMap, turn);
						turn = U2;
					}
					else

					{
						GMap[hd.y][hd.x] = U2;
						printf("○");
						checkStone(hd, GMap, turn);
						turn = U1;
					}
				}
				break;

			case ESC:
				exit(1);
				break;
			}

			gotoxy(hd.x * 2, hd.y);
		}
	}
}

int main() {
	PlaySound(TEXT(Third_Run), NULL, SND_FILENAME | SND_ASYNC | SND_LOOP);
	system("mode con cols=222 lines=70");
	printf("> KEY - Arrow keys, Spaces bar\n");
	printf("> Enter the height\n");
	scanf_s("%d", &MAP_Y);
	printf("> Enter the width\n");
	scanf_s("%d", &MAP_X);
		
	GMap = (int**)malloc(sizeof(int*) * MAP_Y);
	GMap[0] = (int*)malloc(sizeof(int) * MAP_Y, MAP_X);
	for (int i = 1; i < MAP_Y; i++) {
		GMap[i] = GMap[i - 1] + MAP_X;
	}

	printf("\nheight: %d, width: %d", MAP_Y, MAP_X);
	printf("\nEnd key(ESC)\n\n");
	printf("press to start");
	getch();
	system("cls");
	initGame();
	startGame(GMap);
	free(GMap[0]);
	free(GMap);
}
