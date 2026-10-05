void vuln(void)
{
    pid_t pid;
    int status;
    int choice = 0;
    unsigned int hp = 10;

    while (hp > 0) {
        printf("You have %d HP. What do you want to do?\n", hp);
        puts("1. Attack!");
        puts("2. Defend!");
        puts("3. Heal!");
        printf("> ");

        scanf("%d", &choice);

        if (choice == 3) {
            hp += 5;
        }
        else {
            if (choice == 1) {
                pid = fork();

                if (pid == 0) {
                    exit(attack());
                }
            }
            else if (choice == 2) {
                pid = fork();

                if (pid == 0) {
                    exit(defend());
                }
            }

            status = 0;
            wait(&status);

            if ((status >> 8) == 1) {
                hp -= 1;
            }
            else if ((status & 0xff) != 0) {
                puts("Ouch! This was unexpected!");
                hp -= 3;
            }
        }
    }

    puts("You have been defeated!");
}

int attack(void)
{
    char weapon[40];

    puts("What weapon do you want to use?");
    puts("Your options are: sword, bow, staff");

    read(0, weapon, 128);

    if (strstr(weapon, "sword") != NULL) {
        puts("*SLASH* You hit the enemy with your sword!");
    }
    else if (strstr(weapon, "bow") != NULL) {
        puts("*TWANG* You hit the enemy with your bow!");
    }
    else if (strstr(weapon, "staff") != NULL) {
        puts("*WHOOSH* You hit the enemy with your staff!");
    }
    else {
        puts("You missed the enemy!");
    }

    return 1;
}
