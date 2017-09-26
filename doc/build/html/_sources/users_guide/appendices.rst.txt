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

The CESM scripts access CAM's ``configure`` via the script
``$CAM_ROOT/models/atm/cam/bld/cam.buildnml.csh``. The
``cam.buildnml.csh`` script acts as the interface between the CESM
scripts and CAM's ``configure`` and ``build-namelist`` utilities.


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
the files
``$CAM_ROOT/models/atm/cam/bld/config_files/defaults_*.xml``. A few
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
  Switch on [off] SMP parallelism (OpenMP). This option can be used when building a model that doesn't contain CICE. It allows building an executable whose thread count can be set at run time.

``-[no]spmd``
  Switch on [off] SPMD parallelism (MPI). This option can be used when building a model that doesn't contain CICE. It allows building an executable whose task count can be set at run time.

######################################################
CAM parallelization when running standalone with CICE
######################################################

``-ntasks <n>``
  This option must be used to specify SPMD parallelism when the CICE component is present. ``<n>`` is the number of MPI tasks. Setting ntasks > 0 implies ``-spmd``. Use ``-nospmd`` to turn off linking with an MPI library. To configure for pure MPI specify ``"-ntasks N -nosmp". ntasks`` is used by CICE to determine default grid decompositions which must be specified at build time.

``-nthreads <n>``
  This option must be used to specify SMP parallelism when the CICE component is present. ``<n>`` is the number of OpenMP threads per process. Setting nthreads > 0 implies ``-smp``. Use ``-nosmp`` to turn off compilation of OMP directives. For pure OpenMP set ``"-nthreads N -nospmd". nthreads`` is used by CICE to determine default grid decomposition which must be specified at build time.

**NOTE:**  When CAM is running standalone with CICE the default CICE decomposition is determined from the values of the ``-ntasks`` and ``-nthreads`` arguments. The user also has the ability to explicitly set the CICE decomposition using the following four arguments. If any of these arguments is set then *ALL FOUR* must be set.

``-cice_bsizex <n>``
  CICE block size in longitude dimension. This size must evenly divide the number of longitude points in the global grid.

``-cice_bsizey <n>``
  CICE block size in latitude dimension. This size must evenly divide the number of latitude points in the global grid.

``-cice_maxblocks <n>``
  Maximum number of CICE blocks per process.

``-cice_decomptype <name>``
  CICE decomposition type ``[ cartesian | spacecurve | roundrobin ]``.

############################
General options to configure
############################

``-cache <name>``
  Name of output cache file. Default: ``config_cache.xml``.

``-cachedir <dir>``
  Name of directory where output cache file is written. Default: CAM build directory.

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

``-ocn`` [ ``docn`` | ``dom`` | ``som`` | ``socn`` | ``aquaplanet`` ]``
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
  Directory where CAM will be built. This is where configure will write the output files it generates (Makefile, Filepath, etc...). Default: ./

``-cam_exe <name>``
  Name of the CAM executable. Default: ``cam``.

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
  User specified Fortran compiler. Default: Depends on the OS and whether MPI is enabled.

``-fc_type [pgi | lahey | intel | pathscale | gnu | xlf]``
  Type of the Fortran compiler. This argument is used in conjunction with the ``-fc`` argument when the name of the fortran compiler refers to a wrapper script (e.g., ``mpif90`` or ``ftn``). In this case the user needs to specify the type of Fortran compiler that is being invoked by the wrapper script. Default: Depends on the name of the Fortran compiler.

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
  User specified linker. Default: use the Fortran compiler.

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
  Override the OS setting for cross platform compilation from the following list ``[aix|irix|linux| bgl|bgp ]``. Default: OS on which configure is executed as defined by the Perl $OSNAME variable.

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
  ``$CAM_ROOT/models/atm/cam/bld/namelist_files/namelist_defaults_cam.xml``,
  and in the use case files located in the directory
  ``$CAM_ROOT/models/atm/cam/bld/namelist_files/use_cases/``.

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

-cice_nl <namelist>
  Specify namelist settings for CICE directly on the commandline by supplying a string containing FORTRAN namelist syntax, e.g., ``-cice_nl` "&ice histfreq=1 /"``. This namelist will be passed to the invocation of the CICE build-namelist via its -``namelist`` argument.

``-config <filepath>``
  Read the specified configuration cache file to determine the configuration of the CAM executable. Default: ``config_cache.xml``.

``-config_cice <filepath>``
  Filepath of the CICE config_cache file. This filepath is passed to the invocation of the CICE ``build-namelist``. Only specify this to override the default filepath which was set when the CICE ``configure`` was invoked by the CAM ``configure``.

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
is `here <http://www.cesm.ucar.edu/models/cesm2.0/namelists/cam_nml.html>`_.
