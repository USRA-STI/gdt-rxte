# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT 
# WITH UNLIMITED RIGHTS
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
#
import unittest
from gdt.missions.rxte.asm.time import *


# Values confirmed using xtime utility using utc for iso string and tt for mjd
# rxte_mission_week from short term schedule at RXTE GOF
# rxte mission day starts from timezero

# start of first asm dwell
met1 = 63440899.37843167
utc_str1 = '1996-01-05 06:28:20.757'
mjd1 = 50087.27040440814
sct1 = 63440896.0
mission_day1 = 734
mission_week1 = -2

# start of asm ev files
met2 = 226109235.37843168
utc_str2 = '2001-03-02 00:07:14.757'
mjd2 = 51970.00577477851
sct2 = 226109232.0
mission_day2 = 2617
mission_week2 = 266

# last of asm dwell file
met3 = 503710467.37843168
utc_str3 = '2009-12-17 23:34:24.757'
mjd3 = 55182.982997000734
sct3 = 503710464.0
mission_day3 = 5829
mission_week3 = 724

class TestTime(unittest.TestCase):
    
    def test_to_utc(self):
        assert Time(met1, format='rxte').utc.iso == utc_str1
        assert Time(met2, format='rxte').utc.iso == utc_str2
        assert Time(met3, format='rxte').utc.iso == utc_str3

    def test_utc_to_rxte(self):
        self.assertAlmostEqual(Time(utc_str1, format='iso', scale='utc').rxte, met1, 3)
        self.assertAlmostEqual(Time(utc_str2, format='iso', scale='utc').rxte, met2, 3)
        self.assertAlmostEqual(Time(utc_str3, format='iso', scale='utc').rxte, met3, 3)


    def test_to_mjd(self):
        assert Time(met1, format='rxte').mjd == mjd1
        assert Time(met2, format='rxte').mjd == mjd2
        assert Time(met3, format='rxte').mjd == mjd3

    def test_mjd_to_rxte(self):
        self.assertAlmostEqual(Time(mjd1, format='mjd', scale='tt').rxte, met1, 3)
        self.assertAlmostEqual(Time(mjd2, format='mjd', scale='tt').rxte, met2, 3)
        self.assertAlmostEqual(Time(mjd3, format='mjd', scale='tt').rxte, met3, 3)
        
    def test_to_sct(self):
        assert Time(met1, format='rxte').sct == sct1
        assert Time(met2, format='rxte').sct == sct2
        assert Time(met3, format='rxte').sct == sct3
       
    def test_to_mission_week(self):
        assert Time(met1, format='rxte').rxte_mission_week == mission_week1
        assert Time(met2, format='rxte').rxte_mission_week == mission_week2
        assert Time(met3, format='rxte').rxte_mission_week == mission_week3
         
    def test_to_mission_day(self):
        assert Time(met1, format='rxte').rxte_mission_day == mission_day1
        assert Time(met2, format='rxte').rxte_mission_day == mission_day2
        assert Time(met3, format='rxte').rxte_mission_day == mission_day3
   
