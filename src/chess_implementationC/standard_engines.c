#include "standard_engines.h"

void neg_max(struct ChessBoard *board, int depth, int original_depth, int *score){

    if(depth == 0){
        eval(board, score);
        return;
    }
    int max = -999999;
    signed char moves[2000];
    short move_count = 0;
    int best_move = 0;
    int score_next = 0;
    find_all_moves(board, moves, &move_count);
    for(int ind = 0; ind < move_count; ind += 5){
        make_move(board, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
        neg_max(board, depth-1, original_depth, &score_next);
        undo_last_move(board);
        if (-score_next > max){
            best_move = ind;
            max = -score_next;
        }
    }
    if (depth != original_depth){
        *score = max;
    }else{
        printf("score: %d ", max);
        *score = best_move;
    }
}

void alpha_beta_basic(struct ChessBoard *board, int depth,int original_depth, int alpha, int beta, int *score, unsigned char *moves_with_score){
    // printf("222");
    if(depth == 0){
        return eval(board, score);
    }
    
    int maxWert = alpha;
    signed char moves[2000];
    signed char moves_with_score_next_depth[2000];
    short move_count = 0;
    int best_move = 0;
    int score_next = 0;
    bool legal[200];
    int sorted_ind[200];
    find_all_moves(board, moves, &move_count);
    if(depth == original_depth){
        legal_moves(board, move_count, moves, legal);
    }
    for(int ind = 0; ind < move_count; ind += 5){
        if(depth == original_depth && !legal[ind/5]){
            // save_move_with_score(moves, ind, moves_with_score, -99999);
            continue;
        }
        make_move(board, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
        alpha_beta_basic(board, depth-1, original_depth, -beta, -maxWert, &score_next, moves_with_score_next_depth);
        undo_last_move(board);
        // if(depth == original_depth){
        //     save_move_with_score(moves, ind, moves_with_score, -score_next);
        // }
        if(-score_next > maxWert){
            maxWert = -score_next;
            best_move = ind;
            if (maxWert >= beta){
                break;
            }
        }
    }
    if (depth != original_depth){
        *score = maxWert;
    }else{
        *score = best_move;
    }
}

void save_move_with_score(signed char *moves, int ind, signed char *moves_with_score, int score){
    int ind_mws = ind/5*6;
    moves_with_score[ind_mws] = moves[ind];
    moves_with_score[ind_mws+1] = moves[ind+1];
    moves_with_score[ind_mws+2] = moves[ind+2];
    moves_with_score[ind_mws+3] = moves[ind+3];
    moves_with_score[ind_mws+4] = moves[ind+4];
    moves_with_score[ind_mws+5] = score;
}
