.. _checking-out-cam-standalone:

***********************************
 Downloading CAM standalone
***********************************

-------------------------------------
Downloading the CAM standalone code 
-------------------------------------

It is important to note that if a user downloads a CAM standalone tag, they
will not be able to run a fully coupled model.  Checking out CAM standalone
should only be done by users to run E, F, Q, or P compsets.

CAM development tags are available through a Subversion
repository to **users who have developer access**.  Access to the development code requires Subversion client software
in place that is compatible with our Subversion server software, such
as a recent version of the command line client, svn. Currently, our
server software is at version 1.8.17. We recommend using a client at
version 1.8 or later, though older versions may suffice. For more information or to
download open source tools, visit `Subversion <http://subversion.apache.org/>`_.

If you do not have developer access, please use the directions for `downloading CESM <http://escomp.github.io/cesm/release-cesm2/downloading_cesm.html>`_ and you should ignore the rest of this chapter.  

With a valid svn client installed on the machine where CAM will be
built and run, the user may download the latest version of the development 
code. First view the available versions with the
following command:

::

    > %svn list https://svn-ccsm-models.cgd.ucar.edu/cam1/trunk_tags

Note that when you are contacting the Subversion server for the first time, you may need to accept an authentication certification.


Be aware that the request is set to the current machine login id and you
must enter the CESM registered name given to you when you requested developer access.

You may be prompted several times for the username and password when
checking out the code for the first time from this new Subversion path.
This is because the code is distributed across a number of different
Subversion repositories and each repository requires authentication.

Once correctly entered, the username and password will be cached in a
protected subdirectory of the user's home directory so that repeated
entry of this information will not be required for a given machine.

The following example shows how to checkout CAM standalone tag cam6_0_002:

::

    > %svn co https://svn-ccsm-models.cgd.ucar.edu/cam1/trunk_tags/cam6_0_002

If a problem was encountered during checkout, which may happen with an older version of the client software, it may appear to have downloaded successfully, but in fact only a partial checkout has occurred. To ensure a successful download, make sure the last line of svn output has the following statement:

::

    > Checked out revision XXXXX.

This will create a directory called ``cam6_0_002`` that can be used to
modify, build, and run the model.

--------------------------------
Checkout out the externals          
--------------------------------

Once the CAM code has been checked out, but before it can be used, the external libraries that CAM uses must be checked out. 

To get the externals, users need to cd to the main CAM directory and run:

::

     > %manage_externals/checkout_externals

This will create and populate all of the external directories.

Note -- You will get an error message if you try to cd into manage_externals and run checkout_externals from that directory.


--------------------------------
Useful svn commands
--------------------------------

For various information regarding the version checked out...

::

    > svn info       

For a listing of files that have changed since checkout...

::

    > svn status 

For a description of the changes made to the working copy...

::

    > svn diff 

