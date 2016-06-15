//-----------------------------------------------------------------------------
//
//   outputapi.c -- API for reading results from EPANet binary output file
//
//   Version:    0.10
//   Date:       08/05/14
//   Date:       05/21/14
//
//   Author:     Michael E. Tryby
//               US EPA - NRMRL
//   Modified:   Maurizio Cingi
//               university of Modena 
//
//   Purpose: Output API provides an interface for retrieving results from
//   an EPANet binary output file.
//
//-----------------------------------------------------------------------------

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include "outputapi.h"
#include "messages.h"

#define INT4  int
#define REAL4 float
#define INTSIZE 4         // integers and reals not always
#define REALSIZE 4        // have same size, couldbe int & double?
#define MEMCHECK(x)  (((x) == NULL) ? 411 : 0 )
#define MAGICNUMBER        516114521


struct ENResultsAPI {
    char name[MAXFNAME + 1];     // file path/name
    FILE *file;                  // FILE structure pointer
    // only meaning for address calculation are loaded and stored
    // meaningless will be read on demand
    INT4 nodeCount, tankCount, linkCount, pumpCount, nPeriods;
    INT4 outputStartPos;         // starting file position of output data
    INT4 bytesPerPeriod;         // bytes saved per simulation time period
};

//-----------------------------------------------------------------------------
//   Local functions
//-----------------------------------------------------------------------------
float  getNodeValue(ENResultsAPI*, int, int, ENR_NodeAttribute);
float  getLinkValue(ENResultsAPI*, int, int, ENR_LinkAttribute);



int DLLEXPORT ENR_open(ENResultsAPI* *penrapi, const char* path)
/*------------------------------------------------------------------------
**   Input:   path
**   Output:  penrapi = pointer to ENResultsAPI struct
**  Returns:  error code
**  Purpose:  Allocate ENResultsAPI struc, open the output binary file and
**            read epilogue
**  NOTE: ENR_open must be called before any other ENR_* functions
**        no need to allocate ENResultsAPI struc before calling
**-------------------------------------------------------------------------
*/
{
    int magic, bytecount;
    ENResultsAPI* enrapi;

    enrapi= malloc(sizeof(struct ENResultsAPI));
    *penrapi= enrapi;
    strncpy(enrapi->name, path, MAXFNAME);

    // Attempt to open binary output file for reading only
    if ((enrapi->file = fopen(path, "rb")) == NULL) {
        ENR_close( penrapi);
        return 434;
    }
    // read magic and check magic number from START of file
    fseek(enrapi->file, 0L, SEEK_SET);
    fread(&magic, INTSIZE, 1, enrapi->file);  // rec #00
    if (magic != MAGICNUMBER ) {
        ENR_close( penrapi);
        return 436;
    }
    // read magic and check magic number from END of file
    fseek(enrapi->file, -1*INTSIZE, SEEK_END);
    fread(&magic, INTSIZE, 1, enrapi->file);
    if (magic != MAGICNUMBER ) {
        ENR_close( penrapi);
        return 436;
    }

    // read network size
    fseek(enrapi->file, 2*INTSIZE, SEEK_SET);
    fread(&(enrapi->nodeCount), INTSIZE, 1, enrapi->file);   // rec #02
    fread(&(enrapi->tankCount), INTSIZE, 1, enrapi->file);   // rec #03
    fread(&(enrapi->linkCount), INTSIZE, 1, enrapi->file);   // rec #04
    fread(&(enrapi->pumpCount), INTSIZE, 1, enrapi->file);   // rec #05
    
    // read nPeriods from file epilogue
    fseek(enrapi->file, -3*INTSIZE, SEEK_END);
    fread(&(enrapi->nPeriods), INTSIZE, 1, enrapi->file);


    // Compute positions and offsets for retrieving data
    bytecount = 15*INTSIZE;            // 15 integer values
    bytecount+= MAXTITLE*(MAXMSG+1);   //title
    bytecount+= 2*(MAXFNAME+1);        //filenames
    bytecount+= 2*(MAXID+1);           //ChemName QUALITY.Units
    bytecount+= enrapi->nodeCount*(MAXID+1);  //nodenames
    bytecount+= enrapi->linkCount*(MAXID+1);  //linknames
    bytecount+= enrapi->linkCount*INTSIZE* 3; //N1, N2, Type
    bytecount+= enrapi->tankCount*(INTSIZE+ REALSIZE); // Tank[i].Node+ Tank[i].A
    bytecount+= enrapi->nodeCount*(REALSIZE);  //node elevations
    bytecount+= enrapi->linkCount* REALSIZE*2; //link lengths & diameters
    bytecount+= enrapi->pumpCount* REALSIZE* 7+ REALSIZE; //energy section
    enrapi->outputStartPos= bytecount;

    /* old  outputStartPos calculation:
    enrapi->outputStartPos  = 884;
    enrapi->outputStartPos += 32*enrapi->nodeCount + 32*enrapi->linkCount;
    enrapi->outputStartPos += 12*enrapi->linkCount+ 8*enrapi->tankCount
    		+ 4*enrapi->nodeCount + 8*enrapi->linkCount;
    enrapi->outputStartPos += 28*enrapi->pumpCount + 4;  */

    enrapi->bytesPerPeriod = NNODERESULTS*REALSIZE*enrapi->nodeCount +
                             NLINKRESULTS*REALSIZE*enrapi->linkCount;

    return 0;
}

int DLLEXPORT ENR_close(ENResultsAPI **enrapi)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**  Returns:  error code
**  Purpose:  Close the output binary file, dellocate ENResultsAPI struc
**            and nullify pointer to ENResultsAPI struct
**  NOTE: ENR_close must be called before program end
**        after calling ENR_close data in  ENResultsAPI struct are no more 
**        accessible
**-------------------------------------------------------------------------
*/
{   if ((*enrapi)!=NULL) {
        // avoid fclose(NULL)-> crash with Linux gcc (segmentation fault)
        if ((*enrapi)->file != NULL) 
	   fclose( (*enrapi)->file);
        free(*enrapi);
        *enrapi = NULL;
        return 0;
    }
    // Error binary file not opened
    else return 412;

    return 1;
}


int DLLEXPORT ENR_getEnVersion(ENResultsAPI* enrapi, int* version)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**   Output:  version  Epanet version
**  Returns: error code
**  Purpose: Returns Epanet version that wrote EBOFile
**
**--------------element codes-------------------------------------------
*/
{       if (enrapi==NULL) return 412;
	fseek(enrapi->file, 1*INTSIZE, SEEK_SET);
	if (fread(version, INTSIZE, 1, enrapi->file)==1) return 0;
	else return 436;
}


int DLLEXPORT ENR_getWarningCode(ENResultsAPI* enrapi, int* warncode)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**   Output:  warncode
**  Returns: error code
**  Purpose: Returns if warnings were generated during EN run
**--------------warncode       -------------------------------------------
**  0 = No warning
**  1 = Warning
**--------------element codes-------------------------------------------
*/
{       if (enrapi==NULL) return 412;
	fseek(enrapi->file, -2*INTSIZE, SEEK_END);
	if (fread(warncode, INTSIZE, 1, enrapi->file)==1) return 0;
	else return 436;
}







int DLLEXPORT ENR_getNetSize(ENResultsAPI* enrapi, ENR_ElementCount code, int* count)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**            code=  element code
**   Output:  count
**  Returns: error code                              
**  Purpose: Returns count of elements  of given kind
**
**--------------element codes-------------------------------------------
**  ENR_nodeCount  = 1
**  ENR_tankCount  = 2
**  ENR_linkCount  = 3
**  ENR_pumpCount  = 4
**  ENR_valveCount = 5
**-------------------------------------------------------------------------
*/
{
    *count = -1;
    if (enrapi==NULL) return 412;
    switch (code)
        {
        case ENR_nodeCount:    *count = enrapi->nodeCount;  break;
        case ENR_tankCount:    *count = enrapi->tankCount;  break;
        case ENR_linkCount:    *count = enrapi->linkCount;  break;
        case ENR_pumpCount:    *count = enrapi->pumpCount;  break;
	case ENR_valveCount:   
            fseek(enrapi->file, 6*INTSIZE, SEEK_SET);
            fread(count, INTSIZE, 1, enrapi->file);  // rec #06
            break;
        default: return 421;
        }
        return 0;
}

int DLLEXPORT ENR_getUnits(ENResultsAPI* enrapi, ENR_Unit code, int* unitFlag)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**            code
**   Output:  count
**  Returns: unitFlag
**  Purpose: Returns pressure or flow unit flag
**
**------------------------ codes-------------------------------------------
**  ENR_flowUnits   = 1
**  ENR_pressUnits  = 2
**--------------pressure unit flags----------------------------------------
**  0 = psi
**  1 = meters
**  2 = kPa
**------------------flow unit flags----------------------------------------
**  0 = cubic feet/second
**  1 = gallons/minute
**  2 = million gallons/day
**  3 = Imperial million gallons/day
**  4 = acre-ft/day
**  5 = liters/second
**  6 = liters/minute
**  7 = megaliters/day
**  8 = cubic meters/hour
**  9 = cubic meters/day
**-------------------------------------------------------------------------
*/
{
    *unitFlag = -1;
    if (enrapi==NULL) return 412;
    switch (code)
        {
        case ENR_flowUnits:   
           fseek(enrapi->file, 9*INTSIZE, SEEK_SET);
           fread(unitFlag, INTSIZE, 1, enrapi->file);    // rec #09
           //  *unitFlag = enrapi->flowFlag;
	   break;
        case ENR_pressUnits:  
           fseek(enrapi->file, 10*INTSIZE, SEEK_SET);
           fread(unitFlag, INTSIZE, 1, enrapi->file);    // rec #10
	   //*unitFlag = enrapi->pressFlag;
	   break;
        default: return 421;
        }
        return 0;
}

int DLLEXPORT ENR_getTimes(ENResultsAPI* enrapi, ENR_Time code, int* time)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**            code=  element code
**   Output:  time
**  Returns: error code                              
**  Purpose: Returns report and simulation time related parameters.
**
**--------------element codes-------------------------------------------
**  ENR_reportStart = 1
**  ENR_reportStep  = 2
**  ENR_simDuration = 3
**  ENR_numPeriods  = 4
**-------------------------------------------------------------------------
*/
{
    *time = -1;
    if (enrapi!=NULL) {
        switch (code)
        {
        case ENR_reportStart:
            fseek(enrapi->file, 12*INTSIZE, SEEK_SET);
            fread(time, INTSIZE, 1, enrapi->file);
	    break;
        case ENR_reportStep:
            fseek(enrapi->file, 13*INTSIZE, SEEK_SET);
            fread(time, INTSIZE, 1, enrapi->file);
	    break;
        case ENR_simDuration: 
            fseek(enrapi->file, 14*INTSIZE, SEEK_SET);
            fread(time, INTSIZE, 1, enrapi->file);
	    break;
        case ENR_numPeriods:  
	   *time = enrapi->nPeriods;     
	   break;
        default: return 421;
        }
        return 0;
    }
    return 412;
}


int DLLEXPORT ENR_getNodeID(ENResultsAPI* enrapi, int nodeIndex, char* id)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**            nodeIndex from 0 to nodeCount-1
**   Output:  id = nodeID
**  Returns: error code
**  Purpose: Retrieves ID of a specified node
**  NOTE: 'id' must be able to hold MAXID characters
**-------------------------------------------------------------------------
*/
{
    int offset;
    if (enrapi==NULL) return 412;
    // calculate byte offset
    offset= 15*INTSIZE+3*(MAXMSG+1)+2*(MAXFNAME+1)+ 2*(MAXID+1);
    offset+= nodeIndex* (MAXID+1);

    fseek(enrapi->file, offset, SEEK_SET);
    fread(id, 1, MAXID+1, enrapi->file);
    return 0;
}

int DLLEXPORT ENR_getLinkID(ENResultsAPI* enrapi, int linkIndex, char* id)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**            linkIndex from 0 to linkCount-1
**   Output:  id = linkID
**  Returns: error code
**  Purpose: Retrieves ID of a specified link
**  NOTE: 'id' must be able to hold MAXID characters
**-------------------------------------------------------------------------
*/
{
    int offset;
    if (enrapi==NULL) return 412;
    // calculate byte offset
    offset= 15*INTSIZE+3*(MAXMSG+1)+2*(MAXFNAME+1)+ 2*(MAXID+1)+
            enrapi->nodeCount* (MAXID+1);
    offset+= linkIndex* (MAXID+1);

    fseek(enrapi->file, offset, SEEK_SET);
    fread(id, 1, MAXID+1, enrapi->file);
    return 0;
}




int DLLEXPORT ENR_getNodeValue(ENResultsAPI* enrapi, int timeIndex, int nodeIndex, ENR_NodeAttribute attr, float *value)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**            nodeIndex from 0 to nodeCount-1
**            timeIndex from 0 to nPeriods-1
**            attr = attribute code
**   Output:  value=
**  Returns: error code                              
**  Purpose: Returns attribute for a node at given time
**
**--------------attribute codes-------------------------------------------
**  ENR_demand   = 0
**  ENR_head     = 1 
**  ENR_pressure = 2 
**  ENR_quality  = 3
**-------------------------------------------------------------------------
*/
{   int offset;
    if (enrapi==NULL) return 412;

    if ( 0 >  timeIndex | timeIndex >=enrapi->nPeriods ) return 437;
    if ( 0 >  nodeIndex | nodeIndex >=enrapi->nodeCount ) return 438;
    // calculate byte offset to start time for series
    offset = enrapi->outputStartPos + timeIndex* enrapi->bytesPerPeriod;
    // add bytepos for node and attribute
    offset += (nodeIndex + attr*enrapi->nodeCount)*REALSIZE;
    fseek(enrapi->file, offset, SEEK_SET);
    if (fread(value, REALSIZE, 1, enrapi->file)!= 1) return 440;
    return 0;
}

int DLLEXPORT ENR_getLinkValue(ENResultsAPI* enrapi, int timeIndex, int linkIndex, ENR_LinkAttribute attr, float *value)
/*------------------------------------------------------------------------
**   Input:   enrapi = pointer to ENResultsAPI struct
**            linkIndex from 0 to linkCount-1
**            timeIndex from 0 to nPeriods-1
**            attr = attribute code
**   Output:  value=
**  Returns: error code
**  Purpose: Returns attribute for a link at given time
**
**--------------attribute codes-------------------------------------------
**  ENR_flow         = 0
**  ENR_velocity     = 1
**  ENR_headloss     = 2
**  ENR_avgQuality   = 3
**  ENR_status       = 4
**  ENR_setting      = 5
**  ENR_rxRate       = 6
**  ENR_frctnFctr    = 7
**-------------------------------------------------------------------------
*/
{   
    int offset;
    if (enrapi==NULL) return 412;
    if ( 0 >  timeIndex | timeIndex >=enrapi->nPeriods ) return 437;
    if ( 0 >  linkIndex | linkIndex >=enrapi->linkCount ) return 439;
    // Calculate byte offset to start time for series
    offset = enrapi->outputStartPos + timeIndex*enrapi->bytesPerPeriod
            + (NNODERESULTS*enrapi->nodeCount)*REALSIZE;
    // add bytepos for link and attribute
    offset += (linkIndex + attr*enrapi->linkCount)*REALSIZE;
    fseek(enrapi->file, offset, SEEK_SET);
    if (fread(value, REALSIZE, 1, enrapi->file)!= 1) return 440;
    return 0;
}



/* -----------------------------------------------------------------------------

   from this point (near) untouched code

-------------------------------------------------------------------------------*/






float* ENR_newOutValueSeries(ENResultsAPI* enrapi, int seriesStart,
        int seriesLength, int* length, int* errcode)
//
//  Purpose: Allocates memory for outValue Series.
//
//  Warning: Caller must free memory allocated by this function using ENR_free().
//
{
    int size;
    float* array;

    if (enrapi!=NULL) {

        size = seriesLength - seriesStart;
        if (size > enrapi->nPeriods)
            size = enrapi->nPeriods;

        // Allocate memory for outValues
        array = (float*) calloc(size + 1, sizeof(float));
        *errcode = (MEMCHECK(array));

        *length = size;
        return array;
    }
    *errcode = 412;
    return NULL;
}

float* ENR_newOutValueArray(ENResultsAPI* enrapi, ENR_ApiFunction func,
        ENR_ElementType type, int* length, int* errcode)
//
//  Purpose: Allocates memory for outValue Array.
//
//  Warning: Caller must free memory allocated by this function using ENR_free().
//
{
    int size;
    float* array;

    if (enrapi!=NULL) {
        switch (func)
        {
        case ENR_getAttribute:
            if (type == ENR_node)
                size = enrapi->nodeCount;
            else
                size = enrapi->linkCount;
            break;
        case ENR_getResult:
            if (type == ENR_node)
                size = NNODERESULTS;
            else
                size = NLINKRESULTS;
            break;
        default: *errcode = 421;
                 return NULL;
        }

        // Allocate memory for outValues
        array = (float*) calloc(size, sizeof(float));
        *errcode = (MEMCHECK(array));

        *length = size;
        return array;
    }
    *errcode = 412;
    return NULL;
}


int DLLEXPORT ENR_getNodeSeries(ENResultsAPI* enrapi, int nodeIndex, ENR_NodeAttribute attr,
        int seriesStart, int seriesLength, float* outValueSeries)
//
//  What if timeIndex 0? length 0?  removed   unused  int* length
//
//  Purpose: Get time series results for particular attribute. Specify series
//  start and length using seriesStart and seriesLength respectively.
//
{
    int k;

    if (enrapi!=NULL) {

        // Check memory for outValues
        if (outValueSeries == NULL) return 411;

        // loop over and build time series
        for (k = 0; k <= seriesLength; k++)
            outValueSeries[k] = getNodeValue(enrapi, seriesStart + 1 + k,
            		nodeIndex, attr);

        return 0;
    }
    // Error no results to report on binary file not opened
    return 412;
}

int DLLEXPORT ENR_getLinkSeries(ENResultsAPI* enrapi, int linkIndex, ENR_LinkAttribute attr,
        int seriesStart, int seriesLength, float* outValueSeries)
//
//  What if timeIndex 0? length 0?
//
//  Purpose: Get time series results for particular attribute. Specify series
//  start and length using seriesStart and seriesLength respectively.
//
{
    int k;

    if (enrapi!=NULL) {
        // Check memory for outValues
        if (outValueSeries == NULL) return 411;

        // loop over and build time series
        for (k = 0; k <= seriesLength; k++)
            outValueSeries[k] = getLinkValue(enrapi, seriesStart +1 + k,
            		linkIndex, attr);

        return 0;
    }
    // Error no results to report on binary file not opened
    return 412;
}


int DLLEXPORT ENR_getNodeAttribute(ENResultsAPI* enrapi, int timeIndex,
        ENR_NodeAttribute attr, float* outValueArray)
//
//   Purpose: For all nodes at given time, get a particular attribute
//
{
    INT4 offset;

    if (enrapi!=NULL) {
        // Check memory for outValues
        if (outValueArray == NULL) return 411;

        // calculate byte offset to start time for series
        offset = enrapi->outputStartPos + (timeIndex)*enrapi->bytesPerPeriod;
        // add offset for node and attribute
        offset += (attr*enrapi->nodeCount)*REALSIZE;

        fseek(enrapi->file, offset, SEEK_SET);
        fread(outValueArray, REALSIZE, enrapi->nodeCount, enrapi->file);

        return 0;
    }
    // Error no results to report on binary file not opened
    return 412;
}

int DLLEXPORT ENR_getLinkAttribute(ENResultsAPI* enrapi, int timeIndex,
        ENR_LinkAttribute attr, float* outValueArray)
//
//   Purpose: For all links at given time, get a particular attribute
//
{
    INT4 offset;

    if (enrapi!=NULL) {
        // Check memory for outValues
        if (outValueArray == NULL) return 411;

        // calculate byte offset to start time for series
        offset = enrapi->outputStartPos + (timeIndex)*enrapi->bytesPerPeriod
                + (NNODERESULTS*enrapi->nodeCount)*REALSIZE;
        // add offset for link and attribute
        offset += (attr*enrapi->linkCount)*REALSIZE;

        fseek(enrapi->file, offset, SEEK_SET);
        fread(outValueArray, REALSIZE, enrapi->linkCount, enrapi->file);

        return 0;
    }
    // Error no results to report on binary file not opened
    return 412;
}

int DLLEXPORT ENR_getNodeResult(ENResultsAPI* enrapi, int timeIndex, int nodeIndex,
        float* outValueArray)
//
//   Purpose: For a node at given time, get all attributes
//
{
    int j;

    if (enrapi!=NULL) {
        // Check memory for outValues
        if (outValueArray == NULL) return 411;

        for (j = 0; j < NNODERESULTS; j++)
            outValueArray[j] = getNodeValue(enrapi, timeIndex + 1, nodeIndex, j);

        return 0;
    }
    // Error no results to report on binary file not opened
    return 412;
}

int DLLEXPORT ENR_getLinkResult(ENResultsAPI* enrapi, int timeIndex, int linkIndex,
        float* outValueArray)
//
//   Purpose: For a link at given time, get all attributes
//
{
    int j;

    if (enrapi!=NULL) {
        // Check memory for outValues
        if (outValueArray == NULL) return 411;

        for (j = 0; j < NLINKRESULTS; j++)
            outValueArray[j] = getLinkValue(enrapi, timeIndex + 1, linkIndex, j);

        return 0;
    }
    // Error no results to report on binary file not opened
    return 412;
}

int DLLEXPORT ENR_free(float* array)
//
//  Purpose: frees memory allocated using ENR_newOutValueSeries() or
//  ENR_newOutValueArray()
//
{
	if (array != NULL)
		free(array);

	return 0;
}




int DLLEXPORT ENR_errMessage(int errcode, char* errmsg, int n)
//
//  Purpose: takes error code returns error message
//
{
    switch (errcode)
    {
    case 411: strncpy(errmsg, ERR411, n); break;
    case 412: strncpy(errmsg, ERR412, n); break;
    case 421: strncpy(errmsg, ERR421, n); break;
    case 434: strncpy(errmsg, ERR434, n); break;
    case 435: strncpy(errmsg, ERR435, n); break;
    case 436: strncpy(errmsg, ERR436, n); break;
    case 437: strncpy(errmsg, ERR437, n); break;
    case 438: strncpy(errmsg, ERR438, n); break;
    case 439: strncpy(errmsg, ERR439, n); break;
    default: return 421;
    }

    return 0;
}






float  getNodeValue(ENResultsAPI* enrapi, int timeIndex, int nodeIndex,
	        	ENR_NodeAttribute attr)
//
//   Purpose: Retrieves an attribute value at a specified node and time
//
{
    REAL4 y;
    INT4  offset;

    // calculate byte offset to start time for series
    offset = enrapi->outputStartPos + (timeIndex - 1)*enrapi->bytesPerPeriod;
    // add bytepos for node and attribute
    offset += (nodeIndex + attr*enrapi->nodeCount)*REALSIZE;

    fseek(enrapi->file, offset, SEEK_SET);
    fread(&y, REALSIZE, 1, enrapi->file);

    return y;
}

float getLinkValue(ENResultsAPI* enrapi, int timeIndex, int linkIndex,
        ENR_LinkAttribute attr)
//
//   Purpose: Retrieves an attribute value at a specified link and time
//
{
    REAL4 y;
    INT4  offset;

    // Calculate byte offset to start time for series
    offset = enrapi->outputStartPos + (timeIndex - 1)*enrapi->bytesPerPeriod
            + (NNODERESULTS*enrapi->nodeCount)*REALSIZE;
    // add bytepos for link and attribute
    offset += (linkIndex + attr*enrapi->linkCount)*REALSIZE;

    fseek(enrapi->file, offset, SEEK_SET);
    fread(&y, REALSIZE, 1, enrapi->file);

    return y;
}
