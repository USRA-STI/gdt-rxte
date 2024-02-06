.. _rxte-time:

*****************************************************
RXTE Mission Epoch  (:mod:`gdt.missions.rxte.time`)
*****************************************************

The RXTE Mission epoch, also called the RXTE Mission Elapsed Time (MET) is 
the number of seconds elapsed since January 1, 1994, 00:00:00 UTC, including 
leap seconds and an RXTE clock correction of 3.37843167 s.  We have defined 
a specialized epoch to work with Astropy ``Time``objects so that RXTE MET can
be easily converted to/from other formats and time scales.

To use this, we simply import and create an astropy Time object with a `'rxte'`
format:

    >>> from gdt.missions.rxte.asm.time import Time
    >>> rxte_met = Time(114264420, format='rxte')
    >>> rxte_met
    <Time object: scale='tt' format='rxte' value=114264420.0>
    
Now, say we want to retrieve the GPS timestamp:

    >>> rxte_met.gps
    555682032.3784316

The Astropy ``Time`` object readily converts it for us. We can also do the 
reverse conversion:

    >>> gps_time = Time(rxte_met.gps, format='gps')
    >>> gps_time
    <Time object: scale='tai' format='gps' value=555682032.3784316>
    
    >>> gps_time.rxte
    1142644120.0

And we should, of course, get back the RXTE MET we started with.  This enables
you do do any time conversions already provided by Astropy, as well as time
conversions between other missions within the GDT.

In addition to time conversions, all time formatting available in Astropy is 
also available here.  For example, we can format the RXTE MET in ISO format:

    >>> rxte_met.iso
    '1997-08-15 12:08:03.562'
    
Finally, there are additional specialized formats associated with the RXTE epoch, which
allows us to compute the RXTE spacecraft time, equal to the RXTE MET-RXTE clock correction of
3.37843167 s, RXTE mission day, and RXTE mission week,which
are time based and needed to identify RXTE ASM data files.

    >>> rxte_met.sct
    114264416.62156834
    
    >>> rxte_met.rxte_mission_day
    1322
    
    >>> rxte_met.rxte_mission_week
    80

    
Reference/API
=============

.. automodapi:: gdt.missions.rxte.asm.time
   :inherited-members:


