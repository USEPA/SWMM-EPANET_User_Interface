import hydraulics.node
#import hydraulics.link #maybe in the future there will be data for links as well
from enum import Enum
import sys
import csv
import pandas as pd

class CalibrationType(Enum):
    """Type of Calibration"""
    DEMAND = 1
    HEAD = 2
    PRESSURE = 3
    QUALITY = 4
    FLOW = 5
    VELOCITY = 6
    NONE = 7

class CalibrationFileStatus(Enum):
    NeedToRead = 1
    ReadToCompletion = 2
    FileNotExists = 3
    ReadIncomplete = 4

class Calibration:
    header_char = ';'
    delimiter_char = '\t'

    def __init__(self, afilename):
        self.type = CalibrationType.NONE
        self.filename = afilename
        self.nodes = {}
        self.quality = None
        self.headers = None
        self.status = CalibrationFileStatus.NeedToRead

    def read_data(self):
        import os.path
        if not os.path.exists(self.filename):
            self.status = CalibrationFileStatus.FileNotExists
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
                for id, time, value in reader:
                    if len(id) > 0:
                        if not id in self.nodes.keys():
                            times = []
                            values = []
                            self.nodes[id] = pd.Series(values, index=times)
                    times.append(time)
                    values.append(value)
            self.status = CalibrationFileStatus.ReadToCompletion
            pass
        except IOError:
            #print 'cannot open', self.filename
            self.status = CalibrationFileStatus.ReadIncomplete
            pass
        else:
            #print self.filename, 'has', len(f.readlines()), 'lines'
            pass
        finally:
            pass
