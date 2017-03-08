.. _sample-interactive-session:

****************************
Sample Interactive Session
****************************

The following sections present an interactive C shell session to build
and run a default version of CAM. Most often these steps will be
encapsulated in shell scripts. An important advantage of using a
script is that it acts to document the run you've done. Knowing the
source code tree, and the ``configure`` and ``build-namelist``
commands provides all the information needed to replicate a run.

For the interactive session the shell variable ``camcfg`` is set to
the directory in the source tree that contains the CAM ``configure``
and ``build-namelist`` utilities (``$CAM_ROOT/models/atm/cam/bld``).
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
to the CAM configuration directory (``$CAM_ROOT/models/atm/cam/bld``).

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
