#include <stdio.h>
#include <stdlib.h>

typedef struct elf {
    unsigned int n;
    struct elf *next;
} elf;

int main(int argc, char **argv) {
    int n_elves = atoi(argv[1]);

    elf *elves = (elf*)malloc(sizeof(elf) * n_elves);

    for (int i = 0; i < n_elves; i++) {
        elf *e = elves + i;
        e->n = i + 1;
        e->next = e + 1;
    }
    (elves + n_elves - 1)->next = elves;

    elf *e = elves;
    elf *f = elves;
    int steps = 0;
    while (n_elves > 1) {
        int forward = n_elves / 2;

        elf *p;
        for (; steps < forward; steps++) {
            p = f;
            f = f->next;
        }

        f = p->next = f->next;
        steps--;
        n_elves--;

        if (n_elves % 10000 == 0) {
            printf("%d elves remaining.\n", n_elves);
        }

        e = e->next;
    }

    printf("%d\n", e->n);
}
