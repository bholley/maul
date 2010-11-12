
class SubseqKernel {

  public:
    SubseqKernel(unsigned maxLen, unsigned seqLength, double lambda);
    ~SubseqKernel();
    double Evaluate(const char *u, const char *v);

  protected:

    /*
     * Data Members
     */
    double mLambda; // Decay factor
    unsigned mMaxLen; // Maximum input string length
    unsigned mSeqLength; // Length of target subsequences
    double ***mCache; // Dynamic Programming LUT

    /*
     * Helper methods
     */
    double Kprime (const char *u, int p, const char *v, int q, int n);
    double K (const char *u, int p, const char *v, int q, int n);
};
