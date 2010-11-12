
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
    double Evaluate(const char *u, const char *v);

  protected:

    /*
     * Data Members
     */
    double mLambda; // Decay factor
    unsigned mMaxLen; // Maximum input string length
    unsigned mSeqLength; // Length of target subsequences
    double ***mCache; // Dynamic Programming LUT
    bool mInitialized; // Whether we've been initialized

    /*
     * Helper methods
     */
    double Kprime (const char *u, int p, const char *v, int q, int n);
    double K (const char *u, int p, const char *v, int q, int n);
};
