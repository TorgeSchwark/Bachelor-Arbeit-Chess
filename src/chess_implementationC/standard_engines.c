#include "standard_engines.h"

/* this is a standard implementation of the negmax algorithm */
void neg_max(struct ChessBoard *board, int depth, int original_depth, int *score, int* count ){
    *count += 1;
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
        neg_max(board, depth-1, original_depth, &score_next, count);
        undo_last_move(board);
        if (-score_next > max){
            best_move = ind;
            max = -score_next;
        }
    }
    if (depth != original_depth){
        *score = max;
    }else{
        *score = best_move;
    }
}

/* basic alpha beta implementation gives back the index of the best move in highest depth otherwise the best score */
void alpha_beta_basic(struct ChessBoard *board, int depth, int original_depth, int alpha, int beta, int *score, int *count){
    *count += 1;
    if(depth == 0){
        return eval(board, score);
    }
    
    int maxWert = alpha;
    signed char moves[2000];
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
            continue;
        }
        make_move(board, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
        alpha_beta_basic(board, depth-1, original_depth, -beta, -maxWert, &score_next, count);
        undo_last_move(board);
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

/* this is a optimisation of the alpha beta algorithm wich sorts the moves by the evaluation before executing them wich gains speed due to more cutoffs*/
void advanced_apha_beta_engine(struct ChessBoard *board, int depth,int original_depth, int alpha, int beta, int *score, int *count){
    *count += 1;
    if(depth == 0){
        return eval(board, score);
    }
    int maxWert = alpha;
    signed char moves[2000];
    short move_count = 0;
    int best_move = 0;
    int score_next = 0;
    bool legal[200];
    int sorted_ind[200];
    int ind = 0;
    find_all_moves(board, moves, &move_count);

    // if(depth >= original_depth-1){
    //     sort_moves(board, moves, move_count, sorted_ind, true, count);
    // }
    // else 
    if(depth >= original_depth-2){
        sort_moves(board, moves, move_count, sorted_ind, false, count);
    }
    if(depth == original_depth){
        legal_moves(board, move_count, moves, legal);
    }
    for(int i = 0; i < move_count/5; i++){
        if(depth == original_depth && !legal[sorted_ind[i]]){
            continue;
        }
        if(depth >= original_depth-2){
            ind = sorted_ind[i]*5;
        }else{
            ind = i*5;
        }
        make_move(board, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
        advanced_apha_beta_engine(board, depth-1, original_depth, -beta, -maxWert, &score_next, count);
        undo_last_move(board);
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

/* puts the index of the moves sorted by the evaluation of the move in the sorted_ind array */
void sort_moves(struct ChessBoard *board, char *moves, short move_count, int *sorted_ind, bool acurate, int *count){
    int evals[200];
    if(!acurate){
        for(int ind = 0; ind < move_count; ind+= 5){
            int score = 0;
            make_move(board,  moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
            eval(board, &score);
            evals[ind/5] = -score;
            undo_last_move(board);
        }
    }
    else{
        for(int ind = 0; ind < move_count; ind+= 5){
            int score = 0;
            make_move(board,  moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
            advanced_apha_beta_engine(board, 2, 20, -999999, 999999, &score, count);
            evals[ind/5] = -score;
            undo_last_move(board);
        }
    }

    for (int i = 0; i <  move_count/5; i++) {
        sorted_ind[i] = i;
    }

    for(int i = 0; i < move_count/5; i++){
        int min_idx = i;
        for(int j = i+1; j < move_count/5; j++){
            if (evals[sorted_ind[j]] > evals[sorted_ind[min_idx]]){
                min_idx = j;
            }
        }
        int temp = sorted_ind[min_idx];
        sorted_ind[min_idx] = sorted_ind[i];
        sorted_ind[i] = temp;
    }
}

void alpha_beta_basic_other_eval(struct ChessBoard *board, int depth, int original_depth, int alpha, int beta, int *score){
    if(depth == 0){
        return eval_without_extra(board, score);
    }
    
    int maxWert = alpha;
    signed char moves[2000];
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
            continue;
        }
        
        make_move(board, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
        alpha_beta_basic_other_eval(board, depth-1, original_depth, -beta, -maxWert, &score_next);
        undo_last_move(board);
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

// alpha beta with sort and quiesce 
void alpha_beta_basic_NN(struct ChessBoard *board, int depth, int original_depth, int alpha, int beta, int *score, int *count){
    *count += 1;
    if(depth == 0){
        return quiesce(board, alpha, beta, score, count);
    }
    
    int maxWert = alpha;
    signed char moves[2000];
    short move_count = 0;
    int best_move = 0;
    int score_next = 0;
    bool legal[200];
    int ind = 0;
    int sorted_ind[200];
    find_all_moves(board, moves, &move_count);
    if(depth >= original_depth-4){
        sort_moves(board, moves, move_count, sorted_ind, false, count);
    }
    if(depth == original_depth){
        legal_moves(board, move_count, moves, legal);
    }
    for(int i = 0; i < move_count/5; i++){
        if(depth == original_depth && !legal[sorted_ind[i]]){
            continue;
        }
        if(depth >= original_depth-4){
            ind = sorted_ind[i]*5;
        }else{
            ind = i*5;
        }
        make_move(board, moves[ind], moves[ind+1], moves[ind+2], moves[ind+3], moves[ind+4]);
        alpha_beta_basic_NN(board, depth-1, original_depth, -beta, -maxWert, &score_next, count);
        undo_last_move(board);
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

