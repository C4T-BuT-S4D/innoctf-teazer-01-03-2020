#ifndef DB_H
#define DB_H

User *get_user(const char *);
void save_user(User *);
void add_pokemon(User *u, Pokemon *p);

#endif