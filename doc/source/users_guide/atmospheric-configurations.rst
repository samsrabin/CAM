.. _atmospheric-configurations:
 

**************************************
Atmospheric configurations (compsets)
**************************************

There are a number of atmospheric models which can run within CESM.  While CAM is the basic atmospheric model within CESM, there are several models with significant extensions to CAM which may also be run within CESM.  The available atmospheric models in CESM2 are:

- **CAM**:  Community Atmosphere Model
- **CAM-chem**: Community Atmosphere Model with Chemistry  
- **WACCM**: Whole Atmosphere Community Climate Model
- **WACCM-X**: Whole Atmosphere Community Climate Model with thermosphere and ionosphere extension

Each of these models have a number of atmospheric configurations provided to run them.  These component sets known as **compsets** are used to supply both configure and namelist settings for predefined experiments.

The predefined compsets exist with one of three levels of support.

- **Scientifically supported**:  Specific compset/resolution pairs which have had significant, multi-year runs made and have been studied scientifically.  It is important to note that resolutions which are not listed, are not scientifically supported, have not had tunings performed and should not be used for scientific studies without careful examination of the results.
- **Tested**: One or more tests for this compset have been made using at least one resolution.  Extensive scientific study has not been performed.  The designation of "Tested" simply acknowledges that one or more compset/resolution pair(s) have been confirmed to run without crashing.  No attempts have been made to validate the scientific quality of these runs and tunings have NOT been performed on them.
- **Unsupported**:  These compsets are setup as a "convenience" for various reasons and they are not supported for science runs.  If a user decides to use one of these compsets, they must also supply the --run-unsupported flag to create_newcase.  These compsets may not even compile and run successfully as they have not been tested.

CAM compsets include the F, P and Q compsets.

- **F**: CAM standalone runs, using an active Atmosphere and Land with prescribed Sea-Surface Temperatures (SSTs) and sea-ice extent. 
- **P**: Parallel offline radiation tool (PORT)
- **Q**: Aquaplanet with either prescribed ocean (QP) or slab ocean(QS)

This chapter will discuss some of the atmospheric compsets in more detail, but a complete listing of all compsets is found at `CESM2 Component Configurations (compsets) <http://www.cesm.ucar.edu/models/cesm2.0/cesm/compsets.html>`_.  The complete listing of grid resolutions can be found at `CESM2 Grid Resolutions <http://www.cesm.ucar.edu/models/cesm2.0/cesm/grids.html>`_.

-------------------------------------------------------------------------------
CAM scientifically supported compsets
-------------------------------------------------------------------------------
CAM has a number of compsets/resolutions which are supported scientifically.  These compsets are detailed in the following table.  A specific compset may be listed below, but unless the resolution is also listed, that compset/resolution combination is not scientifically supported.  Different resolutions exhibit different behavior and as a result require different tunings.  The scientifically supported designation is limited to the specific compset/resolution pairs listed in the following tables.

**Scientifically supported CAM compsets**

+--------------+----------------------+-----------------------------------------+-------------+
| Compset Name | supported resolution |Description                              | Period      |
+==============+======================+=========================================+=============+
| FHIST        | f09_f09_mg17         | Historical CAM6 using 1 degree finite   | 1979 to 2015|
|              |                      | volume dycore *[Note - this is similar  |             |
|              |                      | to the obsolete CAM5 FAMIP compset]*    |             |
+--------------+----------------------+-----------------------------------------+-------------+
| F2000climo   | f09_f09_mg17         | Climatological present day climate      | Climos over |
|              |                      | (year 2000) with CAM6 physics           |  1995-2005  |
|              |                      | using 1 degree fv dycore                |  1995-2005  |
+--------------+----------------------+-----------------------------------------+-------------+

To run the FHIST compset, and create a case called fhist, simply run the following commands::

  % cd cime/scripts
  % ./create_newcase --case fhist --compset FHIST --res f09_f09_mg17 
  % cd fhist
  % ./case.setup
  % ./case.build
  % ./case.submit

To run the F2000climo compset, and create a case called f_present_day, simply run the following commands::

  % cd cime/scripts
  % ./create_newcase --case f_present_day --compset FHIST --res f09_f09_mg17 
  % cd f_present_day
  % ./case.setup
  % ./case.build
  % ./case.submit

  
An important reminder: On cheyenne, if you are building on a login node, you must say::

  % qcmd -- ./case.build
  
It should be noted that a number of CAM4 and CAM5-specific compsets have been eliminated from the CAM6 release.
The rationale behind this is that due to changes in code and namelist settings, a user is unable to numerically reproduce CAM4 or CAM5 runs similar to what they would get running CESM1.2.
It is recommended that if a user wants to make a true CAM4 or CAM5 run, that they do so using CESM1.2 instead of CESM2.0.

-------------------------------------------------------------------------------
CAM Simple Models
-------------------------------------------------------------------------------

There are several simpler configurations in which CAM can be run.  These include:
 - Generic adiabatic simple model (FDABIP04)
 - Held-Suarez simple model (FHS94)
 - Aquaplanet (QP and QS compsets)
 - PORT - Parallel Offline Radiation Tool (P compsets)
 - SCAM - single column model (FSCAM compset)

**Scientifically supported CAM simpler model compsets**

+--------------+----------------------+-----------------------------------------+-------------+
| Compset Name | supported resolution |Description                              | Period      |
+==============+======================+=========================================+=============+
| FDABIP04     | T42z30_T42_mg17,     | Generic adiabatic simple model          |             |
|              | T85z30_T85_mg17,     |                                         |             |
|              | T85z60_T85_mg17      |                                         |             |
+--------------+----------------------+-----------------------------------------+-------------+
| FSCAM        | T42_T42              | Single column CAM                       |             |
+--------------+----------------------+-----------------------------------------+-------------+
| FHS94        | T42z30_T42_mg17,     | Held-Suarez simpler model               |             |
|              | T85z30_T85_mg17,     |                                         |             |
|              | T85z60_T85_mg17      |                                         |             |
+--------------+----------------------+-----------------------------------------+-------------+
| QPC6         | f09_f09_mg17,        | Prescribed SST Aquaplanet using CAM6    | 2000 to 2015|
|              | f19_f19_mg17         |                                         |             |
+--------------+----------------------+-----------------------------------------+-------------+
| QSC6         | f09_f09_mg17,        | Slab-Ocean Aquaplanet using CAM6        | 2000 to 2015|
|              | f19_f19_mg17         |                                         |             |
+--------------+----------------------+-----------------------------------------+-------------+


====================================================================================
CAM aquaplanet (QP and QS compsets)
====================================================================================

Aquaplanets are configurations of global atmospheric models that have no landmasses and saturated lower boundaries. The aquaplanet compsets in CESM2 provide a convenient way to configure CAM with prescribed, zonally symmetric SST, a user-supplied SST dataset, or a slab-ocean lower boundary. The surface is controlled through the data ocean model. There are a standard set of SST profiles based on the AquaPlanet Experiment project (APE; Neale & Hoskins [2]_, Williamson et al. [3]_). The advantage of an aquaplanet configuration is that it allows the user to run the full CAM parameterization suite while retaining much simpler surface conditions than the complex combination of land, ocean, and sea-ice in the real world.  The CAM5 aquaplanet configuration is described by Medeiros et al. [1]_


Aquaplanet compsets which have been tested, but are not scientifically supported: 
 - QPC5 -- Prescribed SST Aquaplanet using CAM5
 - QPC4 -- Prescribed SST Aquaplanet using CAM4
 - QSC5 -- Slab-Ocean Aquaplanet for CAM5
 - QSC4 -- Slab-Ocean Aquaplanet for CAM4

###############################################################
Example 1: Default Aquaplanet with prescribed SST
###############################################################
To run the standard CAM6 aquaplanet, simply supply the compset name::

  % cd cime/scripts
  % ./create_newcase --case aqua_case --compset QPC6 --res f09_f09_mg17 
  % cd aqua_case
  % ./case.setup
  % ./case.build
  % ./case.submit

By default, initial conditions from a previous aquaplanet simulation are used. The SST pattern is the APE "QOBS" option, which is used in APE and CFMIP protocols. The atmospheric ozone is specified to be that used for APE. Aerosol emissions are neglected except for sea salt (which is diagnostic), see Medeiros et al. [1]_ for details.

###############################################################
Example 2: Default Aquaplanet with Slab-Ocean Model
###############################################################
To run the standard CAM6 aquaplanet with a 30 m uniform slab-ocean, simply supply the compset name::

  % cd cime/scripts
  % ./create_newcase --case aqua_case --compset QSC6 --res f09_f09_mg17
  % cd aqua_case
  % ./case.setup
  % ./case.build
  % ./case.submit
 
Note that the slab-ocean model has no ocean heat transport by default; the user must specify an appropriate "qflux" file. To specify such a file::

  % ./xmlchange DOCN_SOM_FILENAME="path/to/file.nc"

where path/to/file.nc is the path to the ppropriate "qflux" file.

###############################################################
Example 3: Aquaplanet with alternate prescribed SST
###############################################################
All of the APE SST profiles are available. To use them invoke the long compset name with the user compset option::

  % cd cime/scripts
  % ./create_newcase --case cam5_3keq --compset 2000_CAM50_SLND_SICE_DOCN%AQP7_SROF_SGLC_SWAV --res f09_f09_mg17 --run-unsupported
     (Note that you may see a message "Did not find an alias or longname compset match..."  This message may be ignored)
  % cd cam5_3keq
  % ./case.setup
  % ./case.build
  % ./case.submit

The example uses the 3KEQ SST pattern, which is specified with "AQP7" in the compset name. The analytical SST profiles are defined in the source code (cime/src/components/data_comps/docn/docn_comp_mod.F90). Also note this example switched to CAM5 physics by specifying "CAM50" in the compset name. The run-unsupported flag is required.

###############################################################
Example 4: Aquaplanet with user-specified SST dataset
###############################################################
An arbitrary SST dataset can be specified instead of the default APE SST. To do that, start with the default case, and then change the data ocean mode and specify the file::

  % cd cime/scripts
  % ./create_newcase --case aqua_sst_case --compset QPC4 --res f19_f19_mg17  --run-unsupported
  % cd aqua_sst_case
  % ./case.setup
  % ./xmlchange DOCN_MODE=sst_aquapfile 
  % ./xmlchange DOCN_AQP_FILENAME=sst.nc
  % ./case.build
  % ./case.submit

Where sst.nc is the user-supplied SST file, which follows the same conventions as SST files used for F compsets. Note this example switches to CAM4 physics on a 2-degree grid, so requires the run-unsupported flag.

.. [1] Medeiros, B., D. L. Williamson, and J. G. Olson, 2016: Reference aquaplanet climate in the community atmosphere model, version 5. Journal of Advances in Modeling Earth Systems, doi: http://dx.doi.org/10.1002/2015MS000593

.. [2] Neale, R. B. and B. J. Hoskins, 2000a: A standard test for AGCMs including their physical parametrizations. I: The proposal. Atmos. Sci. Lett., 1, 101-107. http://dx.doi.org/10.1006/asle.2000.0022

.. [3] Williamson, D. L., and Coauthors, 2012: The APE atlas. NCAR Technical Note NCAR/TN-484+STR, doi:10.5065/D6FF3QBR. http://dx.doi.org/10.5065/D6FF3QBR

====================================================================================
CAM Parallel Offline Radiation Tool (PORT - P compsets)
====================================================================================
PORT is used as part of the process for computing radiative forcing and instantaneous radiative forcing.
For effective radiative forcing please see the documentation related to F-case runs.

PORT uses instantaneous samples of the model state to compute the radiative fluxes and heating rates
through the atmosphere.  This computation does not include middle and upper atmospheric radiative
transfer as implemented in WACCM.  The only prognostic variable is temperature, in the specific PORT
configuration to compute radiative forcing that includes the stratospheric adjustment (fixed dynamical heating).

##########################################################################
PORT Compsets
##########################################################################

+------------+-----------------------------------------------+
| short name | long name                                     |
+============+===============================================+
| PC4        | 2000_CAM40%PORT_SLND_SICE_SOCN_SROF_SGLC_SWAV |
+------------+-----------------------------------------------+
| PC5        | 2000_CAM50%PORT_SLND_SICE_SOCN_SROF_SGLC_SWAV |
+------------+-----------------------------------------------+
| PC6        | 2000_CAM60%PORT_SLND_SICE_SOCN_SROF_SGLC_SWAV |
+------------+-----------------------------------------------+

The user is required to supply radiation input datasets via one of the namelist options:

- **offline_driver_infile** (for single input file)
- **offline_driver_fileslist** (sequential list of input files)

These can be set in the **user_nl_cam** file found in the CESM case directory.

##########################################################################
Example: Using PORT to study flux differences due to 2 x CO2
##########################################################################

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sample the base run
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the base sampling case::
  
  % cd cime/scripts
  % ./create_newcase --case base_run_case --res f09_f09_mg17 --compset F2000climo
  % cd base_run_case
  % ./case.setup

Set up the **user_nl_cam** file for the base run::

  ! Output the radiation data
  rad_data_output=.true.

  ! Specify the radiation data be written to history file number 2 (rad_data will be in files with cam.h1 in their name)
  rad_data_histfile_num=2

  ! Write out the instantaneous rad_data and radiation diagnostics
  rad_data_avgflag = 'I'
  avgflag_pertape = 'A','I'

  ! Make certain the radiation is called every time step
  iradlw = 1
  iradsw = 1

  ! Include radiation diagnostics
  fincl2 = 'FLNT', 'FLNR','FLNS', 'FSNT','FSNR', 'FSNS'

  ! Output frequency
  nhtfrq = 0,73

  ! number of time records per individual history file
  mfilt = 1,5

  ! double precision output
  ndens = 1,1

Note: It has been found that sampling every 73'rd time step is a good balance of computational cost
and size of data for dtime = 1800 and a 2-degree horizontal resolution. [4]_

.. [4] Conley, A. J., Lamarque, J.-F., Vitt, F., Collins, W. D., and Kiehl, J.: PORT, a CESM tool for the diagnosis of radiative forcing, Geosci. Model Dev., 6, 469-476, https://doi.org/10.5194/gmd-6-469-2013, 2013.
  

Build and submit this sampling run data::

 % ./xmlchange STOP_N=16
 % ./xmlchange STOP_OPTION=nmonths
 % ./case.build
 % ./case.submit

After your job completes, you will have a number of files, including ones with filenames containing "cam.h1".
The "cam.h1" files contain the radiation history which was specified by the namelist and will be used in the
next step.  

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PORT validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  
Create the PORT validation run::
  
  % ./create_newcase --case port_run_case --res f09_f09_mg17 --compset PC6
  % cd port_run_case

Set up the **user_nl_cam** file for the PORT run::

  ! PORT input data
  offline_driver_infile = '/path/base_run_case.cam.h1.0001-01-01-00000.nc'

  ! Output the radiation data
  rad_data_output=.true.

  ! Specify the radiation data be written to history file number 2 (rad_data will be in files with cam.h1 in their name)
  rad_data_histfile_num=2

  ! Write out the instantaneous rad_data and radiation diagnostics
  rad_data_avgflag = 'I'
  avgflag_pertape = 'A','I'

  ! Make certain the radiation is called every time step
  iradlw = 1
  iradsw = 1

  ! Include radiation diagnostics
  fincl2 = 'FLNT', 'FLNR','FLNS', 'FSNT','FSNR', 'FSNS'

  ! Output frequency
  nhtfrq = 0,73

  ! number of time records per individual history file
  mfilt = 1,5

  ! double precision output
  ndens = 1,1

For verification tests the run time length should be long enough to include at least a few sampling times.

Build and submit this validation run data::

 % ./case.setup
 % ./xmlchange STOP_N=5
 % ./xmlchange STOP_OPTION=ndays
 % ./case.build
 % ./case.submit

The differences in radiation diagnostics (FLNT,FLNR,FLNS,FSNT,FSNR,FSNS) in the the sampling base run and the
PORT run should be zero (or within roundoff).

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Compute forcing due to a change in composition (CO2, as an example)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this case we are doubling the CO2 and modifying this via the netcdf utility, ncap for each file.
Further documentation on ncap can be found in the `NCO User Guide <http://nco.sourceforge.net/nco.html>`_.

Modify the composition in the sample files.  For each file listed in /path/samples.inputs::
  
  % for fin in base_run_case.cam.h1*nc; do fout="${fin/cam.h1/cam.h1-2xCO2}"; ncap2 -s "rad_CO2=2.0*rad_CO2" $fin $fout; done

Prepare sequential list of input files for the PORT run::

  % ls -1 /path/base_run_case.cam.h1-2xCO2.*nc > /path/samples2xCO2.inputs

Prepare the PORT run::
  
  % ./create_newcase --case port_2xCO2_case --res f09_f09_mg17 --compset PC6
  % cd port_2xCO2_case

Set up the **user_nl_cam** file for the PORT run::

  ! Sequential list of input files
  offline_driver_fileslist = '/path/samples2xCO2.inputs'

  ! Allow temperatures above the tropopause to equilibrate under the assumption of fixed dynamical heating
  rad_data_fdh = .true.

  ! Write out the instantaneous radiation diagnostics
  avgflag_pertape = 'A','I'
 
  ! Make certain the radiation is called every time step
  iradlw = 1
  iradsw = 1

  ! Include radiation diagnostics
  fincl2 = 'FLNT', 'FLNR','FLNS', 'FSNT','FSNR', 'FSNS'
 
  ! Output frequency
  nhtfrq = 0,73

Build and submit::

 % ./case.setup
 % ./xmlchange STOP_N=16
 % ./xmlchange STOP_OPTION=nmonths
 % ./case.build
 % ./case.submit

Forcing is the difference between:
 - the net flux at the tropopause (FLNR-FSNR) from the last 12 months of the sample files  AND
 - the net flux at the tropopause (FLNR-FSNR) from the last 12 months of the 2xCO2sample files

===============================================================================
CAM single column (FSCAM compset)
===============================================================================

SCAM cases are set up for a small set of different locations/dates, called an Intensive Observing Period (IOP).  Each of these IOP's have separate preconfigured settings which are referenced by create_new_case using the --user-mods-dir flag. 

The list of the available configurations and the associated usermods_dirs directory are:

 -  **ARM95**: scam_arm95
 -  **ARM97**: scam_arm97 -- *default*
 -  **ATEX**: scam_atex
 -  **BOMEX**: scam_bomex
 -  **CGILSS11**: scam_cgilsS11
 -  **CGILSS12**: scam_cgilsS12
 -  **CGILSS6**: scam_cgilsS6
 -  **DYCOMSRF01**: scam_dycomsRF01
 -  **DYCOMSRF02**: scam_dycomsRF02
 -  **GATEIII**: scam_gateIII
 -  **MPACE**: scam_mpace
 -  **RICO**: scam_rico
 -  **SPARTICUS**: scam_sparticus
 -  **TOGAII**: scam_togaII
 -  **TWP06**: scam_twp06
 -  Mandatory settings: scam_mandatory (used by all SCAM runs, and not to be modified by the user)

#########################################################################################
SCAM Configuration Options
#########################################################################################

The default SCAM settings read in initial conditions for aerosols off of an initial condition file: typically a CAM initial condition file. The aerosols and the Temperature field are relaxed to the initial conditions with a variable timescale from 10 days at the bottom of the model to 2 days at the top of the model. U and V wind are taken from the IOP file. This ensures that aerosols and temperature do not drift too far in the upper troposphere and above: where advection for aerosols is important, and where non-represented dynamical forcing would dominate the temperature field. Any field can be relaxed using this method if the user desires it. 

Emissions of constituents from the surface occur as in a standard CAM simulation, reading off climatological emissions files for the year 2000.

Default Settings:
::

	scm_use_obs_uv         = .true.
	scm_relaxation         = .true.
	scm_relax_fincl = 'T', 'bc_a1', 'bc_a4', 'dst_a1', 'dst_a2', 'dst_a3', 'ncl_a1', 'ncl_a2',
	                  'ncl_a3', 'num_a1', 'num_a2', 'num_a3',
	                  'num_a4', 'pom_a1', 'pom_a4', 'so4_a1', 'so4_a2', 'so4_a3', 'soa_a1', 'soa_a2'
	scm_relax_bot_p        = 105000.
	scm_relax_top_p        = 200.
	scm_relax_linear       = .true.
	scm_relax_tau_bot_sec  = 864000.
	scm_relax_tau_top_sec  = 172800.


#########################################################################################
Example:  Setting up a SCAM run 
#########################################################################################
Users specify the directory containing the specifications for running an IOP using the --user-mods-dir flag.  In this example we are using the MPACE IOP.  Note that the default settings are to run for all of the observations within the IOP, but a user may shorten that by issuing an xmlchange for the STOP_N setting.  In this example we will limit the run to 600 timesteps
::

	% cd cime/scripts
	% ./create_newcase --case test_scam_mpace --compset FSCAM --res T42_T42 --user-mods-dir ../../components/cam/cime_config/usermods_dirs/scam_mpace
	% cd test_scam_mpace
	% ./case.setup
	% ./xmlchange STOP_N=600
	% ./case.build
	% ./case.submit

If the user neglects to specify a --use-mods-dir, then it defaults to a shortened run of ARM97.

The user may also find it useful to modify the sample script **components/cam/bld/scripts/create_scam6_iop**.
 
#########################################################################################
Example:  Efficient way to cycle over several SCAM IOP locations 
#########################################################################################
While a user can use the above directions for running multiple IOP's, rebuilding the executable for each IOP is time-consuming and unnecessary as the same executable may be used for multiple IOP's.  A more efficient way to run over several IOP's is to use create_newcase using the scam_mandatory setup and then using create_clone for all SCAM IOP's.  This example, will make runs for TWP06 and SPARTICUS by running create_newcase using the setup in scam_mandatory and then using create_clone for test_scam_twp06 and test_scam_sparticus.  Note the addition of the flag --keepexe on the create_clone command to indicate that the executable will be used from the test_scam_mandatory case.
::

        % cd cime/scripts
        % ./create_newcase --case test_scam_mandatory --compset FSCAM --res T42_T42 --user-mods-dir ../../components/cam/cime_config/usermods_dirs/scam_mandatory
        % cd test_scam_mandatory
        % ./case.setup
        % ./case.build

        % cd ..
        % ./create_clone --case test_scam_twp06 --clone test_scam_mandatory --user-mods-dir ../../components/cam/cime_config/usermods_dirs/scam_twp06 --keepexe
        % cd test_scam_twp06
        % ./case.submit

        % cd ..
        % ./create_clone --case test_scam_sparticus --clone test_scam_mandatory --user-mods-dir ../../components/cam/cime_config/usermods_dirs/scam_sparticus --keepexe
        % cd test_scam_sparticus
        % ./case.submit

The user may modify the sample script **components/cam/bld/scripts/create_scam6_iop_multi**.

#########################################################################################
Example:  Setting up User Defined IOP for SCAM  
#########################################################################################

If a user wishes to run SCAM with an IOP location that is not already predefined, the following directions may be used to generate a user defined IOP.  This example will assume that the user wishes to create an IOP at 305 degrees E and 62 degrees N over the Labrador Sea.  It is important to note that the user needs to have the NetCDF Command Language (NCL) and NetCDF Operators (NCO) installed on their machine as the generation scripts utilize this library.


1. First, run CAM (in any desired configuration ) with following namelist, specifying fields at a point (305 degrees E, 62 degrees N)
::
   
        fincl2=U, V, T, Q, OMEGA, TTEND_TOT, PTTEND, TAQ, TS,PS,PSL
        fincl2lonlat = ‘305e_62n’
        nhtfrq = 0,-3
        avgflag_pertape = 'A','I'

Averaging can be either 'I'nstantaneous or 'A' average for fincl2
This produces 3 hourly output at a point for fincl2 fields on an h1 file.

2. Run the following script on the resulting h1 files: 
::

        ./components/cam/bld/scripts/camfv2iop.ncl

This uses NCL and NCO to create a SCAM IOP file. See internal to the script for documentation on what needs to be changed for a particular case.

3. Run the User IOP case.

To run the user iop with SCAM, follow the following steps (here it is a test case over the Labrador Sea from a CAM Run)

- Decide your iop name (e.g. usrLabSea)
- Add this IOP to the script create_scam6_iop
- In the tag you have downloaded, go to the 'usermods_dirs' directory
	- cam6_0_000/components/cam/cime_config/usermods_dirs
- Copy one of the directories for the IOP cases, e.g.
        - cp -r scam_arm97 scam_usrLabSea
- Change files in this directory
	- **shell_commands**: XML change commands: Typically the LAT, LON, STARTDATE, START_TOD, STOP_OPTION and STOP_N
	- **user_nl_cam**:  usually just iopfile. May also want to change mfilt (to keep all times on one file) 
- Run create_scam6_iop script with appropriate IOP (e.g. IOP=scam_usrLabSea in this case)

	
-------------------------------------------------------------------------------
Other CAM compsets
-------------------------------------------------------------------------------

There are a number of other CAM compsets which have not been described in this document. The complete listing of all compsets is found `here <http://www.cesm.ucar.edu/models/cesm2.0/cesm/compsets.html>`_.  Users are cautioned about using compsets that are not scientifically supported or tested.  These compsets are not supported and users may encounter problems or get invalid results using them.

===============================================================================
Super-parameterized CAM (SPCAM)
===============================================================================

Another set of compsets which require a brief description are ones for Super-parameterized CAM (SPCAM). SPCAM implements a 2D cloud resolving model (the System for Atmospheric Modeling SAM, Version 6.10.4) in CAM6.0 to replace its conventional parameterization for moist convection and large-scale condensation [5]_. Four different compsets are provided. FSPCAMS uses one moment SAM microphysics, and is based on Khairoutdinov and Randall [6]_. FSPCAMM uses two moment microphysics from Morrison et al [7]_, and its implementation is based on Wang et al. [5]_; [8]_; [9]_. FSPCAMCLBS and FSPCAMCLBM are the same as FSPCAMS and FSPCAMM respectivly, but are coupled with a higher-order turbulence closure scheme, CLUBB [5]_.  In FSPCAMM ad FSPCAMCLBM, the Explicit-Cloud-Parameterized-Pollutant (ECPP) approach is used to treat cloud processing of aerosols with statistics of cloud properties resolved by the cloud resolving model (Gustafson et al., 2008) [10]_ . It is important to point out that the CLUBB version used in SPCAM is an older version of CLUBB than what is used by CAM6.0 and this customized version of CLUBB resides in the CRM library.  The performance of these four compsets as they existed in CAM5.2 has been documented in detail [5]_ and [11]_.

.. [5] Wang, M., V. Larson, S. Ghan, M. Ovchinnikov, D. Schanen, H. Xiao, X. Liu, Z.  Guo, and P. Rasch (2015), A multiscale modeling framework model (superparameterized CAM5) with a higher-order turbulence closure: Model description and low-cloud simulations, Journal of Advances in Modeling Earth Systems, 7, https://doi.org/10.1002/2014MS000375.

.. [6] Khairoutdinov, M. F., and D. A. Randall (2001), A cloud resolving model as a cloud parameterization in the NCAR Community Climate System Model: Preliminary results, Geophys Res Lett, 28(18), 3617-3620.

.. [7] Morrison, H., Curry, J. A., Khvorostyanov, V. I. (2005). A new double-moment microphysics parameterization for application in cloud and climate models. Part I: Description. Journal of the atmospheric sciences, 62(6), 1665-1677.

.. [8] Wang, M., et al. (2011a), The multi-scale aerosol-climate model PNNL-MMF: model description and evaluation, Geosci. Model Dev., 4(1), 137–168, doi:10.5194/gmd-4-137-2011.

.. [9] Wang, M., S. Ghan, M. Ovchinnikov, X. Liu, R. Easter, E. Kassianov, Y. Qian, and H. Morrison (2011b), Aerosol indirect effects in a multi-scale aerosol-climate model PNNL-MMF, Atmos. Chem. Phys., 11(11), 5431-5455.

.. [10] Gustafson, W. I., L. K. Berg, R. C. Easter, and S. J. Ghan (2008), The Explicit- Cloud Parameterized-Pollutant hybrid approach for aerosol-cloud interactions in multiscale modeling framework models: tracer transport results, Environ Res Lett, 3(2), 025005.

.. [11] Zhang, K., Fu, R., Shaikh, M. J., Ghan, S., Wang, M., Leung, L. R., … Marengo, J. (2017). Inﬂuence of superparameterization and a higher-order turbulence closure on rainfall bias over Amazonia in Community Atmosphere Model version 5. Journal of Geophysical Research: Atmosphere s, 122, 9879-9902, https://doi.org/10.1002/2017JD026576


**SPCAM tested compsets**

 - FSPCAMS: SPCAM using the single moment microphysics
 - FSPCAMM: SPCAM using the double moment microphysics

**SPCAM run-unsupported compsets**
 - FSPCAMCLBS: SPCAM using the single moment microphysics and a custom version of CLUBB 
 - FSPCAMCLBM: SPCAM using the double moment microphysics and a custom version of CLUBB 

-------------------------------------------------------------------------------
CAM-chem tested compsets
-------------------------------------------------------------------------------
CAM-chem tested compsets in CESM2.0
(CAM-chem scientifically supported compsets will be available in CESM2.1)

CAM-chem has a number of compsets/resolutions which are tested in CESM2.0, see Table.  
All available compsets use observed SSTs and sea-ice values and CMIP6 emissions until 2015. 
Specified dynamics compsets are nudged to winds, temperature and surface fluxes and run on 
56 levels, aligned with the MERRA2 vertical levels. Additional SD configurations are tested 
to run with 32 levels that are not availble at this point. Half-degree SD compsets use 
1-degree emissions. Users have to change to half-degree emissions if desired. 

+--------------+-----------------------+-----------------------------------------+-------------+
| Compset Name | tested resolution     |Description                              | Period      |
+==============+=======================+=========================================+=============+
| FCHIST       | f09_f09_mg17          | Historical CAM6-chem using 1 degree FV  | 1979 to 2015|
|              |                       | dycore, using CMIP6 emissions, coupled  |             |
|              |                       | to interactive land and MEGAN2.1        |             |
+--------------+-----------------------+-----------------------------------------+-------------+
| FCSD         | f09_f09_mg17          | Historical CAM6-chem 1deg compset using |             |
|              |                       | MERRA2 analsysis with a 50-hour         | 1980 to 2015|
|              |                       | relaxation. See details in the text     |             |
+--------------+-----------------------+-----------------------------------------+-------------+
| FCSD         | f05_f05_mg17          | Historical CAM6-chem half deg compset   | 1980 to 2015|
|              |                       | using MERRA2 analysis                   |             |
+--------------+-----------------------+-----------------------------------------+-------------+
| FC2010climo  | f09_f09_mg17          | Climatological CAM6-chem using 1 degree | 2010        |
|              |                       | FV dycore, averaged SSTs, emissions, and|             |
|              |                       | lower boundary conditions (2005-2015)   |             |
+--------------+-----------------------+-----------------------------------------+-------------+



-------------------------------------------------------------------------------
WACCM compsets
-------------------------------------------------------------------------------

========================================================
Scientifically supported WACCM atmosphere compsets
========================================================

Scientifically supported WACCM atmosphere configurations for CESM2.0 use TSMLT1 chemistry 
(see :ref:`chemical mechanisms <chemical-mechanisms>` ) and 
0.95° latitude x 1.25° longitude horizontal resolution (f09_f09_mg17). 
Additional scientifically validated configurations will be available in CESM2.1.

+---------+------------+-----------------------------------------+-------------+
| Compset | Resolution | Description                             | Period      |
+=========+============+=========================================+=============+
| FW1850  |f09_f09_mg17| Pre-industrial control WACCM6 using     | 1850        |
|         |            | 1-degree FV dycore, TSMLT1, CMIP6       |             |
|         |            | piControl emissions, year 1850 SSTs,    |             |
|         |            | coupled to interactive land and MEGAN2.1|             |
+---------+------------+-----------------------------------------+-------------+
| FWHIST  |f09_f09_mg17| Historical WACCM6 using 1-degree FV     | 1974 to 2015|
|         |            | dycore, TSMLT1, CMIP6 emissions,        |             |
|         |            | historical SSTs, coupled to interactive |             |
|         |            | land and MEGAN2.1                       |             |
+---------+------------+-----------------------------------------+-------------+
| FW2000  |f09_f09_mg17| Year 2000 WACCM6 1deg compset using     | 2000        |
|         |            | 1-degree FV dycore, TSMLT1, year 2000   |             |
|         |            | CMIP6 emissions, year 2000 SSTs, coupled|             |
|         |            | to interactive land and MEGAN2.1        |             |
+---------+------------+-----------------------------------------+-------------+
| FWSD    |f09_f09_mg17| Historical SD-WACCM6 using GEOS5        | 2005 to 2015|
|         |            | analysis with a 50-hour relaxation,     |             |
|         |            | TSMLT1, CMIP6 emissions,                |             |
|         |            | historical SSTs, coupled to interactive |             |
|         |            | land and MEGAN2.1                       |             |
+---------+------------+-----------------------------------------+-------------+
| FWscHIST|f09_f09_mg17| Historical SC-WACCM6 using 1-degree FV  | 1976 to 2015|
|         |            | dycore, specified chemistry, historical |             |
|         |            | SSTs                                    |             |
+---------+------------+-----------------------------------------+-------------+

========================================================
Tested WACCM atmosphere compsets
========================================================

Tested WACCM atmosphere configurations for CESM2.0 use middle atmosphere (MA) and 
middle atmosphere plus D-region (MAD) chemistry (see 
:ref:`chemical mechanisms <chemical-mechanisms>` ) and 
0.95° latitude x 1.25° longitude horizontal resolution (f09_f09_mg17).

+---------+------------+-----------------------------------------+-------------+
| Compset | Resolution | Description                             | Period      |
+=========+============+=========================================+=============+
| FWmaHIST|f09_f09_mg17| Historical WACCM6 using 1-degree FV     | 1974 to 2015|
|         |            | dycore, MA chemistry, CMIP6 emissions,  |             |
|         |            | historical SSTs, coupled to interactive |             |
|         |            | land and MEGAN2.1                       |             |
+---------+------------+-----------------------------------------+-------------+
|FWmadHIST|f09_f09_mg17| Historical WACCM6 using 1-degree FV     | 1974 to 2015|
|         |            | dycore, MAD chemistry, CMIP6 emissions, |             |
|         |            | historical SSTs, coupled to interactive |             |
|         |            | land and MEGAN2.1                       |             |
+---------+------------+-----------------------------------------+-------------+
| FWmaSD  |f09_f09_mg17| Historical SD-WACCM6 using GEOS5        | 2005 to 2015|
|         |            | analysis with a 50-hour relaxation,     |             |
|         |            | MA chemistry, CMIP6 emissions,          |             |
|         |            | historical SSTs, coupled to interactive |             |
|         |            | land and MEGAN2.1                       |             |
+---------+------------+-----------------------------------------+-------------+
| FWmadSD |f09_f09_mg17| Historical SD-WACCM6 using GEOS5        | 2005 to 2015|
|         |            | analysis with a 50-hour relaxation,     |             |
|         |            | MAD chemistry, CMIP6 emissions,         |             |
|         |            | historical SSTs, coupled to interactive |             |
|         |            | land and MEGAN2.1                       |             |
+---------+------------+-----------------------------------------+-------------+

-------------------------------------------------------------------------------
WACCM-X compsets
-------------------------------------------------------------------------------
WACCM-X has three compsets/resolutions which are supported scientifically.  These compsets 
are detailed in the following table.  A specific compset may be listed below, but unless 
the resolution is also listed, that compset/resolution combination is not scientifically 
supported.  Different resolutions exhibit different behavior and as a result require 
different tunings.  The scientifically supported designation is limited to the specific 
compset/resolution pairs listed in the following table.

**Scientifically supported WACCM-X compsets**

+--------------+----------------------+-----------------------------------------+-------------+
| Compset Name | Supported Resolution |Description                              | Period      |
+==============+======================+=========================================+=============+
| FXHIST       | f19_f19_mg16         | Historical WACCM-X based on CAM4 using  | 2000 to 2015|
|              |                      | 2 degree FV dycore, MA chemistry, CCMI  |             |
|              |                      | emissions, historical SSTs, coupled to  |             |
|              |                      | land, prescribed ice, river             |             |
+--------------+----------------------+-----------------------------------------+-------------+
| FX2000       | f19_f19_mg16         | Year 2000 WACCM-X based on CAM4 2 degree| 2000        |
|              |                      | FV dycore, using MA chemistry, year 2000|             |
|              |                      | CCMI emissions and SSTs, coupled to     |             |
|              |                      | interactive land, prescribed ice, river |             |
+--------------+----------------------+-----------------------------------------+-------------+
| FXSD         | f19_f19_mg16         | Historical SD-WACCM-X based on CAM4     | 2000 to 2015|
|              |                      | using 2 degree FV dycore, MERRA1 with a |             |
|              |                      | 50-hour relaxation, MA chemistry, CCMI  |             |
|              |                      | emissions, historical SSTs, coupled to  |             |
|              |                      | interactive land, prescribed ice, river |             |
+--------------+----------------------+-----------------------------------------+-------------+

It should be noted that these WACCM-X compsets are based on the previous version 4 of 
CAM/WACCM and therefore are not derivatives of the version 6 CAM/WACCM compsets described 
above. 


