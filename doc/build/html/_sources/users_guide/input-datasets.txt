.. _input-datasets:

***************************
Input Datasets
***************************

Input datasets are required to run the model and differ depending on the configuration used. Here we described data sets that are required for some or all of the CESM2 configurations.

All atmospheric configuration require to include emissions, lower boundary condition dataset, soil erodibility files for dust emissions, topography files, and solar input files.  In addition, meteorological data are required to run the model in specified dynamics mode. Furthermore, CAM and WACCM SC (specified chemistry), and simulations with prescribed stratospheric aerosols require prescribed input dataset that are derived from full chemistry simulations. 
Additional dataset include sea-surface temperatures, and prescribed land data.

------------------------------
Emissions
------------------------------

All CAM, CAM-chem and WACCM configurations require surface emissions and / or external forcings (vertically distributed emissions), in all of these we place all biomass burning emissions at the surface, as well as anthropogenic emissions, besides sulfate. Aircraft and volcanic emissions are distributed with altitude. Different emission sectors are separted in these categories: anthropogenic (anthro), biomass burning (bb), biogenic (bg), volcanic source and others (soil, ocean etc.). 

================================================
List of available emissions datasets
================================================

CESM2.0 default emissions are based on the CMIP6 inventories for anthropogenic and biomass burning emissions, provided by the Community Emissions Data System (CEDS, http://www.globalchange.umd.edu/ceds/ceds-cmip6-data/), original files are available at: https://esgf-node.llnl.gov/search/input4mips/.  Additional emissions (soil, ocean) are from the POET inventory (http://eccad.aeris-data.fr/).

================================================
List of species with emissions (CAM)
================================================

Surface (anthro, bb): bc_a4 , pom_a4 , num_a4 (for bc_a4 and pom_a4), SO2 

Surface (anthro, bb, biogenic): SOAG 

Vertical (extfrc): SO2 (aircraft, contvolcano), so4_a1 (anthro-ene, contvolcano), so4_a2 (contvolcano), bc_a4 (aircraft), num_a1, num_a2, num_a4

=================================================
List of species with dry and wet deposition (CAM) 
=================================================

Dry and wet deposition:

Aerosols: bc_a1, bc_a4, dst_a1, dst_a2, dst_a3, ncl_a1, ncl_a2, ncl_a3, 
num_a1, num_a2, num_a3, num_a4, pom_a1, pom_a4, so4_a1, so4_a2, so4_a3, 
soa_a1, soa_a2

Gas-phase: H2O2, H2SO4, SO2

================================================
List of species with emissions (CAMchem/WACCM)
================================================

Surface (anthro, bb, other): NO, NH3, CO, C2H4, C2H6, C3H6, C3H8

Surface (anthro, bb): bc_a4, pom_a4, num_a4, SO2, C2H2, BIGALK, BIGENE, BENZENE, TOLUENE, XYLENES, CH3OH, C2H5OH, CH2O, CH3CHO, CH3COCH3, MEK, HCOOH, CH3COOH, HCN, CH3CN, IVOC, SVOC, 

Vertical: NO2 (aircraft), SO2 (aircraft, contvolcano, eruptingVolcanoes), so4_a1 (anthro-ene, contvolcano), so4_a2 (contvolcano), bc_a4 (aircraft),  num_a1, num_a2, num_a4


============================================================
List of species with dry and wet deposition (CAMChem/WACCM) 
============================================================

Species with dry deposition:

Aerosols: bc_a1, bc_a4, dst_a1, dst_a2, dst_a3, ncl_a1, ncl_a2, ncl_a3, 
num_a1, num_a2, num_a3, num_a4, pom_a1, pom_a4, so4_a1, so4_a2, so4_a3, 
soa1_a1, soa1_a2, soa2_a1, soa2_a2, soa3_a1, soa3_a2, soa4_a1, soa4_a2, soa5_a1, soa5_a2

Gas-phase: ALKNIT, ALKOOH, BENZOOH, BZOOH, C2H5OH, C2H5OOH,
C3H7OOH, C6H5OOH, CH2O, CH3CHO, CH3CN, CH3COCH3, CH3COCHO,
CH3COOH, CH3COOOH, CH3OH, CH3OOH, CO, EOOH, GLYALD, H2O2,
H2SO4, HCN, HCOOH, HNO3, HO2NO2, HONITR, HPALD, HYAC,
HYDRALD, IEPOX, ISOPNITA, ISOPNITB, ISOPNO3, ISOPNOOH,
ISOPOOH, IVOC, MACROOH, MEKOOH, MPAN, NC4CH2OH, NC4CHO,
NH3, NH4, NO, NO2, NOA, NTERPOOH, O3, ONITR, PAN,
PHENOOH, POOH, ROOH, SO2, SOAG0, SOAG1, SOAG2, SOAG3,
SOAG4, SVOC, TERP2OOH, TERPNIT, TERPOOH, TERPROD1, TERPROD2,
TOLOOH, XOOH, XYLENOOH, XYLOLOOH

Species with wet deposition:
Aerosols:  bc_a1, bc_a4, dst_a1, dst_a2, dst_a3, ncl_a1, ncl_a2, ncl_a3, 
 num_a1, num_a2, num_a3, num_a4, pom_a1, pom_a4, so4_a1, so4_a2, so4_a3, 
 soa1_a1, soa1_a2, soa2_a1, soa2_a2, soa3_a1, soa3_a2, soa4_a1, soa4_a2, soa5_a1, soa5_a2

Gas-phase: ALKNIT, ALKOOH, BENZOOH, BRONO2, BZOOH, C2H5OH, C2H5OOH, C3H7OOH, C6H5OOH, CH2O, CH3CHO, CH3CN, CH3COCH3, CH3COCHO, CH3COOH, CH3COOOH, CH3OH, CH3OOH, CLONO2, COF2, COFCL, EOOH, GLYALD, H2O2, H2SO4, HBR, HCL, HCN, HCOOH, HF, HNO3, HO2NO2, HOBR, HOCL, HONITR, HPALD, HYAC, HYDRALD, IEPOX, ISOPNITA, ISOPNITB, ISOPNO3, ISOPNOOH, ISOPOOH, IVOC, MACR, MACROOH, MEKOOH, MVK, NC4CH2OH, NC4CHO, NDEP, NH3, NH4, NHDEP, NOA, NTERPOOH, ONITR, PHENOOH, POOH, ROOH, SO2, SOAG0, SOAG1, SOAG2, SOAG3, SOAG4, SVOC, TERP2OOH, TERPNIT, TERPOOH, TERPROD1, TERPROD2, TOLOOH, XOOH, XYLENOOH, XYLOLOOH

============================================================
List of species with biogenic emissions (CAMChem/WACCM) 
============================================================

Species with MEGAN emissions (CAM-chem (TS1) and WACCM (TSMLT)) are listed in drv_flds_in, and can be modified in user_nl_cam.
Note, modifications may be required for other mechanisms)::

  megan_specifier = 'ISOP = isoprene',
      'MTERP = pinene_a + carene_3 + thujene_a + 2met_styrene + cymene_p + cymene_o + terpinolene + bornene + fenchene_a +
 ocimene_al + pinene_b + sabinene + camphene + limonene + phellandrene_a + terpinene_g + terpinene_a + phellandrene_b + 
 myrcene + ocimene_t_b + ocimene_c_b',
      'BCARY = caryophyllene_b + bergamotene_a + bisabolene_b + farnescene_b + humulene_a',
      'CH3OH = methanol', 
      'C2H5OH = ethanol', 
      'CH2O = formaldehyde',
      'CH3CHO = acetaldehyde', 
      'CH3COOH = acetic_acid', 
      'CH3COCH3 = acetone',
      'HCOOH = formic_acid', 
      'HCN = hydrogen_cyanide', 
      'CO = carbon_monoxide',
      'C2H6 = ethane', 
      'C2H4 = ethene', 
      'C3H8 = propane', 
      'C3H6 = propene',
      'BIGALK = pentane + hexane + heptane + tricyclene', 
      'BIGENE = butene',
      'TOLUENE = toluene'

================================================
WACCM-X
================================================
WACCM-X uses emissions relevant to middle atmosphere (MA) chemistry, consistent with those 
provided for the REF-C1 experiment of the `IGAC/SPARC Chemistry-Climate Model Initiative 
(CCMI) <http://www.sparc-climate.org/fileadmin/customer/6_Publications/Newsletter_PDF/40_SPARCnewsletter_Jan2013_web.pdf>`_ 
Community Simulations.

WACCM-X uses emissions relevant to middle atmosphere (MA) chemistry, consistent with those
provided for the REF-C1 experiment of the `IGAC/SPARC Chemistry-Climate Model Initiative
(CCMI) <http://www.sparc-climate.org/fileadmin/customer/6_Publications/Newsletter_PDF/40_SPARCnewsletter_Jan2013_web.pdf>`_
Community Simulations.

------------------------------
Lower boundary data sets
------------------------------

For CESM2.0 we provide one lower boundary data set from 1750 to the end of 2015, that can be used for different horizontal resolutions. 
This data file includes of different long-lived greenhouse and other gases that are prescribed as concentrations at the surface. This file works for all CESM2 atmospheric configurations.

flbc_file = ‘/glade/p/cesmdata/cseg/inputdata/atm/waccm/lb/LBC_17500116-20150116_CMIP6_0p5degLat_c180227.nc’

Additional lower boundary condition files for future CMIP6 pathways will be provided in CESM2.1

------------------------------
Soil erodibility files
------------------------------

Soil erodibility maps provide a proxy for the relative ability of the soils in different regions to generate dust.  The maps are input as a netcdf file, with no time dependence, and are a unitles factor for each grid box, and are interpolated to the resolution of the model within the model.  They are input in the CAM, although the rest of the dust generation itself is included in CLMl.  The idea of the soil erodibility map comes from Ginoux et al., 2001, and the specific maps used is the geomorphic map from Zender et al., 2003a and are used in combination with the Dust Entrainment and Deposition scheme from Zender et la., 2003b, as described in Mahowald et al., 2006.  The regional distribution of these values are tuned to generate a good distribution as described in Albani et al., 2014.  

The file used:
soil_erod_file         = '/glade/p/cesmdata/cseg/inputdata/atm/cam/dst/dst_source2x2tunedcam6-2x2-04062017.nc’


------------------------------
Topography files
------------------------------

------------------------------
Meteorological data sets
------------------------------

For specified dynamics model simulation, meteorolocial analysis from the  Goddard Earth Observing System Model, Version 5 (GEOS5) and the Modern-Era Retrospective analysis for Research and Applications, Version 2 (MERRA2) data have been prepared to run CESM and WRF simulations and are available in 3 resulution, and are availbe on the Research Data Archive: 


GEOS5 2005-present (currently only 1.9x2.5 degree horizontal resolution): https://rda.ucar.edu/datasets/ds313.0/
 
and 

MERRA2 1980-close to present (1.9x2.5, 0.9x1.25, and 0.5x0.63 degrees horizontal resolution): https://rda.ucar.edu/datasets/ds313.3/

These datasets and additional resolutions for GEOS5 and MERRA can be found on the NCAR hsi, and on local disk.

------------------------------
Solar input files
------------------------------
CESM2 uses `CMIP6 solar input files <http://solarisheppa.geomar.de/cmip6>`_:

**solar_irrad_data_file**: provides spectral solar irradiance (SSI)

WACCM and WACCM-X use 2 additional solar input files for upper-atmosphere processes:

**solar_parms_data_file**: geomagnetic parameters

**epp_all_filepath**: Provides *epp_ion_rates* variable with ion pair production rate from
energetic particle precipitation, including solar protons, cosmic rays, and
medium energy electrons.

The data for all three inputs have been combined into a single file for each time period,
so that WACCM points to the same file for each.

piControl:
 solar_irrad_data_file = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6piControl_c160921.nc'
 
 solar_parms_data_file = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6piControl_c160921.nc'
 
 epp_all_filepath      = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6piControl_c160921.nc'

Historical:
 solar_irrad_data_file = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6_18491230-22991231_c171031.nc'
 
 solar_parms_data_file = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6_18491230-22991231_c171031.nc'

 epp_all_filepath      = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6_18491230-22991231_c171031.nc'


WACCM-X uses the Naval Research Laboratory (NRL) Version 1 reconstruction for solar 
irradiance (Lean, ref), rather than CMIP6. Instead of the *epp_all_filepath*, WACCM-X uses
the *epp_spe_filepath*, which provides ion pair production rates just for solar proton 
events.

Historical:
 solar_irrad_data_file = '$DIN_LOC_ROOT/atm/cam/solar/spectral_irradiance_Lean_1950-2014_daily_GOME-Mg_Leap_c150623.nc'
 
 epp_spe_filepath      = '$DIN_LOC_ROOT/atm/waccm/solar/spes_1963-2014_c150717.nc'
 
 solar_parms_data_file = '$DIN_LOC_ROOT/atm/waccm/solar/waxsolar_3hr_c170504.nc'
 
Constant year 2000:
 solar_irrad_data_file = '$DIN_LOC_ROOT/atm/cam/solar/spectral_irradiance_Lean_1950-2014_daily_GOME-Mg_Leap_c150623.nc'
 
 epp_spe_filepath      = '$DIN_LOC_ROOT/atm/waccm/solar/spes_1963-2014_c150717.nc'
 
 solar_parms_data_file = '$DIN_LOC_ROOT/atm/waccm/solar/wa_avg_c20170519.nc'
 

CESM2 uses `CMIP6 solar input files <http://solarisheppa.geomar.de/cmip6>`_:

*solar_irrad_data_file*: provides spectral solar irradiance (SSI)

WACCM and WACCM-X use 2 additional solar input files for upper-atmosphere processes:

*solar_parms_data_file*: geomagnetic parameters

*epp_all_filepath*: energetic particle precipitation, including solar proton events and
medium energy electrons

*epp_spe_filepath*: used just for solar proton events

The data for all three inputs have been combined into a single file for each time period,
so that WACCM points to the same file for each.

piControl:
 solar_irrad_data_file = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6piControl_c160921.nc'

 solar_parms_data_file = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6piControl_c160921.nc'

 epp_all_filepath      = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6piControl_c160921.nc'

Historical:
 solar_irrad_data_file = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6_18491230-22991231_c171031.nc'

 solar_parms_data_file = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6_18491230-22991231_c171031.nc'

 epp_all_filepath      = '$DIN_LOC_ROOT/atm/cam/solar/SolarForcingCMIP6_18491230-22991231_c171031.nc'


WACCM-X uses the Naval Research Laboratory (NRL) Version 1 reconstruction for solar
irradiance (Lean, ref), rather than CMIP6.

Historical:
 solar_irrad_data_file = '$DIN_LOC_ROOT/atm/cam/solar/spectral_irradiance_Lean_1950-2014_daily_GOME-Mg_Leap_c150623.nc'

 epp_spe_filepath      = '$DIN_LOC_ROOT/atm/waccm/solar/spes_1963-2014_c150717.nc'

 solar_parms_data_file = '$DIN_LOC_ROOT/atm/waccm/solar/waxsolar_3hr_c170504.nc'

Constant year 2000:
 solar_irrad_data_file = '$DIN_LOC_ROOT/atm/cam/solar/spectral_irradiance_Lean_1950-2014_daily_GOME-Mg_Leap_c150623.nc'

 epp_spe_filepath      = '$DIN_LOC_ROOT/atm/waccm/solar/spes_1963-2014_c150717.nc'

 solar_parms_data_file = '$DIN_LOC_ROOT/atm/waccm/solar/wa_avg_c20170519.nc'


------------------------------
WACCM
------------------------------

------------------------------
WACCM-X
------------------------------


