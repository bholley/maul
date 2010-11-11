#include <math.h>
#include <string.h>
#include <stdlib.h>
#include "subsequence.h"

/* Original code from http://www.learning-kernel-classifiers.org/code/string_kernels/strings.c */

double     ***cache;       /* this dynamic variable saves the auxillary
            kernel values computed */

double Kprime (char *u, int p, char *v, int q, int n, double lambda) {
  register int         j;
  double               tmp;

  /* case 1: if a full substring length is processed, return*/
  if (n == 0) return (1.0);

  /* check, if the value was already computed in a previous computation */
  if (cache [n] [p] [q] != -1.0) return (cache [n] [p] [q]); 
  
  /* case 2: at least one substring is to short */
  if (p < n || q < n) return (0.0);
    
  /* case 3: recursion */
  for (j= 0, tmp = 0; j < q; j++) {
    if (v [j] == u [p - 1]) 
      tmp += Kprime (u, p - 1, v, j, n - 1, lambda) *   
        pow (lambda, (float) (q - j + 1));
  }

  cache [n] [p] [q] = lambda * Kprime (u, p - 1, v, q, n, lambda) + tmp;
  return (cache [n] [p] [q]);
}

double K (char *u, int p, char *v, int q, int n, double lambda) {
  register int  j;
  double        KP;

  /* the simple case: (at least) one string is to short */
  if (p < n || q < n) return (0.0);

  /* the recursion: use Kprime for the t'th substrings*/
  for (j = 0, KP = 0.0; j < q; j++) {
    if (v [j] == u [p - 1]) 
      KP += Kprime (u, p - 1, v, j, n - 1, lambda) * lambda * lambda;
  }
  
  return (K (u, p - 1, v, q, n, lambda) + KP);
}

/* recursively computes the subsequence kernel between s and t
   where subsequences of EXACTLY length n are considered */
double subsequence (char *u, char *v, int n, double lambda) {
  int           p = strlen (u), q = strlen (v), i, j, k;
  double        ret;

  /* allocate memory for auxiallary cache variable */
  cache  = (double ***) malloc (n * sizeof (double **));
  for (i = 1; i < n; i++) {
    cache  [i] = (double **) malloc (p * sizeof (double *));
    for (j = 0; j < p; j++) {
      cache  [i] [j] = (double *) malloc (q * sizeof (double));
      for (k = 0; k < q; k++) 
  cache  [i] [j] [k] = -1.0;
    }
  }
  
  /* invoke recursion */
  ret = K (u, p, v, q, n, lambda);
  
  /* free memory */
  for (i = 1; i < n; i++) {
    for (j = 0; j < p; j++) 
      free (cache  [i] [j]);
    free (cache  [i]);
  }
  free (cache);
  
  /* return the computed value */
  return (ret);
}
