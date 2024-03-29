.. _rxte-missiontable:

*****************************************************************
RXTE ASM Data Finders (:mod:`gdt.missions.rxte.asm.missiontable`)
*****************************************************************
A natural question may be: "Where do I find the data I need?" Well, you're in 
luck, because this will show you how to find the data you seek. RXTE ASM Data is 
hosted publicly on Zenodo. You will need to download the tar files to get the mission table and individual dwell files. The data 
are stored in a consistent directory structure. But instead of having to navigate a winding maze of directories, we provide a 
couple of  classes built to retrieve the data you want once you've downloaded it. RXTE ASM data is ordered 
into dwells and dwell sequence numbers that are summarized in the mission table file.


Finding RXTE ASM Data
======================
First make sure you have followed the instructions 
:ref:`here<download_test_data>` to download and unpack the RXTE ASM data.

Let's start with reading in the RXTE ASM Mission Table. Note that this table needs to be read only at the beginning of a session:

    >>> from gdt.missions.rxte.asm.missiontable import RXTEMissionTable
    >>> asm_table_data = RXTEMissionTable.open()
    RXTEMissionTable read complete
    
    
Now select a time you are interested in, for example a trigger time from RXTE or another mission    
    >>> from gdt.missions.rxte.asm.time import Time
    >>> time = Time("1997-08-15T12:07:04")
    >>> t0 = time.rxte
    

We don't really care about the directory structure, we just want the data. So 
this class finds the files we want, if the time is within th data, and returns the file names. 
The file names contain the dwell time (in spacecraft time 114262324, or t0.sct) and the dwell sequence number (21).

    >>> dwell_file = RXTEMissionTable.get_dwell_file(t0)
    >>> print(dwell_file)
    camera_data/cam_dwasc_02/amts114262324.21
    
If we want data from 90s after t0, we can get that dwell file name too:

    >>> dwell_file2 = RXTEMissionTable.get_dwell_file(t0+90)
    >>> print(dwell_file2)
    camera_data/cam_dwasc_02/amts114262324.22
    

Great! Now we have two dwell files. :ref:`Continue<rxte-phaii>` to learn 
how to read them in for plotting.



Reference/API
=============

.. automodapi:: gdt.missions.rxte.asm.missiontable
   :inherited-members:


