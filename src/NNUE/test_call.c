#include "test_call.h"

int main(){

    // init nn weights
    nnue_init("nn-04cf2b4ed1da.nnue");
    printf("hey\n");
    int pieces[33];
    int squares[33];

    struct ChessBoard test_board;
    //printChessBoard(&test_board);
    
    setup_normals(&test_board);
   
    create_chess(&test_board);
   
    board_to_nnue(&test_board, pieces, squares);
    for(int i = 0; i < 33; i++){
        printf("piece %d, squares %d \n", pieces[i], squares[i]);
    }

    printf("score fen: %d \n" ,evaluate_nnue((test_board.color_to_move==-1), pieces, squares));
    // probe NNUE score via FEN input
    clock_t start, end;
    double cpu_time_used;
    start = clock();
    printf("score fen: %d \n" , evaluate_fen_nnue("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"));
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    printf("Die Funktion benötigte %f Sekunden\n", cpu_time_used);
    return 0;
}