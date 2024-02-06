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
from gdt.missions.rxte.missiontable import RXTEMissionTable
import os

directory = os.environ['RXTE_DATA_PATH']

# read in the mission table. I'm not sure how to make a test for this.
# I'm hard coding my path at the moment to test other parts of the code. I need 
# to fix this later before releasing. 
asm_table_data = RXTEMissionTable.open(os.path.join(directory,"asm_mission_pointing.table")) 

#define three dwells to retrieve
# start of first asm dwell
met1 = 63449123.37843167
sct1 = 63449120
dwell_start1 = 63449088
dwell_seq1 = 63448692
dwell_id1 = 4
dwell_file1 = 'cam_dwasc_01/amts63448692.04'

# start of last asm dwell before ev mode
met2 = 226105491.37843168
sct2 = 226105488
dwell_start2 = 226105488
dwell_seq2 = 226104807
dwell_id2 = 7
dwell_file2 = 'cam_dwasc_03/amts226104807.07'


# start of asm ev files
met3 = 226109235.37843168
sct3 = 226109232
dwell_start3 = 226109232
dwell_seq3 = 226109232
dwell_id3 = 0
dwell_file3 = 'cam_evasc_01/ev226109232.00'

# last of asm dwell files'
met4 = 503710467.37843168
sct4 = 503710464
dwell_start4 = 503710464
dwell_seq4 = 503710464
dwell_id4 = 0
dwell_file4 = 'cam_evasc_04/ev503710464.00'

class TestMissionTable(unittest.TestCase):
    
    def test_get_dwell_ids(self):
        assert RXTEMissionTable.get_dwell_ids(met1) == (dwell_start1, dwell_seq1, dwell_id1)
        assert RXTEMissionTable.get_dwell_ids(met2) == (dwell_start2, dwell_seq2, dwell_id2)
        assert RXTEMissionTable.get_dwell_ids(met3) == (dwell_start3, dwell_seq3, dwell_id3)
        assert RXTEMissionTable.get_dwell_ids(met4) == (dwell_start4, dwell_seq4, dwell_id4)

    def test_get_dwell_file(self):
        assert RXTEMissionTable.get_dwell_file(met1, directory) == os.path.join(directory,dwell_file1)
        assert RXTEMissionTable.get_dwell_file(met2, directory) == os.path.join(directory,dwell_file2)
        assert RXTEMissionTable.get_dwell_file(met3, directory) == os.path.join(directory,dwell_file3)
        assert RXTEMissionTable.get_dwell_file(met4, directory) == os.path.join(directory,dwell_file4)
