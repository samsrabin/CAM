.. _getting-help:

**************************
Getting Help
**************************

This chapter describes several ways in which a user may obtain help when using CAM.

-----------------------
The CAM Web Page
-----------------------

The central source for information on CAM is the `CAM web page <http://www.cesm.ucar.edu/models/cesm2.0/atmosphere>`_.
This webpage is a veritable goldmine of information about CAM.

------------------------------
The CESM Bulletin Board
------------------------------

The CESM Bulletin Board is a moderated forum for rapid exchange of information, ideas, and topics of interest relating to all components of the CESM. 
This includes sharing software tools, datasets, programming tips and examples, as well as discussions of questions, problems and workarounds. 
The primary motivation for the establishment of this forum is to facilitate and encourage communication between the users of the CESM around the world. This bulletin board will also be used to distribute announcements related to CESM.

The CESM Bulletin Board is here: `http://bb.cgd.ucar.edu/ <http://bb.cgd.ucar.edu/>`_.

You will find specific sections about CAM, WACCM and CAM-chem.

---------------------
Reporting bugs
---------------------

If a user should encounter bugs in the code (i.e., it doesn't behave in a way in which the documentation says it should), the problem should be reported electronically to the `CESM Bulletin Board <http://bb.cgd.ucar.edu/>`_. 
When writing a bug report the guiding principle should be to provide enough information so that the bug can be reproduced. 
The following list suggests the minimal information that should be contained in the report:

1. The version number of the CESM release that CAM is part of (or the CAM tag if it was a standalone checkout).
2. The architecture on which the code was built. Include relevant information such as the Fortran compiler, MPI library, etc.
3. The ``create_newcase`` command-line. If it is this command that is failing, then report the output from this command. 
4. Any  ``xmlchange`` commands.
5. Model printout. Ideally this would contain a stack trace. But it should at least contain any error messages printed to the output log.

Please note that CAM is a research tool, and not all features contained in the code base are supported.
