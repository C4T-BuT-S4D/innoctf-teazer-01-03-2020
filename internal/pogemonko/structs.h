#ifndef STRUCTS_H
#define STRUCTS_H

typedef struct Pokemon
{
    char name[56];
    char *description;
    unsigned int power;
    struct Pokemon *next;
} Pokemon;

typedef struct User
{
    char username[64];
    char password[64];
    Pokemon *pokemons;
} User;

#endif