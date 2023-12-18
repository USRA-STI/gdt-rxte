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
from gdt.core.headers import Header, FileHeaders
from ..time import Time

__all__ = ['PhaiiHeaders']

# mission definitions
_telescope = 'RXTE'
_instrument = 'ASM'
_observer = 'None'
_origin = 'gdt-rxte'
_timesys = 'TT'
_timeunit = 's'
_radecsys = 'FK5'
_equinox = 2000.0
_mjdrefi = 49353
_mjdreff = '6.965740760000000E-04'

# common keyword cards
_ancrfile_card = ('ANCRFILE', 'none', 'Name of corresponding ARF file (if any)')
_areascale_card = ('AREASCAL', 1.0, 'No special scaling of effective area by channel')
_backfile_card = ('BACKFILE', 'none', 'Name of corresponding background file (if any)')
_backscale_card = ('BACKSCAL', 1.0, 'No scaling of background')
_chantype_card = ('CHANTYPE', 'PHA', 'No corrections have been applied')
_corrfile_card = ('CORRFILE', 'none', 'Name of corresponding correction file (if any)')
_corrscale_card = ('CORRSCAL', 1., 'Correction scaling file')
_datatype_card = ('DATATYPE', '', 'RXTE datatype used for this file')
_date_card = ('DATE', '', 'file creation date (YYYY-MM-DDThh:mm:ss UT)')
_date_end_card = ('DATE-END', '', 'Date of end of observation')
_date_obs_card = ('DATE-OBS', '', 'Date of start of observation')
#_dec_obj_card = ('DEC_OBJ', 0.0, 'Calculated Dec of burst')
_detchans_card = ('DETCHANS', 0, 'Total number of channels in each rate')
_detnam_card = ('DETNAM', '', 'Individual detector name')
#_equinox_card = ('EQUINOX', _equinox, 'Equinox for RA and Dec')
#_err_rad_card = ('ERR_RAD', 0.0, 'Calculated Location Error Radius')
_extname_card = ('EXTNAME', '', 'name of this binary table extension')
_extver_card = ('EXTVER', 1, 'Version of this extension format')
_filename_card = ('FILENAME', '', 'Name of this file')
_filetype_card = ('FILETYPE', '', 'Name for this type of FITS file')
_filever_card = ('FILE-VER', '1.0.0', 'Version of the format for this filetype')
_filter_card = ('FILTER', 'none', 'The instrument filter in use (if any)')
_grouping_card = ('GROUPING', 0, 'No special grouping has been applied')
_hduclass_card = ('HDUCLASS', 'OGIP', 'Conforms to OGIP standard indicated in HDUCLAS1')
_hduvers_card = ('HDUVERS', '1.2.1', 'Version of HDUCLAS1 format in use')
_infile_card = ('INFILE01', '', 'Level 1 input lookup table file')
_instrument_card = ('INSTRUME', _instrument, 'Specific instrument used for observation')
_mjdrefi_card = ('MJDREFI', _mjdrefi, 'MJD of RXTE reference epoch, integer part')
_mjdreff_card = ('MJDREFF', _mjdreff, 'MJD of RXTE reference epoch, fractional part')
_object_card = ('OBJECT', '', 'Burst name in standard format, yymmddfff')
_observer_card = ('OBSERVER', _observer, 'RXTE All-Sky Monitor P.I.')
_origin_card = ('ORIGIN', _origin, 'Name of organization making file')
_poiserr_card = ('POISSERR', True, 'Assume Poisson Errors')
#_radecsys_card = ('RADECSYS', _radecsys, 'Stellar reference frame')
#_ra_obj_card = ('RA_OBJ', 0.0, 'Calculated RA of burst')
_respfile_card = ('RESPFILE', 'none', 'Name of corresponding RMF file (if any)')
_syserr_card = ('SYS_ERR', 0., 'No systematic errors')
_telescope_card = ('TELESCOP', _telescope, 'Name of mission/satellite')
_timesys_card = ('TIMESYS', _timesys, 'Time system used in time keywords')
_timeunit_card = ('TIMEUNIT', _timeunit, 'Time since MJDREF, used in TSTART and TSTOP')
_tstart_card = ('TSTART', 0.0, '[GLAST MET] Observation start time')
_tstop_card = ('TSTOP', 0.0, '[GLAST MET] Observation stop time')
_trigtime_card = ('TRIGTIME', 0.0, 'Trigger time relative to MJDREF, double precision')

#----------------
class RxteHeader(Header):

    def __setitem__(self, key, val):
        if not isinstance(key, tuple):
            if key.upper() == 'TSTART':
                self['DATE-OBS'] = Time(val, format='rxte').iso
            elif key.upper() == 'TSTOP':
                self['DATE-END'] = Time(val, format='rxte').iso
            else:
                pass

            if 'INFILE' in key.upper():
                super(Header, self).__setitem__(key, val)
                return

        super().__setitem__(key, val)


class DataPrimaryHeader(RxteHeader):
    name = 'PRIMARY'
    keywords = [Header.creator(), _filetype_card, _filever_card, 
                _telescope_card, _instrument_card, _detnam_card, _observer_card,
                _origin_card, _date_card, _date_obs_card, _date_end_card,
                _timesys_card, _timeunit_card,_mjdrefi_card,_mjdreff_card,
                _tstart_card, _tstop_card, _filename_card, _datatype_card]


class EboundsHeader(RxteHeader):
    name = 'EBOUNDS'
    keywords = [_extname_card, _telescope_card, _instrument_card, _detnam_card,
                _observer_card, _origin_card, _date_card, _date_obs_card,
                _date_end_card, _timesys_card, _timeunit_card, _mjdrefi_card,
                _mjdreff_card, _tstart_card, _tstop_card, _hduclass_card,
                ('HDUCLAS1', 'RESPONSE', 'These are typically found in RMF ' \
                                         'files'),
                ('HDUCLAS2', 'EBOUNDS', 'From CAL/GEN/92-002'), _hduvers_card,
                _chantype_card, _filter_card, _detchans_card,
                ('CH2E_VER', '', 'Channel to energy conversion scheme used'),
                ('GAIN_COR', 0.0, 'Gain correction factor applied to energy ' \
                                  'edges')]

class SpectrumHeader(RxteHeader):
    name = 'SPECTRUM'
    keywords = [_extname_card, _telescope_card, _instrument_card, _detnam_card,
                _observer_card, _origin_card, _date_card, _date_obs_card,
                _date_end_card, _timesys_card, _timeunit_card, _mjdrefi_card,
                _mjdreff_card, _tstart_card, _tstop_card, _filter_card, 
                _areascale_card, _backfile_card, _backscale_card, 
                _corrfile_card, _corrscale_card, _respfile_card, _ancrfile_card,
                _syserr_card, _poiserr_card, _grouping_card, _hduclass_card,
                ('HDUCLAS1', 'SPECTRUM', 'PHA dataset (OGIP memo OGIP-92-007)'),
                ('HDUCLAS2', 'TOTAL', 'Indicates gross data (source + background)'),
                ('HDUCLAS3', 'COUNT', 'Indicates data stored as counts'),
                ('HDUCLAS4', 'TYPEII', 'Indicates PHA Type II file format'),
                _hduvers_card, _chantype_card, _detchans_card, _extver_card]                   

class GtiHeader(RxteHeader):
    name = 'GTI'
    keywords = [_extname_card, _telescope_card, _instrument_card, _detnam_card,
                _observer_card, _origin_card, _date_card, _date_obs_card,
                _date_end_card, _timesys_card, _timeunit_card, _mjdrefi_card,
                _mjdreff_card, _tstart_card, _tstop_card, _hduclass_card,
                ('HDUCLAS1', 'GTI', 'Indicates good time intervals'),
                _hduvers_card, _extver_card]


#-------------------------------------

class PhaiiHeaders(FileHeaders):
    """FITS headers for continuous RXTE ASM files"""
    _header_templates = [DataPrimaryHeader(), EboundsHeader(), SpectrumHeader(), 
                         GtiHeader()]

    
