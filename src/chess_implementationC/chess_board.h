// chess_board.h

#ifndef CHESS_BOARD_H
#define CHESS_BOARD_H

#include <stdbool.h>

struct ChessBoard
{   
    unsigned char size;
    bool has_king;
    signed char king_pos;
    short move_count;
    unsigned char fifty_move_rule[500];
    unsigned char non_pawn_pieces[30];
    unsigned char past_moves[2500];
    unsigned char captured_piece[500];
    signed char board[20][20];

    unsigned char white_piece_pos[60];
    bool white_piece_alive[30];
    signed char white_piece_jump_moves[30][30];
    signed char white_piece_move_directions[30][28];
    int white_piece_fist_move[30];

    unsigned char black_piece_pos[30];
    bool black_piece_alive[30];
    signed char black_piece_jump_moves[30][30];
    signed char black_piece_move_directions[30][28];
    int black_piece_fist_move[30];

    unsigned char piece_count;
    bool boarder_x[30];
    bool boarder_y[30];
    bool king[30];
    bool pawn[30];
    bool castling[30];
    char *image[30];
};

void add_piece(struct ChessBoard *board, int *move_directions, int *jump_moves, int *position, bool boarder_x, bool boarder_y, bool pawn, bool king, bool castling, char *image, int offset);
void printChessBoard(struct ChessBoard *board);
void add_king(struct ChessBoard *board);
void add_rooks(struct ChessBoard *board);
void add_pawns(struct ChessBoard *board);
void add_knight(struct ChessBoard* board);
void add_bishop(struct ChessBoard *board);
void add_queen(struct ChessBoard *board);
void setup_normals(struct ChessBoard *board);
void create_chess(struct ChessBoard *board);

#endif /* CHESS_BOARD_H */
