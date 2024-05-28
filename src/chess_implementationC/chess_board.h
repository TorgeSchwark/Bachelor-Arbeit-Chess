#ifndef CHESS_BOARD_H
#define CHESS_BOARD_H

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_MOVES 10000
#define MAX_PIECES 32
#define MAX_MOVE_DIRECTIONS 32
#define MAX_JUMP_MOVES 32
#define MAX_FIFTY_MOVE_RULE 2048
#define BOARD_SIZE 20


/* Definition of the Chessboard Struct containig all piece information and all metadata*/
struct ChessBoard
{
    /* meta data */
    signed char color_to_move;
    unsigned char size;
    bool has_king;
    signed char king_pos;
    short move_count;
    unsigned char fifty_move_rule[MAX_FIFTY_MOVE_RULE];
    unsigned char non_pawn_pieces[MAX_PIECES];
    signed char past_moves[MAX_MOVES];
    signed char captured_piece[MAX_FIFTY_MOVE_RULE];
    signed char board[BOARD_SIZE][BOARD_SIZE];

    /* white piece information*/
    unsigned char white_piece_pos[2 * MAX_PIECES];
    bool white_piece_alive[MAX_PIECES];
    signed char white_piece_jump_moves[MAX_PIECES][MAX_JUMP_MOVES*2];
    signed char white_piece_move_directions[MAX_PIECES][MAX_MOVE_DIRECTIONS];
    short white_piece_first_move[MAX_PIECES];
    unsigned char white_piece_img[MAX_PIECES];
    bool white_pawn[MAX_PIECES];

    /*black piece information*/
    unsigned char black_piece_pos[2 * MAX_PIECES];
    bool black_piece_alive[MAX_PIECES];
    signed char black_piece_jump_moves[MAX_PIECES][MAX_JUMP_MOVES *2];
    signed char black_piece_move_directions[MAX_PIECES][MAX_MOVE_DIRECTIONS];
    short black_piece_first_move[MAX_PIECES];
    unsigned char black_piece_img[MAX_PIECES];
    bool black_pawn[MAX_PIECES];

    /*general piece information this cant change with a promotions !!*/
    unsigned char piece_count;
    bool boarder_x[MAX_PIECES];
    bool boarder_y[MAX_PIECES];
    bool king[MAX_PIECES];
    bool castling[MAX_PIECES];
};

void board_to_halfkp(struct ChessBoard *board, bool* input);

void board_to_simple(struct ChessBoard *board, bool* input);

int piece_type_half_kp(struct ChessBoard *board,signed char *piece_ind);

void set_size(struct ChessBoard *board, int size);

void add_piece(struct ChessBoard *board, int *move_directions, int *jump_moves, int *position, bool boarder_x, bool boarder_y, bool pawn, bool king, bool castling, int offset,unsigned char img);
void add_king(struct ChessBoard *board);
void add_rooks(struct ChessBoard *board);
void add_pawns(struct ChessBoard *board);
void add_knight(struct ChessBoard *board);
void add_bishop(struct ChessBoard *board);
void add_queen(struct ChessBoard *board);

void get_piece_type_for_db(struct ChessBoard *board,int *piece_ind, signed char color);

void board_to_fen(struct ChessBoard *board, char *fen);

void setup_normals(struct ChessBoard *board);

void create_chess(struct ChessBoard *board);

void printChessBoard(struct ChessBoard *board);

void copyBoard(struct ChessBoard *board, struct ChessBoard *copies);

#endif // CHESS_BOARD_H
