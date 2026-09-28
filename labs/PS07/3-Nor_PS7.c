#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>

#define INITIAL_STOCK 10000
#define ITERATIONS 10000

int stock = INITIAL_STOCK;
int force_yield = 0;

void change_stock(int amount) {
    int snapshot = stock;
    snapshot += amount;

    if (force_yield) {
        sched_yield();
    }

    stock = snapshot;
}

void *worker(void *arg) {
    (void)arg;

    for (int i = 0; i < ITERATIONS; i++) {
        change_stock(+1);
        change_stock(-1);
    }

    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <threads> <yield: 0|1>\n", argv[0]);
        return 1;
    }

    int thread_count = atoi(argv[1]);
    force_yield = atoi(argv[2]);

    if (thread_count < 1 || (force_yield != 0 && force_yield != 1)) {
        fprintf(stderr, "Invalid arguments\n");
        return 1;
    }

    pthread_t *threads = malloc(sizeof(*threads) * thread_count);
    if (threads == NULL) {
        perror("malloc");
        return 1;
    }

    for (int i = 0; i < thread_count; i++) {
        if (pthread_create(&threads[i], NULL, worker, NULL) != 0) {
            fprintf(stderr, "pthread_create failed\n");
            free(threads);
            return 1;
        }
    }

    for (int i = 0; i < thread_count; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("threads=%d yield=%d expected=%d actual=%d\n",
           thread_count, force_yield, INITIAL_STOCK, stock);

    free(threads);
    return 0;
}