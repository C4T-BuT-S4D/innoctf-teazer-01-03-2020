#include "structs.h"
#include "utils.h"
#include <string.h>
#include <ctype.h>

int
check_username(const char *username)
{
    int len = strlen(username);

    for (int i = 0; i < len; ++i) {
        if (!isalnum(username[i])) {
            return 0;
        }
    }

    return 1;
}

unsigned int
get_pokemons_cnt(User *u)
{
    unsigned int pokemons = 0;
    Pokemon *cur = u->pokemons;
    while (cur != NULL) {
        ++pokemons;
        cur = cur->next;
    }

    return pokemons;
}