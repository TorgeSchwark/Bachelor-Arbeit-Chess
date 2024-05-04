#include "test_engin.h" 
int moves_pos_count = 250; //115
// 5,1,5,2,-1, 2,6,2 ,5 ,-1 , 7, 1, 7 ,3, -2,  3, 6, 3, 5, -1,  1, 0, 2 ,2 ,-1 , 4, 7, 3, 6, -1,  2, 2, 1, 0, -1,  6, 7, 5, 5, -1,  1, 1, 1, 2, -1,  3, 6, 5, 4, -1,  2, 0, 0, 2, -1,  1, 7, 3, 6, -1,  2, 1, 2, 3, -2,  3, 6, 4, 4, -1,  4, 1, 4, 3, -2,  1, 6 ,1 ,4 ,-2 , 7 ,3 ,7 ,4 ,-1,  1, 4, 1, 3, -1,  7, 4 ,7 ,5 ,-1 , 5, 4, 7, 2, -1
int moves_pos[] = {  0 ,1 ,0, 2, -1,  7 ,6 ,7, 5, -1,  6 ,1 ,6, 2, -1,  7 ,5 ,7, 4, -1,  0 ,2 ,0, 3, -1,  4 ,6 ,4, 4, -2,  4 ,1 ,4, 3, -2,  3 ,6 ,3, 4, -2,  2 ,1 ,2, 2, -1,  7 ,7 ,7, 6, -1,  6 ,0 ,5, 2, -1,  4 ,7 ,4, 6, -1,  3 ,0 ,4, 1, -1,  1 ,6 ,1, 4, -2,  6 ,2 ,6, 3, -1,  2 ,6 
,2, 4, -2,  5 ,2 ,6, 0, -1,  7 ,6 ,7, 5, -1,  5 ,0 ,7, 2, -1,  1 ,7 ,3, 6, -1,  2 ,2 ,2, 3, -1,  7 ,4 ,6, 3, -1,  1 ,1 ,1, 2, -1,  3 ,6 ,1, 7, -1,  1 ,0 ,2, 2, -1,  3 ,4 ,2, 3, -1,  2 ,2 ,0, 1, -1,  7 ,5 ,3, 5, -1,  5 ,1 ,5, 2, -1,  6 ,3 ,7, 2, -1,  4 ,0 ,3, 0, -1,  2 ,7 ,4, 5, -1,  3 ,0 ,4, 0, -1,  1 ,4 ,0, 3, -1,  1 ,2 ,1, 3, -1,  4 ,6 ,1, 6, -1,  3 ,1 ,3, 2, -1,  1 ,7 ,0, 5, -1,  4 ,1 ,3, 1, -1,  6 ,6 ,6, 4, -2,  3 ,1 ,3, 0, -1,  6 ,4 ,6, 3, -1,  0 ,0 ,1, 0, -1,  3 ,5 ,1, 5, -1,  6 ,0 ,7, 2, -1,  1 ,6 ,1, 7, -1,  
4 ,0 ,6, 2, -1,  5 ,7 ,6, 6, -1,  3 ,0 ,4, 0, -1,  5 ,6 ,5, 5, -1};


void undo_game(struct ChessBoard *board){
    while(board->move_count > 0){
        undo_last_move(board);
    }
}

void is_check_mate(struct ChessBoard *board, float *matt){
    signed char moves[2000];
    short move_count = 0;
    find_all_moves(board, moves, &move_count);
    bool legal[400];
    legal_moves(board, move_count, moves, legal);
    // wen fifty move rule remie
    if(board->move_count > 0){
        if(board->fifty_move_rule[board->move_count-1] >= 50){
            *matt = 0.5;
            return;
        }
    }
    // wenn 3 fold rep remie
    if(three_fold_repetition(board)){
    
        *matt = 0.5;
        return;

    }
    // wenn nicht 3 fold oder 50 move und legale züge kein ende
    for(int i = 0; i < move_count/5; i++){
        if(legal[i]){
            *matt = 0;
            return;
        }
    }
    
    //wenn keine legale züge und bedrohung matt
    signed char move_from_enemy[2000];
    short enemy_move_count = 0;
    board->color_to_move = -board->color_to_move;
    find_all_moves(board, move_from_enemy, &enemy_move_count);
    for(int i = 0; i < enemy_move_count; i+=5){
        if(!is_legal(board, move_from_enemy[i], move_from_enemy[i+1], move_from_enemy[i+2], move_from_enemy[i+3],move_from_enemy[i+4])){
            board->color_to_move = -board->color_to_move;
            *matt = 1;
            return;
        }
    }
    board->color_to_move = -board->color_to_move;
    // sonst patt
    *matt = 0.5;
}

bool three_fold_repetition(struct ChessBoard *board){
    //printf("1: color to move %d ,move_count %d \n", board->color_to_move, board->move_count);
    signed char current_board[20][20];
    signed char all_moves[2000];
    short current_move_count = 0;
    current_move_count = board->move_count;
    char current_fen[200];
    board_to_fen(board, current_fen);
    copy_moves_and_board(board, current_board, all_moves);
    int same_positions = 0;
    while(board->move_count > 0){
        undo_last_move(board);
        signed char compare_fen[200];
        board_to_fen(board, compare_fen);
        int spaces = 0;
        int compare_ind = 0;
        while(spaces <= 2){
            if(compare_fen[compare_ind] != current_fen[compare_ind]){
                break;
            }
            if(compare_fen[compare_ind] == ' '){
                spaces += 1;
                continue;
            }
            compare_ind += 1;
        }
        if(spaces == 3){
            same_positions += 1;
        }
    }
    //printf("2 :color to move %d ,move_count %d \n", board->color_to_move, board->move_count);
    for(int i = 0; i < current_move_count*5; i+= 5){
        make_move(board, all_moves[i], all_moves[i+1], all_moves[i+2], all_moves[i+3], all_moves[i+4]);
    }
    //printf("3: color to move %d ,move_count %d \n", board->color_to_move, board->move_count);
    if(same_positions > 2){
        printf("MORE THAN 3 REPETITIONS");
        return true;
    }else if(same_positions == 2){
        return true;
    }
    return false;
}

void copy_moves_and_board(struct ChessBoard *board, signed char current_board[20][20], signed char *all_moves){
    for(int i = 0; i < board->size; i++){
        for(int m = 0; m < board->size; m++){
            current_board[i][m] = board->board[i][m];
        }
    }
    for(int i = 0; i < board->move_count*5; i++){
        all_moves[i] = board->past_moves[i];
    }
}

bool same_move(struct ChessBoard *board, int ind, int ind_past){
    if(board->past_moves[ind] == board->past_moves[ind_past] && board->past_moves[ind+1] == board->past_moves[ind_past+1] && board->past_moves[ind+2] == board->past_moves[ind_past+2] && board->past_moves[ind+3] == board->past_moves[ind_past+3] && board->past_moves[ind+4] == board->past_moves[ind_past+4]){
        return true;
    }
    return false;
}

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
        }
        undo_last_move(board);
    }
}

void test_engine(struct ChessBoard *board, int depth){

    long long counts[400];
    char fen[400];
    signed char color;
    bool wrong = false;
    for(short i = 0; i < moves_pos_count; i+=5){
        // printf(" %d, %d ,%d ,%d, %d \n",moves_pos[i], moves_pos[i+1], moves_pos[i+2], moves_pos[i+3], moves_pos[i+4]);
        color = board->color_to_move;
        make_move(board, moves_pos[i], moves_pos[i+1], moves_pos[i+2], moves_pos[i+3], moves_pos[i+4]);

        if(board->color_to_move == color){
            wrong = true;
        }
        if(wrong){
            break;
        }
        for(int ind = 0; ind < MAX_PIECES; ind++){
            if(board->white_piece_alive[ind] && board->board[board->white_piece_pos[ind*2]][board->white_piece_pos[ind*2+1]] != ind +1){
                wrong = true;
            }
            if(board->black_piece_alive[ind] && board->board[board->black_piece_pos[ind*2]][board->black_piece_pos[ind*2+1]] != -(ind +1)){
                wrong = true;
            }
        }
        if(wrong){
            break;
        }
    }
    printChessBoard(board);

    board_to_fen(board, fen);

    count_for_each_move(board, depth, counts);

    // printChessBoard(board);
    
}

void count_for_each_move(struct ChessBoard *board, int depth, long long *counts){
    char chess_not[] = "hgfedcba";
    signed char moves[2000];
    signed char debug_moves[2000];
    short move_count_debug = 0;
    int sum = 0;
    for (int i = 0; i < 400; i++){
        counts[i] = 0;
    }
    short move_count = 0;
    find_all_moves(board, moves, &move_count);

    for(short i = 0; i < move_count; i+=5){
        
        make_move(board, moves[i], moves[i+1], moves[i+2], moves[i+3], moves[i+4]);
        if(moves[i] == 4 && moves[i+1] == 0 && moves[i+2] == 4 && moves[i+3] == 3){
            printChessBoard(board);
            find_all_moves(board, debug_moves, &move_count_debug);
            break;
        }
        test_engine_all_moves(board, depth-1, &counts[i/5]);

        undo_last_move(board);

        
    }

    for(short i = 0; i < move_count; i+=5){
        sum += counts[i/5];
    }
    

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
            if(i != 1){ // if king is in check from a pawn before casling or after we will notice in the legal check above / below if a pawn treatens the field in between we dont the pawn therefore needs to stand infront of the field the king is moving from or to ...
                if((board->board[king_x][king_y-board->color_to_move]) != 0 && ((board->color_to_move == 1 && board->board[king_x][king_y-board->color_to_move] <= 8 && board->board[king_x][king_y-board->color_to_move] > 0 && board->white_pawn[abs(board->board[king_x][king_y-board->color_to_move])-1]) || (board->color_to_move == -1 && board->board[king_x][king_y-board->color_to_move] >= -8 && board->board[king_x][king_y-board->color_to_move] < 0 && board->black_pawn[abs(board->board[king_x][king_y-board->color_to_move])-1]) ) ){
                    return false;
                }
            }
            for(short ind = 0; ind < past_moves_count; ind+=5){
                if(past_moves[ind+2] == king_x && past_moves[ind+3] == king_y){
                    return false;
                }
            }
            king_x += direction;
        }

    }
    return true;
}

int quick_over(struct ChessBoard *board){
    if(!board->white_piece_alive[board->king_pos]){
        return -1;
    }else if(!board->black_piece_alive[board->king_pos]){
        return 1;
    }
    return 0;
}


bool is_legal(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    if( (board->color_to_move == -1 && board->white_piece_pos[board->king_pos<<1] == to_x && board->white_piece_pos[(board->king_pos<<1)+1] == to_y) || (board->color_to_move == 1 && board->black_piece_pos[board->king_pos<<1] == to_x && board->black_piece_pos[(board->king_pos<<1)+1] == to_y)){
        return false;
    }
    return true;

}