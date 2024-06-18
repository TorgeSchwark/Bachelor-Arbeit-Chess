#include "features.h"

// gcc -o chess_program features.c chess_board.c


#define NUM_SQ 64
#define NUM_SQ_X 8
#define NUM_SQ_Y 8
#define NUM_PT 12
#define NUM_PLANES (NUM_SQ * NUM_PT + 1)

// Function to orient the square based on perspective
int orient(bool is_white_pov, int sq) {
    return (56 * (!is_white_pov)) ^ sq;
}

// Example implementation of get_piece_type
int get_piece_type_KA(int piece, struct ChessBoard *board) {
    // Convert your piece representation to piece type
    // Example: assuming piece is 0 for empty, 1-6 for white pieces, 7-12 for black pieces
    int color = 0;
    int piece_ind = piece-1;
    if(piece > 0){
        color = 1;
    }else{
        piece_ind = (-piece)-1;
    }
    if (piece == 0) return 0;

    if(color == 1){
        if(board->white_pawn[piece_ind]){
            piece_ind = 1;
        }else if(board->white_piece_jump_moves[piece_ind][0] == 17 && board->king[piece_ind] == false){
            piece_ind = 2;
        }else if(board->white_piece_jump_moves[piece_ind][0] == 17){
            piece_ind = 6;
        }else if(board->white_piece_move_directions[piece_ind][0]  == 25 ){
            piece_ind = 5;
        }else if(board->white_piece_move_directions[piece_ind][0] == 13 && (abs(board->white_piece_move_directions[piece_ind][1]) == abs(board->white_piece_move_directions[piece_ind][2]))){
            piece_ind = 3;
        }else{
            piece_ind = 4;
        }
    }else{
        if(board->black_pawn[piece_ind]){
            piece_ind = 1;
        }else if(board->black_piece_jump_moves[piece_ind][0] == 17 && board->king[piece_ind] == false){
            piece_ind = 2;
        }else if(board->black_piece_jump_moves[piece_ind][0] == 17){
            piece_ind = 6;
        }else if(board->black_piece_move_directions[piece_ind][0]  == 25){
            piece_ind = 5;
        }else if(board->black_piece_move_directions[piece_ind][0] == 13 && (abs(board->black_piece_move_directions[piece_ind][1]) == abs(board->black_piece_move_directions[piece_ind][2]))) {
            piece_ind = 3;
        }else{
            piece_ind = 4;
        }
    }
    return piece_ind;
}

// Function to calculate halfka index
int halfka_idx(bool is_white_pov, int king_sq, int sq, int piece_type) {
    int p_idx = (piece_type - 1) * 2 + (!is_white_pov);
    return 1 + orient(is_white_pov, sq) + p_idx * NUM_SQ + king_sq * NUM_PLANES;
}

int real_square(int x, int y){
    return (7-x)+y*8;
}
// Function to get active features
void get_active_features(struct ChessBoard *board, bool turn, float features[NUM_PLANES * NUM_SQ]) {
    int king_sq = -1;

    // Find the king square
    for (int sq_x = 0; sq_x < NUM_SQ_X; sq_x++) {
        for(int sq_y = 0; sq_y < NUM_SQ_Y; sq_y++){
            if (get_piece_type_KA(board->board[sq_x][sq_y], board) == 6 && ((turn && (board->board[sq_x][sq_y] < 0)) || (!turn && !(board->board[sq_x][sq_y] < 0)))) {
                king_sq = real_square(sq_x, sq_y);
                break;
            }
        }
    }

    printf("kings: %d", king_sq);

    if (king_sq == -1) {
        printf("Error: King not found on the board.\n");
        return;
    }

    // Initialize features to 0
    for (int i = 0; i < NUM_PLANES * NUM_SQ; i++) {
        features[i] = 0.0;
    }

    // Set active features
    for (int sq_x = 0; sq_x < NUM_SQ_X; sq_x++) {
        for (int sq_y = 0; sq_y < NUM_SQ_X; sq_y++) {
            int piece_type = get_piece_type_KA(board->board[sq_x][sq_y], board);
            if (piece_type != 0) { // If there is a piece on the square
                int idx = halfka_idx(turn, orient(turn, king_sq), real_square(sq_x, sq_y), piece_type);
                features[idx] = 1.0;
            }
        }
    }
}

void test_start(float* features_white, float* features_black) {
    // Example usage/ Initialize your board state here
  
    struct ChessBoard board;
    setup_normals(&board);
    create_chess(&board);

    // Initialize features to 0
    for (int i = 0; i < NUM_PLANES * NUM_SQ; i++) {
        features_white[i] = 0.0;
        features_black[i] = 0.0;
    }

    // Set active features for white pieces
    get_active_features(&board, false, features_white);

    // Set active features for black pieces
    get_active_features(&board, true, features_black);
}
