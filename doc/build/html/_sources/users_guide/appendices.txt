.. _appendices:

***************
Appendices
***************

======================
The configure utility
======================

----------------------------------------------
How configure is called from the CESM scripts
----------------------------------------------

The user is able to pass arguments to CAM's configure by issuing an ``xlmchange`` command for  **CAM_CONFIG_OPTS**.  It is important to use the ``--append`` option if a compset's settings are to be maintained.  The CESM scripts use the CAM  script ``components/cam/bld/configure``.   


.. _arguments-to-configure:

----------------------------------------------
Arguments to configure
----------------------------------------------

All configuration options can be specified using command line
arguments to ``configure`` and this is the recommended
practice. Options specified via command line arguments take precedence
over options specified any other way.

At the next level of precedence a few options can be specified by
setting environment variables. And finally, at the lowest precedence,
many options have hard-coded defaults. Most of these are located in
the file
``components/cam/bld/config_files/definition.xml``. A few
that depend on the values of other options are set by logic contained
in the ``configure`` script (a Perl script). The hard-coded defaults
are designed to produce the standard production configurations of CAM.

The configure script allows the user to specify compile time options
such as model resolution, dynamical core type, additional compiler
flags, and many other aspects. The user can type ``configure --help``
for a complete list of available options.

The options may all be specified with either one or two leading
dashes, e.g., ``-help`` or ``--help``. The few options that can be
expressed as single letter switches may not be clumped, e.g., ``-h -s
-v`` may NOT be expressed as ``-hsv``. When multiple options are
listed separated by a vertical bar either version may be used.

####################
CAM configuration
####################


These options will have an effect whether running CAM as part of CESM or running in a CAM standalone mode:

``-[no]age_of_air_trcs``
  Switch on [off] age of air tracers. 
 
  Default: on if ``-waccm_phys``, otherwise off.

``-analytic_ic``
  Enables the (namelist controlled) dycore testing infrastructure

``-aquaplanet``
  Switch on aqua-planet mode.

``-build_chem_proc``
  Switch forces the build of the chemistry preprocessor (primarily for testing).

``-carma <name>`` 
  [ ``none`` (disabled) | ``bc_strat`` (Stratospheric Black Carbon) | ``cirrus`` (Cirrus Clouds) |
  ``cirrus_dust`` (Cirrus Clouds with dust) | ``dust`` (Dust) | ``meteor_impact`` (Meteor Impact) |
  ``meteor_smoke`` (Meteor Smoke) | ``mixed_sulfate`` (Meteor Smoke and Sulfate) | ``pmc`` (Polar Mesospheric Clouds) | 
  ``pmc_sulfate`` (PMC and Sulfate) | ``sea_salt`` (Sea Salt) | ``sulfate`` (Sulfate Aerosols) | 
  ``tholin`` (early earth haze) | ``test_detrain`` (Detrainment) | ``test_growth`` (Particle Growth) | 
  ``test_passive`` (Passive Dust) | ``test_radiative`` (Radiatively Active Dust) | ``test_swelling`` (Sea Salt) | 
  ``test_tracers`` (Asian Monsoon) | ``test_tracers2`` (Guam) ]

  Build CAM with specified CARMA microphysics model

  Default: ``none``

``-chem <name>``
  [ ``trop_mam3`` | ``trop_mam4`` | ``trop_mam7`` | ``trop_mozart`` | ``trop_strat_mam4_vbs`` |
  ``trop_bam`` | ``trop_ghg`` | ``waccm_ma`` | ``waccm_mad_mam4`` | ``waccm_ma_mam4`` |
  ``waccm_ma_sulfur`` | ``waccm_sc`` | ``waccm_sc_mam4`` | ``waccm_tsmlt`` | ``waccm_tsmlt_mam4`` |
  ``waccm_tsmlt_sulfur`` | ``super_fast_llnl`` | ``super_fast_llnl_mam3`` | ``terminator`` | ``none`` ]``.

  Build CAM with specified prognostic chemistry package

  Default: 
   -  ``trop_mam4``:  if the physics package is ``cam6``
   -  ``trop_mam3``:  if the physics package is ``cam5`` 
   -  otherwise ``none``

``-[no]clubb_sgs``    
  Switch on [off] CLUBB_SGS.  

  Default: ``on`` for ``cam6``, otherwise ``off``.

``-clubb_opts`` [``clubb_do_adv`` (Advect CLUBB moments)]
  Comma separated list of CLUBB options to turn on/off.  

  Default: they are all off.

``-co2_cycle``
  This option is usually used with the ``-ccsm_seq`` option as part of
  the configuration for running biogeochemistry (BGC) compsets. It
  modifies the CAM configuration by increasing the number of advected
  constituents by 4. 

  Default: not set.

``-comp_intf`` [``mct`` | ``esmf``]
  Specify the component interfaces 

  Default: ``mct``

``-cosp``
  Enable the COSP simulator package. 

  Default: not set.

``-cppdefs <string>``
  A string of user specified CPP defines appended to Makefile
  defaults. E.g. ``-cppdefs '-DVAR1 -DVAR2'``. Note that a string
  containing whitespace will need to be quoted.

``-dyn`` [``eul`` | ``fv`` | ``se`` ]
  Build CAM with specified dynamical core. 

  Default: ``fv``

``-edit_chem_mech``
  Invokes ``CAMCHEM_EDITOR`` to allow the user to edit the chemistry mechanism file.

``-hgrid <name>``
  Specify horizontal grid. For spectral grids use ``nlatxnlon`` where
  ``nlat`` and ``nlon`` are the number of latitude and longitude grid
  points respectively in the global Gaussian grid (e.g.,
  ``64x128``). For FV grids use ``dlatxdlon`` where ``dlat`` and
  ``dlon`` are the grid cell size in degrees for latitude and
  longitude respectively (e.g., ``1.9x2.5``). For SE grids (cubed
  sphere) use ``neNnpM`` where ``N`` is the number of elements on an
  edge of the cube, and ``M`` is the number of Gauss points on the
  edge of an element (e.g., ``ne30np4``).

``-ionosphere`` [ ``none`` | ``wxi`` | ``wxie`` ].
   Ionophere module used in WACCMX 

   Default: ``none``

``-macrophys`` [ ``rk`` , ``park`` , ``clubb_sgs`` , ``spcam_sam1mom`` , ``spcam_m2005`` , ``none``]
  Specify the macrophysics option  

  Default:
   - ``clubb_sgs``:  if ``cam6`` and clubb_sgs not explicitly turned off 
   - ``park``:  if ``cam6`` and ``noclubb_sgs`` or ``cam5`` 
   - ``rk``:  if ``cam3`` or ``cam4``

``-max_n_rad_cnst`` <n> 
  Maximum number of constituents that are either radiatively active, or in any single diagnostic list for the radiation.  Default: ``30``

``-microphys`` [ ``rk`` , ``mg1`` , ``mg2`` , ``spcam_m2005`` , ``spcam_sam1mom`` , ``none`` ]
  Specify the microphysics package. 

  Default: 
   - ``mg2``:  if the physics package is ``cam6``
   - ``mg1``:  if it is ``cam5``
   - ``rk``:  if it is ``cam3`` or ``cam4``.

``-nadv <n>``
  Set total number of advected species to ``<n>``. If ``-nadv`` is set
  to a larger number than is required by the selected physics and
  chemistry schemes, then the remainder will automatically be used for
  test tracers (N.B. the namelist variable ``tracers_flag`` must be
  set to ``.true.`` to enable the test tracer code.) 

  Default: set to the number required by the selected physics and chemistry schemes.

``-nadv_tt <n>``
  Set number of advected test tracers to <n>. Setting the number of
  test tracers explicitly with this option allows ``build-namelist``
  to automatically enable the test tracer code by setting the
  ``tracers_flag`` namelist variable. 

  Default: ``0``

``-nlev <n>``
  Set number of vertical layers to ``<n>``. 

  Default:
   -  ``32``:  if the physics package is ``cam6``.  
   -  ``30``:  if the physics package is ``cam5``, ``ideal``, or ``adiabatic`` or ``spcam_m2005``. 
   -  ``26``:  if the physics package is ``cam3``, ``cam4`` or ``spcam_sam1mom``. 
   -  ``66``:  if the chemistry package is ``waccm`` and physics package is ``cam4``. 
   -  ``70``:  if the chemistry package is ``waccm`` and physics package is not ``cam4``. 
   -  ``81``:  if ``-waccmx`` is set.
   -  ``126``:  if ``-waccmx`` is set and ``-ionosphere`` is ``wxie``

``-offline_dyn``
  Switch enables the use of offline driver for FV dycore. 

   Default: not set.

``-pbl`` [ ``clubb_sgs`` , ``hb`` (Holtslag and Boville), ``hbr`` (Holtslag, Boville, and Rasch),  ``spcam_sam1mom``, ``spcam_m2005``, ``uw`` (University of Washington), ``none`` ]
  PBL package. 

  Default: 
   - ``clubb_sgs``:  if the physics package is ``cam6`` or the ``-clubb_sgs`` switch is set 
   - ``hb``:  if the physics package is ``cam3`` or ``cam4``
   - ``spacm_m2005``:  if it the physics package is ``spcam_m2005``
   - ``spacm_sam1mom``:  if it the physics package is ``spcam_sam1mom``
   - ``uw``:  if the physics package is ``cam5`` or ``cam6`` and ``-noclubb_sgs``
   - otherwise ``none``

``-pcols <n>``
  Set maximum number of grid columns in a chunk to ``<n>``. 

  Default: 
   - ``1``:  if ``-scam`` is set
   - otherwise ``16`` 

``-pergro``
  Switch enables building CAM for perturbation growth tests. Only
  valid with ``cam3`` and ``cam4`` physics packages.

``-phys`` [ ``cam3`` | ``cam4`` | ``cam5`` | ``cam6`` | ``adiabatic`` | ``held_suarez`` | ``kessler`` | ``spcam_sam1mom`` | ``spcam_m2005`` ]

  Physics package. 

  Default: 
   - ``cam6``:  except
   - ``cam4``:  if ``-waccmx`` or ``-chem`` contains ``_mam`` in its setting

``-prog_species <list>``
  Comma separated list of prognostic mozart species
  packages. Currently available: ``DST,SSLT,SO4,GHG,OC,BC,CARBON16``

``-psubcols <n>``
  Set maximum number of subcolumns in a grid column to ``<n>``. 

  Default: ``1``.

``-rad`` [``rrtmg`` | ``camrt`` | ``none``]
  Radiation package. 

  Default: 
   - ``rrtmg``:  if the physics package is ``cam5``, ``cam6`` or ``spacm_m2005``
   - ``camrt``:  if the physics package is ``cam3``, ``cam4`` or ``spacm_sam1mom``

``-spcam_clubb_sgs``   Turn on the SPCAM version of CLUBB

``-spcam_nx`` <n>      SPCAM x-grid. - defaults to ``4`` (note the CRM requires spcam_nx to be greater than or equal to 4)

``-spcam_ny`` <n>      SPCAM y-grid. - defaults to ``1``

``-spcam_dx`` <n>      SPCAM horizontal grid spacing.

``-spcam_dt`` <n>      SPCAM timestep.

``-unicon``            Switch to turn on the UNICON scheme. Default: ``off``.

``-usr_mech_infile <name>``
  Full pathname of the user supplied chemistry mechanism file.

``-waccm_phys``
  Switch enables the use of WACCM physics in any chemistry configuration. 

  Default: 
   - ``Off``:  unless one of the waccm chemistry options is chosen, then it's automatically turned ``on``.

``-waccmx``
  Build CAM/WACCM with WACCM upper Thermosphere/Ionosphere extended package.

``-zmconv_org``       
  Include parameterization for sub-grid scale convective organization for the ZM deep convective scheme based on Mapes and Neale (2011)


####################
SCAM configuration
####################

``-camiop``
  Configure CAM to generate an IOP file that can be used to drive SCAM. This switch only works with the Eulerian dycore.

``-scam``
  Compiles model in single column mode. Only works with Eulerian dycore.

####################
CAM parallelization
####################

``-[no]smp``
  Switch on [off] SMP parallelism (OpenMP).

``-[no]spmd``
  Switch on [off] SPMD parallelism (MPI). 

############################
General options to configure
############################

``-cache <name>``
  Name of output cache file. 

  Default: ``config_cache.xml``.

``-cachedir <dir>``
  Name of directory where output cache file is written. 

  Default: CAM build directory.

``-ccsm_seq``
  Switch to specify that CAM is being built from within the CESM scripts. This produces Filepath and CCSM_cppdefs files that contains only the paths and CPP macros needed to build a library for the CAM component.

``-help | -h``
  Print usage to STDOUT.

``-silent | -s``
  Turns on silent mode - only fatal messages printed to STDOUT.

``-test``
  Switch on testing of Fortran compiler and linking to external libraries.

``-verbose | -v``
  Turn on verbose echoing of settings made by configure.

``-version``
  Echo the repository tag name used to check out this CAM source tree.

#########################################
Surface components used in standalone CAM
#########################################

Options for surface components used in standalone CAM mode:

``-ocn`` [ ``docn`` | ``dom`` | ``som`` | ``socn`` | ``aquaplanet`` ]
  Specify ocean component.  Use data ocean model (``docn`` or ``dom``), stub ocean (``socn``), or aqua planet 
  ocean (``aquaplanet``) in cam build.  When built from the CESM scripts the value of ocn may be set to 
  pop.  This doesn't impact how CAM is built, only how attributes are matched when searching for 
  namelist defaults.  If ocn is set to ``som`` then the ``docn`` component is used.

  Default: 
   - ``aquaplanet``:  if ``-aquaplanet`` set
   -  otherwise ``socn`` 

######################
CAM standalone build
######################

Options for building CAM via standalone scripts:

``-cam_bld <dir>``
  Directory where CAM will be built. This is where configure will write the output files it generates (Makefile, Filepath, etc...).

  Default: ``.``

``-cam_exe <name>``
  Name of the CAM executable. 

  Default: ``cam``.

``-cam_exedir <dir>``
  Directory where CAM executable will be created. Default: CAM build directory.

``-cc <name>``
  User specified C compiler. Default: Depends on the OS and the Fortran compiler.

``-cflags <string>``
  A string of user specified C compiler options appended to the default options set in Makefile.

``-debug``
  Switch to turn on building CAM with compiler options for debugging. The specific options are compiler dependent. These flags are set in the ``Makefile.in`` template file.

``-esmf_libdir <dir>``
  Directory containing ESMF library and the ``esmf.mk`` file. If this option is specified then the external ESMF library will be used in place of the ESMF-WRF time manager code which is provided in the CESM source distribution.

``-fc <name>``
  User specified Fortran compiler. 

  Default: Depends on the OS and whether MPI is enabled.

``-fc_type [pgi | lahey | intel | pathscale | gnu | xlf]``
  Type of the Fortran compiler. This argument is used in conjunction with the ``-fc`` argument when the name of the fortran compiler refers to a wrapper script (e.g., ``mpif90`` or ``ftn``). In this case the user needs to specify the type of Fortran compiler that is being invoked by the wrapper script. 

  Default: Depends on the name of the Fortran compiler.

``-fflags <string>``
  A string of user specified Fortran compiler options appended to the default options set in the Makefile. See ``-fopt`` to override optimization flags.

``-fopt <string>``
  A string of user specified Fortran compiler optimization flags. Overrides Makefile defaults.

``-gmake <name>``
  Name of the GNU make program on your system. Supply the absolute pathname if the program is not in your path (or fix your path). This is only needed by configure for running tests via the ``-test`` option.

``-lapack_libdir <dir>``
  Directory containing LAPACK library.

``-ldflags <string>``
  A string of user specified load options. Appended to Makefile defaults.

``-linker <name>``
  User specified linker. 

  Default: use the Fortran compiler.

``-mpi_inc <dir>``
  Directory containing MPI include files.

``-mpi_lib <dir>``
  Directory containing MPI library.

``-nc_inc <dir>``
  Directory containing NetCDF include files.

``-nc_lib <dir>``
  Directory containing NetCDF library.

``-nc_mod <dir>``
  Directory containing NetCDF module files.

``-pnc_inc <dir>``
  Directory containing PnetCDF include files.

``-pnc_lib <dir>``
  Directory containing PnetCDF library.

``-rad_driver``
  Build CAM with the offline radiation driver. This produces an executable that can only be used for offline radiation calculations.

``-target_os <name>``
  Override the OS setting for cross platform compilation from the following list ``[aix|irix|linux| bgl|bgp ]``. 

  Default: OS on which configure is executed as defined by the Perl $OSNAME variable.

``-usr_src <dir1>[,<dir2>[,<dir3>[...]]]``
  Directories containing user source code. Note that these directories will also be searched for modified versions of the files needed by the ``build-namelist`` script, e.g., the namelist definition and use case files.

===========================
The build-namelist utility
===========================

The ``build-namelist`` utility builds namelists (and on occasion other
types of input files) which specify run-time details for CAM and the
components it's running with in standalone mode. When executed from
the CESM scripts it only produces a namelist file for the CAM
component (in the file ``atm_in``), and a namelist file for control of
dry deposition which is shared by CAM and CLM (in the file
``drv_flds_in``).  

The task of constructing a correct namelist has become extremely
complex due to the large number of configurations supported by
CAM. Editing namelists by hand is an extremely fragile process due to
the number of variables that need to be set, and to the many
interdependencies among them. *We strongly discourage editing
namelists by hand.* All customizations of the CAM namelist are
possible by making use of the ``build-namelist`` command line options.

Some of the important features of ``build-namelist`` are:

* All valid namelist variables are known to ``build-namelist``. So an
  invalid variable specified by the user (supplied either by the
  ``-infile`` or ``-namelist`` options) will cause ``build-namelist`` to
  fail with an error message telling which namelist variable is
  invalid. This is a big improvement over a runtime failure caused by an
  invalid variable which typically gives no hint as to which variable
  caused the problem.

* In addition to knowing all valid variable names and their types,
  ``build-namelist`` also knows which namelist group each variable
  belongs to. This means that the user only needs to specify variable
  names to ``build-namelist`` and not the group names. The ``-infile``
  and ``-namelist`` options still require valid namelist syntax as
  input, but the group name is ignored. So all variables can be put in
  a single group with an arbitrary name, for example, "&xxx ... /"
  where "xxx" is the namelist group name.

* Since ``build-namelist`` knows all namelist variables specified by
  the user it is able to do consistency checking. In general however,
  ``build-namelist`` assumes that the user is the expert and will not
  override a user specification unless there is a major inconsistency,
  for example if variables have been set to use parameterizations
  which can not be run at the same time.

* All configurations have namelist variables that must be specified,
  and ``build-namelist`` has a mechanism to provide default values for
  these variables. When an appropriate default value cannot be found
  then ``build-namelist`` will fail with an informative message.

* When running a configuration for the first time there are often many
  input datasets that may not be in the local input data directory. In
  order to facilitate getting the required datasets ``build-namelist``
  has an option, ``-test``, that can be used to produce a complete
  list of required datasets and report status of whether or not they
  are present in the local directory. This list can then be used to
  obtain the needed datasets from the CESM SVN input data repository.

* One required input for ``build-namelist`` is a configuration cache
  file produced by a previous invocation of ``configure``
  (``config_cache.xml`` by default). ``build-namelist`` looks at this
  file to determine the features of the CAM executable, such as the
  dynamical core and horizontal resolution, that affect the default
  specifications for namelist variables. The default values themselves
  are specified in the file
  ``components/cam/bld/namelist_files/namelist_defaults_cam.xml``,
  and in the use case files located in the directory
  ``components/cam/bld/namelist_files/use_cases/``.

* The other required input for ``build-namelist`` is the root
  directory for the input datasets. This is required since nearly all
  input files must be specified using absolute filepaths, but the
  defaults are stored as filepaths which are relative to the root
  directory. It is expected that the actual location of the root
  directory is something that will be resolved at runtime. The way
  this is done is to either specify it using the ``-csmdata``
  argument, or to set the environment variable ``CSMDATA``.

The methods for setting the values of namelist variables, listed from highest to lowest precedence, are:

1. using specific command-line options, e.g., ``-case`` and ``-runtype``,
2. using the ``-namelist`` option,
3. setting values in a file specified by ``-infile``,
4. specifying a ``-use_case`` option,
5. setting values in the namelist defaults file.

* The first four of these methods for specifying namelist variables
  are the ones available to the user without requiring code
  modification. Any namelist variable recognized by CAM can be
  modified using method 2 or 3. The final two methods represent
  defaults that are hard coded as part of the code base.


----------------------------------------------
Options to build namelist
----------------------------------------------

To get a list of all available options, type ``build-namelist --help``. Available options are also listed just below.

The following options may all be specified with either one or two leading dashes, e.g., ``-help`` or ``--help``. The few options that can be expressed as single letter switches may not be clumped, e.g., ``-h -s -v`` may NOT be expressed as ``-hsv``. When multiple options are listed separated by a vertical bar either version may be used.

``-case <name>``
  Case identifier up to 80 characters. This value is used to set the case_name variable in the driver namelist. Default: ``camrun``

``-config <filepath>``
  Read the specified configuration cache file to determine the configuration of the CAM executable. Default: ``config_cache.xml``.

``-csmdata <dir>``
  Root directory of CESM input data. Can also be set by using the ``CSMDATA`` environment variable.

``-dir <dir>``
  Directory where output namelist files for each component will be written, i.e., ``atm_in``, ``drv_in``, ``ice_in``, ``lnd_in`` and ``ocn_in``. Default: current working directory.

``-help | -h``
  Print usage to STDOUT.

``-ignore_ic_date``
  Ignore the date attribute of the initial condition files when determining the default.

``-ignore_ic_year``
  Ignore just the year part of the date attribute of the initial condition files when determining the default.

``-infile <filepath>``
  Specify a file containing namelists to read values from.

``-inputdata <filepath>``
  Writes out a list of pathnames for required input datasets to the specified file.

``-namelist <namelist>``
  Specify namelist settings directly on the commandline by supplying a string containing FORTRAN namelist syntax, e.g., -``namelist "&atm stop_option='ndays' stop_n=10 /"``

``-ntasks <n>``
  Specify the number of MPI tasks to be used by the run. This is only used to set a default decomposition for the FV dycore, i.e., the npr_yz variable.

``-runtype [startup|continue|branch]``
  Type of simulation. Default: startup.

``-silent | -s``
  Turns on silent mode - only fatal messages issued.

``-test``
  Enable checking that input datasets exist on local filesystem. This is also a convenient way to generate a list of the required input datasets for a model run.

``-use_case <name>``
  Specify a use case.

``-verbose | -v``
  Turn on verbose echoing of informational messages.

``-version``
  Echo the source code repository tag name used to check out this CAM distribution.

----------------------------------------------
Environment variables used by build namelist
----------------------------------------------

The environment variables recognized by ``build-namelist`` are presented below.

``CSMDATA``

Root directory of CESM input data. Note that the commandline argument
``-csmdata`` takes precedence over the environment variable.

``OMP_NUM_THREADS``

If values of the specific variables that set the thread count for each
component, i.e., ``atm_nthreads``, ``cpl_nthreads``, ``ice_nthreads``,
``lnd_nthreads``, or ``ocn_nthreads``, are set via the ``-namelist``,
or ``-infile`` options, then these values have highest precedence. The
``OMP_NUM_THREADS`` environment variable has next highest precedence
for setting any of the component specific thread count
variables. Lowest precedence for setting these variables is the value
of ``nthreads`` from the configure cache file.


----------------------------------------------
CAM Namelist variables
----------------------------------------------

A searchable (or browsable) page containing all CAM namelist variables
is `here <http://www.cesm.ucar.edu/models/cesm2.0/component_namelists/cam_nml.html>`_.


=============================
Sample Interactive Session
=============================

**Brian Eaton will review and amend this section to the end of the chapter**

The following sections present an interactive C shell session to build
and run a default version of CAM. Most often these steps will be
encapsulated in shell scripts. An important advantage of using a
script is that it acts to document the run you've done. Knowing the
source code tree, and the ``configure`` and ``build-namelist``
commands provides all the information needed to replicate a run.

For the interactive session the shell variable ``camcfg`` is set to
the directory in the source tree that contains the CAM ``configure``
and ``build-namelist`` utilities (``models/atm/cam/bld``).
::

   Much of the example code in this document is set off in sections like this.
   Many examples refer to files in the distribution source tree using
   filepaths that are relative to distribution root directory, which we
   denote, using a UNIX shell syntax, by $CAM_ROOT.  The notation indicates
   that CAM_ROOT is a shell variable that contains the filepath.  This could
   just as accurately be referred to as $CCSMROOT since the root directory of
   the CESM distribution is the same as the root of the CAM distribution
   which is contained within it.

-------------------------------------------
Configuring CAM for serial execution
-------------------------------------------

We start by changing into the directory in which the CAM executable
will be built, and then setting the environment variables INC_NETCDF
and LIB_NETCDF which specify the locations of the NetCDF include files
and library. This information is required by ``configure`` in order
for it to produce the ``Makefile``. The NetCDF library is require by
all CAM builds. The directories given are just examples; the locations
of the NetCDF include files and library are system dependent. The
information provided by these environment variables could
alternatively be provided via the commandline arguments ``-nc_inc``
and ``-nc_lib``.

**NOTE:** A common problem is to encounter build failures due to
specifying a NetCDF library which was built with a different Fortran
compiler than the one used to build CAM. Consult your system's
documentation (or some other knowledgeable source) to find the
location of the NetCDF library which was built with the Fortran
compiler you intend to use.  
::

   % cd /work/user/cam_test/bld
   % setenv INC_NETCDF /usr/local/include
   % setenv LIB_NETCDF /usr/local/lib


Next we issue the ``configure`` command (see the example just
below). The argument ``-dyn fv`` specifies using the FV dynamical core
which is the default for CAM5, but we recommend always adding the
dynamical core (dycore for short) argument to ``configure`` commands
for clarity. The argument ``-hgrid 10x15`` specifies the horizontal
grid. This is the coarsest grid available for the FV dycore in CAM and
is often useful for testing purposes.

We recommend using the ``-test`` option the first time CAM is built on
any machine. This will check that the environment is properly set up
so that the Fortran compiler works and can successfully link to the
NetCDF and MPI (if SPMD is enabled) libraries. Furthermore, if the
configuration is for serial execution, then the tests will include
both build and run phases which may be useful in exposing run time
problems that don't show up during the build, for example when shared
libraries are linked dynamically. If any tests fail then it is useful
to rerun the ``configure`` command and add the ``-v`` option which
will produce verbose output of all aspects of the configuration
process including the tests. If the configuration is for an SPMD
build, then no attempt to run the tests will be made. Typically MPI
runs must be submitted to a batch queue and are not enabled from
interactive sessions. Also the method of launching an MPI job is
system dependent. But the build and static linking will still be
tested.
::

   % $camcfg/configure -dyn fv -hgrid 10x15 -nospmd -nosmp -test 
   Issuing command to the CICE configure utility:
      $CAM_ROOT/models/ice/cice/bld/configure -hgrid 10x15 -cice_mode prescribed \
           -ntr_aero 0 -nx 24 -ny 19 -bsizex 6 -bsizey 19 -maxblocks 4 -decomptype blkrobin \
           -cache config_cache_cice.xml -cachedir /work/user/cam_test/bld
   CICE configure done.
   MCT configure is done.
   creating /work/user/cam_test/bld/Filepath
   creating /work/user/cam_test/bld/Makefile
   creating /work/user/cam_test/bld/config.h
   creating /work/user/cam_test/bld/config_cache.xml
   Looking for a valid GNU make... using gmake
   Testing for Fortran 90 compatible compiler... using pgf95
   Test linking to NetCDF library... ok
   CAM configure done.

The first line of output from the ``configure`` command is an echo of
the system command that CAM's ``configure`` issues to invoke the CICE
``configure`` utility. CICE's ``configure`` is responsible for setting
the values of the CPP macros that are needed to build the CICE code.

After the CICE ``configure`` is complete the MCT ``configure`` script
is executed to create the Makefile for building MCT as a separate
library. There is a status line output to indicate success of that
process.

The next four lines of output inform the user of the files being
created by ``configure``. All these files except for the cache file
are required to be in the CAM build directory, so it is generally
easiest to be in that directory when ``configure`` is invoked.

The output from the ``-test`` option tells us that ``gmake`` is a GNU
Make on this machine; that the Fortran compiler is ``pgf95``; and that
code compiled with the Fortran compiler can be successfully linked to
the NetCDF library. The CAM ``configure`` script is the place where
the default compilers are specified. On Linux systems the default is
``pgf95``. Finally, since this is a serial configuration no test for
linking to the MPI library was done.

--------------------------------------
Specifying the Fortran compiler
--------------------------------------

In the previous section the ``configure`` command was issued without
specifying which Fortran compiler to use. For that to work we were
depending on the CAM ``configure`` script to select a default
compiler. One of the differences between the CAM standalone build and
a build using the CESM scripts is that CAM's ``configure`` provides
defaults based on the operating system name (as determined by the Perl
internal variable ``$OSNAME``), while the CESM scripts require the
user to specify a specific machine (and compiler if the machine
supports more than one) as an argument to the ``create_newcase``
command.

The CAM makefile currently recognizes the following operating systems and compilers.
::

   AIX
   xlf95_r, mpxlf95_r

   Linux
   pgf95 (this is the default)

   lf95
   
   ifort
   
   gfortran (has had minimal testing)
   
   pathf90 (has had minimal testing)
   
   Darwin
   xlf95_r, mpxlf95_r, ifort
   
   BGL
   blrts_xlf95
   
   BGP
   mpixlf95_r

The above list contains two IBM Blue Gene machines; BGL and BGP. The
executables on these machines are produced by cross compilation and
hence the ``configure`` script is not able to determine the machine
for which the build is intented. In this case the user must supply
this information to ``configure`` by using the ``-target_os`` option
with the values of either ``bgl`` or ``bgp``.

On a Linux platform several compilers are recognized with the default
being ``pgf95``. It is assumed that the compiler to be used is in the
user's path (i.e., in one of the directories in the PATH environment
variable). If it isn't then the ``-test`` option will issue an error
indicating that the compiler was not found.

Suppose for example that one would like to use the Intel compiler on a
local Linux system. The CAM makefile recognizes ``ifort`` as the name
of the Intel compiler. To invoke this compiler use the ``-fc``
argument to ``configure``. The following example illustrates the
output you get when the compiler you ask for isn't in your PATH: 
::

   % $camcfg/configure -fc ifort -dyn fv -hgrid 10x15 -nospmd -nosmp -test 
   Issuing command to the CICE configure utility:
   $CAM_ROOT/models/ice/cice/bld/configure -hgrid 10x15 -cice_mode prescribed \
   -ntr_aero 0 -ntasks 1 -nthreads 1 -cache config_cache_cice.xml \
   -cachedir /work/user/cam_test/bld
   CICE configure done.
   FAILURE: MCT configure

In previous CAM versions this problem would be caught by the ``-test``
option, but with the addition of MCT's configure the problem is now
detected there. By default MCT will be build in a subdirectory of the
build directory named ``mct``. That directory will contain a file,
``config.log``, which should be examined to track down the cause of
the failure. In this case the file contains the message:
::

   $CAM_ROOT/models/utils/mct/configure: line 3558: ifort: command not found

This means that the PATH environment variable has not been correctly
set. The first thing to try is to verify the directory that contains
the compiler, and then to prepend this directory name to the PATH
environment variable.

**NOTE:**  We have made progress porting CAM to the ``gfortran`` compiler, but it is still not regularly tested or used for production work.

-------------------------------------
Dealing with compiler wrappers
-------------------------------------

Another instance where the user needs to supply information about the
Fortran compiler type to configure is when the compiler is being
invoked by a wrapper script. A common example of this is using the
``mpif90`` command to invoke the Fortran compiler that was used to
build the MPI libraries. This facilitates correct compilation and
linking with the MPI libraries without the user needing to add the
required include and library directories, or library names. The same
benefit is provided by the ``ftn`` wrapper used on Cray XT and XE
systems. In the usual case that a Linux OS is being used, since the
CAM makefile will not recognize these compiler names, it will assume
that the default compiler is being used, and thus will supply compiler
arguments that are appropriate for ``pgf90``. The compilation will
fail if ``pgf90`` is not the compiler being invoked by the wrapper
script (invoking configure with the ``-test`` option is a good way to
catch this problem). The way to specify which Fortran compiler is
being invoked by a wrapper script is via the ``-fc_type`` argument to
configure. This argument takes one of the values ``pgi``, ``lahey``,
``intel``, ``pathscale``, ``gnu``, or ``xlf``.

CAM's ``configure`` script attempts to determine the compiler type
when a compiler specific name is used. It does so by a regular
expression match against the unique part of specific compiler names
(e.g., any compiler name matching 'pgf' will be given the default type
of pgi). If the default is wrong then the user will need to manually
override the default via setting the ``-fc_type`` argument.

---------------------------------------------
Configuring CAM for parallel execution
---------------------------------------------

Before moving on to building CAM we address configuring the executable
for parallel execution. But before talking about configuration
specifics let's briefly discuss the parallel execution capabilities of
CAM.

CAM makes use of both distributed memory parallelism implemented using
MPI (referred to throughout this document as `SPMD
<http://en.wikipedia.org/wiki/SPMD>`_), and shared memory parallelism
implemented using OpenMP (referred to as `SMP
<http://en.wikipedia.org/wiki/Symmetric_multiprocessing>`_). Each of
these parallel modes may be used independently of the other, or they
may be used at the same time which we refer to as "hybrid mode". When
talking about the SPMD mode we usually refer to the MPI processes as
"tasks", and when talking about the SMP mode we usually refer to the
OpenMP processes as "threads". A feature of CAM which is very helpful
in code development work is that the simulation results are
independent of the number of tasks and threads used.

Now consider configuring CAM to run in pure SPMD mode. Prior to the
introduction of CICE as the sea ice model SPMD was turned on using the
``-spmd`` option. But if we try that now we find the following:
::

   % $camcfg/configure -dyn fv -hgrid 10x15 -spmd -nosmp
   **    ERROR: If CICE decomposition parameters are not specified, then
   **    -ntasks must be specified to determine a default decomposition
   **    for a pure MPI run.  The setting was:  ntasks=

A requirement of the CICE model is that its grid decomposition (which
is independent of CAM's decomposition even when the two models are
using the same horizontal grid) must be specified at build time. In
order for CICE's ``configure`` to set the decomposition it needs to
know how much parallelism is going to be used. This information is
provided by specifying the number of MPI tasks that the job will use
via setting the ``-ntasks`` argument.

**NOTE:** The default CICE decomposition can be overridden by setting
  it explicitly using the ``configure`` options provided for that
  purpose.

When running CAM in SPMD mode the build procedure must be able to find
the MPI include files and library. The recommended method for doing
this is to use scripts provided by the MPI installation to invoke the
compiler and linker. On Linux systems a common name for this script is
``mpif90``. The CAM Makefile does not currently use this script by
default on Linux platforms, so the user must explicitly specify it on
the configure commandline using the ``-fc`` argument:
::

   % $camcfg/configure -fc mpif90 -fc_type pgi -cc mpicc -dyn fv -hgrid 10x15 -ntasks 6 -nosmp -test
   Issuing command to the CICE configure utility:
   $CAM_ROOT/models/ice/cice/bld/configure -hgrid 10x15 -cice_mode prescribed \
   -ntr_aero 0 -ntasks 6 -nthreads 1 -cache config_cache_cice.xml \
   -cachedir /work/user/cam_test/bld
   CICE configure done.
   MCT configure is done.
   creating /work/user/cam_test/bld/Filepath
   creating /work/user/cam_test/bld/Makefile
   creating /work/user/cam_test/bld/config.h
   creating /work/user/cam_test/bld/config_cache.xml
   Looking for a valid GNU make... using gmake
   Testing for Fortran 90 compatible compiler... using mpif90
   Test linking to NetCDF library... ok
   Test linking to MPI library... ok
   CAM configure done.

Notice that the number of tasks specified to CAM's ``configure`` is
passed through to the commandline that invokes the CICE
``configure``. Generally any number of tasks that is appropriate for
CAM to use for a particular horizontal grid will also work for
CICE. But it is possible to get an error from CICE at this point in
which case either the number of tasks requested should be adjusted, or
the options that set the CICE decomposition explicitly will need to be
used.

**NOTE:** The use of the ``-ntasks`` argument to configure implies
  building for SPMD. This means that an MPI library will be
  required. Hence, the specification ``-ntasks 1`` is not the same as
  building for serial execution which is done via the ``-nospmd``
  option and does not require a full MPI library. (Implementation
  detail: when building for serial mode a special serial MPI library
  is used which basically provides a complete MPI API, but doesn't do
  any message passing.)

Next consider configuring CAM to run in pure SMP mode. Similarly to
SPMD mode, prior to the introduction of the sea ice component CICE the
SMP mode was turned on using the ``-smp`` option. But with CAM5 that
will result in the same error from CICE that we obtained above from
attempting to use ``-spmd``. If we are going to run the CICE code in
parallel, we need to specify up front how much parallelism will be
used so that the CICE configure utility can set the CPP macros that
determine the grid decomposition. We specify the amount of SMP
parallelism by setting the ``-nthreads`` option as follows:
::

   % $camcfg/configure -dyn fv -hgrid 10x15 -nospmd -nthreads 6 -test
   Issuing command to the CICE configure utility:
   $CAM_ROOT/models/ice/cice/bld/configure -hgrid 10x15 -cice_mode prescribed \
   -ntr_aero 0 -ntasks 1 -nthreads 6 -cache config_cache_cice.xml \
  -cachedir /work/user/cam_test/bld
   CICE configure done.
   ...

We see that the number of threads has been passed through to the CICE ``configure`` command.

**NOTE:** The use of the ``-nthreads`` argument to configure implies
  building for SMP. This means that the OpenMP directives will be
  compiled. Hence, the specification ``-nthreads 1`` is not the same
  as building for serial execution which is done via the ``-nosmp``
  option and does not require a compiler that supports OpenMP.

Finally, to configure CAM for hybrid mode, simply specify both the ``-ntasks`` and ``-nthreads`` arguments to configure.

-------------------
Building CAM
-------------------

Once ``configure`` is successful, build CAM by issuing the make command:
::

   % gmake -j2  >&! make.out

The argument ``-j2`` is given to allow a parallel build using 2
processes. The optimal number of processes to use depends on the
compute resource available. There is a lot of available parallelism in
the build procedure, so using 16 or even 32 processes may speed things
up considerably. Note however that the build happens in shared (not
distributed) memory. So specifying more processes than there are
processors in a shared memory node is generally not helpful (although
the presence of hyperthreading or SMT on a node may provide an
advantage to specifying twice the number of processors).

It is useful to redirect the output from ``make`` to a file for later
reference. This file contains the exact commands that were issued to
compile each file and the final command which links everything into an
executable file. Relevant information from this file should be
included when posting a bug report concerning a build failure.

----------------------------
Building the Namelist
----------------------------

The first step in the run procedure is to generate the namelist
files. The safest way to generate consistent namelist settings is via
the ``build-namelist`` utility. Even in the case where only a slight
modification to the namelist is desired, the best practice is to
provide the modified value as an argument to ``build-namelist`` and
allow it to actually generate the namelist files.

**NOTE:** The default configuration of CAM using the ``cam5`` physics
  package requires that about 60 datasets and dozens of parameter
  values be specified in order to run correctly. Trying to manage
  namelists of that complexity by hand editing files is extremely
  error prone and is strongly discouraged. User modifications to the
  default namelist settings can be made in a number of ways while
  still letting ``build-namelist`` actually generate the final
  namelist. In particular, the ``-namelist``, ``-infile``, and
  ``-use_case`` arguments to ``build-namelist`` are all mechanisms by
  which the user can override default values or specify additional
  namelist variables and still allow ``build-namelist`` to do the
  error and consistency checking which makes the namelist creation
  process more robust.

The following interactive C shell session builds a default namelist
for CAM. We assume that a successful execution of ``configure`` was
performed in the build directory as discussed in the previous
sections. This is an essential prerequisite because the
``config_cache.xml`` file produced by configure is a required input
file to ``build-namelist``. One of the responsibilities of
``build-namelist`` is to set appropriate default values for many
namelist variables, and it can only do this if it knows how the CAM
executable was configured. That information is present in the cache
file. As in the previous section the shell variable ``camcfg`` is set
to the CAM configuration directory (``components/cam/bld``).

We begin by changing into the directory where CAM will be run. It is
usually convenient to have the run directory be separate from the
build directory. Possibly a number of different runs will be done that
each need to have a separate run directory for the output files, but
will all use the same executable file from a common build
directory. It is, of course, possible to execute ``build-namelist`` in
the build directory since that's where the cache file is and so you
don't need to specify to ``build-namelist`` where to find that file
(it looks in the current working directory by default). But then,
assuming you plan to run CAM in a different directory, all the files
produced by ``build-namelist`` need to be copied to the run
directly. If you're running ``configure`` and ``build-namelist`` from
a script, then you need to know how to specify the filenames for the
files that need to be copied. For this reason it's more robust to
change to the run directory and execute ``build-namelist`` there. That
way if there's a change to the files that are produced, your script
doesn't break due to the files not all getting copied to the run
directory.

Next we set the ``CSMDATA`` environment variable to point to the root
directory of the tree containing the input data files. Note that this
is a required input for ``build-namelist`` (this information may
alternatively be provided using the ``-csmdata`` argument). If not
provided then ``build-namelist`` will fail with an informative
message. The information is required because many of the namelist
variables have values that are absolute filepaths. These filepaths are
resolved by ``build-namelist`` by prepending the ``CSMDATA`` root to
the relative filepaths that are stored in the default values database.

The ``build-namelist`` commandline contains the ``-config`` argument
which is used to point to the cache file which was produced in the
build directory. It also contains the ``-test`` argument, explained
further below.  
::

   % cd /work/user/cam_test
   % setenv CSMDATA /fs/cgd/csm/inputdata
   % $camcfg/build-namelist -test -config /work/user/cam_test/bld/config_cache.xml
   Writing CICE namelist to ./ice_in 
   Writing RTM namelist to ./rof_in 
   Writing DOCN namelist to ./docn_ocn_in 
   Writing DOCN stream file to ./docn.stream.txt 
   Writing CLM namelist to ./lnd_in 
   Writing driver namelist to ./drv_in 
   CAM writing dry deposition namelist to drv_flds_in 
   Writing ocean component namelist to ./docn_in 
   CAM writing namelist to atm_in 
   Checking whether input datasets exist locally...
   OK -- found depvel_file = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart/dvel/depvel_monthly.nc
   OK -- found tracer_cnst_filelist = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/oxid/oxid_1.9x2.5_L26_clim_list.c090805.txt
   OK -- found tracer_cnst_datapath = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/oxid
   OK -- found depvel_lnd_file = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart/dvel/regrid_vegetation.nc
   OK -- found xs_long_file = /fs/cgd/csm/inputdata/atm/waccm/phot/temp_prs_GT200nm_jpl06_c080930.nc
   OK -- found rsf_file = /fs/cgd/csm/inputdata/atm/waccm/phot/RSF_GT200nm_v3.0_c080416.nc
   OK -- found clim_soilw_file = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart/dvel/clim_soilw.nc
   OK -- found exo_coldens_file = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart/phot/exo_coldens.nc
   OK -- found tracer_cnst_file = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/oxid/oxid_1.9x2.5_L26_1850-2005_c091123.nc
   OK -- found season_wes_file = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart/dvel/season_wes.nc
   OK -- found solar_data_file = /fs/cgd/csm/inputdata/atm/cam/solar/solar_ave_sc19-sc23.c090810.nc
   OK -- found soil_erod = /fs/cgd/csm/inputdata/atm/cam/dst/dst_10x15_c090203.nc
   OK -- found bndtvs = /fs/cgd/csm/inputdata/atm/cam/sst/sst_HadOIBl_bc_10x15_clim_c050526.nc
   OK -- found focndomain = /fs/cgd/csm/inputdata/atm/cam/ocnfrac/domain.camocn.10x15_USGS_070807.nc
   OK -- found tropopause_climo_file = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart/ub/clim_p_trop.nc
   OK -- found fpftcon = /fs/cgd/csm/inputdata/lnd/clm2/pftdata/pft-physiology.c110425.nc
   OK -- found fsnowaging = /fs/cgd/csm/inputdata/lnd/clm2/snicardata/snicar_drdt_bst_fit_60_c070416.nc
   OK -- found fatmlndfrc = /fs/cgd/csm/inputdata/share/domains/domain.lnd.fv10x15_USGS.110713.nc
   OK -- found fsnowoptics = /fs/cgd/csm/inputdata/lnd/clm2/snicardata/snicar_optics_5bnd_c090915.nc
   OK -- found fsurdat = /fs/cgd/csm/inputdata/lnd/clm2/surfdata/surfdata_10x15_simyr2000_c090928.nc
   OK -- found prescribed_ozone_datapath = /fs/cgd/csm/inputdata/atm/cam/ozone
   OK -- found prescribed_ozone_file = /fs/cgd/csm/inputdata/atm/cam/ozone/ozone_1.9x2.5_L26_2000clim_c091112.nc
   OK -- found liqopticsfile = /fs/cgd/csm/inputdata/atm/cam/physprops/F_nwvl200_mu20_lam50_res64_t298_c080428.nc
   OK -- found iceopticsfile = /fs/cgd/csm/inputdata/atm/cam/physprops/iceoptics_c080917.nc
   OK -- found water_refindex_file = /fs/cgd/csm/inputdata/atm/cam/physprops/water_refindex_rrtmg_c080910.nc
   OK -- found ncdata = /fs/cgd/csm/inputdata/atm/cam/inic/fv/cami_0000-01-01_10x15_L30_c081013.nc
   OK -- found bnd_topo = /fs/cgd/csm/inputdata/atm/cam/topo/USGS-gtopo30_10x15_remap_c050520.nc
   OK -- found ext_frc_specifier for SO2 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so2_elev_2000_c090726.nc
   OK -- found ext_frc_specifier for bc_a1 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_bc_elev_2000_c090726.nc
   OK -- found ext_frc_specifier for num_a1 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_num_a1_elev_2000_c090726.nc
   OK -- found ext_frc_specifier for num_a2 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_num_a2_elev_2000_c090726.nc
   OK -- found ext_frc_specifier for pom_a1 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_oc_elev_2000_c090726.nc
   OK -- found ext_frc_specifier for so4_a1 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so4_a1_elev_2000_c090726.nc
   OK -- found ext_frc_specifier for so4_a2 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so4_a2_elev_2000_c090726.nc
   OK -- found srf_emis_specifier for DMS = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/aerocom_mam3_dms_surf_2000_c090129.nc
   OK -- found srf_emis_specifier for SO2 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so2_surf_2000_c090726.nc
   OK -- found srf_emis_specifier for SOAG = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_soag_1.5_surf_2000_c100217.nc
   OK -- found srf_emis_specifier for bc_a1 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_bc_surf_2000_c090726.nc
   OK -- found srf_emis_specifier for num_a1 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_num_a1_surf_2000_c090726.nc
   OK -- found srf_emis_specifier for num_a2 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_num_a2_surf_2000_c090726.nc
   OK -- found srf_emis_specifier for pom_a1 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_oc_surf_2000_c090726.nc
   OK -- found srf_emis_specifier for so4_a1 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so4_a1_surf_2000_c090726.nc
   OK -- found srf_emis_specifier for so4_a2 = /fs/cgd/csm/inputdata/atm/cam/chem/trop_mozart_aero/emis/ar5_mam3_so4_a2_surf_2000_c090726.nc
   OK -- found mode_defs for so4_a1 = /fs/cgd/csm/inputdata/atm/cam/physprops/sulfate_rrtmg_c080918.nc
   OK -- found mode_defs for pom_a1 = /fs/cgd/csm/inputdata/atm/cam/physprops/ocpho_rrtmg_c101112.nc
   OK -- found mode_defs for soa_a1 = /fs/cgd/csm/inputdata/atm/cam/physprops/ocphi_rrtmg_c100508.nc
   OK -- found mode_defs for bc_a1 = /fs/cgd/csm/inputdata/atm/cam/physprops/bcpho_rrtmg_c100508.nc
   OK -- found mode_defs for dst_a1 = /fs/cgd/csm/inputdata/atm/cam/physprops/dust4_rrtmg_c090521.nc
   OK -- found mode_defs for ncl_a1 = /fs/cgd/csm/inputdata/atm/cam/physprops/ssam_rrtmg_c100508.nc
   OK -- found mode_defs for so4_a2 = /fs/cgd/csm/inputdata/atm/cam/physprops/sulfate_rrtmg_c080918.nc
   OK -- found mode_defs for soa_a2 = /fs/cgd/csm/inputdata/atm/cam/physprops/ocphi_rrtmg_c100508.nc
   OK -- found mode_defs for ncl_a2 = /fs/cgd/csm/inputdata/atm/cam/physprops/ssam_rrtmg_c100508.nc
   OK -- found mode_defs for dst_a3 = /fs/cgd/csm/inputdata/atm/cam/physprops/dust4_rrtmg_c090521.nc
   OK -- found mode_defs for ncl_a3 = /fs/cgd/csm/inputdata/atm/cam/physprops/ssam_rrtmg_c100508.nc
   OK -- found mode_defs for so4_a3 = /fs/cgd/csm/inputdata/atm/cam/physprops/sulfate_rrtmg_c080918.nc
   OK -- found rad_climate for mam3_mode1 = /fs/cgd/csm/inputdata/atm/cam/physprops/mam3_mode1_rrtmg_c110318.nc
   OK -- found rad_climate for mam3_mode2 = /fs/cgd/csm/inputdata/atm/cam/physprops/mam3_mode2_rrtmg_c110318.nc
   OK -- found rad_climate for mam3_mode3 = /fs/cgd/csm/inputdata/atm/cam/physprops/mam3_mode3_rrtmg_c110318.nc

The first nine lines of output from ``build-namelist`` inform the user
about the files that have been created. There are namelist files for
the ice component (``ice_in``), the river runoff component
(``rof_in``), the land component (``lnd_in``), the data ocean
component (``docn_in``, ``docn_ocn_in``), the atmosphere component
(``atm_in``), the driver (``drv_in``), and a file that is read by both
the atmosphere and land components (``drv_flds_in``). There is also a
"stream file" (``docn.stream.txt``) which is read by the data ocean
component. Note that these filenames are hardcoded in the components
and cannot be changed without source code modifications.

The next section of output is the result of using the ``-test``
argument to ``build-namelist``. As with ``configure`` we recommend
using this argument whenever a model configuration is being run for
the first time. It checks that each of the files that are present in
the generated namelists can be found in the input data tree whose root
is given by the ``CSMDATA`` environment variable. If a file is not
found then the user will need to take steps to make that file
accessible to the executing model before a successful run will be
possible. The following is a list of possible actions:

- Acquire the missing file. If this is a default file supplied by the
  CESM project then you will be able to download the file from the
  project's svn data repository (see `Section 2.1.7, “Acquiring Input Datasets”
  <CAM-2.1-Sample-Interactive-Session#217-acquiring-input-datasets>`_).
- If you have write permissions in the directory under ``$CSMDATA``
  then add the missing file to the appropriate location there.  If you
  don't have write permissions under ``$CSMDATA`` then put the file in
  a place where you can (for example, your run directory) and rerun
  ``build-namelist`` with an explicit setting for the file using your
  specific filepath.

===============================================================================
Example: Use build-namelist to specify a dataset in a non-default location.
===============================================================================

Suppose that the ``-test`` option informed you that the ncdata file
cami_0000-01-01_10x15_L30_c081013.nc was not found. You acquire the
file from the data repository, but don't have permissions to write in
the ``$CSMDATA`` tree. So you put the file in your run directory and
issue a ``build-namelist`` command that looks like this:
::

   % $camcfg/build-namelist -config /work/user/cam_test/bld/config_cache.xml \
   -namelist "&atm ncdata='/work/user/cam_test/cami_0000-01-01_10x15_L30_c081013.nc' /"
   
Now the namelist in ``atm_in`` will contain an initial file (specified by namelist variable ``ncdata``) which will be found by the executing CAM model.
   
-------------------------------
Acquiring Input Datasets
-------------------------------

If you are doing a standard production run that is supported in the
CESM scripts, then using those scripts will automatically invoke a
utility to acquire needed input datasets. The information in this
section is to aid developers using CAM standalone scripts.

The input datasets required to run CAM are available from a Subversion
repository located here:
`https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/
<https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/>`_. The user
name and password for the input data repository will be the same as
for the code repository (which are provided to users when they
register to acquire access to the CESM source code repository).

====================================
Acquire missing dataset
====================================

If you have a list of files that you need to acquire before running
CAM, then you can either just issue commands interactively, or if your
list is rather long then you may want to put the commands into a shell
script. For example, suppose after running ``build-namelist`` with the
``-test`` option you find that you need to acquire the file
*/fs/cgd/csm/inputdata/atm/cam/inic/fv/cami_0000-01-01_10x15_L26_c030918.nc*. And
let's assume that */fs/cgd/csm/inputdata/* is the root directory of
the inputdata tree, and that you have permissions to write there. If
the subdirectory *atm/cam/inic/fv/* doesn't already exist, then create
it. Finally, issue the following commands at an interactive C shell
prompt:
::

   % set svnrepo='https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata'
   % cd /fs/cgd/csm/inputdata/atm/cam/inic/fv
   % svn export $svnrepo/atm/cam/inic/fv/cami_0000-01-01_10x15_L26_c030918.nc
   Error validating server certificate for 'https://svn-ccsm-inputdata.cgd.ucar.edu:443':
   - The certificate is not issued by a trusted authority. Use the
   fingerprint to validate the certificate manually!
   - The certificate hostname does not match.
   - The certificate has expired.
     Certificate information:
    - Hostname: localhost.localdomain
    - Valid: from Feb 20 23:32:25 2008 GMT until Feb 19 23:32:25 2009 GMT
    - Issuer: SomeOrganizationalUnit, SomeOrganization, SomeCity, SomeState, --
    - Fingerprint: 86:01:bb:a4:4a:e8:4d:8b:e1:f1:01:dc:60:b9:96:22:67:a4:49:ff
     (R)eject, accept (t)emporarily or accept (p)ermanently? p
      A    cami_0000-01-01_10x15_L26_c030918.nc
      Export complete.

The messages about validating the server certificate will only occur for the first file that you export if you answer "p" to the question as in the example above.

------------------
Running CAM
------------------

Once the namelist files have successfully been produced, and the
necessary input datasets are available, the model is ready to
run. Usually CAM will be run with SPMD parallelization enabled, and
this requires setting up MPI resources and possibly dealing with batch
queues. These issues will be addressed briefly in `Section 2.2,
“Sample Run Scripts” <CAM-2.2-Sample-Run-Scripts>`_. But for a simple
test in serial mode executed from an interactive shell, we only need
to issue the following command:
::

   % /work/user/cam_test/bld/cam >&! cam.log

The commandline above redirects STDOUT and STDERR to the file
``cam.log``. The CAM logfile contains a substantial amount of
information from all components that can be used to verify that the
model is running as expected. Things like namelist variable settings,
input datasets used, and output datasets created are all echoed to the
log file. This is the first place to look for problems when a model
run is unsuccessful. It is also very useful to include relevant
information from the logfile when submitting bug reports.
