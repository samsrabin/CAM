***************
Appendices
***************

======================
The configure utility
======================

.. _ug63-arguments-to-configure:

----------------------------------------------
Arguments to configure
----------------------------------------------

All configuration options can be specified using command line arguments to
CAM's ``configure`` script (a Perl script).  Options not specified on the
command line will be set to default values which are either hard-coded, or
come from the definition file
``components/cam/bld/config_files/definition.xml``.  Those that depend on
the values of other options are set by logic contained in ``configure``.

The user is able to pass arguments to CAM's configure by issuing an
``xlmchange`` command for **CAM_CONFIG_OPTS**.  It is important to use the
``--append`` option if a compset's settings are to be maintained.

The options may all be specified with either one or two leading dashes,
e.g., ``-help`` or ``--help``.  A consequence of allowing long names with
single leading dashes is that the few options that can be expressed as
single letter switches may **not** be bundled, e.g., ``-h -s -v`` may NOT
be expressed as ``-hsv``.

User supplied values are denoted in angle brackets "<>".  Any value that contains
white-space must be quoted.  For options that can be set from small set of
legal values, those values are given as a vertical bar separated list.

The arguments to ``configure`` are:
::

     -[no]age_of_air_trcs
                        Switch on [off] age of air tracers. Default: on for waccm_phys, otherwise off.

     -analytic_ic       Enables the (namelist controlled) dycore testing infrastructure.

     -aquaplanet        Switch on aqua-planet mode.

     -build_chem_proc   Switch forces the build of the chemistry preprocessor (primarily for testing).

     -cache <file>      Name of output cache file which contains all configuration parameters
                        set by configure script.
                        Default: config_cache.xml

     -cachedir <file>   Name of directory where output cache file is written.
                        Default: current working directory

     -camiop            Configure CAM to generate an IOP file that can be used to drive SCAM.
                        This switch only works with the Eulerian dycore.

     -carma <name>      Build CAM with specified CARMA microphysics model
                        [ none (disabled) | bc_strat (Stratospheric Black Carbon) |
                          cirrus (Cirrus Clouds) | cirrus_dust (Cirrus Clouds with dust) |
                          dust (Dust) | meteor_impact (Meteor Impact) | meteor_smoke (Meteor Smoke) |
                          mixed_sulfate (Meteor Smoke and Sulfate) | pmc (Polar Mesospheric Clouds) |
                          pmc_sulfate (PMC and Sulfate) | sea_salt (Sea Salt) |
                          sulfate (Sulfate Aerosols) | tholin (early earth haze) |
                          test_detrain (Detrainment) | test_growth (Particle Growth) |
                          test_passive (Passive Dust) | test_radiative (Radiatively Active Dust) |
                          test_swelling (Sea Salt) | test_tracers (Asian Monsoon) |
                          test_tracers2 (Guam)].
                        Default: none.

     -chem <name>       Build CAM with specified prognostic chemistry package
                        [ trop_mam3 | trop_mam4 | trop_mam7 | trop_mozart | trop_strat_mam4_vbs | 
                          trop_bam | trop_ghg | waccm_ma | waccm_mad_mam4 | waccm_ma_mam4 | 
                          waccm_ma_sulfur | waccm_sc | waccm_sc_mam4 | waccm_tsmlt |
                          waccm_tsmlt_mam4 | waccm_tsmlt_sulfur | super_fast_llnl |
                          super_fast_llnl_mam3 | terminator | none ].
                        Default: trop_mam4 for cam6, trop_mam3 for cam5,
                                 otherwise none.

     -[no]clubb_sgs     Switch on [off] CLUBB_SGS.  Default: on for cam6, otherwise off.

     -clubb_opts <list> Comma separated list of CLUBB options to turn on.
                        [clubb_do_adv (Advect CLUBB moments)]

     -co2_cycle         Switch to turn on the carbon cycle code (adds 4 advected constituents)

     -cosp              Enable the COSP simulator.

     -dyn <name>        Dynamical core option.
                        [eul (Eulerian) | fv (Finite Volume)].

     -edit_chem_mech    Invokes CAMCHEM_EDITOR to allow the user to edit the chemistry mechanism file.

     -help [or -h]      Print usage to STDOUT.

     -hgrid <name>      Specify horizontal grid. For spectral grids use nlatxnlon where
                        nlat and nlon are the number of latitude and longitude grid
                        points respectively in the global Gaussian grid (e.g., T42 is
                        specified 64x128). For FV grids use dlatxdlon where dlat and
                        dlon are the grid cell size in degrees for latitude and longitude
                        respectively (e.g., 1.9x2.5).

     -ionosphere        Ionophere module used in WACCMX [ none | wxi | wxie ].
                        Default: none

     -macrophys <name>  Override the default macrophysics set by the physics package
                        [rk | park | clubb_sgs | spcam_sam1mom | spcam_m2005]
                        Defaults:
                        clubb_sgs if cam6
                        park if cam6 and noclubb_sgs, or cam5
                        rk if cam3 or cam4

     -max_n_rad_cnst <n> Maximum number of constituents that are either radiatively
                        active, or in any single diagnostic list for the radiation.
                        Default: 30

     -microphys <name>  Override the microphysics set by the physics package
                        [mg1 | mg2 | rk | spcam_m2005 | spcam_sam1mom].
                        Defaults:
                        mg2 if cam6
                        mg1 if cam5
                        rk if cam3 or cam4

     -nadv <n>          Override the total number of advected species set by the
                        physics and chemistry packages.

     -nadv_tt <n>       Set number of advected test tracers.
                        Default: 0

     -nlev <n>          Override the number of levels set by the physics or chemistry package.
                        Default:
                          32 if cam6
                          30 if cam5, simple physics, or spcam_m2005
                          26 if cam3, cam4, or spcam_sam1mom
                          66 if waccm and cam4
                          70 if waccm and cam5 or cam6
                          81 if waccmx
                         126 if waccmx and ionosphere is wxie

     -offline_drv <name> Specify offline unit driver.
                         [rad (PORT)]

     -offline_dyn       Enable offline driver for FV dycore.

     -ocn <name>        Allows build system to inform CAM which ocean component is being used.
                        This information is stored in the cache file and used by build-namelist
                        for selecting the default values of some tuning parameters.
                        [docn | som | socn | aquaplanet | pop].

     -pbl <name>        Override the PBL scheme set by the physics package.
                        [clubb_sys | uw | hb | spcam_sam1mom | spcam_m2005].
                        Default PBL schemes:
                          clubb_sgs if cam6
                          uw if cam5
                          hb if cam3 or cam4
                          spacm_m2005 if the physics package is spcam_m2005
                          spacm_sam1mom if the physics package is spcam_sam1mom

     -pcols <n>         Maximum number of columns in a chunk.
                        Default: 16, or if SCAM mode then 1.

     -pergro            Switch enables building CAM for perturbation growth tests.
                        Only valid with cam3 or cam4 physics.

     -phys <name>       Physics option.
                        [cam3 | cam4 | cam5 | cam6 | held_suarez | adiabatic | kessler | 
                         spcam_sam1mom | spcam_m2005].
                        Default: cam6, or if waccmx then cam4.

     -prog_species <list>Comma-separate list of prognostic mozart species packages.
                        Currently available: DST,SSLT,SO4,GHG,OC,BC,CARBON16

     -psubcols <n>      Maximum number of sub-columns in a grid column.
                        Default: 1

     -rad <name>        Override the radiation scheme set by the physics package.
                        [rrtmg | camrt].
                        Default radiation scheme:
                          rrtmg if cam5, cam6, or spcam_m2005
                          camrt if cam3, cam4, or spcam_sam1mom

     -scam              Compiles model in single column (SCAM) mode.
                        Only works with Eulerian dycore.

     -silent [or -s]    Turns on silent mode - only fatal messages issued.

     -[no]smp           Switch on [off] SMP parallelism (OpenMP)

     -spcam_clubb_sgs   Turn on the SPCAM version of CLUBB

     -spcam_nx <n>      SPCAM x-grid.  (note the CRM requires spcam_nx to be greater
                        than or equal to 4)
                        Default: 4 

     -spcam_ny <n>      SPCAM y-grid.
                        Default: 1

     -spcam_dx <n>      SPCAM horizontal grid spacing.

     -spcam_dt <n>      SPCAM timestep in seconds.

     -[no]spmd          Switch on [off] SPMD parallelism (MPI).

     -unicon            Switch to turn on the UNICON scheme.

     -usr_mech_infile   Absolute pathname of the user supplied chemistry mechanism file.

     -usr_src <dir1>[,<dir2>[,<dir3>[...]]]
                        Directories containing user source code.  Note that these
                        directories will also be searched for modified versions of the
                        files needed by the build-namelist script, e.g., the
                        namelist definition, defaults, and use case files.

     -verbose [or -v]   Turn on verbose echoing of settings made by configure.

     -version           Echo the tag name of the CAM component.

     -waccm_phys        Switch enables the use of WACCM physics in any chemistry configuration.
                        Default: off unless one of the waccm chemistry options is chosen.

     -waccmx            Build CAM/WACCM with WACCM upper Thermosphere/Ionosphere extended package.

     -zmconv_org        Enable sub-grid scale convective organization for the ZM deep
                        convective scheme based on Mapes and Neale (2011)
   

===========================
The build-namelist utility
===========================

The ``build-namelist`` utility produces namelists for the CAM
component (in the file ``atm_in``), and namelists for the control of dry
deposition which is shared by CAM and CLM (in the file ``drv_flds_in``).

The task of constructing a correct namelist is extremely complex
due to the large number of configurations supported by CAM. Editing
namelists by hand is a fragile process due to the number of variables that
need to be set, and to the many interdependencies among them. **We strongly
discourage editing namelists by hand.** All customizations of the CAM
namelist are possible by making use of the ``build-namelist`` command line
options.  The most common way to do this is by adding customized variables
to the ``user_nl_cam`` file which is then processed by ``build-namelist``
via the ``-infile`` option.

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
  are present in the local filesystem. This list can then be used to
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

The methods for setting the values of namelist variables, listed from
highest to lowest precedence, are:

1. using the ``-namelist`` option,
2. setting values in a file specified by ``-infile``,
3. specifying a ``-use_case`` option,
4. setting values in the namelist defaults file.

* The first three of these methods for specifying namelist variables
  are the ones available to the user without requiring code
  modification. Any namelist variable recognized by CAM can be
  modified using method 1 or 2. The final two methods represent
  defaults that are hard coded as part of the code base.


----------------------------------------------
Arguments to build namelist
----------------------------------------------

The options may all be specified with either one or two leading dashes,
e.g., ``-help`` or ``--help``.  A consequence of allowing long names with
single leading dashes is that the few options that can be expressed as
single letter switches may **not** be bundled, e.g., ``-h -s -v`` may NOT
be expressed as ``-hsv``.

User supplied values are denoted in angle brackets "<>".  Any value that contains
white-space must be quoted.  For options that can be set from small set of
legal values, those values are given as a vertical bar separated list.
::

     -config <filepath>    Read the given configuration cache file to determine the configuration
                           of the CAM executable.
                           Default: "config_cache.xml".

     -csmdata <dir>        Root directory of CESM input data.
                           Can also be set by using the CSMDATA environment variable.

     -dir <directory>      Directory where output namelist files will be written,
                           i.e., atm_in, and drv_flds_in.
                           Default: current working directory.

     -help [or -h]         Print usage to STDOUT.

     -ignore_ic_date       Ignore the date of the initial condition files
                           when determining the default.

     -ignore_ic_year       Ignore just the year part of the date of the initial condition files
                           when determining the default.

     -infile <filepath>    Specify a file containing namelists to read values from.

     -inputdata <filepath> Writes out a list containing pathnames for required input datasets to
                           the specified filepath.

     -namelist <namelist>  Specify namelist settings directly on the commandline by supplying
                           a string containing FORTRAN namelist syntax, e.g.,
                              -namelist "&camexp state_debug_checks=.true. /"

     -ntasks <n>           Specify the number of MPI tasks being used by the run.  This is used
                           to set a default decomposition for the FV dycore only (npr_yz).

     -silent [-s]          Turns on silent mode - only fatal messages issued.

     -test                 Enable checking that input datasets exist on local filesystem.

     -use_case             Specify a use case.

     -verbose [or -v]      Turn on verbose echoing of informational messages.

     -version              Echo the tag name of the CAM component.

   
----------------------------------------------
CAM Namelist variables
----------------------------------------------

Follow link for a searchable (or browsable) page containing all 
`CAM namelist variables
<http://www.cesm.ucar.edu/models/cesm2/settings/2.2.0/cam_nml.html>`_

