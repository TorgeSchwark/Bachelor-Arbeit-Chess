#ifndef TEST_ENGIN_H
#define TEST_ENGIN_H


#include <stdio.h>
#include "chess_board.h"
#include "find_moves.h"
#include "make_moves.h"

/* checks if the kings are alive*/
int quick_over(struct ChessBoard *board);

/* undoes a whole game*/
void undo_game(struct ChessBoard *board);

/* returns if the player to move is checkmate 0 if its no checkmate 0.5 if its a patt or remie and 1 if the game is over */
void is_check_mate(struct ChessBoard *board, float *matt);

/* checks for threefold repetition therefor only checks if the current position occured the third time*/
bool three_fold_repetition(struct ChessBoard *board);

/* copies only the board it self and the past_moves from the chess board into current_board and *all_moves */
void copy_moves_and_board(struct ChessBoard *board, signed char current_board[20][20], signed char *all_moves);

/* checks if two moves in the past_moves list where the same */
bool same_move(struct ChessBoard *board, int ind, int ind_past);

/* counts the amount of legal moves for every move upto a certain depth */
void count_for_each_move(struct ChessBoard *board, int depth, long long *counts);

/* checks if a move is completly legal */
bool all_legal(struct ChessBoard *board, signed char *moves, short *move_count);

/* checks if any move is a king capture */
bool is_legal(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* plays the game specified in move_pos then counts the folow moves for every move in that position (used for PERFT debugging) */
void test_engine(struct ChessBoard *board, int depth); 

/* counts the moves upto a certain depth */
void test_engine_all_moves(struct ChessBoard *board, int depth, long long *count);

/* searches for real legal moves for every move that is legal the legal array contains a true otherwise a false */
void legal_moves(struct ChessBoard *board, short move_count, char *moves, bool *legal);

#endif
