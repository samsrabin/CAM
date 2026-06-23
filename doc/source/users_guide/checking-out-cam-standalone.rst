***********************************
 Downloading CAM standalone
***********************************

-------------------------------------
Downloading the CAM standalone code 
-------------------------------------

It is important to note that if a user downloads a CAM standalone tag, they
will not be able to run a fully coupled model.  Checking out CAM standalone
should only be done by users to run E, F, Q, or P compsets.  If you wish to use other compsets you will need to download the entire CESM model.  Please use the directions for `downloading CESM <http://escomp.github.io/CESM/versions/cesm2.2/html/downloading_cesm.html>`_ and you should ignore the rest of this chapter.  

Also for scientific studies, it
is much better to use a released version of CESM and not do a CAM standalone checkout.  These
directions are provided for users who are collaborating on CAM development.

CAM development tags are available through `CAM's github
repository <https://github.com/ESCOMP/CAM>`_.


To download a standalone CAM

::

     % git clone https://github.com/ESCOMP/CAM
     % cd CAM

At this point you will see you have two files: README.md and CODE_OF_CONDUCT.md

The README.md file lists the current branches that the CAM repository contains along with some basic information.  

The following example shows how to checkout CAM standalone tag cam6_3_000:

::

    % git checkout cam6_3_000

If a user wishes to get the most recent CAM development code, they can checkout the head of the cam_development branch.  Please note that this code is the most recently committed code and while basic testing has occurred, its use for scientific studies is not recommended.

--------------------------------
Checkout out the externals          
--------------------------------

Once the CAM code has been checked out, but before it can be used, the external libraries that CAM uses must be checked out. 

To get the externals, users need to cd to the main CAM directory and run:

::

     % manage_externals/checkout_externals

This will create and populate all of the external directories.

Note -- You will get an error message if you try to cd into manage_externals and run checkout_externals from that directory.


--------------------------------
Useful git commands
--------------------------------

For a listing of files that have changed since checkout...

::

    % git status 

For a description of the changes made to the working copy...

::

    % git diff  -- or -- git difftool


------------------------------------------------------------
Useful documentation about CAM development and git resources
------------------------------------------------------------

The `wiki page for CAM development <http://github.com/ESCOMP/CAM/wiki>`_ contains more detailed information. 


