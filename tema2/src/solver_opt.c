/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"
#include <string.h>

/*
 * Add your optimized implementation here
 */
double* my_solver(int N, double *A, double* B) {


	for (int i = 0; i < N; i++) {
		// j will start from i because we want to transpose the upper triangular part of A
		for (int j = i; j < N; j++) {
		}
	}
	// A transpose
	// B transpose
	double *AT = (double*)malloc(N * N * sizeof(double));
	double *BT = (double*)malloc(N * N * sizeof(double));
	memset(AT, 0, N * N * sizeof(double));
	memset(BT, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			AT[j * N + i] = A[i * N + j];
			BT[j * N + i] = B[i * N + j];
		}
	}

	// make BT X B
	double *BTXB = (double*)malloc(N * N * sizeof(double));
	memset(BTXB, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			register double *a = &BT[i * N];
			register double *b = &B[j];

			register double sum = 0.0;
			for (int k = 0; k < N; k++) {
				sum = sum + *a * *b;
				a++;
				b += N;
			}
			BTXB[i * N + j] = sum;
		}
	}

	// make B X A
	double *BXA = (double*)malloc(N * N * sizeof(double));
	memset(BXA, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			register double *a = &B[i * N];
			register double *b = &A[j];

			register double sum = 0.0;
			// k will go only to j because A is upper triangular
			for (int k = 0; k <= j; k++) {
				sum = sum + *a * *b;
				a++;
				b += N;
			}
			BXA[i * N + j] = sum;
		}
	}

	// BXA X AT
	double *BXAXAT = (double*)malloc(N * N * sizeof(double));
	memset(BXAXAT, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			register double *a = &BXA[i * N + j];
			register double *b = &AT[j * N + j];

			register double sum = 0.0;
			// k will start with j because A is lower triangular
			for (int k = j; k < N; k++) {
				sum = sum + *a * *b;
				a++;
				b += N;
			}
			BXAXAT[i * N + j] = sum;
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
