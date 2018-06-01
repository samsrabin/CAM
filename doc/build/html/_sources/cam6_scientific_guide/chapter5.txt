.. |cam| replace:: CAM6.0

.. |waccm| replace:: WACCM4.0

.. |lowres| replace:: :math:`4 \times 5 ^{\circ}`

.. |medres| replace:: :math:`1.9 \times 2.5 ^{\circ}`

.. |higres| replace:: :math:`0.9 \times 2.5 ^{\circ}`

.. _extensions-to-cam:

Extensions to CAM
=================

Introduction
------------

This section contains a description of the neutral constituent chemical
options available CAM and |waccm|, including different chemical schemes,
emissions, boundary conditions, lightning, dry depositions and wet
removal; 2) the photolysis approach; 3) numerical algorithms used to
solve the corresponding set of ordinary differential equations.; 4)
additions to superfast chemistry.

Chemistry
---------

Chemistry Schemes
~~~~~~~~~~~~~~~~~

For CAM-Chem, an extensive tropospheric chemistry option is available
(trop mozart), as well as an extensive tropospheric and stratospheric
chemistry (trop-strat mozart) as discussed in detail in (:cite:`lamarque:12`),
including a list of all species and reactions. Furthermore, a superfast
chemistry option is available for CAM, as discussed in
Section :ref:`sec-chem_superfast`. For each chemical scheme,
CAM-chem uses the same chemical preprocessor as MOZART-4. This
preprocessor generates Fortran code for each specific chemical
mechanism, allowing for an easy update and modification of existing
chemical mechanisms. In particular, the generated code provides two
chemical solvers, one explicit and one semi-implicit, which the user
specifies based on the chemical lifetime of each species. For all
supported compsets, this generated code is available in a sub-directory
of ``atm/src/chemistry``.

The Bulk Aerosol Model
^^^^^^^^^^^^^^^^^^^^^^

CAM4-chem uses the bulk aerosol model discussed in :cite:`lamarque:05`
and :cite:`emmons:10`. This model has a representation of aerosols
based on the work by :cite:`{tie:02` and :cite:`tie:05`, i.e. sulfate
aerosol is formed by the oxidation of SO\ :math:`_{2}` in the gas
phase (by reaction with the hydroxyl radical) and in the aqueous phase
(by reaction with ozone and hydrogen peroxide).  Furthermore, the
model includes a representation of ammonium nitrate that is dependent
on the amount of sulfate present in the air mass following the
parameterization of gas/aerosol partitioning by
:cite:`metzger:01`. Because only the bulk mass is calculated, a
lognormal distribution is assumed for all aerosols using different
mean radius and geometric standard deviation :cite:`liao:03`.  The
conversion of carbonaceous aerosols (organic and black) from
hydrophobic to hydrophilic is assumed to occur within a fixed 1.6 days
:cite:`tie:05`. Natural aerosols (desert dust and sea salt) are
implemented following :cite:`mahowald:06a` and :cite:`mahowald:06b`
and the sources of these aerosols are derived based on the model
calculated wind speed and surface conditions.  In addition,
secondary-organic aerosols (SOA) are linked to the gas-phase chemistry
through the oxidation of atmospheric non-methane hydrocarbons (NMHCs),
as in :cite:`lack:04`.


CAM-Chem using the Modal Aerosol Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CAM-Chem has the ability to run with two modal aerosols models, the MAM3
and MAM7 (:cite:`liu:12`). The Modal Aerosols Model, is described in Section
4.8.2. In CAM5-Chem, the gase-phase chemistry is coupled to Modal
Aerosol Model in chemical species O\ :math:`_{3}`, OH, HO\ :math:`_{2}`
and NO\ :math:`_{3}`, as derived from the chemical mechanism and not
from a climatoloty. The tropospheric gas-phase and heterogeneous
reactions as discribed in Section 4.8.2. are added to the standard MAM
chemical mechanism.

Trop MOZART Chemistry
^^^^^^^^^^^^^^^^^^^^^

The extensive tropospheric chemistry scheme represents a minor update to
the MOZART-4 mechanism, fully described in (:cite:`emmons:10`). In particular, we
have included C\ :math:`_{2}`\ H\ :math:`_{2}`, HCOOH, HCN and
CH\ :math:`_{3}`\ CN. Reaction rates have been updated to JPL-2006
(:cite:`sander_etal:06`). A minor update has been made to the isoprene oxidation
scheme, including an increase in the production of glyoxal. This
mechanism is mainly of relevance in the troposphere and is intended for
simulations for which long-term trends in the stratospheric composition
are not crucial. Therefore, in this configuration, the stratospheric
distributions of long-lived species (see discussion below) are specified
from previously performed WACCM simulations (:cite:`garcia_etal:07`); see Section :ref:`sec-boundary`).

Trop-Strat MOZART Chemistry
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The extensive tropospheric and stratospheric chemistry includes the full
stratospheric chemistry from |waccm|, with an updated enforcement of the
conservation of total chlorine and total bromine under advection to
improve the performance of the model in simulating the ozone hole. In
addition, we have updated the heterogeneous chemistry module to reflect
that the model was underestimating the supercooled ternary solution
(STS) surface area density (SAD), see more detail in
Section [sec:waccm]; (**???**), Kinnison et al, 2012, (in prepareation).

SOA calculation in CAM-Chem
^^^^^^^^^^^^^^^^^^^^^^^^^^^

An SOA simulation of intermediate complexity is also available in
CAM-Chem. This is based on the 2-product model scheme of
:cite:`odum:97`, as implemented in CAM-Chem by :cite:`heald:08`. This
treats the products of VOC oxidation as semi-volatile species, which
re-partition every time step based on the temperature (enthalpy of
vaporization of 42 kJmol-1) and organic aerosol mass available for
condensation of vapours :cite:`pankow:94`.  In CAM-Chem we treat
secondary organic aerosol formation from the products of isoprene,
monoterpene and aromatic (benzene, toluene and xylene) oxidation by
OH, O\ :math:`_{3}` and NO\ :math:`_{3}`.  The yields and partitioning
coefficients are based on smog chamber studies
:cite:`griffin:99,henze:08,ng:07`.  The SOA calculation is setup to
run with biogenic emissions calucated by the MEGAN2.1 model (see Section :ref:`sec-Emissions`).

.. _sec-Emissions:

Emissions
~~~~~~~~~

Surface emissions are used in as a flux boundary condition for the
diffusion equation of all applicable tracers in the planetary
boundary-layer scheme. The surface flux files used in the released
version are discussed in (**???**) and conservatively remapped from
their original resolution (monthly data available every decade at
0.5x0.5) to (monthly data every year at 1.9x2.5). The remapping is made
offline to avoid the internal remapping, which consists of a simple
linear interpolation and therefore does not ensure exact conservation of
emissions between resolutions.

Emissions of Trace Gases
^^^^^^^^^^^^^^^^^^^^^^^^

Emissions for historic and future model simulations are based on ACCMIP
((**???**)) and different RCP scenarios, which are available for the
years 1850-2000, and 2000-2100.

Additional emissions are available for a short period covering
1992-2010, as discussed in (**???**). More specifically, for 1992-1996,
which is prior to satellite-based fire inventories, monthly mean
averages of the fire emissions for 1997-2008 from GFED2 (**???** and
updates) are used for each year. For 2009-2010, fire emissions are from
FINN (Fire INventory from NCAR) (**???**). If running with FINN fire
emissions, additional species are availabel: NO\ :math:`_{2}`, BIGALD,
CH\ :math:`_{3}`\ COCHO, CH\ :math:`_{3}`\ COOH, CRESOL, GLYALD, HYAC,
MACR, MVK. Most of the anthropogenic emissions come from the POET
(Precursors of Ozone and their Effects in the Troposphere) database for
2000 (**???**). The anthropogenic emissions (from fossil fuel and
biofuel combustion) of black and organic carbon determined for 1996 are
from (**???**). For SO\ :math:`_{2}` and NH\ :math:`_{3}`, anthropogenic
emissions are from the EDGAR-FT2000 and EDGAR-2 databases, respectively
(http://www.mnp.nl/edgar/).

For Asia, these inventories have been replaced by the Regional Emission
inventory for Asia (REAS) with the corresponding annual inventory for
each year simulated (**???**). Only the Asian emissions from REAS vary
each year, all other emissions are repeated annually for each year of
simulation. The DMS emissions are monthly means from the marine
biogeochemistry model HAMOCC5, representative of the year 2000
(**???**).

Additional emissions (volcanoes and aircraft) are included as
three-dimensional arrays, conservatively-remapped to the CAM-chem grid.
The volcanic emission are from (**???**) and the aircraft
(NO:math:`_{2}`) emissions are from (**???**). In the case of volcanic
emissions (SO:math:`_{2}` and SO\ :math:`_{2}`), an assumed 2% of the
total sulfur mass is directly released as SO\ :math:`_{2}`.
SO\ :math:`_{2}` emissions from continuously outgassing volcanoes are
from the GEIAv1 inventory (Andres and Kasgnoc, 1998). Totals for each
year and emitted species are listed in (**???**), Table 7. Aerosol
Emissions available to be used in CAM5-Chem are described above (Section
4.8.1.).

Biogenic emissions
^^^^^^^^^^^^^^^^^^

Biogenic emissions can be calculated by the Model of Emissions of Gases
and Aerosols from Nature version 2.1 (MEGAN2.1) (**???**). In this case,
MEGAN2.1 is coupled to the CESM atmosphere and land model. Biogenic
emissions of volatile organic compounds (i.e. isoprene and monoterpenes)
are calculated based upon emission factors, land cover (LAI and PFT),
and driving meteorological variables. CO\ :math:`_{2}` effect on
isoprene emission is also included (**???**). Emission factors of
different MEGAN compounds can be specified from mapped files or based on
PFTs. These are made available for atmospheric chemistry, unless the
user decides to explicitly set those emissions using pre-defined (i.e.
contained in a file) gridded values. Details of this implementation in
the CLM3 are discussed in (**???**) and (**???**): Vegetation in the CLM
model is described by 17 plant function types (PFTs, see (**???** Table
1)). Present-day land cover data such as leaf area index are consistent
with MODIS land surface data sets (**???**). Alternate land cover and
density can be either specified or interactively simulated with the
dynamic vegetation model (CLMCNDV) or the carbon nitrogen model (CLMCN)
of the CLM for any time period of interest. Additional namelist
parameters have been included to facilitate the mapping between the
emissions in MEGAN2.1 (147 species) and the chemical mechanism. Surface
emissions without biogenic emissions have to be used if the MEGAN2.1
model produces biogenic emissions to prevent double counting.

.. _sec-boundary:

Boundary conditions
~~~~~~~~~~~~~~~~~~~

Lower boundary conditions
^^^^^^^^^^^^^^^^^^^^^^^^^

For all long-lived species (methane and longer lifetimes, in addition to
hydrogen and methyl bromide) (**???** see Table 3), the surface
concentrations are specified using the historical reconstruction from
(**???**). In addition, for CO\ :math:`_{2}` and CH\ :math:`_{4}`, an
observationally-based seasonal cycle and latitudinal gradient are
imposed on the annual average values provided by (**???**). These values
are used in the model by overwriting at each time step the corresponding
model mixing ratio in the lowest model level with the time (and
latitude, if applicable) interpolated specified mixing ratio.

Specified stratospheric distributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the trop-mozart chemistry, no stratospheric chemistry is explicitly
represented in the model. Therefore, it is necessary to ensure a proper
distribution of some chemically-active stratospheric (namely
O\ :math:`_{3}`, NO, NO\ :math:`_{2}`, HNO\ :math:`_{3}`, CO,
CH\ :math:`_{4}`, N\ :math:`_{2}`\ O, and
N\ :math:`_{2}`\ O\ :math:`_{5}`) species, as is the case for MOZART-4.
This monthly-mean climatological distribution is obtained from WACCM
simulations covering 1950-2005 (**???**). Because of the vast changes
that occur over that time period, our data distribution provides files
for three separate periods: 1950-1959, 1980-1989 and 1996-2005. This
ensure that users can perform simulations with a stratospheric
climatology representative of the pre-CFC era, as well as during the
high CFC and post-Pinatubo era. Additional datasets for different RCP
runs are also available or can easily be constructed if necessary.

Upper boundary condition
^^^^^^^^^^^^^^^^^^^^^^^^

The model top at about 40km is considered a rigid lid (no flux across
that boundary) for all chemical species. For trop-mozart

Lightning
~~~~~~~~~

The emissions of NO from lightning are included as in (**???**), i.e.
using the Price parameterization ((**???**; **???**), scaled to provide
a global annual emission of 3-4 Tg(N)/year. The vertical distribution
follows (**???**) as in (**???**). In addition, the strength of
intra-cloud (IC) lightning strikes is assumed to be equal to
cloud-to-ground strikes, as recommended by (**???**).

Lightning NOx can be modifid in the namelist. For CAM5-Chem, lightning
NOx is increased by a factor of 3 to reach the same emissions of 3-4
Tg(N)/year.

.. _sec-Dry deposition:

Dry deposition
~~~~~~~~~~~~~~

Dry deposition is represented following the resistance approach
originally described in (**???**), as discussed in (**???**), this
earlier paper was subsequently updated and we have included all updates
(**???**; **???**). Following this approach, all deposited chemical
species (the specific list of deposited species is defined along with
the chemical mechanisms, see section 4) are mapped to a
weighted-combination of ozone and sulfur dioxide depositions; this
combination represents a definition of the ability of each considered
species to oxidize or to be taken up by water. In particular, the latter
is dependent on the effective Henry’s law coefficient. While this
weighting is applicable to many species, we have included specific
representations for CO/H\ :math:`_{2}` (**???**; **???**) and
peroxyacetylnitrate (PAN) (**???**). Furthermore, it is assumed that the
surface resistance for SO\ :math:`_{2}` can be neglected (**???**).
Finally, following (**???**), the deposition velocities of black and
organic carbonaceous aerosols are specified to be 0.1 cm/s over all
surfaces. Dust and sea-salt are represented following (**???**) and
(**???**).

The computation of deposition velocities in CAM-chem takes advantage of
its coupling to the Community Land Model (CLM; http://www.cesm.ucar.edu/
models/cesm1.0/ clm/index.shtml). In particular, the computation of
surface resistances in CLM leads to a representation at the level of
each plant functional type (Table 1) of the various drivers for
deposition velocities. The grid-averaged velocity is computed as the
weighted-mean over all land cover types available at each grid point.
This ensures that the impact on deposition velocities from changes in
land cover, land use or climate is taken into account. All species in
the mechanism are per default affected by dry deposition if depostion
velocities are defined in the model.

.. _sec-Wet removal:

Wet removal
~~~~~~~~~~~

Wet removal of soluble gas-phase species is the combination of two
processes: in-cloud, or nucleation scavenging (rainout), which is the
local uptake of soluble gases and aerosols by the formation of initial
cloud droplets and their conversion to precipitation, and below-cloud,
or impaction scavenging (washout), which is the collection of soluble
species from the interstitial air by falling droplets or from the liquid
phase via accretion processes (e.g. **???**).

Removal is modeled as a simple first-order loss process
X\ :math:`_{iscav}`
=X\ :math:`_{i} \cdot`\ F\ :math:`\cdot (1- exp(- \lambda ~ \Delta`\ t)).
In this formula, X\ :math:`_{iscav}` is the species mass (in kg) and
X\ :math:`_{i}` scavenged in time step :math:`\Delta`\ t , F is the
fraction of the grid box from which tracer is being removed, and
:math:`\lambda` is the loss rate. In-cloud scavenging is proportional to
the amount of condensate converted to precipitation, and the loss rate
depends on the amount of cloud water, the rate of precipitation
formation, and the rate of tracer uptake by the liquid phase.
Below-cloud scavenging is proportional to the precipitation flux in each
layer and the loss rate depends on the precipitation rate and either the
rate of tracer uptake by the liquid phase (for accretion processes), the
mass-transfer rate (for highly soluble gases and small aerosols), or the
collision rate (for larger aerosols).

In CAM-chem two separate parameterizations are available: (**???**) from
MOZART-2 and (**???**). The distinguishing features of the Neu and
Prather scheme are related to three aspects of the parameterization: 1)
the partitioning between in-cloud and below cloud scavenging, 2) the
treatment of soluble gas uptake by ice and 3) the Neu and Prather scheme
uniquely accounts for the spatial distribution of clouds in a column and
the overlap of condensate and precipitation. Given a cloud fraction and
precipitation rate in each layer, the scheme determines the fraction of
the gridbox exposed to precipitation from above and that exposed to new
precipitation formation under the assumption of maximum overlap of the
precipitating fraction. Each model level is partitioned into as many as
four sections, each with a gridbox fraction, precipitation rate, and
precipitation diameter: 1) Cloudy with precipitation falling through
from above; 2) Cloudy with no precipitation falling through from above;
3) Clear sky with precipitation falling through from above; 4) Clear sky
with no precipitation falling from above. Any new precipitation
formation is spread evenly between the cloudy fractions (1 and 2). In
region 3, we assume a constant rate of evaporation that reduces both the
precipitation area and amount so that the rain rate remains constant.
Between levels, we average the properties of the precipitation and
retain only two categories, precipitation falling into cloud and
precipitation falling into ambient air, at the top boundary of each
level. If the precipitation rate drops to zero, we assume full
evaporation and random overlap with any precipitating levels below. Our
partitioning of each level and overlap assumptions are in many ways
similar to those used for the moist physics in the ECMWF model
(**???**).

The transfer of soluble gases into liquid condensate is calculated using
Henry’s Law, assuming equilibrium between the gas and liquid phase.
Nucleation scavenging by ice, however, is treated as a burial process in
which trace gas species deposit on the surface along with water vapor
and are buried as the ice crystal grows. (**???**) have found that the
burial model successfully reproduces the molar ratio of HNO\ :math:`_{3}` to H\ :math:`_{2}`\ O on ice crystals as a function of
temperature for a large number of aircraft campaigns spanning a wide
variety of meteorological conditions. We use the empirical relationship
between the HNO\ :math:`_{3}` H\ :math:`_{2}`\ O molar ratio and
temperature given by (**???**) to determine in-cloud scavenging during
ice particle formation, which is applied to nitric acid only.
Below-cloud scavenging by ice is calculated using a rough representation
of the riming process modeled as a collision-limited first order loss
process. (**???**) provide a full description of the scavenging
algorithm.

On the other hand, the Horowitz approach uses the rain generation
diagnostics from the large-scale and convection precipitation
parameterizations in CAM; equilibrium between gas-phase and liquid phase
is then assumed based on the effective Henry’s law.

Photolytic Approach (Neutral Species)
-------------------------------------

The calculation of the photolysis coefficients is divided into two
regions: (1) 120 nm to 200 nm (33 wavelength intervals); (2) 200 nm to
750 nm (67 wavelength intervals). The total photolytic rate constant (J)
for each absorbing species is derived during model execution by
integrating the product of the wavelength dependent exo-atmospheric flux
(F:math:`_{exo}`); the atmospheric transmission function (or normalized
actinic flux) (N:math:`_A`), which is unity at the top of atmosphere in
most wavelength regions; the molecular absorption cross-section
(:math:`\sigma`); and the quantum yield (:math:`\phi`). The
exo-atmospheric flux over these wavelength intervals can be specified
from observations and varied over the 11-year solar sunspot cycle (see
section [sec:short\ :sub:`w`\ ave]).

The wavelength-dependent transmission function is derived as a function
of the model abundance of ozone and molecular oxygen. For wavelengths
greater than 200 nm a normalized flux lookup table (LUT) approach is
used, based on the 4-stream version of the Stratosphere, Troposphere,
Ultraviolet (STUV) radiative transfer model (S. Madronich, personal
communication), (**???**). The transmission function is interpolated
from the LUT as a function of altitude, column ozone, surface albedo,
and zenith angle. The temperature and pressure dependences of the
molecular cross sections and quantum yields for each photolytic process
are also represented by a LUT in this wavelength region. At wavelengths
less than 200 nm, the wavelength-dependent cross section and quantum
yields for each species are specified and the transmission function is
calculated explicitly for each wavelength interval. There are two
exceptions to this approach. In the case of J(NO) and J(O\ :math:`_2`),
detailed photolysis parameterizations are included inline. In the
Schumann-Runge Band region (SRBs), the parameterization of NO photolysis
in the :math:`\delta`-bands is based on (**???**). This parameterization
includes the effect of self-absorption and subsequent attenuation of
atmospheric transmission by the model-derived NO concentration. For
J(O\ :math:`_2`), the SRB and Lyman-alpha parameterizations are based on
(**???**) and (**???**), respectively.

While the lookup table provides explicit quantum yields and
cross-sections for a large number of photolysis rate determinations,
additional ones are available by scaling of any of the explicitly
defined rates. This process is available in the definition of the
chemical preprocessor input files (see (**???** Table 3) for a complete
list of the photolysis rates available). The impact of clouds on
photolysis rates is parameterized following (**???**). However, because
we use a lookup table approach, the impact of aerosols (tropospheric or
stratospheric) on photolysis rates cannot be represented.

As an extension of MOZART-4 and to provide the ability to seamlessly
perform tropospheric and stratospheric chemistry simulations, the
calculation of photolysis rates for wavelengths shorter than 200 nm is
included; this was shown to be important for ozone chemistry in the
tropical upper troposphere (**???**). In addition, because the standard
configuration of CAM only extends into the lower stratosphere (model top
is usually around 40 km), an additional layer of ozone and oxygen above
the model top is included to provide a very accurate representation of
photolysis rates in the upper portion of the model as compared to the
equivalent calculation using a fully-resolved stratospheric
distribution.

In addition, tropospheric photolysis rates can be computed
interactively. Users interested in using this capability have to contact
the Chemistry-CLimate Working Group Liaison as this is an unsupported
option.

Numerical Solution Approach
---------------------------

Chemical and photochemical processes are expressed by a system of
time-dependent ordinary differential equations at each point in the
spatial grid, of the following form:

.. math::
   :label: solver1

   \frac{d\vec{y}}{dt} = \vec{P}(\vec{y}, t) - \vec{L}(\vec{y}, t) \cdot \vec{y}
   

.. math:: \vec y(t) = \{y_i(t)\} \quad i = 1, 2, \ldots, N

where :math:`\vec y` is the vector of all solution variables (chemical
species), :math:`N` is the number of variables in the system, and
:math:`y_i` represents the :math:`i^{th}` variable. :math:`\vec P` and
:math:`\vec L` represent the production and loss rates, which are, in
general, non-linear functions of the :math:`y_i`. This system of
equations is solved via two algorithms: an explicit forward Euler
method:

.. math::
   :label: solver2

   y_i^{n+1} = y_i^n + \Delta t \cdot f_i(t_{n}, y^{n})
   

in the case of species with long lifetimes and weak forcing terms
(e.g., N\ :math:`_2`\ O), and a more robust implicit backward Euler
method:

.. math::
   :label: solver3

   y_i^{n+1} = y_i^n + \Delta t\cdot f_i(t_{n+1}, y^{n+1})
   

for species that comprise a\`\`stiff system" with short lifetimes and
strong forcings (e.g., OH). Here :math:`n` represents the time step
index. Each method is first order accurate in time and conservative. The
overall chemistry time step, :math:`\Delta t = t_{n+1}-t_n`, is fixed at
30 minutes. Preprocessing software requires the user to assign each
solution variable, :math:`y_i`, to one of the solution schemes. The
discrete analogue for methods :eq:`solver2`  and :eq:`solver3`  above results
in two systems of algebraic equations at each grid point. The solution
to these algebraic systems for equation :eq:`solver2`  is straightforward
(i.e., explicit). The algebraic system from the implicit method
:eq:`solver3`  is quadratically non-linear. This system can be written as:

.. math::
   :label: solver4

   \vec{G}(\vec{y}^{\,\, n+1})=\vec{y}^{\,\, n+1}-\vec{y}^{\,\, n}- \Delta t\cdot\vec{f}(t_{n+1},\vec{y}^{\,\, n+1})=0
   

Here :math:`G` is an :math:`N`-valued, non-linear vector function,
where :math:`N` equals the number of species solved via the implicit
method. The solution to equation :eq:`solver4`  is solved with a Newton-
Raphson iteration approach as shown below:

.. math::
   :label: solver5

   \vec{y}^{\,\, n+1}_{m+1} = \vec{y}^{\,\, n+1}_m - \vec{J} \cdot \vec{G}(\vec{y}^{\,\, n+1}_m); \; m=0,1,\ldots, M    

Where :math:`m` is the iteration index and has a maximum value of ten.
The elements of the Jacobian matrix :math:`\vec J` are given by:

.. math:: J_{ij}=\frac{\partial G_i}{\partial y_j}

The iteration and solution of equation :eq:`solver5`  is carried out with
a sparse matrix solution algorithm. This process is terminated when the
given solution variable changes in a relative measure by less than a
prescribed fractional amount. This relative error criterion is set on a
species by species basis, and is typically 0.001; however, for some
species (e.g., O\ :math:`_3`), where a tighter error criterion is
desired, it is set to 0.0001. If the iteration maximum is reached (for
any species) before the error criterion is met, the time step is cut in
half and the solution to equation :eq:`solver5`  is iterated again. The
time step can be reduced five times before the solution is accepted.
This approach is based on the work of :cite:`sandu_etal:96` and :cite:`sandu_etal:97`; see also
:cite:`brasseur_etal:99`.

.. _sec-chem_superfast:

Superfast Chemistry
-------------------

Chemical mechanism
~~~~~~~~~~~~~~~~~~

The super-fast mechanism was developed for long coupled
chemistry-climate simulations, and is based on an updated version of the
full non-methane hydrocarbon effects (NMHC) chemical mechanism for the
troposphere and stratosphere used in the Lawrence Livermore National
Laboratory off-line 3D global chemistry-transport model (IMPACT)
citep[]rotman:04. The super-fast mechanism includes 15 photochemically
active trace species (O:math:`_{3}`, OH, HO\ :math:`_{2}`,
H\ :math:`_{2}`\ O\ :math:`_{2}`, NO, NO\ :math:`_{2}`,
HNO\ :math:`_{3}`, CO, CH\ :math:`_{2}`\ O,
CH\ :math:`_{3}`\ O\ :math:`_{2}`, CH\ :math:`_{3}`\ OOH, DMS,
SO\ :math:`_{2}`, SO\ :math:`_{4}`, and
C\ :math:`_{5}`\ H\ :math:`_{8}`) that allow us to calculate the major
terms by which global change operates in tropospheric ozone and sulfate
photochemistry. The families selected are Ox, HOx, NOy, the
CH\ :math:`_{4}` oxidation suite plus isoprene (to capture the main NMHC
effects), and a group of sulfur species to simulate natural and
anthropogenic sources leading to sulfate aerosol.
Sulfate aerosols is handled following :cite:`tie2005`.
In this scheme, CH4 concentrations are read in from a file and uses CAM3.5 simulations :cite:`lamarque:10`.
The super-fast mechanism was validated by comparing the super-fast and full mechanisms in side-by-side simulations.

Emissions for CAM4 superfast chemistry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| \|lccc\| & Anthro. &Natural & Interactive
| CH\ :math:`_{2}`\ O & x & x &
| CO & x & x &
| DMS & & x &
| ISOP & & & x
| NO & x & &
| SO\ :math:`_{2}` & x & &

LINOZ
~~~~~

Linoz is linearized ozone chemistry for stratospheric 
modeling :cite:`mclinden:00`. It calculates the net 
production of ozone (i.e., production minus loss) as a 
function of only three independent variables: local ozone 
concentration, temperature, and overhead column ozone). A 
zonal mean climatology for these three variables as well as 
the other key chemical variables such a total odd-nitrogen 
methane abundance is developed from satellite and other in 
situ observations. A relatively complete photochemical box 
model :cite:`prather:92` is used to integrate the radicals to a 
steady state balance and then compute the net production of 
ozone. Small perturbations about the chemical climatology 
are used to calculate the coefficients of the first-order Taylor 
series expansion of the net production in terms of local 
ozone mixing ratio (f), temperature (T), and overhead 
column ozone (c).

.. math::

   \begin{aligned}
   \frac{df}{df} &=& (P - L)^o + \left.{\frac{\delta (P - L)}{\delta f}}\right|_o(f - f^o) + \left.\frac{\delta (P - L)}{\delta T}\right|_o (T - T^o)\\ \nonumber
   & & + \left.\frac{\delta (P - L)}{\delta c}\right|_o(c - c^o)  \end{aligned}

The photochemical tendency for the climatology is denoted by
:math:`(P-L)_o`, and the climatology values for the independent
variables are denoted by :math:`f_o`, :math:`c_o`, and :math:`T_o`,
respectively. Including these four climatology values and the three
partial derivatives, Linoz is defined by seven tables. Each table is
specified by 216 atmospheric profiles: 12 months by 18 latitudes
(85:math:`^o`\ S to 85\ :math:`^o`\ N). For each profile, quantities are
evaluated at every 2 km in pressure altitude from :math:`z^*` = 10 to 58
km (:math:`z^*` = 16 km log\ :math:`_10` (1000/p)). These tables
(calculated for each decade, 1850-2000 to take into account changes in
CH4 and N2O) are automatically remapped onto the CAM-chem grid with the
mean vertical properties for each CAM-chem level calculated as the
mass-weighted average of the interpolated Linoz profiles. Equation (1)
is implemented for the chemical tendency of ozone in CAM-chem.

Parameterized PSC ozone loss
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the superfast chemistry, we incorporate the PSCs parameterization
scheme of :cite:`cariolle_et_al:90` when the temperature falls below
195 K and the sun is above the horizon at stratospheric altitudes.
The O\ :math:`_3` loss scales as the squared stratospheric chlorine
loading (normalized by the 1980 level threshold). In this formulation
PSC activation invokes a rapid e-fold of O\ :math:`_3` based on a
photochemical model, but only when t he temperature stays below the
PSC threshold. The stratospheric chlorine loading (1850-2005) is input
in the model using equivalent effective stratospheric chlorine (EESC)
(:cite:`newman:07`) table based on observed mixing ratios at the
surface.

This can be used instead of the more explicit representation available
from WACCM in the strat-trop configuration.

Physical Parameterizations
---------------------------

In |waccm|, we extend the physical parameterizations used in CAM4 by adding
constituent separation velocities to the molecular (vertical) diffusion
and modifying the gravity spectrum parameterization. Both of these
parameterizations are present, but not used, in CAM4. In addition, we
replace the CAM4 parameterizations for both solar and longwave radiation
above :math:`\sim 65` km, and add neutral and ion chemistry models.

Domain and Resolution
~~~~~~~~~~~~~~~~~~~~~~

|waccm| has 66 vertical levels from the ground to :math:`5.1 \times 10^{-6}`
hPa, as in the previous WACCM versions. As in CAM4, the vertical
coordinate is purely isobaric above 100 hPa, but is terrain following
below that level. At any model grid point, the local pressure p is
determined by

.. math:: p(i,j,k) = A(k) \, p_0 + B(k) \, p_s(i,j) 
	  :label: eq:p

where :math:`A` and :math:`B` are functions of model level, :math:`k`,
only; :math:`p_0=10^3` hPa is a reference surface pressure; and
:math:`p_s` is the predicted surface pressure, which is a function of
model longitude and latitude (indexed by :math:`i` and :math:`j`). The
finite volume dynamical core uses locally material surfaces for its
internal vertical coordinate and remaps (conservatively interpolates) to
the hybrid surfaces after each time step.

Within the physical and chemical parameterizations, a local pressure
coordinate is used, as described by :eq:`eq:p` . However, in the remainder
of this note we refer to the vertical coordinate in terms of
log-pressure altitude

.. math:: Z = H \log\left(\frac{p_0}{p}\right).

The value adopted for the scale height, :math:`H=7` km, is
representative of the real atmosphere up to :math:`\sim 100` km, above
that altitude temperature increases very rapidly and the typical scale
height becomes correspondingly larger. It is important to distinguish
:math:`Z` from the *geopotential* height :math:`z`, which is obtained
from integration of the hydrostatic equation.

In terms of log-pressure altitude, the model top level is found at
:math:`Z=140` km (:math:`z\simeq 150` km). It should be noted that the
solution in the top 15-20 km of the model is undoubtedly affected by the
presence of the top boundary. However, it should not be thought of as a
*sponge layer*, since molecular diffusion is a real process and is the
primary damping on upward propagating waves near the model top. Indeed,
this was a major consideration in moving the model top well above the
turbopause. Considerable effort has been expended in formulating the
upper boundary conditions to obtain realistic solutions near the model
top and all of the important physical and chemical processes for that
region have been included.

The standard vertical resolution is variable; it is 3.5 km above about
65 km, 1.75 km around the stratopause (50 km), 1.1-1.4 km in the lower
stratosphere (below 30 km), and 1.1 km in the troposphere (except near
the ground where much higher vertical resolution is used in the
planetary boundary layer).

Two standard horizontal resolutions are supported in |waccm|: the |lowres| (latitude
:math:`\times` longitude) low resolution version has 72 longitude and 46
latitude points; the |medres| medium resolution version has 96 longitude and 144
latitude points. A |higres| high resolution version of  has had limited testing,
and is not yet supported, due to computational cost constraints. The
|lowres| version has been used extensively for MLT studies, where it gives very
similar results to the |medres| version. However, caution should be exercised in
using |lowres| results below the stratopause, since the meridional resolution
may not be sufficient to represent adequately the dynamics of either the
polar vortex or synoptic and planetary waves.

At all resolutions, the time step is 1800 s for the physical
parameterizations. Within the finite volume dynamical core, this time
step is subdivided as necessary for computational stability.

Molecular Diffusion and Constituent Separation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The vertical diffusion parameterization in CAM4 provides the interface
to the turbulence parameterization, computes the molecular diffusivities
(if necessary) and finally computes the tendencies of the input
variables. The diffusion equations are actually solved implicitly, so
the tendencies are computed from the difference between the final and
initial profiles. In |waccm|, we extend this parameterization to include the
terms required for the gravitational separation of constituents of
differing molecular weights. The formulation for molecular diffusion
follows (**???**)

A general vertical diffusion parameterization can be written in terms of
the divergence of diffusive fluxes:

.. math::
   :label: eq:contz1

   \begin{aligned}
   \frac{\partial }{\partial t} (u,v,q) 
   	&=& - \frac{1}{\rho} \frac{\partial}{\partial z} (F_u, F_v, F_q) \\
   \end{aligned}

.. math::
   :label: eq:contz3

   \begin{aligned}
   \frac{\partial}{\partial t} s
   	&=& - \frac{1}{\rho} \frac{\partial}{\partial z} F_H + D 
   \end{aligned}

where :math:`s = c_p T + g z` is the dry static energy, :math:`z` is the
geopotential height above the local surface (does not include the
surface elevation) and :math:`D` is the heating rate due to the
dissipation of resolved kinetic energy in the diffusion process. The
diffusive fluxes are defined as:

.. math::
   :label: eq:fluxz1

   F_{u,v} =-\rho K_m \frac{\partial}{\partial z}(u,v),  

.. math::
   :label: eq:fluxz2

   F_{H}   =-\rho K_H \frac{\partial s}{\partial z}
   	    +\rho K_H^t\gamma_{H}                    , 

.. math::
   :label: eq:fluxz3

   F_{q}  =-\rho K_q \frac{\partial q}{\partial z}
   	    +\rho K_q^t\gamma_{q}  + {\rm sep-flux}  . 

The viscosity :math:`K_m` and diffusivities :math:`K_{q,H}` are the
sums of: turbulent components :math:`K_{m,q,H}^t`, which dominate below
the mesopause; and molecular components :math:`K_{m,q,H}^m`, which
dominate above  120 km. The non-local transport terms
:math:`\gamma_{q,H}` are given by the ABL parameterization and and the
kinetic energy dissipation is

.. math::
   :label: eq:diss_heat

   D \equiv -\frac{1}{\rho} \left( F_u\frac{\partial u}{\partial z} 
                 +  F_v\frac{\partial v}{\partial z} \right). 

The treatment of the turbulent diffusivities :math:`K_{m,q,H}^t`, the
energy dissipation :math:`D` and the nonlocal transport terms
:math:`\gamma_{H,q}` is described in the  Technical Description and will
be omitted here.

Molecular viscosity and diffusivity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The empirical formula for the molecular kinematic viscosity is

.. math:: K_m^m = 3.55\times 10^{-7} T^{2/3} / \rho, 
	  :label: Kmm

and the molecular diffusivity for heat is

.. math:: K_H^m = P_r K_m^m,                         
	  :label: Kmh

where :math:`P_r` is the Prandtl number and we assume :math:`P_r=1` in
|waccm|. The constituent diffusivities are

.. math:: K_q^m = T^{1/2} M_w/ \rho,                 
	  :label: Kmq

where :math:`M_w` is the molecular weight.

Diffusive separation velocities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As the mean free path increases, constituents of different molecular
weights begin to separate in the vertical. In |waccm|, this separation is
represented by a separation velocity for each constituent with respect
mean air. Since  extends only into the lower thermosphere, we avoid the
full complexity of the separation problem and represent mean air by the
usual dry air mixture used in the lower atmosphere
(:math:`M_w = 28.966`) (:cite:`banks-kockarts:73`).

Discretization of the vertical diffusion equations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In CAM4, as in previous version of the CCM, :eq:`eq:contz1` [eq:fluxz2])
are cast in pressure coordinates, using

.. math:: dp = -\rho g dz,   
	  :label: eq:hydrostatic

and discretized in a time-split form using an Euler backward time step.
Before describing the numerical solution of the diffusion equations, we
define a compact notation for the discrete equations. For an arbitrary
variable :math:`\psi`, let a subscript denote a discrete time level,
with current step :math:`\psi_n` and next step :math:`\psi_{n+1}`. The
model has :math:`L` layers in the vertical, with indexes running from
top to bottom. Let :math:`\psi^k` denote a layer midpoint quantity and
let :math:`\psi^{k\pm}` denote the value at the interface above (below)
:math:`k`. The relevant quantities, used below, are then:

.. math::

   \begin{aligned}
   \psi^{k+}&=&(\psi^{k}+\psi^{k+1})/2,\quad k\in (1,2,3,...,L-1) \nonumber \\
   \psi^{k-}&=&(\psi^{k-1}+\psi^{k})/2,\quad k\in (2,3,4...,L)    \nonumber \\
   \delta^{k}\psi &=& \psi^{k+}-\psi^{k-},       \nonumber \\
   \delta^{k+}\psi &=& \psi^{k+1}-\psi^{k},      \nonumber \\
   \delta^{k-}\psi &=& \psi^{k}-\psi^{k-1},      \nonumber \\
   \psi_{n+}&=&(\psi_{n}+\psi_{n+1})/2,          \nonumber \\
   \delta_n\psi &=& \psi_{n+1}-\psi_{n},         \nonumber \\
   \delta t &=& t_{n+1}-t_{n},                   \nonumber \\
   \Delta^{k,l} &=& 1,\ k=l,          \nonumber \\
                &=& 0,\ k\neq l.      \nonumber\end{aligned}

Like the continuous equations, the discrete equations are required to
conserve momentum, total energy and constituents. Neglecting the
nonlocal transport terms, the discrete forms of
:eq:`eq:contz1` [eq:contz3]) are:

.. math::
   :label: eq:vduvq

   \frac{\delta_n (u,v,q)^k}{\delta t} = g \frac{\delta^k F_{u,v,q}}{\delta^k p}    

.. math::
   :label: eq:vds

   \frac{\delta_n s^k}{\delta t} = g \frac{\delta^k F_{H}}{\delta^k p} + D^k.  

For interior interfaces, :math:`1\le k \le L-1`,

.. math::
   :label: eq:vdfuv


   F_{u,v}^{k+} = \left(g\rho^2 K_m\right)_n^{k+} \frac{\delta^{k+} (u,v)_{n+1}} {\delta^{k+} p}

.. math::
   :label: eq:vdfqs

   F_{q,H}^{k+} = \left(g\rho^2 K_{q,H}\right)_n^{k+} \frac{\delta^{k+} (u,v)_{n+1}} {\delta^{k+} p}.

Surface fluxes :math:`F_{u,v,q,H}^{L+}` are provided explicitly at time
:math:`n` by separate surface models for land, ocean, and sea ice while
the top boundary fluxes are usually :math:`F_{u,v,q,H}^{1-}=0`. The
turbulent diffusion coefficients :math:`K_{m,q,H}^{t}` and non-local
transport terms :math:`\gamma_{q,H}` are calculated for time :math:`n`
by the turbulence model (identical to CAM4). The molecular diffusion
coefficients, given by :eq:`Kmm` [Kmq]) are also evaluated at time
:math:`n`.

Solution of the vertical diffusion equations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Neglecting the discretization of :math:`K_{m,q,H}^t`, :math:`D` and
:math:`\gamma_{q,H}`, a series of time-split operators is defined by
:eq:`eq:vduvq` [eq:vdfqs]). Once the diffusivities (:math:`K_{m,q,H}`) and
the non-local transport terms (:math:`\gamma_{q,H}`) have been
determined, the solution of :eq:`eq:vduvq` [eq:vdfqs]), proceeds in several
steps.

#. update the bottom level values of :math:`u`, :math:`v`, :math:`q` and
   :math:`s` using the surface fluxes;

#. invert :eq:`eq:vduvq`  and :eq:`eq:vdfuv`  for :math:`u,v_{n+1}`;

#. compute :math:`D` and use to update the :math:`s` profile;

#. invert :eq:`eq:vduvq` [eq:vds]) and :eq:`eq:vdfqs`  for :math:`s_{n+1}` and
   :math:`q_{n+1}`

Note that since all parameterizations in CAM4 return tendencies rather
modified profiles, the actual quantities returned by the vertical
diffusion are :math:`\delta_n (u,v,s,q) / \delta t`.

Equations :eq:`eq:vduvq` [eq:vdfqs]) constitute a set of four tridiagonal
systems of the form

.. math::
   :label: eq:tridiag1

   -A^k \psi^{k+1}_{n+1} + B^k\psi^k_{n+1} -C^k\psi^{k-1}_{n+1} 
   	= \psi^k_{n\prime},

where :math:`\psi_{n\prime}` indicates :math:`u`, :math:`v`, :math:`q`,
or :math:`s` after updating from time :math:`n` values with the nonlocal
and boundary fluxes. The super-diagonal (:math:`A^k`), diagonal
(:math:`B^k`) and sub-diagonal (:math:`C^k`) elements of :eq:`eq:tridiag1` 
are:

.. math::

   \begin{aligned}
   A^k &=& \frac{1}{\delta^{k} p} 
   	\frac{\delta t}{\delta^{k+}p}\left(g^2\rho^2 K\right)_n^{k+},\\
   B^k &=& 1 + A^k + C^k, \\
   C^k &=& \frac{1}{\delta^{k} p} 
   	\frac{\delta t}{\delta^{k-}p}\left(g^2\rho^2 K\right)_n^{k-}.\end{aligned}

The solution of :eq:`eq:tridiag1`  has the form

.. math:: \psi^k_{n+1} = E^k \psi^{k-1}_{n+1} + F^k,           
	  :label: eq:tridiag2

or,

.. math:: \psi^{k+1}_{n+1} = E^{k+1} \psi^{k}_{n+1} + F^{k+1}. 
	  :label: eq:tridiag3

Substituting :eq:`eq:tridiag3`  into :eq:`eq:tridiag1` ,

.. math::
   :label: eq:tridiag4

   \psi^{k}_{n+1} = \frac{C^k}{B^k - A^k E^{k+1}} \psi^{k-1}_{n+1} 
   	+ \frac{\psi^k_{n\prime} + A^k F^{k+1}}{B^k - A^k E^{k+1}}.
   	

Comparing :eq:`eq:tridiag2`  and :eq:`eq:tridiag4` , we find

.. math::
   :label: eq:tridiag5

   E^k = \frac{C^k} {B^k - A^k E^{k+1}}, \quad L>k>1,  

.. math::
   :label: eq:tridiag6
	   
   F^k = \frac{\psi^k_{n\prime} + A^k F^{k+1}}{B^k - A^k E^{k+1}}, \quad L>k>1 

The terms :math:`E^k` and :math:`F^k` can be determined upward from
:math:`k=L`, using the boundary conditions

.. math:: E^{L+1} = F^{L+1} = A^L = 0.

Finally, :eq:`eq:tridiag4`  can be solved downward for
:math:`\psi^{k}_{n+1}`, using the boundary condition

.. math:: C^1 = 0 \Rightarrow E^1 = 0.

CCM1-3 used the same solution method, but with the order of the solution
reversed, which merely requires writing :eq:`eq:tridiag3`  for
:math:`\psi^{k-1}_{n+1}` instead of :math:`\psi^{k+1}_{n+1}`. The order
used here is particularly convenient because the turbulent diffusivities
for heat and all constituents are the same but their molecular
diffusivities are not. Since the terms in :eq:`eq:tridiag5` and :eq:`eq:tridiag6`
are determined from the bottom upward, it is only necessary to
recalculate :math:`A^k`, :math:`C^k`, :math:`E^k` and :math:`1/({B^k - A^k E^{k+1}})` 
for each constituent within the region where molecular
diffusion is important.

Gravity Wave Drag
~~~~~~~~~~~~~~~~~

Vertically propagating gravity waves can be excited in the atmosphere
where stably stratified air flows over an irregular lower boundary and
by internal heating and shear.  These waves are capable of
transporting significant quantities of horizontal momentum between
their source regions and regions where they are absorbed or
dissipated.  Previous GCM results have shown that the large-scale
momentum sinks resulting from breaking gravity waves play an important
role in determining the structure of the large-scale flow. CAM4 
incorporates a parameterization for a spectrum of vertically
propagating internal gravity waves based on the work of
:cite:`lindzen:81`, :cite:`holton:82`,
:cite:`garcia-solomon:85` and 
:cite:`mcfarlane:87`. The parameterization solves separately for a general
spectrum of monochromatic waves and for a single stationary wave generated by
flow over orography, following :cite:`mcfarlane:87`. The spectrum is omitted in
the standard tropospheric version of CAM4, as in previous versions of the CCM.
Here we describe the modified version of the gravity wave spectrum
parameterization used in |waccm|. 

Adiabatic inviscid formulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Following (**???**), the continuous equations for the gravity wave
parameterization are obtained from the two-dimensional hydrostatic
momentum, continuity and thermodynamic equations in a vertical plane:

.. math::
   :label: eq:gw_mom

   \left( \frac{\partial}{\partial t} + u\frac{\partial}{\partial x}\right)u 
     = -\frac{\partial\Phi}{\partial x}\, ,  

.. math::
   :label: eq:gw_cont

   \frac{\partial u}{\partial x} + \frac{\partial W}{\partial Z} = 0\, ,
                                             

.. math::
   :label: eq:gw_therm

   \left( \frac{\partial}{\partial t} + u\frac{\partial}{\partial x}\right)
   \ \frac{\partial\Phi}{\partial Z} + N^2 w = 0\, . 

Where :math:`N` is the local Brunt-Väisällä frequency, and :math:`W` is
the vertical velocity in log pressure height (:math:`Z`) coordinates.
Eqs. :eq:`eq:gw_mom` –:eq:`eq:gw_therm`  are linearized
about a large scale background wind :math:`\overline u`, with
perturbations :math:`u^\prime,w^\prime`, and combined to obtain:

.. math::
   :label: eq:gw_lin

   \left( \frac{\partial}{\partial t} + 
     {\overline u}\frac{\partial}{\partial x}\right)^2 
        \frac{\partial^2 w^\prime}{\partial Z^2} 
      + N^2 \frac{\partial^2 w^\prime}{\partial x^2} = 0\, . 

Solutions to :eq:`eq:gw_lin`  are assumed to be of the form:

.. math:: 
   :label: eq:gw_sol

   w^\prime = {\hat w} \, e^{ik(x-ct)} \, e^{Z/2H} \, , 

where :math:`H` is the scale height, :math:`k` is the horizontal
wavenumber and :math:`c` is the phase speed of the wave. Substituting
:eq:`eq:gw_sol` into :eq:`eq:gw_lin` , one obtains:

.. math::
   :label: eq:gw_what

   -k^2 (\overline u -c)^2 
    \left( \frac{\partial}{\partial Z} + \frac{1}{2H} \right)^2{\hat w}
    - k^2 N^2 {\hat w} = 0\, . 

Neglecting :math:`\frac{1}{2H}` compared to
:math:`\frac{\partial}{\partial Z}` in eq:`gw_what`, one
obtains the final form of the two dimensional wave equation:

.. math:: 
   :label: eq:gw_2d

   \frac{d^2 {\hat w}}{d Z^2} + \lambda^2 {\hat w} = 0\, , 

with the coefficient defined as:

.. math:: 
   :label: eq:gw_lam

   \lambda= \frac{N}{(\overline u -c)}\, . 

The WKB solution of :eq:`eq:gw_2d`  is:

.. math::
   :label: eq:gw_wkbsol

   {\hat w} = A \lambda^{-1/2}\exp\left(i\int_0^Z\lambda
   dz^\prime\right)\, , 

and the full solution, from :eq:`eq:gw_sol` , is:

.. math::
   :label: eq:gw_final

   w^\prime(Z,t) = A \lambda^{-1/2}\exp\left(i\int_0^Z\lambda
   dz^\prime\right) \ e^{ik(x-ct)}\  e^{Z/2H} \, .  

The constant :math:`A` is determined from the wave amplitude at the
source (:math:`z=0`), The Reynolds stress associated with
eq:`eq:gw_final` is:

.. math::
   :label: eq:gw_reyn

   \tau(Z) = \tau(0) = \rho\overline{ u^\prime  w^\prime} = -\frac{2}{k}
   |A|^2\rho_0{\rm sgn}(\lambda)\, , 

and is conserved, while the momentum flux
:math:`\overline{ u^\prime  w^\prime} = -(m/k)\ \overline{w^\prime w^\prime}`
grows exponentially with altitude as :math:`\exp(Z/H)`, per
:eq:`eq:gw_final`. We note that the vertical flux of wave energy
is :math:`c_{gz}\ E' = (U-c)\ \tau` ((**???**)), where :math:`c_{gz}` is
the vertical group velocity, so that deposition of wave momentum into
the mean flow will be accompanied by a transfer of energy to the
background state.

Saturation condition
^^^^^^^^^^^^^^^^^^^^

The wave amplitude in :eq:`eq:gw_final`  grows as :math:`e^{Z/2H}`
until the wave becomes unstable to convective overturning,
Kelvin-Helmholtz instability, or other nonlinear processes. At that
point, the wave amplitude is assumed to be limited to the amplitude that
would trigger the instability and the wave is “saturated”. The
saturation condition used in CAM4 is from (**???**), based on a maximum
Froude number (:math:`F_c`), or streamline slope.

.. math::
   :label: eq:gw_satcond

   |\rho\overline{ u^\prime  w^\prime}| 
       \leq \tau^{*} = F_c^2\frac{k}{2}\rho \frac{|\overline{u}-c|^3}{N}
     \, , 

where :math:`\tau^*` is the saturation stress and :math:`F_c^2=0.5`. In
, :math:`F_c^2=1` and is omitted hereafter. Following (**???**), within
a saturated region the momentum tendency can be determined analytically
from the divergence of :math:`\tau^*`:

.. math::
   :label: eq:gw_utend

   \begin{aligned}
   \frac{\partial \overline u}{\partial t} &= -\frac{e}{\rho}\frac{\partial}{\partial Z}
    \rho\overline{ u^\prime  w^\prime}\, , \nonumber \\
   & \simeq -e \frac{k}{2} \frac{(\overline u-c)^3}{N}
        \frac{1}{\rho}\frac{\partial\rho}{\partial Z}\, , \nonumber \\
   & \simeq -e \frac{k}{2} \frac{(\overline u-c)^3}{N H}, \end{aligned}

where :math:`e` is an “efficiency” factor. For a background wave
spectrum, :math:`e` represents the temporal and spatial intermittency in
the wave sources. The analytic solution :eq:`eq:gw_utend`  is not
used in |waccm|; it is shown here to illustrate how the acceleration due to
breaking gravity waves depends on the intrinsic phase speed. In the
model, the stress profile is computed at interfaces and differenced to
get the specific force at layer midpoints.

Diffusive damping
^^^^^^^^^^^^^^^^^

In addition to breaking as a result of instability, vertically
propagating waves can also be damped by molecular diffusion (both
thermal and momentum) or by radiative cooling. Because the intrinsic
periods of mesoscale gravity waves are short compared to IR relaxation
time scales throughout the atmosphere, we ignore radiative damping. We
take into account the molecular viscosity, :math:`K_m^m`, such that the
stress profile is given by:

.. math::
   :label: eq:gw_taudamp

   \tau(Z) =  \tau(Z_t) \exp\left(-\frac{2}{H}\int_0^Z\lambda_i
   dz^\prime\right) \, , 
   

where :math:`Z_t` denotes the top of the region, below :math:`Z`, not
affected by thermal dissipation or molecular diffusion. The imaginary
part of the local vertical wavenumber, :math:`\lambda_i` is then:

.. math::
   :label: eq:gw_lambdai

   \lambda_i = \frac{N^3 \ K_m^m}{2 k (\overline u -c)^4 } \, .
   

In |waccm|, (:eq:`eq:gw_taudamp` – :eq:`eq:gw_lambdai`) are only used
within the domain where molecular diffusion is important (above
:math:`\sim 75` km). At lower altitudes, molecular diffusion is
negligible, :math:`\lambda_i \rightarrow 0`, and :math:`\tau` is
conserved outside of saturation regions.

Transport due to dissipating waves
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When the wave is dissipated, either through saturation or diffusive
damping, there is a transfer of wave momentum and energy to the
background state. In addition, a phase shift is introduced between the
wave’s vertical velocity field and its temperature and constituent
perturbations so that fluxes of heat and constituents are nonzero within
the dissipation region. The nature of the phase shift and the resulting
transport depends on the dissipation mechanism; in |waccm|, we assume that the
dissipation can be represented by a linear damping on the potential
temperature and constituent perturbations. For potential temperature,
:math:`\theta`, this leads to:

.. math::
   :label: eq:gw_thetaprime

   \left( {\partial \over \partial t} + \overline u {\partial \over \partial x}
   \right) \theta^\prime + w' {\partial \overline\theta \over \partial z} 
   = -\delta \theta^\prime \, , 

where :math:`\delta` is the dissipation rate implied by wave breaking,
which depends on the wave’s group velocity, :math:`c_{gz}` (see :cite:`garcia:91`).

.. math::
   :label: eq:gw_dissip

   \delta = {c_{gz} \over 2H} = k \ {(\overline u - c)^2 \over 2H N} 
   \, .

Substitution of :eq:`eq:gw_dissip`  into
:eq:`eq:gw_thetaprime`  then yields the eddy heat flux:

.. math::
   :label: eq:gw_kzz

   \overline{w^\prime \theta^\prime} 
   = -\left[ {\delta \ \overline{w^\prime w^\prime} 
   \over k^2(\overline u - c)^2 + \delta^2} \right]
   {\partial \overline\theta \over \partial z} \, .  

Similar expressions can be derived for the flux of chemical
constituents, with mixing ratio substituted in place of potential
temperature in ([eq:gw:sub:`k`\ zz]). We note that these wave fluxes are
always downgradient and that, for convenience of solution, they may be
represented as vertical diffusion, with coefficient :math:`K_{zz}` equal
to the term in brackets in :eq:`eq:gw_kzz` , but they do not
represent turbulent diffusive fluxes but rather eddy fluxes. Any
additional turbulent fluxes due to wave breaking are ignored. To take
into account the effect of localization of turbulence (e.g., :cite:`fritts-dunkerton:85,mcintyre:89`)
:eq:`eq:gw_kzz`  is multiplied times an inverse Prandtl
number, :math:`{Pr}^{-1}`; in |waccm| we use :math:`{Pr}^{-1}=0.25`.

Heating due to wave dissipation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The vertical flux of wave energy density, :math:`E'`, is related to the
stress according to:

.. math:: c_{gz} \ E' = (\overline u-c) \ \tau \ ,

where :math:`c_{gz}` is the vertical group velocity [Andrews et al.,
1987]. Therefore, the stress divergence
:math:`\partial \tau / \partial Z` that accompanies wave breaking
implies a loss of wave energy. The rate of dissipation of wave energy
density is:

.. math::

   {\partial E' \over \partial t} 
   \simeq (\overline u-c) {1 \over c_{gz}}{\partial \tau \over \partial t}
   = (\overline u-c) {\partial \tau \over \partial Z} \ .

For a saturated wave, the stress divergence is given by
:eq:`eq:gw_utend` , so that:

.. math::
   :label: eq:gw_eprime

   {\partial E' \over \partial t} = 
   (\overline u - c) \ {\partial \, \tau^* \over \partial Z}
   = - e \cdot \rho \ {k \, (U-c)^4 \over 2 N H} \ .       

This energy loss by the wave represents a heat source for the
background state, as does the change in the background kinetic energy
density implied by wave drag on the background flow:

.. math::
   :label: eq:gw_kbar

   {\partial \overline K \over \partial t} \equiv 
   {\rho \over 2} {\partial \overline u^2 \over \partial t} = 
   \overline u \ {\partial \, \tau^* \over \partial Z} =
   -e \cdot \rho \ {k \, \overline u \, (\overline u-c)^3 \over 2 NH} \ , 

which follows directly from :eq:`eq:gw_utend` . The background
heating rate, in K sec\ :math:`^{-1}`, is then:

.. math::

   Q_{gw} = -{1 \over \rho\, c_p}
   \left[{\partial \overline K \over \partial t} 
   + {\partial E' \over \partial t} \right].

Using :math:`(\ref{eq:gw_eprime})-(\ref{eq:gw_kbar})`, this heating
rate may be expressed as:

.. math::
   :label: eq:gw_qgw

   Q_{gw} = 
     {1 \over \rho\, c_p} \ c \ {\partial \, \tau^* \over \partial Z} =
     {1 \over c_p} \left[ \ e  \cdot  {k \, c\,(c-\overline u)^3 \over 2 N H} \right] ,
     

where :math:`c_p` is the specific heat at constant pressure. In |waccm|,
:math:`Q_{gw}` is calculated for each component of the gravity wave
spectrum using the first equality in :eq:`eq:gw_qgw` , i.e., the
product of the phase velocity times the stress divergence.

Orographic source function
^^^^^^^^^^^^^^^^^^^^^^^^^^

For orographically generated waves, the source is taken from (**???**):

.. math::
   :label: eq:oro_tau

   \tau_g = |\rho\overline{ u^\prime  w^\prime}|_0 
      = \frac{k}{2} h_0^2 \rho_0 N_0 \overline u_0\, , 

where :math:`h_0` is the streamline displacement at the source level,
and :math:`\rho_0`, :math:`N_0`, and :math:`\overline u_0` are also
defined at the source level. For orographic waves, the subgrid-scale
standard deviation of the orography :math:`\sigma` is used to estimate
the average mountain height, determining the typical streamline
displacement. An upper bound is used on the displacement (equivalent to
defining a “separation streamline”) which corresponds to requiring that
the wave not be supersaturated at the source level:

.. math:: h_0=\min(2\sigma,  \frac{\overline u_0}{N_0})\, . 
	  :label: eq:oro_h0

The source level quantities :math:`\rho_0`, :math:`N_0`, and
:math:`\overline u_0` are defined by vertical averages over the source
region, taken to be :math:`2\sigma`, the depth to which the average
mountain penetrates into the domain:

.. math::
   :label: 4.e.18

   \psi_0 = \int_0^{2\sigma} \psi\rho dz, \qquad \psi \in \{\rho,N,
   u, v\} \, . 

The source level wind vector :math:`(u_0,v_0)` determines the
orientation of the coordinate system in
:eq:`eq:gw_mom` –:eq:`eq:gw_therm`  and the magnitude of the
source wind :math:`\overline u_0`.

Non-orographic source functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The source spectrum for non-orographic gravity waves is no longer
assumed to be a specified function of location and season, as was the
case with the earlier version of the model described by (**???**).
Instead, gravity waves are launched according to trigger functions that
depend on the atmospheric state computed in WACCM4 at any given time and
location, as discussed by (**???**). Two trigger functions are used:
convective heat release (which is a calculated model field) and a
"frontogenesis function", (**???**), which diagnoses regions of
strong wind field deformation and temperature gradient using the
horizontal wind components and potential temperature field calculated by
the model.

In the case of convective excitation, the method of (**???**) is used to
determine a phase speed spectrum based upon the properties of the
convective heating field. A spectrum is launched whenever the deep
convection parameterization in WACCM4 is active, and the vertical
profile of the convective heating, together with the mean wind field in
the heating region, are used to determine the phase speed spectrum of
the momentum flux. Convectively generated waves are launched at the top
of the convective region (which varies according to the depth of the
convective heating calculated in the model).

Waves excited by frontal systems are launched whenever the frontogenesis
trigger function exceeds a critical value (see (**???**)). The waves are
launched from a constant source level, which is specified to be 600 mb.
The momentum flux phase speed spectrum is given by a Gaussian function
in phase speed:

.. math::
   :label: eq:tau_s

   \tau_s (c)  = \tau_b
      \exp\left[-\left( \frac{c - V_s}{c_w} \right)^2\right], 

centered on the source wind, :math:`V_s = |{\bf V}_s|`, with width
:math:`c_w=30` m/s. A range of phase speeds with specified width and
resolution is used:

.. math::
   :label: eq:phase_s

   c \in V_s + [\pm d_c, \pm 2d_c, ... \pm c_{max}]\, , 

with :math:`d_c = 2.5` m s\ :math:`^{-1}` and :math:`c_{max} = 80` m
s\ :math:`^{-1}`, giving 64 phase speeds. Note that :math:`c=V_s` is
retained in the code for simplicity, but has a critical level at the
source and, therefore, :math:`\tau_s(c=V_s)=0`. Note also that
:math:`\tau_b` is a tunable parameter; in practice this is set such that
the height of the polar mesopause, which is very sensitive to gravity
wave driving, is consistent with observations. In WACCM4, :math:`\tau_b`
= 1.5 x 10\ :math:`^{-3}` Pa.

Above the source region, the saturation condition is enforced separately
for each phase speed, :math:`c_i`, in the momentum flux spectrum:

.. math::
   :label: eq:tau_i

   \tau(c_i) \leq \tau_i^{*}
        =F_c^2 \frac{k}{2}\rho \frac{|\overline u-c_i|^3}{N} .

Numerical approximations
^^^^^^^^^^^^^^^^^^^^^^^^

The gravity wave drag parameterization is applied immediately after the
nonlinear vertical diffusion. The interface Brunt-Väisällä frequency is

.. math::
   :label: 4.e.25

   \left(N^{k+}\right)^2 = \frac{g^2}{T^{k+}} \left( \frac{1}{c_p}
      - \rho^{k+} \frac{\delta^{k+} T}{\delta^{k+} p} \right) \, , 

Where the interface density is:

.. math:: \rho^{k+} = \frac{R T^{k+}}{p^{k+}}.

The midpoint Brunt-Väisällä frequencies are
:math:`N^k=(N^{k+}+N^{k-})/2`.

The level for the orographic source is an interface determined from an
estimate of the vertical penetration of the subgrid mountains within the
grid box. The subgrid scale standard deviation of the orography,
:math:`\sigma_h`, gives the variation of the mountains about the mean
elevation, which defines the Earth’s surface in the model. Therefore the
source level is defined as the interface, :math:`k_s-1/2`, for which
:math:`z^{k_s+} < 2\sigma_h <
z^{k_s-}`, where the interface heights are defined from the midpoint
heights by :math:`z^{k+} = \sqrt(z^{k} z^{k+1})`.

The source level wind vector, density and Brunt-Väisällä frequency are
determined by vertical integration over the region from the surface to
interface :math:`k_s+1/2`:

.. math::
   :label: 4.e.27

   \psi_0 = \sum_{k=k_s}^K \psi^k \delta^k p\, , \qquad \psi \in
   \{\rho,N, u, v\} \, . 

The source level background wind is :math:`\overline u_0 =\sqrt(u_0^2 +
v_0^2)`, the unit vector for the source wind is

.. math:: 
   :label: 4.e.28

   (x_0, y_0) = (u_0, v_0) /\overline u_0 \, , 

and the projection of the midpoint winds onto the source wind is

.. math:: 
   :label: 4.e.29

   \overline u^k = u^k x_0 + v^k y_0 \, . 

Assuming that :math:`\overline u_0 > 2` m s\ :math:`^{-1}` and
:math:`2\sigma^h > 10` m, then the orographic source term,
:math:`\tau_g` is given by :eq:`eq:oro_tau`  and
:eq:`eq:oro_h0` , with :math:`F_c^2` =1 and :math:`k = 2\pi/10^5`
m\ :math:`^{-1}`. Although the code contains a provision for a linear
stress profile within a “low level deposition region”, this part of the
code is not used in the standard model.

The stress profiles are determined by scanning up from the bottom of the
model to the top. The stress at the source level is determined by
:eq:`eq:oro_tau` . The saturation stress, :math:`\tau^*_\ell` at
each interface is determined by :eq:`eq:tau_i` , and
:math:`\tau^*_\ell=0` if a critical level is passed. A critical level is
contained within a layer if
:math:`(\overline u^{k+} -c_\ell) / (\overline u^{k-} -c_\ell) < 0`.

Within the molecular diffusion domain, the imaginary part of the
vertical wavenumber is given by :eq:`eq:gw_lambdai` . The interface
stress is then determined from the stress on the interface below by:

.. math::
   :label: eq:tau_km

   \tau^{k-} = \min \left[ \left(\tau^*\right)^{k-}, 
      \tau^{k+}\exp\left( -2 \lambda_i \frac{R}{g} T^k \delta^k\ln p
           \right) \right] \, . 

Below the molecular diffusion domain, the exponential term in
:eq:`eq:tau_km`  is omitted.

Once the complete stress profile has been obtained, the forcing of the
background wind is determined by differentiating the profile during a
downward scan:

.. math::
   :label: 4.e.35

   \frac{\partial \overline u^k_\ell}{\partial t} = 
       g \frac{\delta^k\tau_\ell}{\delta^k p}
       < \left( \frac{\partial \overline u^k_\ell}{\partial t}\right)^{\rm max}
       \, . 

.. math::
   :label: 4.e.36

   \left( \frac{\partial \overline u^k_\ell}{\partial t}\right)^{\rm max} 
     = \min\left[
       \frac{|c_\ell - \overline u^k_\ell|}{2 \delta t}\, ,
       500 {\rm ~m ~s^{-1}~ day^{-1}}
       \right]
   \, . 

The first bound on the forcing comes from requiring that the forcing
not be large enough to push the wind more than half way towards a
critical level within a time step and takes the place of an implicit
solution. This bound is present for numerical stability, it comes into
play when the time step is too large for the forcing. It is not feasible
to change the time step, or to write an implicit solver, so an *a
priori* bound is used instead. The second bound is used to constrain the
forcing to lie within a physically plausible range (although the value
used is extremely large) and is rarely invoked.

When any of the bounds in :eq:`4.e.35`  are invoked, conservation of stress
is violated. In this case, stress conservation is ensured by decreasing
the stress on the lower interface to match the actual stress divergence
in the layer:

.. math::
   :label: 4.e.37

   \tau^{k+}_\ell = \tau^{k-}_\ell + 
      \frac{\partial \overline u^k}{\partial t}  
      \frac{\delta^k p}{g} \, . 

This has the effect of pushing some of the stress divergence into the
layer below, a reasonable choice since the waves are propagating up from
below.

Finally, the vector momentum forcing by the gravity waves is determined
by projecting the background wind forcing with the unit vectors of the
source wind:

.. math::
   :label: 4.e.38

   \frac{\partial {\bf V}^k}{\partial t} =  (x_0, y_0) \times E \sum_\ell
         \frac{\partial \overline u^k_\ell}{\partial t}
   \, . 

In addition, the frictional heating implied by the momentum tendencies,
:math:`\frac{1}{c_p} {\bf V}^k \cdot {\partial {\bf V}^k / \partial t}`,
is added to the thermodynamic equation. This is the correct heating for
orographic (:math:`c_\ell=0`) waves, but not for waves with
:math:`c_\ell\ne 0`, since it does not account for the wave energy flux.
This flux is accounted for in some middle and upper atmosphere versions
of CAM4, but also requires accounting for the energy flux at the source.

Turbulent Mountain Stress
~~~~~~~~~~~~~~~~~~~~~~~~~

An important difference between WACCM4 and earlier versions is the
addition of surface stress due to unresolved orography. A numerical
model can compute explicitly only surface stresses due to resolved
orography. At the standard 1.9\ :math:`^\circ` x 2.5\ :math:`^\circ`
(longitude x latitude) resolution used by WACCM4 only the gross outlines
of major mountain ranges are resolved. To address this problem,
unresolved orography is parameterized as turbulent surface drag, using
the concept of effective roughness length developed by (**???**).
Fiedler and Panofsky defined the roughness length for heterogeneous
terrain as the roughness length that homogenous terrain would have to
give the correct surface stress over a given area. The concept of
effective roughness has been used in several Numerical Weather
Prediction models (e.g., (**???**); (**???**)).

In WACCM4 the effective roughness stress is expressed as:

.. math::
   :label: tms

   \tau = \rho \, C_d \, |{\bf V}| {\bf V} \, , 
   

where :math:`\rho` is the density and :math:`C_d` is a turbulent drag
coefficient,

.. math:: C_d = \frac{f(R_i)\, k ^2}{\ln^2\left[\frac{z+z_0}{z_0}\right]} \, ,

:math:`k` is von Kármán’s constant; :math:`z` is the height above the
surface; :math:`z_0` is an effective roughness length, defined in terms
of the standard deviation of unresolved orography; and :math:`f(R_i)` is
a function of the Richardson number (see (**???**) for details).

The stress calculated by :eq:`tms`  is used the model’s nonlocal PBL scheme
to evaluate the PBL height and nonlocal transport, per Eqs.
(3.10)Ð(3.12) of (**???**). This calculation is carried out only over
land, and only in grid cells where the height of topography above sea
level, :math:`z`, is nonzero.

QBO Forcing
~~~~~~~~~~~

WACCM4 has several options for forcing a quasi-biennial oscillation
(QBO) by applying a momentum forcing in the tropical stratosphere. The
parameterization relaxes the simulated winds to a specified wind field
that is either fixed or varies with time. The parameterization can also
be turned off completely. The namelist variables and input files can be
selected to choose one of the following options:

-  Idealized QBO East winds, used for perpetual fixed-phase of the QBO,
   as described by (**???**).

-  Idealized QBO West winds, as above but for the west phase.

-  Repeating idealized 28-month QBO, also described by (**???**).

-  QBO for the years 1953-2004 based on the climatology of Giorgetta
   [see:
   http://www.pa.op.dlr.de/CCMVal/Forcings/qbo\_data\_ccmval/u\_profile\_195301-200412.html,
   2004].

-  QBO with a 51-year repetition, based on the 1953-2004 climatology of
   Giorgetta, which can be used for any calendar year, past or future.

The relaxation of the zonal wind is based on (**???**) and is described
in (**???**). The input winds are specified at the equator and the
parameterization extends latitudinally from 22\ :math:`^{\circ}`\ N to
22\ :math:`^{\circ}`\ S, as a Gaussian function with a half width of
10\ :math:`^{\circ}` centered at the equator. Full vertical relaxation
extends from 86 to 4 hPa with a time constant of 10 days. One model
level below and above this altitude range, the relaxation is half as
strong and is zero for all other levels. This procedure constrains the
equatorial winds to more realistic values while allowing resolved and
parameterized waves to continue to propagate.

The fixed or idealized QBO winds (first 3 options) can be applied for
any calendar period. The observed input (Giorgetta climatology) can be
used only for the model years 1953-2004. The winds in the final option
were determined from the Giorgetta climatology for 1954-2004 via
filtered spectral decomposition of that climatology. This gives a set of
Fourier coefficients that can be expanded for any day and year. The
expanded wind fields match the climatology during the years 1954-2004.

Radiation
~~~~~~~~~

The radiation parameterizations in CAM4 are quite accurate up to
:math:`\sim 65` km, but deteriorate rapidly above that altitude. Because
65 km is near a local minimum in both shortwave heating and longwave
cooling, it is a particularly convenient height to merge the heating
rates from parameterizations for the lower and upper atmosphere.
Therefore, we retain the CAM4 parameterizations below :math:`\sim 65` km
and use new parameterizations above.

The merged shortwave and longwave radiative heatings are determined from

.. math:: Q = w_1 \, Q_{CAM3} + w_2 \, Q_{MLT},   
	  :label: eq:rad_heat

where :math:`w_1(z^*<z_b^*) = 1`, :math:`w_2(z^*>z_t^*) = 1` and
:math:`z^* =
\log(10^5/p)` is the pressure scale height. The CAM4 radiation
parameterizations are used below :math:`z_b^*` and the MLT
parameterizations are used above :math:`z_t^*`. For :math:`z_b^* < z <
z_t^*`, :math:`w_2 = 1 - w_1` and

.. math:: w_1 = 1 - \tanh\left( \frac{z^* - z_b^*}{z_w*}\right),
	  :label: eq:rad_wght

where :math:`z_w*` is the transition width.

The merging was developed and tested separately for shortwave and
longwave radiation and the constants are slightly different. For
longwave radiation, the constants are :math:`z_b^*=8.57`,
:math:`z_t^*=10` and :math:`z_w^*=0.71`. For shortwave radiation, the
constants are :math:`z_b^*=9`, :math:`z_t^*=10` and :math:`z_w^*=0.75`.
These constants give smooth heating profiles. Note that a typical
atmospheric scale height of :math:`H=7` km places the transition zones
between 60 and 70 km.

Longwave radiation
^^^^^^^^^^^^^^^^^^

|waccm| retains the longwave (LW) formulation used in CAM4 (**???**). However,
in the MLT longwave radiation uses the parameterization of (**???**) for
:math:`\rm CO_2` and :math:`\rm O_3` cooling and the parameterization of
(**???**) for :math:`\rm NO` cooling at 5.3 :math:`\mu`\ m. As noted
above, the LW heating/cooling rates produced by these parameterizations
are merged smoothly at 65 km with those produced by the standard CAM4 LW
code, as recently revised by (**???**). In the interactive chemistry
case all of the gases (O, :math:`\rm O_2`, :math:`\rm O_3`,
:math:`\rm N_2`, NO, and :math:`\rm CO_2`) that are required by these
parameterizations, are predicted within |waccm|.

Shortwave radiation
^^^^^^^^^^^^^^^^^^^

|waccm| uses a combination of solar parameterizations to specify spectral
irradiances over two spectral intervals. The first spectral interval
covers soft x-ray and extreme ultraviolet irradiances (wavelengths
between 0.05 nm to Lyman-\ :math:`\alpha` (121.6 nm)) and is calculated
using the parameterization of (**???**). The parameterizations take as
input the 10.7 cm solar radio flux (:math:`f10.7`) and its 81-day
average (:math:`f10.7a`). Daily values of :math:`f10.7` are obtained
from NOAA’s Space Environment Center (www.sec.noaa.gov).

The irradiance of the :math:`j`\ th spectral interval is:

.. math::

   F_j = F_j^0 * \left\{ 1 + R_j*\left[\frac{(f10.7 + f10.7a)}{2}-F_{min}\right] 
    \right\}

where :math:`F_{min}` = 80. :math:`F_j^0` and :math:`R_j` are taken from
Table A1 of (**???**).

Fluxes for the second interval between Lyman-\ :math:`\alpha` (121.6 nm)
and 100 :math:`\mu`\ m. are specified using an empirical model of the
wavelength-dependent sunspot and facular influences (**???**; Wang,
Lean, and Sheeley 2005). Spectral resolution is 1 nm between 121.6 nm
and 750nm, 5 nm between 750nm and 5\ :math:`\mu`\ m, 10 nm between
5\ :math:`\mu`\ m and 10\ :math:`\mu`\ m, and 50 nm between
10\ :math:`\mu`\ m and 100 :math:`\mu`\ m.

In the troposphere, stratosphere and lower mesosphere (z :math:`<` 65km)
|waccm| retains the CAM4 shortwave heating (200 nm to 4.55 :math:`\mu`\ m)
which is calculated from the net shortwave spectral flux into each layer
(**???**). The solar spectrum for the CAM4 heating calculation is
divided into 19 intervals (**???**). The heating in these intervals must
be adjusted to match the irradiances calculated for the upper part of
the model, and those used in the photolysis calculations. This is
achieved by applying a scaling (:math:`S_j`) to the solar heating in the
:math:`j`\ th CAM4 spectral interval using the spectrum from (**???**)
and Wang, Lean, and Sheeley (2005):

.. math:: S_j = \frac{F_{j}}{F_{j}^{ref}},

where :math:`F_j` is the spectral irradiance (W/m:math:`^2`/nm)
integrated over the :math:`j`\ th band, and :math:`F_{j}^{ref}` is the
same integral taken over a reference spectrum calculated from annual
mean fluxes over a 3-solar-cycle period from XX to YY.

In the MLT region, shortwave heating is the sum of the heating due to
absorption of photons and subsequent exothermic chemical reactions that
are initiated by photolysis. The majority of energy deposited by an
absorbed photon goes into breaking molecular bonds, rather than into
translational energy of the absorbing molecule (heat). Chemical heating
results when constituents react to form products of lower total chemical
potential energy. This heating can take place months after the original
photon absorption and thousands of kilometers away. Heating rates range
from 1 K/day near 75 km to 100-300 K/day near the top of the model
domain. It is clear that quenching of :math:`O(^1D)` is a large source
of heating throughout the MLT.  Above 100 km ion reactions and reactions
involving atomic nitrogen are significant sources of heat, while below
that level O\ :math:`_X` (= O + O\ :math:`_3`) and HO\ :math:`_X` (= H +
OH + HO\ :math:`_2`) reactions are the dominant producers of chemical
heating.

Heating within the MLT from the absorption of radiation that *is*
directly thermalized is calculated over the wavelength range of 0.05 nm
to 350 nm. For wavelengths less than Lyman-\ :math:`\alpha`, it is
assumed that 5% of the energy of each absorbed photon is directly
thermalized:

.. math::

   Q_{EUV} = (\rho c_p)^{-1} \sum_{k} n_k \sum_{j} 
               \epsilon J_{k}(\lambda_j) \frac{hc}{\lambda_j},

where :math:`\epsilon` = 0.05. Here :math:`\rho` is mass density,
:math:`c_p` is the specific heat of dry air, :math:`n` is the number
density of the absorbing species, and :math:`J` is the
photolysis/photoionization rate. The total heating is the sum of
:math:`k` photolysis reactions and :math:`j` wavelengths intervals. At
these wavelengths absorption of a photon typically leads to
photoionization, with the resulting photoelectron having sufficient
energy to ionize further molecules. Calculation of :math:`J_{ij}` and
ionization rates from photoelectrons is calculated based on the
parameterization of (**???**). In a similar manner, the heating rate
within the aurora (:math:`Q_{AUR}`) is calculated as the product of the
total ionization rate, 35 eV per ion pair, and the same heating
efficiency of 5%.

Between Lyman-\ :math:`\alpha` and 350 nm the energy required to break
molecular bonds is explicitly accounted for. The heating rate is thus
defined as:

.. math::

   Q_{UV} = (\rho c_p)^{-1} \sum_{k} n_k \sum_{j} 
               J_{k}(\lambda_j) \{ \frac{hc}{\lambda_j} -BDE_k \},

where :math:`BDE` is the bond dissociation energy.

In addition to these sources of heat, |waccm| calculates heating by absorption
in the near-infrared by CO\ :math:`_2` (between 1.05 to 4.3
:math:`\mu`\ m), which has its largest contribution near 70km and can
exceed 1 K/day (**???**). Heating from this process is calculated using
the parameterization of (**???**). Finally, the heating produced by
collisions of electrons and neutrals (Joule heating) is also calculated
using the predicted ion and electron concentrations. This is described
in section [ion:sub:`d`\ rag]. Local heating rates from joule heating
can be very large in the auroral regions, reaching over
10\ :math:`^3`\ K/day in the upper levels of the model.

Airglow, radiation produced when excited atoms or molecules
spontaneously emit, is accounted for in |waccm| for emissions of
O\ :math:`_2(^1\Delta )`, O\ :math:`_2(^1\Sigma )`, and vibrationally
excited OH. Airglow from the excited molecular oxygen species are
handled explicitly; radiative lifetimes for O\ :math:`_2(^1\Delta )` and
O\ :math:`_2(^1\Sigma )` are 2.58\ :math:`\times`\ 10\ :math:`^{-4}`
s\ :math:`^{-1}` and 0.085 s\ :math:`^{-1}` respectively. However,
modeling of the many possible vibrational transitions of OH is
impractical in a model as large as |waccm|. Energy losses from the emission of
vibrationally excited OH are therefore accounted for by applying an
efficiency factor to the exothermicity of the reaction that produces
vibrationally excited OH; the reaction of hydrogen and ozone. In other
words, the reaction H + O\ :math:`_3` produces ground state OH only, but
the chemical heating from the reaction has been reduced to take into
consideration that some of the chemical potential energy has been lost
in airglow. This approach is the same one used by (**???**) and we use
their recommended efficiency factor of 60%. Any energy lost through
airglow is assumed to be lost to space, and so represents an energy
pathway that does not generate heat.

Volcanic Heating
^^^^^^^^^^^^^^^^

The sulfate aerosol heating is a function of a prescribed aerosol
distribution varying in space and time that has a size distribution
similar to that seen after a volcanic eruption (**???**). The
H\ :math:`_{\rm 2}`\ SO\ :math:`_{\rm 4}` mass distribution is
calculated from the prescribed sulfate surface area density (SAD)
assuming a lognormal size distribution, number of particles per cm-3,
and distribution width (see section 3.6.2). The H2SO4 mass distribution
is then passed to the radiative transfer code (CAMRT), which in turn
calculates heating and cooling rates.

 chemistry
~~~~~~~~~~

Chemical Mechanism (Neutral Species)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 includes a detailed neutral chemistry model for the middle atmosphere
based on the Model for Ozone and Related Chemical Tracers, Version 3
(**???**). The mechanism represents chemical and physical processes in
the troposphere through the lower thermosphere. The species included
within this mechanism are contained within the O\ :math:`_{\rm X}`,
NO\ :math:`_{\rm X}`, HO\ :math:`_{\rm X}`, ClO\ :math:`_{\rm X}`, and
BrO\ :math:`_{\rm X}` chemical families, along with CH\ :math:`_4` and
its degradation products. This mechanism contains 52 neutral species,
one invariant (N:math:`_2`), 127 neutral gas-phase reactions, 48 neutral
photolytic reactions, and 17 heterogeneous reactions on three aerosol
types (see below). Lists of the chemical species are given in Table 1.
The first column lists the symbolic name (as used in the mechanism); the
second column lists the species atomic composition; the third column
designates which numerical solution approach is used (i.e., explicit or
implicit); the fourth column lists any deposition processes (wet or dry)
for that species; and the fifth column indicates whether the surface (or
upper) boundary condition is fixed vmr or flux, or if a species has an
in-situ flux (from lightning or aircraft emissions).

The gas-phase reactions included in the  middle atmosphere chemical
mechanism are listed in Table 2. In most all cases the chemical rate
constants are taken from JPL06-2 (**???**). Exceptions to this condition
are described in the comment section for any given reaction.

Heterogeneous reactions on four different aerosols types are also
represented in the  chemical mechanism (see Table 3): 1) liquid binary
sulfate (LBS); 2) Supercooled ternary solution (STS); 3) Nitric acid
trihydrate (NAT); and 4) water-ice. There are 17 reactions, six
reactions on liquid sulfate aerosols (LBS or STS), five reactions on
solid NAT aerosols, and six reactions on solid water-ice aerosols. The
rate constants for these 17 heterogeneous reactions can be divided up
into two types: 1) first order; and 2) pseudo second order. For first
order hydrolysis reactions (Table 3, reactions 1-3, 7-8, 11, and 12-14),
the heterogeneous rate constant is derived in the following manner:

.. math:: k=\frac{1}{4}V\cdot SAD \cdot \gamma

Where V = mean velocity; SAD = surface area density of LBS, STS, NAT, or
water-ice, and :math:`\gamma` = reaction probability for each reaction.
The units for this rate constant are s\ :math:`^{-1}`. Here the
H\ :math:`_2`\ O abundance is in excess and assumed not change relative
to the other reactant trace constituents. The mean velocity is dependent
on the molecular weight of the non-H\ :math:`_2`\ O reactant (i.e.,
N\ :math:`_2`\ O\ :math:`_5`, ClONO\ :math:`_2`, or BrONO\ :math:`_2`).
The SAD for each aerosol type is described in section 7. The reaction
probability is dependent on both composition and temperature for sulfate
aerosol (see JPL06-2). The reaction probability is a fixed quantity for
NAT and water-ice aerosols and is listed in Table 3. Multiplying the
rate constant times the concentration gives a loss rate in units of
molecules cm\ :math:`^{-3}` sec\ :math:`^{-1}` for the reactants and is
used in the implicit solution approach. The non-hydrolysis reaction
(Table 3, reactions 4-6, 9-10, and 15-17) are second order reactions.
Here, the first order rate constant (equation 6) is divided by the HCl
concentration, giving it the typical bimolecular rate constant unit
value of cm\ :math:`^3` molecule\ :math:`^{-1}` sec\ :math:`^{-1}`. This
approach assumes that all the HCl is in the aerosol particle.

Stratospheric Aerosols
^^^^^^^^^^^^^^^^^^^^^^

Heterogeneous processes on liquid sulfate aerosols and solid polar
stratospheric clouds (Type 1a, 1b, and 2) are included following the
approach of (**???**). This approach assumes that the condensed phase
mass follows a lognormal size distribution taken from (**???**),

.. math::
   :label: sizeqn

   N(r) = \frac{N_0}{r \sigma \sqrt{2\pi}}\exp\left[\frac{-\ln (r / r_0)^2}
   {2 \sigma ^2}\right]
   

where :math:`N` is the aerosol number density (particles
cm\ :math:`^{-3}`); :math:`r` and :math:`r_0` are the particle radius
and median radius respectively; and :math:`\sigma` is the standard
deviation of the lognormal distribution. :math:`N_0` and :math:`r_0` are
supplied for each aerosol type. The aerosol surface area density (SAD)
is the second moment of this distribution.

At model temperatures (T:math:`_{\rm model}`) greater than 200 K, liquid
binary sulfate (LBS) is the only aerosol present. The surface area
density (SAD) for LBS is derived from observations from SAGE, SAGE-II
and SAMS (**???**) as updated by Considine (**???**). As the model
atmosphere cools, the LBS aerosol swells, taking up both HNO\ :math:`_3`
and H\ :math:`_2`\ O to give STS aerosol. The Aerosol Physical Chemistry
Model (ACPM) is used to derive STS composition (**???**). The STS
aerosol median radius and surface area density is derived following the
approach of (**???**). The width of the STS size distribution
(:math:`\sigma=1.6`) and number density (10 particles cm\ :math:`^{-3}`)
are prescribed according to measurements from (**???**). The STS aerosol
median radius can swell from approximately 0.1 :math:`\mu`\ m to
approximately 0.5 :math:`\mu`\ m. There is no aerosol settling assumed
for this type of aerosol. The median radius is used in derivation of
sulfate aerosol reaction probability coefficients. Both the LBS and STS
surface area densities are used for the calculation of the rate
constants as listed in Table 3; reactions (1)-(6).

Solid nitric acid containing aerosol formation is allowed when the model
temperature reaches a prescribed super saturation ratio of
HNO\ :math:`_3` over NAT [Hansen and Mauersberger, 1988]. This ratio is
set to 10 in  (**???**). There are three methods available to handle the
HNO\ :math:`_3` uptake on solid aerosol. The first method directly
follows (**???**; **???**). Here, after the supersaturation ratio
assumption is met, the available condensed phase HNO\ :math:`_3` is
assumed to reside in the solid NAT aerosol. The derivation of the NAT
median radius and surface area density follows the same approach as the
STS aerosol, by assuming: a lognormal size distribution, a width of a
distribution (:math:`\sigma=1.6`; (**???**)), and a number density (0.01
particles cm\ :math:`^{-3}`; (**???**)). The NAT radius settles with a
value of :math:`r_0` ranging between 2 and 5 :math:`\mu`\ m; this value
depends on the model temperature and subsequent amount of condensed
phase HNO\ :math:`_3` formed. This NAT median radius :math:`r_0` is also
used to derive the terminal velocity for settling of NAT (section 8) and
the eventual irreversible denitrification. The NAT surface area density
is used to calculate the rate constants for heterogeneous reactions 7-11
(Table 3). Since the available HNO\ :math:`_3` is included inside the
NAT aerosol, there is no STS aerosol present. However, there are still
heterogeneous reactions occurring on the surface of LBS aerosols.

If the calculated atmospheric temperature, :math:`T`, becomes less than
or equal to the saturation temperature (T:math:`_{sat}`) for water vapor
over ice (e.g., (**???**)), water-ice aerosols can form. In  the
condensed phase H\ :math:`_2`\ O is derived in the prognotic water
routines of CAM and passed into the chemistry module. Using this
condensed phase H\ :math:`_2`\ O, the median radius and the surface area
density for water-ice are again derived following the approach of
(**???**). The water-ice median radius and surface area density assumes
a lognormal size distribution, a width of a distribution = 1.6
(**???**), and a number density of 0.001 particles cm\ :math:`^{-3}`
(**???**). The value of :math:`r_0` is typically 10\ :math:`\mu`\ m. The
water-ice surface area density is used for the calculation of the rate
constants for reactions 12-17 (Table 3).

Sedimentation of Stratospheric Aerosols
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The sedimentation of HNO\ :math:`_3` in stratospheric aerosols follows
the approach described in (**???**). The following equation is used to
derive the flux (:math:`F`) of HNO\ :math:`_3`, as NAT aerosol, across
model levels in units of molecules cm\ :math:`^{-2}` sec\ :math:`^{-1}`.

.. math:: F_i = V_i \cdot C_i \, \exp(8 \ln^2\sigma_i),

where :math:`i = 1` for NAT; :math:`V_i` is the terminal velocity of the
aerosol particles (cm s\ :math:`^{-1}`); :math:`C` is the
condensed-phase concentration of HNO\ :math:`_3` (molecules
cm\ :math:`^{-3}`); :math:`\sigma` is the width of the lognormal size
distribution for NAT (see discussion above). The terminal velocity is
dependent on the given aerosol: 1) mass density; 2) median radius; 3)
shape; 4) dynamic viscosity; and 5) Cunningham correction factor for
spherical particles (see (**???**) and (**???**) for the theory behind
the derivation of terminal velocity). For each aerosol type the terminal
velocity could be calculated, however, in  this quantity is only derived
for NAT. Settling of HNO\ :math:`_3` contain in STS is not derived based
on the assumption that the median radius is too small to cause any
significant denitrification and settling of condensed phase
H\ :math:`_2`\ O is handled in the CAM4 prognostic water routines.

Ion Chemistry
^^^^^^^^^^^^^

 includes a six constituent ion chemistry model (O:math:`^+`,
O\ :math:`_2^+`, N\ :math:`^+`, N\ :math:`_2^+`, NO\ :math:`^+`, and
electrons) that represents the the E-region ionosphere. The global mean
ion and electron distributions simulated by for solar minimum conditions
are shown in Figure [ionfig], which clearly shows that the dominant ions
in this region are NO\ :math:`^+` and O\ :math:`_2^+`. Ion-neutral and
recombination reactions included in  are listed in Table [ionrxntab].
The reaction rate constants for these reactions are taken from
(**???**).

Ionization sources include not only the aforementioned absorption of
extreme ultraviolet and soft x-ray photons, and photoelectron impact,
but also energetic particles precipitation in the auroral regions. The
latter is calculated by a parameterization based on code from the NCAR
TIME-GCM model (**???**) that rapidly calculates ion-pair production
rates, including production in the polar cusp and polar cap. The
parameterization takes as input hemispheric power (HP), the estimated
power in gigawatts deposited in the polar regions by energetic
particles.

Currently  uses a parameterization of HP (in GW) based on an empirical
relationships between HP and the :math:`K_p` planetary geomagnetic
index. For :math:`K_p \leq 7`,  uses the relationship obtained by
(**???**) from TIMED/GUVI observations:

.. math:: {\rm HP} = 16.82*K_p*\exp{(0.32)}-4.86

For :math:`K_p > 7`,  linearly interpolates HP, assuming HP equals to
300 when :math:`K_p` is 9, based on NOAA satellite measurements:

.. math:: {\rm HP} = 153.13 + \frac{K_p - 7}{9-7}*(300 - 153.13)

:math:`K_p` is also available from NOAA’s Space Environment Center and
covers the period from 1933 to the present, making it ideal for
long-term retrospective simulations.

.. figure:: figures/ions.jpg
   :align: center

   Global mean distribution of charged constituents during July
   solar minimum conditions.

   Global mean distribution of charged constituents during July solar
   minimum conditions.

.. figure:: figures/ionprod.jpg
   :align: center

   a) Global distribution of ionization rates at
   7.3\ :math:`\times 10^{-5}` hPa, July 1, UT0100 HRS. Contour interval
   is 2\ :math:`\times 10^{3}` cm\ :math:`^{-3}` s\ :math:`^{-1}`. b)
   Simultaneous global mean ionization rates (cm:math:`^{-3}`
   s\ :math:`^{-1}`) versus pressure.

Total ionization rates at 110km during July for solar maximum conditions
are shown in Figure [qsumfig]a. The broad region of ionization centered
in the tropics is a result of EUV ionization, and has a peak value of
almost 10\ :math:`^3` at 22\ :math:`^\circ`\ N. Ionization rates from
particle precipitation can exceed this rate by 40% but are limited to
the high-latitudes, as can been seen by the two bands that are
approximately aligned around the magnetic poles. The global mean
ionization rate (Figure [qsumfig]b)

An important aspect of including ionization processes (both in the
aurora and by energetic photons and photoelectrons), is that it leads to
a more accurate representation of thermospheric nitric oxide. Not only
does nitric oxide play an important role in the energy balance of the
lower thermosphere through emission at 5.3 :math:`\mu`\ m, it might also
be transported to the upper stratosphere, where it can affect ozone
concentrations. Nitric oxide is produced through quenching of
N\ :math:`(^2D)`:

.. math:: N(^2D) + O_2 \rightarrow NO + O(^1D) + 1.84eV

N\ :math:`(^2D)` is produced either via recombination of NO\ :math:`^+`
(see Table [ionrxntab]) or directly by ionization of molecular nitrogen.
The branching ratio between N\ :math:`(^2D)` and ground-state atomic
nitrogen for the photoionization process is critical in determining the
effectiveness of NO production. If ground-state atomic nitrogen is
produced then it can react with NO to produce molecular nitrogen and
effectively remove to members of the NOx family. In  60% of the atomic
nitrogen produced is in the excited state, which implies absorption of
EUV results in a net source of NO. Also shown are maxima at high
latitudes due to auroral ionization.  reproduces many of the features of
the Nitric Oxide Empirical Model (NOEM) distribution (**???**), which is
based on data from the Student Nitric Oxide Explorer satellite (**???**)
In particular, larger NO in the winter hemisphere (a result of less
photolytic loss), and a more localized NO maximum in the Northern
Hemisphere (related to the lesser offset of geographic and magnetic
poles, and so less spread when viewed as a geographic zonal mean).

****

+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| no.   | Symbolic Name   | Chemical Formula                 | Numerics    | Deposition   | Boundary Condition   |
+=======+=================+==================================+=============+==============+======================+
| 1     | O               | O(\ :math:`^3`\ P)               | Implicit    |              | ubvmr                |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 2     | O1D             | O(\ :math:`^1`\ D)               | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 3     | O3              | O\ :math:`_3`                    | Implicit    | dry          |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 4     | O2              | O\ :math:`_2`                    | Implicit    |              | ubvmr                |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 5     | O2\_1S          | O\ :math:`_2(^1\Sigma)`          | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 6     | O2\_1D          | O\ :math:`_2(^1\Delta)`          | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 7     | H               | H                                | Implicit    |              | ubvmr                |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 8     | OH              | OH                               | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 9     | HO2             | HO\ :math:`_2`                   | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 10    | H2              | H\ :math:`_2`                    | Implicit    |              | vmr, ubvmr           |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 11    | H2O2            | H\ :math:`_2`\ O\ :math:`_2`     | Implicit    | dry, wet     |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 12    | N               | N                                | Implicit    |              | ubvmr                |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 13    | N2D             | N(\ :math:`^2`\ D)               | Implicit    |              | from TIME-GCM        |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 14    | N2              | N\ :math:`_2`                    | Invariant   |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 15    | NO              | NO                               | Implicit    |              | flux, ubvmr,         |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
|       |                 |                                  |             |              | lflux, airflux       |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 16    | NO2             | NO\ :math:`_2`                   | Implicit    | dry          |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 17    | NO3             | NO\ :math:`_3`                   | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 18    | N2O5            | N\ :math:`_2`\ O\ :math:`_5`     | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 19    | HNO3            | HNO\ :math:`_3`                  | Implicit    | dry, wet     |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 20    | HO2NO2          | HO\ :math:`_2`\ NO\ :math:`_2`   | Implicit    | dry, wet     |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 21    | CL              | Cl                               | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 22    | CLO             | ClO                              | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 23    | CL2             | Cl\ :math:`_2`                   | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 24    | OCLO            | OClO                             | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 25    | CL2O2           | Cl\ :math:`_2`\ O\ :math:`_2`    | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 26    | HCL             | HCl                              | Implicit    | wet          |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 27    | HOCL            | HOCl                             | Implicit    | wet          |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 28    | ClONO2          | ClONO\ :math:`_2`                | Implicit    | wet          |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 29    | BR              | Br                               | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 30    | BRO             | BrO                              | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 31    | HOBR            | HOBr                             | Implicit    | wet          |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 32    | HBR             | HBr                              | Implicit    | wet          |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 33    | BrONO 2         | BrONO\ :math:`_2`                | Implicit    | wet          |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+
| 34    | BRCL            | BrCl                             | Implicit    |              |                      |
+-------+-----------------+----------------------------------+-------------+--------------+----------------------+

Table:  Neutral Chemical Species (51 computed species + N\ :math:`_2`)

[mozart1a]

****

+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| no.                                                                                           | Symbolic Name   | Chemical Formula                              | Numerics   | Deposition   | Boundary Condition     |
+===============================================================================================+=================+===============================================+============+==============+========================+
| 35                                                                                            | CH4             | CH\ :math:`_4`                                | Implicit   |              | vmr, airflux           |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 36                                                                                            | CH3O2           | CH\ :math:`_3`\ O\ :math:`_2`                 | Implicit   |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 37                                                                                            | CH3OOH          | CH\ :math:`_3`\ OOH                           | Implicit   | dry, wet     |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 38                                                                                            | CH2O            | CH\ :math:`_2`\ O                             | Implicit   | dry, wet     | flux                   |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 39                                                                                            | CO              | CO                                            | Explicit   | dry          | flux, ubvmr, airflux   |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 40                                                                                            | CH3CL           | CH\ :math:`_3`\ Cl                            | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 41                                                                                            | CH3BR           | CH\ :math:`_3`\ Br                            | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 42                                                                                            | CFC11           | CFCl\ :math:`_3`                              | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 43                                                                                            | CFC12           | CF\ :math:`_2`\ Cl\ :math:`_2`                | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 44                                                                                            | CFC113          | CCl\ :math:`_2`\ FCClF\ :math:`_2`            | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 45                                                                                            | HCFC22          | CHClF\ :math:`_2`                             | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 46                                                                                            | CCL4            | CCl\ :math:`_4`                               | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 47                                                                                            | CH3CCL3         | CH\ :math:`_3`\ CCl\ :math:`_3`               | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 48                                                                                            | CF2CLBR         | CBr\ :math:`_2`\ F\ :math:`_2` (Halon-1211)   | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 49                                                                                            | CF3BR           | CBrF\ :math:`_3` (Halon-1301)                 | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 50                                                                                            | H2O             | H\ :math:`_2`\ O                              | Explicit   |              | flux                   |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 51                                                                                            | N2O             | N\ :math:`_2`\ O                              | Explicit   |              | vmr                    |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| 52                                                                                            | CO2             | CO\ :math:`_2`                                | Explicit   |              | vmr, ubvmr             |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|                                                                                               |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| **Deposition:**                                                                               |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|  wet = wet deposition included                                                                |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|  dry = surface dry deposition included                                                        |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| If there is no designation in the deposition column, this species is not operated on by wet   |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|  or dry deposition algorthims.                                                                |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|                                                                                               |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| **Boundary Condition:**                                                                       |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|  flux = flux lower boundary conditions                                                        |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|  vmr = fixed volume mixing ratio (vmr) lower boundary condition                               |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|  ubvmr = fixed vmr upper boundary condition                                                   |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|  lflux = lightning emission included for this species                                         |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|  airflux= aircraft emissions included for this species                                        |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
| If there is no designation in the Boundary Conditions column, this species has a zero flux    |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+
|  boundary condition for the top and bottom of the model domain.                               |                 |                                               |            |              |                        |
+-----------------------------------------------------------------------------------------------+-----------------+-----------------------------------------------+------------+--------------+------------------------+

Table: (continued)  Neutral Chemical Species (51 computed species +
N\ :math:`_2`)

[mozart1b]

****

+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| no.   | Reactions                                                                                                                   | Comments                              |
+=======+=============================================================================================================================+=======================================+
|       | Oxygen Reactions                                                                                                            |                                       |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 1     | O + O\ :math:`_2` + M :math:`\rightarrow` O\ :math:`_3` + M                                                                 | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 2     | O + O\ :math:`_3` :math:`\rightarrow` 2 O\ :math:`_2`                                                                       | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 3     | O + O + M :math:`\rightarrow` O\ :math:`_2` + M                                                                             | Smith and Robertson (2008)            |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 4     | O\ :math:`_2`\ (:math:`^1\Sigma`) + O :math:`\rightarrow` O\ :math:`_2`\ (:math:`^1\Delta`) + O                             | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 5     | O\ :math:`_2` 1S + O\ :math:`_2` :math:`\rightarrow` O\ :math:`_2`\ (:math:`^1\Delta`) + O\ :math:`_2`                      | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 6     | O\ :math:`_2`\ (:math:`^1\Sigma`) + N\ :math:`_2` :math:`\rightarrow` O\ :math:`_2`\ (:math:`^1\Delta`) + N\ :math:`_2`     | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 7     | O\ :math:`_2`\ (:math:`^1\Sigma`) + O\ :math:`_3` :math:`\rightarrow` O\ :math:`_2`\ (:math:`^1\Delta`) + O\ :math:`_3`     | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 8     | O\ :math:`_2`\ (:math:`^1\Sigma`) + CO\ :math:`_2` :math:`\rightarrow` O\ :math:`_2`\ (:math:`^1\Delta`) + CO\ :math:`_2`   | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 9     | O\ :math:`_2`\ (:math:`^1\Sigma`) :math:`\rightarrow` O\ :math:`_2`                                                         | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 10    | O\ :math:`_2`\ (:math:`^1\Delta`) + O :math:`\rightarrow` O\ :math:`_2` + O                                                 | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 11    | O\ :math:`_2`\ (:math:`^1\Delta`) + O\ :math:`_2` :math:`\rightarrow` 2 O\ :math:`_2`                                       | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 12    | O\ :math:`_2`\ (:math:`^1\Delta`) + N\ :math:`_2` :math:`\rightarrow` O\ :math:`_2` + N\ :math:`_2`                         | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 13    | O\ :math:`_2`\ (:math:`^1\Delta`) :math:`\rightarrow` O\ :math:`_2`                                                         | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 14    | O(\ :math:`^1`\ D) + N\ :math:`_2` :math:`\rightarrow` O + N\ :math:`_2`                                                    | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 15    | O(\ :math:`^1`\ D)+ O\ :math:`_2` :math:`\rightarrow` O + O\ :math:`_2`\ (:math:`^1\Sigma`)                                 | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 16    | O(\ :math:`^1`\ D)+ O\ :math:`_2` :math:`\rightarrow` O + O\ :math:`_2`                                                     | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 17    | O(\ :math:`^1`\ D)+ H\ :math:`_2`\ O :math:`\rightarrow` 2 OH                                                               | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 18    | O(\ :math:`^1`\ D) + N\ :math:`_2`\ O :math:`\rightarrow` 2 NO                                                              | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 19    | O(\ :math:`^1`\ D) + N\ :math:`_2`\ O :math:`\rightarrow` N\ :math:`_2` + O\ :math:`_2`                                     | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 20    | O(\ :math:`^1`\ D) + O\ :math:`_3` :math:`\rightarrow` 2 O\ :math:`_2`                                                      | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 21    | O(\ :math:`^1`\ D) + CFC11 :math:`\rightarrow` 3 Cl                                                                         | JPL-06; Bloomfield (1994)             |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
|       |                                                                                                                             | for quenching of O(\ :math:`^1`\ D)   |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 22    | O(\ :math:`^1`\ D) + CFC12 :math:`\rightarrow` 2 Cl                                                                         | JPL-06; Bloomfield (1994)             |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 23    | O(\ :math:`^1`\ D) + CFC113 :math:`\rightarrow` 3 Cl                                                                        | JPL-06; Bloomfield (1994)             |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 24    | O(\ :math:`^1`\ D) + HCFC22 :math:`\rightarrow` Cl                                                                          | JPL-06; Bloomfield (1994)             |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 25    | O(\ :math:`^1`\ D) + CCl\ :math:`_4` :math:`\rightarrow` 4 Cl                                                               | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 26    | O(\ :math:`^1`\ D) + CH\ :math:`_3`\ Br :math:`\rightarrow` Br                                                              | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 27    | O(\ :math:`^1`\ D) + CF\ :math:`_2`\ ClBr :math:`\rightarrow` Cl + Br                                                       | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 28    | O(\ :math:`^1`\ D) + CF\ :math:`_3`\ Br :math:`\rightarrow` Br                                                              | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 29    | O(\ :math:`^1`\ D) + CH\ :math:`_4` :math:`\rightarrow` CH\ :math:`_3`\ O\ :math:`_2` + OH                                  | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 30    | O(\ :math:`^1`\ D) + CH\ :math:`_4` :math:`\rightarrow` CH\ :math:`_2`\ O + H + HO\ :math:`_2`                              | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 31    | O(\ :math:`^1`\ D) + CH\ :math:`_4` :math:`\rightarrow` CH\ :math:`_2`\ O + H\ :math:`_2`                                   | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 32    | O(\ :math:`^1`\ D) + H\ :math:`_2` :math:`\rightarrow` H + OH                                                               | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 33    | O(\ :math:`^1`\ D) + HCl :math:`\rightarrow` Cl + OH                                                                        | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+
| 34    | O(\ :math:`^1`\ D) + HBr :math:`\rightarrow` Br + OH                                                                        | JPL-06                                |
+-------+-----------------------------------------------------------------------------------------------------------------------------+---------------------------------------+

Table:  Gas-phase Reactions.

****

+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| no.   | Reactions                                                                                                   | Comments                                              |
+=======+=============================================================================================================+=======================================================+
|       | Nitrogen Radicals                                                                                           |                                                       |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 35    | N(\ :math:`^2`\ D) + O\ :math:`_2` :math:`\rightarrow` NO + O(\ :math:`^1`\ D)                              | :math:`\qquad \qquad` JPL-06 :math:`\qquad \qquad`    |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 36    | N(\ :math:`^2`\ D) + O :math:`\rightarrow` N + O                                                            | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 37    | N + O\ :math:`_2` :math:`\rightarrow` NO + O                                                                | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 38    | N + NO :math:`\rightarrow` N\ :math:`_2` + O                                                                | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 39    | N + NO\ :math:`_2` :math:`\rightarrow` N\ :math:`_2`\ O + O                                                 | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 40    | NO + O + M :math:`\rightarrow` NO\ :math:`_2` + M                                                           | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 41    | NO + HO\ :math:`_2` :math:`\rightarrow` NO\ :math:`_2` + OH                                                 | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 42    | NO + O\ :math:`_3` :math:`\rightarrow` NO\ :math:`_2` + O\ :math:`_2`                                       | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 43    | NO\ :math:`_2` + O :math:`\rightarrow` NO + O\ :math:`_2`                                                   | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 44    | NO\ :math:`_2` + O + M :math:`\rightarrow` NO\ :math:`_3` + M                                               | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 45    | NO\ :math:`_2` + O\ :math:`_3` :math:`\rightarrow` NO\ :math:`_3` + O\ :math:`_2`                           | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 46    | NO\ :math:`_2` + NO\ :math:`_3` + M :math:`\rightarrow` N\ :math:`_2`\ O5 + M                               | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 47    | N\ :math:`_2`\ O\ :math:`_5` + M :math:`\rightarrow` NO\ :math:`_2` + NO\ :math:`_3` + M                    | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 48    | NO\ :math:`_2` + OH + M :math:`\rightarrow` HNO\ :math:`_3` + M                                             | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 49    | HNO\ :math:`_3` + OH :math:`\rightarrow` NO\ :math:`_3` + H\ :math:`_2`\ O                                  | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 50    | NO\ :math:`_2` + HO\ :math:`_2` + M :math:`\rightarrow` HO\ :math:`_2`\ NO\ :math:`_2` + M                  | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 51    | NO\ :math:`_3` + NO :math:`\rightarrow` 2 NO\ :math:`_2`                                                    | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 52    | NO\ :math:`_3` + O :math:`\rightarrow` NO\ :math:`_2` + O\ :math:`_2`                                       | :math:`\qquad \qquad` JPL-06 :math:`\qquad \qquad`    |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 53    | NO\ :math:`_3` + OH :math:`\rightarrow` NO\ :math:`_2` + HO\ :math:`_2`                                     | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 54    | NO\ :math:`_3` + HO\ :math:`_2` :math:`\rightarrow` NO\ :math:`_2` + OH + O\ :math:`_2`                     | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 55    | HO\ :math:`_2`\ NO\ :math:`_2` + OH :math:`\rightarrow` NO\ :math:`_2` + H\ :math:`_2`\ O + O\ :math:`_2`   | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 56    | HO\ :math:`_2`\ NO\ :math:`_2` + M :math:`\rightarrow` HO\ :math:`_2` + NO\ :math:`_2` + M                  | JPL-06                                                |
+-------+-------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+

Table: (continued)  Gas-phase Reactions.

****

+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| no.   | Reactions                                                                                          | Comments                                              |
+=======+====================================================================================================+=======================================================+
|       | Hydrogen Radicals                                                                                  |                                                       |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 57    | H + O\ :math:`_2` + M :math:`\rightarrow` HO\ :math:`_2` + M                                       | :math:`\qquad \qquad` JPL-06 :math:`\qquad \qquad`    |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 58    | H + O\ :math:`_3` + M :math:`\rightarrow` OH + O\ :math:`_2`                                       | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 59    | H + HO\ :math:`_2` :math:`\rightarrow` 2 OH                                                        | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 60    | H + HO\ :math:`_2` :math:`\rightarrow` H\ :math:`_2` + O\ :math:`_2`                               | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 61    | H + HO\ :math:`_2` :math:`\rightarrow` H\ :math:`_2`\ O + O                                        | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 62    | OH + O :math:`\rightarrow` H + O\ :math:`_2`                                                       | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 63    | OH + O\ :math:`_3` :math:`\rightarrow` HO\ :math:`_2` + O\ :math:`_2`                              | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 64    | OH + HO\ :math:`_2` :math:`\rightarrow` H\ :math:`_2`\ O + O\ :math:`_2`                           | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 65    | OH + OH :math:`\rightarrow` H\ :math:`_2`\ O + O                                                   | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 66    | OH + OH + M :math:`\rightarrow` H\ :math:`_2`\ O\ :math:`_2` + M                                   | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 67    | OH + H\ :math:`_2` :math:`\rightarrow` H\ :math:`_2`\ O + H                                        | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 68    | OH + H\ :math:`_2`\ O\ :math:`_2` :math:`\rightarrow` H\ :math:`_2`\ O + HO\ :math:`_2`            | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 69    | HO\ :math:`_2` + O :math:`\rightarrow` OH + O\ :math:`_2`                                          | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 70    | HO\ :math:`_2` + O\ :math:`_3` :math:`\rightarrow` OH + 2O\ :math:`_2`                             | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 71    | HO\ :math:`_2` + HO\ :math:`_2` :math:`\rightarrow` H\ :math:`_2`\ O\ :math:`_2` + O\ :math:`_2`   | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 72    | H\ :math:`_2`\ O\ :math:`_2` + O :math:`\rightarrow` OH + HO\ :math:`_2`                           | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
|       | Chlorine Radicals                                                                                  |                                                       |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 73    | Cl + O\ :math:`_3` :math:`\rightarrow` ClO + O\ :math:`_2`                                         | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 74    | Cl + H\ :math:`_2` :math:`\rightarrow` HCl + H                                                     | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 75    | Cl + H\ :math:`_2`\ O\ :math:`_2` :math:`\rightarrow` HCl + HO\ :math:`_2`                         | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 76    | Cl + HO\ :math:`_2` :math:`\rightarrow` HCl + O\ :math:`_2`                                        | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 77    | Cl + HO\ :math:`_2` :math:`\rightarrow` ClO + OH                                                   | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 78    | Cl + CH\ :math:`_2`\ O :math:`\rightarrow` HCl + HO\ :math:`_2` + CO                               | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 79    | Cl + CH\ :math:`_4` :math:`\rightarrow` CH\ :math:`_3`\ O\ :math:`_2` + HCl                        | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 80    | ClO + O :math:`\rightarrow` Cl + O\ :math:`_2`                                                     | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 81    | ClO + OH :math:`\rightarrow` Cl + HO\ :math:`_2`                                                   | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 82    | ClO + OH :math:`\rightarrow` HCl + O\ :math:`_2`                                                   | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 83    | ClO + HO\ :math:`_2` :math:`\rightarrow` HOCl + O\ :math:`_2`                                      | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 84    | ClO + NO :math:`\rightarrow` NO\ :math:`_2` + Cl                                                   | :math:`\qquad \qquad` JPL-06 :math:`\qquad \qquad`    |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 85    | ClO + NO\ :math:`_2` + M :math:`\rightarrow` ClONO\ :math:`_2` + M                                 | JPL-06                                                |
+-------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------+

Table: (continued)  Gas-phase Reactions.

****

+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| no.   | Reactions                                                                    | Comments                                              |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
|       | Chlorine Radicals Continued                                                  |                                                       |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 86    | ClO + ClO :math:`\rightarrow` 2 Cl + O\ :math:`_2`                           | :math:`\qquad \qquad` JPL-06 :math:`\qquad \qquad`    |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 87    | ClO + ClO :math:`\rightarrow` Cl2 + O\ :math:`_2`                            | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 88    | ClO + ClO :math:`\rightarrow` Cl + OClO                                      | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 89    | ClO + ClO + M :math:`\rightarrow` Cl\ :math:`_2`\ O\ :math:`_2` + M          | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 90    | Cl\ :math:`_2`\ O\ :math:`_2` + M :math:`\rightarrow` 2 ClO + M              | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 91    | HCl + OH :math:`\rightarrow` H\ :math:`_2`\ O + Cl                           | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 92    | HCl + O :math:`\rightarrow` Cl + OH                                          | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 93    | HOCl + O :math:`\rightarrow` ClO + OH                                        | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 94    | HOCl + Cl :math:`\rightarrow` HCl + ClO                                      | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 95    | HOCl + OH :math:`\rightarrow` ClO + H\ :math:`_2`\ O                         | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 96    | ClONO\ :math:`_2` + O :math:`\rightarrow` ClO + NO\ :math:`_3`               | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 97    | ClONO\ :math:`_2` + OH :math:`\rightarrow` HOCl + NO\ :math:`_3`             | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 98    | ClONO\ :math:`_2` + Cl :math:`\rightarrow` Cl\ :math:`_2` + NO\ :math:`_3`   | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| no.   | Reactions                                                                    | Comments                                              |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
|       | Bromine Radicals                                                             |                                                       |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 99    | Br + O\ :math:`_3` :math:`\rightarrow` BrO + O\ :math:`_2`                   | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 100   | Br + HO\ :math:`_2` :math:`\rightarrow` HBr + O\ :math:`_2`                  | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 101   | Br + CH\ :math:`_2`\ O :math:`\rightarrow` HBr + HO\ :math:`_2` + CO         | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 102   | BrO + O :math:`\rightarrow` Br + O\ :math:`_2`                               | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 103   | BrO + OH :math:`\rightarrow` Br + HO\ :math:`_2`                             | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 104   | BrO + HO\ :math:`_2` :math:`\rightarrow` HOBr + O\ :math:`_2`                | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 105   | BrO + NO :math:`\rightarrow` Br + NO\ :math:`_2`                             | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 106   | BrO + NO\ :math:`_2` + M :math:`\rightarrow` BrONO\ :math:`_2` + M           | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 107   | BrO + ClO :math:`\rightarrow` Br + OClO                                      | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 108   | BrO + ClO :math:`\rightarrow` Br + Cl + O\ :math:`_2`                        | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 109   | BrO + ClO :math:`\rightarrow` BrCl + O\ :math:`_2`                           | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 110   | BrO + BrO :math:`\rightarrow` 2 Br + O\ :math:`_2`                           | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 111   | HBr + OH :math:`\rightarrow` Br + H\ :math:`_2`\ O                           | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 112   | HBr + O :math:`\rightarrow` Br + OH                                          | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 113   | HOBr + O :math:`\rightarrow` BrO + OH                                        | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+
| 114   | BrONO\ :math:`_2` + O :math:`\rightarrow` BrO + NO\ :math:`_3`               | JPL-06                                                |
+-------+------------------------------------------------------------------------------+-------------------------------------------------------+

Table: (continued)  Gas-phase Reactions.

****

+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| no.   | Reactions                                                                                                                            | Comments                                              |
+=======+======================================================================================================================================+=======================================================+
|       | Halogen Radicals                                                                                                                     |                                                       |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 115   | CH\ :math:`_3`\ Cl + Cl :math:`\rightarrow` HO\ :math:`_2` + CO + 2HCl                                                               | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 116   | CH\ :math:`_3`\ Cl + OH :math:`\rightarrow` Cl + H\ :math:`_2`\ O + HO\ :math:`_2`                                                   | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 117   | CH\ :math:`_3`\ CCl\ :math:`_3` + OH :math:`\rightarrow` 3 Cl + H\ :math:`_2`\ O                                                     | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 118   | HCFC22 + OH :math:`\rightarrow` Cl + H\ :math:`_2`\ O + HO\ :math:`_2`                                                               | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 119   | CH\ :math:`_3`\ Br + OH :math:`\rightarrow` Br + H\ :math:`_2`\ O + HO\ :math:`_2`                                                   | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
|       | CH\ :math:`_4` and Derivatives                                                                                                       |                                                       |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 120   | CH\ :math:`_4` + OH :math:`\rightarrow` CH\ :math:`_3`\ O\ :math:`_2` + H\ :math:`_2`\ O                                             | :math:`\qquad \qquad` JPL-06 :math:`\qquad \qquad`    |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 121   | CH\ :math:`_3`\ O\ :math:`_2` + NO :math:`\rightarrow` CH\ :math:`_2`\ O + NO\ :math:`_2` + HO\ :math:`_2`                           | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 122   | CH\ :math:`_3`\ O\ :math:`_2` + HO\ :math:`_2` :math:`\rightarrow` CH\ :math:`_3`\ OOH + O\ :math:`_2`                               | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 123   | CH\ :math:`_3`\ OOH + OH :math:`\rightarrow` 0.7 CH\ :math:`_3`\ O\ :math:`_2` + 0.3 OH + 0.3 CH\ :math:`_2`\ O + H\ :math:`_2`\ O   | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 124   | CH\ :math:`_2`\ O + NO\ :math:`_3` :math:`\rightarrow` CO + HO\ :math:`_2` + HNO\ :math:`_3`                                         | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 125   | CH\ :math:`_2`\ O + OH :math:`\rightarrow` CO + H\ :math:`_2`\ O + H                                                                 | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 126   | CH\ :math:`_2`\ O + O :math:`\rightarrow` OH + HO\ :math:`_2` + CO                                                                   | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+
| 127   | CO + OH :math:`\rightarrow` H + CO\ :math:`_2`                                                                                       | JPL-06                                                |
+-------+--------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------+

Table: (continued)  Gas-phase Reactions.

****

+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| no.   | Reaction                                                                                | Comments                                           |
+=======+=========================================================================================+====================================================+
|       | Sulfate Aerosol                                                                         |                                                    |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 1     | N\ :math:`_2`\ O\ :math:`_5` + H\ :math:`_2`\ O :math:`\rightarrow` 2 HNO\ :math:`_3`   | JPL-06; f (sulfuric acid wt %)                     |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 2     | ClONO\ :math:`_2` + H\ :math:`_2`\ O :math:`\rightarrow` HOCl + HNO\ :math:`_3`         | JPL-06; f (T, P, HCl, H\ :math:`_2`\ O, r)         |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 3     | BrONO\ :math:`_2` + H\ :math:`_2`\ O :math:`\rightarrow` HOBr + HNO\ :math:`_3`         | JPL-06; f (T, P, H\ :math:`_2`\ O, r)              |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 4     | ClONO\ :math:`_2` + HCl :math:`\rightarrow` Cl\ :math:`_2` + HNO\ :math:`_3`            | JPL-06; f (T, P, HCl, H\ :math:`_2`\ O, r)         |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 5     | HOCl + HCl :math:`\rightarrow` Cl\ :math:`_2` + H\ :math:`_2`\ O                        | JPL-06; f (T, P, HCl, HCl, H\ :math:`_2`\ O, r)    |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 6     | HOBr + HCl :math:`\rightarrow` BrCl + H\ :math:`_2`\ O                                  | JPL-06; f (T, P, HCl, HOBr, H\ :math:`_2`\ O, r)   |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
|       | NAT Aerosol                                                                             |                                                    |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 7     | N\ :math:`_2`\ O\ :math:`_5` + H\ :math:`_2`\ O :math:`\rightarrow` 2 HNO\ :math:`_3`   | JPL-06; :math:`\gamma = 4 \times 10^{-4}`          |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 8     | ClONO\ :math:`_2` + H\ :math:`_2`\ O :math:`\rightarrow` HOCl + HNO\ :math:`_3`         | JPL-06; :math:`\gamma = 4 \times 10^{-3}`          |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 9     | ClONO\ :math:`_2` + HCl :math:`\rightarrow` Cl\ :math:`_2` + HNO\ :math:`_3`            | JPL-06; :math:`\gamma = 0.2`                       |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 10    | HCl + HCl :math:`\rightarrow` Cl\ :math:`_2` + H\ :math:`_2`\ O                         | JPL-06; :math:`\gamma = 0.1`                       |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 11    | BrONO\ :math:`_2` + H\ :math:`_2`\ O :math:`\rightarrow` HOBr + HNO\ :math:`_3`         | JPL-06; :math:`\gamma = 0.3`                       |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
|       | Water-Ice Aerosol                                                                       |                                                    |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 12    | N\ :math:`_2`\ O\ :math:`_5` + H\ :math:`_2`\ O :math:`\rightarrow` 2 HNO\ :math:`_3`   | JPL-06; :math:`\gamma = 0.02`                      |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 13    | ClONO\ :math:`_2` + H\ :math:`_2`\ O :math:`\rightarrow` HOCl + HNO\ :math:`_3`         | JPL-06; :math:`\gamma = 0.3`                       |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 14    | BrONO\ :math:`_2` + H\ :math:`_2`\ O :math:`\rightarrow` HOBr + HNO\ :math:`_3`         | JPL-06; :math:`\gamma = 0.3`                       |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 15    | ClONO\ :math:`_2` + HCl :math:`\rightarrow` Cl\ :math:`_2` + HNO\ :math:`_3`            | JPL-06; :math:`\gamma = 0.3`                       |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 16    | HOCl + HCl :math:`\rightarrow` Cl\ :math:`_2` + H\ :math:`_2`\ O                        | JPL-06; :math:`\gamma = 0.2`                       |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+
| 17    | HOBr + HCl :math:`\rightarrow` BrCl + H\ :math:`_2`\ O                                  | JPL-06; :math:`\gamma = 0.3`                       |
+-------+-----------------------------------------------------------------------------------------+----------------------------------------------------+

Table:  Heterogeneous Reactions on liquid and solid aerosols.

****

+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| no.   | Reactants                                         | Products                             | Comments                                                              |
+=======+===================================================+======================================+=======================================================================+
| 1     | O\ :math:`_2` + h\ :math:`\nu`                    | O + O(\ :math:`^1`\ D)               | Ly-\ :math:`\alpha`: Chabrillat and Kockarts (1997, 1998)             |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\phi`\ (Ly-:math:`\alpha`): Lacoursiere et al. (1999)          |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | SRB: Koppers and Murtaugh (1996)                                      |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | For wavelength\ :math:`\nu` regions not Ly-\ :math:`\alpha` or SRB,   |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\sigma` (120-205nm): Brasseur and Solomon (1986);              |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\sigma` (205-240 nm): Yoshino et al. (1988)                    |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 2     | O\ :math:`_2` + h\ :math:`\nu`                    | 2 O                                  | see above                                                             |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 3     | O\ :math:`_3` + h\ :math:`\nu`                    | O(\ :math:`^1`\ D) + O\ :math:`_2`   | :math:`\sigma` (120-136.5nm): Tanaka et al. (1953);                   |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\sigma` (136.5-175nm): Ackerman (1971);                        |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\sigma` (175-847nm): WMO (1985); except for                    |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\sigma` (185-350nm): Molina and Molina (1986)                  |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\phi` (:math:`<`\ 280nm): Marsh (1999)                         |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\phi` (:math:`>`\ 280nm): JPL-06.                              |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 4     | O\ :math:`_3` + h\ :math:`\nu`                    | O + O\ :math:`_2`                    | see above                                                             |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 5     | N\ :math:`_2`\ O + h\ :math:`\nu`                 | O(\ :math:`^1`\ D) + N\ :math:`_2`   | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 6     | NO + h\ :math:`\nu`                               | N + O                                | Minschwaner et al. (1993)                                             |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 7     | NO + h\ :math:`\nu`                               | NO\ :math:`^+` + e                   |                                                                       |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 8     | NO\ :math:`_2` + h\ :math:`\nu`                   | NO + O                               | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 9     | N\ :math:`_2`\ O\ :math:`_5` + h\ :math:`\nu`     | NO\ :math:`_2` + NO\ :math:`_3`      | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 10    | N\ :math:`_2`\ O5 + h\ :math:`\nu`                | NO + O + NO\ :math:`_3`              | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 11    | HNO\ :math:`_3` + h\ :math:`\nu`                  | OH + NO\ :math:`_2`                  | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 12    | NO\ :math:`_3` + h\ :math:`\nu`                   | NO\ :math:`_2` + O                   | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 13    | NO\ :math:`_3` + h\ :math:`\nu`                   | NO + O\ :math:`_2`                   | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 14    | HO\ :math:`_2`\ NO\ :math:`_2` + h\ :math:`\nu`   | OH + NO\ :math:`_3`                  | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 15    | HO\ :math:`_2`\ NO\ :math:`_2` + h\ :math:`\nu`   | NO\ :math:`_2` + HO\ :math:`_2`      | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 16    | CH\ :math:`_3`\ OOH + h\ :math:`\nu`              | CH\ :math:`_2`\ O + H + OH           | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 17    | CH\ :math:`_2`\ O + h\ :math:`\nu`                | CO + 2 H                             | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 18    | CH\ :math:`_2`\ O + h\ :math:`\nu`                | CO + H\ :math:`_2`                   | JPL-06                                                                |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
| 19    | H\ :math:`_2`\ O + h\ :math:`\nu`                 | H + OH                               | :math:`\phi` (Ly-:math:`\alpha`): Slanger et al. (1982);              |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\phi` (105-145nm): Stief et al. (1975);                        |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\phi` (:math:`>`\ 145): JPL-06                                 |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\phi` (120-182nm): Yoshino et al. (1996);                      |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+
|       |                                                   |                                      | :math:`\phi` (183-194nm): Cantrell et al. (1997)                      |
+-------+---------------------------------------------------+--------------------------------------+-----------------------------------------------------------------------+

Table:  Photolytic Reactions.

****

+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| no.   | Reactants                                        | Products                                          | Comments                                           |
+=======+==================================================+===================================================+====================================================+
| 20    | H\ :math:`_2`\ O + h\ :math:`\nu`                | H\ :math:`_2` + O(\ :math:`^1`\ D)                | (see above)                                        |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 21    | H\ :math:`_2`\ O + h\ :math:`\nu`                | H + 2 O                                           | (see above)                                        |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 22    | H\ :math:`_2`\ O\ :math:`_2` + h\ :math:`\nu`    | 2 OH                                              | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 23    | Cl\ :math:`_2` + h\ :math:`\nu`                  | 2 Cl                                              | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 24    | ClO + h\ :math:`\nu`                             | Cl + O                                            | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 25    | OClO + h\ :math:`\nu`                            | O + ClO                                           | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 26    | Cl\ :math:`_2`\ O\ :math:`_2` + h\ :math:`\nu`   | Cl + ClOO                                         | Burkholder et al. (1990);                          |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
|       |                                                  |                                                   | Stimpfle et al. (2004)                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 27    | HOCl + h\ :math:`\nu`                            | Cl + OH                                           | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 28    | HCl + h\ :math:`\nu`                             | Cl + H                                            | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 29    | ClONO\ :math:`_2` + h\ :math:`\nu`               | Cl + NO\ :math:`_3`                               | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 30    | ClONO\ :math:`_2` + h\ :math:`\nu`               | ClO + NO\ :math:`_2`                              | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 31    | BrCl + h\ :math:`\nu`                            | Br + Cl                                           | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 32    | BrO + h\ :math:`\nu`                             | Br + O                                            | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 33    | HOBr + h\ :math:`\nu`                            | Br + OH                                           | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 34    | BrONO\ :math:`_2` + h\ :math:`\nu`               | Br + NO\ :math:`_3`                               | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 35    | BrONO\ :math:`_2` + h\ :math:`\nu`               | BrO + NO\ :math:`_2`                              | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 36    | CH\ :math:`_3`\ Cl + h\ :math:`\nu`              | Cl + CH\ :math:`_3`\ O\ :math:`_2`                | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 37    | CCl\ :math:`_4` + h\ :math:`\nu`                 | 4 Cl                                              | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 38    | CH\ :math:`_3`\ CCl3 + h\ :math:`\nu`            | 3 Cl                                              | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 39    | CFC11 + h\ :math:`\nu`                           | 3 Cl                                              | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 40    | CFC12 + h\ :math:`\nu`                           | 2 Cl                                              | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 41    | CFC113 + h\ :math:`\nu`                          | 3 Cl                                              | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 42    | HCFC22 + h\ :math:`\nu`                          | Cl                                                | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 43    | CH\ :math:`_3`\ Br + h\ :math:`\nu`              | Br + CH\ :math:`_3`\ O\ :math:`_2`                | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 44    | CF\ :math:`_3`\ Br + h\ :math:`\nu`              | Br                                                | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 45    | CF\ :math:`_2`\ ClBr + h\ :math:`\nu`            | Br + Cl                                           | JPL-06                                             |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 46    | CO\ :math:`_2` + h\ :math:`\nu`                  | CO + O                                            | :math:`\sigma` (120-167): Nakata, et al. (1965);   |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
|       |                                                  |                                                   | :math:`\sigma` (167-199): Huffman (1971)           |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 47    | CH\ :math:`_4` + h\ :math:`\nu`                  | H + CH\ :math:`_3`\ O\ :math:`_2`                 | :math:`\sigma`: JPL-06;                            |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
|       |                                                  |                                                   | based on Brownsword et al. (1997)                  |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
| 48    | CH\ :math:`_4` + h\ :math:`\nu`                  | H\ :math:`_2` + 0.18 CH\ :math:`_2`\ O + 0.18 O   |                                                    |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
|       |                                                  | + 0.44 CO\ :math:`_2` + 0.44 H\ :math:`_2`        | see above                                          |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+
|       |                                                  | + 0.38 CO + 0.05 H\ :math:`_2`\ O                 |                                                    |
+-------+--------------------------------------------------+---------------------------------------------------+----------------------------------------------------+

Table: (continued)  Photolytic Reactions.

****

+---------------------------------------------------------------------------------------+--------------------------------------------+
| Reaction                                                                              | :math:`\Delta H` (kJ mol\ :math:`^{-1}`)   |
+=======================================================================================+============================================+
| O\ :math:`^+` + O\ :math:`_2` :math:`\rightarrow` O\ :math:`_2^+` + O                 | 150.11                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| O\ :math:`^+` + N\ :math:`_2` :math:`\rightarrow` NO\ :math:`^+` + N                  | 105.04                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| N\ :math:`_2^+` + O :math:`\rightarrow` NO\ :math:`^+` + N(\ :math:`^2`\ D)           | 67.53                                      |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| O\ :math:`_2^+` + N :math:`\rightarrow` NO\ :math:`^+` + O                            | 406.16                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| O\ :math:`_2^+` + NO :math:`\rightarrow` NO\ :math:`^+` + O\ :math:`_2`               | 271.38                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| N\ :math:`^+` + O\ :math:`_2` :math:`\rightarrow` O\ :math:`_2^+` + N                 | 239.84                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| N\ :math:`^+` + O\ :math:`_2` :math:`\rightarrow` NO\ :math:`^+` + O                  | 646.28                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| N\ :math:`^+` + O :math:`\rightarrow` O\ :math:`^+` + N                               | 95.55                                      |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| N\ :math:`_2^+` + O\ :math:`_2` :math:`\rightarrow` O\ :math:`_2^+` + N\ :math:`_2`   | 339.59                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| O\ :math:`_2^+` + N\ :math:`_2` :math:`\rightarrow` NO\ :math:`^+` + NO               | –                                          |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| N\ :math:`_2^+` + O :math:`\rightarrow` O\ :math:`^+` + N\ :math:`_2`                 | –                                          |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| NO\ :math:`^+` + e :math:`\rightarrow` 0.2N + 0.8N(\ :math:`^2`\ D) + O               | 82.389                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| O\ :math:`_2^+` + e :math:`\rightarrow` 1.15O + 0.85O(\ :math:`^1`\ D)                | 508.95                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+
| N\ :math:`_2^+` + e :math:`\rightarrow` 1.1N + 0.9N(\ :math:`^2`\ D)                  | 354.83                                     |
+---------------------------------------------------------------------------------------+--------------------------------------------+

Table: Ion-neutral and recombination reactions and exothermicities.

[ionrxntab]

****

+------------------------------------------------------------------------------------------------------------+
| O + h\ :math:`\nu` :math:`\rightarrow` O\ :math:`^+` + e                                                   |
+------------------------------------------------------------------------------------------------------------+
| O + e\ :math:`^*` :math:`\rightarrow` O\ :math:`^+` + e + e\ :math:`^*`                                    |
+------------------------------------------------------------------------------------------------------------+
| N + hv :math:`\rightarrow` N\ :math:`^+` + e                                                               |
+------------------------------------------------------------------------------------------------------------+
| O\ :math:`_2` + h\ :math:`\nu` :math:`\rightarrow` O\ :math:`_2^+` + e                                     |
+------------------------------------------------------------------------------------------------------------+
| O\ :math:`_2` + e\ :math:`^*` :math:`\rightarrow` O\ :math:`_2^+` + e + e\ :math:`^*`                      |
+------------------------------------------------------------------------------------------------------------+
| O\ :math:`_2` + h\ :math:`\nu` :math:`\rightarrow` O + O\ :math:`^+` + e                                   |
+------------------------------------------------------------------------------------------------------------+
| O\ :math:`_2` + e\ :math:`^*` :math:`\rightarrow` O + O\ :math:`^+` + e + e\ :math:`^*`                    |
+------------------------------------------------------------------------------------------------------------+
| N\ :math:`_2` + h\ :math:`\nu` :math:`\rightarrow` N\ :math:`_2^+` + e                                     |
+------------------------------------------------------------------------------------------------------------+
| N\ :math:`_2` + e\ :math:`^*` :math:`\rightarrow` N\ :math:`_2^+` + e + e\ :math:`^*`                      |
+------------------------------------------------------------------------------------------------------------+
| N\ :math:`_2` + h\ :math:`\nu` :math:`\rightarrow` N + N\ :math:`^+` + e                                   |
+------------------------------------------------------------------------------------------------------------+
| N\ :math:`_2` + e\ :math:`^*` :math:`\rightarrow` N + N\ :math:`^+` + e + e\ :math:`^*`                    |
+------------------------------------------------------------------------------------------------------------+
| N\ :math:`_2` + h\ :math:`\nu` :math:`\rightarrow` N(\ :math:`^2`\ D) + N\ :math:`^+` + e                  |
+------------------------------------------------------------------------------------------------------------+
| N\ :math:`_2` + e\ :math:`^*` :math:`\rightarrow` N(\ :math:`^2`\ D) + N\ :math:`^+` + e + e\ :math:`^*`   |
+------------------------------------------------------------------------------------------------------------+

Table: Ionization reactions.

****

+-----------------------+------------------------------------------+---------------+
| wavelength interval   | :math:`F_i^0`                            | :math:`R_i`   |
+-----------------------+------------------------------------------+---------------+
| nm                    | ph cm\ :math:`^{-2}`\ s\ :math:`^{-1}`   |               |
+-----------------------+------------------------------------------+---------------+
| 0.05 - 0.4            | 5.010e+01                                | 6.240e-01     |
+-----------------------+------------------------------------------+---------------+
| 0.4 - 0.8             | 1.000e+04                                | 3.710e-01     |
+-----------------------+------------------------------------------+---------------+
| 0.8 - 1.8             | 2.000e+06                                | 2.000e-01     |
+-----------------------+------------------------------------------+---------------+
| 1.8 - 3.2             | 2.850e+07                                | 6.247e-02     |
+-----------------------+------------------------------------------+---------------+
| 3.2 - 7.0             | 5.326e+08                                | 1.343e-02     |
+-----------------------+------------------------------------------+---------------+
| 7.0 - 15.5            | 1.270e+09                                | 9.182e-03     |
+-----------------------+------------------------------------------+---------------+
| 15.5 - 22.4           | 5.612e+09                                | 1.433e-02     |
+-----------------------+------------------------------------------+---------------+
| 22.4 - 29.0           | 4.342e+09                                | 2.575e-02     |
+-----------------------+------------------------------------------+---------------+
| 29.0 - 32.0           | 8.380e+09                                | 7.059e-03     |
+-----------------------+------------------------------------------+---------------+
| 32.0 - 54.0           | 2.861e+09                                | 1.458e-02     |
+-----------------------+------------------------------------------+---------------+
| 54.0 - 65.0           | 4.830e+09                                | 5.857e-03     |
+-----------------------+------------------------------------------+---------------+
| 65.0 - 79.8           | 1.459e+09                                | 5.719e-03     |
+-----------------------+------------------------------------------+---------------+
| 65.0 - 79.8           | 1.142e+09                                | 3.680e-03     |
+-----------------------+------------------------------------------+---------------+
| 79.8 - 91.3           | 2.364e+09                                | 5.310e-03     |
+-----------------------+------------------------------------------+---------------+
| 79.8 - 91.3           | 3.655e+09                                | 5.261e-03     |
+-----------------------+------------------------------------------+---------------+
| 79.8 - 91.3           | 8.448e+08                                | 5.437e-03     |
+-----------------------+------------------------------------------+---------------+
| 91.3 - 97.5           | 3.818e+08                                | 4.915e-03     |
+-----------------------+------------------------------------------+---------------+
| 91.3 - 97.5           | 1.028e+09                                | 4.955e-03     |
+-----------------------+------------------------------------------+---------------+
| 91.3 - 97.5           | 7.156e+08                                | 4.422e-03     |
+-----------------------+------------------------------------------+---------------+
| 97.5 - 98.7           | 4.482e+09                                | 3.950e-03     |
+-----------------------+------------------------------------------+---------------+
| 98.7 - 102.7          | 4.419e+09                                | 5.021e-03     |
+-----------------------+------------------------------------------+---------------+
| 102.7 - 105.0         | 4.235e+09                                | 4.825e-03     |
+-----------------------+------------------------------------------+---------------+
| 105.0 - 121.0         | 2.273e+10                                | 3.383e-03     |
+-----------------------+------------------------------------------+---------------+

Table: EUVAC model parameters.

[euvactab]

Electric Field
~~~~~~~~~~~~~~

The global electric field is based on a composite of two empirical
models for the different latitude regions: at high latitude the Weimer95
model (**???**), and at low- and midlatitude the Scherliess model
(**???**). In the following the different models are described since the
model is not published to date.

Low- and midlatitude electric potential model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The low- and mid latitude electric field model was developed by Ldger
Scherliess (**???**). It’s based on Incoherent Scatter Radar data
(ISR) from Jicamarca, Arecibo, Saint Santin, Millstone Hill, and the
MU radar in Shigaraki. The electric field is calculated for a given
year, season, UT, :math:`S_a`, local time, and with
longitudinal/latitudinal variation. The empirical model is constructed
from a model for low solar flux (:math:`S_a = 90`) and a high solar
flux model (:math:`S_a = 180`). The global electric potential is
expressed according to (**???**) by

.. math::

   \begin{split}
     \Phi(d,T,t,\lambda) = \sum_{k=0}^2 \sum_{l=-2}^2 \sum_{m=-n}^n \sum_{n=1}^{12}
       & A_{klmn} P_n^m(sin \lambda) f_m(\frac{2 \Pi t}{24})  \\
       & f_l(\frac{2 \Pi T}{24}) f_{-k}(\frac{2 \Pi (d + 9)}{365.24})
    \end{split}

with

.. math::

   \begin{aligned}
      f_m(\phi) & = \sqrt{2} \sin(m \phi) \quad & m > 0 \\
      f_m(\phi) & = 1                     \quad & m = 0 \\
      f_m(\phi) & = \sqrt{2} \cos(m \phi) \quad & m < 0\end{aligned}

the day of the year is denoted by :math:`d`, universal time by
:math:`T`, magnetic local time by :math:`t`, and geomagnetic latitude
:math:`\lambda`. The values of :math:`d`, :math:`T`, and :math:`t` are
expressed as angles between 0 and 2\ :math:`\Pi`. :math:`P_n^m` are
fully normalized Legendre polynomials. Due to the assumption that the
geomagnetic field lines are highly conducting, the :math:`n+m` odd
coefficients are set to zero to get a symmetrical electric potential
about the magnetic equator. The coefficients :math:`A_{klmn}` are
found by a least–square fit for low and high solar flux. The solar
cycle dependence is introduced by inter- and extrapolation of the sets
of coefficients :math:`A_{klmn}^{low}` for :math:`S_a = 90` and
:math:`A_{klmn}^{high}` for :math:`S_a =
180`.

.. math::

   \begin{aligned}
     A_{klmn} =A^{low}_{klmn} + S_{aM}[A^{high}_{klmn} - A^{low}_{klmn}] \end{aligned}

with

.. math::

   \begin{aligned}
   S_{aM}  & = \frac{arctan[(S_a-65)^2/ 90^2]- a_{90}}{a_{180}-a_{90}} \\
   a_{90}  & = arctan[(90-65)^2/90^2]\\
   a_{180} & = arctan[(180-65)^2/90^2]\end{aligned}

We are using the daily :math:`F_{10.7}` number for :math:`S_a`.
:math:`S_{aM}` levels off at high and low solar flux numbers, and
therefore the model does not predict unrealistic high or low electric
potential values.

The geomagnetic field is described by modified apex coordinates
(**???**) which already take into account the distortion of the magnetic
field. Modified apex coordinates have a reference height associated with
them, which in our case is set to 130 km. The electric field
:math:`\mathbf{E}` and the electromagnetic drift velocity
:math:`\mathbf{v}_E` can be expressed by quantities mapped to the
reference height, e.g. by :math:`E_{d1}`, :math:`E_{d2}` and
:math:`v_{e1}`, :math:`v_{e2}`. These quantities are not actual electric
field or electromagnetic drift velocity components, but rather the
representation of the electric field or electromagnetic drift velocities
by being constant along the geomagnetic field line. The fields in an
arbitrary direction :math:`\mathbf{I}` can be expressed by

.. math::

   \begin{aligned}
   \mathbf{I} \cdot \mathbf{E}   &=\mathbf{I} \cdot  \mathbf{d}_1  E_{d1} + \mathbf{I} \cdot \mathbf{d}_2  E_{d2} \\
   \mathbf{I} \cdot \mathbf{v}_E &= \mathbf{I} \cdot \mathbf{e}_1  v_{e1} + \mathbf{I} \cdot \mathbf{e}_2  v_{e2}\end{aligned}

The basis vector :math:`\mathbf{d}_1` and :math:`\mathbf{e}_1` are in
more–or–less magnetic eastward direction and :math:`\mathbf{d}_2` and
:math:`\mathbf{e}_2` in downward/ equatorward direction. The base
vectors vary with height, :math:`\mathbf{d}_i` is decreasing and
:math:`\mathbf{e}_i` increasing with altitude. Therefore when the base
vectors are applied to the mapped field at the reference height, e.g.
:math:`E_{d1}`, :math:`E_{d2}` and :math:`v_{e1}`, :math:`v_{e2}`, they
already take into account the height and directional variation of the
corresponding quantity. Note that the modified apex coordinates are
using the International Geomagnetic Reference Field (IGRF), and in the
WACCM4 code the IGRF is only defined between the years 1900 and 2000.
The description of the IGRF can be updated every 5 years to be extended
in time.

High–latitude electric potential model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The high–latitude electric potential model from Weimer (**???**) is
used. The model is based on spherical harmonic coefficients that were
derived by least square fitting of measurements from the Dynamics
Explorer 2 (DE2) satellite. The variation of the spherical harmonic
coefficients with the interplanetary magnetic field (IMF) clock angle,
IMF strength, solar wind velocity and season can be reproduced by a
combination of Fourier series and multiple linear regression formula.
The final model varies with magnetic latitude, magnetic local time,
season, IMF strength and direction, and solar wind velocity. For our
purpose we have set the solar wind speed to a constant value of 400 km/s
and only consider the effects of IMF :math:`B_z` (:math:`B_y=0`). Since
the IMF conditions are not known all the time, we developed an empirical
relation between :math:`B_z` and the :math:`K_p` index and the solar
flux number :math:`S_a`. Both, the :math:`K_p` index and the daily solar
flux number :math:`F_{10.7}`, are known in the WACCM4 model.

.. math::

   \begin{split}
    B_z (K_p, F_{10.7}) = & - 0.085 K_p^2 - 0.08104 K_p + 0.4337 + \\
                     & 0.00794 F_{10.7} - 0.00219 K_p F_{10.7}
    \end{split}

Note that the Weimer model uses an average year of 365.24 days/year and
an average month of 30.6001 days/month. The boundary of the Weimer model
is at :math:`46^o` magnetic latitude. The model was developed for an
averaged northern and southern hemisphere. The :math:`B_y` value and the
season are reversed to get the values for the other hemisphere.

Combing low–/ mid–latitude with the high latitude electric potential
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After the low/mid–latitude electric potential :math:`\Phi_{mid}` and the
high latitude potential :math:`\Phi_{hgh}` are calculated, both patterns
are combined to be smooth at the boundary. The boundary between high and
mid latitude :math:`\lambda_{bnd}` is defined to lie where the electric
field magnitude :math:`E` from :math:`\Phi_{hgh}` equals 15 mV/m. After
finding the longitudinal variation of the high latitude boundary
:math:`\lambda_{bnd}`, it’s shifted halfway towards :math:`54^o`
magnetic latitude. The width of the transition zone
:math:`2 \Delta \lambda_{trs}` from high to mid latitude varies with
magnetic local time. First, the high and mid latitude electric potential
are adjusted by a constant factor such that the average for the high and
mid latitude electric potential along the boundary :math:`\lambda_{bnd}`
are the same. The combined electric potential :math:`\Phi` is defined by

.. math::

   \Phi = \begin{cases}  \Phi_{mid} \quad & | \lambda | < \lambda_{bnd}-\Delta \lambda_{trs} \\
                         \Phi_{hgh} \quad & | \lambda | > \lambda_{bnd}+\Delta \lambda_{trs} \\
                         F_{int}(\Phi_{mid},\Phi_{hgh}) \quad & \lambda_{bnd}-\Delta \lambda_{trs} \leq
                            | \lambda | \leq \lambda_{bnd}+\Delta \lambda_{trs}
           \end{cases}

with

.. math::

   \begin{split}
   F_{int}(\Phi_{mid},\Phi_{hgh}) = \frac{1}{3} \frac{1}{2 \Delta \lambda_{trs}}[
         &  \left\{
           \Phi_{mid}(\phi,\lambda_{bnd}-\Delta \lambda_{trs}) + 2
           \Phi_{mid}(\phi,\lambda) \right\} \\
         & \left\{\lambda_{bnd}-|\lambda|+\Delta \lambda_{trs} \right\}
           + ( \Phi_{hgh}(\phi,\lambda_{bnd}+\Delta \lambda_{trs}) + \\
         & 2
           \Phi_{hgh}(\phi,\lambda) ) \left\{-\lambda_{bnd}+|\lambda|+\Delta \lambda_{trs}\right\}
          ]
    \end{split}

Calculation of electric field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The electric field can be derived from the electric potential by

.. math::

   \begin{aligned}
     \mathbf{E} = - \nabla \Phi\end{aligned}

The more-or-less magnetic eastward electric field component
:math:`E_{d1}` and the in general downward/ equatorward :math:`E_{d2}`
component are calculated. These components are constant along the
magnetic field line. They are calculated at a reference height
:math:`h_r= \; 130` km with :math:`R = R_{earth}+ h_r`. The electric
field does not vary much with altitude, and therefore we assume in the
code that the electric field is constant in height.

.. math::

   \begin{aligned}
     E_{d1} &= -\frac{1}{R cos \lambda}\frac{\partial \Phi}{\partial \phi} \\
     E_{d2} &= \frac{1}{R \sin I}\frac{\partial \Phi}{\partial \lambda}\end{aligned}

with :math:`\sin I = 2\sin \lambda [4-3\cos^2\lambda]^{0.5}`.

Calculation of electrodynamic drift velocity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The electric field is calculated on a :math:`2^o \; \times \; 2^o`
degree geomagnetic grid with the magnetic longitude represented by the
magnetic local time (MLT) from 0 MLT to 24 MLT. Therefore, the
magnetic local time of the geographic longitudes of the WACCM4 grid
has to be determined first to map from the geomagnetic to the
geographic WACCM4 grid. The magnetic local time is calculated by using
the location of the geomagnetic dipole North pole, the location of the
subsolar point, and the apex longitude of the geographic WACCM4 grid
point. A bilinear interpolation is used for the mapping. Note that
every processor calculates the global electric field, which is
computationally inexpensive. Otherwise, to calculate the electric
field some communication between the different processors would be
necessary to get the spatial derivatives.
The mapped electric field is rotated into the geographic direction by

.. math::

   \begin{aligned}
   \mathbf{E} &= \mathbf{d}_1 E_{d1} + \mathbf{d}_2 E_{d2}\end{aligned}

with the components of :math:`\mathbf{E}` being the geographic
eastward, westward and upward electric field.
At high altitudes the ion–neutral collision frequency :math:`\nu_{in}`
is small in relation to the angular gyrofrequency of the ions
:math:`\Omega_i` (:math:`\nu_{in} \ll \Omega_i`), and the
electron–neutral collision frequency :math:`\nu_{en}` is much smaller
than the angular gyrofrequency of the electrons :math:`\Omega_e`
(:math:`\nu_{en} \ll \Omega_e`), due to the decrease in neutral
density with increasing altitude. Therefore, the ion drift
:math:`\mathbf{v}_{i\bot}` perpendicular to the geomagnetic field can
be simplified by the electrodynamic drift velocity
:math:`\mathbf{v}_E`

.. math::

   \begin{aligned}
   \mathbf{v}_{i\bot} \approx \mathbf{v}_E =  \frac{\mathbf{E}
   \times \mathbf{B}_o}{\mathbf{B}_o^2}\end{aligned}

with :math:`\mathbf{B}_o` the geomagnetic main field from IGRF.

Ion drag calculation
^^^^^^^^^^^^^^^^^^^^

The following is written according to the source code. Two subroutines
iondrag\_calc exist in the code, one uses the calculated ion drag
coefficients if WACCM\_MOZART  is used, and the other one uses look-up
tables for the ion drag coefficients :math:`\lambda_1` and
:math:`\lambda_2`. It is assumed that the electron :math:`T_e` and ion :math:`T_i`
temperature is equal to the neutral temperature :math:`T_n`.

.. math::

   \begin{aligned}
   T_i = T_e = T_n\end{aligned}

The dip angle I of the geomagnetic field is calculated by

.. math::

   \begin{aligned}
   I = \arctan \frac{B_z}{\sqrt{B_{north}^2+B_{east}^2}}\end{aligned}

with a minimum dip angle :math:`|I| \geq 0.17`. The declination is

.. math::

   \begin{aligned}
   D = \arctan \frac{B_{east}}{B_{north}}\end{aligned}

The magnetic field component :math:`B_z, B_{east}, B_{north}` are
determined from the International Geomagnetic Reference Field (IGRF).
The collision frequencies :math:`\nu` in units of :math:`s^{-1}` are
determined by, e.g. (**???**)

.. math::

   \begin{aligned}
   \frac{1}{N_{O_2}} \nu_{O_2^+ - O_2} &= 2.59\times 10^{-11}\sqrt{\frac{T_i +
   T_e}{2}}\left[ 1-0.73 log_{10}\sqrt{\frac{T_i +
   T_e}{2}}\right]^2  \\
   \frac{1}{N_{O_2}} \nu_{O^+ - O_2}  &=6.64\times 10^{-10}  \\
   \frac{1}{N_{O_2}} \nu_{NO^+ - O_2} &=4.27\times 10^{-10}  \\
   \frac{1}{N_{O}} \nu_{O^+ - O}      &=3.67\times
   10^{-11}\sqrt{\frac{T_i +
   T_e}{2}}\left[ 1-0.064 log_{10}\sqrt{\frac{T_i +
   T_e}{2}}\right]^2  f_{cor}  \\
   \frac{1}{N_{O}} \nu_{NO^+ - O}    &=2.44\times 10^{-10}  \\
   \frac{1}{N_{O}} \nu_{O_2^+ - O}   &=2.31\times 10^{-10}  \\
   \frac{1}{N_{N_2}} \nu_{O_2^+ - N_2}&=4.13\times 10^{-10} \\
   \frac{1}{N_{N_2}} \nu_{NO^+ - N_2} &=4.34\times 10^{-10} \\
   \frac{1}{N_{N_2}} \nu_{O^+ - N_2}  &=6.82\times 10^{-10}\end{aligned}

with :math:`N_n` the number density for the neutral n in units of
:math:`1/cm^3`, and the temperature in Kelvins. The collisions
frequencies for :math:`\nu_{O_2^+ - O_2}` and :math:`\nu_{O^+ - O}`
are resonant, all other are nonresonant. The arbitrary correction
factor :math:`f_{cor}` multiplies the :math:`\nu_{O^+ - O}` collision
frequency and is set to :math:`f_{cor} =1.5` which has been found to
improve agreement between calculated and observed winds and electron
densities in the upper thermosphere in other models. The mean mass
:math:`\overline{m}_{mid}` [g/mole] at the midpoints of the height
level is calculated in the Mozart module. The number densities
:math:`[1/cm^3]` are

.. math::

   \begin{aligned}
   N_{O_2} &= \frac{N \overline{m}_{mid} mmr_{O_2}}{m_{O_2}} \\
   N_{O}   &= \frac{N \overline{m}_{mid} mmr_{O}}{m_{O}} \\
   N_{N_2} &= \frac{N \overline{m}_{mid} mmr_{N_2}}{m_{N_2}} \\
   N_{O_2^+}&= \frac{N \overline{m}_{mid} mmr_{O_2^+}}{m_{O_2^+}} \\
   N_{O^+} &= \frac{N \overline{m}_{mid} mmr_{O^+}}{m_{O^+}} \\
   N_{e}   &= \frac{N \overline{m}_{mid} mmr_e }{m_{e}}\end{aligned}

with :math:`mmr` the mass mixing ratio, and :math:`N` the total
number density in units of :math:`1/cm^3`. The pressure
:math:`[dyne/cm^2]` and the mean mass at the midpoint
:math:`\overline{m}_{mid}` in units of :math:`g/mole` are

.. math::

   \begin{aligned}
   p = 10 \; p_{mid} \\
   N \overline{m}_{mid} = \frac{p \; \overline{m}}{k_B T_n}\end{aligned}

with the factor 10 to convert from [Pa] to :math:`[dyne/cm^2]`, and
:math:`k_B` the Boltzmann constant. The collision frequencies are

.. math::

   \begin{aligned}
   \nu_{O_2^+} &= \nu_{O_2^+ - O_2} + \nu_{O_2^+ - O} +
   \nu_{O_2^+ - N_2}  \\
   \nu_{O^+}   &= \nu_{O^+ - O_2} + \nu_{O^+ - O} +
   \nu_{O^+ - N_2}  \\
   \nu_{NO^+}  &= \nu_{NO^+ - O_2} + \nu_{NO^+ - O} +
   \nu_{NO^+ - N_2}  \\
   \begin{split}
   \nu_{en}   &= 2.33\times10^{-11} N_{N_2} T_e (1-1.21 \times 10^{-4}
   T_e) + \\
   & 1.82 \times 10^{-10} N_{O_2} \sqrt{T_e} (1 + 3.6 \times 10^{-2}
   \sqrt{T_e}) + \\
   & 8.9 \times 10^{-11} N_O \sqrt{T_e} (1 + 5.7 \times 10^{-4} T_e)
   \end{split}\end{aligned}
   
The ratios :math:`r` between collision frequency :math:`\nu` and gyro
frequency :math:`\Omega` are

.. math::

   \begin{aligned}
   r_{O_2^+} &= \frac{\nu_{O_2^+}}{\Omega_{O_2^+}}\\
   r_{O^+}   &= \frac{\nu_{O^+}}{\Omega_{O^+}}\\
   r_{NO^+}  &= \frac{\nu_{NO^+}}{\Omega_{NO^+}}\\
   r_{e}     &= \frac{\nu_{en}}{\Omega_{e}}\end{aligned}

with the gyro frequency for ions :math:`\Omega_i = e B/m_i` and for
electrons :math:`\Omega_e=eB/m_e`. The Pedersen conductivity [ S/m] is

.. math::
     
   \begin{split}
   \sigma_P = &\frac{e}{B} [ N_{O^+} \frac{r_{O^+}}
   {1+r_{O^+}^2 } +
   N_{O_2^+} \frac{r_{O_2^+}}
   {1+r_{O_2^+}^2 } + \\
   & N_{NO^+} \frac{r_{NO^+}}
   {1+r_{NO^+}^2 } +
   N_{e} \frac{r_e}
   {1+r_e^2 } ]
   \end{split}

The Hall conductivity [S/m] is

.. math::

   \begin{split}
   \sigma_H = &\frac{e}{B} [ -N_{O^+} \frac{1}
   {1+r_{O^+}^2 } -
   N_{O_2^+} \frac{1}
   {1+r_{O_2^+}^2 } - \\
   & N_{NO^+} \frac{1}
   {1+r_{NO^+}^2 }+
   N_{e} \frac{1}
   {1+r_{e}^2 }  ]
   \end{split}

The ion drag coefficients are

.. math::

   \begin{aligned}
   \lambda_1 &= \frac{\sigma_P B^2}{\rho} \\
   \lambda_2 &= \frac{\sigma_H B^2}{\rho}\end{aligned}

with :math:`\rho= N \frac{\overline{m}}{N_A}` , and :math:`N_A` the
Avagadro number. The ion drag tensor in magnetic direction
:math:`\underline{\lambda}^{mag}` is

.. math::

   \begin{gathered}
   \underline{\lambda}^{mag}=
   \begin{pmatrix}
   \lambda_{xx}^{mag} & \lambda_{xy}^{mag} \\
   \lambda_{yx}^{mag} & \lambda_{yy}^{mag}
   \end{pmatrix} =
   \begin{pmatrix}
   \lambda_1 & \lambda_{2}sin I\\
   -\lambda_2 sin I & \lambda_{1} sin^2 I
   \end{pmatrix}\end{gathered}

with the x–direction in magnetic east, and y–direction magnetic north
in the both hemispheres. The ion drag tensor can be rotated in
geographic direction by using the rotation matrix :math:`\mathbf{R}`

.. math::

   \begin{gathered}
   \mathbf{R} =
   \begin{pmatrix}
   \cos D & \sin D\\
   -\sin D & \cos D
   \end{pmatrix}\end{gathered}
   
Applying the rotation to the ion drag tensor
:math:`\mathbf{R}\underline{\lambda}^{mag}\mathbf{R}^{-1}` leads to

.. math::

   \begin{gathered}
   \Lambda =
   \begin{pmatrix}
   \lambda_{xx} & \lambda_{xy}  \\
   \lambda_{yx} & \lambda_{yy}
   \end{pmatrix}
   = \\
   \begin{pmatrix}
   \lambda_{xx}^{mag} cos^2 D + \lambda_{yy}^{mag}
   sin^2 D &  \lambda_{xy}^{mag} + (\lambda_{yy}^{mag}-
   \lambda_{xx}^{mag}) \sin D \cos D  \\
   \lambda_{yx}^{mag} + (\lambda_{yy}^{mag}-
   \lambda_{xx}^{mag}) \sin D \cos D  & \lambda_{yy}^{mag} \cos^2 D + \lambda_{xx}^{mag}
   \sin^2 D
   \end{pmatrix}\end{gathered}

The ion drag acceleration :math:`\mathbf{a}_i` due to the Ampère
force is

.. math::

   \begin{aligned}
   \mathbf{a}_i = \frac{\mathbf{J}\times \mathbf{B}}{\rho} =
   \lambda_1 (\mathbf{v}_E - \mathbf{u}_{n\perp}) + \lambda_2
   \mathbf{\hat{b}}\times (\mathbf{v}_E - \mathbf{u}_{n\perp})\end{aligned}
   
with :math:`\mathbf{u}_{n\perp}` the neutral wind velocity
perpendicular to the geomagnetic field and :math:`\mathbf{\hat{b}}`
the unit vector of the geomagnetic field. The tendencies on the
neutral wind are calculated by

.. math::

   \begin{aligned}
   \frac{\partial \mathbf{v}_{En}}{\partial t} = -\Lambda \mathbf{v}_{En}\end{aligned}

For stability an implicit scheme is used with

.. math::

   \begin{aligned}
   \frac{\mathbf{v}_{En}(t+\Delta t) - \mathbf{v}_{En}(t)}{\Delta t} =
   -\Lambda \mathbf{v}_{En}(t+\Delta t)\end{aligned}
   
which leads to

.. math::

   \begin{aligned}
   (\frac{1}{\Delta t} I + \Lambda)\mathbf{v}_{En}(t+\Delta t)  =
   \frac{1}{\Delta t}\mathbf{v}_{En}(t)\end{aligned}
   
with :math:`I` the unit matrix. Solving for
:math:`\mathbf{v}_{En}(t+\Delta t)` gives

.. math::

   \begin{aligned}
   \mathbf{v}_{En}(t+\Delta t)  =
   \frac{1}{\Delta t}(\frac{1}{\Delta t} I + \Lambda)^{-1}\mathbf{v}_{En}(t)\end{aligned}
   
The tendencies are determined by

.. math::

   \begin{aligned}
   \frac{\partial \mathbf{v}_{En}}{\partial t} =
   \frac{\mathbf{v}_{En}(t+\Delta t) - \mathbf{v}_{En}(t)}{\Delta t} =
   \frac{1}{\Delta t}[ \frac{1}{\Delta t}(\frac{1}{\Delta t} I + \Lambda)^{-1}-1]
   \mathbf{v}_{En}(t)\end{aligned}

The tensor :math:`\frac{1}{\Delta t} I + \Lambda` is

.. math::

   \begin{gathered}
   \begin{pmatrix}
   \lambda_{11}^* & \lambda_{12}^* \\
   \lambda_{21}^* & \lambda_{22}^*
   \end{pmatrix}
   =
   \begin{pmatrix}
   \frac{1}{\Delta t} + \lambda_{xx}& \lambda_{xy} \\
   \lambda_{yx} & \frac{1}{\Delta t } + \lambda_{yy}
   \end{pmatrix}\end{gathered}
   
.. math::
      
   \begin{aligned}
   \frac{Det}{\Delta t} = \frac{1}{\Delta t} \frac{1}{\lambda_{11}^* \lambda_{22}^* - \lambda_{12}^* \lambda_{21}^*}\end{aligned}
   
The tendencies applied to the neutral winds with
:math:`\mathbf{v}_{En}=(u_E- u_n, v_E - v_n)` gives
      
.. math::

   \begin{aligned}
   d_t u_i =& \frac{1}{\Delta t} \left[\frac{Det}{\Delta t}  \left( \lambda_{12}^* (v_E - v_n)
   - \lambda_{22}^* (u_E- u_n) \right) + u_E - u_n \right] \\
     d_t v_i =& \frac{1}{\Delta t} \left[ \frac{Det}{\Delta t} \left( \lambda_{21}^* (u_E -u_n)
     - \lambda_{11}^* (v_E- v_n) \right) + v_E - v_n \right]\end{aligned}
       
The electromagnetic energy transfer to the ionosphere is

.. math::

   \begin{aligned}
   \mathbf{J}\cdot\mathbf{E} = \mathbf{J}\cdot\mathbf{E}' +
   \mathbf{u}_n \cdot \mathbf{J}\times\mathbf{B}\end{aligned}

The first term on the right hand side denotes the Joule heating, which
is the electromagnetic energy transfer rate in the frame of reference of
the neutral wind. The second term represents the generation of kinetic
energy due to the Ampère force. Since the electric field is small along
the magnetic field line, we consider only the perpendicular component to
the magnetic field of the Joule heating
:math:`\mathbf{J}_{\perp}\cdot\mathbf{E}'`. The electric field in the
frame of the neutral wind :math:`\mathbf{u}` can be written as

.. math::

   \begin{aligned}
   \mathbf{E}' = \mathbf{E} + \mathbf{u}\times \mathbf{B}\end{aligned}

The Joule heating can be expressed by

.. math::

   \begin{aligned}
    \mathbf{J}_{\perp}\cdot\mathbf{E}' = \sigma_P \mathbf{E}'^2\end{aligned}

with

.. math::

   \begin{aligned}
     \mathbf{E}'^2 = B^2 (\frac{\mathbf{E}\times\mathbf{B}}{B^2} -
     \mathbf{u}_{\perp})^2\end{aligned}

and :math:`\frac{\mathbf{E}\times\mathbf{B}}{B^2}` the electromagnetic
drift velocity :math:`\mathbf{v}_E` with the components :math:`u_E` and
:math:`v_E`. The Joule heating :math:`Q_J` is

.. math::

   \begin{aligned}
    Q_J = (u_E - u_n)^2 \lambda_{xx} + (u_E - u_n)(v_E - v_n)
    (\lambda_{xy} - \lambda_{yx}) _+ (v_E - v_n)^2 \lambda_{yy}\end{aligned}

Note, that the vertical velocity components are not taken into account
here.

Boundary Conditions
~~~~~~~~~~~~~~~~~~~

The upper boundary conditions for momentum and for most constituents are
the usual zero flux conditions used in CAM4. However, in the energy
budget of the thermosphere, much of the SW radiation at wavelengths
:math:`<`\ 120 nm is absorbed above 145 km (the upper boundary of the
model), where LW radiation is very inefficient. This energy is
transported downward by molecular diffusion to below 120 km, where it
can be dissipated more efficiently by LW emission. Imposing a zero flux
upper boundary condition on heat omits a major term in the heat budget
and causes the lower thermosphere to be much too cold. Instead, we use
the Mass Spectrometer-Incoherent Scatter (MSIS) model (**???**; **???**)
to specify the temperature at the top boundary as a function of season
and phase of the solar cycle. The version of the MSIS model used in is
NRLMSISE-00 [see
http://uap-www.nrl.navy.mil/models\_web/msis/msis\_home.htm].

For chemical constituents, surface mixing ratios of CH\ :math:`_4`,
N\ :math:`_2`\ O, CO\ :math:`_2`, H\ :math:`_2`, CFC-11, CFC-12,
CFC-113, HCFC-22, H-1211, H-1301, CCl\ :math:`_4`,
CH\ :math:`_3`\ CCH\ :math:`_3`, CH\ :math:`_3`\ Cl, and
CH\ :math:`_3`\ Br are specified from observations. The model accounts
for surface emissions of NO\ :math:`_{\rm X}` and CO based on the
emission inventories described in (**???**). The
NO\ :math:`_{\rm X}` source from lightning is distributed according to
the location of convective clouds based on (**???**) and (**???**), with
a vertical profile following (**???**). Aircraft emissions of
NO\ :math:`_{\rm X}` and CO are included in the model and based on
(**???**).

At the upper boundary, a zero-flux upper boundary condition is used for
most species whose mixing ratio is negligible in the lower thermosphere,
while mixing ratios of other species are specified from a variety of
sources. The MSIS model is used to specify the mixing ratios of O,
O\ :math:`_2`, H, and N; as in the case of temperature, the MSIS model
returns values of these constituents as functions of season and phase of
the solar cycle. CO and CO\ :math:`_2` are specified at the upper
boundary using output from the TIME-GCM (**???**). NO is specified using
data from the Student Nitric Oxide Explorer (SNOE) satellite (**???**),
which has been parameterized as a function of latitude, season, and
phase of the solar cycle in the Nitric Oxide Empirical Model (NOEM) of
(**???**). Finally, a global-mean value (typical of the sunlit lower
thermosphere) is specified for species such as H\ :math:`_2`\ O, whose
abundance near the top of the model is very small under sunlit
conditions, but which can be rapidly transported upward by diffusive
separation in polar night (since they are lighter than the background
atmosphere). In these cases, a zero-flux boundary condition leads to
unrealistically large mixing ratios at the model top in polar night.

Slab Ocean Model
================

The Slab Ocean Model (SOM) configuration enables a simple but tightly
coupled ocean modeling component combined with a thermodynamic sea ice
component based on the CCSM3 sea ice model. This configuration of the
atmospheric model allows for a fully-interactive treatment of surface
exchange processes in the |cam|. The ocean prognostic variable is the mixed
layer temperature :math:`T_{o}`, while the thermodynamic sea ice model
treats snow depth, surface temperature, ice thickness, ice fractional
coverage, and internal energy at four layers for a single thickness
category. The ocean mixed layer contains an internal heat source
:math:`Q` (also called a :math:`Q` flux), whose values are generally
specified by a CAM control run, representing seasonal deep water
exchange and horizontal ocean heat transport. For example, using
prescribed sea surface temperatures and sea ice distributions, the net
surface energy flux over the ocean surface can be evaluated to yield the
heat source :math:`Q`. Additional exchange of heat occurs between the
ocean mixed layer and the sea ice model during ice formation and ice
melt. To ensure the |cam| SOM sea ice simulation compares well to the observed
ice distribution, and to moderate sea ice changes in climate change
experiments, the :math:`Q` flux term is adjusted under the ice in a
globally conserving manner.

Open Ocean Component
--------------------

The general formulation for the open ocean slab model is taken from
Hansen et al. (1984), although we have modified it to allow for a
fractional sea ice coverage. The governing equation for ocean mixed
layer temperature :math:`T_o` is:

.. math::
   :label: 6.a.1

   \rho_o C_o h_o \frac{\partial T_{o}}{\partial t} = (1-A) F + Q 
   + A F_{oi} + (1-A) F_{frz} 

where :math:`T_o` is the ocean mixed layer temperature, :math:`\rho_o`
is the density of ocean water, :math:`C_o` is the heat capacity of ocean
water, :math:`h_o` is the annual mean ocean mixed layer depth (m),
:math:`A` is the fraction of the ocean covered by sea ice, :math:`F` is
the net atmosphere to ocean heat flux (Wm:math:`^{-2}`), :math:`Q` is
the internal ocean mixed layer heat flux (Wm:math:`^{-2}`), simulating
deep water heat exchange and ocean transport, :math:`F_{oi}` is the heat
exchanged with the sea ice (Wm:math:`^{-2}`) (including solar radiation
transmitted through the ice) and :math:`F_{frz}` is the heat gained when
sea ice grows over open water (Wm:math:`^{-2}`). :math:`\rho_o` and
:math:`C_o` are constants (see Table [table:somconst] for values of the
constants), and the nomenclature is such that all right-hand-side fluxes
are positive down.

+-----------------------------------------------------------------------+
| **Temperatures**                                                      |
+=======================================================================+
| :math:`T_f = -1.8 \ \mathrm{^{\circ}C}`                               |
+-----------------------------------------------------------------------+
| **Ocean**                                                             |
+-----------------------------------------------------------------------+
| :math:`\rho_{o} = 1.026 \times 10^{3} \ \mathrm{kg \: m^{-3}}`        |
+-----------------------------------------------------------------------+
| :math:`C_o = 3.93 \times 10^{3} \ \mathrm{J \:  kg^{-1} \: K^{-1}}`   |
+-----------------------------------------------------------------------+
| **Ice**                                                               |
+-----------------------------------------------------------------------+
| :math:`L_i = 3.014 \times 10^{8} \ \mathrm{J \: m^{-3}}`              |
+-----------------------------------------------------------------------+

Table: [table:somconst]Constants for the Slab Ocean Model

The geographic structure of ocean mixed layer depth :math:`h_o` is
specified from Levitus (1982). Monthly mean mixed layer depths are
determined using this dataset’s standard measure of salinity
:math:`\sigma_t = (\rho_S
- 1) \cdot 10^3` (:math:`\rho_S` is the density of sea water for a
specified salinity, temperature, and atmospheric pressure) where the
equality :math:`\sigma_t(h_o)-\sigma_t`\ (surface) = .125 is satisfied
on a :math:`1^\circ 
\times 1^\circ` grid. These data are then averaged to the standard |cam| grid
(all data falling within a |cam| grid box are equally weighted), horizontally
smoothed 10 times using a 1-2-1 smoother, and capped at 200m (to prevent
excessively long adjustment times in coupled atmosphere ocean
experiments). The resulting mixed layer depths in the tropics are
generally shallow (10m-30m) while at high latitudes in both hemispheres
there are large seasonal variations (from 10m up to the 200m maximum).
The annually-averaged geographically-varying mixed layer depth, which is
used for purposes related to energy conservation, is produced by
averaging the monthly mean values.

The geographic distribution of the internal heat source :math:`Q` is
generally specified on a monthly basis using a control |cam| integration as
described below. During a SOM numerical integration :math:`Q` is
linearly interpolated between monthly values (taken as mid month) to the
appropriate model time step. The energy fluxes associated with ice
formation and ice melt (:math:`F_{frz}` and :math:`F_{mlt}`
respectively) are explicitly predicted.

The net atmosphere-to-ocean heat flux in the absence of sea ice,
:math:`F`, is defined as:

.. math:: F = FS - FL - SH - LH 
	  :label: 6.a.2

where :math:`FS` is the net solar flux absorbed by the ocean mixed
layer, :math:`FL` is the net longwave energy flux of the ocean surface
to the atmosphere, :math:`SH` is the sensible heat flux from the ocean
to the atmosphere, and :math:`LH` is the latent heat flux from the ocean
to the atmosphere. The surface temperature used in evaluating these
fluxes is :math:`T_o`.

The evolution of the mixed-layer temperature field, :math:`T_o`, is
evaluated using an explicit forward time step. At iteration *n* the
required information to advance the forecast include :math:`T_o^n,
h_o, F^n, Q^n`, and :math:`A^n`, where :math:`h_o` is time invariant and
:math:`Q^n` is linearly interpolated in time between prescribed
mid-monthly values. It is assumed that the exchange between the ocean
mixed layer and the atmosphere occurs faster than deep adjustments.
Hence, the first adjustment to :math:`T_o` is evaluated as:

.. math::
   :label: 6.a.3

   T_o^{(n+1)'} = T_o^n + \frac{(1-A^{n}) F^{n}}
   {\rho_{o} C_o h_{o}} \Delta t 

where :math:`\Delta t` is the model time step. We note that :math:`A^n`
is computed from the fraction of the total |cam| grid box that is not covered
by land, since only ocean and sea ice covered portion of the grid cell
are considered for the SOM configuration:

.. math:: 
   :label: 6.a.4

   A^n = \frac{{icefrac}^n} {(1 - landfrac)} 

where :math:`icefrac` is the fraction of ice in the |cam| grid cell and
:math:`landfrac` is the fraction of land in the |cam| grid box.

The :math:`Q^n` flux is then adjusted since it is possible (using
monthly specified values of :math:`Q`) to introduce a non-physical
cooling of the mixed layer when its temperature is at the freezing
point. Therefore, if :math:`Q^n > 0` and
:math:`T_o^{(n+1)'} < 0^\circ C`, then

.. math:: 
   :label: 6.a.5

   Q^{n'} = Q^{n} f_T 	     

where :math:`f_T = {(T_f - T_o^{(n+1)'})}/{T_f}`, and :math:`T_f` is the
ocean freezing temperature of -1.8:math:`^\circ`\ C (where :math:`T_o`
is expressed in units of :math:`^\circ`\ C). This adjustment smoothly
reduces the loss of heat from the mixed layer (if any) to zero as its
temperature approaches the specified freezing point of sea water.

To ensure that the predicted SOM sea ice distribution compares favorably
with the control simulation, and is bounded against unchecked growth or
loss for atmospheric conditions significantly different from present
day, an additional adjustment to :math:`Q` under sea ice is applied:

.. math:: Q^{n''} = Q^{n'} +  [ A^n f(h_i) q_{hem} ]

where

.. math::

   \begin{aligned}
     f(h_i) &= h_i / (1 + h_i) \;\;   q_{hem} < 0 
   \nonumber\\
     f(h_i) &= 1  / (1 + h_i)  \;\;   q_{hem} > 0\end{aligned}

:math:`h_i` is the local ice thickness, and :math:`q_{hem}` is a tuning
constant which may have different values for the Northern and Southern
hemispheres. The coefficient :math:`A^n` ensures this adjustment only
occurs under sea ice covered ocean. The function :math:`f(h_i)` is
empirical, and is designed to ensure that the hemispheric adjustments
asymptote properly for very small and very large values of ice
thickness. For present-day climate simulations the values of
:math:`q_{hem}` which yield good control sea ice distributions are
+15\ :math:`W/m^2` and -10:math:`W/m^2` for the Northern and Southern
hemispheres respectively.

The adjusted :math:`Q^{n}` (:math:`Q^{n''}`) is then used to update all
ocean points due to deep ocean heat exchange and transport as:

.. math::

   T_o^{(n+1)''} = T_o^{(n+1)'} - \frac{Q^{n''} + A^n F_{oi}^n} 
   {(\rho_o C_o h_o )} \Delta t

where :math:`F_{oi}^{n}` is the energy flux associated with any ice melt
and shortwave radiation transmitted through the sea ice from the
previous time step.

The quantity :math:`F_{frz}^{n}` is nonzero only if the temperature of
the slab ocean falls below the freezing point:

.. math:: F_{frz}^{n+1} = (\rho_o C_o h_o) max(T_f - T_o^{(n+1)''},0)/ \Delta t

If :math:`F_{frz}^{n+1}` is nonzero, new ice forms over the ice-free
portion of the grid cell and :math:`T_o^{n+1}` is returned to the
freezing temperature:

.. math:: T_o^{(n+1)''} = max(T_o^{(n+1)''},T_f)

A renormalization is necessary to ensure energy is conserved when
:math:`Q` is adjusted as described above. We distinguish warm ocean as
those points for which :math:`T_o > 0^\circ`\ C. An adjustment for warm
ocean points is computed after all modifications to :math:`Q` are
completed. Let :math:`Q_o` be the original unadjusted :math:`Q`, and let
:math:`<Q_o>` be the global (area weighted) mean. The final (total)
:math:`Q` applied to warm ocean points is:

.. math:: Q''' = Q'' + [ (<Q_o>-<Q''>) (A_o/A_w) ]

where :math:`A_o` is the global area over all ocean, and :math:`A_w` the
corresponding area over warm ocean. Taking the global mean of the
bracketed quantity (which is zero over non-warm oceans) results in a
multiplicative factor :math:`(A_w/A_o)`. Thus, :math:`<Q'''> = <Q_o>`,
satisfying global energy conservation of :math:`Q` for every time step.
In practice, the bracket term adjustment is applied to warm ocean points
after the Q redistribution is completed.

Thermodynamic Sea Ice Model
---------------------------

After the slab ocean component computes the atmosphere-ocean heat fluxes
and updates :math:`T_o` and :math:`F_{frz}`, the thermodynamic sea ice
model takes the latter two variables as input and computes the
atmosphere-ice and ocean-ice heat fluxes and advances the state of the
sea ice, including snow depth, surface temperature, ice thickness, ice
fractional coverage, and internal energy profile in the ice. The physics
of the sea ice component model in |cam| are discussed in detail in the next
chapter.

Evaluation of the Ocean :math:`Q` Flux
--------------------------------------

The ocean :math:`Q` flux is generally evaluated using a |cam| control 
simulation driven by prescribed sea surface temperature and sea ice
distributions. Let

.. math:: F_{net} = FS - FL - LH - SH

over ocean (regardless of whether the ocean surface is open or ice
covered), for each of 12 ensemble mean months (n=1,...,12). The Q flux
distribution for each month n is then evaluated: (note that here we use
the |cam| sign convention on the Q flux).

.. math:: Q = Q_{ocean} - Q_{ice} - F_{net}

where:

.. math::

   Q_{ocean} = (\rho_o C_o h_o/\texttt{daysmonth}(m))
              {\{(1-A(m+1)) T_o(m+1) - (1-A(m-1)) T_o(m-1)\}}

.. math::

   Q_{ice} = L_i {\{A(m+1)h_i(m+1) -
                     A(m-1)h_i(m-1)\}}/\texttt{daysmonth}(m)

where :math:`\texttt{daysmonth}` is the number of days in each month,
:math:`L_i` is the latent heat of fusion for ice, and :math:`h_i` is the
regionally specified ice thickness. We then define an annual average
using the monthly mean data:

.. math:: \overline{Q} = \sum_{m=1,12} \texttt{daysmonth}(m) Q(m)/365

By definition

.. math:: \overline{Q_{ocean}} = 0

.. math:: \overline{Q_{ice}} = 0

so that

.. math:: \overline{Q} = -\overline{F_{net}}

Since :math:`F_{net}` is the monthly mean flux into the ocean directly
from the control, :math:`Q` must be constrained to ensure that the
actual :math:`Q` applied in the SOM configuration has the same annual
mean as :math:`-\overline{F_{net}}`. Otherwise, the application of the
:math:`Q` flux would introduce a source or sink of heat with respect to
the control.

The actual :math:`Q` applied in the SOM configuration is based on linear
interpolation between monthly means, taken as midpoints. Since the
months have different lengths, in general the annual mean of the
:math:`Q` flux applied to the SOM *will not* equal
:math:`-\overline{F_{net}}`. Thus, we must define another annual mean,
based on the time interpolated :math:`Q`, to ensure that the SOM applied
Q has the identical annual mean as the fluxes :math:`F_{net}` from the
control run.
