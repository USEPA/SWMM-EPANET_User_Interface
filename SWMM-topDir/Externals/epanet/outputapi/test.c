#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include "outputapi.h"

int   main()
/*--------------------------------------------------------------
 ** test for outputapi library
 **--------------------------------------------------------------
 */
{
  ENResultsAPI* addr;
  int ENversion, warncode;
  char* filename= "Net1.bin";
  char* nodeID;
  int ierr, count, max, i, idx=10;
  float value;
  nodeID= malloc(sizeof(char)*(MAXID+1));

  printf("so far so good\n");

  // try to open file
  ierr= ENR_open(&addr, filename );
  if (ierr==0) printf("%s opened\n", filename);
  else {
    printf("open failed!\n");
    return 1;
    }
    
  //check ENversion
  ENR_getEnVersion(addr, &ENversion);
  printf("EN version %d\n", ENversion);
  
  //check warnings
  ENR_getWarningCode(addr, &warncode);
  if (warncode) printf("warnings!  %d\n", warncode);
  else printf("no warning\n");

  // then check some values
  ierr= ENR_getNetSize(addr, ENR_nodeCount, &count);
  if (ierr==0) printf("nodes %d\n", count);

  ierr= ENR_getNetSize(addr, ENR_tankCount, &count);
  if (ierr==0) printf("tanks %d\n", count);

  ierr= ENR_getNetSize(addr, ENR_linkCount, &count);
  if (ierr==0) printf("links %d\n", count);

  ierr= ENR_getNetSize(addr, ENR_pumpCount, &count);
  if (ierr==0) printf("pumps %d\n", count);

  ierr= ENR_getNetSize(addr, ENR_valveCount, &count);
  if (ierr==0) printf("valves %d\n", count);
  
  ENR_getTimes(addr, ENR_numPeriods, &max);
  ENR_getNodeID(addr, idx, nodeID);
  printf("\n\nHead at node index=%d, ID=%s\n", idx, nodeID);
  for(i = 1; i <= max; i++)
       if ( ENR_getNodeValue(addr,  i, idx,
                              ENR_head , &value)==0)
  	printf("%f ", value);

  printf("\n\n");

  // at the end politely close file
  ierr= ENR_close(&addr);
  if (ierr!=0) {
    printf("close failed!\n");
    return 1;
    }

  return 0;
}