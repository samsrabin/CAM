.. _building-and-running-cam:

**************************
Building and Running CAM
**************************

The following describes how to build and run CAM in its standalone configuration. 
We do not provide scripts that are setup to work out of the box on a particular set of platforms. 
If you would like this level of support then consider running CAM from the CESM scripts (see `CESM-1.2 User's Guide <http://www.cesm.ucar.edu/models/cesm2.0/...>`_). We do however provide some examples of simple run scripts which should provide a useful starting point for writing your own scripts (see `Section 2.2, “Sample Run Scripts” <CAM-2.2-Sample-Run-Scripts>`_).

In order to build and run CAM the following are required:

- The source tree. CAM-5.3 is distributed with CESM-1.2. To obtain the source code go to the section "Acquiring the Code" on the `CESM Home Page <http://www.cesm.ucar.edu/>`_. When we refer to the root of the CAM source tree, this is the same directory as the root of the CESM source tree. This directory is referred to throughout this document as ``$CAM_ROOT``.
- Perl (version 5.4 or later).
- A GNU version of the ``make`` utility.
- Fortran and C compilers. The Fortran compiler needs to support at least the Fortran95 standard.
- A NetCDF library (version 4.1.3 or later) that has the Fortran APIs built using the same Fortran compiler that is used to build the rest of the CAM code. This library is used extensively by CAM both to read input datasets and to write the output datasets. The NetCDF source code is available `here <http://www.unidata.ucar.edu/downloads/netcdf/>`_. We have updated the required NetCDF library version from 3.6 to 4.1.3 due to a recently discovered bug which affects all previous versions of the NetCDF library. The bug only occurs in special circumstances that are not that easy to replicate, however the result is that corrupt files are silently created. A more complete description of the bug is here.

Input datasets. 
The required datasets depend on the CAM configuration. Determining which datasets are required for any configuration is discussed in `Section 2.1.6, “Building the Namelist” <CAM-2.1-Sample-Interactive-Session#216-building-the-namelist>`_. Acquiring those datasets is discussed in `Section 2.1.7, “Acquiring Input Datasets” <CAM-2.1-Sample-Interactive-Session#217-acquiring-input-datasets>`_.

To build CAM for SPMD execution it will also be necessary to have an MPI library (version 1 or later). As with the NetCDF library, the Fortran API should be build using the same Fortran compiler that is used to build the rest of CAM. Otherwise linking to the library may encounter difficulties, usually due to inconsistencies in Fortran name mangling.

Building and running CAM takes place in the following steps:

1. Configure model
2. Build model
3. Build namelist
4. Execute model

**Configure model.**  This step is accomplished by running the ``configure`` utility to set the compile-time parameters such as the dynamical core (Eulerian Spectral, Semi-Lagrangian Spectral, Finite Volume, or Spectral Element), horizontal grid resolution, and the type of parallelism to employ (shared-memory and/or distributed memory). 
The ``configure`` utility is discussed in `Appendix A, The configure utility <CAM-6.1-The-configure-utility>`_.

**Build model.**  This step includes compiling and linking the executable using the GNU make command (``gmake``). 
``configure`` creates a ``Makefile`` in the directory where the build is to take place. The user then need only change to this directory and execute the ``gmake`` command.

**Build namelist.**  This step is accomplished by running the ``build-namelist`` utility, which supports a variety of options to control the run-time behavior of the model. 
Any namelist variable recognized by CAM can be changed by the user via the ``build-namelist`` interface. There is also a high level "use case" functionality which makes it easy for the user to specify a consistent set of namelist variable settings for running particular types of experiments. The ``build-namelist`` utility is discussed in `Appendix B, The build-namelist utility <CAM-6.2-The-build-namelist-utility>`_.

**Execute model.**  This step includes the actual invocation of the executable. 
When running using distributed memory parallelism this step requires knowledge of how your machine invokes (or "launches") MPI executables. When running with shared-memory parallelism (using OpenMP) you may also set the number of OpenMP threads. On most HPC platforms access to the compute resource is through a batch queue system. The sample run scripts discussed in `Section 2.2, “Sample Run Scripts” <CAM-2.2-Sample-Run-Scripts>`_ show how to set the batch queue resources on several HPC platforms.
