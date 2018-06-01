.. _customizing-compsets:

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

   %./xmlchange --append CAM_CONFIG_OPTS='-nthreads 2'


CAM has numerous options which can modify it's configuration.  A few of the more widely used settings will be discussed here.  The complete listing of configure options is at :ref:`arguments to configure<arguments-to-configure>`.  More information on xmlchange can be found at the `xmlchange web page <http://esmci.github.io/cime/Tools_user/xmlchange.html>`_.

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
There are a number of ways that CAM can be modified via namelist settings.  These values control the way the code is run and do not require a recompile of the code after they are changed.  CAM namelist variables include settings to tune the model for various quantities, control over output and many other options.  An example using CMIP5 emissions will be described here and a full explanation of controlling CAM output can be found at :ref:`Model Output<model-output>`. .  A complete listing of all of CAM's namelists is available at `CAM's namelist variables <http://www.cesm.ucar.edu/models/cesm2.0/component_namelists/cam_nml.html>`_ 

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

A simple example will be discussed here, but a more comprehensive writeup can be found in `creating new compsets <http://esmci.github.io/cime/users_guide/compsets.html#creating-new-compsets.html>`_.

Typically users use shortnames in their ``./create_newcase`` commands for example:
::

  % ./create_newcase --case test_FHIST_shortname --res f09_f09_mg17 --compset FHIST

A user may also use the long name for the compset which specifies all of the various components and versions.  An example to run the FHIST compset using it's longname is:
::

  % ./create_newcase --case test_FHIST_longname --res f09_f09_mg17 --compset HIST_CAM60_CLM50%BGC-CROP_CICE%PRES_DOCN%DOM_MOSART_CISM2%NOEVOLVE_SWAV

Both of the two examples above will create identical results.  The shortname is an easy to use alias for the longname.  If a user wants to make their own user-defined compset, they will need to supply the longname.  For example, if a user wanted to use CAM5.0 instead of CAM6.0, they could supply the following to the ``./create_newcase`` command:
::

  % ./create_newcase --case test_FHIST_cam5 --res f09_f09_mg17 --compset HIST_CAM50_CLM50%BGC-CROP_CICE%PRES_DOCN%DOM_MOSART_CISM2%NOEVOLVE_SWAV

It is important to note that CAM5.0 is not tuned in the CAM6.0 version of the model, and while a user may be able to make a run using this user-defined compset, they will need to make a careful examination of their results.


