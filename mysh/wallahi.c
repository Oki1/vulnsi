#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <ctype.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>

#define CHAR_BUF_SIZE 512
#define MAX_ARGS 32

char *command[MAX_ARGS];
int command_size;

char name[512];
short exit_status;


/* Hidden function present in the binary */
void win(void)
{
    system("/bin/sh");
}


void readline(char *input)
{
    int i;
    int pos;
    char c;

    for (i = 0; i < command_size; i++)
        command[i][0] = '\0';

    command_size = 0;

    c = input[0];
    pos = 1;

    /* Skip leading whitespace */
    while (isspace((unsigned char)c)) {
        c = input[pos++];
    }

    /* Comment */
    if (c == '#') {
        while (c != '\n')
            c = input[pos++];

        command[0][0] = '\0';
        return;
    }

    if (c == '\n') {
        command[0][0] = '\0';
        return;
    }

    if (c == EOF)
        exit(0);

    int out = 0;

    while (c != '\n' && c != '\0') {

        if (c == '"') {

            c = input[pos++];

            while (c != '"') {

                if (out > CHAR_BUF_SIZE) {
                    printf(
                        "CHAR_BUF_SIZE limit (%d) exceeded at line %d\n",
                        CHAR_BUF_SIZE,
                        0x39
                    );
                    exit(1);
                }

                command[command_size][out++] = c;
                command[command_size][out] = '\0';

                c = input[pos++];
            }

            c = input[pos++];
        }

        else if (!isspace((unsigned char)c)) {

            command[command_size][out++] = c;
            command[command_size][out] = '\0';

            c = input[pos++];
        }

        else {

            command_size++;
            out = 0;

            while (isspace((unsigned char)c) && c != '\n')
                c = input[pos++];
        }
    }

    command_size++;
}


void builtin_name(int argc, char **argv)
{
    if (argc < 2)
        puts(name);
    else
        strncpy(name, argv[1], 512);

    exit_status = 0;
}


void builtin_help(void)
{
    puts("      name - Print or change shell name");
    puts("      help - Print short help");
    puts("    status - Print last command status");
    puts("      exit - Exit from shell");
    puts("     print - Print arguments");
    puts("      echo - Print arguments and newline");
    puts("       pid - Print PID");
    puts("      ppid - Print PPID");
    puts(" dirchange - Change directory");
    puts("  dirwhere - Print current working directory");
    puts("   dirmake - Create a directory");
    puts(" dirremove - Remove a directory");
    puts("   dirlist - Print files in current working directory");
    puts("  linkhard - Create hard link");
    puts("  linksoft - Create soft link");
    puts("  linkread - man 2 readlink");
    puts("  linklist - Undocumented...");
    puts("    unlink - Remove a file");
    puts("    rename - Rename a file");

    exit_status = 0;
}


void builtin_status(void)
{
    printf("%d\n", exit_status);
    exit_status = 0;
}


void builtin_exit(int argc, char **argv)
{
    if (argc < 2)
        exit(0);

    exit(atoi(argv[1]));
}


void builtin_print(int argc, char **argv)
{
    printf("%s", argv[1]);

    for (int i = 2; i < argc; i++)
        printf(" %s", argv[i]);

    exit_status = 0;
}


void builtin_echo(int argc, char **argv)
{
    builtin_print(argc, argv);
    puts("");
    exit_status = 0;
}


void builtin_pid(void)
{
    printf("%d\n", getpid());
    exit_status = 0;
}


void builtin_ppid(void)
{
    printf("%d\n", getppid());
    exit_status = 0;
}


void builtin_dirchange(void)
{
    if (command_size < 2) {
        strcpy(command[1], "/");
        command_size = 2;
    }

    errno = 0;

    chdir(command[1]);

    int err = errno;

    if (errno != 0)
        perror("dirchange");

    exit_status = err;
}


void builtin_dirwhere(void)
{
    char buf[512];

    getwd(buf);
    puts(buf);

    exit_status = 0;
}


void builtin_dirmake(int argc, char **argv)
{
    if (argc < 2) {
        puts("No name was specified");
        exit_status = 1;
        return;
    }

    errno = 0;

    mkdir(argv[1], 0777);

    int err = errno;

    if (errno != 0)
        perror("dirmake");

    exit_status = err;
}


void builtin_dirremove(int argc, char **argv)
{
    if (argc < 2) {
        puts("No name was specified");
        exit_status = 1;
        return;
    }

    errno = 0;

    rmdir(argv[1]);

    int err = errno;

    if (errno != 0)
        perror("dirremove");

    exit_status = err;
}


void builtin_dirlist(void)
{
    if (command_size < 2) {
        strcpy(command[1], ".");
        command_size = 2;
    }

    errno = 0;

    DIR *dir = opendir(command[1]);
    int err = errno;

    if (errno != 0) {
        perror("opendir");
        exit_status = err;
        return;
    }

    struct dirent *entry;

    while ((entry = readdir(dir)) != NULL)
        printf("%s  ", entry->d_name);

    puts("");

    errno = 0;
    closedir(dir);

    err = errno;

    if (errno != 0)
        perror("closedir");

    exit_status = err;
}


void builtin_linkhard(int argc, char **argv)
{
    if (argc < 3) {
        puts("Too few arguments");
        return;
    }

    if (link(argv[1], argv[2]) == 0) {
        exit_status = 0;
    } else {
        int err = errno;
        perror("linkhard");
        exit_status = err;
    }
}


void builtin_linksoft(int argc, char **argv)
{
    if (argc < 3) {
        puts("Too few arguments");
        return;
    }

    if (symlink(argv[1], argv[2]) == 0) {
        exit_status = 0;
    } else {
        int err = errno;
        perror("linksoft");
        exit_status = err;
    }
}


void builtin_linkread(int argc, char **argv)
{
    char *buf = malloc(512);

    errno = 0;

    ssize_t len = readlink(argv[1], buf, 511);

    /*
     * This matches the binary's behavior.
     * Note that len == -1 would make this unsafe.
     */
    buf[len] = '\0';

    if (errno == 0) {
        puts(buf);
        exit_status = 0;
    } else {
        int err = errno;
        perror("linkread");
        exit_status = err;
    }

    free(buf);
}


void builtin_linklist(void)
{
    char path[304];
    struct stat info;

    stat(command[1], &info);

    int inode = (int)info.st_ino;

    errno = 0;

    DIR *dir = opendir(".");
    int err = errno;

    if (errno != 0) {
        perror("opendir");
        exit_status = err;
        return;
    }

    struct dirent *entry;

    while ((entry = readdir(dir)) != NULL) {

        path[0] = '.';
        path[1] = '/';

        strcpy(path + 2, entry->d_name);

        lstat(path, &info);

        if ((long)inode == info.st_ino)
            printf("%s  ", path + 2);
    }

    puts("");

    errno = 0;
    closedir(dir);

    err = errno;

    if (errno != 0)
        perror("closedir");

    exit_status = err;
}


void builtin_unlink(void)
{
    errno = 0;

    unlink(command[1]);

    if (errno != 0)
        perror("unlink");

    exit_status = errno;
}


void builtin_rename(void)
{
    errno = 0;

    rename(command[1], command[2]);

    if (errno != 0)
        perror("unlink");

    exit_status = errno;
}


void execute(void)
{
    if (command[0][0] == '\0')
        return;

    if (!strcmp(command[0], "name"))
        builtin_name(command_size, command);

    else if (!strcmp(command[0], "help"))
        builtin_help();

    else if (!strcmp(command[0], "status"))
        builtin_status();

    else if (!strcmp(command[0], "exit"))
        builtin_exit(command_size, command);

    else if (!strcmp(command[0], "print"))
        builtin_print(command_size, command);

    else if (!strcmp(command[0], "echo"))
        builtin_echo(command_size, command);

    else if (!strcmp(command[0], "pid"))
        builtin_pid();

    else if (!strcmp(command[0], "ppid"))
        builtin_ppid();

    else if (!strcmp(command[0], "dirchange"))
        builtin_dirchange();

    else if (!strcmp(command[0], "dirwhere"))
        builtin_dirwhere();

    else if (!strcmp(command[0], "dirmake"))
        builtin_dirmake(command_size, command);

    else if (!strcmp(command[0], "dirremove"))
        builtin_dirremove(command_size, command);

    else if (!strcmp(command[0], "dirlist"))
        builtin_dirlist();

    else if (!strcmp(command[0], "linkhard"))
        builtin_linkhard(command_size, command);

    else if (!strcmp(command[0], "linksoft"))
        builtin_linksoft(command_size, command);

    else if (!strcmp(command[0], "linkread"))
        builtin_linkread(command_size, command);

    else if (!strcmp(command[0], "linklist"))
        builtin_linklist();

    else if (!strcmp(command[0], "unlink"))
        builtin_unlink();

    else if (!strcmp(command[0], "rename"))
        builtin_rename();

    else
        puts("Not found!");
}


void sigchld_handler(int sig)
{
    int status;
    pid_t pid;

    do {
        pid = waitpid(-1, &status, WNOHANG);
    } while (pid > 0);
}


void interactive_mode(void)
{
    char buf[512];

    while (1) {

        printf("%s> ", name);

        if (fgets(buf, 511, stdin) == NULL)
            break;

        readline(buf);
        execute();
    }
}


void setup(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}


int main(void)
{
    setup();

    signal(SIGCHLD, sigchld_handler);

    for (int i = 0; i < MAX_ARGS; i++)
        command[i] = malloc(512);

    interactive_mode();

    for (int i = 0; i < MAX_ARGS; i++) {
        free(command[i]);
        command[i] = NULL;
    }

    return 0;
}
