
#include "chess_board.h"

// pawns can only walk like normal pawns!


// [-9999] [-1, -1, -1, 1, -1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1] [5, 4, 10, 4] False False False False False Knight.png 4
void add_piece(struct ChessBoard *board, int *move_directions, int *jump_moves, int *position, bool boarder_x, bool boarder_y, bool pawn, bool king, bool castling, int offset,unsigned char img){
    int len_start_pos = position[0]; 
    if ((king && board->has_king) || king && len_start_pos > 3){
        printf("game already has a king and can only have one king");
    }else if(castling && !(board->has_king || king)){
        printf("add king before adding a castling piece");
    }else{
        if(castling && !king){
            for(int ind = 1; ind < len_start_pos; ind+=2){
                if(position[ind+1]-offset != board->white_piece_pos[board->king_pos*2+1] || abs(position[ind]-offset -board->white_piece_pos[board->king_pos*2]) < 2){
                    printf("castling pieces must be in the same row as the king ");
                    return;
                }
            }
        }

        bool new_piece = true;

        for( int ind = 1; ind < len_start_pos; ind+=2){
            int x = position[ind] - offset;
            int y = position[ind+1] - offset;

            if(y > board->size/2){
                printf("White piece must be on the lower half :%d, %d )", x, y);
            }
            
            // add the white piece information
            board->white_piece_pos[board->piece_count*2] = x;
            board->white_piece_pos[board->piece_count*2+1] = y;
            printf("%d", (sizeof(jump_moves) / sizeof(jump_moves[0])));
            if (jump_moves[0] != -9999){
                for (int ind_jm = 1; ind_jm < jump_moves[0]; ind_jm+=2){
                    board->white_piece_jump_moves[board->piece_count][ind_jm] = jump_moves[ind_jm];
                    board->white_piece_jump_moves[board->piece_count][ind_jm+1] = jump_moves[ind_jm+1];
                    board->white_piece_jump_moves[board->piece_count][0] = ind_jm+2;
                }
            }

            if (move_directions[0] != -9999){
                for (int ind_md = 1; ind_md < move_directions[0]; ind_md+=3){
                    board->white_piece_move_directions[board->piece_count][ind_md] = move_directions[ind_md];
                    board->white_piece_move_directions[board->piece_count][ind_md+1] = move_directions[ind_md+1];
                    board->white_piece_move_directions[board->piece_count][ind_md+2] = move_directions[ind_md+2];
                    board->white_piece_move_directions[board->piece_count][0] = ind_md+3;
                }
            }
            board->white_piece_alive[board->piece_count] = true;
            board->white_piece_fist_move[board->piece_count] = -1;
            
            board->board[x][y] = board->piece_count+1; 
            board->white_piece_img[board->piece_count] = img;
            board->white_pawn[board->piece_count] = pawn;

            
            // add the neutral information

            board->boarder_x[board->piece_count] = boarder_x;
            board->boarder_y[board->piece_count] = boarder_y;
            board->king[board->piece_count] = king;
            board->castling[board->piece_count] = castling;

            // add the black piece information
            board->black_piece_pos[board->piece_count*2] = x;
            board->black_piece_pos[board->piece_count*2+1] = board->size-1-y;
            if (jump_moves[0] != -9999){
                for (int ind_jm = 1; ind_jm < jump_moves[0]; ind_jm+=2){
                    board->black_piece_jump_moves[board->piece_count][ind_jm] = -jump_moves[ind_jm];
                    board->black_piece_jump_moves[board->piece_count][ind_jm+1] = -jump_moves[ind_jm+1];
                    board->black_piece_jump_moves[board->piece_count][0] = ind_jm+2;
                }
            }

            if (move_directions[0] != -9999){
                for (int ind_md = 1; ind_md < move_directions[0]; ind_md+=3){
                    board->black_piece_move_directions[board->piece_count][ind_md] = -move_directions[ind_md];
                    board->black_piece_move_directions[board->piece_count][ind_md+1] = -move_directions[ind_md+1];
                    board->black_piece_move_directions[board->piece_count][ind_md+2] = move_directions[ind_md+2];
                    board->black_piece_move_directions[board->piece_count][0] = ind_md+3;
                }
            }

            board->black_piece_alive[board->piece_count] = true;
            board->black_piece_fist_move[board->piece_count] = -1;
            board->black_pawn[board->piece_count] = pawn;
            board->black_piece_img[board->piece_count] = img;

            board->board[x][board->size-1-y] = -(board->piece_count+1);
            
            // other data
            if (king){
                board->king_pos = board->piece_count;
                board->has_king = true;
            }
            if (new_piece && !(king || pawn)){
                new_piece = false;
                board->non_pawn_pieces[board->non_pawn_pieces[0]] = board->piece_count;
                board->non_pawn_pieces[0] += 1; 
            }else if (new_piece && pawn){
                new_piece = false;
            }

            board->piece_count += 1;
        }
    }

}

// Funktion zum Drucken eines ChessBoard-Objekts
void printChessBoard(struct ChessBoard *board) {
    printf("size: %u\n", board->size);
    printf("has_king: %s\n", board->has_king ? "true" : "false");
    printf("king_pos: %d\n", board->king_pos);
    printf("move_count: %hd\n", board->move_count);
    
    printf("fifty_move_rule:\n");
    for (int i = 0; i < board->move_count; i++) {
        printf("%u ", board->fifty_move_rule[i]);
    }
    printf("\nnon_pawn_pieces:\n");
    for (int i = 1; i < board->non_pawn_pieces[0]; i++) {
        printf("%u ", board->non_pawn_pieces[i]);
    }
    printf("\npast_moves:\n");
    for (int i = 0; i < board->move_count*5; i+=5) {
        printf("( %d , %d ) -> ( %d , %d ) %d ", board->past_moves[i],board->past_moves[i+1],board->past_moves[i+2], board->past_moves[i+3], board->past_moves[i+4]);
    }
    printf("\ncaptured_piece:\n");
    for (int i = 0; i < board->move_count; i++) {
        printf("%u ", board->captured_piece[i]);
    }
    printf("\nboard:\n");
    for (int i = 0; i < board->size; i++) {
        for(int j = 0; j < board->size; j++){
            printf("%d ", board->board[i][j]);
        }
        printf("\n");
    }
    
    printf("\nwhite_piece_pos:\n");
    for (int i = 0; i < board->piece_count*2; i++) {
        printf("%u ", board->white_piece_pos[i]);
    }
    printf("\nwhite_piece_alive:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%u ", board->white_piece_alive[i]);
    }
    printf("\nwhite_piece_jump_moves:\n");
    for (int i = 0; i < 30; i++) {
        for (int j = 0; j < board->white_piece_jump_moves[i][0]; j++) {
            printf("%d ", board->white_piece_jump_moves[i][j]);
        }
        printf("\n");
    }
    printf("\nwhite_piece_move_directions:\n");
    for (int i = 0; i < 30; i++) {
        for (int j = 0; j < board->white_piece_move_directions[i][0]; j++) {
            printf("%d ", board->white_piece_move_directions[i][j]);
        }
        printf("\n");
    }
    printf("\nwhite_piece_fist_move:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%d ", board->white_piece_fist_move[i]);
    }
    
    printf("\nblack_piece_pos:\n");
    for (int i = 0; i < board->piece_count*2; i++) {
        printf("%u ", board->black_piece_pos[i]);
    }
    printf("\nblack_piece_alive:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%u ", board->black_piece_alive[i]);
    }
    printf("\nblack_piece_jump_moves:\n");
    for (int i = 0; i < 30; i++) {
        for (int j = 0; j < board->black_piece_jump_moves[i][0]; j++) {
            printf("%d ", board->black_piece_jump_moves[i][j]);
        }
        printf("\n");
    }
    printf("\nblack_piece_move_directions:\n");
    for (int i = 0; i < 30; i++) {
        for (int j = 0; j < board->black_piece_move_directions[i][0]; j++) {
            printf("%d ", board->black_piece_move_directions[i][j]);
        }
        printf("\n");
    }
    printf("\nblack_piece_fist_move:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%d ", board->black_piece_fist_move[i]);
    }
    
    printf("\nboarder_x:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%s ", board->boarder_x[i] ? "true" : "false");
    }
    printf("\nboarder_y:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%s ", board->boarder_y[i] ? "true" : "false");
    }
    printf("\nking:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%s ", board->king[i] ? "true" : "false");
    }
    printf("\nwhite pawns:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%s ", board->white_pawn[i] ? "true" : "false");
    }
    printf("\nblack pawns:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%s ", board->black_pawn[i] ? "true" : "false");
    }
    printf("\ncastling:\n");
    for (int i = 0; i < board->piece_count; i++) {
        printf("%s ", board->castling[i] ? "true" : "false");
    }
    printf("\nwhite piece imges\n");
    for(int i = 0; i < board->piece_count; i++){
        printf("%d\n", board->white_piece_img[i]);
    }
    printf("\nblack piece imges\n");
    for(int i = 0; i < board->piece_count; i++){
        printf("%d\n", board->black_piece_img[i]);
    }
    printf("\n");
}

void add_king(struct ChessBoard *board){
    int move_direction[1] = {-9999};
    int jump_moves[17] = {17,0,1,1,0,1,1,-1,0,-1,-1,-1,1,1,-1,0,-1};
    int position[3] = {3,3,0};
    bool boarder_x = false;
    bool boarder_y = false;
    bool king = true;
    bool pawn = false;
    bool castling = false;
    int offset = 0;
    
    add_piece(board, move_direction, jump_moves, position, boarder_x, boarder_y, pawn, king ,castling, offset, 0);
}

void add_rooks(struct ChessBoard *board){
    int move_direction[13] = {13,0,1,0,0,-1,0,-1,0,0,1,0,0};
    int jump_moves[1] = {-9999};
    int position[5] = {5,0,0,7,0};
    bool boarder_x = false;
    bool boarder_y = false;
    bool king = false;
    bool castling = true;
    bool pawn = false;
    int offset = 0;
    
    add_piece(board, move_direction, jump_moves, position, boarder_x, boarder_y, pawn, king ,castling, offset, 0);
}

void add_pawns(struct ChessBoard *board){
    int move_directions[4] = {4,0,1,1};
    int jump_moves[1] =  {-9999};
    int position[17] = {17,0,1,1,1,2,1,3,1,4,1,5,1,6,1,7,1};
    bool boarder_x = false;
    bool boarder_y = false;
    bool pawn = true;
    bool king = false;
    bool castling = false;
    int offset = 0;

    add_piece(board, move_directions, jump_moves, position, boarder_x, boarder_y, pawn, king, castling, offset, 0);
}

void add_knight(struct ChessBoard* board){
    int move_directions[1] = {-9999};
    int jump_moves[17] = {17, 2,1 ,1,2 ,-1,2, 2,-1, -2,1, 1,-2, -1,-2, -2,-1};
    int position[5] = {5, 1,0, 6,0};
    bool boarder_x = false;
    bool boarder_y = false;
    bool king = false;
    bool pawn = false;
    bool castling = false;
    int offset = 0;

    add_piece(board, move_directions, jump_moves, position, boarder_x, boarder_y, pawn, king, castling, offset, 0);
} 

void add_bishop(struct ChessBoard *board){
    int move_directions[13] = {13, 1,1,0, 1,-1,0, -1,1,0 ,-1,-1,0};
    int jump_moves[1] = {-9999};
    int position[5] = {5, 2,0 ,5,0};
    bool boarder_x = false;
    bool boarder_y = false;
    bool king = false;
    bool pawn = false;
    bool castling = false;
    int offset = 0;

    add_piece(board, move_directions, jump_moves, position, boarder_x, boarder_y, pawn, king, castling, offset, 0);
}

void add_queen(struct ChessBoard *board){
    int move_directions[25] = {25, 0,1,0 ,1,0,0, 1,1,0, -1,0,0, -1,-1,0, -1,1,0, 1,-1,0, 0,-1,0};
    int jump_moves[1] = {-9999};
    int position[3] = {3,4,0};
    bool boarder_x = false;
    bool boarder_y = false;
    bool king = false;
    bool pawn = false;
    bool castling = false;
    int offset = 0;

    add_piece(board, move_directions, jump_moves, position, boarder_x, boarder_y, pawn, king, castling, offset, 0);
}

void setup_normals(struct ChessBoard *board){
    board->color_to_move = 1;
    board->size = 0;
    board->has_king = false;
    board->king_pos = -1;
    board->move_count = 0;
    board->non_pawn_pieces[0] = 1;
    board->has_king = false;
    for(int i = 0; i < 30; i++){
        board->white_piece_jump_moves[i][0] = 0;
        board->black_piece_jump_moves[i][0] = 0;

        board->white_piece_move_directions[i][0] = 0;
        board->black_piece_move_directions[i][0] = 0;
    }

    for (int ind_row = 0; ind_row < 20; ind_row++){
        for (int ind_col = 0; ind_col < 20; ind_col++){
            board->board[ind_row][ind_col] = 0;
        }
    }
    for (int i = 0; i < 500; i++){
        board->captured_piece[i] = 0;
    }
}

void create_chess(struct ChessBoard *board){
    setup_normals(board);
    board->size = 8;
    add_pawns(board);
    add_king(board);
    add_rooks(board);
    add_queen(board);
    add_knight(board);
    add_bishop(board);
}

int main() {
    // Erstellen einer Instanz der Struktur ChessBoard
    struct ChessBoard board;

    create_chess(&board);
    printChessBoard(&board);

    
    return 0;
}