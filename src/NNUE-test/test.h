#ifndef TEST_H
#define TEST_H

#define M 256
#define N 40960

#ifdef __cplusplus
extern "C" {
#endif

// Hier können C-kompatible Funktionsdeklarationen hinzugefügt werden

#ifdef __cplusplus
}
#endif

#ifdef __cplusplus
#include <cstdlib> // Für std::rand und std::srand

struct LinearLayer {
    int inputDimension;
    int outputDimension;
    float* biases;
    float** weights; // zweidimensionales Array für Gewichtungen

    // Constructor to initialize the layer with random biases and weights
    LinearLayer(int inDim, int outDim) : inputDimension(inDim), outputDimension(outDim) {
        biases = new float[outDim];
        weights = new float*[outDim];

        // Initialize biases with random values between -1 und 1
        for (int i = 0; i < outDim; ++i) {
            biases[i] = static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX) * 2.0f - 1.0f;
        }

        // Initialize weights with random values between -1 und 1
        for (int i = 0; i < outDim; ++i) {
            weights[i] = new float[inDim];
            for (int j = 0; j < inDim; ++j) {
                weights[i][j] = static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX) * 2.0f - 1.0f;
            }
        }
    }

    // Destructor to release dynamically allocated memory
    ~LinearLayer() {
        delete[] biases;
        for (int i = 0; i < outputDimension; ++i) {
            delete[] weights[i];
        }
        delete[] weights;
    }
};

struct NNUE {
    LinearLayer layer_0;
    LinearLayer layer_1;
    LinearLayer layer_2;
    LinearLayer layer_3;

    // Constructor for NNUE structure
    NNUE(int inputDim_0, int outputDim_0, int inputDim_1, int outputDim_1, int inputDim_2, int outputDim_2, int inputDim_3, int outputDim_3)
        : layer_0(inputDim_0, outputDim_0),
          layer_1(inputDim_1, outputDim_1),
          layer_2(inputDim_2, outputDim_2),
          layer_3(inputDim_3, outputDim_3) {}
};

enum Color {
 WHITE = 1,
 BLACK = 0,
};

struct NnueAccumulator {
    float v[2][M];
    // we count the updates since last refresh for each side since updates can introduce error we can than refresh every x updates
    int updates[2];
    // Konstruktor zum Initialisieren mit null
    NnueAccumulator() {
        for (int i = 0; i < 2; ++i) {
            for (int j = 0; j < M; ++j) {
                v[i][j] = 0.0f;
            }
        }
        updates[0] = 0;
        updates[1] = 0;
    }

    float* operator[](Color perspective) {
        return v[perspective];
    }
};

void call_refresh_accumulator(int* active_features, int size, NNUE* nnue, NnueAccumulator* acc, int color_to_move);

void update_accumulator(int *added_features, int size_add, int* removed_features, int size_removed, NNUE * nnue, NnueAccumulator* acc, int color_to_move);

#endif // __cplusplus

#endif // TEST_H
