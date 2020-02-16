#include "structs.h"
#include "db.h"
#include "utils.h"
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void
add_pokemon(User *u, Pokemon *p)
{
    if (u->pokemons == NULL) {
        u->pokemons = p;
        return;
    }

    Pokemon *cur = u->pokemons;
    while (cur->next != NULL) {
        cur = cur->next;
    }

    cur->next = p;
}

unsigned int
load_int(FILE *stream)
{
    unsigned int n = 0;
    char buf[sizeof(n)];
    fread(buf, sizeof(n), 1, stream);
    n = *(unsigned int *)(buf);
    return n;
}

Pokemon *
load_pokemon(FILE *stream)
{
    Pokemon *p = calloc(1, sizeof(*p));
    fread(p->name, sizeof(p->name), 1, stream);
    unsigned int len = load_int(stream);
    p->description = calloc(1, len);
    fread(p->description, sizeof(*p->description), len, stream);
    p->power = load_int(stream);

    return p;
}

User *
get_user(const char *username)
{
    char *filename = calloc(1, strlen("users/") + strlen(username) + 1);
    strcat(filename, "users/");
    strcat(filename, username);
    FILE *f = fopen(filename, "r");

    if (f == NULL) {
        free(filename);
        return NULL;
    }

    User *u = calloc(1, sizeof(*u));
    fread(u->username, sizeof(u->username), 1, f);
    fread(u->password, sizeof(u->password), 1, f);
    unsigned int pokemons = load_int(f);
    Pokemon *cur = NULL;
    for (int i = 0; i < pokemons; ++i) {
        Pokemon *poke = load_pokemon(f);
        if (cur == NULL) {
            u->pokemons = poke;
        } else {
            cur->next = poke;
        }
        cur = poke;
    }

    fclose(f);
    free(filename);

    return u;
}

void
save_int(unsigned int n, FILE *stream)
{
    char buf[sizeof(n)];
    *(unsigned int *)(buf) = n;
    fwrite(buf, sizeof(n), 1, stream);
}

void
save_pokemon(Pokemon *p, FILE *stream)
{
    fwrite(p->name, sizeof(p->name), 1, stream);
    int len = strlen(p->description);
    save_int(len, stream);
    fwrite(p->description, len, 1, stream);
    save_int(p->power, stream);
}

void
save_user(User *u)
{
    char *filename = calloc(1, strlen("users/") + strlen(u->username) + 1);
    strcat(filename, "users/");
    strcat(filename, u->username);
    FILE *f = fopen(filename, "w");
    fwrite(u->username, sizeof(u->username), 1, f);
    fwrite(u->password, sizeof(u->password), 1, f);
    save_int(get_pokemons_cnt(u), f);
    Pokemon *cur = u->pokemons;
    while (cur != NULL) {
        save_pokemon(cur, f);
        cur = cur->next;
    }
    fclose(f);
    free(filename);
}