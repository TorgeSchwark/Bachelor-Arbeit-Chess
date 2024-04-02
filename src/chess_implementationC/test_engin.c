#include "test_engin.h"

void test_engine(struct ChessBoard *board, int depth){
    int count = 0;

    test_engine_all_moves(board, depth, &count);

    printf("%d", count);
}

void test_engine_all_moves(struct ChessBoard *board, int depth, int *count){
    *count += 1;

    if (depth >0){
        signed char moves[500];
        short move_count = 0;
        find_all_moves(board, moves, &move_count);

        for(short i = 0; i < move_count; i+=5){
            make_move(board, moves[i], moves[i+1], moves[i+2], moves[i+3], moves[i+4]);

            test_engine_all_moves(board, depth-1, count);

            undo_last_move(board);
        }
    }


}