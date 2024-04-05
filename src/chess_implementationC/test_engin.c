#include "test_engin.h"


// Struktur für Argumente, die an den Thread übergeben werden
struct ThreadArgs {
    struct ChessBoard *board;
    int depth;
    int *count;
};

// Funktion, die von jedem Thread ausgeführt wird
DWORD WINAPI thread_function(LPVOID lpParam) {
    struct ThreadArgs *args = (struct ThreadArgs *)lpParam;
    printf("sogar hier");
    test_engine_all_moves(args->board, args->depth, args->count);
    return 0;
}

// Funktion zum Parallelisieren des Testens aller Züge
void parallel_test_engine_all_moves(struct ChessBoard *board, int depth, int *count) {
    // Array für Thread-Handles
    HANDLE threads[NUM_THREADS];
    // Array für Argumente an Threads übergeben
    struct ThreadArgs thread_args[NUM_THREADS];

    printf("angekommen");

    // Erstellen und Ausführen von Threads
    for (int i = 0; i < NUM_THREADS; i++) {
        printf("hier");
        struct ChessBoard board_copy;
        thread_args[i].board = copy_board(board, &board_copy);
        thread_args[i].depth = depth;
        thread_args[i].count = count;
        threads[i] = CreateThread(NULL, 0, thread_function, &thread_args[i], 0, NULL);
        if (threads[i] == NULL) {
            fprintf(stderr, "Fehler beim Erstellen des Threads\n");
            return;
        }
    }

    // Auf das Beenden aller Threads warten
    WaitForMultipleObjects(NUM_THREADS, threads, TRUE, INFINITE);
    // Schließen der Thread-Handles
    for (int i = 0; i < NUM_THREADS; i++) {
        CloseHandle(threads[i]);
    }
}

// Ihre ursprüngliche test_engine Funktion
void test_engine(struct ChessBoard *board, int depth){
    int count = 0;
    printf("hey %d", NUM_THREADS);
    parallel_test_engine_all_moves(board, depth, &count);

    printf("moves %d\n", count);
}



void test_engine_all_moves(struct ChessBoard *board, int depth, int *count){
    printf("i tryed");
    *count += 1;


    if (depth >0){
        
        signed char moves[1000];
        short move_count = 0;
        find_all_moves(board, moves, &move_count);

        

        for(short i = 0; i < move_count; i+=5){

            if(depth == 5 && move_count > 270){
                printChessBoard(board);
            }
            make_move(board, moves[i], moves[i+1], moves[i+2], moves[i+3], moves[i+4]);

            test_engine_all_moves(board, depth-1, count);

            undo_last_move(board);
        }
    }


}