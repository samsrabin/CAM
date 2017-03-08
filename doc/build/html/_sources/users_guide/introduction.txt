.. _introduction:

**************************
Introduction 
**************************

The Community Atmosphere Model version CAM-5.3 is released as the atmosphere component of the Community Earth System Model version CESM-1.2. 
It is the latest in a series of global atmosphere models whose development is guided by the `Atmosphere Model Working Group (AMWG) <http://www.cesm.ucar.edu/working_groups/Atmosphere/>`_ of the `Community Earth System Model (CESM) <http://www.cesm.ucar.edu//>`_ project. 
CAM is the atmospheric component of the CESM. 
CAM is has a "standalone" configuration in CESM, by we mean that the atmosphere is coupled to an active land model (CLM), a thermodynamic only sea ice model (a special configuration of CICE), and a data ocean model (DOCN). 
When one speaks of "doing CAM simulations" the implication is that it's a standalone configuration that is being used. 
When CAM is coupled to CESM active ocean and sea ice models then we refer to it as a "fully coupled CESM simulation".

CAM provides a framework for running the "Whole Atmosphere" configurations; WACCM, and WACCM-X. 
To run CAM in a WACCM or WACCM-X configuration the user is referred to the `CESM-1.2 User's Guide <http://www.cesm.ucar.edu/models/cesm2.0/>`_.

In versions of CAM before 4.0 the driver for the standalone configuration was completely separate code from what was used to couple the components of the CCSM. 
One of the most significant software changes in CAM-4.0 was a refactoring of how the land, ocean, and sea ice components are called which enabled the use of the CCSM coupler to act as the CAM standalone driver (this also depended on the complete rewritting of the CCSM coupler to support sequential execution of the components). 
Hence, for the CESM1 model, just as for CCSM4 before it, it is accurate to say that a CAM standalone configuration is nothing more than a special configuration of CESM in which the active ocean and sea ice components are replaced by data ocean and thermodynamic sea ice components.

Since the CAM standalone model is just a special configuration of CESM it can be run using the CESM scripts. 
This is done by using one of the "F" compsets and is described in the `CESM-1.2 User's Guide <http://www.cesm.ucar.edu/models/cesm2.0/>`_. 
The main advantage of running CAM via the CESM scripts is to leverage the high level of support that those scripts provide for doing production runs of predefined experiments on supported platforms. 
The CESM scripts do things like: setting up reasonable runtime environments; automatically retrieving required input datasets from an SVN server; and archiving output files. 
But CAM is used in a lot of environments where the complexity of production ready scripts is not necessary. 
In these instances the flexibility and simplicity of being able to completely describe a run using a short shell script is a valuable option. 
In either case though, the ability to customize a CAM build or runtime configuration depends on being able to use the utilities described in this document. 
Any build configuration can be set up via appropriate commandline arguments to CAM's ``configure`` utility, and any runtime configuration can be set up with appropriate arguments to CAM's ``build-namelist`` utility. 
Issues that are specific to running CAM from the CESM scripts will not be discussed in this guide. 
Rather we focus on issues that are independent of which scripts are used to run CAM, although there is some attention given in this guide to the construction of simple scripts designed for running CAM in its standalone mode.
