/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"

/*
 * Add your unoptimized implementation here
 */
double* my_solver(int N, double *A, double* B) {

	// A transpose
	double *AT = (double*)malloc(N * N * sizeof(double));
	memset(AT, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = i; j < N; j++) {
			AT[i][j] = A[j][i];
		}
	}

	// B transpose
	double *BT = (double*)malloc(N * N * sizeof(double));
	memset(BT, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			BT[i][j] = B[j][i];
		}
	}

	// make BT X B
	double *BTXB = (double*)malloc(N * N * sizeof(double));
	memset(BTXB, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			for (int k = 0; k < N; k++) {
				BTXB[i][j] = BTXB[i][j] + BT[i][k] * B[k][j];
			}
		}
	}

	// make B X A
	double *BXA = (double*)malloc(N * N * sizeof(double));
	memset(BXA, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			for (int k = 0; k <= i; k++) {
				BXA[i][j] = BXA[i][j] + B[i][k] * A[k][j];
			}
		}
	}

	// BXA X AT
	double *BXAXAT = (double*)malloc(N * N * sizeof(double));
	memset(BXAXAT, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			for (int k = 0; k < N; k++) {
				BXAXAT[i][j] = BXAXAT[i][j] + BXA[i][k] * AT[k][j];
			}
		}
	}

	// BXAXAT + BTXB
	double *result = (double*)malloc(N * N * sizeof(double));
	memset(result, 0, N * N * sizeof(double));
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			result[i][j] = BXAXAT[i][j] + BTXB[i][j];
		}
	}

	free(AT);
	free(BT);
	free(BTXB);
	free(BXA);
	free(BXAXAT);
	
	return result;
}
