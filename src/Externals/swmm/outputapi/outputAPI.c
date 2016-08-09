/*
* outputAPI.c
*
*      Author: Colleen Barr
*
*/

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include "outputAPI.h"

#define MEMCHECK(x)  (((x) == NULL) ? 411 : 0 )

static const int RECORDSIZE = 4;       // number of bytes per file record

//-----------------------------------------------------------------------------
//  Shared variables
//-----------------------------------------------------------------------------

struct SMOutputAPI {
	char name[MAXFNAME + 1];           // file path/name
	bool isOpened;                     // current state (CLOSED = 0, OPEN = 1)
	FILE* file;                        // FILE structure pointer

	int Nperiods;                      // number of reporting periods
	int FlowUnits;                     // flow units code

	int Nsubcatch;                     // number of subcatchments
	int Nnodes;                        // number of drainage system nodes
	int Nlinks;                        // number of drainage system links
	int Npolluts;                      // number of pollutants tracked

	int SubcatchVars;                  // number of subcatch reporting variables
	int NodeVars;                      // number of node reporting variables
	int LinkVars;                      // number of link reporting variables
	int SysVars;                       // number of system reporting variables

	double StartDate;                  // start date of simulation
	int    ReportStep;                 // reporting time step (seconds)

	int IDPos;					       // file position where object ID names start
	int ObjPropPos;					   // file position where object properties start
	int ResultsPos;                    // file position where results start
	int BytesPerPeriod;                // bytes used for results in each period
};

//-----------------------------------------------------------------------------
//   Local functions
//-----------------------------------------------------------------------------
double getTimeValue(SMOutputAPI* smoapi, int timeIndex);
float getSubcatchValue(SMOutputAPI* smoapi, int timeIndex, int subcatchIndex,
	SMO_subcatchAttribute attr);
float getNodeValue(SMOutputAPI* smoapi, int timeIndex, int nodeIndex, SMO_nodeAttribute attr);
float getLinkValue(SMOutputAPI* smoapi, int timeIndex, int linkIndex, SMO_linkAttribute attr);
float getSystemValue(SMOutputAPI* smoapi, int timeIndex, SMO_systemAttribute attr);

void AddIDentry(struct IDentry* head, char* idname, int numChar);

int SMR_open(const char* path, SMOutputAPI** smoapi)
//
//  Purpose: Open the output binary file and read epilogue.
//
{
	int magic1, magic2, errCode, offset, version;
	int err;

	*smoapi = malloc(sizeof(SMOutputAPI));

	strncpy((*smoapi)->name, path, MAXFNAME);
	(*smoapi)->isOpened = false;

	// --- open the output file
	if (((*smoapi)->file = fopen(path, "rb")) == NULL)
		return 434;
	else
		(*smoapi)->isOpened = true;

	// --- check that file contains at least 14 records
	fseek((*smoapi)->file, 0L, SEEK_END);
	if (ftell((*smoapi)->file) < 14 * RECORDSIZE) {
		fclose((*smoapi)->file);
		return 435;
	}

	// --- read parameters from end of file
	fseek((*smoapi)->file, -6 * RECORDSIZE, SEEK_END);
	fread(&((*smoapi)->IDPos), RECORDSIZE, 1, (*smoapi)->file);
	fread(&((*smoapi)->ObjPropPos), RECORDSIZE, 1, (*smoapi)->file);
	fread(&((*smoapi)->ResultsPos), RECORDSIZE, 1, (*smoapi)->file);
	fread(&((*smoapi)->Nperiods), RECORDSIZE, 1, (*smoapi)->file);
	fread(&errCode, RECORDSIZE, 1, (*smoapi)->file);
	fread(&magic2, RECORDSIZE, 1, (*smoapi)->file);

	// --- read magic number from beginning of file
	fseek((*smoapi)->file, 0L, SEEK_SET);
	fread(&magic1, RECORDSIZE, 1, (*smoapi)->file);

	// --- perform error checks
	if (magic1 != magic2) err = 435;
	else if (errCode != 0) err = 435;
	else if ((*smoapi)->Nperiods == 0) err = 435;
	else err = 0;

	// --- quit if errors found
	if (err > 0)
	{
		fclose((*smoapi)->file);
		(*smoapi)->file = NULL;
		return err;
	}

	// --- otherwise read additional parameters from start of file
	fread(&version, RECORDSIZE, 1, (*smoapi)->file);
	fread(&((*smoapi)->FlowUnits), RECORDSIZE, 1, (*smoapi)->file);
	fread(&((*smoapi)->Nsubcatch), RECORDSIZE, 1, (*smoapi)->file);
	fread(&((*smoapi)->Nnodes), RECORDSIZE, 1, (*smoapi)->file);
	fread(&((*smoapi)->Nlinks), RECORDSIZE, 1, (*smoapi)->file);
	fread(&((*smoapi)->Npolluts), RECORDSIZE, 1, (*smoapi)->file);

	// Skip over saved subcatch/node/link input values
		offset = ((*smoapi)->Nsubcatch + 2) * RECORDSIZE  // Subcatchment area
		+ (3 * (*smoapi)->Nnodes + 4) * RECORDSIZE  // Node type, invert & max depth
		+ (5 * (*smoapi)->Nlinks + 6) * RECORDSIZE; // Link type, z1, z2, max depth & length
	offset = (*smoapi)->ObjPropPos + offset;
	fseek((*smoapi)->file, offset, SEEK_SET);

	// Read number & codes of computed variables
	fread(&((*smoapi)->SubcatchVars), RECORDSIZE, 1, (*smoapi)->file); // # Subcatch variables
	fseek((*smoapi)->file, (*smoapi)->SubcatchVars*RECORDSIZE, SEEK_CUR);
	fread(&((*smoapi)->NodeVars), RECORDSIZE, 1, (*smoapi)->file);     // # Node variables
	fseek((*smoapi)->file, (*smoapi)->NodeVars*RECORDSIZE, SEEK_CUR);
	fread(&((*smoapi)->LinkVars), RECORDSIZE, 1, (*smoapi)->file);     // # Link variables
	fseek((*smoapi)->file, (*smoapi)->LinkVars*RECORDSIZE, SEEK_CUR);
	fread(&((*smoapi)->SysVars), RECORDSIZE, 1, (*smoapi)->file);     // # System variables

	// --- read data just before start of output results
	offset = (*smoapi)->ResultsPos - 3 * RECORDSIZE;
	fseek((*smoapi)->file, offset, SEEK_SET);
	fread(&((*smoapi)->StartDate), sizeof(double), 1, (*smoapi)->file);
	fread(&((*smoapi)->ReportStep), RECORDSIZE, 1, (*smoapi)->file);

	// --- compute number of bytes of results values used per time period
	(*smoapi)->BytesPerPeriod = 2 * RECORDSIZE +      // date value (a double)
		((*smoapi)->Nsubcatch*(*smoapi)->SubcatchVars +
		(*smoapi)->Nnodes*(*smoapi)->NodeVars +
		(*smoapi)->Nlinks*(*smoapi)->LinkVars +
		(*smoapi)->SysVars)*RECORDSIZE;

	// --- return with file left open
	return err;

}


int SMO_getProjectSize(SMOutputAPI* smoapi, SMO_elementCount code, int* count)
//
//   Purpose: Returns project size.
// 
{
	*count = -1;
	if (smoapi->isOpened) 
	{
		switch (code)
		{
		case subcatchCount:		*count = smoapi->Nsubcatch;	break;
		case nodeCount:			*count = smoapi->Nnodes;	break;
		case linkCount:			*count = smoapi->Nlinks;	break;
		case pollutantCount:	*count = smoapi->Npolluts;	break;
		default: return 421;
		}
		return 0;
	}
	return 412;
}


int SMO_getUnits(SMOutputAPI* smoapi, SMO_unit code, int* unitFlag)
//
//   Purpose: Returns flow rate units.
//
{
	*unitFlag = -1;
	if (smoapi->isOpened) 
	{
		switch (code)
		{
		case flow_rate:			*unitFlag = smoapi->FlowUnits; break;
			//		case concentration:		*unitFlag = ConcUnits; break;
		default: return 421;
		}
		return 0;
	}
	return 412;
}


int SMO_getPollutantUnits(SMOutputAPI* smoapi, int pollutantIndex, int* unitFlag)
//
//   Purpose: Return integer flag representing the units that the given pollutant is measured in.
//	          Concentration units are located after the pollutant ID names and before the object properties start,
//			  and are stored for each pollutant.  They're stored as 4-byte integers with the following codes:
//		          0: mg/L
//				  1: ug/L
//				  2: count/L
//
//   pollutantIndex: valid values are 0..Npolluts-1
{
	if (smoapi->isOpened)
	{
	    if (pollutantIndex < 0 || pollutantIndex >= smoapi->Npolluts)
	        return 421;
        int offset = smoapi->ObjPropPos - (smoapi->Npolluts - pollutantIndex) * RECORDSIZE;
        fseek(smoapi->file, offset, SEEK_SET);
        fread(unitFlag, RECORDSIZE, 1, smoapi->file);
		return 0;
	}
	return 412;
}

int SMO_getStartTime(SMOutputAPI* smoapi, double* time)
//
//	Purpose: Returns start date.
//
{
	*time = -1;
	if (smoapi->isOpened)
	{
		*time = smoapi->StartDate;
		return 0;
	}
	return 412;
}


int SMO_getTimes(SMOutputAPI* smoapi, SMO_time code, int* time)
//
//   Purpose: Returns step size and number of periods.
//
{
	*time = -1;
	if (smoapi->isOpened) 
	{
		switch (code)
		{
		case reportStep:  *time = smoapi->ReportStep;   break;
		case numPeriods:  *time = smoapi->Nperiods;     break;
		default: return 421;
		}
		return 0;
	}
	return 412;
}


void AddIDentry(struct IDentry* head, char* idname, int numChar)
//
//	Purpose: add ID to linked list (can't be used for first entry).
//
{
	idEntry* current = head;
	while (current->nextID != NULL)
	{
		current = current->nextID;
	}

	current->nextID = malloc(sizeof(idEntry));

	current->nextID->IDname = calloc(numChar + 1, sizeof(char));
	strcpy(current->nextID->IDname, idname);

	current->nextID->nextID = NULL;
}

struct IDentry* SMO_getSubcatchIDs(SMOutputAPI* smoapi, int *errcode)
//
//	 Purpose: Get subcatchment IDs. 
//
//   Warning: Caller must free memory allocated by this function using SMO_free_list
//
//	 Note:	  The number of characters of each ID can vary and is stored in the binary file before each ID
//			  No null characters or spaces are used to separate the IDs or number of characters
//
{
	int arraySize = (smoapi->Nsubcatch); 
	int* numChar = (int*)calloc(arraySize, RECORDSIZE);
	int stringSize = 0;
	int i;

	char *idname;

	idEntry* head = NULL;

	if (arraySize == 0)
	{
		free(numChar);
		*errcode = 411;
		return head;
	}

	if (smoapi->isOpened)
	{
		head = (idEntry*)malloc(sizeof(idEntry));

		rewind(smoapi->file);
		fseek(smoapi->file, smoapi->IDPos, SEEK_SET);

		fread(&numChar[0], RECORDSIZE, 1, smoapi->file);
		idname = calloc(numChar[0] + 1, sizeof(char));
		fread(idname, sizeof(char), numChar[0], smoapi->file);

		head[0].IDname = calloc(numChar[0] + 1, sizeof(char));
		strcpy(head[0].IDname, idname);
		(*head).nextID = NULL;

		free(idname);

		for (i = 1; i < arraySize; i++)
		{
			fread(&numChar[i], RECORDSIZE, 1, smoapi->file);
			idname = calloc(numChar[i] + 1, sizeof(char));
			fread(idname, sizeof(char), numChar[i], smoapi->file);
			AddIDentry(head, idname, numChar[i]);
			free(idname);
		}

		free(numChar);

		*errcode = 0;
		return head;
	}

	*errcode = 412;
	return head;
}

struct IDentry* SMO_getNodeIDs(SMOutputAPI* smoapi, int* errcode)
//
//	 Purpose: Get node IDs. 
//
//   Warning: Caller must free memory allocated by this function using SMO_free_list
//
{
	int arraySize = (smoapi->Nnodes);
	int* numChar = (int*)calloc(arraySize, RECORDSIZE);
	int stringSize = 0;
	int i;

	char *idname;

	idEntry* head = NULL;

	// new
	int fwdSize = smoapi->Nsubcatch;
	int* fwdNumChar = (int*)calloc(fwdSize, RECORDSIZE);

	if (arraySize == 0)
	{
		free(fwdNumChar);
		free(numChar);
		*errcode = 411;
		return head;
	}

	if (smoapi->isOpened)
	{
		head = (idEntry*)malloc(sizeof(idEntry));
		rewind(smoapi->file);
		fseek(smoapi->file, smoapi->IDPos, SEEK_SET);

		// fast forward through subcatchment IDs
		for (i = 0; i < fwdSize; i++)
		{
			fread(&fwdNumChar[i], RECORDSIZE, 1, smoapi->file);
			fseek(smoapi->file, fwdNumChar[i], SEEK_CUR);
		}

		fread(&numChar[0], RECORDSIZE, 1, smoapi->file);
		idname = calloc(numChar[0] + 1, sizeof(char));
		fread(idname, sizeof(char), numChar[0], smoapi->file);

		head[0].IDname = calloc(numChar[0] + 1, sizeof(char));
		strcpy(head[0].IDname, idname);
		(*head).nextID = NULL;

		free(idname);

		for (i = 1; i < arraySize; i++)
		{
			fread(&numChar[i], RECORDSIZE, 1, smoapi->file);
			idname = calloc(numChar[i] + 1, sizeof(char));
			fread(idname, sizeof(char), numChar[i], smoapi->file);
			AddIDentry(head, idname, numChar[i]);
			free(idname);
		}

		free(fwdNumChar);
		free(numChar);

		*errcode = 0;
		return head;
	}

	*errcode = 412;
	return head;
}

struct IDentry* SMO_getLinkIDs(SMOutputAPI* smoapi, int* errcode)
//
//	 Purpose: Get link IDs. 
//
//   Warning: Caller must free memory allocated by this function using SMO_free_list
//
{
	int arraySize = (smoapi->Nlinks);
	int* numChar = (int*)calloc(arraySize, RECORDSIZE);
	int stringSize = 0;
	int i;

	char *idname;

	idEntry* head = NULL;

	// new
	int fwdSize = smoapi->Nsubcatch + smoapi->Nnodes;
	int* fwdNumChar = (int*)calloc(fwdSize, RECORDSIZE);

	if (arraySize == 0)
	{
		free(fwdNumChar);
		free(numChar);
		*errcode = 411;
		return head;
	}

	if (smoapi->isOpened)
	{
		head = (idEntry*)malloc(sizeof(idEntry));
		rewind(smoapi->file);
		fseek(smoapi->file, smoapi->IDPos, SEEK_SET);

		// fast forward through subcatchment and node IDs
		for (i = 0; i < fwdSize; i++)
		{
			fread(&fwdNumChar[i], RECORDSIZE, 1, smoapi->file);
			fseek(smoapi->file, fwdNumChar[i], SEEK_CUR);
		}

		fread(&numChar[0], RECORDSIZE, 1, smoapi->file);
		idname = calloc(numChar[0] + 1, sizeof(char));
		fread(idname, sizeof(char), numChar[0], smoapi->file);

		head[0].IDname = calloc(numChar[0] + 1, sizeof(char));
		strcpy(head[0].IDname, idname);
		(*head).nextID = NULL;

		free(idname);

		for (i = 1; i < arraySize; i++)
		{
			fread(&numChar[i], RECORDSIZE, 1, smoapi->file);
			idname = calloc(numChar[i] + 1, sizeof(char));
			fread(idname, sizeof(char), numChar[i], smoapi->file);
			AddIDentry(head, idname, numChar[i]);
			free(idname);
		}

		free(fwdNumChar);
		free(numChar);

		*errcode = 0;
		return head;
	}

	*errcode = 412;
	return head;
}


struct IDentry* SMO_getPollutIDs(SMOutputAPI* smoapi, int* errcode)
//
//	 Purpose: Get pollutant IDs. 
//
//   Warning: Caller must free memory allocated by this function using SMO_free_list
//
{
	int arraySize = (smoapi->Npolluts);
	int* numChar = (int*)calloc(arraySize, RECORDSIZE);
	int stringSize = 0;
	int i;

	char *idname;

	idEntry* head = NULL;

	// new
	int fwdSize = smoapi->Nsubcatch + smoapi->Nnodes + smoapi->Nlinks;
	int* fwdNumChar = (int*)calloc(fwdSize, RECORDSIZE);

	if (arraySize == 0)
	{
		free(fwdNumChar);
		free(numChar);
		*errcode = 411;
		return head;
	}

	if (smoapi->isOpened)
	{
		head = (idEntry*)malloc(sizeof(idEntry));

		rewind(smoapi->file);
		fseek(smoapi->file, smoapi->IDPos, SEEK_SET);

		// fast forward through subcatchment, node, and link IDs
		for (i = 0; i < fwdSize; i++)
		{
			fread(&fwdNumChar[i], RECORDSIZE, 1, smoapi->file);
			fseek(smoapi->file, fwdNumChar[i], SEEK_CUR);
		}

		fread(&numChar[0], RECORDSIZE, 1, smoapi->file);
		idname = calloc(numChar[0] + 1, sizeof(char));
		fread(idname, sizeof(char), numChar[0], smoapi->file);

		head[0].IDname = calloc(numChar[0] + 1, sizeof(char));
		strcpy(head[0].IDname, idname);
		(*head).nextID = NULL;

		free(idname);

		for (i = 1; i < arraySize; i++)
		{
			fread(&numChar[i], RECORDSIZE, 1, smoapi->file);
			idname = calloc(numChar[i] + 1, sizeof(char));
			fread(idname, sizeof(char), numChar[i], smoapi->file);
			AddIDentry(head, idname, numChar[i]);
			free(idname);
		}

		free(fwdNumChar);
		free(numChar);

		*errcode = 0;
		return head;
	}

	*errcode = 412;
	return head;
}




float* SMO_newOutValueSeries(SMOutputAPI* smoapi, int seriesStart,
	int seriesLength, int* length, int* errcode)
//
//  Purpose: Allocates memory for outValue Series.
//
//  Warning: Caller must free memory allocated by this function using SMO_free().
//
{
	int size;
	float* array;

	if (smoapi->isOpened) 
	{
		size = seriesLength - seriesStart;
		if (size > smoapi->Nperiods)
			size = smoapi->Nperiods;

		array = (float*)calloc(size, sizeof(float));
		*errcode = (MEMCHECK(array));

		*length = size;
		return array;
	}
	*errcode = 412;
	return NULL;
}


float* SMO_newOutValueArray(SMOutputAPI* smoapi, SMO_apiFunction func,
	SMO_elementType type, int* length, int* errcode)
//
// Purpose: Allocates memory for outValue Array.
//
//  Warning: Caller must free memory allocated by this function using SMO_free().
//
{
	int size;
	float* array;

	if (smoapi->isOpened) 
	{
		switch (func)
		{
		case getAttribute:
			if (type == subcatch)
				size = smoapi->Nsubcatch;
			else if (type == node)
				size = smoapi->Nnodes;
			else if (type == link)
				size = smoapi->Nlinks;
			else // system
				size = 1;
		break;

		case getResult:
			if (type == subcatch)
				size = smoapi->SubcatchVars;
			else if (type == node)
				size = smoapi->NodeVars;
			else if (type == link)
				size = smoapi->LinkVars;
			else // system
				size = smoapi->SysVars;
		break;

		default: *errcode = 421;
			return NULL;
		}

		// Allocate memory for outValues
		array = (float*)calloc(size, sizeof(float));
		*errcode = (MEMCHECK(array));

		*length = size;
		return array;
	}
	*errcode = 412;
	return NULL;
}


double* SMO_newOutTimeList(SMOutputAPI* smoapi, int* errcode)
//
//  Purpose: Allocates memory for TimeList.
//
//  Warning: Caller must free memory allocated by this function using SMO_free_double().
//
{
	int size;
	double* array;

	if (smoapi->isOpened)
	{
		size = smoapi->Nperiods;

		array = (double*)calloc(size, sizeof(double));
		*errcode = (MEMCHECK(array));

		return array;
	}
	*errcode = 412;
	return NULL;
}

int SMO_getTimeList(SMOutputAPI* smoapi, double* array)
//
//	Purpose: Return list of all times corresponding to computed results in decimal days since 12/13/1899.
//			 Note that the initial conditions (time 0) are not included in the file. 
{
	int k;

	if (smoapi->isOpened)
	{
		if (array == NULL) return 411;

		// loop over and build time series
		for (k = 0; k < smoapi->Nperiods; k++)
			array[k] = getTimeValue(smoapi, k);

		return 0;
	}
	
	// Error no results to report on binary file not opened
	return 412;
}



int SMO_getSubcatchSeries(SMOutputAPI* smoapi, int subcatchIndex,
	SMO_subcatchAttribute attr, int timeIndex, int length, float* outValueSeries)
//
//  Purpose: Get time series results for particular attribute. Specify series
//  start and length using timeIndex and length respectively.
//
{
	int k;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueSeries == NULL) return 411;

		// loop over and build time series
		for (k = 0; k < length; k++)
			outValueSeries[k] = getSubcatchValue(smoapi, timeIndex + k,
			subcatchIndex, attr);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;
}


int SMO_getNodeSeries(SMOutputAPI* smoapi, int nodeIndex, SMO_nodeAttribute attr,
	int timeIndex, int length, float* outValueSeries)
//
//  Purpose: Get time series results for particular attribute. Specify series
//  start and length using timeIndex and length respectively.
//
{
	int k;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueSeries == NULL) return 411;

		// loop over and build time series
		for (k = 0; k < length; k++)
			outValueSeries[k] = getNodeValue(smoapi, timeIndex + k,
			nodeIndex, attr);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;
}


int SMO_getLinkSeries(SMOutputAPI* smoapi, int linkIndex, SMO_linkAttribute attr,
	int timeIndex, int length, float* outValueSeries)
//
//  Purpose: Get time series results for particular attribute. Specify series
//  start and length using timeIndex and length respectively.
//
{
	int k;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueSeries == NULL) return 411;

		// loop over and build time series
		for (k = 0; k < length; k++)
			outValueSeries[k] = getLinkValue(smoapi, timeIndex + k, linkIndex, attr);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;
}



int SMO_getSystemSeries(SMOutputAPI* smoapi, SMO_systemAttribute attr,
	int timeIndex, int length, float *outValueSeries)
//
//  Purpose: Get time series results for particular attribute. Specify series
//  start and length using timeIndex and length respectively.
//
{
	int k;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueSeries == NULL) return 411;

		// loop over and build time series
		for (k = 0; k < length; k++)
			outValueSeries[k] = getSystemValue(smoapi, timeIndex + k, attr);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;
}

int SMO_getSubcatchAttribute(SMOutputAPI* smoapi, int timeIndex,
	SMO_subcatchAttribute attr, float* outValueArray)
//
//   Purpose: For all subcatchments at given time, get a particular attribute.
//
{
	int k;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueArray == NULL) return 411;

		// loop over and pull result
		for (k = 0; k < smoapi->Nsubcatch; k++)
			outValueArray[k] = getSubcatchValue(smoapi, timeIndex, k, attr);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;

}



int SMO_getNodeAttribute(SMOutputAPI* smoapi, int timeIndex,
	SMO_nodeAttribute attr, float* outValueArray)
//
//  Purpose: For all nodes at given time, get a particular attribute.
//
{
	int k;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueArray == NULL) return 411;

		// loop over and pull result
		for (k = 0; k < smoapi->Nnodes; k++)
			outValueArray[k] = getNodeValue(smoapi, timeIndex, k, attr);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;

}

int SMO_getLinkAttribute(SMOutputAPI* smoapi, int timeIndex,
	SMO_linkAttribute attr, float* outValueArray)
//
//  Purpose: For all links at given time, get a particular attribute.
//
{
	int k;

	if (smoapi->isOpened)
	{
		// Check memory for outValues
		if (outValueArray == NULL) return 411;

		// loop over and pull result
		for (k = 0; k < smoapi->Nlinks; k++)
			outValueArray[k] = getLinkValue(smoapi, timeIndex, k, attr);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;

}


int SMO_getSystemAttribute(SMOutputAPI* smoapi, int timeIndex,
	SMO_systemAttribute attr, float* outValueArray)
//
//  Purpose: For the system at given time, get a particular attribute.
//
{
	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueArray == NULL) return 411;

		// don't need to loop since there's only one system
		outValueArray[0] = getSystemValue(smoapi, timeIndex, attr);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;

}

int SMO_getSubcatchResult(SMOutputAPI* smoapi, int timeIndex, int subcatchIndex,
	float* outValueArray)
//
// Purpose: For a subcatchment at given time, get all attributes.
// 
{
	int offset;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueArray == NULL) return 411;

		// --- compute offset into output file
		offset = smoapi->ResultsPos + (timeIndex)*smoapi->BytesPerPeriod + 2 * RECORDSIZE;
		// add offset for subcatchment
		offset += (subcatchIndex*smoapi->SubcatchVars)*RECORDSIZE;

		fseek(smoapi->file, offset, SEEK_SET);
		fread(outValueArray, RECORDSIZE, smoapi->SubcatchVars, smoapi->file);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;
}


int SMO_getNodeResult(SMOutputAPI* smoapi, int timeIndex, int nodeIndex,
	float* outValueArray)
//
//	Purpose: For a node at given time, get all attributes.
//
{
	int offset;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueArray == NULL) return 411;

		// calculate byte offset to start time for series
		offset = smoapi->ResultsPos + (timeIndex)*smoapi->BytesPerPeriod + 2 * RECORDSIZE;
		// add offset for subcatchment and node
		offset += (smoapi->Nsubcatch*smoapi->SubcatchVars + nodeIndex*smoapi->NodeVars)*RECORDSIZE;

		fseek(smoapi->file, offset, SEEK_SET);
		fread(outValueArray, RECORDSIZE, smoapi->NodeVars, smoapi->file);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;
}


int SMO_getLinkResult(SMOutputAPI* smoapi, int timeIndex, int linkIndex,
	float* outValueArray)
//
//	Purpose: For a link at given time, get all attributes.
//
{
	int offset;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueArray == NULL) return 411;

		// calculate byte offset to start time for series
		offset = smoapi->ResultsPos + (timeIndex)*smoapi->BytesPerPeriod + 2 * RECORDSIZE;
		// add offset for subcatchment and node and link
		offset += (smoapi->Nsubcatch*smoapi->SubcatchVars
			+ smoapi->Nnodes*smoapi->NodeVars + linkIndex*smoapi->LinkVars)*RECORDSIZE;

		fseek(smoapi->file, offset, SEEK_SET);
		fread(outValueArray, RECORDSIZE, smoapi->LinkVars, smoapi->file);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;
}

int SMO_getSystemResult(SMOutputAPI* smoapi, int timeIndex, float* outValueArray)
//
//	Purpose: For the system at given time, get all attributes.
//
{
	int offset;

	if (smoapi->isOpened) 
	{
		// Check memory for outValues
		if (outValueArray == NULL) return 411;

		// calculate byte offset to start time for series
		offset = smoapi->ResultsPos + (timeIndex)*smoapi->BytesPerPeriod + 2 * RECORDSIZE;
		// add offset for subcatchment and node and link (system starts after the last link)
		offset += (smoapi->Nsubcatch*smoapi->SubcatchVars + smoapi->Nnodes*smoapi->NodeVars
			+ smoapi->Nlinks*smoapi->LinkVars)*RECORDSIZE;

		fseek(smoapi->file, offset, SEEK_SET);
		fread(outValueArray, RECORDSIZE, smoapi->SysVars, smoapi->file);

		return 0;
	}
	// Error no results to report on binary file not opened
	return 412;
}

void SMO_free(float *array)
//
//  Purpose: frees memory allocated using SMO_newOutValueSeries() or
//  SMO_newOutValueArray().
//
{
	if (array != NULL)
		free(array);
}

void SMO_freeIDList(struct IDentry* head)
{
	struct IDentry* temp;

	while (head != NULL)
	{
		temp = head;
		head = head->nextID;
		free(temp->IDname);
		free(temp);
		temp = NULL;
	}
}

void SMO_freeTimeList(double *array)
//
//  Purpose: frees memory allocated using SMO_newTimeList
//
{
	if (array != NULL)
		free(array);
}

int SMO_close(SMOutputAPI* smoapi)
//
//   Purpose: Clean up after and close Output API
//
{
	if (smoapi->isOpened) 
	{
		fclose(smoapi->file);
		smoapi->isOpened = false;
		free(smoapi);
		smoapi = NULL;
	}
	// Error binary file not opened
	else return 412;

	return 0;
}

int SMO_errMessage(int errcode, char* errmsg, int n)
//
//  Purpose: takes error code returns error message
//
//  Input Error 411: no memory allocated for results
//  Input Error 412: no results binary file hasn't been opened
//  Input Error 421: invalid parameter code
//  File Error  434: unable to open binary output file
//  File Error  435: run terminated no results in binary file
{
	switch (errcode)
	{
	case 411: strncpy(errmsg, ERR411, n); break;
	case 412: strncpy(errmsg, ERR412, n); break;
	case 421: strncpy(errmsg, ERR421, n); break;
	case 434: strncpy(errmsg, ERR434, n); break;
	case 435: strncpy(errmsg, ERR435, n); break;
	default: return 421;
	}

	return 0;
}


// Local functions:
double getTimeValue(SMOutputAPI* smoapi, int timeIndex)
{
	int offset;
	double value;

	// --- compute offset into output file
	offset = smoapi->ResultsPos + timeIndex*smoapi->BytesPerPeriod;

	// --- re-position the file and read the result
	fseek(smoapi->file, offset, SEEK_SET);
	fread(&value, RECORDSIZE * 2, 1, smoapi->file);

	return value;
}


float getSubcatchValue(SMOutputAPI* smoapi, int timeIndex, int subcatchIndex,
	SMO_subcatchAttribute attr)
{
	int offset;
	float value;

	// --- compute offset into output file
	offset = smoapi->ResultsPos + timeIndex*smoapi->BytesPerPeriod + 2 * RECORDSIZE;
	// offset for subcatch
	offset += RECORDSIZE*(subcatchIndex*smoapi->SubcatchVars + attr);

	// --- re-position the file and read the result
	fseek(smoapi->file, offset, SEEK_SET);
	fread(&value, RECORDSIZE, 1, smoapi->file);

	return value;
}

float getNodeValue(SMOutputAPI* smoapi, int timeIndex, int nodeIndex,
	SMO_nodeAttribute attr)
{
	int offset;
	float value;

	// --- compute offset into output file
	offset = smoapi->ResultsPos + timeIndex*smoapi->BytesPerPeriod + 2 * RECORDSIZE;
	// offset for node
	offset += RECORDSIZE*(smoapi->Nsubcatch*smoapi->SubcatchVars + nodeIndex*smoapi->NodeVars + attr);

	// --- re-position the file and read the result
	fseek(smoapi->file, offset, SEEK_SET);
	fread(&value, RECORDSIZE, 1, smoapi->file);

	return value;
}


float getLinkValue(SMOutputAPI* smoapi, int timeIndex, int linkIndex,
	SMO_linkAttribute attr)
{
	int offset;
	float value;

	// --- compute offset into output file
	offset = smoapi->ResultsPos + timeIndex*smoapi->BytesPerPeriod + 2 * RECORDSIZE;
	// offset for link
	offset += RECORDSIZE*(smoapi->Nsubcatch*smoapi->SubcatchVars + smoapi->Nnodes*smoapi->NodeVars +
		linkIndex*smoapi->LinkVars + attr);

	// --- re-position the file and read the result
	fseek(smoapi->file, offset, SEEK_SET);
	fread(&value, RECORDSIZE, 1, smoapi->file);

	return value;
}

float getSystemValue(SMOutputAPI* smoapi, int timeIndex,
	SMO_systemAttribute attr)
{
	int offset;
	float value;

	// --- compute offset into output file
	offset = smoapi->ResultsPos + timeIndex*smoapi->BytesPerPeriod + 2 * RECORDSIZE;
	//  offset for system
	offset += RECORDSIZE*(smoapi->Nsubcatch*smoapi->SubcatchVars + smoapi->Nnodes*smoapi->NodeVars +
		smoapi->Nlinks*smoapi->LinkVars + attr);

	// --- re-position the file and read the result
	fseek(smoapi->file, offset, SEEK_SET);
	fread(&value, RECORDSIZE, 1, smoapi->file);

	return value;
}
