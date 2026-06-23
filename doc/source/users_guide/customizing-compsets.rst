.. _ug63-customizing-compsets:

**************************************
Customizing CAM runs
**************************************

Compsets are useful for easily setting up standard runs of CAM.  Sometimes though a user wants to customize a run.  The first step in doing this is to start with a compset which is close to what a user wants to run and then applying the appropriate modifications.  Users must be mindful of using a compset which has appropriate settings for the experiment to be run.  

It is important to understand that there are two main ways that CAM runs can be modified. 
 - **configuration**: These variables change the way that the actual code is compiled and results in an executable which contains this code setup.  They must be set prior to running ``./case.build``.  If any modifications are made to the configuration after ``./case.build`` has been run, the user must cleanup the prior build using ``case.build --clean-all`` followed by another ``./case.build`` to rebuild the executable.
 - **namelist**: These variables are used to modify the way that CAM is run.  The code does not need to be rebuilt when modifying these settings.

Users need to be careful when modifying CAM's configuration and namelists as it is very easy to create an invalid run.  An example would be with the ``-nlev`` configuration setting as input files are dependent on this setting and may not exist for the requested dynamics/nlev combination.

-------------------------------------------------------------------------------
Changing CAM configurations
-------------------------------------------------------------------------------

All configure options change the way that CAM is built and need to be applied before ``case.build`` is run.  Changing the configuration is done by issuing an ``xmlchange`` command for **CAM_CONFIG_OPTS**.  It is important to make sure that you use the ``--append`` flag to maintain configuration options that are set by the compset.
::

   %./xmlchange --append CAM_CONFIG_OPTS='-cosp'


CAM has numerous options which can modify it's configuration.  A few of the
more widely used settings will be discussed here.  The complete listing of
configure options is at :ref:`arguments to
configure<ug63-arguments-to-configure>`.  More information on xmlchange can
be found at the `xmlchange web page
<http://esmci.github.io/cime/versions/cesm2.2/html/Tools_user/xmlchange.html>`_.

#########################################
Changing the physics
#########################################

There are a number of settings which can change the physics which is run.  Some of the more popular settings are:
 - ``chem <name>`` - Build CAM with the specified prognostic chemistry package
 - ``cosp`` - Enable the COSP simulator package
 - ``ionosphere`` - Specifies the ionopshere model which is used in WACCM-X


-------------------------------------------------------------------------------
Changing CAM namelist options
-------------------------------------------------------------------------------

There are a number of ways that CAM can be modified via namelist settings.
These values control the way the code is run and do not require a recompile
of the code after they are changed.  CAM namelist variables include
settings to tune the model for various quantities, control over output and
many other options.  An example using CMIP5 emissions will be described
here and a full explanation of controlling CAM output can be found at
:ref:`Model Output<ug63-model-output>`.  A complete listing of all of CAM's
namelists is available at `CAM's namelist variables
<http://www.cesm.ucar.edu/models/cesm2/settings/2.2.0/cam_nml.html>`_

#######################################################################
Modifying Namelist settings:  Detailed Example -- Using CMIP5 emissions
#######################################################################
The following steps illustrate how to change the CMIP emissions back to the CMIP5 version.  If a user desires to do this, they may cut/paste the ext_frc_specifier and srf_emis_specifier settings below and put them into their own user_nl_cam.

First the user must create a case and set it up
::

        % cd cime/scripts
        % ./create_newcase --case test_FHIST_CMIP5_emiss --res f09_f09_mg17 --compset FHIST
        % cd test_FHIST
        % ./case.setup


Then the user should make any namelist changes by editing the user_nl_cam file.  Depending on the compset requested, this file may or may not already have information within it.  The user should either add or replace the variables they want to set.  To revert to CMIP5 emissions, we only need to change the values of the files specifed by ext_frc_specifier and srf_frc_specifier.
::

        ext_frc_specifier  = 'H2O -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/emis/elev/H2O_emission_CH4_oxidationx2_elev_1850-2100_CCMI_RCP6_0_c160219.nc',
                             'SO2         -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/emis/ccmi_1960-2008/IPCC_emissions_volc_SO2_1850-2100_1.9x2.5_c130426cycle.nc',
                             'bc_a4       -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_bc_elev_1850-2005_c090804.nc',
                             'num_a1      -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam4_num_a1_elev_1850-2005_c150205.nc',
                             'num_a2      -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_num_a2_elev_1850-2005_c090804.nc',
                             'num_a4      -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam4_num_a4_elev_1850-2005_c150205.nc',
                             'pom_a4      -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_pom_elev_1850-2005_c130424.nc',
                             'so4_a1      -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so4_a1_elev_1850-2005_c090804.nc',
                             'so4_a2      -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so4_a2_elev_1850-2005_c090804.nc'

        srf_emis_specifier = 'DMS       -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/emis/ccmi_1950_2100_rcp6/IPCC_emissions_DMS_surface_1850-2100_1.9x2.5_c130814.nc',
                             'SO2       -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/emis/ccmi_1950_2100_rcp6/IPCC_emissions_SO2_surface_1850-2100_1.9x2.5_c130814.nc',
                             'SOAG      -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_soag_1.5_surf_1850-2005_c130424.nc',
                             'bc_a4     -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_bc_surf_1850-2005_c090804.nc',
                             'num_a1    -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam4_num_a1_surf_1850-2005_c150205.nc',
                             'num_a2    -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_num_a2_surf_1850-2005_c090804.nc',
                             'num_a4    -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam4_num_a4_surf_1850-2005_c150205.nc',
                             'pom_a4    -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_pom_surf_1850-2005_c130424.nc',
                             'so4_a1    -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so4_a1_surf_1850-2005_c090804.nc',
                             'so4_a2    -> /glade/p/cesmdata/cseg/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so4_a2_surf_1850-2005_c090804.nc'

At this point, it is good practice to run preview_namelists and examine the **CaseDocs/atm_in** file to make sure that the requested changes have made it into the CAM namelist file.
::

        % ./preview_namelists

After confirming that the requested namelist changes have been put into the atm_in file, then it is safe to continue with building and submitting the job.
::

        % ./case.build
        % ./case.submit

-------------------------------------------------------------------------------
User-Defined Compsets       
-------------------------------------------------------------------------------

Sometimes a user does not find a specific compset that brings in all of the specific versions of components that they want.  In this case, a user will need to create a user defined compset.  This is something that only an expert user should do as not all versions and variations of components are able to work together.  It is also important to note that creating runs outside of supported compsets may yield incorrect results due to the simple fact that they have not been tuned or tested.  A user needs to be extremely cautious when making their own user-defined compsets.

A simple example will be discussed here, but a more comprehensive writeup can be found in `creating new compsets <http://esmci.github.io/cime/versions/cesm2.2/html/users_guide/compsets.html#creating-new-compsets.html>`_.

Typically users use shortnames in their ``./create_newcase`` commands for example:
::

  % ./create_newcase --case test_FHIST_shortname --res f09_f09_mg17 --compset FHIST

-------------------------------------------------------------------------------
Changing Specified Dynamics Compsets       
-------------------------------------------------------------------------------

Specified dynamics compsets are setup to use specified meteorological
analysis (MERRA2 or GEOS5) to nudge the internally derived meteorology from
the model to the analysis fields. Available compsets are only produced for
a specific date and resolution.  Meteorological data sets (dates and
resolutions) can be downloaded from the repository or from the Research
Data Archive.  Information how to download MERRA2 or GEOS5 data sets can be
found in :ref:`Meteorological Datasets <ug63-meteorological-datasets>`.

To change the start data of a specified dynamics simulation, the new start date and location of the meteorological data have to be adjusted in user_nl_cam, as shown in the following example for Jan 1st 2014 (start date) and using GEOS5 1 deg meteorological analysis. Also met_filenames_list needs to be updated if the simulation covers a different period than included in this file.  One has to make sure to also update nc_data to the start date, even if a branch or hybrid run is performed: ::

 met_data_file          = '2014/GEOS5_09x125_20140101.nc'
 met_data_path          = '/glade/p/cesmdata/cseg/inputdata/atm/cam/met/GEOS5/0.9x1.25'
 met_filenames_list             = '/glade/p/cesmdata/cseg/inputdata/atm/cam/met/GEOS5/0.9x1.25/filenames_list.txt'


The relaxation factor that determines the amount of nudging towards the meteorological analysis is controlled by the user_nl_cam namelist variable  met_rlx_time. The value can be changed and is often set to 5 for a rather strong nudgen (5 hours) or a looser nudging (every 50 hours). 

Changes in specified dynamics simulations may also require to adjust the bnd_top file, that is specific to the resolution of the run and the meteorological analysis fields used, e.g., for GEOS5: ::

 bnd_topo               = '/glade/p/cesmdata/cseg/inputdata/atm/cam/topo/fv_0.9x1.25_nc3000_Nsw042_Nrs008_Co060_Fi001_ZR_geos5_c160702.nc'


To create a new bnd_topo file one has to replace the Surface geopotential (PHIS) from CESM with the one from PHIS of one of the meteorological analysis fields.

If the user wants to create a specified dynamics simulation from a F compset, other changes will be required, including specifing the levels (nlev) and the nudging option (offline_dyn) in env_build.xml, for example: ::

<entry id="CAM_CONFIG_OPTS" value="-phys cam6 -age_of_air_trcs -chem waccm_tsmlt_mam4 -offline_dyn -nlev 88


Furthermore, if the simulation is meant to include the LEAP year, one has to change the calendar option in env_build.xml to GREGORIAN: ::

<entry id="CALENDAR" value="GREGORIAN">


Specified dynamics simulations do not currently run with CISM and simulations have to be setup with SGLC to run, as the case for existing SD compsets. 


Specified dynamics simulations can also be performed using internally generated 3 or 6 hour meteorological data produced by CESM. The internal meteorogical fields can be produced from a free running simulation using a new output string with the following fields: ::

 fincl2        = 'FSDS', 'ICEFRAC', 'LANDFRAC', 'OCNFRAC', 'PHIS', 'PS', 'Q', 'QFLX', 'SHFLX', 'T', 'TAUX', 'TAUY', 'TS', 'U', 'V'
 mfilt          = 1,4
 nhtfrq         = 0,-6



From the output a met_data_path, met_data_file and met_filenames_list has to be defined in the specified dynamics simulation.


