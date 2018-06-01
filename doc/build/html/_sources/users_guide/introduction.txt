.. _introduction:

 -**Need to verify what are active and data components in the text below and replace/remove the ?????**

**************************
Introduction 
**************************

The Community Atmosphere Model version CAM6 is released as the atmosphere component of the Community Earth System Model version CESM-2.0. 
It is the latest in a series of global atmosphere models whose development is guided by the `Atmosphere Model Working Group (AMWG) <http://www.cesm.ucar.edu/working_groups/Atmosphere/>`_ of the `Community Earth System Model (CESM) <http://www.cesm.ucar.edu//>`_ project. 
CAM can be run in a "standalone" configuration within CESM, by which we mean that the atmosphere is coupled to an active land model (CLM), a thermodynamic only sea ice model (a special configuration of CICE), and a data ocean model (DOCN) + ??????????????????????????. 
When one speaks of "doing CAM simulations" the implication is that it's a standalone configuration that is being used. 
When CAM is coupled to CESM active ocean and sea ice models + ?????????????????? then we refer to it as a "fully coupled CESM simulation".

Since the CAM standalone model is just a special configuration of CESM it can be run using the CESM scripts. 
This is done by using one of the "F" compsets and details on using the scripts can be found in the :ref:`Building and Running CAM within CESM <building-and-running-cam>` section of this User's Guide or the `CESM2 Quick Start Guide <http://escomp.github.io/cesm/release-cesm2>`_. 
The main advantage of running CAM via the CESM scripts is to leverage the high level of support that those scripts provide for doing production runs of predefined experiments on supported platforms. 
The CESM scripts do things like: setting up reasonable runtime environments; automatically retrieving required input datasets from an SVN server; and archiving output files. 
The ability to customize a CAM build or runtime configuration depends on being able to use the utilities described in this document. 
Any build configuration can be set up via appropriate commandline arguments to CAM's ``configure`` utility, and any runtime configuration can be set up with appropriate arguments to CAM's ``build-namelist`` utility. 

CAM provides the basic atmospheric physics for several other models included in this release:

 - CAM-chem: Community Atmosphere Model with Chemistry
 - WACCM: Whole Atmosphere Community Climate Model
 - WACCM-X: Whole Atmosphere Community Climate Model with thermosphere and ionosphere extension

Throughout this document, we will use the name CAM in a generic sense and directions provided will be useful for CAM-chem, WACCM and WACCM-X also.

It should be noted that in CAM6, we are unable to support reproducibility of CAM4 and CAM5 numerical results with what a user would get running those configuration in CESM1.2 or prior. This is due to many factors including code changes and namelist settings.  While a user is still able to set the "-phys" namelist setting to either cam4 or cam5, the results will differ with what a user would get using those settings in CESM1.2. Due to these changes, a number of compsets specific to CAM4 or CAM5 have been removed.  We recommend that if a user wants a pure CAM4 or CAM5 run, that they use CESM1.2 for those runs.  WACCM-X which utilizes CAM4 does not have this issue and it should be run using the CESM2 release of CAM.
