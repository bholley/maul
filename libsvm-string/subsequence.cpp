#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "subsequence.h"

/*
 * Original code from:
 * http://www.learning-kernel-classifiers.org/code/string_kernels/strings.c
 * */

void
SubseqKernel::Init(unsigned maxLen, unsigned seqLength, double lambda)
{
  // Store initialization parameters
  mMaxLen = maxLen;
  mSeqLength = seqLength;
  mLambda = lambda;

  // Allocate memory for the dynamic programming cache variable
  mCache  = (double ***) malloc (mSeqLength * sizeof (double **));
  for (unsigned i = 1; i < mSeqLength; i++) {
    mCache  [i] = (double **) malloc (mMaxLen * sizeof (double *));
    for (unsigned j = 0; j < maxLen; j++)
      mCache  [i] [j] = (double *) malloc (mMaxLen * sizeof (double));
  }

  // Precompute powers of lambda
  mLambdaPows = (double *) malloc ((maxLen + 2) * sizeof(double));
  mLambdaPows[0] = 1;
  mLambdaPows[1] = mLambda;
  for (unsigned i = 2; i < maxLen + 2; ++i)
    mLambdaPows[i] = mLambdaPows[i-1] * mLambda;


  // Mark us as initialized
  mInitialized = true;
}

SubseqKernel::~SubseqKernel()
{
  // If we were never initialized, there's nothing to do.
  if (!mInitialized)
    return;

  // Free the DP LUT
  for (unsigned i = 1; i < mSeqLength; i++) {
    for (unsigned j = 0; j < mMaxLen; j++) 
      free(mCache[i][j]);
    free(mCache[i]);
  }
  free(mCache);

  // Free the lambda cache
  free(mLambdaPows);

  mInitialized = false;
}

double
SubseqKernel::Evaluate(const char *u, const char *v)
{
  // We must be initialized
  if (!mInitialized) {
    fprintf(stderr, "Trying to evaluate using subsequence kernel, but not intialized!\n");
    exit(-1);
  }

  // We're screwed if the string is too big.
  unsigned ulen = strlen(u);
  unsigned vlen = strlen(v);
  if (ulen > mMaxLen || vlen > mMaxLen) {
    fprintf(stderr, "String passed to subsequence kernel is too large! Aborting!\n");
    exit(-1);
  }

  // New strings, so blow away the parts of the cache that we're going to use
  for (unsigned i = 1; i < mSeqLength; ++i)
    for (unsigned j = 0; j < ulen; ++j)
      for (unsigned k = 0; k < vlen; ++k)
        mCache[i][j][k] = -1.0;

  // Invoke recursion
  return K(u, strlen(u), v, strlen(v), mSeqLength);
}

/*
 * Protected helper methods
 */

double
SubseqKernel::Kprime(const char *u, int p, const char *v, int q, int n)
{
  int j;
  double tmp;

  /* case 1: if a full substring length is processed, return*/
  if (n == 0) return (1.0);

  /* check, if the value was already computed in a previous computation */
  if (mCache [n] [p] [q] != -1.0) return (mCache [n] [p] [q]); 
  
  /* case 2: at least one substring is to short */
  if (p < n || q < n) return (0.0);
    
  /* case 3: recursion */
  for (j= 0, tmp = 0; j < q; j++) {
    if (v [j] == u [p - 1]) 
      tmp += Kprime (u, p - 1, v, j, n - 1) * mLambdaPows[q-j+1];
  }

  mCache [n] [p] [q] = mLambda * Kprime (u, p - 1, v, q, n) + tmp;
  return (mCache [n] [p] [q]);
}

double
SubseqKernel::K(const char *u, int p, const char *v, int q, int n)
{
  int j;
  double KP;

  /* the simple case: (at least) one string is to short */
  if (p < n || q < n) return (0.0);

  /* the recursion: use Kprime for the t'th substrings*/
  for (j = 0, KP = 0.0; j < q; j++) {
    if (v [j] == u [p - 1]) 
      KP += Kprime (u, p - 1, v, j, n - 1) * mLambda * mLambda;
  }
  
  return (K (u, p - 1, v, q, n) + KP);
}

