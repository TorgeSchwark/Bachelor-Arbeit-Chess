#include <immintrin.h> // Für AVX2 Intrinsics
#include <stdint.h>    // Für int16_t
#include <vector>
#include <cassert>
#include <iostream>
#include <algorithm>
#include <cstring>
#include <chrono> 

const int M = 256;
const int N = 40960;

typedef enum { WHITE = 0, BLACK = 1 } Color;

struct NnueAccumulator {
    // Two vectors of size M. v[0] for white's, and v[1] for black's perspectives.
    int v[2][M];

    // This will be utilised in later code snippets to make the access less verbose
    int* operator[](Color perspective) {
        return v[perspective];
    }
};

struct LinearLayer {
    int bias[M];
    int weight[N][M];

    int num_inputs;
    int num_outputs;

    // Konstruktor, um num_inputs und num_outputs festzulegen
    LinearLayer(int inputs, int outputs) : num_inputs(inputs), num_outputs(outputs) {
        // Initialisiere bias und weight hier entsprechend deiner Anforderungen
        // Beispiel: Alle Bias-Werte auf 0 setzen
        std::fill_n(bias, M, 0.0f);

        // Beispiel: Gewichtungen initialisieren
        // Für Demo-Zwecke: Initialisiere weight mit zufälligen Werten
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < M; ++j) {
                weight[i][j] = static_cast<int
                >(rand()) / static_cast<int
                >(RAND_MAX); // Zufälliger Wert zwischen 0 und 1
            }
        }
    }
};

void refresh_accumulator(
    const LinearLayer&      layer,            // this will always be L_0
    NnueAccumulator&        new_acc,          // storage for the result
    const std::vector<int>& active_features,  // the indices of features that are active for this position
    Color                   perspective       // the perspective to refresh
) {
    // First we copy the layer bias, that's our starting point
    for (int i = 0; i < M; ++i) {
        new_acc[perspective][i] = layer.bias[i];
    }

    // Then we just accumulate all the columns for the active features. That's what accumulators do!
    for (int a : active_features) {
        for (int i = 0; i < M; ++i) {
            new_acc[perspective][i] += layer.weight[a][i];
        }
    }
}

void update_accumulator(
    const LinearLayer&      layer,            // this will always be L_0
    NnueAccumulator&        new_acc,          // it's nice to have already provided storage for
                                              // the new accumulator. Relevant parts will be overwritten
    NnueAccumulator&  prev_acc,         // the previous accumulator, the one we're reusing
    const std::vector<int>& removed_features, // the indices of features that were removed
    const std::vector<int>& added_features,   // the indices of features that were added
    Color                   perspective       // the perspective to update, remember we have two,
                                              // they have separate feature lists, and it even may happen
                                              // that one is updated while the other needs a full refresh
) {
    // First we copy the previous values, that's our starting point
    for (int i = 0; i < M; ++i) {
        new_acc[perspective][i] = prev_acc[perspective][i];
    }

    // Then we subtract the weights of the removed features
    for (int r : removed_features) {
        for (int i = 0; i < M; ++i) {
            // Just subtract r-th column
            new_acc[perspective][i] -= layer.weight[r][i];
        }
    }

    // Similar for the added features, but add instead of subtracting
    for (int a : added_features) {
        for (int i = 0; i < M; ++i) {
            new_acc[perspective][i] += layer.weight[a][i];
        }
    }
}

int* linear(const LinearLayer& layer,  // the layer to use. We have two: L_1, L_2
    int *             output, // the already allocated storage for the result
    const int*       input   // the input, which is the output of the previous ClippedReLU layer
) {
    // First copy the biases to the output. We will be adding columns on top of it.
    for (int i = 0; i < layer.num_outputs; ++i) {
        output[i] = layer.bias[i];
    }

    // Remember that rainbowy diagram long time ago? This is it.
    // We're adding columns one by one, scaled by the input values.
    for (int i = 0; i < layer.num_inputs; ++i) {
        for (int j = 0; j < layer.num_outputs; ++j) {
            output[j] += input[i] * layer.weight[i][j];
        }
    }

    // Let the caller know where the used buffer ends.
    return output + layer.num_outputs;
}

int min(int x, int y){
    if(x > y){
        return y;
    }else{
        return x;
    }
}

int max(int x, int y){
    if(x < y){
        return y;
    }else{
        return x;
    }
}

int* crelu(
    int        size,   // no need to have any layer structure, we just need the number of elements
    int*       output, // the already allocated storage for the result
    const int* input   // the input, which is the output of the previous linear layer
) {
    for (int i = 0; i < size; ++i) {
        output[i] = min(max(input[i], 0), 1);
    }

    return output + size;
}
LinearLayer L_0(40960, 512);
LinearLayer L_1(512, 32);
LinearLayer L_2(32, 32);
LinearLayer L_3(32, 1);




int nnue_evaluate(NnueAccumulator& accumulator) {
    int buffer[2*N]; // allocate enough space for the results

    // We need to prepare the input first! We will put the accumulator for
    // the side to move first, and the other second.
    int input[2*M];
    Color stm = WHITE;
    for (int i = 0; i < M; ++i) {
        input[  i] = accumulator[ stm][i];
        input[M+i] = accumulator[BLACK][i];
    }

    int* curr_output = buffer;
    int* curr_input = input;
    int* next_output;

    // Evaluate one layer and move both input and output forward.
    // The last output becomes the next input.
    next_output = crelu(2 * M, curr_output, curr_input);
    curr_input = curr_output;
    curr_output = next_output;

    next_output = linear(L_1, curr_output, curr_input);
    curr_input = curr_output;
    curr_output = next_output;

    next_output = crelu(L_2.num_outputs, curr_output, curr_input);
    curr_input = curr_output;
    curr_output = next_output;

    next_output = linear(L_3, curr_output, curr_input);

    // We're done. The last layer should have put 1 value out under *curr_output.
    return *curr_output;
}

int main() {
    // 

    // Du kannst jetzt L_0 in den Funktionen verwenden, die LinearLayer benötigen,
    // wie z.B. refresh_accumulator, update_accumulator, linear und nnue_evaluate.

    // Beispiel für die Verwendung von L_0 in den Funktionen refresh_accumulator und update_accumulator
    NnueAccumulator accumulator; // Beispiel für NnueAccumulator Instanz
    std::vector<int> active_features = {0, 1, 2};
    std::vector<int> removed_features = {3, 4};
    std::vector<int> added_features = {5, 6};

    refresh_accumulator(L_0, accumulator, active_features, WHITE);
    update_accumulator(L_0, accumulator, accumulator, removed_features, added_features, BLACK);

    // Beispiel für die Verwendung von L_0 in anderen Teilen deines Programms

    auto start_evaluate = std::chrono::high_resolution_clock::now();
    int evaluation_result;
    for (int i = 0; i < 1000000; i++){
        evaluation_result = nnue_evaluate(accumulator);
    }
    auto end_evaluate = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_evaluate = end_evaluate - start_evaluate;
    std::cout << "Time for nnue_evaluate: " << elapsed_evaluate.count() << " seconds\n";



    printf("das Ergebniss ist %d", evaluation_result);

    // Weitere Verwendung von L_0 gemäß deiner Anwendungslogik
    // ...

    return 0;
}