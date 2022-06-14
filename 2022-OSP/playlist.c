#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#pragma warning(disable : 4996)

typedef char* element;

typedef struct DListNode {
	struct DListNode* llink;
	struct DListNode* rlink;
	element data;
}DListNode;

DListNode* current; // 현재 위치(현재 play되는 곡)

void init(DListNode* head) {
	head->rlink = head;
	head->llink = head;
}

void dinsert(DListNode* prev, element data) {
	DListNode* new_node = (DListNode*)malloc(sizeof(DListNode));
	new_node->data = (char*)malloc(sizeof(char) * (strlen(data) + 1));
	strcpy(new_node->data, data);

	new_node->rlink = prev->rlink;
	new_node->llink = prev;

	prev->rlink->llink = new_node;
	prev->rlink = new_node;
}

void ddelete(DListNode* head, DListNode* removed) {
	if (removed == head) return;
	else {
		removed->llink->rlink = removed->rlink;
		removed->rlink->llink = removed->llink;
		if (removed == current) current = current->rlink;
		free(removed);
	}
}

void free_node(DListNode* head) {
	DListNode* p = head->rlink, * next;
	while (p != head) {
		next = p->rlink;
		free(p);
		p = next;
	}
}

void search(DListNode* head, element data) {
	DListNode* p = head->rlink;
	for (; p != head; p = p->rlink) {
		if (strcmp(p->data, data) == 0) {
			p->rlink->llink = p->llink;
			p->llink->rlink = p->rlink;
			ddelete(head, p);
			printf("%s를 성공적으로 플레이어에서 삭제\n", data);
			return;
		}
	}
	printf("%s 탐색 실패\n\n", data);
}
void print_dlist(DListNode* head) {
	DListNode* p = head->rlink; // 첫번째 노드의 주소 대입
	for (; p != head; p = p->rlink) {
		if (p == current)
			printf("<-| %s |-> ", p->data);
		else
			printf("<-| %s |-> ", p->data);
	}
	printf("\n\n");
}


int main() {
	char ch= '0'; // command < > q
	char title[100];

	char song1[] = "DM";
	char song2[] = "GLASSY";
	char song3[] = "Villain";

	DListNode* head = (DListNode*)malloc(sizeof(DListNode)); // 헤드 노드
	init(head);
	printf("playlist\n");
	printf("---- %s ---- is playing\n" ,song3);
	dinsert(head, song1);
	dinsert(head, song2);
	dinsert(head, song3);

	current = head->rlink; // 현재 play되는 곡 - current 포인터는 첫번째 데이터를 담은 노드
	print_dlist(head);

	while(ch != 'q') {
		printf("\n명령어를 입력하시오( <, >, a, d, q) : ");
		ch = getchar();

		switch (ch) {
		case 'a':
			getchar();
			printf("새로 추가할 곡명 : ");
			gets(title);
			dinsert(head, title);
			break;
		case 'd':
			getchar();
			printf("삭제하고 싶은 곡명 : ");
			gets(title);
			search(head, title);
			break;
		case '<': // 이전 곡으로 이동
			current = current->llink; // left link로 이동
			if (current == head) // 헤드 노드인 경우 예외처리 -> 헤드의 왼쪽
				current = head->llink;
			getchar();
			break;
		case '>': // 다음 곡으로 이동
			current = current->rlink; // right link로 이동
			if (current == head) // 헤드 노드인 경우 예외처리 -> 헤드의 오른쪽
				current = head->rlink;
			getchar();
			break;
		}
		printf("\n---- %s ---- is playing\n", current->data);
		print_dlist(head);
		//getchar(); // 줄바꿈 문자 제거
	}
	printf("Ending Playlist\n");
	printf("Good bye\n");

	free(head);
	return 0;
}

