CC=gcc

.PHONY: all
all: pogemonko

pogemonko: main.o db.o utils.o
	$(CC) -o $@ $^

main.o: main.c structs.h
	$(CC) -c -o $@ $<

db.o: db.c db.h structs.h
	$(CC) -c -o $@ $<

utils.o: utils.c utils.h structs.h
	$(CC) -c -o $@ $<

.PHONY: clean
clean:
	rm -rf ./*.o
	rm -rf ./pogemonko