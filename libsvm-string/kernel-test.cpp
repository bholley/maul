#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "subsequence.h"

int edit(const char *px, const char *py);
#ifndef min
template <class T> static inline T min(T x,T y) { return (x<y)?x:y; }
#endif
#ifndef max
template <class T> static inline T max(T x,T y) { return (x>y)?x:y; }
#endif

//const char *s1 = "Mozilla/5.0 (X11; U; DragonFly i386; de; rv:1.9.1) Gecko/20090720 Firefox/3.5.1";
//const char *s2 = "Mozilla/5.0 (X11; U; FreeBSD amd64; en-US; rv:1.8.0.8) Gecko/20061116 Firefox/1.5.0.8";

const char *s1 = "rv:1.9.1) Gecko/20090720 Firefox/3.5.1";
const char *s2 = "rv:1.8.0.8) Gecko/20061116 Firefox/1.5.0.8";

int main(int argc, char **argv)
{

  double similar, different = 0.0;

  SubseqKernel<char> kernel;
  kernel.Init(1000, 5, .8);

  for (int i = 0; i < 2000; ++i)
    similar = kernel.Evaluate(s1, s2);

  /*
  double similar = edit("whatareyoudoing", "whatareyoudoing");
  double different = edit("whatareyoudoing", "gdaymate");
  */

  printf("similar: %f, different: %f\n", similar, different);

  return 0;
}

int edit(const char *px, const char *py)
{
  static unsigned callCount = 0;
	int* row[2];
	int len1,len2;
	int now,old;
	int i,j;
	int result;

  callCount++;
  if (!(callCount % 1000))
    printf("CallCount: %u\n", callCount);

	len1=(int)strlen(px); len2=(int)strlen(py);

	row[0] = (int*) malloc( (len1+1) * sizeof(int) );
	row[1] = (int*) malloc( (len1+1) * sizeof(int) );

	for(i=0;i<len1+1;i++) row[0][i]=i;
	now=1; old=0;

	for(j=0;j<len2;j++) /* j=0 is the first char of py */
	{
		row[now][0]=j+1;
		for(i=0;i<len1;i++) /* i=0 is the first char of px */
		{
			row[now][i+1] = min(min( row[old][i] + (px[i]==py[j]?0:1) , 
						 row[old][i+1] + 1),
					    row[now][i] + 1                        );
		}

		now=1-now; old=1-old;
	}

	result=row[old][len1];
   
	free(row[0]); free(row[1]);

	return result;
}
