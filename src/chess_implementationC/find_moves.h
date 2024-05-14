#ifndef FIND_MOVES_H
#define FIND_MOVES_H

#include "chess_board.h"
/* this code is well tested for NORMAL chess rules via PERFT debugging */

#define NORMAL_MOVE -1
#define DOUBLE_PAWN -2
#define CASTLING -3
#define EN_PASSANT -4
/* function that finds all moves in the current position. generates illegal moves: king can be captured/exposed. castling when squares are under atack but not if quare is not free*/
void find_all_moves(struct ChessBoard *board, signed char *moves, short *moves_count);

/* adds all jump moves from for one piece */
void find_jump_moves(struct ChessBoard *board,unsigned char* color_pos, signed char* piece_jump_moves, signed char *moves, short *moves_count, unsigned char piece_ind);

/* finds the moves for all pieces that can move in a direction also resticted range */
void find_move_directions(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_move_directions, signed char *moves, short *move_counts, unsigned char piece_ind);

/* adds a move to the move stack and increases the move_count */
void add_move(signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type, signed char* moves, short *moves_count);

/* checks if a position is on the board */
bool on_board(signed char x, unsigned char size);

/* checks if a move goes to the last rank of the correct side*/
bool promotion(signed char y, signed char color, unsigned char size);

/* adds all pawn moves also en passant promotion and double moves. promoting a pawn dosnt gain the right to move over edges! */
void find_pawn_moves(struct ChessBoard *board, unsigned char *color_pos, signed char *piece_move_directions,short *color_first_moves, signed char *moves, short *moves_count, unsigned char piece_ind);

/* adds a en_passant move if it is allowed */
void add_en_passant(struct ChessBoard *board, unsigned char *color_pos,unsigned char piece_ind, signed char *moves, short *moves_count);

void add_promotion(signed char from_x, signed char from_y, signed char to_x, signed char to_y, unsigned char *non_pawn_pieces, signed char* moves, short *move_count);

/* adds the castling if both the rook and the king didnt move this far and no piece stands in between*/
void add_castling(struct ChessBoard *board, unsigned char *color_pos, short *color_first_move, unsigned char piece_ind, bool *color_alive, signed char *moves, short* moves_count);

/* finds the move in the move stack and returns the index of it */
void real_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, char *piece, signed char* moves, short moves_count, int *ind);

#endif /* FIND_MOVES_H */
