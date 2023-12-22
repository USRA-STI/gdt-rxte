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
##Make Phaii for RXTE ASM data
# when defining in a new instrument module, do a relative import instead:
#from ..core.data_primitives import Ebounds, Gti, TimeEnergyBins
#from ..core.phaii import Phaii
from gdt.core.data_primitives import Ebounds, Gti, TimeEnergyBins
from gdt.core.phaii import Phaii
from astropy.io import ascii
from .headers import PhaiiHeaders
import astropy.io.fits as fits
import numpy as np
import os

__all__ = ['RxtePhaiiNoHeaders']

class RxtePhaiiNoHeaders(Phaii):
    def __init__(self, *args):            
        super(RxtePhaiiNoHeaders, self).__init__(*args)
        self._detector = None
    
#    def write(self, dirname, filename=None):
#        #writing the RXTEPhaii is not yet implemented.
#        raise NotImplementedError
    
    @property
    def detector(self):
        #returns the user input value of detector. It should be ssc0, ssc1, or ssc2
        return self._detector
    
    @classmethod
    def open(cls, filename, detector, t0):
        #inputs
        #filename (str) - name of dwell file including path
        #detector (str) - detector name: ssc0, ssc1, or ssc2
	#t0 - (float) trigger time in met
        			    
        obj = cls()
        #check if filename exists	
        if os.path.isfile(filename):
            #if the filename exisits then open it
            obj._filename = filename

            # open and read the text table of ASM dwell information
            # ...
            data = ascii.read(filename)
            #rename colimns
	    #first column is spacecraft time (MET-3.37s)
            data["col1"].name="sct"
            #second column is count rate in 1.5-3 keV band for ssc0
            data["col2"].name="ssc0a"
            #third column is count rate in 3-5 keV band for ssc0
            data["col3"].name="ssc0b"
            #fourth column is count rate in 5-12 keV band for ssc0
	    # pattern repeats with columns 5-7 corresponding to the three bands in ssc1 and 8-10 for the three bands in ssc2
            data["col4"].name="ssc0c"
            data["col5"].name="ssc1a"
            data["col6"].name="ssc1b"
            data["col7"].name="ssc1c"
            data["col8"].name="ssc2a"
            data["col9"].name="ssc2b"
            data["col10"].name="ssc2c"
            # RXTE ASM has fixed energy bounds 1.5-3, 3-5, 5-12 keV for all three detectors.
            # obj._ebounds = Ebounds.from_bounds(emin, emax) 
            emin = np.array([1.5,3.0,5.0])
            emax = np.array([3.0,5.0,12.0])
            obj._ebounds = Ebounds.from_bounds(emin, emax)
            # arrange RXTE ASM data into TimeEnergyBins inputs
            # obj._data = TimeEnergyBins(counts, tstart, tstop, exposure,
            #                            emin, emax, quality=quality)
            if detector == "ssc0":
                counts = np.transpose(np.array([data["ssc0a"],data["ssc0b"],data["ssc0c"]]))
            elif detector == "ssc1":
                counts = np.transpose(np.array([data["ssc1a"],data["ssc1b"],data["ssc1c"]]))
            elif detector == "ssc2":
                counts = np.transpose(np.array([data["ssc2a"],data["ssc2b"],data["ssc2c"]]))
            else:
                #check if detector input correctly
                print (detector,' not found. Input ssc0, ssc1, or ssc2')
                return
            #define times in MET with 1 second long bins
            tstart = np.array([data["sct"]])+3.37843167-t0
            tstop = np.array([data["sct"]])+4.37843167-t0
            #exposure time is not given in data files. Assume 1 second duration.
            exposure = np.ones(np.size(tstart))
            #put TimeEnergyBins into Phaii class 			
            obj._data = TimeEnergyBins(counts, tstart, tstop, exposure, emin, emax)
            # Set GTI as duration of data
            # obj._gti = Gti.from_bounds(gti_start, gti_end)
            obj._gti = Gti.from_bounds(np.amin(tstart),np.amax(tstop))
            # set _detector to input detector value
            obj._detector = detector
            return obj
        else:
            #Error handling - inform user that file is not found and return nothing.
            print (filename,' not found.')
            return

    @classmethod
    def open_fits(cls, filename, detector, t0):
        #inputs
        #filename (str) - name of dwell file including path
                			    
        obj = cls()
        #check if filename exists	
        if os.path.isfile(filename):
            #if the filename exisits then open it
            obj._filename = filename
       
            # get the headers
#            hdrs = [hdu.header for hdu in obj.hdulist]
#            headers = PhaiiHeaders.from_headers(hdrs)

            # the channel energy bounds
            ebounds = Ebounds.from_bounds(obj.column(1, 'E_MIN'), obj.column(1, 'E_MAX'))
            # the 2D time-channel counts data
            time = obj.column(2, 'TIME')
            endtime = obj.column(2, 'ENDTIME')
            
            exposure = obj._assert_exposure(obj.column(2, 'EXPOSURE'))
            
            data = TimeEnergyBins(obj.column(2, 'COUNTS'), time, endtime, exposure, obj.column(1, 'E_MIN'), obj.column(1, 'E_MAX'))

            # the good time intervals
            gti_start = obj.column(3, 'START')
            gti_stop = obj.column(3, 'STOP')
            gti = Gti.from_bounds(gti_start, gti_stop)
            obj.close()
            return class_.from_data(data, gti=gti, trigger_time=trigtime, 
                                filename=obj.filename, headers=headers)
        else:
            #Error handling - inform user that file is not found and return nothing.
            print (filename,' not found.')
            return
	    

    def _build_hdulist(self):

        # create FITS and primary header
        hdulist = fits.HDUList()
#        primary_hdu = fits.PrimaryHDU(header=self.headers['PRIMARY'])
        primary_hdu = fits.PrimaryHDU()
#       for key, val in self.headers['PRIMARY'].items():
#           primary_hdu.header[key] = val
        hdulist.append(primary_hdu)
        
        # the ebounds extension
        ebounds_hdu = self._ebounds_table()
        hdulist.append(ebounds_hdu)
        
        # the spectrum extension
        spectrum_hdu = self._spectrum_table()
        hdulist.append(spectrum_hdu)        
        
        # the GTI extension
        gti_hdu = self._gti_table()
        hdulist.append(gti_hdu)
        
        return hdulist
        
#    def _build_headers(self, trigtime, tstart, tstop, num_chans):
        
#        headers = self.headers.copy()
#        for hdu in headers:
#            hdu['TSTART'] = tstart
#            hdu['TSTOP'] = tstop
#            try:
#                hdu['DETCHANS'] = num_chans
#            except:
#                pass
#            if trigtime is not None:
#                hdu['TRIGTIME'] = trigtime
#        
#        return headers
    
    def _ebounds_table(self):
        chan_col = fits.Column(name='CHANNEL', format='1I', 
                               array=np.arange(self.num_chans, dtype=int))
        emin_col = fits.Column(name='E_MIN', format='1E', unit='keV', 
                               array=self.ebounds.low_edges())
        emax_col = fits.Column(name='E_MAX', format='1E', unit='keV', 
                               array=self.ebounds.high_edges())
        
#        hdu = fits.BinTableHDU.from_columns([chan_col, emin_col, emax_col], 
#                                            header=self.headers['EBOUNDS'])
        hdu = fits.BinTableHDU.from_columns([chan_col, emin_col, emax_col])
#        for key, val in self.headers['EBOUNDS'].items():
#            hdu.header[key] = val

        return hdu

    def _spectrum_table(self):
        tstart = np.copy(self.data.tstart)
        tstop = np.copy(self.data.tstop)
        if self.trigtime is not None:
            tstart += self.trigtime
            tstop += self.trigtime
        
        counts_col = fits.Column(name='COUNTS', 
                                 format='{}I'.format(self.num_chans), 
                                 bzero=32768, bscale=1, unit='count',
                                 array=self.data.counts)
        expos_col = fits.Column(name='EXPOSURE', format='1E', unit='s', 
                                array=self.data.exposure)
#       qual_col = fits.Column(name='QUALITY', format='1I', 
#                               array=self.data.quality)
        time_col = fits.Column(name='TIME', format='1D', unit='s', 
                               bzero=self.trigtime, array=tstart)
        endtime_col = fits.Column(name='ENDTIME', format='1D', unit='s', 
                                  bzero=self.trigtime, array=tstop)
#        hdu = fits.BinTableHDU.from_columns([counts_col, expos_col, qual_col, 
#                                             time_col, endtime_col], 
#                                            header=self.headers['SPECTRUM'])
        hdu = fits.BinTableHDU.from_columns([counts_col, expos_col, 
                                             time_col, endtime_col])

#        for key, val in self.headers['SPECTRUM'].items():
#            hdu.header[key] = val
#        hdu.header.comments['TZERO1'] = 'offset for unsigned integers'
#        hdu.header.comments['TSCAL1'] = 'data are not scaled'
#        hdu.header.comments['TZERO4'] = 'Offset, equal to TRIGTIME'
#        hdu.header.comments['TZERO5'] = 'Offset, equal to TRIGTIME'
        return hdu

    def _gti_table(self):
        tstart = np.array(self.gti.low_edges())
        tstop = np.array(self.gti.high_edges())
#        if self.trigtime is not None:
#            tstart += self.trigtime
#            tstop += self.trigtime

        start_col = fits.Column(name='START', format='1D', unit='s', 
                                bzero=self.trigtime, array=tstart)
        stop_col = fits.Column(name='STOP', format='1D', unit='s', 
                                bzero=self.trigtime, array=tstop)
#        hdu = fits.BinTableHDU.from_columns([start_col, stop_col], 
#                                            header=self.headers['GTI'])
        hdu = fits.BinTableHDU.from_columns([start_col, stop_col])
        
#        for key, val in self.headers['GTI'].items():
#            hdu.header[key] = val        
#        hdu.header.comments['TZERO1'] = 'Offset, equal to TRIGTIME'
#        hdu.header.comments['TZERO2'] = 'Offset, equal to TRIGTIME'
        return hdu
