/*
 * Tema 2 ASC
 * 2022 Spring
 */
#include "utils.h"
#include <cblas.h>
#include <string.h>
#define ALPHA 1
/* 
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {

	// BTXB
	double *BTXB = (double*)malloc(N * N * sizeof(double));
	memset(BTXB, 0, N * N * sizeof(double));
	cblas_dgemm(CblasRowMajor, CblasTrans, CblasNoTrans, N, N, N, ALPHA, B, N, B, N, ALPHA, BTXB, N);

	// BXA
	double *BXA = (double*)malloc(N * N * sizeof(double));
	memset(BXA, 0, N * N * sizeof(double));
	cblas_dcopy(N * N, B, ALPHA, BXA, ALPHA);
	cblas_dtrmm(CblasRowMajor, CblasRight, CblasUpper, CblasNoTrans, CblasNonUnit, N, N, ALPHA, A, N, BXA, N);
	
	// BXAXAT + BTXB
	double *result = (double*)malloc(N * N * sizeof(double));
	memset(result, 0, N * N * sizeof(double));
	cblas_dcopy(N * N, BTXB, ALPHA, result, ALPHA);
	cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasTrans, N, N, N, ALPHA, BXA, N, A, N, ALPHA, result, N);

	free(BTXB);
	free(BXA);

	return result;

}
