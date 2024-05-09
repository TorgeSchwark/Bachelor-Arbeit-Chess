#ifndef MAKE_MOVES_H
#define MAKE_MOVES_H

#include "chess_board.h"
#include "find_moves.h"

/* executes a move therefore calls the make move function wich is responsible for it*/
void make_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* executes a normal move updating every thing in the ChessBoard needed */
void make_normal_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* saves the last move in the last_moves list */
void save_in_last_moves(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* executes an en passant move */
void make_en_passant(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* Executes a castling move */
void make_castling_move(struct ChessBoard* board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* executes a promotion. Careful: pawns wont be able to walk over edges even after proming to a piece that can. The undo promotion makes the pawn to a normal Chess pawn !*/
void make_promotion(struct ChessBoard* board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* undoes the last move therefor calls the last funktion responsible for it */
void undo_last_move(struct ChessBoard *board);

/* undoes normal moves */
void undo_normal_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* undoes en passant moves*/
void undo_en_passant(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* undoes a promotion. Undoing a promotion the piece is turned into a NORMAL chess pawn */
void undo_castling_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

/* saves the last move in the last_moves list */
void undo_promotion(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

#endif