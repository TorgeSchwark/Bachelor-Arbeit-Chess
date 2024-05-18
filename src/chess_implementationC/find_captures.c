# include "find_captures.h"

void find_all_captures(struct ChessBoard *board, signed char *moves, short *moves_count){
    *moves_count = 0;
    short test = 0;

    if (board->color_to_move == 1){
        for (unsigned char ind = 0; ind < board->piece_count; ind++){
            if (board->white_piece_alive[ind]){
                if (board->white_pawn[ind]){
                    find_pawn_captures(board, board->white_piece_pos, board->white_piece_move_directions[ind], board->white_piece_first_move, moves, moves_count, ind);
                }else if(board->king[ind]){
                    find_jump_captures(board, board->white_piece_pos, board->white_piece_jump_moves[ind], moves, moves_count, ind);
                }else{
                    if (board->white_piece_jump_moves[ind][0] > 1){
                        find_jump_captures(board, board->white_piece_pos, board->white_piece_jump_moves[ind], moves, moves_count, ind);
                    }
                    if (board->white_piece_move_directions[ind][0] > 1){
                        find_captures_directions(board, board->white_piece_pos, board->white_piece_move_directions[ind], moves, moves_count, ind);
                    }
                }
            }
        }
    }else{
        for (unsigned char ind = 0; ind < board->piece_count; ind++){
            if (board->black_piece_alive[ind]){
                if (board->black_pawn[ind]){
                    find_pawn_captures(board, board->black_piece_pos, board->black_piece_move_directions[ind], board->black_piece_first_move, moves, moves_count, ind);
                }else if(board->king[ind]){
                    find_jump_captures(board, board->black_piece_pos, board->black_piece_jump_moves[ind], moves, moves_count, ind);
                }else{
                    if (board->black_piece_jump_moves[ind][0] > 1){
                        find_jump_captures(board, board->black_piece_pos, board->black_piece_jump_moves[ind], moves, moves_count, ind);
                    }
                    if (board->black_piece_move_directions[ind][0] > 1){
                        find_captures_directions(board, board->black_piece_pos, board->black_piece_move_directions[ind], moves, moves_count, ind);
                    }
                }
            } 
        }
    }
}


/* adds all jump moves from for one piece */
void find_jump_captures(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_jump_moves, signed char *moves, short *moves_count, unsigned char piece_ind){
    unsigned char piece_pos_ind = piece_ind << 1;
    
    for (unsigned char pos_ind = 1; pos_ind < piece_jump_moves[0]; pos_ind+=2){

        signed char field_x = color_pos[piece_pos_ind] + piece_jump_moves[pos_ind];
        signed char field_y = color_pos[piece_pos_ind+1] + piece_jump_moves[pos_ind+1];
        if( !on_board(field_y, board->size)){
            if (board->boarder_y[piece_ind]){
                field_y -= (field_y >= board->size) * board->size;
                field_y += (field_y < 0) * board->size;
            }else{
                continue;
            }
        }
        if (!on_board(field_x, board->size)){
            if(board->boarder_x[piece_ind]){
                field_x -= (field_x >= board->size) * board->size;
                field_x += (field_x < 0) * board->size;
            }else{
                continue;
            }
        }
        if((board->board[field_x][field_y] != 0) && ((board->board[field_x][field_y] >= 0) != board->board[color_pos[piece_pos_ind]][color_pos[piece_pos_ind+1]] >= 0)){
            add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, NORMAL_MOVE, moves, moves_count);
            //printf("md %d \n", board->board[field_x][field_y]);
        }
    }
}

/* adds all pawn moves also en passant promotion and double moves. promoting a pawn dosnt gain the right to move over edges! */
void find_pawn_captures(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_move_directions,short *color_first_moves, signed char *moves, short *moves_count, unsigned char piece_ind){
    unsigned char piece_pos_ind = piece_ind << 1;
    signed char to_y = color_pos[piece_pos_ind+1] + board->color_to_move; // must be on board pawn cant go over board because promotion!
    signed char to_min_x = color_pos[piece_pos_ind]-1;
    signed char to_plus_x = color_pos[piece_pos_ind]+1;

    if (on_board(to_plus_x, board->size) && (board->board[to_plus_x][to_y] > 0) - (board->board[to_plus_x][to_y] < 0) == -board->color_to_move){
        if (promotion(to_y, board->color_to_move, board->size)){
            add_promotion(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], to_plus_x, to_y, board->non_pawn_pieces, moves, moves_count);
        }else{
            add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], to_plus_x, to_y, NORMAL_MOVE, moves,moves_count);
        }
    }
    if (on_board(to_min_x, board->size) && (board->board[to_min_x][to_y] > 0) - (board->board[to_min_x][to_y] < 0) == -board->color_to_move){
        if (promotion(to_y, board->color_to_move, board->size)){
            add_promotion(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], to_min_x, to_y, board->non_pawn_pieces, moves, moves_count);
        }else{
            add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], to_min_x, to_y, NORMAL_MOVE, moves,moves_count);
        }
    }
    add_en_passant(board, color_pos, piece_pos_ind, moves, moves_count);
}

/* finds the moves for all pieces that can move in a direction also resticted range */
void find_captures_directions(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_move_directions, signed char *moves, short *move_counts, unsigned char piece_ind){
    unsigned char piece_pos_ind = piece_ind << 1;
   
    for(unsigned char ind_md = 1; ind_md < piece_move_directions[0]; ind_md+=3){
       
        unsigned char dist = 1;
        signed char field_x = color_pos[piece_pos_ind] + piece_move_directions[ind_md];
        signed char field_y = color_pos[piece_pos_ind+1] + piece_move_directions[ind_md+1];
        while(dist <= piece_move_directions[ind_md+2] || piece_move_directions[ind_md+2] == 0){
            if( !on_board(field_x ,board->size)){
                if( board->boarder_x[piece_ind]){
                    field_x -= (field_x >= board->size) * board->size;
                    field_x += (field_x < 0) * board->size;
                }else{
                    break;
                }
            }
            if( !on_board(field_y, board->size)){
                if (board->boarder_y[piece_ind]){
                    field_y -= (field_y >= board->size) * board->size;
                    field_y += (field_y < 0) * board->size;
                }else{
                    break;
                }
            }
            if (board->board[field_x][field_y] == 0){
                
            }else if((board->board[field_x][field_y] >= 0) == (board->board[color_pos[piece_pos_ind]][color_pos[piece_pos_ind+1]] >= 0)){
                break;
            }else{
                //printf("cd %d \n", board->board[field_x][field_y]);
                add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, NORMAL_MOVE, moves, move_counts);
                break;
            }
            field_x += piece_move_directions[ind_md];
            field_y += piece_move_directions[ind_md+1]; 
            dist += 1;
        }    
        
    }
}


