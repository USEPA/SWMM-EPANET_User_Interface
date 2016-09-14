from core.project_base import ProjectBase, Section, SectionAsList
#import hydraulics.node
#import hydraulics.link
from enum import Enum
import sys
import csv
import pandas as pd
import os.path

class ECalibrationType(Enum):
    """Type of Calibration"""
    DEMAND = 1
    HEAD = 2
    PRESSURE = 3
    QUALITY = 4
    FLOW = 5
    VELOCITY = 6
    NONE = 7

class ECalibrationFileStatus(Enum):
    NeedToRead = 1
    ReadToCompletion = 2
    FileNotExists = 3
    ReadIncomplete = 4

class Calibration(Section):
    header_char = ';'
    delimiter_char = '\t'

    def __init__(self, afilename):
        Section.__init__(self)
        self.name = ''
        """???just an identifier???"""
        self.etype = ECalibrationType.NONE
        """category of calibration data"""
        self.filename = afilename
        """calibration data file name"""
        self.hobjects = {}
        """object-calibration data collection"""
        self.quality = None
        """calibration data chemical collection"""
        self.headers = None
        """calibration data file header line collection"""
        self.status = ECalibrationFileStatus.NeedToRead
        """calibration data file access status"""
        self.read_data()

    def read_data(self):
        if not os.path.exists(self.filename):
            self.hobjects.clear()
            self.status = ECalibrationFileStatus.FileNotExists
            return
        try:
            if self.headers == None:
                self.headers = []
            else:
                del self.headers[:]

            with open(self.filename, 'r') as f:
                reader = csv.reader(f, delimiter = Calibration.delimiter_char)
                line = ""
                while True:
                    line = f.readline()
                    if len(line) > 0 and line[0] == Calibration.header_char:
                        self.headers.append(line)
                    else:
                        break
                f.seek(0)
                for l in xrange(1, len(self.headers) + 1):
                    next(reader)

                times = None
                values = None
                id_prev = '-999999'
                for id, time, value in reader:
                    if len(id.strip()) > 0:
                        if not id.strip() in self.hobjects.keys():
                            self.hobjects[id.strip()] = None #pd.Series(values, index=times)
                            if id.strip() != id_prev:
                                if id_prev == '-999999':
                                    times = []
                                    values = []
                                elif len(times) > 0:
                                    self.hobjects[id_prev] = pd.Series(values, index=times)
                                    times = []
                                    values = []
                                id_prev = id.strip()
                    times.append(float(time))
                    values.append(float(value))
                #set up the last hobject calibration data
                self.hobjects[id_prev] = pd.Series(values, index=times)
                del times
                del values

            self.status = ECalibrationFileStatus.ReadToCompletion
            pass
        except IOError:
            #print 'cannot open', self.filename
            self.status = ECalibrationFileStatus.ReadIncomplete
            pass
        else:
            #print self.filename, 'has', len(f.readlines()), 'lines'
            pass
        finally:
            pass
