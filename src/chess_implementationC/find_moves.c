#include "find_moves.h"


void find_all_moves(struct ChessBoard *board, signed char *moves, short *moves_count){
    *moves_count = 0;
    short test = 0;

    if (board->color_to_move == 1){
        for (unsigned char ind = 0; ind < board->piece_count; ind++){
            if (board->white_piece_alive[ind]){
                if (board->pawn[ind]){
                    continue;
                }else if(board->king[ind]){
                    continue;
                }else{
                    if (board->white_piece_jump_moves[ind][0] > 1){
                        find_jump_moves(board, board->white_piece_pos, board->white_piece_jump_moves[ind], moves, moves_count, ind);
                    }
                    if (board->white_piece_move_directions[ind][0] > 1){
                        find_move_directions(board, board->white_piece_pos, board->white_piece_move_directions[ind], moves, moves_count, ind);
                    }
                }
            }
        }
    }else{
        printf("");
    }

    
}

bool on_board(signed char x, unsigned char size){
    return (x >= 0 && x < size);
}

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
            add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y,-1, moves, moves_count);
        }
    }

}


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
                add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, -1, moves, move_counts);
            }else if((board->board[field_x][field_y] >= 0) == (board->board[color_pos[piece_pos_ind]],color_pos[piece_pos_ind+1] >= 0)){
                break;
            }else{
                add_move(color_pos[piece_pos_ind], color_pos[piece_pos_ind+1], field_x, field_y, -1, moves, move_counts);
            }
            field_x += piece_move_directions[ind_md];
            field_y += piece_move_directions[ind_md+1]; 
            
            dist += 1;
        }    
        
    }
}


void add_move(signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type, signed char* moves, short *moves_count){
    moves[*moves_count] = from_x;
    moves[(*moves_count) + 1] = from_y;
    moves[(*moves_count) + 2] = to_x;
    moves[(*moves_count) + 3] = to_y;
    moves[(*moves_count) + 4] = move_type;
    (*moves_count) += 5;
}  


