#ifndef _SUBSEQUENCE_H
#define _SUBSEQUENCE_H

template<typename T>
class SubseqKernel {

  public:
    SubseqKernel()
      : mLambda(0.0)
      , mMaxLen(0)
      , mSeqLength(0)
      , mCache(NULL)
      , mInitialized(false) {};
    ~SubseqKernel();
    void Init(unsigned maxLen, unsigned seqLength, double lambda);
    double Evaluate(const T *u, unsigned uLen, const T *v, unsigned vLen);

  protected:

    /*
     * Data Members
     */
    double mLambda; // Decay factor
    unsigned mMaxLen; // Maximum input string length
    unsigned mSeqLength; // Length of target subsequences
    double ***mCache; // Dynamic Programming LUT
    double *mLambdaPows; // Cache of powers of lambda
    bool mInitialized; // Whether we've been initialized

    /*
     * Helper methods
     */
    double Kprime (const T *u, int p, const T *v, int q, int n);
    double K (const T *u, int p, const T *v, int q, int n);
};

// Implementation
#include "subsequence.tcc"

#endif /* _SUBSEQ_H */
