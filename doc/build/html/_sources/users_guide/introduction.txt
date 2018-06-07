.. _introduction:

**************************
Introduction 
**************************

The Community Atmosphere Model version 6 (CAM6) is released as the active atmosphere component of the Community Earth System Model version CESM-2.0. 
It is the latest in a series of global atmosphere models whose development is guided by the `Atmosphere Model Working Group (AMWG) <http://www.cesm.ucar.edu/working_groups/Atmosphere/>`_ of the `Community Earth System Model (CESM) <http://www.cesm.ucar.edu//>`_ project. 
CAM can be run in many configurations within the CESM; it is the atmosphere
component in the B, E, F, Q, and P compsets.
The term "standalone CAM" is often used to refer to a compset which does
not include prognostic ocean and sea ice models.
When one speaks of "doing CAM simulations" the implication is that it's a standalone configuration that is being used. 
When CAM is coupled to prognostic land, ocean, and sea ice models then we refer
to it as a "fully coupled CESM simulation" which are implemented in the B compsets.

To get started running CAM refer to the `CESM2 Quick Start Guide
<http://escomp.github.io/cesm/release-cesm2>`_ and the 
:ref:`Building and Running CAM within CESM <building-and-running-cam>` section of this User's Guide.
Running CAM using the CESM scripts provides a high level of support for doing production runs of predefined experiments on supported platforms. This is the place to start for most users.

CAM provides the basic atmospheric physics for several other models included in this release:

 - CAM-chem: Community Atmosphere Model with Chemistry
 - WACCM: Whole Atmosphere Community Climate Model
 - WACCM-X: Whole Atmosphere Community Climate Model with thermosphere and ionosphere extension

Throughout this document, we will use the name CAM in a generic sense and directions provided will be useful for CAM-chem, WACCM and WACCM-X also.

It should be noted that in CAM6, we are unable to support reproducibility of CAM4 and CAM5 numerical results with what a user would get running those configurations in CESM1.2 or prior.
This is due to many factors including code changes and namelist settings.  While a user is still able to set the "-phys" namelist setting to either cam4 or cam5, the results will differ with what a user would get using those settings in CESM1.2. Due to these changes, a number of compsets specific to CAM4 or CAM5 have been removed.  We recommend that if a user wants a pure CAM4 or CAM5 run, that they use CESM1.2 for those runs.  WACCM-X which utilizes CAM4 does not have this issue and it should be run using the CESM2 release of CAM.
