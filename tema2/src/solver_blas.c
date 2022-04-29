/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"
#include <cblas.h>
#include <string.h>
/* 
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {

	// BTXB
	double *BTXB = calloc(N * N, sizeof(double));
	memset(BTXB, 0, N * N * sizeof(double));
	cblas_dgemm(CblasRowMajor, CblasTrans, CblasNoTrans, N, N, N, 1, B, N, B, N, 1, BTXB, N);

	// BXA
	double *BXA = calloc(N * N, sizeof(double));
	memset(BXA, 0, N * N * sizeof(double));
	cblas_dcopy(N * N, B, 1, BXA, 1);
	cblas_dtrmm(CblasRowMajor, CblasRight, CblasUpper, CblasTrans, CblasNonUnit, N, N, 1, A, N, BXA, N);
	
	//BXAXAT
	double *BXAXAT = calloc(N * N, sizeof(double));
	memset(BXAXAT, 0, N * N * sizeof(double));
	cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasTrans, N, N, N, 1, BXA, N, A, N, 1, BXAXAT, N);

	// BXAXAT + BTXB
	double *result = (double*)malloc(N * N * sizeof(double));
	memset(result, 0, N * N * sizeof(double));
	cblas_dcopy(N * N, BTXB, 1, result, 1);

	// 0 buffer
	double *oneMatrix = calloc(N * N, sizeof(double));
	memset(oneMatrix, 1, N * N * sizeof(double));

	cblas_dgemm(CblasRowMajor, CblasTrans, CblasNoTrans, N, N, N, 1, BXAXAT, N, oneMatrix, N, 1, result, N);

	free(BTXB);
	free(BXA);
	free(BXAXAT);
	free(oneMatrix);

	return result;

}
