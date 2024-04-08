#include "test_engin.h" 



void test_engine(struct ChessBoard *board, int depth){

    int count = 0;
    
    //test_engine_all_moves(board, depth, &count);

    printf("moves : %d", count);

    printChessBoard(board);
}

void test_engine_all_moves(struct ChessBoard *board, int depth, int *count){
    if(board->white_piece_alive[board->king_pos] == false || board->black_piece_alive[board->king_pos] == false){
        printf("fehler");
    }
    *count += 1;

    if (depth >0){
        
        signed char moves[2000];
        short move_count = 0;
        find_all_moves(board, moves, &move_count);


        if(!all_legal(board, moves, &move_count)){
            *count -= 1;
            //printf("illigal");
        }else{
            if(depth > 1){
                for(short i = 0; i < move_count; i+=5){

                    make_move(board, moves[i], moves[i+1], moves[i+2], moves[i+3], moves[i+4]);

                    test_engine_all_moves(board, depth-1, count);

                    undo_last_move(board);
                }
            }
        }
    }


}

bool all_legal(struct ChessBoard *board, signed char *moves, short *move_count){
    for(short i = 0; i < *move_count; i+=5){
        if(!is_legal(board, moves[i], moves[i+1], moves[i+2], moves[i+3], moves[i+4])){
            //printf("warum");
            return false;
        }
    }
    return true;
}


bool is_legal(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    if(move_type == -3){
        printf("castling");
    }
    if( (board->color_to_move == -1 && board->white_piece_pos[board->king_pos<<1] == to_x && board->white_piece_pos[(board->king_pos<<1)+1] == to_y) || (board->color_to_move == 1 && board->black_piece_pos[board->king_pos<<1] == to_x && board->black_piece_pos[(board->king_pos<<1)+1] == to_y)){
        //printf(" \n (%d, %d) -> (%d , %d) %d", from_x, from_y, to_x, to_y, move_type);
        //printf(" \n white_king (%d ,%d), black_king (%d ,%d) ind %d", board->white_piece_pos[board->king_pos<<1], board->white_piece_pos[(board->king_pos<<1)+1], board->black_piece_pos[board->king_pos<<1], board->black_piece_pos[(board->king_pos<<1)+1], board->king_pos);
        return false;
    }
    return true;

}