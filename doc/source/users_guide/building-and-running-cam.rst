.. _building-and-running-cam:

**************************
Building and Running CAM within CESM
**************************

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

- **Scientifically supported**:  Specific compset/resolution pairs which have had significant, multi-year runs made and have been studied scientifically.
- **Tested**: One or more tests for this compset have been made using at least one resolution.  Extensive scientific study has not been performed.
- **Unsupported**:  These compsets are setup as a "convenience" for various reasons and they are not supported for science runs.  If a user decides to use one of these compsets, they must also supply the --run-unsupported flag to create_newcase.

**Scientifically supported CAM compsets**

+--------------+-----------------------------------------+---------+
| Compset Name | Description                             | Period  |
+==============+=========================================+=========+
| FHIST_DEV    | Historical current developer            | 1850    |
|              | setup (CAM6)                            |         |
+--------------+-----------------------------------------+---------+
| F2000climo   | Climatological 21st century             | 2000 to |
|              |                                         | 2015    |
+--------------+-----------------------------------------+---------+



**Tested CAM compsets**

+--------------+-----------------------------------------+---------+
| Compset Name | Description                             | Period  |
+==============+=========================================+=========+
|              |                                         |         |
|              |                                         |         |
+--------------+-----------------------------------------+---------+
|              |                                         |         |
|              |                                         |         |
+--------------+-----------------------------------------+---------+


------------------------------
Modifying CAM's configuration 
------------------------------

- **CAM_CONFIG_OPTS**:  The settings in this variable are passed directly to CAM's configure command.  The list of possible options are detailed at :ref:`arguments to configure<arguments-to-configure>`.  It is important to note that CAM compsets already have this variable set and that a user will most likely want to oppend flags as opposed to replacing them.  If the append flag is not used, this variable is reset to only include the values specified and all preset values are removed.

::

	% cd test_FHIST
	%xmlchange --append CAM_CONFIG_OPTS='-nthreads 3'

------------------------------
Modifying namelist settings in CAM run
------------------------------
To modify CAM namelist settings, add the appropriate keyword/value pair at the end of the $CASEROOT/user_nl_cam file.  If the run needs to change namelist settings in other components, then modify the appropriate $CASEROOT/user_nl_XXX file.

For example, to change the CO2 constant to 400, modify **user_nl_cam** and add the following line at the end:
::

	co2_ppmv=400. 

To see the result, call **preview_namelists** and verify that the new value appears in **CaseDocs/atm_in**.

A complete listing of all of CAM's namelists is available at `CAM's namelist variables <http://www.cesm.ucar.edu/models/cesm2.0/namelists/cam_nml.html>`_

==============================
Example:  Using CMIP5 emissions
==============================

==============================
Example:  Setting up a new Single Column (SCAM) run
==============================
