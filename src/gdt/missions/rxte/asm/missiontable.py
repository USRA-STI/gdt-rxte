# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT 
# WITH UNLIMITED RIGHTS
#
# Grant No.: 80NSSC21K0651
# Grantee Name: Universities Space Research Association
# Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
# Developed by: Colleen A. Wilson-Hodge
# 			    National Aeronautics and Space Administration (NASA)
#     			Marshall Space Flight Center
#     			Astrophysics Branch (ST-12)
#
# This work is a derivative of the Gamma-ray Data Tools (GDT), including the 
# Core and Fermi packages, originally developed by the following:
#
#     William Cleveland and Adam Goldstein
#     Universities Space Research Association
#     Science and Technology Institute
#     https://sti.usra.edu
#     
#     Daniel Kocevski
#     National Aeronautics and Space Administration (NASA)
#     Marshall Space Flight Center
#     Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not 
# use this file except in compliance with the License. You may obtain a copy of 
# the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
# License for the specific language governing permissions and limitations under 
# the License.
#Make a class to read the RXTE mission table 
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
            """open ascii table"""
            data = ascii.read(filename, format='no_header',delimiter='\s',guess=False,fast_reader=True)
            #rename columns
            data["col1"].name="metstarttime"
            data["col2"].name="dwellseqnum"
            data["col3"].name="dwellnum"
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
        """get_dwell_ids selects the record corresponding to t0. 
        inputs: t0 (float) = trigger time"""
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
        """get_dwell_file parses the file name for the dwell file for a given
         t0
        inputs:
        t0 (float) trigger time
        filename (str) dwell file name""" 
        if os.path.isdir(dirname):
            dwell_start_time,dwell_seq_no,dwell_id = self.get_dwell_ids(t0)
            if dwell_start_time.size == 0:
                print ('No dwell files found')
                return ()
            else:
                #Figure out where the dwell time falls within the directory structure
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
