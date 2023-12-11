#Make Phaii for RXTE ASM data
# when defining in a new instrument module, do a relative import instead:
#from ..core.data_primitives import Ebounds, Gti, TimeEnergyBins
#from ..core.phaii import Phaii
from gdt.core.data_primitives import Ebounds, Gti, TimeEnergyBins
from gdt.core.phaii import Phaii
from astropy.io import ascii
import numpy as np
import os

class RxtePhaiiNoHeaders(Phaii):
    def __init__(self, *args):            
        super(RxtePhaiiNoHeaders, self).__init__(*args)
        self._detector = None
    
    def write(self, dirname, filename=None):
        #writing the RXTEPhaii is not yet implemented.
        raise NotImplementedError
    
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

