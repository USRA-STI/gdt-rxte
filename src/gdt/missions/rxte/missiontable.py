#Make a class to read the RXTE mission table from Ron Remillard
#This takes a long time
from astropy.io import ascii
import numpy as np
import os

class RXTEMissionTable():
    def __init__(self, times, dwell_seq_nums, dwell_ids):
        self.times = times
        self.dwell_seq_nums = dwell_seq_nums
        self.dwell_ids = dwell_ids
    
    @classmethod
    def open(cls,filename):
        if os.path.isfile(filename):
            #open ascii table
            data = ascii.read(filename, format='no_header',delimiter='\s',guess=False,fast_reader=True)
            #rename columns
            data["col1"].name="metstarttime"
            data["col2"].name="dwellseqnum"
            data["col3"].name="dwellnum"
            #data[3].name="exposssc0"
            #data[4].name="exposssc1"
            #data[5].name="exposssc2"
            #data[6].name="rassc0"
            #data[7].name="decssc0"
            #data[8].name="posangssc0"
            #data[9].name="rassc1"
            #data[10].name="decssc1"
            #data[11].name="posangssc1"
            #data[12].name="rassc2"
            #data["col14"].name="decssc2"
            #data["col15"].name="posangssc2"
            #data["col16"].name="instrumentrotang"
            #data["col17"].name="sumcounts0"
            #data["col18"].name="sumcounts1"
            #data["col19"].name="sumcounts2"
            cls.times = data["metstarttime"]
            cls.dwell_seq_nums = data["dwellseqnum"]
            cls.dwell_ids = data["dwellnum"]
            print ("RXTEMissionTable read complete")
        
            return cls
        else:
            print (filename,' does not exist')
            return

    @classmethod
    def get_dwell_ids(self,t0):
        #this part selects the record corresponding to t0. I need to figure out how to do error handling
        #if t0 is not found in the file.
        #inputs: t0 (float) - trigger time
        mask = ((t0>self.times)&(t0<self.times+90))
        if self.times[mask].size == 0:
            print ('t0 = ',t0, 'is > 90 s from asm dwell start times.')
            print ('Nearest dwell: ',np.amin(np.absolute(t0-self.times)), 's from t0')
            return (self.times[mask],self.dwell_seq_nums[mask],self.dwell_ids[mask])
        else:
            sel_times = self.times[mask]
            sel_dwell_seq_nums = self.dwell_seq_nums[mask]
            sel_dwell_ids = self.dwell_ids[mask]
            return (sel_times[0],sel_dwell_seq_nums[0],sel_dwell_ids[0])
    
    @classmethod
    def get_dwell_file(self,t0,dirname):
        #this parses the file name for the dwell file for a given t0
        #need to figure out error handling if t0 not found
        #inputs:
        #t0 (float) trigger time
        #filename (str) dwell file name 
        if os.path.isdir(dirname):
            dwell_start_time,dwell_seq_no,dwell_id = self.get_dwell_ids(t0)
            if dwell_start_time.size == 0:
                print ('No dwell files found')
                return ()
            else:
                #Figure out where the dwell time falls within the directory structure from Ron Remillard
                if (dwell_seq_no < 99999999): 
                    dwell_subdir = 'cam_dwasc_01'
                    dwell_file_start_str = 'amts'
                elif (dwell_seq_no > 99999999) & (dwell_seq_no < 160000000):
                    dwell_subdir = 'cam_dwasc_02'
                    dwell_file_start_str = 'amts'
                elif (dwell_seq_no > 160000000) & (dwell_seq_no < 226105000):
                    dwell_subdir = 'cam_dwasc_03'
                    dwell_file_start_str = 'amts'
                elif (dwell_seq_no > 226105000) & (dwell_seq_no < 300000000):
                    dwell_subdir = 'cam_evasc_01'
                    dwell_file_start_str = 'ev'
                elif (dwell_seq_no > 300000000) & (dwell_seq_no < 400000000):
                    dwell_subdir = 'cam_evasc_02'
                    dwell_file_start_str = 'ev'
                elif (dwell_seq_no > 400000000) & (dwell_seq_no < 500000000):
                    dwell_subdir = 'cam_evasc_039'
                    dwell_file_start_str = 'ev'
                elif (dwell_seq_no > 500000000) & (dwell_seq_no < 600000000):
                    dwell_subdir = 'cam_evasc_04'
                    dwell_file_start_str = 'ev'
                else: print ('dwell_seq_no', dwell_seq_no, 'not found')
                #construct dwell_filename (str)
                if dwell_id <10: 
                    dwell_filename = dirname+'/'+dwell_subdir+'/'+dwell_file_start_str + str(dwell_seq_no)+'.0'+str(dwell_id)
                else:
                    dwell_filename = dirname+'/'+dwell_subdir+'/'+dwell_file_start_str + str(dwell_seq_no)+'.'+str(dwell_id)
     
                return dwell_filename
        else:
            print (dirname, 'does not exist')
            return ()

