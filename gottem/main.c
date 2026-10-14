#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_NOTES       10
#define TITLE_BUF_SIZE  64
#define MAX_TITLE_LEN   62
#define MAX_CONTENT_LEN 1022

typedef struct Note {
    int title_len;
    char title[TITLE_BUF_SIZE];
    int content_len;
    char *content;
} Note;

static Note notes[MAX_NOTES];
static Note *selected_note = NULL;

static Note *note_new(void)
{
    Note *note = NULL;

    for (int i = 0; i < MAX_NOTES; i++) {
        if (notes[i].content == NULL) {
            note = &notes[i];
            break;
        }
    }

    if (note == NULL) {
        puts("Max notes reached");
        return NULL;
    }

    printf("Enter title length: ");
    scanf("%d", &note->title_len);
    getchar();

    if (note->title_len < 1 || note->title_len > MAX_TITLE_LEN) {
        puts("Invalid title length");
        return NULL;
    }

    printf("Enter title: ");
    memset(note->title, 0, sizeof(note->title));
    read(STDIN_FILENO, note->title, note->title_len);

    printf("Enter content length: ");
    scanf("%d", &note->content_len);
    getchar();

    if (note->content_len < 1 || note->content_len > MAX_CONTENT_LEN) {
        puts("Invalid content length");
        return NULL;
    }

    note->content = malloc(note->content_len);

    printf("Enter content: ");
    read(STDIN_FILENO, note->content, note->content_len);

    return note;
}

static void note_list(void)
{
    for (int i = 0; i < MAX_NOTES; i++) {
        if (notes[i].content != NULL) {
            printf("%d: %s\n", i, notes[i].title);
        }
    }
}

static Note *note_select(void)
{
    int index = -1;

    printf("Enter note index: ");
    scanf("%d", &index);
    getchar();

    if (index < 0 || index >= MAX_NOTES) {
        puts("Invalid index");
        return NULL;
    }

    if (notes[index].content == NULL) {
        puts("Note does not exist");
        return NULL;
    }

    return &notes[index];
}

static void note_print(void)
{
    if (selected_note == NULL) {
        puts("No note selected");
        return;
    }

    printf("Title: %s\n", selected_note->title);
    printf("Content: %s\n", selected_note->content);
}

static Note *note_resize(void)
{
    if (selected_note == NULL) {
        puts("No note selected");
        return NULL;
    }

    printf("Enter new title length: ");
    scanf("%d", &selected_note->title_len);
    getchar();

    if (selected_note->title_len < 1 || selected_note->title_len > MAX_TITLE_LEN) {
        puts("Invalid title length");
        return NULL;
    }

    printf("Enter new content length: ");
    scanf("%d", &selected_note->content_len);
    getchar();

    if (selected_note->content_len < 1 ||
        selected_note->content_len > MAX_CONTENT_LEN) {
        puts("Invalid content length");
        return NULL;
    }

    selected_note->content =
        realloc(selected_note->content, selected_note->content_len);

    return selected_note;
}

static Note *note_edit(void)
{
    int choice = 0;

    if (selected_note == NULL) {
        puts("No note selected");
        return NULL;
    }

    printf("Edit what?");
    puts("1. Title");
    puts("2. Content");

    scanf("%d", &choice);
    getchar();

    if (choice == 1) {
        printf("Enter new title: ");
        memset(selected_note->title, 0, sizeof(selected_note->title));
        read(STDIN_FILENO, selected_note->title, selected_note->title_len);
        return selected_note;
    }

    if (choice == 2) {
        printf("Enter new content: ");
        read(STDIN_FILENO, selected_note->content, selected_note->content_len);
        return selected_note;
    }

    puts("Invalid choice");
    return NULL;
}

static void note_delete(void)
{
    if (selected_note == NULL) {
        puts("No note selected");
        return;
    }

    free(selected_note->content);
    selected_note->content = NULL;
    selected_note->title_len = 0;
    selected_note->content_len = 0;
}

static void note_menu(void)
{
    puts("0. Create note");
    puts("1. List notes");
    puts("2. Select note");
    puts("3. Print note");
    puts("4. Resize note");
    puts("5. Edit note");
    puts("6. Delete note");
    puts("7. Exit");
    printf("> ");
}

static void vuln(void)
{
    while (1) {
        int choice = 6;

        note_menu();

        scanf("%d", &choice);
        getchar();

        switch (choice) {
        case 0:
            note_new();
            break;
        case 1:
            note_list();
            break;
        case 2:
            selected_note = note_select();
            break;
        case 3:
            note_print();
            break;
        case 4:
            note_resize();
            break;
        case 5:
            note_edit();
            break;
        case 6:
            note_delete();
            break;
        case 7:
            return;
        default:
            puts("Invalid choice");
            break;
        }
    }
}

int main(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    vuln();

    return 0;
}
