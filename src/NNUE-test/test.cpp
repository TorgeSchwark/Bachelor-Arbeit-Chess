#include "test.h"
#include <iostream>
#include <iomanip> // Für std::setprecision
#include <cmath>   // Für std::fabs
#include <cstdlib> // Für std::rand und std::srand
#include <ctime>   // Für std::time
#include <immintrin.h>
#include <chrono> 
#include <vector>

// https://github.com/casanche/casanchess/blob/master/src/NNUE.cpp
// https://github.com/official-stockfish/nnue-pytorch/blob/master/docs/nnue.md


// p_idx = piece_type * 2 + piece_color
// halfkp_idx = piece_square + (p_idx + king_square * 10) * 64

// Struct to represent a linear layer in a neural network

void call_refresh_accumulator(int* active_features, int size, NNUE* nnue, NnueAccumulator* acc, int color_to_move) {
    // Konvertiere das int-Array in einen std::vector<int>
    std::vector<int> active_features_vector(active_features, active_features + size);
    
    if (color_to_move == 1) {
        refresh_accumulator(nnue->layer_0, *acc, active_features_vector, WHITE);
    } else {
        refresh_accumulator(nnue->layer_0, *acc, active_features_vector, BLACK);
    }
}

void update_accumulator(int *added_features, int size_add, int* removed_features, int size_removed, NNUE * nnue, NnueAccumulator* acc, int color_to_move){

    std::vector<int> added_features_vector(added_features, added_features + size_add);
    std::vector<int> removed_features_vector(removed_features, removed_features + size_removed);
  
    if(color_to_move == 1) {
        update_accumulator(nnue->layer_0, *acc, added_features_vector, removed_features_vector, WHITE);
    } else {
        update_accumulator(nnue->layer_0, *acc, added_features_vector, removed_features_vector, BLACK);
    }
}

void refresh_accumulator(
    const LinearLayer&      layer,            // this will always be L_0
    NnueAccumulator&        acc,          // storage for the result
    const std::vector<int>& active_features,  // the indices of features that are active for this position
    Color                   perspective       // the perspective to refresh
) {
    // First we copy the layer bias, that's our starting point
    for (int i = 0; i < M; ++i) {
        acc[perspective][i] = layer.biases[i];
    }

    // Then we just accumulate all the columns for the active features. That's what accumulators do!
    for (int a : active_features) {
        for (int i = 0; i < M; ++i) {
            acc[perspective][i] += layer.weights[a][i];
        }
    }
    acc.updates[perspective] = 0;
}

void update_accumulator(
    const LinearLayer&      layer,            // this will always be L_0
    NnueAccumulator&       acc,         // the previous accumulator, the one we're reusing
    const std::vector<int>& removed_features, // the indices of features that were removed
    const std::vector<int>& added_features,   // the indices of features that were added
    Color                   perspective       // the perspective to update, remember we have two,
                                              // they have separate feature lists, and it even may happen
                                              // that one is updated while the other needs a full refresh
) {
    // Then we subtract the weights of the removed features
    for (int r : removed_features) {
        for (int i = 0; i < M; ++i) {
            // Just subtract r-th column
            acc[perspective][i] -= layer.weights[r][i];
        }
    }

    // Similar for the added features, but add instead of subtracting
    for (int a : added_features) {
        for (int i = 0; i < M; ++i) {
            acc[perspective][i] += layer.weights[a][i];
        }
    }
    acc.updates[perspective] +=1 ;
}


// Function to multiply two __m256 vectors
inline __m256 mm256_mul_ps(__m256 a, __m256 b) {
    return _mm256_mul_ps(a, b);
}

// Function to add two __m256 vectors
inline __m256 mm256_add_ps(__m256 a, __m256 b) {
    return _mm256_add_ps(a, b);
}

// Function to perform fused multiply-add using AVX intrinsics
inline __m256 mm256_fmadd_ps(__m256 a, __m256 b, __m256 c) {
    return mm256_add_ps(mm256_mul_ps(a, b), c);
}

// Function to horizontally sum an __m256 vector
inline float HorizontalSum256(__m256 v) {
    // Perform horizontal addition using AVX intrinsics
    const __m128 r4 = _mm_add_ps(_mm256_castps256_ps128(v), _mm256_extractf128_ps(v, 1));
    const __m128 r2 = _mm_add_ps(r4, _mm_movehl_ps(r4, r4));
    const __m128 r1 = _mm_add_ss(r2, _mm_movehdup_ps(r2));
    return _mm_cvtss_f32(r1);
}

// Function to clamp a float value between 0 and 1
float Clamp(float n) {
    const float min = 0;
    const float max = 1;
    if (n < min) return min;
    if (n > max) return max;
    return n;
}

// Function to compute a layer using AVX instructions
void ComputeLayer(float* inputLayer, float* outputLayer, LinearLayer& layer, bool with_ReLU) {
    int inDim = layer.inputDimension;
    int outDim = layer.outputDimension;

    for (int o = 0; o < outDim; o++) {
        float sum = layer.biases[o];

        const float* weightsRow = layer.weights[o];

        // Initialize accumulator
        __m256 dot = _mm256_setzero_ps();

        // Loop over input dimensions, processing 32 elements at a time
        for (int i = 0; i < inDim; i += 32) {
            // Load inputs using AVX intrinsics
            __m256 inputs = _mm256_loadu_ps(&inputLayer[i]);

            // Load weights using AVX intrinsics
            __m256 weightValues = _mm256_loadu_ps(&weightsRow[i]);

            // Perform FMA (Fused Multiply-Add)
            dot = mm256_fmadd_ps(inputs, weightValues, dot);
        }

        // Horizontal sum of dot products
        sum += HorizontalSum256(dot);

        // Apply ReLU if required
        if (with_ReLU) {
            outputLayer[o] = Clamp(sum);
        } else {
            outputLayer[o] = sum;
        }
    }
}

void testComputeLayer() {
    const int dimInput = 512;
    const int dimOutput1 = 32;
    const int dimOutput2 = 32;
    const int dimOutput3 = 1;

    // Beispiel: Initialisiere Eingabeschicht, Bias, Gewichtungen und Ausgabeschicht für alle drei Layer
    float inputLayer[dimInput];
    float outputLayer1[dimOutput1];
    float outputLayer2[dimOutput2];
    float outputLayer3[dimOutput3];

    // Erstelle die LinearLayer-Objekte für jeden Layer
    LinearLayer layer1(dimInput, dimOutput1);
    LinearLayer layer2(dimOutput1, dimOutput2);
    LinearLayer layer3(dimOutput2, dimOutput3);

    LinearLayer layer0(40960, 512);
    NnueAccumulator acc;
    bool with_ReLU = true;

    const std::vector<int> test = {1,2,3,4};

    refresh_accumulator(layer0, acc, test, WHITE);

    update_accumulator(layer0, acc, test, test, WHITE);

    // Initialisiere Eingabeschicht mit zufälligen Werten zwischen 0 und 1
    for (int i = 0; i < dimInput; ++i) {
        inputLayer[i] = static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX);
    }

    auto start = std::chrono::high_resolution_clock::now();

    // Berechne den ersten Layer
    for( int i  = 0; i < 300000; i++){
        ComputeLayer(inputLayer, outputLayer1, layer1, with_ReLU);

        // Berechne den zweiten Layer
        ComputeLayer(outputLayer1, outputLayer2, layer2, with_ReLU);

        // Berechne den dritten Layer
        ComputeLayer(outputLayer2, outputLayer3, layer3, with_ReLU);
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;

    // Ausgabe der Zeit
    std::cout << "ComputeLayer execution time: " << duration.count() << " seconds\n";

    // Ausgabe der Ergebnisse
    std::cout << "Input Layer:\n";
    for (int i = 0; i < dimInput; ++i) {
        std::cout << inputLayer[i] << " ";
    }
    std::cout << "\n\nOutput Layer 1:\n";
    for (int i = 0; i < dimOutput1; ++i) {
        std::cout << outputLayer1[i] << " ";
    }
    std::cout << "\n\nOutput Layer 2:\n";
    for (int i = 0; i < dimOutput2; ++i) {
        std::cout << outputLayer2[i] << " ";
    }
    std::cout << "\n\nOutput Layer 3:\n";
    for (int i = 0; i < dimOutput3; ++i) {
        std::cout << outputLayer3[i] << " ";
    }
    std::cout << "\n";
}

int main() {
    std::srand(static_cast<unsigned int>(std::time(nullptr))); // Zufallsgenerator initialisieren

    // Teste die ComputeLayer-Funktion
    testComputeLayer();

    return 0;
}
