#ifndef NNUE_EVAL_H
#define NNUE_EVAL_H

#include "./nnue/nnue.h"

int evaluate_fen_nnue(char *fen);
void init_nnue(char *filename);
int evaluate_nnue(int player, int *pieces, int* squares);

#endif
