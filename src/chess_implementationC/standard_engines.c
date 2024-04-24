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

void alpha_beta_basic(struct ChessBoard *board, int depth, int original_depth, int alpha, int beta, int *score){
    // printf("222");
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
        alpha_beta_basic(board, depth-1, original_depth, -beta, -maxWert, &score_next);
        undo_last_move(board);
        if(-score_next > maxWert){
            maxWert = -score_next;
            best_move = ind;
            if (maxWert >= beta){
                break;
            }
        }
    }
    // if (depth != original_depth){
    *score = maxWert;
    // }
    // coment in for use just for db ...
    // }else{
    //     *score = best_move;
    // }
}




void advanced_apha_beta_engine(struct ChessBoard *board, int depth,int original_depth, int alpha, int beta, int *score){

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

    if(depth >= original_depth-2){
        sort_moves(board, moves, move_count, sorted_ind, true);
    }
    else if(depth >= original_depth-4){
        sort_moves(board, moves, move_count, sorted_ind, false);
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
        advanced_apha_beta_engine(board, depth-1, original_depth, -beta, -maxWert, &score_next);
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

void sort_moves(struct ChessBoard *board, char *moves, short move_count, int *sorted_ind, bool acurate){
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
            advanced_apha_beta_engine(board, 2, 20, -999999, 999999, &score);
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

void new_alphaBeta(struct ChessBoard *board, int depth, int original_depth, int alpha, int beta, int *score){

    int bestscore = -999999;
    if(depth == 0){
        return eval(board, score);
    } 
    signed char moves[2000];
    short move_count = 0;
    bool legal[200];
    int best_move = 0;
    find_all_moves(board, moves, &move_count);
    if(depth == original_depth){
        legal_moves(board, move_count, moves, legal);
    }
    int next_eval = 0;
    for(int i = 0; i < move_count; i+=5){
        if(depth == original_depth && !legal[i/5]){
            continue;
        }
        make_move(board, moves[i], moves[i+1], moves[i+2], moves[i+3], moves[i+4]);
        new_alphaBeta(board, depth-1, original_depth, -beta, -alpha, &next_eval);
        undo_last_move(board);
        if(-next_eval >= beta){
            bestscore = -next_eval;
            *score = -next_eval;
            break;
        }
        if(-next_eval  > bestscore){
            bestscore = -next_eval;
            best_move = i;
            if(bestscore > alpha){
                alpha = bestscore;
            }
        }
    }
    if (depth != original_depth){
        *score = bestscore;
    }else{
        *score = best_move;
    }


}