#include "make_moves.h"

/* this code is well tested for NORMAL chess rules via playing and undoing many games ont the same board without braking it as well as runing the chess engine based on this code */

/* executes a move therefore calls the make move function wich is responsible for it*/
void make_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    switch (move_type){
        case -1:
        case -2:
            make_normal_move(board, from_x, from_y, to_x, to_y, move_type);
            break;
        case -3:
            make_castling_move(board, from_x, from_y, to_x, to_y, move_type);
            break;
        case -4:
            make_en_passant(board, from_x, from_y, to_x, to_y, move_type);
            break;
        default:
            make_promotion(board, from_x, from_y, to_x, to_y, move_type);
            break;
    }

}

/* executes a normal move updating every thing in the ChessBoard needed */
void make_normal_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    
    signed char piece_number = board->board[from_x][from_y];
    signed char pos_in_piece_list = abs(piece_number)-1;
   
    if ((board->color_to_move == 1 && board->white_pawn[pos_in_piece_list]) || (board->color_to_move == -1 && board->black_pawn[pos_in_piece_list])){
        board->fifty_move_rule[board->move_count] = 0;
    }else{
        if(board->move_count >= 1){
            board->fifty_move_rule[board->move_count] = board->fifty_move_rule[board->move_count-1]+1;
        }else{
            board->fifty_move_rule[board->move_count] = 1;
        }
    }
    board->board[from_x][from_y] = 0;
    if (board->board[to_x][to_y] != 0){
        board->fifty_move_rule[board->move_count] = 0;
        board->captured_piece[board->move_count] = board->board[to_x][to_y];
        if (board->color_to_move == 1){
            board->black_piece_alive[abs(board->board[to_x][to_y])-1] = false;
        }else{
            board->white_piece_alive[board->board[to_x][to_y]-1] = false;
        }
    }else{
        board->captured_piece[board->move_count] = 0;
    }

    if (board->color_to_move == 1){
        if (board->white_piece_first_move[pos_in_piece_list] == -1){
            board->white_piece_first_move[pos_in_piece_list] = board->move_count;
        }
        board->white_piece_pos[pos_in_piece_list<<1] = to_x;
        board->white_piece_pos[(pos_in_piece_list<<1)+1] = to_y; 
    }else{
        if (board->black_piece_first_move[pos_in_piece_list] == -1){
            board->black_piece_first_move[pos_in_piece_list] = board->move_count;
        }
        board->black_piece_pos[pos_in_piece_list<<1] = to_x;
        board->black_piece_pos[(pos_in_piece_list<<1)+1] = to_y; 
    }

    save_in_last_moves(board, from_x, from_y, to_x, to_y, move_type);

    board->board[to_x][to_y] = piece_number;
    board->color_to_move = -board->color_to_move;
    board->move_count += 1;
}

/* executes an en passant move */
void make_en_passant(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    board->board[to_x][to_y] = board->board[from_x][from_y];
    board->board[from_x][from_y] = 0;
    board->captured_piece[board->move_count] = board->board[to_x][from_y];

    if(board->color_to_move == 1){
        board->white_piece_pos[(board->board[to_x][to_y]-1)<<1] = to_x;
        board->white_piece_pos[((board->board[to_x][to_y]-1)<<1)+1] = to_y;
        board->black_piece_alive[abs(board->board[to_x][from_y])-1] = false;
    }else{
        board->black_piece_pos[(abs(board->board[to_x][to_y])-1)<<1] = to_x;
        board->black_piece_pos[((abs(board->board[to_x][to_y])-1)<<1)+1] = to_y;
        board->white_piece_alive[board->board[to_x][from_y]-1] = false;
    }
    board->board[to_x][from_y] = 0;

    save_in_last_moves(board, from_x, from_y, to_x, to_y, move_type);

    board->fifty_move_rule[board->move_count] = 0;
    board->color_to_move = -board->color_to_move;
    board->move_count += 1;
    
}

/* Executes a castling move */
void make_castling_move(struct ChessBoard* board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    signed char king_moving_direction = (from_x > to_x) ? 2 : -2;

    if (board->color_to_move == 1){
        board->board[board->white_piece_pos[board->king_pos<<1] + king_moving_direction][from_y] = board->board[board->white_piece_pos[board->king_pos<<1]][from_y];
        board->board[board->white_piece_pos[board->king_pos<<1]][from_y] = 0;
        board->white_piece_pos[board->king_pos<<1] = board->white_piece_pos[board->king_pos<<1] + king_moving_direction;
        board->white_piece_first_move[board->king_pos] = board->move_count;
    }else{
        board->board[board->black_piece_pos[board->king_pos<<1]+king_moving_direction][from_y] = board->board[board->black_piece_pos[board->king_pos<<1]][from_y];
        board->board[board->black_piece_pos[board->king_pos<<1]][from_y] = 0;
        board->black_piece_pos[board->king_pos<<1] = board->black_piece_pos[board->king_pos<<1] + king_moving_direction;
        board->black_piece_first_move[board->king_pos] = board->move_count;
    }

    make_normal_move(board, from_x, from_y, to_x, to_y, move_type);

}

/* executes a promotion. Careful: pawns wont be able to walk over edges even after proming to a piece that can. The undo promotion makes the pawn to a normal Chess pawn !*/
void make_promotion(struct ChessBoard* board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
 
    if(board->color_to_move == 1){
        signed char piece_to_ind = board->non_pawn_pieces[move_type];
        signed char piece_ind = board->board[from_x][from_y]-1;
        for(unsigned char jm_ind = 0; jm_ind < board->white_piece_jump_moves[piece_to_ind][0]; jm_ind += 1){
            board->white_piece_jump_moves[piece_ind][jm_ind] = board->white_piece_jump_moves[piece_to_ind][jm_ind];
        }
        if(board->white_piece_jump_moves[piece_to_ind][0] == 0){
            board->white_piece_jump_moves[piece_ind][0] = 0;
        }
        for(unsigned char md_ind = 0; md_ind < board->white_piece_move_directions[piece_to_ind][0]; md_ind += 1){
            board->white_piece_move_directions[piece_ind][md_ind] = board->white_piece_move_directions[piece_to_ind][md_ind];
        }
        if(board->white_piece_move_directions[piece_to_ind][0] == 0){
            board->white_piece_move_directions[piece_ind][0] = 0;
        }
        //board->white_piece_img[piece_ind] = board->white_piece_img[piece_to_ind];
        board->white_pawn[piece_ind] = false;
        board->white_piece_img[piece_ind] = board->white_piece_img[piece_to_ind];
    }else{
        signed char piece_to_ind = board->non_pawn_pieces[move_type];
        signed char piece_ind = (-board->board[from_x][from_y])-1;
        for(unsigned char jm_ind = 0; jm_ind < board->black_piece_jump_moves[piece_to_ind][0]; jm_ind += 1){
            board->black_piece_jump_moves[piece_ind][jm_ind] = board->black_piece_jump_moves[piece_to_ind][jm_ind];
        }
        if(board->black_piece_jump_moves[piece_to_ind][0] == 0){
            board->black_piece_jump_moves[piece_ind][0] = 0;
        }
        for(unsigned char md_ind = 0; md_ind < board->black_piece_move_directions[piece_to_ind][0]; md_ind += 1){
            board->black_piece_move_directions[piece_ind][md_ind] = board->black_piece_move_directions[piece_to_ind][md_ind];
        }
        if(board->black_piece_move_directions[piece_to_ind][0] == 0){
            board->black_piece_move_directions[piece_ind][0] = 0;
        }
        //board->black_piece_img[piece_ind] = board->black_piece_img[piece_to_ind];
        board->black_pawn[piece_ind] = false;
        board->black_piece_img[piece_ind] = board->black_piece_img[piece_to_ind];
    }
    make_normal_move(board, from_x, from_y, to_x, to_y, move_type);
}

/* undoes the last move therefor calls the last funktion responsible for it */
void undo_last_move(struct ChessBoard *board){
   
    switch (board->past_moves[board->move_count*5-1]){
        case -1:
        case -2:
            undo_normal_move(board, board->past_moves[board->move_count*5-5], board->past_moves[board->move_count*5-4], board->past_moves[board->move_count*5-3], board->past_moves[board->move_count*5-2], board->past_moves[board->move_count*5-1]);
            break;
        case -3:
            undo_castling_move(board, board->past_moves[board->move_count*5-5], board->past_moves[board->move_count*5-4], board->past_moves[board->move_count*5-3], board->past_moves[board->move_count*5-2], board->past_moves[board->move_count*5-1]);
            break;
        case -4:
            undo_en_passant(board, board->past_moves[board->move_count*5-5], board->past_moves[board->move_count*5-4], board->past_moves[board->move_count*5-3], board->past_moves[board->move_count*5-2], board->past_moves[board->move_count*5-1]);
            break;
        default:
            undo_promotion(board, board->past_moves[board->move_count*5-5], board->past_moves[board->move_count*5-4], board->past_moves[board->move_count*5-3], board->past_moves[board->move_count*5-2], board->past_moves[board->move_count*5-1]);
            break;
    }
}

/* undoes normal moves */
void undo_normal_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    
    board->board[from_x][from_y] = board->board[to_x][to_y];
    board->board[to_x][to_y] = board->captured_piece[board->move_count-1];
    board->captured_piece[board->move_count] = 0;
    board->fifty_move_rule[board->move_count] = 0;

    if (board->color_to_move == 1){
        board->black_piece_pos[(abs(board->board[from_x][from_y])-1)<<1] = from_x;
        board->black_piece_pos[((abs(board->board[from_x][from_y])-1)<<1)+1] = from_y;
        if(board->board[to_x][to_y]-1 >= 0){
            board->white_piece_alive[board->board[to_x][to_y]-1] = true;
        }
        if(board->black_piece_first_move[abs(board->board[from_x][from_y])-1] == board->move_count-1){
           board->black_piece_first_move[abs(board->board[from_x][from_y])-1] = -1; 
        }
    }else{
        board->white_piece_pos[(board->board[from_x][from_y]-1)<<1] = from_x;
        board->white_piece_pos[((board->board[from_x][from_y]-1)<<1)+1] = from_y;
        if(abs(board->board[to_x][to_y])-1 >= 0){
             board->black_piece_alive[abs(board->board[to_x][to_y])-1] = true;
        }
        if(board->white_piece_first_move[(board->board[from_x][from_y])-1] == board->move_count-1){
           board->white_piece_first_move[(board->board[from_x][from_y])-1] = -1; 
        }
    }


    board->color_to_move = -board->color_to_move;
    board->move_count -= 1;   
}

/* undoes en passant moves*/
void undo_en_passant(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    
    undo_normal_move(board, from_x, from_y, to_x, to_y, move_type);

    if(board->color_to_move == 1){
        board->black_piece_pos[(abs(board->board[to_x][to_y])-1)<<1] = to_x;
        board->black_piece_pos[((abs(board->board[to_x][to_y])-1)<<1)+1] = from_y;
        board->black_piece_alive[(abs(board->board[to_x][to_y])-1)] = true;
    }else{
        board->white_piece_pos[((board->board[to_x][to_y])-1)<<1] = to_x;
        board->white_piece_pos[(((board->board[to_x][to_y])-1)<<1)+1] = from_y;
        board->white_piece_alive[((board->board[to_x][to_y])-1)] = true;
    }

    board->board[to_x][from_y] = board->board[to_x][to_y];
    board->board[to_x][to_y] = 0;
}

/* undoes a castling move */
void undo_castling_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    signed char king_moving_direction = (from_x > to_x) ? -2 : 2;

    if(board->color_to_move == 1){
        board->board[board->black_piece_pos[board->king_pos<<1]][board->black_piece_pos[(board->king_pos<<1)+1]] = 0;
        board->black_piece_pos[board->king_pos<<1] += king_moving_direction;
        board->board[board->black_piece_pos[board->king_pos<<1]][board->black_piece_pos[(board->king_pos<<1)+1]] = -(board->king_pos+1);
        board->black_piece_first_move[board->king_pos] = -1;
    }else{
        board->board[board->white_piece_pos[board->king_pos<<1]][board->white_piece_pos[(board->king_pos<<1)+1]] = 0;
        board->white_piece_pos[board->king_pos<<1] += king_moving_direction;
        board->board[board->white_piece_pos[board->king_pos<<1]][board->white_piece_pos[(board->king_pos<<1)+1]] = (board->king_pos+1);
        board->white_piece_first_move[board->king_pos] = -1;
    }

    undo_normal_move(board, from_x, from_y, to_x, to_y, move_type);
}

/* undoes a promotion. Undoing a promotion the piece is turned into a NORMAL chess pawn */
void  undo_promotion(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    // there is no need to reset castling etc since pawn is checked first in find_moves also boarder_x, boarder_y is not enabled for pawn
    if(board->color_to_move == 1){
        signed char piece_ind = (-board->board[to_x][to_y])-1;
        board->black_pawn[piece_ind] = true;
        board->black_piece_move_directions[piece_ind][0] = 4;
        board->black_piece_move_directions[piece_ind][1] = 0;
        board->black_piece_move_directions[piece_ind][2] = -1;
        board->black_piece_move_directions[piece_ind][3] = 1;
        board->black_piece_jump_moves[piece_ind][0] = 0;
        board->black_piece_img[piece_ind] = 1;
    }else{
        signed char piece_ind = board->board[to_x][to_y]-1;
        board->white_pawn[piece_ind] = true;
        board->white_piece_move_directions[piece_ind][0] = 4;
        board->white_piece_move_directions[piece_ind][1] = 0;
        board->white_piece_move_directions[piece_ind][2] = 1;
        board->white_piece_move_directions[piece_ind][3] = 1;
        board->white_piece_jump_moves[piece_ind][0] = 0;
        board->white_piece_img[piece_ind] = 1;
    }
    undo_normal_move(board, from_x, from_y, to_x, to_y, move_type);
}

/* saves the last move in the last_moves list */
void save_in_last_moves(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    board->past_moves[board->move_count*5] = from_x;
    board->past_moves[board->move_count*5+1] = from_y;
    board->past_moves[board->move_count*5+2] = to_x;
    board->past_moves[board->move_count*5+3] = to_y;
    board->past_moves[board->move_count*5+4] = move_type;
}
    