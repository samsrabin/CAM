.. _building-and-running-cam:

************************************
Building and Running CAM within CESM
************************************

If you need to install CESM, please refer to `downloading CESM <http://cesm-development.github.io/cime/doc/build/html/downloading_cesm.html>`_.

CAM runs are setup, built and submitted via the cime scripts.  A simple session to build an FHIST_DEV, 1 degree case and call it test_FHIST is illustrated as follows:
::

        % cd cime/scripts
	% ./create_newcase --case test_FHIST --res f09_f09_mg17 --compset FHIST_DEV 
	% cd test_FHIST
	% ./case.setup
	% ./case.build
	% ./case.submit

In the example above, the directory test_FHIST is called the **CASEROOT**.  The job will be run in **RUNDIR**.  The values of these (and all the other xml variables set by cime) can be seen by using xmlquery.
::

	%cd test_FHIST
	%./xmlquery CASEROOT
	%./xmlquery RUNDIR

A summary description of the setup/build/submit process can be found at the `CESM quick start <http://cesm-development.github.io/cime/doc/build/html/quickstart.html>`_.  

Further, detailed information for each of the above steps can be found at: 

- `create_newcase <http://esmci.github.io/cime/users_guide/create-a-case.html>`_ 
- `case.setup <http://esmci.github.io/cime/users_guide/setting-up-a-case.html>`_
- `case.build <http://esmci.github.io/cime/users_guide/building-a-case.html>`_
- `case.submit <http://esmci.github.io/cime/users_guide/running-a-case.html>`_

In addtion, there is information for `customizing a case <http://esmci.github.io/cime/users_guide/customizing-a-case.html>`_.  

It is encouraged for users to review these sections as they go into much more detail than is contained here.

--------------------------
CAM compsets
--------------------------
CAM compsets include the F, PORT and Q compsets.

- **F**: CAM standalone runs, using an active Land and everything else is prognostic
- **PORT**: Parallel offline radiation tool
- **Q**: Aquaplanet with either prescribed ocean (QP) or slab ocean(QS)

CAM has a number of predefined compsets with different levels of support.  

- **Scientifically supported**:  Specific compset/resolution pairs which have had significant, multi-year runs made and have been studied scientifically.  It is important to note that resolutions which are not listed, are not scientifically supported, have not had tunings performed and should not be used for scientific studies without careful examination of the results.
- **Tested**: One or more tests for this compset have been made using at least one resolution.  Extensive scientific study has not been performed.  The designation of "Tested" simply acknowledges that one or more compset/resolution pair(s) have been confirmed to run without crashing.  No attempts have been made to validate the scientific quality of these runs and tunings have NOT been performed on them.
- **Unsupported**:  These compsets are setup as a "convenience" for various reasons and they are not supported for science runs.  If a user decides to use one of these compsets, they must also supply the --run-unsupported flag to create_newcase.  These compsets may not even compile and run successfully as they have not been tested.

**Scientifically supported CAM compsets**

+--------------+----------------------+-----------------------------------------+-------------+
| Compset Name | supported resolution |Description                              | Period      |
+==============+======================+=========================================+=============+
| FHIST_DEV    | f09_f09_mg17         | Historical current developer            | 1979 to 2015|
|              |                      | setup (CAM6)                            |             |
+--------------+----------------------+-----------------------------------------+-------------+
| F2000climo   | f09_f09_mg17         | Climatological 21st century             | 2000 to 2015|
+--------------+----------------------+-----------------------------------------+-------------+



**Tested CAM compsets**

+--------------+-----------------------------------------+-------------+
| Compset Name | Description                             | Period      |
+==============+=========================================+=============+
|              |                                         |             |
+--------------+-----------------------------------------+-------------+


------------------------------
Modifying CAM's configuration 
------------------------------

- **CAM_CONFIG_OPTS**:  The settings in this variable are passed directly to CAM's configure command.  The list of possible options are detailed at :ref:`arguments to configure<arguments-to-configure>`.  It is important to note that CAM compsets already have this variable set and that a user will most likely want to append flags as opposed to replacing them.  If the append flag is not used, this variable is reset to only include the values specified and all preset values are removed.

::

	% cd test_FHIST
	%xmlchange --append CAM_CONFIG_OPTS='-nthreads 2'

--------------------------------------
Modifying namelist settings in CAM run
--------------------------------------
To modify CAM namelist settings, add the appropriate keyword/value pair at the end of the $CASEROOT/user_nl_cam file.  If the run needs to change namelist settings in other components, then modify the appropriate $CASEROOT/user_nl_XXX file.

For example, to change the CO2 constant to 400, modify **user_nl_cam** and add the following line at the end:
::

	co2_ppmv=400. 

To see the result, call **preview_namelists** and verify that the new value appears in **CaseDocs/atm_in**.

A complete listing of all of CAM's namelists is available at `CAM's namelist variables <http://www.cesm.ucar.edu/models/cesm2.0/namelists/cam_nml.html>`_

=======================================================================
Modifying Namelist settings:  Detailed Example -- Using CMIP5 emissions
=======================================================================
The following steps illustrate how to change the CMIP emissions back to the CMIP5 version.  If a user desires to do this, they may cut/paste the ext_frc_specifier and srf_emis_specifier settings below and put them into their own user_nl_cam.

First the user must create a case and set it up
::

        % cd cime/scripts
        % ./create_newcase --case test_FHIST_CMIP5_emiss --res f09_f09_mg17 --compset FHIST_DEV
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

===================================================
Example:  Setting up a new Single Column (SCAM) run
===================================================
