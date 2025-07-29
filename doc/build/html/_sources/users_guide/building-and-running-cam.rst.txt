.. _ug70-building-and-running-cam:

**********************************************************
Building and Running the atmospheric model within CESM
**********************************************************

If you need to install CESM, you will need to download it from a git
repository.  Please refer to `downloading CESM
<http://escomp.github.io/CESM/versions/cesm2.2/html/downloading_cesm.html>`_.  

CAM runs are setup, built, and submitted via the CIME scripts.  These directions apply also to the CAM extension models of CAM-chem, WACCM and WACCM-X.  In all cases, the first step to making a run is to create a case using the CIME create_newcase script, passing it a case name, compset, and model resolution.

The case name is used as the name of the new directory which will contain all the information needed to configure, build, and run the case as well as serving as the case title of the CAM model run. 

The compset is chosen from a set of named configurations that provide
defaults for making one of several common types of runs. Examples of
compset choices include configuring CAM to run in parallel with other
components or specifying a particular set of physics parameterizations to
reproduce a well known intermodel comparison or perhaps configuring CAM
with the appropriate input data to run for different time periods
(historical, present-day, future).  The compset determines the general type
of run to be made and the other elements of the CIME case control system
allow the user to fine-tune the particulars of CAM's physics and dynamics
to meet each user's requirements. Compsets will be described in much more
detail in :ref:`Atmospheric configurations <ug70-atmospheric-configurations>`.
For this chapter, we will be using the compset FHIST.

The resolution parameter of create_newcase, like the compset name, is
chosen from a set of grid configurations. These grid configurations
determine which dynamical core will be used in CAM as well as the spatial
resolution of the grids for each component model participating in the
compset. CAM currently supports the Finite Volume (FV), Spectral Element
(SE), and Eulerian (EUL) dynamical cores. This release adds developmental
support for NOAA’s Finite Volume Cubed Sphere (FV3) dynamical core. The
grid name is usually given in a shortened form called an alias which lists
the grids used by the atmosphere, land, and ocean/ice components. CAM grid
names begin with a letter or two denoting the dynamical core followed by a
string of digits representing the grid resolution. The Finite Volume Grids
begin with the letter 'f', SE grid names begin with 'ne', Eulerian grids
begin with 'T', and FV3 grid names begin with the letter 'C'. Grid
resolutions will be covered in detail in the next section :ref:`Atmospheric
configurations <ug70-atmospheric-configurations>`.


A simple session to configure, build, and run CAM for a historical simulation is illustrated as follows:
::

        % cd cime/scripts
	% ./create_newcase --case test_FHIST --res f09_f09_mg17 --compset FHIST 
	% cd test_FHIST
	% ./case.setup
	% ./case.build
	% ./case.submit

Using the --case, --compset, and --res parameters of create_newcase we have specified that our case will be named test_FHIST, it will be set up to run a historical time period, and CAM will use the Finite Volume dynamical core at a 1-degree resolution. A new directory called test_FHIST is created and contains the files and utilities to fine-tune the CAM configuration and run the experiment. For this example, we will allow the model to use the default configuration settings and simply call case.setup, case.build, and case.submit to finalize the case, build the executable, and run the model.


It is important to note that case.build utilizes parallel compilation and will consume much of the node on which it is run.  On machines like cheyenne, this will result in the user being logged off the system partway through the build process.  On cheyenne, if you are executing the commands in a login node, you must say:
::

% qcmd -- ./case.build

In the example above, the case directory name test_FHIST is stored by CIME in XML as the **CASEROOT** entry. And the job will be run under the directory name stored in the **RUNDIR** XML entry.  The values of these (and all the other XML variables set by CIME) can be seen by using xmlquery. 
::

	% cd test_FHIST
	% ./xmlquery CASEROOT
	% ./xmlquery RUNDIR
	% ./xmlquery --listall

A summary description of the setup/build/submit process can be found at the `CESM quick start <https://escomp.github.io/CESM/versions/cesm2.1/html/quickstart.html>`_.  

Further, detailed information for each of the above steps can be found at: 

- `create_newcase <http://esmci.github.io/cime/versions/cesm2.2/html/users_guide/create-a-case.html>`_ 
- `case.setup <http://esmci.github.io/cime/versions/cesm2.2/html/users_guide/setting-up-a-case.html>`_
- `case.build <http://esmci.github.io/cime/versions/cesm2.2/html/users_guide/building-a-case.html>`_
- `case.submit <http://esmci.github.io/cime/versions/cesm2.2/html/users_guide/running-a-case.html>`_

Users are encouraged to review these sections of the CIME user's guide as they fully describe the CIME case control system used to configure and run CAM.

-------------------------------------------------------
Modifying CAM's compiled codebase (configuration)
-------------------------------------------------------

- **CAM_CONFIG_OPTS**: The settings in this variable are passed directly to
  CAM's configure command and are normally set as part of a compset
  definition. Expert users can modify this variable to add or change the
  default parameters passed to configure.  Some examples of modifiable
  options include changing the physics version (cam4, cam5, cam6) or
  enabling the COSP simulator package, etc...  The list of possible options
  are detailed at :ref:`arguments to configure<arguments-to-configure>`.
  It is important to note that CAM compsets already have this variable set
  and that a user will most likely want to append flags as opposed to
  replacing them.  If the append flag is not used, this variable is reset
  to only include the values specified and all preset values are removed.
  More details on changing CAM's configuration can be found at
  :ref:`customizing compsets<ug70-customizing-compsets>`.

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
<http://www.cesm.ucar.edu/models/cesm2/settings/2.2.0/cam_nml.html>`_
More details on changing CAM's namelist can be found at :ref:`customizing
compsets<ug70-customizing-compsets>`.
