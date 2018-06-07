.. _building-and-running-cam:

**********************************************************
Building and Running the atmospheric model within CESM
**********************************************************

If you need to install CESM, you will need to download it from a git
repository.  Please refer to `downloading CESM
<http://escomp.github.io/cesm/release-cesm2/downloading_cesm.html>`_.  

CAM runs are setup, built and submitted via the cime scripts.  These directions apply also to the CAM extension models of CAM-chem, WACCM and WACCM-X.  In all cases, the first step to making a run is to create a case using a named configuration known as a compset.  Compsets will be described in much more detail in :ref:`Atmospheric configurations <atmospheric-configurations>`.  For this chapter, we will be using the compset FHIST.

A simple session to build the compset FHIST, 1 degree finite volume case and name the case test_FHIST is illustrated as follows:
::

        % cd cime/scripts
	% ./create_newcase --case test_FHIST --res f09_f09_mg17 --compset FHIST 
	% cd test_FHIST
	% ./case.setup
	% ./case.build
	% ./case.submit

It is important to note that case.build utilizes parallel compilation and will consume much of the node on which it is run.  On machines like cheyenne, this will result in the user being logged off the system partway through the build process.  On cheyenne, if you are executing the commands in a login node, you must say:
::

% qcmd -- ./case.build


In the example above, the directory test_FHIST is called the **CASEROOT**.  The job will be run in **RUNDIR**.  The values of these (and all the other xml variables set by cime) can be seen by using xmlquery.
::

	% cd test_FHIST
	% ./xmlquery CASEROOT
	% ./xmlquery RUNDIR

A summary description of the setup/build/submit process can be found at the `CESM quick start <http://escomp.github.io/cesm/release-cesm2>`_.  

Further, detailed information for each of the above steps can be found at: 

- `create_newcase <http://esmci.github.io/cime/users_guide/create-a-case.html>`_ 
- `case.setup <http://esmci.github.io/cime/users_guide/setting-up-a-case.html>`_
- `case.build <http://esmci.github.io/cime/users_guide/building-a-case.html>`_
- `case.submit <http://esmci.github.io/cime/users_guide/running-a-case.html>`_

It is encouraged for users to review these sections as they go into much more detail than is contained here.

-------------------------------------------------------
Modifying CAM's compiled code base (configuration)
-------------------------------------------------------

- **CAM_CONFIG_OPTS**:  The settings in this variable are passed directly to CAM's configure command.  Modifications in this variable change the way CAM is compiled.
  This is where you change the numbers of vertical level, the physics (cam4, cam5), where you enable the COSP simulator package, etc...
  The list of possible options are detailed at :ref:`arguments to configure<arguments-to-configure>`.  It is important to note that CAM compsets already have this variable set and that a user will most likely want to append flags as opposed to replacing them.  If the append flag is not used, this variable is reset to only include the values specified and all preset values are removed.  More details on changing CAM's configuration can be found at :ref:`customizing compsets<customizing-compsets>`.

::

	% cd test_FHIST
	% ./xmlchange --append CAM_CONFIG_OPTS='-cosp'

--------------------------------------
Modifying namelist settings in CAM run
--------------------------------------
To modify CAM namelist settings, add the appropriate keyword/value pair at the end of the $CASEROOT/user_nl_cam file.  If the run needs to change namelist settings in other components, then modify the appropriate $CASEROOT/user_nl_XXX file.

For example, to change the CO2 volume mixing ratio to 400.e-6, modify **user_nl_cam** and add the following line at the end:
::

	co2vmr=400.e-6

To see the result, call ``preview_namelists`` and verify that the new value appears in **CaseDocs/atm_in**.  The exception to this are variables within the **camexp** namelist group (as listed in the link immediately below).  Variables within this group are used internally by CAM's build-namelist utility and modify the resulting namelist. They will not be written out to the the atm_in file.

A complete listing of all of CAM's namelists is available at `CAM's
namelist variables
<http://www.cesm.ucar.edu/models/cesm2/component_settings/cam_nml.html>`_
More details on changing CAM's namelist can be found at :ref:`customizing
compsets<customizing-compsets>`.
