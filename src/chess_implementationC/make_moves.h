#ifndef MAKE_MOVES_H
#define MAKE_MOVES_H

#include "chess_board.h"
#include "find_moves.h"

void make_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void make_normal_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void save_in_last_moves(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void make_en_passant(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void make_castling_move(struct ChessBoard* board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void make_promotion(struct ChessBoard* board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void undo_last_move(struct ChessBoard *board);

void undo_normal_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void undo_en_passant(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void undo_castling_move(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

void undo_promotion(struct ChessBoard *board, signed char from_x, signed char from_y, signed char to_x, signed char to_y, signed char move_type);

#endif