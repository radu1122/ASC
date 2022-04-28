/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"
#include <string.h>

/*
 * Add your unoptimized implementation here
 */
double* my_solver(int N, double *A, double* B) {

	// A transpose
	double *AT = (double*)malloc(N * N * sizeof(double));
	memset(AT, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		// j will start from i because we want to transpose the upper triangular part of A
		for (int j = i; j < N; j++) {
			AT[j * N + i] = A[i * N + j];
		}
	}

	// B transpose
	double *BT = (double*)malloc(N * N * sizeof(double));
	memset(BT, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			BT[j * N + i] = B[i * N + j];
		}
	}

	// make BT X B
	double *BTXB = (double*)malloc(N * N * sizeof(double));
	memset(BTXB, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			for (int k = 0; k < N; k++) {
				BTXB[i * N + j] = BTXB[i * N + j] + BT[i * N + k] * B[k * N + j];
			}
		}
	}

	// make B X A
	double *BXA = (double*)malloc(N * N * sizeof(double));
	memset(BXA, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			// k will go only to j because A is upper triangular
			for (int k = 0; k <= j; k++) {
				BXA[i * N + j] = BXA[i * N + j] + B[i * N + k] * A[k * N + j];
			}
		}
	}

	// BXA X AT
	double *BXAXAT = (double*)malloc(N * N * sizeof(double));
	memset(BXAXAT, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			// k will start with j because A is lower triangular
			for (int k = j; k < N; k++) {
				BXAXAT[i * N + j] = BXAXAT[i * N + j] + BXA[i * N + k] * AT[k * N + j];
			}
		}
	}

	// BXAXAT + BTXB
	double *result = (double*)malloc(N * N * sizeof(double));
	memset(result, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			result[i * N + j] = BXAXAT[i * N + j] + BTXB[i * N + j];
		}
	}

	free(AT);
	free(BT);
	free(BTXB);
	free(BXA);
	free(BXAXAT);
	
	return result;
}
