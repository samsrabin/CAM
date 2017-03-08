.. _input-datasets:

***************************
Input Datasets
***************************

The minimal CAM configuration requires an initial conditions dataset. But most configurations require in addition to initial conditions a variety of boundary condition files. This chapter will provide an overview of CAM's dataset requirements and some information on the provenance of the default datasets.

=========================================
SST and Sea Ice Boundary Files
=========================================

The standard CAM standalone configuration (An F compset when using CESM scripts) uses prescribed sea surface temperatures (SST) and sea ice fractions from datasets containing either climatological or time series data. The source of this data for CAM's default datasets is `Hurrell et al. [2008]. <http://www.cesm.ucar.edu/models/cesm1.2/cam/docs/ug5_3/bi01.html#hurrell2008>`_

The default CAM datasets have been preconditioned to comply with the AMIP II requirement as described in `Taylor et al. [2000] <http://www.cesm.ucar.edu/models/cesm1.2/cam/docs/ug5_3/bi01.html#taylor2000>`_. The requirement is that the SST and sea-ice concentration boundary conditions should be specified such that the monthly means computed from model output precisely agree with the monthly means in the input dataset.

The original Hurrell datasets are on a 1 degree grid. The AMIP II versions of these dataset are available as 1 degree datasets and have also been spatially interpolated to several spectral and finite volume grid resolutions. The currently available datasets are:

--------------------------------------------------
Pre-industrial climatology (1870 - 1890):
--------------------------------------------------

::

   atm/cam/sst/sst_HadOIBl_bc_1x1_clim_pi_c101029.nc
   atm/cam/sst/sst_HadOIBl_bc_0.23x0.31_clim_pi_c091020.nc
   atm/cam/sst/sst_HadOIBl_bc_0.47x0.63_clim_pi_c100128.nc
   atm/cam/sst/sst_HadOIBl_bc_0.9x1.25_clim_pi_c100127.nc
   atm/cam/sst/sst_HadOIBl_bc_1.9x2.5_clim_pi_c100127.nc
   atm/cam/sst/sst_HadOIBl_bc_4x5_clim_pi_c100127.nc
   atm/cam/sst/sst_HadOIBl_bc_10x15_clim_pi_c100127.nc
   atm/cam/sst/sst_HadOIBl_bc_128x256_clim_pi_c100128.nc
   atm/cam/sst/sst_HadOIBl_bc_64x128_clim_pi_c100128.nc
   atm/cam/sst/sst_HadOIBl_bc_48x96_clim_pi_c100128.nc
   atm/cam/sst/sst_HadOIBl_bc_32x64_clim_pi_c100128.nc
   atm/cam/sst/sst_HadOIBl_bc_8x16_clim_pi_c100128.nc


--------------------------------------------------
Historical Time Series
--------------------------------------------------
::

   atm/cam/sst/sst_HadOIBl_bc_1x1_1850_2012_c130411.nc
   atm/cam/sst/sst_HadOIBl_bc_0.23x0.31_1850_2010_c110526.nc
   atm/cam/sst/sst_HadOIBl_bc_0.47x0.63_1850_2012_c130411.nc
   atm/cam/sst/sst_HadOIBl_bc_0.9x1.25_1850_2012_c130411.nc
   atm/cam/sst/sst_HadOIBl_bc_1.9x2.5_1850_2012_c130411.nc
   atm/cam/sst/sst_HadOIBl_bc_4x5_1850_2012_c130411.nc
   atm/cam/sst/sst_HadOIBl_bc_10x15_1850_2012_c130411.nc
   atm/cam/sst/sst_HadOIBl_bc_128x256_1850_2012_c130411.nc
   atm/cam/sst/sst_HadOIBl_bc_64x128_1850_2012_c130411.nc
   atm/cam/sst/sst_HadOIBl_bc_48x96_1850_2008_c100128.nc
   atm/cam/sst/sst_HadOIBl_bc_32x64_1850_2012_c130411.nc
   atm/cam/sst/sst_HadOIBl_bc_8x16_1850_2012_c130411.nc

--------------------------------------------------
Present day climatology (1982 - 2001):
--------------------------------------------------
::

   atm/cam/sst/sst_HadOIBl_bc_1x1_clim_c101029.nc
   atm/cam/sst/sst_HadOIBl_bc_0.23x0.31_clim_c061106.nc
   atm/cam/sst/sst_HadOIBl_bc_0.47x0.63_clim_c061106.nc
   atm/cam/sst/sst_HadOIBl_bc_0.9x1.25_clim_c040926a.nc
   atm/cam/sst/sst_HadOIBl_bc_1.9x2.5_clim_c061031.nc
   atm/cam/sst/sst_HadOIBl_bc_4x5_clim_c061031.nc
   atm/cam/sst/sst_HadOIBl_bc_10x15_clim_c050526.nc
   atm/cam/sst/sst_HadOIBl_bc_256x512_clim_c031031.nc
   atm/cam/sst/sst_HadOIBl_bc_128x256_clim_c050526.nc
   atm/cam/sst/sst_HadOIBl_bc_64x128_clim_c050526.nc
   atm/cam/sst/sst_HadOIBl_bc_48x96_clim_c050526.nc
   atm/cam/sst/sst_HadOIBl_bc_32x64_clim_c050526.nc
   atm/cam/sst/sst_HadOIBl_bc_8x16_clim_c050526.nc
