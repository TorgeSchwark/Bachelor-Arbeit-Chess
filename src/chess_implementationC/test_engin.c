#include "test_engin.h" 
int moves_pos_count = 0;
int moves_pos[] = {4,1,4,3,-2, 2,6,2,4,-2, 4,3,4,4,-1, 3,6,3,4,-2, 4,0,4,3,-1};


void legal_moves(struct ChessBoard *board, short move_count, char *moves, bool *legal){
    
    for(int ind = 0; ind < move_count; ind += 5){
        make_move(board, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
        
        signed char moves_legal[2000];
        short move_count_legal = 0;
        
        find_all_moves(board, moves_legal, &move_count_legal);
    
        if(all_legal(board, moves_legal, &move_count_legal)){
            legal[ind/5] = true;
        }else{
            legal[ind/5] = false;
        }
        if(board->fifty_move_rule[board->move_count-1] >= 50 || board->move_count > 2000){
            legal[ind/5] = false;
            printf("hey illegal");
        }
        undo_last_move(board);
    }
}

void test_engine(struct ChessBoard *board, int depth){

    long long count = 0;
    
    //test_engine_all_moves(board, depth, &count);

    for(short i = 0; i < moves_pos_count; i+=5){
        make_move(board, moves_pos[i], moves_pos[i+1], moves_pos[i+2], moves_pos[i+3], moves_pos[i+4]);
       
    }

    test_engine_all_moves(board, depth, &count);
    printf("\n moves %d \n", count);
    
}

void count_for_each_move(struct ChessBoard *board, int depth){
    char chess_not[] = "hgfedcba";
    long long counts[400];
    signed char moves[2000];
    signed char debug_moves[2000];
    short move_count_debug = 0;
    int sum = 0;
    for (int i = 0; i < 400; i++){
        counts[i] = 0;
    }
    short move_count = 0;
    find_all_moves(board, moves, &move_count);
    printf( "moves %d \n", move_count);

    for(short i = 0; i < move_count; i+=5){
        
        make_move(board, moves[i], moves[i+1], moves[i+2], moves[i+3], moves[i+4]);
        if(moves[i] == 4 && moves[i+1] == 0 && moves[i+2] == 4 && moves[i+3] == 3){
            printChessBoard(board);
            find_all_moves(board, debug_moves, &move_count_debug);
            for(int m = 0; m < move_count_debug; m +=5){
                 printf(" move (%c, %d) -> (%c,%d) %d \n",  chess_not[debug_moves[m]], debug_moves[m+1]+1, chess_not[debug_moves[m+2]], debug_moves[m+3]+1, debug_moves[m+4]);
            }
            break;
        }
        test_engine_all_moves(board, depth-1, &counts[i/5]);

        undo_last_move(board);

        
    }

    for(short i = 0; i < move_count; i+=5){
        sum += counts[i/5];
        printf("after move (%c, %d) -> (%c,%d) %d there are %d moves \n",  chess_not[moves[i]], moves[i+1]+1, chess_not[moves[i+2]], moves[i+3]+1, moves[i+4], counts[i/5]);
    }
    printf("all moves %d\n", sum);

}

void test_engine_all_moves(struct ChessBoard *board, int depth, long long *count){
    if(board->white_piece_alive[board->king_pos] == false || board->black_piece_alive[board->king_pos] == false){
        printf("fehler");
    }
    if(depth == 1){
        *count += 1;
    }

    if (depth >0){
        
        signed char moves[2000];
        short move_count = 0;
        find_all_moves(board, moves, &move_count);


        if(!all_legal(board, moves, &move_count)){
            if(depth == 1){
                *count -= 1;
            }
            
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

//check castling
bool all_legal(struct ChessBoard *board, signed char *moves, short *move_count){
    for(short i = 0; i < *move_count; i+=5){
        if(!is_legal(board, moves[i], moves[i+1], moves[i+2], moves[i+3], moves[i+4])){
            return false;
        }
    }
    if(board->past_moves[board->move_count*5-1] == -3){
        signed char sav_from_x = board->past_moves[board->move_count*5-5];
        signed char sav_from_y = board->past_moves[board->move_count*5-4];
        signed char sav_to_x = board->past_moves[board->move_count*5-3];
        signed char sav_to_y = board->past_moves[board->move_count*5-2];
        signed char sav_move_type = board->past_moves[board->move_count*5-1];
        undo_last_move(board);

        signed char past_moves[2000];
        short past_moves_count = 0;
        board->color_to_move = -board->color_to_move;
        find_all_moves(board, past_moves, &past_moves_count);
        board->color_to_move = -board->color_to_move;
        make_move(board, sav_from_x, sav_from_y, sav_to_x, sav_to_y, sav_move_type);
        
        //to know wether white was in check we need to undo the castling and genereate the moves for black even though its whites turn ...

        signed char from_x = board->past_moves[board->move_count*5-5];
        signed char from_y = board->past_moves[board->move_count*5-4];
        signed char to_x = board->past_moves[board->move_count*5-3];
        signed char to_y = board->past_moves[board->move_count*5-2];
        signed char king_x;
        signed char king_y;
        signed char direction;
        if(board->color_to_move == 1){
            king_x = board->black_piece_pos[board->king_pos<<1];
            king_y = board->black_piece_pos[(board->king_pos<<1)+1];
        }else{
            king_x = board->white_piece_pos[board->king_pos<<1];
            king_y = board->white_piece_pos[(board->king_pos<<1)+1];
        }
        if(from_x > to_x){
            direction = -1; // king pos has already changed check from new field to old one !
        }else{ 
            direction = 1;
        }
        for(int i = 0; i < 3; i++){
            for(short ind = 0; ind < past_moves_count; ind+=5){
                if(past_moves[ind+2] == king_x && past_moves[ind+3] == king_y){
                    printf("illegal_castling");
                    return false;
                }
            }
            king_x += direction;
        }

    }
    return true;
}


bool is_legal(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    if( (board->color_to_move == -1 && board->white_piece_pos[board->king_pos<<1] == to_x && board->white_piece_pos[(board->king_pos<<1)+1] == to_y) || (board->color_to_move == 1 && board->black_piece_pos[board->king_pos<<1] == to_x && board->black_piece_pos[(board->king_pos<<1)+1] == to_y)){
        return false;
    }
    return true;

}