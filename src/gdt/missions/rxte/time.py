# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT WITH UNLIMITED RIGHTS
#
# Contract No.: CA 80MSFC17M0022
# Contractor Name: Universities Space Research Association
# Contractor Address: 7178 Columbia Gateway Drive, Columbia, MD 21046
#
# Copyright 2017-2022 by Universities Space Research Association (USRA). All rights reserved.
#
# Developed by: William Cleveland and Adam Goldstein
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
#
# Developed by: Daniel Kocevski
#               National Aeronautics and Space Administration (NASA)
#               Marshall Space Flight Center
#               Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing permissions and limitations under the
# License.
##this will be part of time.py

from astropy.time import TimeFromEpoch, TimeUnique, ScaleValueError, Time

__all__ = ['RxteSecTime', 'Time']

class RxteSecTime(TimeFromEpoch):
    """"Represents the number of seconds elapsed since Jan 1, 1994 00:00:00 UTC including leap seconds and RXTE clock correction of 3.37843167E+00 s """
    
    name = 'rxte'
    """(str): Name of the mision"""    
    
    unit = 1.0/86400
    """(float): unit in days"""
    
    epoch_val = '1994-01-01 00:01:03.56243157'
    """(str): The epoch in Terrestrial Time"""
    
    epoch_val2 = None
    
    epoch_scale = 'tt' # Terrestrial Time
    """(str): The scale of :attr: `epoch_val`"""
    
    epoch_format = 'iso'
    """(str): Format of :attr:`epoch_val`"""
    
from astropy.time import Time as AstropyTime

class Time(AstropyTime):    

    @property
    def sct(self):
        # Return the spacecraft time (used for dwell file names) corresponding to the met
        return self.rxte - 3.37843167
	
    @property
    def rxte_mission_day(self):
        # Return the RXTE mission day - this needs to be in Spacecraft time to match the 
        # dwell sequence
        return int((self.sct)/86400)
    
    @property
    def rxte_mission_week(self):
        # Return the RXTE mission week - this is computed in MJD based on an e-mail from 
        # Ron Remillard on Mar-2-2022. This is used if xapt files are retrieved from the HEASARC. 
        return int((self.mjd-50115.0)/7)
	    
 
