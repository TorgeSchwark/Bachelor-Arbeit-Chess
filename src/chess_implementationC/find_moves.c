#include "find_moves.h"

/* this code is well tested for NORMAL chess rules via PERFT debugging */

signed char NORMAL_MOVE = -1;
signed char DOUBLE_PAWN = -2;
signed char CASTLING = -3;
signed char EN_PASSANT = -4;

/* function that finds all moves in the current position. generates illegal moves: king can be captured/exposed. castling when squares are under atack but not if quare is not free*/
void find_all_moves(struct ChessBoard *board, signed char *moves, short *moves_count){
    *moves_count = 0;
    short test = 0;

    if (board->color_to_move == 1){
        for (unsigned char ind = 0; ind < board->piece_count; ind++){
            if (board->white_piece_alive[ind]){
                if (board->white_pawn[ind]){
                    find_pawn_moves(board, board->white_piece_pos, board->white_piece_move_directions[ind], board->white_piece_first_move, moves, moves_count, ind);
                }else if(board->king[ind]){
                    find_jump_moves(board, board->white_piece_pos, board->white_piece_jump_moves[ind], moves, moves_count, ind);
                }else{
                    if (board->white_piece_jump_moves[ind][0] > 1){
                        find_jump_moves(board, board->white_piece_pos, board->white_piece_jump_moves[ind], moves, moves_count, ind);
                    }
                    if (board->white_piece_move_directions[ind][0] > 1){
                        find_move_directions(board, board->white_piece_pos, board->white_piece_move_directions[ind], moves, moves_count, ind);
                    }
                    if (board->castling[ind]){
                        add_castling(board, board->white_piece_pos, board->white_piece_first_move, ind,board->white_piece_alive, moves, moves_count);
                    }
                }
            }
        }
    }else{
        for (unsigned char ind = 0; ind < board->piece_count; ind++){
            if (board->black_piece_alive[ind]){
                if (board->black_pawn[ind]){
                    find_pawn_moves(board, board->black_piece_pos, board->black_piece_move_directions[ind], board->black_piece_first_move, moves, moves_count, ind);
                }else if(board->king[ind]){
                    find_jump_moves(board, board->black_piece_pos, board->black_piece_jump_moves[ind], moves, moves_count, ind);
                }else{
                    if (board->black_piece_jump_moves[ind][0] > 1){
                        find_jump_moves(board, board->black_piece_pos, board->black_piece_jump_moves[ind], moves, moves_count, ind);
                    }
                    if (board->black_piece_move_directions[ind][0] > 1){
                        find_move_directions(board, board->black_piece_pos, board->black_piece_move_directions[ind], moves, moves_count, ind);
                    }
                    if (board->castling[ind]){
                        //continue;
                        add_castling(board, board->black_piece_pos, board->black_piece_first_move, ind, board->black_piece_alive, moves, moves_count);
                    }
                }
            } 
        }
    }
}

/* adds the castling if both the rook and the king didnt move this far and no piece stands in between*/
void add_castling(struct ChessBoard *board, unsigned char *color_pos, short *color_first_move, unsigned char piece_ind, bool *color_alive, signed char *moves, short* moves_count){
    
    if(color_first_move[piece_ind] == -1 && color_first_move[board->king_pos] == -1 && color_alive[board->king_pos]){
        unsigned char piece_pos_ind = piece_ind << 1;
        unsigned char king_pos_ind = board->king_pos << 1;
        signed char direction = (color_pos[piece_pos_ind] < color_pos[king_pos_ind]) ? -1 : 1;
        signed char field_x = color_pos[king_pos_ind] + direction;
        signed char field_y = color_pos[king_pos_ind+1];
        while (field_x != color_pos[piece_pos_ind]){
            if (board->board[field_x][field_y] != 0){
                return;
            }
            field_x += direction;
        }
        add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], color_pos[king_pos_ind]+direction, color_pos[king_pos_ind+1], CASTLING, moves, moves_count);
    }
}

/* checks if a position is on the board */
bool on_board(signed char x, unsigned char size){
    return (x >= 0 && x < size);
}

/* checks if a move goes to the last rank of the correct side*/
bool promotion(signed char y, signed char color, unsigned char size){
    return (color == 1 && y == size-1) || (color == -1 && y == 0);
}

/* adds all jump moves from for one piece */
void find_jump_moves(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_jump_moves, signed char *moves, short *moves_count, unsigned char piece_ind){
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
        if( board->board[field_x][field_y] == 0 || ( board->board[field_x][field_y] >= 0) != board->board[color_pos[piece_pos_ind]][color_pos[piece_pos_ind+1]] >= 0){
           
            add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, NORMAL_MOVE, moves, moves_count);
        }
    }

}

/* adds all pawn moves also en passant promotion and double moves. promoting a pawn dosnt gain the right to move over edges! */
void find_pawn_moves(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_move_directions,short *color_first_moves, signed char *moves, short *moves_count, unsigned char piece_ind){
    unsigned char piece_pos_ind = piece_ind << 1;
    for(unsigned char ind_md = 1; ind_md < piece_move_directions[0]; ind_md+=3){
        unsigned char dist = 1;
        unsigned char range = piece_move_directions[ind_md+2];
        unsigned char real_range = piece_move_directions[ind_md+2];
        signed char field_x = color_pos[piece_pos_ind] + piece_move_directions[ind_md];
        signed char field_y = color_pos[piece_pos_ind+1] + piece_move_directions[ind_md+1];

        if (color_first_moves[piece_ind] == -1){
            range = range << 1;
        }
        while(dist <= range && on_board(field_x, board->size) && on_board(field_y, board->size)){
            if(board->board[field_x][field_y] == 0){
                if (dist <= real_range && !promotion(field_y, board->color_to_move, board->size)){
                    add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, NORMAL_MOVE, moves, moves_count);
                }else if(dist > real_range){
                    add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, DOUBLE_PAWN, moves, moves_count);
                }else{
                    add_promotion(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, board->non_pawn_pieces, moves, moves_count);
                }
            }else{
                break;
            }
            field_x += piece_move_directions[ind_md];
            field_y += piece_move_directions[ind_md+1];
            dist += 1;
        }
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
}

/* adds a en_passant move if it is allowed */
void add_en_passant(struct ChessBoard *board, unsigned char *color_pos,unsigned char piece_pos_ind, signed char *moves, short *moves_count){
    if (board->move_count > 0){
        if (board->past_moves[board->move_count*5-1] == DOUBLE_PAWN){
            if (color_pos[piece_pos_ind+1] == board->past_moves[board->move_count*5-2] && abs(color_pos[piece_pos_ind] - board->past_moves[board->move_count*5-3]) == 1){
                add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], board->past_moves[board->move_count*5-3], board->past_moves[board->move_count*5-2] + board->color_to_move, EN_PASSANT, moves, moves_count);
            }
        }
    }
}

/* finds the moves for all pieces that can move in a direction also resticted range */
void find_move_directions(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_move_directions, signed char *moves, short *move_counts, unsigned char piece_ind){
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
                add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, NORMAL_MOVE, moves, move_counts);
            }else if((board->board[field_x][field_y] >= 0) == (board->board[color_pos[piece_pos_ind]][color_pos[piece_pos_ind+1]] >= 0)){
                break;
            }else{
                add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, NORMAL_MOVE, moves, move_counts);
                break;
            }
            field_x += piece_move_directions[ind_md];
            field_y += piece_move_directions[ind_md+1]; 
            
            dist += 1;
        }    
        
    }
}

/* adds a move to the move stack and increases the move_count */
void add_move(signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type, signed char* moves, short *moves_count){
    moves[*moves_count] = from_x;
    moves[(*moves_count) + 1] = from_y;
    moves[(*moves_count) + 2] = to_x;
    moves[(*moves_count) + 3] = to_y;
    moves[(*moves_count) + 4] = move_type;
    (*moves_count) += 5;
}  

/* adds a promotion to the move stack (the move and every piece the pawn can evolve to)*/
void add_promotion(signed char from_x, signed char from_y, signed char to_x, signed char to_y, unsigned char *non_pawn_pieces, signed char* moves, short *move_count){
    for(unsigned char ind = 1; ind < non_pawn_pieces[0]; ind++){
        add_move(from_x, from_y, to_x, to_y, ind, moves, move_count);
    }
}

/* finds the move in the move stack and returns the index of it */
void real_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, char *piece, signed char* moves, short moves_count, int *ind){
    
    signed char move_type = -10;
    if (piece[0] != 'x'){
        if(piece[0] == 'q'){
            move_type = 4;
        }else if(piece[0] == 'r'){
            move_type = 1;
        }else if(piece[0] == 'b'){
            move_type = 3;
            printf("move_type %d", 3);
        }else{
            printf("move_type %d", 2);
            move_type = 2;
        }
    }
    if((board->color_to_move == 1 && from_x == board->white_piece_pos[board->king_pos<<1] && from_y == board->white_piece_pos[(board->king_pos<<1)+1]) || (board->color_to_move == -1 && from_x == board->black_piece_pos[board->king_pos<<1] && from_y == board->black_piece_pos[(board->king_pos<<1)+1])){
        if(abs(from_x - to_x) == 2){
            move_type = -3;
            if(to_x == 1){
                from_x = 0;
                to_x = 2;
            }else if(to_x == 5){
                from_x = 7;
                to_x = 4;
            }
        }
    }
    
    for(int i = 0; i < moves_count; i+=5){
        if(move_type == -10){
            if(moves[i] == from_x && moves[i+1] == from_y && moves[i+2] == to_x && moves[i+3] == to_y){
                *ind = i;
                
            }
        }else{
            if(moves[i] == from_x && moves[i+1] == from_y && moves[i+2] == to_x && moves[i+3] == to_y && moves[i+4] == move_type){
                
                *ind = i;
            }
        }
    }

}