from core.project_base import ProjectBase, Section, SectionAsList
#import hydraulics.node
#import hydraulics.link
from enum import Enum
import sys
import csv
import pandas as pd
import os.path
#for banker's rounding
import numpy as np

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

class CalibrationDataset:
    colname_obs = 'Obs'
    colname_sim = 'Sim'
    colname_diff = 'Obs-Sim'
    def __init__(self):
        self.id = ''
        self.data = None
        self.is_selected = False
        self.sum_obs = 0.0  #Sums[2]
        self.sum_sim = 0.0  #Sums[3]
        self.sum_err = 0.0  #Sums[4] e = Abs(sim-obs)
        self.sum_err2 = 0.0  #Sums[5] e*e
        self.sum_sim_stats_ctr = 0 #Sum[1]
        self.sum_obs_non0_ctr = 0 #Sum[7]
        self.sum_err_relative = 0.0 #Sum[8] e/obs
        self.mean_obs = 0.0 # stats[2] obs mean
        self.mean_sim = 0.0 # stats[3] sim mean
        self.mean_err = 0.0 # stats[4] mean error
        self.mean_rms = 0.0 # stats[5] RMS (root-mean-square) error
        self.need_to_calculate_stats = True

    def read_simulated_values(self, sim_tser, rptStart, rptStep, Dur, Nsim):
        # Now match up obs vs sim
        #self.data = pd.DataFrame()
        strsim = CalibrationDataset.colname_sim
        for lrow in range(0, len(self.data)):
            tobs_sec = self.data.index[lrow]
            self.data[strsim].values[lrow] = \
                self.get_sim_value(sim_tser, tobs_sec, rptStart, rptStep, Dur, Nsim)

    def get_sim_value(self, sim_tser, tobs_sec, rptStart, rptStep, Dur, Nsim):
        '''

        Args:
            sim_tser: simulation time series
            tobs_sec: an observation time in seconds
            rptStart: start of reporting period (sec)
            rptStep: interval between reporting (sec)
            Dur: duration of simulation (sec)
            Nsim: number of time periods

        Returns: simulated value at time tobs_sec
        (interpolate if tobs_sec falls between time periods)

        '''
        # ToDo: ensure report timestep is in seconds
        j1 = 0 #time period, int
        j2 = 0 #time period, int
        t1 = 0.0 #time in hours, single
        t2 = 0.0 #time in hours, single
        v1 = 0.0 #sim value at t1
        v2 = 0.0 #sim value at t2
        vs = -1.0 #final simulated value, single
        e = 0.0 #error, single

        if Nsim == 1:
            vs = sim_tser[0]
        elif tobs_sec >= rptStart and tobs_sec <= Dur:
            #ensure floor division or floor divsion
            j1 = int((tobs_sec - rptStart) // rptStep)
            j2 = j1 + 1
            if j1 >= 0 and j2 < Nsim:
                t1 = sim_tser.index[j1]
                v1 = sim_tser[j1]
                t2 = sim_tser.index[j2]
                v2 = sim_tser[j2]
                if sim_tser.index[1] / 3600.0 < 1.0:
                    t1 *= 3600.0
                    t2 *= 3600.0
                vs = v1 + (tobs_sec - t1) / (t2 - t1) * (v2 - v1)

        return vs

    def read_simulated_values_seqential(self, sim_tser):
        # Now match up obs vs sim
        self.data = pd.DataFrame()
        lsimrow_start = 0
        strsim = CalibrationDataset.colname_sim
        for lrow in range(0, len(self.data)):
            tobs_sec = self.data.index[lrow]
            self.data.ix[lrow, strsim], lsimrow_start = \
                self.get_sim_value(sim_tser, tobs_sec, lsimrow_start)
        pass

    def get_sim_value_seqential(self, sim_tser, tobs_sec, simrow_start):
        for lrow in range(simrow_start, len(sim_tser)):
            #ToDo: ensure report timestep is in seconds
            rpttime = sim_tser.index[lrow] * 3600.0
            if rpttime == tobs_sec:
                return (sim_tser[lrow], lrow)
            elif rpttime > tobs_sec:
                # now interpolate
                v1 = sim_tser[lrow - 1]
                t1 = sim_tser.index[lrow - 1] * 3600
                v2 = sim_tser[lrow]
                t2 = sim_tser.index[lrow] * 3600
                ratio_t = (tobs_sec - t1) / (t2 - t1)
                v_idx = v1 + (v2 - v1) * ratio_t
                return (v_idx, lrow)
        pass

    def calc_stats(self):
        vo = 0.0
        vs = 0.0
        sigma = Calibration.DefMeasError / 100.0 #std. dev. of measurement error
        for idx in range(0, len(self.data)):
            vs = self.data[CalibrationDataset.colname_sim].values[idx]
            if vs >= 0.0:
                self.sum_sim_stats_ctr += 1
                vo = self.data[CalibrationDataset.colname_obs].values[idx]
                self.sum_obs += vo
                self.sum_sim += vs
                self.sum_err += abs(vs - vo)
                self.sum_err2 += (vs - vo) ** 2
                if sigma > 0 and vo != 0.0:
                    self.sum_obs_non0_ctr += 1
                    self.sum_err_relative += ((vs - vo)/vo) ** 2
        self.SumsToStats()
        self.need_to_calculate_stats = False
        pass

    def SumsToStats(self):
        if self.sum_sim_stats_ctr > 0:
            self.mean_obs = self.sum_obs / self.sum_sim_stats_ctr
            self.mean_sim = self.sum_sim / self.sum_sim_stats_ctr
            self.mean_err = self.sum_err / self.sum_sim_stats_ctr
            self.mean_rms = np.sqrt(self.sum_err2 / self.sum_sim_stats_ctr)


class Calibration(Section):
    header_char = ';'
    delimiter_char = '\t'

    DefMeasError = 5 #precision error (%) of measurement, integer
    FLOWTOL = 0.005
    MISSING = -1.0e10
    METERSperFOOT = 0.3048
    FEETperMETER = 3.281

    def __init__(self, afilename):
        Section.__init__(self)
        self.name = ''
        """???just an identifier???"""
        self.etype = ECalibrationType.NONE
        """category of calibration data"""
        self.is_flow = None
        self.filename = afilename
        """calibration data file name"""
        self.hobjects = {}
        """object-calibration dataset collection"""
        self.quality = None
        """calibration data chemical collection"""
        self.headers = None
        """calibration data file header line collection"""
        self.status = ECalibrationFileStatus.NeedToRead
        """calibration data file access status"""
        self.netsum_obs = 0.0 #Sums[2]
        self.netsum_sim = 0.0 #Sums[3]
        self.netsum_err = 0.0  #Sums[4] e = Abs(sim-obs)
        self.netsum_err2 = 0.0  #Sums[5] e*e
        self.netsum_sim_stats_ctr = 0 #Sum[1]
        self.netsum_obs_non0_ctr = 0 #Sum[7]
        self.netsum_err_relative = 0.0 #Sum[8] e/obs
        self.meansum_ctr = 0 # s[1] # of values
        self.meansum_obs = 0.0 # s[2] obs mean: Sum of X
        self.meansum_sim = 0.0 # s[3] sim mean: Sum of Y
        self.meansum_obs2 = 0.0 # s[4] Sum of X*X
        self.meansum_sim2 = 0.0 # s[5] Sum of Y*Y
        self.meansum_os = 0.0 # s[6] Sum of X*Y
        self.netmean_obs = 0.0
        self.netmean_sim = 0.0
        self.netmean_err = 0.0  # stats[4] mean error
        self.netmean_rms = 0.0  # stats[5] RMS (root-mean-square) error
        self.read_data()

    def str_hours_to_float(self, strtime):
        '''
        converst time in Hours:Mins:Secs to decimal hours
        Args:
            strtime: input time string
        Returns:
        '''
        n = 0
        hr = 0
        min = 0
        sec = 0

        #strtime = '2000:55:00'

        try:
            good_hr = False
            good_min = False
            good_sec = False
            if ':' in strtime:
                #parse strtime into hours, minuts, & seconds
                sa = strtime.split(':')
                hr, good_hr = self.intTryParse(sa[0])
                min, good_min = self.intTryParse(sa[1])
                if len(sa) >= 3:
                    sec, good_sec = self.intTryParse(sa[2])

                if not good_hr:
                    hr = 0
                if not good_min:
                    min = 0
                if not good_sec:
                    sec = 0

                return float(hr) + float(min) / 60.0 + float(sec) / 3600.0
            else:
                #if no ':' separator then strtime is a decimal number
                t = -1.0
                try:
                    t = float(strtime)
                except ValueError:
                    t = -1.0
                return t
        except ValueError:
            return -1.0
        finally:
            pass

    def intTryParse(self, value):
        try:
            return int(value), True
        except ValueError:
            return value, False

    def floatTryParse(self, value):
        try:
            return float(value), True
        except ValueError:
            return value, False

    def read_data(self):
        '''
        consult Fcalib.pas
        Returns:

        '''
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
                strobs = CalibrationDataset.colname_obs
                strsim = CalibrationDataset.colname_sim
                reader = csv.reader(f, delimiter = Calibration.delimiter_char)
                line = ""
                while True:
                    line = f.readline()
                    if len(line) > 0 and line[0] == Calibration.header_char:
                        self.headers.append(line)
                    else:
                        break
                f.seek(0)
                for l in range(1, len(self.headers) + 1):
                    next(reader)

                times = None
                values = None
                simvals = None
                id_prev = '-999999'
                time_val_hr = 0.0
                time_val_sec = 0.0
                v_val = 0.0
                v_val_good = False
                for id, time, value in reader:
                    if len(id.strip()) > 0:
                        if not id.strip() in self.hobjects.keys():
                            self.hobjects[id.strip()] = None #pd.Series(values, index=times)
                            if id.strip() != id_prev:
                                if id_prev == '-999999':
                                    times = []
                                    values = []
                                    simvals = []
                                elif len(times) > 0:
                                    obs = pd.Series(values, index=times)
                                    sim = pd.Series(simvals, index=times)
                                    self.hobjects[id_prev] = CalibrationDataset()
                                    self.hobjects[id_prev].id = id_prev
                                    # new_dataset.dataset = pd.Series(values, index=times)
                                    self.hobjects[id_prev].data = pd.DataFrame({strobs: obs, strsim: sim})
                                    times = []
                                    values = []
                                    simvals = []
                                id_prev = id.strip()

                    #consult Fcalib.pas: UpdateErrorStats
                    #convert observed time to seconds from decimal hours
                    #ensure to use banker's rounding as Pascal's Round acts like that
                    time_val_hr = self.str_hours_to_float(time)
                    v_val, v_val_good = self.floatTryParse(value)
                    if time_val_hr < 0 or not v_val_good:
                        #bypass bad time steps and bad obs values
                        pass
                    else:
                        time_val_sec = np.round(time_val_hr * 3600.0)
                        times.append(time_val_sec)
                        values.append(v_val)
                        simvals.append(float('NaN'))
                #set up the last hobject calibration data
                obs = pd.Series(values, index=times)
                sim = pd.Series(simvals, index=times)
                self.hobjects[id_prev] = CalibrationDataset()
                self.hobjects[id_prev].id = id_prev
                self.hobjects[id_prev].data = pd.DataFrame({strobs: obs, strsim: sim})
                del times
                del values
                del simvals

            self.status = ECalibrationFileStatus.ReadToCompletion
            pass
        except IOError:
            #print ('cannot open', self.filename)
            self.status = ECalibrationFileStatus.ReadIncomplete
            pass
        else:
            #print (self.filename, 'has', len(f.readlines()), 'lines')
            pass
        finally:
            pass

    def update_network_sum_stats(self):
        self.reset_network_stats()
        for lid in self.hobjects:
            lcali = self.hobjects[lid]
            #lcali = CalibrationDataset()
            if lcali.is_selected and not lcali.need_to_calculate_stats:
                self.netsum_sim_stats_ctr += lcali.sum_sim_stats_ctr
                self.netsum_obs += lcali.sum_obs
                self.netsum_sim += lcali.sum_sim
                self.netsum_err += lcali.sum_err
                self.netsum_err2 += lcali.sum_err2
                self.netsum_obs_non0_ctr += lcali.sum_obs_non0_ctr
                self.netsum_err_relative += lcali.sum_err_relative

                #Updates cumulative sums used for correlation coeff.
                self.meansum_ctr += 1
                self.meansum_obs += lcali.mean_obs
                self.meansum_sim += lcali.mean_sim
                self.meansum_obs2 += lcali.mean_obs ** 2
                self.meansum_sim2 += lcali.mean_sim ** 2
                self.meansum_os += lcali.mean_obs * lcali.mean_sim

        self.SumsToStats()

    def calc_Rcoeff(self):
        #Finds correlation coefficient between X & Y where:
        # s[1] = # values
        # s[2] = Sum of X
        # s[3] = Sum of Y
        # s[4] = Sum of X**2
        # s[5] = Sum of Y**2
        # s[6] = Sum of X*Y

        t1 = self.meansum_ctr * self.meansum_obs2 - self.meansum_obs ** 2
        t2 = self.meansum_ctr * self.meansum_sim2 - self.meansum_sim ** 2
        t3 = self.meansum_ctr * self.meansum_os - self.meansum_obs * self.meansum_sim
        t4 = t1 * t2
        if t4 <= 0:
            return 0.0
        else:
            return t3 / np.sqrt(t4)
        pass

    def SumsToStats(self):
        if self.meansum_ctr > 0:
            self.netmean_obs = self.meansum_obs / self.meansum_ctr
            self.netmean_sim = self.meansum_sim / self.meansum_ctr
            self.netmean_err = self.netsum_err / self.netsum_sim_stats_ctr
            self.netmean_rms = np.sqrt(self.netsum_err2 / self.netsum_sim_stats_ctr)

    def reset_network_stats(self):
        self.netsum_sim_stats_ctr = 0
        self.netsum_obs = 0.0
        self.netsum_sim = 0.0
        self.netsum_err = 0.0
        self.netsum_err2 = 0.0
        self.netsum_obs_non0_ctr = 0
        self.netsum_err_relative = 0.0

        self.meansum_ctr = 0
        self.meansum_obs = 0.0
        self.meansum_sim = 0.0
        self.meansum_obs2 = 0.0
        self.meansum_sim2 = 0.0
        self.meansum_os = 0.0
