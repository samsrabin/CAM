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

- **F**: CAM standalone runs, using an active Land and everything else is prognostic
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
| F2000climo   | f09_f09_mg17         | Climatological 21st century using 1     | 2000 to 2015|
|              |                      | degree fv dycore                        |             |
+--------------+----------------------+-----------------------------------------+-------------+

It should be noted that a number of CAM4 and CAM5-specific compsets have been eliminated from the CAM6 release.  The rationale behind this is that due to changes in code and namelist settings, a user is unable to numerically reproduce CAM4 or CAM5 runs similar to what they would get running CESM1.2. It is recommended that if a user wants to make a true CAM4 or CAM5 run, that they do so using CESM1.2 instead of CESM2.0.

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

  cd cime/scripts
  ./create_newcase --case aqua_case --compset QPC6 --res f09_f09_mg17
  cd aqua_case
  ./case.setup
  ./case.build
  ./case.submit

By default initial conditions from a previous aquaplanet simulation are used. The SST pattern is the APE "QOBS" option, which is used in APE and CFMIP protocols. The atmospheric ozone is specified to be that used for APE. Aerosol emissions are neglected except for sea salt (which is diagnostic), see Medeiros et al. [1]_ for details.

###############################################################
Example 2: Default Aquaplanet with Slab-Ocean Model
###############################################################
To run the standard CAM6 aquaplanet with a 30 m uniform slab-ocean, simply supply the compset name::

  cd cime/scripts
  ./create_newcase --case aqua_case --compset QSC6 --res f09_f09_mg17
  cd aqua_case
  ./case.setup
  ./case.build
  ./case.submit

Note that the slab-ocean model has no ocean heat transport by default; the user must specify an appropriate "qflux" file. To specify such a file::

  ./xmlchange --file env_run.xml --id DOCN_SOM_FILENAME --val path/to/file.nc


###############################################################
Example 3: Aquaplanet with alternate prescribed SST
###############################################################
All of the APE SST profiles are available. To use them invoke the long compset name with the user compset option::

  cd cime/scripts
  ./create_newcase --case cam5_3keq --compset 2000_CAM50_SLND_SICE_DOCN%AQP7_SROF_SGLC_SWAV --user-compset --res f09_f09_mg17 --run-unsupported
  cd cam5_3keq
  ./case.setup
  ./case.build
  ./case.submit

The example uses the 3KEQ SST pattern, which is specified with "AQP7" in the compset name. The analytical SST profiles are defined in the source code (cime/src/components/data_comps/docn/docn_comp_mod.F90). Also note this example switched to CAM5 physics by specifying "CAM50" in the compset name. The run-unsupported flag is required.

###############################################################
Example 4: Aquaplanet with user-specified SST dataset
###############################################################
An arbitrary SST dataset can be specified instead of the default APE SST. To do that, start with the default case, and then change the data ocean mode and specify the file::

  cd cime/scripts
  ./create_newcase --case aqua_sst_case --compset QPC4 --res f19_f19_mg17  --run-unsupported
  cd aqua_case
  ./case.setup
  ./xmlchange --file env_run.xml --id DOCN_MODE --val sst_aquapfile
  ./xmlchange --file env_run.xml --id DOCN_AQP_FILENAME --val sst.nc
  ./case.build
  ./case.submit

Where sst.nc is the user-supplied SST file, which follows the same conventions as SST files used for F compsets. Note this example swtiches to CAM4 physics on a 2-degree grid, so requires the run-unsupported flag.

.. [1] Medeiros, B., D. L. Williamson, and J. G. Olson, 2016: Reference aquaplanet climate in the community atmosphere model, version 5. Journal of Advances in Modeling Earth Systems, doi: http://dx.doi.org/10.1002/2015MS000593

.. [2] Neale, R. B. and B. J. Hoskins, 2000a: A standard test for AGCMs including their physical parametrizations. I: The proposal. Atmos. Sci. Lett., 1, 101-107. http://dx.doi.org/10.1006/asle.2000.0022

.. [3] Williamson, D. L., and Coauthors, 2012: The APE atlas. NCAR Technical Note NCAR/TN-484+STR, doi:10.5065/D6FF3QBR. http://dx.doi.org/10.5065/D6FF3QBR

====================================================================================
CAM Parallel Offline Radiation Tool (PORT - P compsets)
====================================================================================
PORT is used as part of the process for computing radiative forcing and instantaneous radiative forcing.  For effective radiative forcing please see the documentation related to F-case runs.

PORT uses instantaneous samples of the model state to compute the radiative fluxes and heating rates through the atmosphere.  This computation does not include middle and upper atmospheric radiative transfer as implemented in WACCM.  The only prognostic variable is temperature, in the specific PORT configuration to compute radiative forcing that includes the stratospheric adjustment (fixed dynamical heating).

##########################################################################
**STILL BEING EDITED** Example: Verifying a PORT setup
##########################################################################

- Run CESM 9 timesteps outputting in addition to rad, FLNT,FSNT, etc.
- Run PORT using the h1 file - need to output every timestep
- Compare FLNT from step 1 and step 2  (BFB comparison)

##########################################################################
Example: Using PORT to study flux differences due to 4 x CO2
##########################################################################

There are typically three stages to computing radiative forcing

Extracting samples of CESM state

Set up the **user_nl_cam** file
::

 ! Output the radiation data
 rad_data_output=.true.

 ! Specify the radiation data be written to histfile number 2 (rad_data will be in files with cam.h1 in their name)
 rad_data_histfile_num=2
 
 ! Write out the instantaneous rad_data
 rad_data_avgflag='I'
 
 ! Add back in the fields for the output
 fincl1 = 'SOLIN', 'QRS', 'FSNS', 'FSNT','FSNSC', 'FSDSC','FSNR','FLNR',
          'FSNTOA', 'FSUTOA', 'FSNTOAC', 'FSNTC', 'FSDSC', 'FSDS', 'SWCF',
          'QRL', 'FLNS', 'FLDS', 'FLNT', 'LWCF', 'FLUT' ,'FLUTC', 'FLNTC',
          'FLNSC', 'FLDSC'
 
 fincl2 = 'SOLIN', 'QRS', 'FSNS', 'FSNT','FSNSC', 'FSDSC','FSNR','FLNR',
          'FSNTOA', 'FSUTOA', 'FSNTOAC', 'FSNTC', 'FSDSC', 'FSDS', 'SWCF',
          'QRL', 'FLNS', 'FLDS', 'FLNT', 'LWCF', 'FLUT' ,'FLUTC', 'FLNTC',
          'FLNSC', 'FLDSC'
 
 ! Write out every timestep
 nhtfrq=1

:: 

 % ./create_newcase --case test_PORT_setup_orig --res f09_f09_mg17 --compset FHIST_DEV
 % cd test_PORT_setup_orig

 - Using PORT to compute fluxes and heating rates on the extracted samples
 - Using PORT to compute fluxes and heating rates on modifications of the extracted samples

Radiative Forcing is defined as the difference between the top of atmosphere fluxes computed in stages 2 and 3 above.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Step 1:  Extracting CESM state for use in PORT.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A user first needs to set up a run from which the radiation data will be extracted.  In this example, we will use the F2000_DEV compset, but any configuration of CAM may be used, dependent on what the user wishes to study.
::

 % ./create_newcase --case test_forPORT --res f09_f09_mg17 --compset F2000_DEV
 % cd test_forPORT
 
To output the radiation data, the **user_nl_cam** needs to contain the following settings.
::

 ! Output the radiation data
 rad_data_output=.true.

 ! Specify the radiation data be written to histfile number 2 (rad_data will be in files with cam.h1 in their name)
 rad_data_histfile_num=2

 ! Write out the instantaneous rad_data
 rad_data_avgflag='I'


For this test, the user needs to complete the setup/build process and run for at least 16 months.  For a simple verification test, the times can be as short as 9 timesteps.
::

 % ./case.setup
 % ./xmlchange STOP_N=16
 % ./xmlchange STOP_OPTION=nmonths
 % ./case.build
 % ./case.submit

After your job completes, you will have a number of files, including ones with filenames containing "cam.h1".  The "cam.h1" files contain the radiation history which was specified by the namelist and will be used in the next step.  

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Step 2:  Compile and run PORT on extracted radiation data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Configure CESM to construct the PORT executable by running the offline radiation tool.  A new case needs to be created for this step and it will use the special CAM6 PORT compset, PC6
::

 % ./create_newcase --case test_PORT_run_orig --res f09_f09_mg17 --compset PC6
 % cd test_PORT_run_orig

Create a file that contains the full filepaths to all of the h1 files created in step 1.  Setup the namelist in **user_nl_cam** and have it use the fileslist
::

 ! Use the radiation with the latest date (has cam.h1 in the name)
 offline_driver_fileslist='/fullpath/fileslist_orig'
 
 ! turn on Fixed Dynamical Heating in the offline radiation tool (PORT)
 rad_data_fdh=.true.

Compile and submit this run of the original data
::

 % ./case.setup
 % ./xmlchange STOP_N=16
 % ./xmlchange STOP_OPTION=nmonths
 % ./case.build
 % ./case.submit

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Step 3:  Create file with 4xCO2 and compile and run PORT using this new file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a variation to the input files to study the effects the variation has on radiation.  In this case we are quadrupling the CO2 and modifying this via the netcdf utility, ncap for each file.  Further documentation on ncap can be found in the `NCO User Guide <http://nco.sourceforge.net/nco.html>`_.
::

  %ncap -s "rad_co2=4*rad_co2" extracted_file.nc extracted_file_with_quadrupled_co2.nc

Repeat the same setup that you did in Step 2 with a different case name, creating a new list with the modified files and putting this new fileslist in **user_nl_cam**
::

 % ./create_newcase --case test_PORT_run_4xCO2 --res f09_f09_mg17 --compset PC6
 % cd test_PORT_run_4xCO2
 
Setup the namelist in **user_nl_cam** and have it use the file generated in the previous example
::

 ! Use the radiation with the latest date (has cam.h1 in the name)
 offline_driver_fileslist='/fullpath/fileslist_4XCO2'
 
 ! turn on Fixed Dynamical Heating in the offline radiation tool (PORT)
 rad_data_fdh=.true.

Compile and submit this run with the modified data
::

 % ./case.setup
 % ./xmlchange STOP_N=16
 % ./xmlchange STOP_OPTION=nmonths
 % ./case.build
 % ./case.submit

Differencing the resulting output files with those from Example 2 provides the forcing as well as changes in heating rates.

===============================================================================
CAM single column (FSCAM compset)
===============================================================================

SCAM cases are set up for a small set of different locations/dates, called an Intensive Observing Period (IOP) (see XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX for more information).  Each of these IOP's have separate preconfigured settings which are referenced by create_new_case using the --user-mods-dir flag. 

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

If user neglects to specify a --use-mods-dir, then it defaults to a shortened run of ARM97.

The user may modify the sample script **components/cam/bld/scripts/create_scam6_iop**.
 
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

** STILL BEING WRITTEN**

If a user wishes to run SCAM with an IOP location that is not already predefined, the following directions may be used to generate a user defined IOP.  This example will assume that the user wishes to create an IOP at (305 degrees E and 62 degrees N).  It is important to note that the user needs to have the NetCDF Command Language (NCL) installed on their machine as the generation scripts utilizes this library.

        % ./create_newcase --case 

** INSTRUCTIONS FOR USER IOP GO HERE **

** REFERENCE SCRIPT (and make sure it is checked in **

** Running the USER IOP Case **

To run the user iop with SCAM, follow the following steps (here it is a test case over the SGP site output from a CAM Run)

- Decide your iop name (e.g. usrsgp)
- Add this to the script create_scam6_iop
- In the tag you have downloaded, go to the 'usermods_dirs' directory
	e.g. cam6_0_000/components/cam/cime_config/usermods_dirs
- Copy one of the directories for the IOP cases, e.g. cp -r scam_arm97 scam_usrsgp
- Change files in this directory
	Shell commands: XML change commands: Typically the LAT, LON, STARTDATE, START_TOD, STOP_OPTION and STOP_N
	User_nl_cam:  usually just iopfile. May also want to change mfilt (to keep all times on one file) 
- Run create_sca6_iop script with apprpriate IOP (scam_usrsgp in this case)

	
-------------------------------------------------------------------------------
Other CAM compsets
-------------------------------------------------------------------------------

There are a number of other CAM compsets which have not been described in this document. The complete listing of all compsets is found `here <http://www.cesm.ucar.edu/models/cesm2.0/cesm/compsets.html>`_.  Users are cautioned about using compsets that are not scientifically supported or tested.  These compsets are not supported and users may encounter problems or get invalid results using them.

===============================================================================
Super-parameterized CAM (SPCAM)
===============================================================================

Another set of compsets which require a brief description are ones for Super-parameterized CAM (SPCAM). SPCAM implements a 2D cloud resolving model (the System for Atmospheric Modeling SAM, Version 6.8.2) in CAM6.0 to replace its conventional parameterization for moist convection and large-scale condensation. Two different sets are provided. SAM1MOM use one moment SAM microphysics, and is based on Khairoutdinov and Randall [5]_. M2005 uses two moment microphysics from Morrison et al [6]_, and its implementation is based on Wang et al. [7]_; [8]_. In M2005, Explicit-Cloud-Parameterized-Pollutant (ECPP) approach is used to treat cloud processing of aerosols with statistics of cloud properties resolved by the cloud resolving model (Gustafson et al., 2008) [4]_ . It is important to point out that the CLUBB version used in SPCAM is an older version of CLUBB than what is used by CAM6.0 and this customized version of CLUBB resides in the CRM library.

.. [4] Gustafson, W. I., L. K. Berg, R. C. Easter, and S. J. Ghan (2008), The Explicit-Cloud Parameterized-Pollutant hybrid approach for aerosol-cloud interactions in multiscale modeling framework models: tracer transport results, Environ Res Lett, 3(2), 025005.

.. [5]  Khairoutdinov, M. F., and D. A. Randall (2001), A cloud resolving model as a cloud parameterization in the NCAR Community Climate System Model: Preliminary results, Geophys Res Lett, 28(18), 3617-3620.

.. [6]  Morrison, H., Curry, J. A., & Khvorostyanov, V. I. (2005). A new double-moment microphysics parameterization for application in cloud and climate models. Part I: Description. Journal of the atmospheric sciences, 62(6), 1665-1677.

.. [7]  Wang, M., et al. (2011a), The multi-scale aerosol-climate model PNNL-MMF: model description and evaluation, Geosci. Model Dev., 4(1), 137--168, doi:10.5194/gmd-4-137-2011.

.. [8]  Wang, M., S. Ghan, M. Ovchinnikov, X. Liu, R. Easter, E. Kassianov, Y. Qian, and H. Morrison (2011b), Aerosol indirect effects in a multi-scale aerosol-climate model PNNL-MMF, Atmos. Chem. Phys., 11(11), 5431-5455.


**SPCAM tested compsets**

 - FSPCAMS: SPCAM using the single moment microphysics
 - FSPCAMM: SPCAM using the double moment microphysics

**SPCAM run-unsupported compsets**
 - FSPCAMCLBS: SPCAM using the single moment microphysics and a custom version of CLUBB 
 - FSPCAMCLBM: SPCAM using the double moment microphysics and a custom version of CLUBB 

More details about SPCAM can be found at: **????????????????????**

-------------------------------------------------------------------------------
CAM-chem compsets
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
WACCM compsets
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
WACCM-X compsets
-------------------------------------------------------------------------------

