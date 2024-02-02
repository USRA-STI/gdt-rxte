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
#
import os
import unittest
#from tempfile import TemporaryDirectory
#from gdt.core import data_path
from gdt.missions.rxte.phaii import RxtePhaiiNoHeaders
from gdt.core.binning.binned import combine_by_factor

test_dwell_file = "/Users/cwilsonh/proposals/Goldstein2021_ADAP/rxte_asm/camera_data/cam_dwasc_01/amts72245226.01"
t0 = 72245338.62156843
detector = "ssc2"

#@unittest.skipIf(not test_dwell_file.exists(), "test files aren't downloaded.")
class TestRxtePhaii(unittest.TestCase):
    
    def setUp(self):
        self.phaii = RxtePhaiiNoHeaders.open_ascii(test_dwell_file, detector, t0)
    
    def tearDown(self):
        self.phaii.close()
    
    def test_detector(self):
        self.assertEqual(self.phaii.detector, 'ssc2')
    
    def test_energy_range(self):
        self.assertAlmostEqual(self.phaii.energy_range[0], 1.5, places=3)
        self.assertAlmostEqual(self.phaii.energy_range[1], 12.0, places=3)

    def test_filename(self):
        self.assertEqual(self.phaii.filename, test_dwell_file)
    
#    def test_headers(self):
#        self.assertEqual(self.phaii.headers.num_headers, 4)
    
    def test_num_chans(self):
        self.assertEqual(self.phaii.num_chans, 3)

    def test_time_range(self):
        t0, t1 = self.phaii.time_range
        t0 += self.phaii.trigtime
        t1 += self.phaii.trigtime
        self.assertAlmostEqual(t0, 72245331.37843166, places=6)
        self.assertAlmostEqual(t1, 72245421.37843166, places=6)
    
    def test_trigtime(self):
        self.assertAlmostEqual(self.phaii.trigtime, 72245338.62156843, places=6)     
        
#    def test_rebin_energy(self):
#        phaii2 = self.phaii.rebin_energy(combine_by_factor, 2)
#        self.assertEqual(phaii2.num_chans, self.phaii.num_chans//2)
    
    def test_rebin_time(self):
        phaii2 = self.phaii.rebin_time(combine_by_factor, 2)
        self.assertEqual(phaii2.data.num_times, 
                         self.phaii.data.num_times//2)

    def test_slice_energy(self):
        phaii2 = self.phaii.slice_energy((1.0, 5.0))
        emin, emax = phaii2.energy_range
        self.assertAlmostEqual(emin, 1.5, places=3)
        self.assertAlmostEqual(emax, 5.0, places=3)

    def test_slice_time(self):
        phaii2 = self.phaii.slice_time((10.0, 20.0))
        t0, t1 = phaii2.time_range
        t0 += phaii2.trigtime
        t1 += phaii2.trigtime
        self.assertAlmostEqual(t0, 72245348.37843166, places=5)
        self.assertAlmostEqual(t1, 72245359.37843166, places=5)
    
    def test_to_lightcurve(self):
        lc = self.phaii.to_lightcurve()
        self.assertEqual(self.phaii.data.num_times, lc.size)

    def test_to_pha(self):
        pha = self.phaii.to_pha()
        self.assertEqual(self.phaii.num_chans, pha.num_chans)

    def test_to_spectrum(self):
        spec = self.phaii.to_spectrum()
        self.assertEqual(self.phaii.num_chans, spec.size)

    def test_write(self):
#        with TemporaryDirectory() as this_path:
        this_path = "/Users/cwilsonh"
        outfile = "test_rxte_phaii_ssc2_960416.phaii"
        RxtePhaiiNoHeaders.write(self.phaii,filename=outfile, directory=this_path, overwrite=True)
        phaii = RxtePhaiiNoHeaders.open_fits(os.path.join(this_path, outfile), self.phaii.detector, self.phaii.trigtime)
        self.assertListEqual(phaii.data.counts.tolist(), self.phaii.data.counts.tolist())
        self.assertListEqual(phaii.data.tstart.tolist(), self.phaii.data.tstart.tolist())
        self.assertListEqual(phaii.data.tstop.tolist(), self.phaii.data.tstop.tolist())
        self.assertListEqual(phaii.data.exposure.tolist(), self.phaii.data.exposure.tolist())
        self.assertListEqual(phaii.ebounds.low_edges(), self.phaii.ebounds.low_edges())
        self.assertListEqual(phaii.ebounds.high_edges(), self.phaii.ebounds.high_edges())
        self.assertListEqual(phaii.gti.low_edges(), self.phaii.gti.low_edges())
        self.assertListEqual(phaii.gti.high_edges(), self.phaii.gti.high_edges())
        self.assertEqual(phaii.trigtime, self.phaii.trigtime)
        self.assertEqual(phaii.detector, "ssc2")
        phaii.close()
