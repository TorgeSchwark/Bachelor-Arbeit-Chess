#include "make_moves.h"

const signed char NORMAL_MOVE = -1;
const signed char DOUBLE_PAWN = -2;
const signed char CASTLING = -3;
const signed char EN_PASSANT = -4;


void make_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    switch (move_type){
        case -1:
        case -2:
            make_normal_move(board, from_x, from_y, to_x, to_y, move_type);
            break;
        case -3:
            // Behandlung für das Schach-Rochade
            break;
        case -4:
            // Behandlung für das en-passant-Zug
            break;
        default:
            // Behandlung für alle anderen Fälle
            break;

        
    }
}

void make_normal_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    unsigned char piece_number = board->board[from_x, from_y];
    unsigned char pos_in_piece_list = abs(piece_number)-1;

    if (board->pawn[pos_in_piece_list]){
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
    }

    if (board->color_to_move == 1){
        if (board->white_piece_fist_move[pos_in_piece_list] == -1){
            board->white_piece_fist_move[pos_in_piece_list] = board->move_count;
        }
        board->white_piece_pos[pos_in_piece_list<<1] = to_x;
        board->white_piece_pos[pos_in_piece_list<<1 +1] = to_y; 
    }else{
        if (board->black_piece_fist_move[pos_in_piece_list] == -1){
            board->black_piece_fist_move[pos_in_piece_list] = board->move_count;
        }
        board->black_piece_pos[pos_in_piece_list<<1] = to_x;
        board->black_piece_pos[pos_in_piece_list<<1 +1] = to_y; 
    }

    save_in_last_moves(board, from_x, from_y, to_x, to_y, move_type);

    board->board[to_x][to_y] = piece_number;
    board->color_to_move = -board->color_to_move;
    board->move_count += 1;
}

void save_in_last_moves(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type){
    board->past_moves[board->move_count] = from_x;
    board->past_moves[board->move_count+1] = from_y;
    board->past_moves[board->move_count+2] = to_x;
    board->past_moves[board->move_count+3] = to_y;
    board->past_moves[board->move_count+4] = move_type;
}
    