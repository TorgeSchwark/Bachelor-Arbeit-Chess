// https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function
// PeSTO evaluation funktion
/* piece/sq tables */
/* values from Rofchade: http://www.talkchess.com/forum3/viewtopic.php?f=2&t=68311&start=19 */
#include "evaluation.h"

int side2move;
int board[64];

#define SIZE 7
#define FLIP(sq) ((sq)^56)
#define OTHER(side) ((side)^ 1)

int isolated_pawn_reward = 17;
int double_pawn_penalty = -13;
int double_bishop_rewartd = 10;
int double_knight_penalty = -5;
int mg_value[6] = { 82, 337, 365, 477, 1025,  20000};
int eg_value[6] = { 94, 281, 297, 512,  936,  20000};



int mg_pawn_table[64] = {
      0,   0,   0,   0,   0,   0,  0,   0,
     98, 134,  61,  95,  68, 126, 34, -11,
     -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0,
};

int eg_pawn_table[64] = {
      0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0,
};

int mg_knight_table[64] = {
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
};

int eg_knight_table[64] = {
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
};

int mg_bishop_table[64] = {
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
};

int eg_bishop_table[64] = {
    -14, -21, -11,  -8, -7,  -9, -17, -24,
     -8,  -4,   7, -12, -3, -13,  -4, -14,
      2,  -8,   0,  -1, -2,   6,   0,   4,
     -3,   9,  12,   9, 14,  10,   3,   2,
     -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17,
};

int mg_rook_table[64] = {
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
};

int eg_rook_table[64] = {
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
     7,  7,  7,  5,  4,  -3,  -5,  -3,
     4,  3, 13,  1,  2,   1,  -1,   2,
     3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20,
};

int mg_queen_table[64] = {
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
};

int eg_queen_table[64] = {
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41,
};

int mg_king_table[64] = {
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
};

int eg_king_table[64] = {
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
};

int* mg_pesto_table[6] =
{
    mg_pawn_table,
    mg_knight_table,
    mg_bishop_table,
    mg_rook_table,
    mg_queen_table,
    mg_king_table
};

int* eg_pesto_table[6] =
{
    eg_pawn_table,
    eg_knight_table,
    eg_bishop_table,
    eg_rook_table,
    eg_queen_table,
    eg_king_table
};

int gamephaseInc[12] = {0,0,1,1,1,1,2,2,4,4,0,0};
int mg_table[12][64];
int eg_table[12][64];

void init_tables()
{
    int pc, p, sq;
    for (p = PAWN, pc = WHITE_PAWN; p <= KING; pc += 2, p++) {
        for (sq = 0; sq < 64; sq++) {
            mg_table[pc]  [sq] = mg_value[p] + mg_pesto_table[p][sq];
            eg_table[pc]  [sq] = eg_value[p] + eg_pesto_table[p][sq];
            mg_table[pc+1][sq] = mg_value[p] + mg_pesto_table[p][FLIP(sq)];
            eg_table[pc+1][sq] = eg_value[p] + eg_pesto_table[p][FLIP(sq)];
        }
    }
}

/* returns the piece type (number) in the pesto tables since they can be in a abitrary order in the ChessBoard struct */
int piece_white(signed char ind, struct ChessBoard *pos_board){
    if(pos_board->white_pawn[ind]){
        return WHITE_PAWN;
    }else if(pos_board->king[ind]){
        return WHITE_KING;
    }else if(pos_board->castling[ind]){
        return WHITE_ROOK;
    }else if(pos_board->white_piece_jump_moves[ind][0] == 17){
        return WHITE_KNIGHT;
    }else if(pos_board->white_piece_move_directions[ind][0] == 25){
        return WHITE_QUEEN;
    }else{
        return WHITE_BISHOP;
    }
}

/* returns the piece type (number) in the pesto tables since they can be in a abitrary order in the ChessBoard struct */
int piece_black(signed char ind, struct ChessBoard *pos_board){
    if(pos_board->black_pawn[ind]){
        return BLACK_PAWN;
    }else if(pos_board->king[ind]){
        return BLACK_KING;
    }else if(pos_board->castling[ind]){
        return BLACK_ROOK;
    }else if(pos_board->black_piece_jump_moves[ind][0] == 17){
        return BLACK_KNIGHT;
    }else if(pos_board->black_piece_move_directions[ind][0] == 25){
        return BLACK_QUEEN;
    }else{
        return BLACK_BISHOP;
    }
}

/* checking for any repititions is coputationaly expensive therefor this function checks if the last 3 moves where a direct repetition wich is mutch faster */
bool direct_repetition(struct ChessBoard *board){
    if(board->move_count >= 8){
        if(same_move(board, board->move_count-1,  board->move_count-5) && same_move(board, board->move_count-3, board->move_count-7) && same_move(board, board->move_count-2, board->move_count-6) && same_move(board, board->move_count-4, board->move_count-8)){
            return true;
        }
    }
    return false;

}

void quiesce(struct ChessBoard *pos_board, int alpha, int beta, int *score){
    int stand_pat;
    eval(pos_board, &stand_pat);
    if( stand_pat >= beta ){
        *score =  beta;
        return;
    }
    if (alpha < stand_pat){
        alpha = stand_pat;
    }
    signed char moves[2000];
    short move_count;
    find_all_captures(pos_board, moves, &move_count);
    for(int ind = 0; ind < move_count; ind+=5){
        int score_next = 0;
        make_move(pos_board, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
        quiesce(pos_board, -beta, -alpha, &score_next);
        undo_last_move(pos_board);

        if(-score_next >= beta){
            *score =  beta;
            return;
        }
        if(score_next > alpha){
            alpha = score_next;
        }

    }
    *score = alpha;
    
}

/* A PeSTO like evaluation funktion that only uses pieces tables with aditional information about pawn structure and double bishop/knight */
void eval(struct ChessBoard *pos_board, int *score)
{   
    if(direct_repetition(pos_board)){
        *score = 0;
        return;
    }
    int mg[2];
    int eg[2];
    int gamePhase = 0;

    unsigned char white_double_pawns = 0;
    unsigned char black_double_pawns = 0;
    
    unsigned char white_pawns = 0;
    unsigned char black_pawns = 0;
    unsigned char white_isolated = 0;
    int count_white_iso = 0;
    unsigned char black_isolated = 0;
    int count_black_iso = 0;
    
    unsigned char white_bishop = 0;
    unsigned char black_bishop = 0;

    unsigned char white_knight = 0;
    unsigned char black_knight = 0;

    mg[WHITE] = 0;
    mg[BLACK] = 0;
    eg[WHITE] = 0;
    eg[BLACK] = 0;

    /* evaluate each piece */
    for(int ind = 0; ind < pos_board->piece_count; ind++){
        int pc_w = piece_white(ind, pos_board);
        int pc_b = piece_black(ind, pos_board);
        
        if(pos_board->white_piece_alive[ind]){ // ChessBoards are upside down left right swaped and indices between 0 and 63
            mg[WHITE] += mg_table[pc_w][(7-pos_board->white_piece_pos[ind<<1])+((7-pos_board->white_piece_pos[(ind<<1)+1])<<3)];
            eg[WHITE] += mg_table[pc_w][(7-pos_board->white_piece_pos[ind<<1])+((7-pos_board->white_piece_pos[(ind<<1)+1])<<3)];
            gamePhase += gamephaseInc[pc_w];
            if(pos_board->white_pawn[ind]){
                if(white_pawns & (1<<pos_board->white_piece_pos[ind<<1])){
                    white_double_pawns += 1;
                }else{
                    white_pawns += 1<<pos_board->white_piece_pos[ind<<1];
                }
            }else if(pc_w == WHITE_BISHOP){
                white_bishop += 1;
            }else if(pc_w == WHITE_KNIGHT){
                white_knight += 1;
            }
        }
        if(pos_board->black_piece_alive[ind]){
            mg[BLACK] += mg_table[pc_b][(7-pos_board->black_piece_pos[ind<<1])+((7-pos_board->black_piece_pos[(ind<<1)+1])<<3)];
            eg[BLACK] += mg_table[pc_b][(7-pos_board->black_piece_pos[ind<<1])+((7-pos_board->black_piece_pos[(ind<<1)+1])<<3)];
            gamePhase += gamephaseInc[pc_b];
            if(pos_board->black_pawn[ind]){
                if( black_pawns & (1<<pos_board->black_piece_pos[ind<<1])){
                    black_double_pawns += 1;
                }else{
                    black_pawns += 1<<pos_board->black_piece_pos[ind<<1];
                }
            }else if(pc_b == BLACK_BISHOP){
                black_bishop += 1;
            }else if(pc_b == BLACK_KNIGHT){
                black_knight +=  1;
            }
        }
    }
    
    white_isolated = (((white_pawns) & !black_pawns) & !(black_pawns<<1)) & !(black_pawns>>1);
    black_isolated = (((black_pawns) & !white_pawns) & !(white_pawns<<1)) & !(white_pawns>>1);
    while (white_isolated) {
        white_isolated &= (white_isolated - 1);
        count_white_iso++;
    }
    while (black_isolated){
        black_isolated &= (black_isolated -1);
        count_black_iso++;
    }
    
    if(pos_board->color_to_move == 1){
        side2move = WHITE;
    }else{
        side2move = BLACK;
    }
    int bonus = (((white_bishop == 2) - (black_bishop==2)) * double_bishop_rewartd) + (((white_knight == 2) - (black_knight==2)) * double_knight_penalty) + ((count_white_iso-count_black_iso) * isolated_pawn_reward) + ((white_double_pawns-black_double_pawns)*double_pawn_penalty);
    bonus *= pos_board->color_to_move;
    int mgScore = mg[side2move] - mg[OTHER(side2move)];
    int egScore = eg[side2move] - eg[OTHER(side2move)];
    int mgPhase = gamePhase;
    if (mgPhase > 24){
        mgPhase = 24;
    } 
    int egPhase = 24 - mgPhase;
    srand((unsigned int)clock()); 
    int random_number = rand() % RANDOMNESS;
    int random_sin = rand()%2;
    if( random_sin){
        random_number = -random_number;
    }
    *score = ((mgScore * mgPhase + egScore * egPhase) / 24) + bonus+ random_number;
}


void eval_without_extra(struct ChessBoard *pos_board, int *score)
{   
    if(direct_repetition(pos_board)){
        *score = 0;
        return;
    }
    int mg[2];
    int eg[2];
    int gamePhase = 0;

    mg[WHITE] = 0;
    mg[BLACK] = 0;
    eg[WHITE] = 0;
    eg[BLACK] = 0;

    /* evaluate each piece */
    for(int ind = 0; ind < pos_board->piece_count; ind++){
        int pc_w = piece_white(ind, pos_board);
        int pc_b = piece_black(ind, pos_board);
        
        if(pos_board->white_piece_alive[ind]){ // ChessBoards are upside down left right swaped and indices between 0 and 63
            mg[WHITE] += mg_table[pc_w][(7-pos_board->white_piece_pos[ind<<1])+((7-pos_board->white_piece_pos[(ind<<1)+1])<<3)];
            eg[WHITE] += mg_table[pc_w][(7-pos_board->white_piece_pos[ind<<1])+((7-pos_board->white_piece_pos[(ind<<1)+1])<<3)];
            gamePhase += gamephaseInc[pc_w];
        }
        if(pos_board->black_piece_alive[ind]){
            mg[BLACK] += mg_table[pc_b][(7-pos_board->black_piece_pos[ind<<1])+((7-pos_board->black_piece_pos[(ind<<1)+1])<<3)];
            eg[BLACK] += mg_table[pc_b][(7-pos_board->black_piece_pos[ind<<1])+((7-pos_board->black_piece_pos[(ind<<1)+1])<<3)];
            gamePhase += gamephaseInc[pc_b];
        }
        
    }
    
    if(pos_board->color_to_move == 1){
        side2move = WHITE;
    }else{
        side2move = BLACK;
    }
    
    int mgScore = mg[side2move] - mg[OTHER(side2move)];
    int egScore = eg[side2move] - eg[OTHER(side2move)];
    int mgPhase = gamePhase;
    if (mgPhase > 24){
        mgPhase = 24;
    } 
    int egPhase = 24 - mgPhase;
    srand((unsigned int)clock()); 
    int random_number = rand() % RANDOMNESS;
    int random_sin = rand()%2;
    if( random_sin){
        random_number = -random_number;
    }
    *score = ((mgScore * mgPhase + egScore * egPhase) / 24) + random_number;
}