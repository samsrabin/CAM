.. _model-output:

**************************
Model Output:
**************************

CAM produces a series of NetCDF format history files containing atmospheric gridpoint data generated during the course of a run. It also produces a series of NetCDF format restart files necessary to continue a run once it has terminated successfully and a series of initial conditions files that may be used to initialize new simulations. The contents of these datasets are described below.

------------------------
Model History Files
------------------------

History files contain model data values written at specified frequencies during a run. Options are also available to record averaged, instantaneous, maximum, or minimum values on a field-by-field basis. If the user wishes to see a field written at more than one time frequency (e.g. daily, hourly), additional history files must be declared. This functionality is available via setting namelist variables.

History files may be visualized using various commercial or freely available tools. Examples include the the NCAR Graphics package (via NCL), CDAT, FERRET, ncview, MATLAB, and IDL. For a list of software tools for interacting with NetCDF files, view the UNIDATA maintained link `Software for Manipulating or Displaying NetCDF Data <http://www.unidata.ucar.edu/software/netcdf/software.html>`_.

--------------------------------------------------------
 Customizing output History Fields
--------------------------------------------------------

CAM writes a sequence of time samples to each of its specified history files.  By default, CAM will output a set of fields to a single monthly average history file.  There are namelist parameters which allow the user to customize output from their run. Up to ten history file streams may be output, each with its own set of characteristics.  This section will highlight some of the most commonly used history namelist settings.

The following namelist settings are specified to customize each output stream desired.  Within the file, individual fields may be specified to be instantaneous or averaged along with other settings.  See the `namelist page <http://www.cesm.ucar.edu/models/cesm2.0/component_namelists/cam_nml.html>`_ and review the fincl defintion for more options for the fields.

- ``finclX`` - List the fields to include in the output file #X (X=1-10)
- ``fexclX`` - List the fields to exclude from the output file #X (X=1-10)

The following three namelist variables are arrays up to length 10 which specify characteristics for the output files.  

- ``nhtfrq`` - Array of write frequencies for each history file series.  If nhtfrq(1) = 0, the file will be a monthly average.  Only the first file series may be a monthly average.  If nhtfrq(i) > 0, frequency is specified as number of timesteps.  If nhtfrq(i) < 0, frequency is specified as number of hours.
- ``ndens`` - set to 1 to output double precision reals, and 2 to output single precision
- ``mfilt`` - the maximum number of times to output into a file for each output stream

There are also namelist settings which control output in a general way.  

- ``empty_htapes`` - turn off all default output and only write out the fields explicitly set via fincl settings
- ``history_YYY`` - add fields for specific diagnostic purposes to the
  default output.  For the complete listing go to the `namelist page <http://www.cesm.ucar.edu/models/cesm2.0/component_namelists/cam_nml.html>`_ and search for namelist variables with the ``history_`` prefix (i.e. ``history_amwg``, ``history_clubb``, etc.)


----------------------------------------
General Features of History Files
----------------------------------------

Each time sample in a history file has an associated timestamp which conforms to the `CF metadata conventions <http://cfconventions.org/>`_. The time unit used in CAM's output files is "days since reference date" where the reference date is the run start date by default, but can be customized via the ``ref_ymd and ref_tod`` namelist variables. The variables relevant to the timestamps are the following (from the output of the NetCDF ``ncdump`` utility):
::

        double time(time) ;
                time:long_name = "time" ;
                time:units = "days since 0000-01-01 00:00:00" ;
                time:calendar = "noleap" ;
                time:bounds = "time_bnds" ;

        double time_bnds(time, nbnd) ;
                time_bnds:long_name = "time interval endpoints" ;

        int date(time) ;
                date:long_name = "current date (YYYYMMDD)" ;

        int datesec(time) ;
                datesec:long_name = "current seconds of current date" ;


The variable names, ``time``, ``time_bnds``, ``date``, and ``datesec`` are all local conventions. What makes the history files CF compliant is that the time coordinate, ``time``, can be identified by it's units attribute "days since 0000-01-01 00:00:00". The reference date is in the form YYYY-MM-DD HH:MM:SS where YYYY, MM, DD, HH, MM, SS are year, month, day, hour, minute, second respectively, and a missing timezone defaults to UTC. The ``calendar`` and ``bounds`` attributes are also part of CF. The ``calendar`` value ``"noleap"`` denotes the Gregorian calendar with no leap years. The bounds value ``time_bnds`` denotes that the variable with the name ``time_bnds`` contains the timestamps that bound the time intervals over which an operation such as computing an averager or a minimum or maximum value has been applied. Whether or not the interval specified by ``time_bnds`` is relevent depends on the individual variables, e.g., a single file can contain both instantaneous and time averaged fields. The type of the time operation that has been applied is contained in the ``cell_methods`` attribute of each variable, e.g.,
::

        float T(time, lev, lat, lon) ;
                T:mdims = 1 ;
                T:units = "K" ;
                T:long_name = "Temperature" ;
                T:cell_methods = "time: mean" ;


The ``cell_methods`` attribute for the temperature variable indicates that it is being output as a time averaged field. If temperature was instantaneous then the ``cell_methods`` attribute would not be present since instantaneous is the default.

The variables ``date`` and ``datesec`` are for convenience only; they don't play any role in terms of CF compliance. The ``date`` variable is an integer which is encoded to contain the digits YYYYMMDD where YYYY, MM, and DD are the year, month, and day of month respectively. ``datesec`` is the integer number of seconds past 0Z in the current day. The variables ``date`` and ``datesec`` are redundant in the sense that they can be recovered from the time variable via a date calculation using the specified calendar.

-----------------------------
Timestamps and time intervals
-----------------------------

**The timestamp associated with each time sample in a history file is the model time at the end of the timestep during which the model writes data to the disk.** In the case of instantaneous data the meaning is clear. However when the data is representative of a time interval, the timestamp corresponds to **the end of the interval**.

This is often a point of confusion when looking at history files. Since the endpoint of one interval is the same as the beginning of the next interval, when looking at a monthly average for January, which has a timestamp of 0Z on Feb 01, at first glance the timestamp would seem to correspond to a February average. Hence it's important for post processing tools to make use of the data in the ``time_bnds`` variable so that the time interval endpoints can be used to compute an interval midpoint which is the more appropriate timestamp to associate with the interval.

======================================================
Example: Timestamps for a year of monthly averages
======================================================

Here are the timestamps and corresponding time interval bounds for a one year sequence of monthly averages starting at 0000-01-01 00:00:00.
::

   Month    time    date   datesec   time_bnds
   Jan       31      201      0        0,  31
   Feb       59      301      0       31,  59
   Mar       90      401      0       59,  90
   Apr      120      501      0       90, 120
   May      151      601      0      120, 151
   Jun      181      701      0      151, 181
   Jul      212      801      0      181, 212
   Aug      243      901      0      212, 243
   Sep      273     1001      0      243, 273
   Oct      304     1101      0      273, 304
   Nov      334     1201      0      304, 334
   Dec      365    10101      0      334, 365


--------------------------------------
Multiple time samples in a single file
--------------------------------------

CAM's default history output is a sequence of monthly averaged fields, written with one time sample per file. This restriction is related to the default file naming scheme which uses the string "YYYY-MM" to indicate the year and month of the average contained in the file. However in general it is possible to write multiple time samples in any of the history file streams that don't contain monthly time intervals. However there is one somewhat unexpected "feature" of multiple time sample files that we wish to point out here.

===============================================
Example: Timestamps for five daily averages
===============================================

Here are the timestamps and corresponding time interval bounds for all time samples written to a single file from a 5 day run starting at 0000-01-01 00:00:00.
::

   Sample    time    date   datesec   time_bnds
   1           0      101     0         0, 0
   2           1      102     0         0, 1
   3           2      103     0         1, 2
   4           3      104     0         2, 3
   5           4      105     0         4, 5
   6           5      106     0         5, 6

Instead of ending up with a file containing five time samples, i.e., a daily average for each of the first five days of January, we get six time samples. The first one looks a bit strange since the time bounds are indicating an interval of zero duration. But in fact that's correct for the first time sample which is instantaneous data representing the initial conditions which have only been modify by a partial first step up to the point of the radiation calculation. This "extra" time sample from the initialization phase is included in every history file except for the monthly average file. An unfortunate consequence of this extra time sample is that it's not possible to create a sequence of files with the same number of time intervals since the first file in the sequence will always have one fewer time interval than the rest due to the inclusion of the time zero sample.

--------------------------------------------------------
Example: Default History Fields and Master Field Lists
--------------------------------------------------------

CAM is set up by default to output a set of fields to a single monthly average history file. There is a much larger set of available fields, known as the "master field list," from which the user can choose fields of interest to add to the history file via namelist settings. Both the set of default fields and the master field list depend on how CAM is configured. Due to the large number of fields we have chosen to make lists of fields for some standard configuration available via linked documents rather than to inline the lists here. Each of the field list documents is comprised of tables containing the lists of fields that are output by default as well as the master field list.

**NOTE:**  The master field list tables may contain some fields that are not actually available for output. The presence of a field in the master field list is a necessary, but not sufficient condition that the corresponding field in the history file will contain valid data. This is because in some instances fields are added to the master field list (this is done in the source code) even though that field may not be computed in the configuration that is built (specified via the arguments to ``configure``). When adding non-default fields to the history file it's important to check that the fields contain reasonable data before doing a long run.

The following links provide tables of default and master field lists for some standard model compsets. The source of the information in these tables is CAM's default log file, so you can always look there for any configuration not included in the list below.

- `F2000climo <http://www.cesm.ucar.edu/models/cesm2/atmosphere/docs/ug6/hist_flds_f2000.html>`_
