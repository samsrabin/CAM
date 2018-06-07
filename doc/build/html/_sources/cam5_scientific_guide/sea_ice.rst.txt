.. |cam| replace:: CAM5.0

.. _sea_ice:

Sea Ice Thermodynamics
======================

This chapter describes the physics of the sea ice thermodynamics
beginning with basic assumptions and followed by a description of the
fundamental equations, various parameterization, and numerical
approximations. The philosophy behind the design of the sea ice
formulation of |cam| is to use the same physics, where possible, as in the sea
ice model within CCSM, which is known as CSIM for community sea ice
model. The sea ice formulation in |cam| uses parameterizations from CSIM for
predicting snow depth, brine pockets, internal shortwave radiative
transfer, surface albedo, ice-atmosphere drag, and surface exchange
fluxes. The full CSIM is described in detail in an NCAR technical note
by :cite:`briegleb02`. The pieces of CSIM that are also used in |cam|
(without the flux coupler) are described here.

The features of the sea ice model that are used in depend on the
boundary conditions over ice-free ocean. If sea surface temperatures
(SSTs) are prescribed, then sea ice concentration and thickness are also
prescribed. In this case, the primary function of the sea ice model in |cam|
is to compute surface fluxes. However, if the slab ocean model is
employed, sea ice thickness and concentration are computed within |cam|.
These two types of surface boundary conditions within |cam| will be referred
to as uncoupled and coupled in this chapter.

Basic assumptions
-----------------

When |cam| is run uncoupled (i.e., without an ocean model), sea ice thickness
and concentration must be specified. Sea ice concentrations are known
with reasonable accuracy owing to satellite microwave instruments and
ship observations. However, no adequate measurements of thickness exist
to produce a comprehensive dataset. Therefore, when ice thickness must
be specified, the thickness of the ice covered portion of the grid cell
is fixed in space and time at 2 m in the Northern Hemisphere and 0.5 m
in the Southern Hemisphere. Ice concentrations are interpolated from
monthly input data, which may vary in space and time. [1]_

For either coupled or uncoupled integrations, snow depth on sea ice is
prognostic as snow accumulates when precipitation falls as snow, and it
melts when allowed by the surface energy balance. For uncoupled
simulations only, the maximum snow depth is fixed at 0.5 m. Rain has no
effect on sea ice or snow on sea ice in the model.

Fundamental Equations
---------------------

The method for computing the surface turbulent heat and radiative
exchange, evaporative flux, and surface drag is integrally coupled with
the formulation of heat transfer through the sea ice and snow. The
equation governing vertical heat transfer in the ice and snow, which
allows for internal absorption of penetrating solar radiation, is

.. math::
   :label: eq:heateq

   \rho c { \partial T \over  \partial t} = \left( { \partial  \over
   \partial z} k { \partial T \over \partial z} + Q_{SW} \right)

where :math:`\rho` is the density, :math:`c` is the heat capacity,
:math:`T` is the temperature, :math:`k` is the thermal conductivity,
:math:`Q_{SW}` is shortwave radiative heating, :math:`z` is the vertical
coordinate, and :math:`t` is time. Note that :math:`\rho`, :math:`c`,
and :math:`k` differ for snow and sea ice, and also the latter two
depend on temperature and salinity within the sea ice to account for the
behavior of brine pockets.

The boundary condition for the heat equation at the surface is

.. math::
   :label: eq:top

   
     F_{TOP}(T_s) = F_{SW}-I_{SW} + F_{LW} + F_{SH} + F_{LH} + k {dT
       \over dz}

where :math:`T_s` is the surface temperature, :math:`F_{SW}` is the
absorbed shortwave flux, :math:`I_{SW}` is the shortwave flux that
penetrates into the ice interior, :math:`F_{LW}` is the net longwave
flux, :math:`F_{SH}` is the sensible heat flux, and :math:`F_{LH}` is
the latent heat flux. All fluxes are taken as positive down. If
:math:`F_{TOP}(T_s=0) \ge 0`, then the surface is assumed to be melting
and a temperature boundary conditions (i.e., :math:`T_s=0`) is used for
the upper boundary with Eq. [eq:heateq]. However if
:math:`F_{TOP}(T_s=0) < 0` in Eq. [eq:top], then the surface is assumed
to be freezing and a flux boundary condition is used for Eq.
[eq:heateq], and Eqs. [eq:heateq] and [eq:top] are solved simultaneously
with :math:`F_{TOP}(T_s) = 0` in the latter.

Snow melt and accumulation is computed from

.. math::
   :label: eq:snow

   
     \rho_s {dh_s \over dt} = {-F_{TOP} \over L_i} + 
     {F_{LH} \over L_i+L_v} + F_{SNW}

where :math:`h_s` is the snow depth, :math:`\rho_s` is the snow density,
:math:`L_i` and :math:`L_v` are the latent heats of fusion and
vaporization, and :math:`F_{SNW}` is the snowfall rate (see Table [table:siphysconst] for values of constants).

When |cam| is coupled to the mixed layer ocean and the sea ice is snow-free,
sea ice surface melt is computed from

.. math::
   :label: eq:hicetop

   {dh_i \over dt} = {F_{TOP} \over q} + 
   {F_{LH} \over - q+\rho_i L_v}

where :math:`h_i` is the ice thickness, :math:`\rho_i` is the ice
density, and :math:`q` is the energy of melting of sea ice (:math:`q<0`
by definition, see section [bpocks] on brine pockets). Basal growth or
melt is computed from

.. math::
   :label: eq:hicebot
   
   {dh_i \over dt} = {F_{BOT} \over q} - {k \over q}{dT \over dz}

where :math:`F_{BOT}` is the heat flux from the ocean to the ice (see
section [Fbot-sec]). Finally an equation is needed to describe the
evolution of the ice concentration :math:`A`:

.. math::
   :label: eq:daice

   {dA \over dt} = {\mathcal A}

where :math:`\mathcal A` accounts for new ice formation over open water
and lateral melt (see section [lateralmelt])

Parameterizations of albedo, surface fluxes, brine pockets, and
shortwave radiative transfer within the sea ice are given next. Finally,
the numerical solution to Eq. [eq:heateq] is described. Numerical
methods for Eqs. [eq:top] –[eq:daice] are straight-forward and hence are
not described here.

[htb]

| \|l\|l\|l\| Symbol & Description & Value
| :math:`\rho_s` & Density of snow & 330 kg m\ :math:`^{-3}`
| :math:`\rho_i` & Density of ice & 917 kg m\ :math:`^{-3}`
| :math:`\rho_o` & Density of surface ocean water & 1026 kg
  m\ :math:`^{-3}`
| :math:`C_p` & Specific heat of atmosphere dry & 1005 J
  kg\ :math:`^{-1}` K\ :math:`^{-1}`
| :math:`C_{pwv}` & Specific heat of atmosphere water & 1810 J
  kg\ :math:`^{-1}` K\ :math:`^{-1}`
| :math:`C_o` & Specific heat of ocean water & 3996 J kg\ :math:`^{-1}`
  K\ :math:`^{-1}`
| :math:`c_s` & Specific heat of snow & 0 J kg\ :math:`^{-1}`
  K\ :math:`^{-1}`
| :math:`c_o` & Specific heat of fresh ice & 2054 J kg\ :math:`^{-1}`
  K\ :math:`^{-1}`
| :math:`z_i` & Aerodynamic roughness of ice & 5.0x10\ :math:`^{-4}` m
| :math:`z_{ref}` & Reference height for bulk fluxes & 10 m
| :math:`q_1(ice)`\ & saturation specific humidity constant & 11637800
| :math:`q_2(ice)`\ & saturation specific humidity constant & 5897.8
| :math:`k_{s}` & Thermal conductivity of snow & 0.31 W m\ :math:`^{-1}`
  K\ :math:`^{-1}`
| :math:`k_{o}` & Thermal conductivity of fresh ice & 2.0340 W
  m\ :math:`^{-1}` K\ :math:`^{-1}`
| :math:`\beta` & Thermal conductivity ice constant & 0.1172 W
  m\ :math:`^{-1}` ppt\ :math:`^{-1}`
| :math:`L_{i}` & Latent heat of fusion of ice & 3.340x10\ :math:`^5` J
  kg\ :math:`^{-1}`
| :math:`L_{v}` & Latent heat of vaporization & 2.501x10\ :math:`^6` J
  kg\ :math:`^{-1}`
| :math:`T_{melt}`\ & Melting temperature of top surface & 0
  :math:`^\circ`\ C
| :math:`\mu` & Ocean freezing temperature constant & 0.054
  :math:`^\circ`\ C ppt\ :math:`^{-1}`
| :math:`\sigma_{sb}`\ & Stefan-Boltzmann constant &
  5.67x10\ :math:`^{-8}` W m\ :math:`^{-2}` K\ :math:`^{-4}`
| :math:`\varepsilon`\ & Ice emissivity & 0.95
| :math:`\kappa_{vs}`\ & Ice SW visible extinction coefficient & 1.4
  m\ :math:`^{-1}`
| :math:`\kappa_{ni}`\ & Ice SW near-ir extinction coefficient & 17.6
  m\ :math:`^{-1}`

NOTE: CSIM in |cam| uses the shared constants defined in Appendix [physical\ :sub:`c`\ onstants].

Snow and Ice Albedo
-------------------

The albedo depends upon spectral band, snow thickness, ice thickness and
surface temperature. Snow and ice spectral albedos (visible :math:`=vs`,
wavelengths :math:`< 0.7\mu m` and near-infrared :math:`=ni`,
wavelengths :math:`>
0.7\mu m`) are distinguished, as both snow and ice spectral
reflectivities are significantly higher in the :math:`vs` band than in
the :math:`ni` band. This two-band separation represents the basic
spectral dependence. The near-infrared spectral structure, with
generally decreasing reflectivity with increasing wavelength (Ebert and
Curry 1993) is ignored. The zenith angle dependence of snow and ice is
ignored (Ebert and Curry 1993; Grenfell, Warren, and Mullen 1994), and
hence there is no distinction between downwelling direct and diffuse
shortwave radiation. The approximations made for the albedo are further
described by Briegleb et al. (2002).

Here we ignore the dependence of snow albedo on age, but retain the
melting/non-melting distinction and thickness dependence. Dry snow
spectral albedos are:

.. math::

   \alpha_{vsdf}^s(dry) = & {0.96}  \\
   \alpha_{nidf}^s(dry) = & {0.68}  

To represent melting snow albedos, the surface temperature is used.
Springtime warming produces a rapid transition from sub-zero to melting
temperatures, while late fall values transition more slowly to sub-zero
conditions. This is approximated by a temperature dependence out to
:math:`-1^\circ`\ C. If :math:`T_{s} \ge -1^\circ`\ C, then

.. math::

   \Delta T_s  =  & {T_{s} + 1.0}    \\
   \alpha_{vsdf}^s(melt) = & {\alpha_{vsdf}^s(dry) - 0.10 \Delta T_s}  \\
   \alpha_{nidf}^s(melt) = & {\alpha_{nidf}^s(dry) - 0.15 \Delta T_s}  

For bare non-melting sea ice thicker than 0.5 m, as is the case for all
sea ice prescribed in |cam|, the albedos are

.. math::

   \alpha_{vsdf}(dry) = & {0.73}  \\
   \alpha_{nidf}(dry) = & {0.33}  .

For bare melting sea ice, melt ponds can significantly lower the area
averaged albedo. This effect is crudely approximated by the following
temperature dependence:

.. math::

   \alpha_{vsdf}(melt) = & {\alpha_{vsdf}(dry) - 0.075 \Delta T_s }  \\
   \alpha_{nidf}(melt) = & {\alpha_{nidf}(dry) - 0.075 \Delta T_s }  

for :math:`T_{s} \ge -1^\circ`\ C.

The horizontal fraction of surface covered with snow is assumed to be

.. math::
   :label: horizfrac

   f_s = \frac{h_s}{h_s + 0.02}.

Finally, combining ice and snow albedos by averaging over the horizontal
coverage results in

.. math::

   \alpha_{vsdf} = & {\alpha_{vsdf}(1 - f_{s}) + f_{s} \alpha_{vsdf}^s}  \\
   \alpha_{nidf} = & {\alpha_{nidf}(1 - f_{s}) + f_{s} \alpha_{nidf}^s}  .

The same equations applies for direct albedos.

Ice to Atmosphere Flux Exchange
-------------------------------

Atmospheric states and downwelling fluxes, along with surface states and
properties, are used to compute atmosphere-ice shortwave and longwave
fluxes, stress, sensible and latent heat fluxes. Surface states are
temperature :math:`T_{s}` and albedos :math:`\alpha_{vsdr}`,
:math:`\alpha_{vsdf}`, :math:`\alpha_{nidr}`, :math:`\alpha_{nidf}` (see
section [albedo]), while surface properties are longwave emissivity
:math:`\varepsilon` and aerodynamic roughness :math:`z_i` (note that
these properties in general vary with ice thickness, but are here
assumed constant). Additionally, certain flux temperature derivatives
required for the ice temperature calculation are computed, as well as a
reference diagnostic surface air temperature.

The following formulas are for the absorbed shortwave fluxes and
upwelling longwave flux:

.. math::

   F_{SWvs} = &  F_{SWvsdr}(1 - \alpha_{vsdr}) + F_{SWvsdf}(1 - \alpha_{vsdf}) \\ 
   F_{SWni} = &  F_{SWnidr}(1 - \alpha_{nidr}) + F_{SWnidf}(1 -\alpha_{nidf})  \\
   F_{SW}   = &  F_{SWvsn} + F_{SWnin} \\
   F_{LWUP} = &  -\varepsilon\sigma_{sb} T_s^4+(1-\varepsilon)F_{LWDN} 

for :math:`T_{s}` in Kelvin and :math:`\sigma_{sb}` denotes the
Stefan-Boltzmann constant. The downwelling shortwave flux and albedos
distinguish between visible (:math:`vs, \lambda < 0.7\mu m`),
near-infrared (:math:`ni,
\lambda > 0.7\mu m`), direct (:math:`dr`) and diffuse (:math:`df`)
radiation for each category. Note that the upwelling longwave flux has a
reflected component from the downwelling longwave whenever
:math:`\varepsilon < 1`.

For stress components :math:`\tau_{ax}` and :math:`\tau_{ay}` and
sensible and latent heat fluxes the following bulk formulas are used
(Bryan et al. 1996):

.. math::
   :label: sibulkfluxes

   \tau_{ax} = & \rho_a r_{m} u^\ast u_a \\
   \tau_{ay} = & \rho_a r_{m} u^\ast v_a \\
   F_{SH} = & \rho_a c_a r_{h} u^\ast \left( \theta_a - T_{s} \right) \\
   F_{LH} = & \rho_a (L_i+L_v) r_{e}  u^\ast \left( q_a - {\overline q}^{*}  \right). 

The quantities from the lowest layer of the atmosphere include wind
components :math:`u_a` and :math:`v_a`, the density of air
:math:`\rho_a`, the potential temperature :math:`\theta_a`, and the
specific humidity :math:`q_a`. The surface saturation specific humidity
is

.. math:: 

   {\overline q}^{*} = (q_1/ \rho_a) e^{-q_2/T_{s}}

where the values of :math:`q_1` and :math:`q_2` were kindly supplied by
Xubin Zeng of the University of Arizona. The specific heat of the air in
the lowest layer is evaluated from

.. math::

   c_a = & C_p ( 1 + C_{pvir} {\overline q}^{*}) \\
   C_{pvir} = & (C_{pwv}/C_p) - 1 

where specific heat of dry air and water vapor are :math:`C_p` and
:math:`C_{pwv}`, respectively. Values for the exchange coefficients for
momentum, sensible and latent heat :math:`r_{m,h,e}` and the friction
velocity :math:`u^\ast` require further consideration.

The bulk formulas are based on Monin-Obukhov similarity theory. Among
boundary layer scalings, this is the most well tested (Large 1998). It
is based on the assumption that in the surface layer (typically the
lowest tenth of the atmospheric boundary layer), but away from the
surface roughness elements, only the distance from the boundary and the
surface kinematic fluxes are important in the turbulent exchange. The
fundamental turbulence scales that are formed from these quantities are
the friction velocity :math:`u^\ast`, the temperature and moisture
fluctuations :math:`\theta^\ast` and :math:`q^\ast` respectively, and
the Monin-Obukhov length scale :math:`L`:

.. math::

   u^\ast      = & r_{m} V_{mag}    \\
   \theta^\ast = & r_{h} (\theta_a - T_{s}) \\  
   q^\ast      = & r_{e} (q_a - {\overline q}^{*}))  \\
   L           = & u^{\ast 3} / (\kappa F)   

with

.. math:: 

   V_{mag} = \max(1.0,\sqrt{u_a^2 + v_a^2}),

to prevent zero or small fluxes under quiescent wind conditions,
:math:`\kappa` is von Karman’s constant (0.4), and :math:`F` is the
buoyancy flux, defined as:

.. math::

   F = \frac{u^\ast} {g} \left[ \frac{\theta^\ast}{\theta_{v}} 
      + \frac{q^\ast}{z_v^{-1}+q_a} \right]

with g the gravitational acceleration and the virtual potential
temperature :math:`\theta_{v} = \theta_a(1+z_vq_a)` where :math:`z_v=\rho_{wv}/\rho_a - 1`.

Similarity theory holds that the vertical gradients of mean horizontal
wind, potential temperature and specific humidity are universal
functions of stability parameter :math:`\zeta = z / L`, where :math:`z`
is height above the surface (:math:`\zeta` is positive for a stable
surface layer and negative for an unstable surface layer). These
universal similarity functions are determined from observations in the
atmospheric boundary layer (Hogstrom 1988) though no single form is
widely accepted. Integrals of the vertical gradient relations result in
the familiar logarithmic mean profiles, from which the exchange
coefficients can be defined, where :math:`\zeta = z_a / L`:

.. math::

   r_{m} = & r_0 \left\{1+\frac{r_0}{\kappa}\left[\ln(z_a/z_{ref})-\chi_m(\zeta)\right]\right\}^{-1} \\
   r_{h} = & r_0 \left\{1+\frac{r_0}{\kappa}\left[\ln(z_a/z_{ref})-\chi_h(\zeta)\right]\right\}^{-1} \\
   r_{e} = & r_{h} 

with the neutral coefficient

.. math:: r_0 = \frac{\kappa}{ln(z_{ref}/z_i)}.

The flux profile functions (integrals of the similarity functions
mentioned above) for momentum :math:`m` and heat/moisture :math:`h` are:

.. math:: \chi_m(\zeta) = \chi_h(\zeta) = -5\zeta

for stable conditions (:math:`\zeta > 0`). For unstable conditions
(:math:`\zeta < 0`):

.. math::

   \begin{aligned}
   \chi_m(\zeta) &=  \ln \{(1+X(2+X))(1+X^2)/8\} - 2 \tan^{-1}(X) + 0.5\pi \\
   \chi_h(\zeta) & = 2 \ln\{(1+X^2)/2\} \\*[-1.0em]
   \intertext{with} \nonumber\\*[-2.0em]
   X &= \left\{ \max((1-16\zeta)^{1/2}),1\right\}^{1/2}. \end{aligned}

The stability parameter :math:`\zeta` is a function of the turbulent
scales and thus the fluxes, so an iterative solution is necessary. The
coefficients are initialized with their neutral value :math:`r_0`, from
which the turbulent scales, stability, and then flux profile functions
can be evaluated. This order is repeated for five iterations to ensure
convergence to an acceptable solution.

The surface temperature derivatives required by the ice temperature
calculation are evaluated as:

.. math::

   \frac{dF_{LWUP}}{dT_{s}} &= -4\varepsilon\sigma_{sb} T_{s}^3 \\
   \frac{dF_{SH}}{dT_{s}} &= - \rho_a c_a r_{h} u^\ast \\
   \frac{dF_{LH}}{dT_{s}} &= - \rho_a L_s r_{e}  u^\ast \frac{d{\overline q}^{*}(T_{s})}{dT_{s}}

where the small temperature dependencies of :math:`c_a`, the exchange
coefficients :math:`r_{h}` and :math:`r_{e}` and velocity scale
:math:`u^\ast` are ignored.

For diagnostic purposes, an air temperature (:math:`T_{REF}`) at the
reference height of :math:`z_{2m}=2m` is computed, making use of the
stability and momentum/sensible heat exchange coefficients. Defining
:math:`b_m = \kappa / r_{m}`, and :math:`b_h = \kappa / r_{h}`, we have:

.. math::

   \ln_m = & \ln\{(1+z_{2m}/z_a)(e^{b_m}-1)\} \\
   \ln_h = & \ln\{(1+z_{2m}/z_a)(e^{b_m-b_h}-1)\}. 

For stable conditions (:math:`\zeta > 0`)

.. math::

   \begin{aligned}
    f_{int}&= (\ln_m-(z_{2m}/z_a)(b_m-b_h))/b_h \\
   \intertext{and for unstable conditions ($\zeta < 0$)}\nonumber\\*[-2.0em]
   f_{int}&= (\ln_m-\ln_h)/b_h \end{aligned}

where :math:`f_{int}` is bounded by 0 and 1. The resulting reference
temperature is:

.. math:: T_{ref} = T_{s} + (T_a - T_{s})f_{int}.

Ice to Ocean Flux Exchange
--------------------------

This section is only relevant when \cam is coupled to a slab ocean. When sea
ice is present, only a fraction of the melting potential from heat
stored in the ocean actually reaches the ice at the base and side. The
melting potential is

.. math:: F_{max} = - h_o \rho_o C_o (T_o-T_f)

where :math:`h_o`, :math:`\rho_o`, :math:`C_o`, and :math:`T_o` are the
ocean layer thickness, density, heat capacity, and temperature and
:math:`T_f` is the freezing temperature of the layer (assumed to be
-1.8:math:`^o`\ C).

Usually only a fraction of :math:`F_{max}` is available to melt ice at
the base and side, and these fractions are determined from
boundary-layer theories at the ice-ocean interfaces. However, it is
critical that the sum of the fractions never exceeds one, otherwise ice
formation might become unstable. Hence we compute the upper-limit
partitioning of :math:`F_{max}`, even though these amounts are rarely
reached. The partitioning assumes :math:`F_{oi}` is dominated by
shortwave radiation and that shortwave radiation absorbed in the ocean
surface layer above the mean ice thickness causes side melting and below
it causes basal melting:

.. math::

   f_{bot} = & {Re^{-h/\zeta_1} + (1-R)e^{-h/\zeta_2}} \\
   f_{sid} = & {1-f_{bot} }  

where :math:`R = 0.68`, :math:`\zeta_1=1.2~m^{-1}`,
:math:`\zeta_2=28~m^{-1}` (Paulson and Simpson 1983) and :math:`f_{bot}`
and :math:`f_{sid}` are the fractions of bottom and side melt flux
available, respectively. Thus the maximum fluxes available for melt are
:math:`f_{bot} F_{oi}` and :math:`f_{sid} F_{oi}`. The actual amount
used for bottom melting, :math:`F_{BOT}`, is based on boundary layer
theory of McPhee (1992):

.. math::
   :label: eq:fbot

   
   F_{BOT} = max(-\rho_o C_o c_h u^*(T_o - T_f), f_{bot} F_{max})

where the empirical drag coefficient :math:`c_h`\ =0.006 and the skin
friction speed :math:`u^* = 1` cm/s (Steele 1995).

The heat flux for lateral melt is the product of the vertically-summed,
thickness-weighted energy of melting of snow and ice :math:`E_{tot}`
with the interfacial melting rate :math:`M_a` and the total floe
perimeter :math:`p_f` per unit floe area :math:`A_f`. The interfacial
melting rate is taken from the empirical expression of Maykut and
Perovich (1987) based on Marginal Ice Zone Experiment observations:
:math:`M_a = m_1 (T_o - T_f)^{m_2}`, where
:math:`m_1=1.6\times10^{-6}`\ m s\ :math:`^{-1}` deg\ :math:`^{m_2}`
and :math:`m_2=1.36`. The lead-ice perimeter depends on the ice floe
distribution and geometry. For a mean floe diameter :math:`d` and number
of floes :math:`n_f`, :math:`p_f
= n_f \pi d` and the floe area :math:`A_f = \eta_{lm} d^2` (Rothrock and
Thorndike 1984). Thus the heat flux for lateral melt is
:math:`E_{tot}(p_f/A_f)M_a`, so that the actual amount used is:

.. math::
   :label: FSID

   
   F_{SID} = max(\frac{E_{tot} \pi}{\eta_{lm} d} m_1 (T_o - T_f)^{m_2}, 
   f_{sid} F_{max})

where :math:`\eta_{lm}=0.66` (Rothrock and Thorndike 1984). Based
partially on tuning and partially on the results of floe distribution
measurements, the mean floe diameter of :math:`d`\ =300 m was chosen.
The ice area, volume, snow volume, and ice energy are all reduced by
side melt in time :math:`\Delta t` by the fraction
:math:`R_{side} = \vert \frac{F_{SID}\Delta t}{E_{tot}} \vert`.

The heat flux that is actually used by the ice model is then:

.. math:: F_{BOT} + F_{SID} \le F_{max}.

The net flux exchanged between ocean and ice :math:`F_{oi}` also
includes the shortwave flux transmitted to the ocean through sea ice

.. math:: F_{SWo}  = I_{0vs} e^{-\kappa_{vs} h} +I_{0ni} e^{-\kappa_{ni} h}

(see Eq. [eq:swtran]). Hence

.. math::
   :label: Focnice

   
   F_{oi}=F_{SWo}+F_{BOT} + F_{SID}.

Brine Pockets and Internal Energy of Sea Ice
--------------------------------------------

Shortwave radiative heating within the sea ice and conduction warms the
sea ice and opens brine pockets, melting the ice internally and storing
latent heat. This storage of latent heat is accounted for explicitly by
using a heat capacity and thermal conductivity that depend on
temperature and salinity following the work of Maykut and Untersteiner
(1971) and Bitz and Lipscomb (1999). The equation for the heat capacity
for sea ice :math:`c` was first postulated by Untersteiner (1961) and
then later derived from first principles by Ono (1967):

.. math::
   :label: eq:ci

   
   c(T,S) = c_o + \frac{L_i \mu S}{T^2},

where :math:`c_o` is the heat capacity for fresh ice, :math:`S` is the
sea ice salinity, :math:`T` is the temperature, and :math:`\mu` is an
empirical constant relating the freezing temperature of sea water
linearly to its salinity (:math:`T_f=-\mu S`).

Equation [eq:ci] can be multiplied by the sea ice density and integrated
to give the amount of energy :math:`Q` required to raise the temperature
of a unit volume of sea ice from :math:`T` to :math:`T'`:

.. math::
   :label: eq:Q

   
   Q(S,T,T')=\rho_i c_o(T'-T)-\rho_i L_o\mu S \left({1 \over T'} - {1 \over
       T}\right).

If we take :math:`T'` to be the melting temperature of ice with salinity
:math:`S`, then at :math:`T'` sea ice consists entirely of brine; that
is, the brine pockets have grown to encompass the entire mass of ice.
The amount of energy needed to melt a unit volume of sea ice of salinity
:math:`S` at temperature :math:`T`, resulting in meltwater at
:math:`T_f`, is equal to

.. math::
   :label: eq:q

   
   q(S,T)=\rho_i c_o(-\mu S-T)+\rho_i L_o \left(1+{\mu S \over T}\right).

:math:`q` is referred to as the *energy of melting* of sea ice, and it
appears in Eqs. [eq:hicetop] and [eq:hicebot].

The thermal conductivity for sea ice :math:`k` is

.. math:: k(S,T) = k_o + \frac {\beta S} {T}

where :math:`k_o` and :math:`\beta` are empirical constants from
Untersteiner (1961).

The vertical salinity profile is prescribed based on the work of Maykut
and Untersteiner (1971) to be

.. math::

   S(w) = 1.6 \left[ 1 - \cos \left( 
           \pi w^{\frac{0.407}{0.573 + w}} \right) \right]

with the normalized coordinate :math:`w = z/h`. This results in a
profile that varies from :math:`0` ppt at ice surface increasing to
:math:`3.2` ppt at ice base. Snow is assumed fresh.

Shortwave radiative heating within the sea ice :math:`Q_{SW}` is equal
to the vertical gradient of the radiative transfer within the sea ice:

.. math::
   :label: eq:swtran

    
     Q_{SW} = - \frac{d}{dz} \{ I_{0vs} e^{-\kappa_{vs} z} + 
                                I_{0ni} e^{-\kappa_{ni} z} \}

where :math:`I_{0vs}` and :math:`I_{0ni}`, the visible and near infrared
radiation fluxes that penetrate the surface, are reduced according to
Beer’s law with the sea ice spectral extinction coefficients
:math:`\kappa_{vs}` and :math:`\kappa_{ni}`, respectively. For
simplicity no shortwave radiation is allowed to penetrate through snow
and all of the near-infrared radiation and 30% of the visible radiation
is assumed to be absorbed at the surface of sea ice (Gary Maykut,
personal communication):

.. math::

   \begin{aligned}
   I_{0vs} &= 0.70 F_{SWvsn} (1-f_{s}) \\
   I_{0ni} &= 0.0\end{aligned}

where :math:`f_{s}` is the horizontal fraction of surface covered by
snow (see Eq. [horizfrac]).

Open-Water Growth and Ice Concentration Evolution
-------------------------------------------------

When coupled to a mixed layer ocean, the ice model must account for new
ice growth over open water and other processes that alter the lateral
sea ice coverage. New ice growth occurs whenever the surface layer in
the ocean is at the freezing temperature and the fluxes would draw
additional heat out of the ocean (see Eq. [6.a.1]). In this case the
additional heat comes from freezing sea water, as the ocean cannot
supercool in this model. Hence

.. math::
   :label: hnew

   
   q_f {\partial h_{new} \over \partial t} = F_{frz} \ (1-A)

where :math:`q_f` is the energy of melting for new ice growth (assuming
the salinity is 4psu and the new ice temperature is -1.8:math:`^o`\ C),
:math:`h_{new}` is the thickness of the new ice, and :math:`F_{frz}` is
the additional heat lost by slab ocean once it reaching the freezing
point (see section 5.1). When new ice grows over open water, it is
recombined with the rest of the ice in the grid cell by first reshaping
the new ice volume so its thickness is at least 15 cm - this recreates
ice-free ocean if the thickness was below 15 cm. Then the new ice is
added to the old ice in the grid cell and a new thickness and
concentration are computed by conserving ice volume.

In motionless sea ice model, such as this one, open water is not created
by deformation as in nature, and hence the ice concentration would tend
to 0 or 100% unless open water production is parameterized somehow. A
typical method is to assume the ice thickness on a subgrid-scale is
linearly distributed between 0 and :math:`2h`, so that when ice melts
vertically, it also reduces the concentration:

.. math::
   :label: dA1

   
   \left(A-{\partial A \over \partial t}\right)^2
   = {A^2 \over h_i} \left( h - {\partial h_i \over \partial t} \right)

The ice concentration is also reduced by a lateral heat flux from the
ocean (see Eq. [FSID]):

.. math::
   :label: dA2

   
   {\partial A \over \partial t} = A {F_{SID} \over E_{TOT}}

although it is typically only a small contribution to the concentration
tendency.

It is not possible to combine Eqs. [hnew]–[dA2] to make a single
analytic expression for :math:`\mathcal A` in Eq. [eq:daice]. Instead the
model using time splitting to solve the three equations independently.

Snow-Ice Conversion
-------------------

Snow to ice conversion occurs if the snow layer overlying the sea ice
becomes thick enough to depress the snow-ice interface below freeboard
(the ocean surface). This process is only accounted for when |cam| is coupled
to a mixed layer ocean, otherwise the snow depth is merely capped at 0.5
m. The interface height is:

.. math:: z_{int} = h - (\rho_s h_s + \rho_i h) / \rho_o.

If :math:`z_{int} < 0`, then an amount of snow equal to
:math:`-z_{int} \rho_i / \rho_s` is removed from the snow layer and
added to the ice. It is assumed that ocean water floods the depressed
snow, and then converts it into ice of thickness :math:`-z_{int}`. The
energy of melting of the newly formed ice is:
:math:`q_{flood} = q_s \rho_i / \rho_s`. Note that such conversion is
assumed to occur with no heat or salt exchange with the ocean.

Numerics
--------

The heat content change within the sea ice over the time interval
:math:`t` to :math:`t'` corresponding to temperatures :math:`T` and
:math:`T'`, respectively, allowing for temperature dependent heat
capacity, thermal conduction (see section [bpocks]) and internal
absorption of penetrating solar radiation, is given by:

.. math::

   \int^{T'}_T \rho_i c dT = 
      \rho_i c_o(T'-T) \left(1 + {L_i\mu S \over  c_o T' T} \right) 
     =\int^{t'}_t \left( { \partial  \over
     \partial z} k { \partial T \over \partial z} + Q_{SW} \right) dt

The heat equation is discretized using a backwards-Euler, space-centered
scheme. Using a staggered grid with :math:`T_l` representing the layer
temperature and :math:`k_l` representing conductivity at the layer
interfaces, for interior layers we have

.. math::
   :label: num:1

    
    \rho_i c_o(T_l^{m+1}  -  T_l^m)
     \left(1 + {L_i\mu S_l \over  c_o T_l^{m+1} T_l^m} \right) = 
      { \Delta t  \over  \Delta h^m  } \left( 
       k_{l+1}^m { T_{l+1}^{m+1} - T_l^{m+1}  \over  \Delta h^m  } 
       - k_l^m   { T_l^{m+1} - T_{l-1}^{m+1}  \over  \Delta h^m  } 
       +  I^m_l \right),

where :math:`\Delta h^m =h^m/L`, the conductivity is

.. math::

   k_l^m = k\left({ S_l+S_{l+1} \over 2 } ,
            { T_l^m+T_{l+1}^m \over 2 }  \right),

and the absorbed solar radiation is

.. math::

   I_l^m  = I_{0vs} (e^{-\kappa_{vs} l \Delta h^m} - 
                     e^{-\kappa_{vs} (l+1) \Delta h^m}) +
            I_{0ni} (e^{-\kappa_{ni} l \Delta h^m} - 
                     e^{-\kappa_{ni} (l+1) \Delta h^m}).

.. figure:: figures/figure6-1.jpg
   :align: center
	   
   Vertical grid of the sea ice (a) when snow is present and (b)
   when the ice is snow free; :math:`\Delta h` is the thickness of an
   ice layer and :math:`h_s` is the thickness of the snow layer. The
   surface temperature in either case is :math:`T_s`. Modified from Bitz
   and Lipscomb (1999).

See Figure [fig:stag] for a diagram on the vertical level structure.

For a purely implicit backward scheme, :math:`k` should be evaluated at
the :math:`m+1` time level. However, when :math:`k` is evaluated at time
level :math:`m`, experiments show that the solution is stable and
converges to the same solution one gets when evaluating :math:`k` at
:math:`m+1`.

The discrete heat equation for the surface layers is modified slightly
from :eq:`num:1` to maintain second-order accuracy for :math:`\partial{T} \over \partial{z}`. 
The equation for the bottom layer (:math:`l=L`) is

.. math::
   :label: num:1b

   \rho_i c_o&(T_L^{m+1}- T_L^m)
     \left(1 + {L_i\mu S_L \over  c_o T_L^{m+1} T_L^m} \right) =\\ 
     & { \Delta t  \over  \Delta h^m  } 
       \left(
       3 k_{L+1}        { T_b - T_L^{m+1} \over \Delta h^m    } -
    {1 \over 3} k_{L+1} { T_b - T_{L-1}^{m+1} \over \Delta h^m}
      - k_L^m             { T_L^{m+1} - T_{L-1}^{m+1}  \over  \Delta h^m  } 
             +  I^m_L \right), 

where the :math:`L+1` interface in contact with the underlying ocean is
assumed to be at temperature :math:`T_b=-1.8^\circ`\ C, and where the
conductivity is simply :math:`k_{L+1} = k(S_b,T_b)`. The equations for
the top surface depend on the surface conditions, of which there are
four possibilities, as outlined in Table [tab:bc].

+------------+--------------------+-----------+
|            | snow accumulated   | melting   |
+============+====================+===========+
| case I     | yes                | no        |
+------------+--------------------+-----------+
| case II    | no                 | no        |
+------------+--------------------+-----------+
| case III   | yes                | yes       |
+------------+--------------------+-----------+
| case IV    | no                 | yes       |
+------------+--------------------+-----------+

Table: Top Surface Boundary Cases

Case I: Snow accumulated with no melting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The discrete heat equation for the uppermost layer (i.e, the snow layer)
is

.. math::
   :label: num:1t0

    
    \rho_s c_s(T_0^{m+1} - T_0^m) 
     =  { \Delta t  \over  h_s^m }  
   \left[ k_1^m { T_1^{m+1} - T_0^{m+1} \over (\Delta h^m+h_s^m)/2} 
      - \alpha k_s { T_0^{m+1} - T_s^{m+1} \over h_s^m  } 
         - \beta k_s { T_1^{m+1} - T_s^{m+1} \over h_s^m  } 
            \right].

The heat equation solver is formulated for the general case where the
heat capacity of snow :math:`c_s` may be specified, although it is taken
to be :math:`0`. The parameters :math:`\alpha` and :math:`\beta` are
defined to give second-order accurate spatial differencing for
:math:`\partial T / \partial z` across the changing layer spacing at the
snow/ice boundary;

.. math::

   \alpha & = { h_s^m + \Delta h^m/2 \over h_s^m/2 }~{2 \over h_s^m + \Delta h^m} h_s^m \\
   \beta  & = {-h_s^m/2 \over h_s^m + \Delta h^m/2 }~{2 \over h_s^m + \Delta h^m} h_s^m.

The conductivity at the snow–ice interface is found by equating
conductive fluxes above and below the interface;

.. math::

   k_1^m={2 k_s k(S_1,T_1^m) \over h_s^m k(S_1,T_1^m) + \Delta h^m k_s} ~
      {h_s^m+\Delta h^m \over 2}.

Because :math:`T_s` is below melting, a flux boundary condition is
used, and an additional equation is required in the coupled set:

.. math::
   :label: num:1surf

    
   F_o(T_s^{m+1})+\alpha k_s { T_0^{m+1} - T_s^{m+1} \over h_s^m }
         +\beta k_s { T_1^{m+1} - T_s^{m+1} \over h_s^m }= 0,

where :math:`F_o(T_s^{m+1})` is the sum of all terms on the right-hand
side of Eq. [eq:top] except :math:`k \partial T / \partial z`. The net
surface flux :math:`F_o(T_s^{m+1})` is approximated as linear in
:math:`T_s^{m+1}`; thus

.. math::
   :label: topboundary

   
   F_o(T_s^{m+1})\sim F_o(T_s^m)+\left.{\partial F_o \over \partial
       T_s}\right|_{T_s^m}(T_s^{m+1}-T_s^m).

with

.. math::

   \left.{\partial F_o \over \partial T_s}\right|_{T_s^m} =
   \left.{\partial F_{LWUP} \over \partial T_s}\right|_{T_s^m} +
   \left.{\partial F_{SH} \over \partial T_s}\right|_{T_s^m} +
   \left.{\partial F_{LH} \over \partial T_s}\right|_{T_s^m}

To simplify our set of equations, we define

.. math::
   :label: eq:chat

   
   \hat c_l^{m+1}= \rho_i \left( c_o + {L_i \mu S \over T_l^{m+1} T_l^m}\right),

where the hat implies that :math:`\hat c_l^{m+1}` depends on
:math:`T_l^m` as well as on :math:`T_l^{m+1}`, and

.. math::
   :label: eq:eta

   
   \chi_l^{m+1}= {\Delta t \over \Delta h^m } {1 \over \hat c_l^{m+1}}.

Also, let

.. math::
   :label: eq:ktrick

   \begin{aligned}
   
   k_l&= {k_l^m \over \Delta h^m}.\\*[-1.0em]
   \intertext{for $l \ge 2$ and} \nonumber\\*[-2.0em]
   k_0&= {k_s \over h_s^m} \\
   k_1&= {k_1^m \over (\Delta h^m + h_s^m)/2}\end{aligned}

and suppress the index :math:`m` for :math:`I_l^m`, so that for
interior layers (:math:`l=1...L-1`),

.. math::

   \begin{aligned}
   T_l^{m+1}-T_l^m&=\chi_l^{m+1}\left[k_{l+1}(T_{l+1}^{m+1}-T_l^{m+1})
                                        -k_l(T_l^{m+1}-T_{l-1}^{m+1})+I_l\right]\\
   \intertext{and at the bottom layer}\nonumber\\*[-1.0em]
          T_L^{m+1}-T_L^m&=\chi_L^{m+1}\biggl[3k_b(T_b-T_L^{m+1})
                              -{1 \over 3}k_b(T_b-T_{L-1}^{m+1})  
                    & \ \ \ \ \ \ \ \ \ \ \ \   
                               -k_L(T_L^{m+1}-T_{L-1}^{m+1})+I_L\biggr] \end{aligned}

where :math:`k_b = k_{L+1} / \Delta h^m`. The equation describing the
snow layer is written

.. math::
   :label: toplayerI

   
   \rho_s c_s (T_0^{m+1}-T_0^m)={\Delta t \over h_s^m } 
                     \left[ k_1(T_1^{m+1}-T_0^{m+1})
                     -\alpha k_0(T_0^{m+1}-T_s^{m+1})
                     -\beta  k_0(T_1^{m+1}-T_s^{m+1}) \right].

Finally, the flux boundary condition becomes

.. math::

   F_o(T_s^m)+ \left. {\partial F_o \over \partial T_s} \right|_{T_s^m}
         (T_s^{m+1}-T_s^m) =
    -\alpha k_0(T_0^{m+1}-T_s^{m+1}) -\beta k_0(T_1^{m+1}-T_s^{m+1}).

The complete set of coupled equations for case I can be written with all
of the terms that explicitly depend on temperature at the :math:`m+1`
time step gathered on the right-hand side:

.. math::
   :label: setI

   -F_o(T_s^m)+ \left.{\partial F_o \over 
   \partial T_s}\right|_{T_s^m}T_s^m &=
   T_s^{m+1}\left(\left.{\partial F_o \over \partial T_s}
   \right|_{T_s^m}-\alpha k_0 - \beta k_0 \right) \\
   & \hspace{0.5cm} + T_0^{m+1} \alpha k_0 + T_1^{m+1} \beta k_0 \\
   \rho_s c_s T_0^m  &=
   T_s^{m+1}\left( -{\Delta t \over h_s^m } \right) (\alpha k_0 
   +  \beta k_0) \\
   & \hspace{0.5cm}  + T_0^{m+1}\left( \rho_s c_s 
   + {\Delta t \over h_s^m }  (\alpha k_0+k_1) \right) \\
   & \hspace{0.5cm}  + T_1^{m+1}{\Delta t \over h_s^m } (\beta k_0-k_1) \\
   T_l^m + \chi_l^{m+1} I_l &=
   T_{l-1}^{m+1}(-\chi_l^{m+1} k_l) \\
   & \hspace{0.5cm} + T_l^{m+1}(1+\chi_l^{m+1} k_l + \chi_l^{m+1} k_{l+1} ) \\
   & \hspace{0.5cm} + T_{l+1}^{m+1}(-\chi_l^{m+1} k_{l+1})  \\
   T_L^m + \chi_L^{m+1} I_L + {8 \over 3} \chi_L^{m+1} k_bT_b &=
   T_{L-1}^{m+1}\left(-{1 \over 3}\chi_L^{m+1} k_b -
   \chi_L^{m+1} k_L \right) \\
   & \hspace{0.5cm} + T_L^{m+1}(1+3 \chi_L^{m+1} k_b + \chi_L^{m+1} k_L ). \\

These equations are subsequently related to the following abbreviated
form

.. math::

   r_s &= T_s^{m+1} b_s + T_0^{m+1}c_s+ T_1^{m+1}d_s \\
   r_0 &= T_s^{m+1} a_0 + T_0^{m+1}b_0+ T_1^{m+1}c_0 \\
   r_1 &= T_0^{m+1} a_1 + T_1^{m+1}b_1+ T_2^{m+1}c_1 \\
   & \vdots \\
   r_L &= T_{L-1}^{m+1} a_L + T_L^{m+1}b_L. 

The first two rows can be combined to eliminate the coefficient on
:math:`T_1^{m+1}` in the first row, allowing the set to be written in
tridiagonal form:

.. math::

   \begin{array}{l l l}
    r = \left[ \begin{array}{c}
                   r_s c_0 - r_0 d_s \\
                   r_0 \\
                   r_1 \\
                  \vdots     \\
               \end{array}
        \right]
   &{\mbox{\hspace{5pt}}}
    A= \left[ \begin{array}{cccc}
                    b_s c_0 - a_0 d_s & c_s c_0 - b_0 d_s &      &     \\
                    a_0               &  b_0              & c_0  &     \\
                                      &  a_1              & b_1  & c_1 \\
                                      &                   &      & \ddots  \\
               \end{array} \right]
   &{\mbox{\hspace{5pt}}}
    T = \left[ \begin{array}{c}
                  T_s^{m+1} \\
                  T_0^{m+1} \\
                  T_1^{m+1} \\
                  \vdots     \\
               \end{array}
        \right].
   \end{array}

Because the matrix A depends on :math:`\chi_l^{m+1}`, which in turn
depends on :math:`T_l^{m+1}`, the system of equations is solved
iteratively. An initial guess is used for the temperature dependence of
:math:`\chi_l^{m+1}`, and then :math:`\chi_l^{m+1}` is updated
successively after each iteration. Under most conditions the method
approaches a solution in less than four iterations with a maximum error
tolerance of :math:`\Delta T_{err}` for :math:`T_l` with an initial
guess of :math:`T_l^{m+1}=T_l^m`.

Case II: Snow free with no melting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nearly the same method applies when the ice is snow free, except one
less equation is needed to describe the evolution of the temperature
profile. The equation for the uppermost ice layer is written

.. math::
   :label: num:1ti

   \rho_i c_o(& T_1^{m+1} - T_1^m)  
   \left(1 + {L_i\mu S_1 \over  c_o T_1^{m+1} T_1^m} \right) \\ 
   &= { \Delta t  \over  \Delta h^m  } 
   \left( 
   k_2^m { T_2^{m+1} - T_1^{m+1}  \over \Delta h^m } 
   -3 k_1^m { T_1^{m+1} - T_s^{m+1} \over \Delta h^m  } 
   +{1 \over 3} k_1^m { T_2^{m+1} - T_s^{m+1} \over \Delta h^m } 
   +  I^m_1 \right),  

where :math:`k_1^m=k(S_1,T_1^m)`. After the definitions from Eqs.
[eq:chat]–[eq:ktrick] are applied, Eq. [num:1ti] becomes

.. math::
   :label: toplayerII

   
   T_1^{m+1}-T_1^m=\chi_1^{m+1}\left[k_2(T_2^{m+1}-T_1^{m+1})
                                -3k_1(T_1^{m+1}-T_s^{m+1})
                        +{1 \over 3}k_1(T_2^{m+1}-T_s^{m+1})+I_1^m\right].

The flux boundary condition follows after linearizing
:math:`F_o(T_s^{m+1})` in :math:`T_s^{m+1}`:

.. math::

   F_o(T_s^m)+\left.{\partial F_o \over \partial T_s}\right|_{T_s^m}
        (T_s^{m+1}-T_s^m) =
       -3k_1(T_1^{m+1}-T_s^{m+1}) +{1 \over 3} k_1(T_2^{m+1}-T_s^{m+1}).

The complete set of coupled equation includes Eqs. [setI] for layers 2
to L with the following two equations for the surface and upper ice
layer:

.. math::
   :label: setII

   -F_o(T_s^m)+\left.{\partial F_o \over \partial T_s}\right|_{T_s^m} T_s^m &=
   T_s^{m+1}\left(\left.{\partial F_o \over \partial T_s}\right|_{T_s^m}
   -k_1 {8 \over 3}\right) + T_1^{m+1}3 k_1 + T_2^{m+1}( -k_1/3 ) \\
   T_1^m + \chi_1^{m+1} I_1^m &=
   T_s^{m+1}\left(-\chi_1^{m+1} k_1 {8 \over 3}\right) \\
   & + T_1^{m+1}(1+\chi_1^{m+1} k_2 + 3 \chi_1^{m+1} k_1 ) \\
   & + T_2^{m+1}(-\chi_1^{m+1} k_2 - {1 \over 3}\chi_1^{m+1} k_1), 

which can be written

.. math::
   :label: reqATII

   r_s &= T_s^{m+1} b_s + T_1^{m+1}c_s+ T_2^{m+1}d_s \\
   r_1 &= T_s^{m+1} a_1 + T_1^{m+1}b_1+ T_2^{m+1}c_1. 

These two equations can be combined to eliminate the coefficient on
:math:`T_2^{m+1}`, allowing the set to be written in tridiagonal form:

.. math::

   \begin{array}{l l l}
    r = \left[ \begin{array}{c}
                   r_s c_1 - r_1 d_s \\
                   r_1 \\
                   r_2 \\
                  \vdots     \\
               \end{array}
        \right]
   &{\mbox{\hspace{9pt}}}
    A= \left[ \begin{array}{cccc}
                    b_s c_1 - a_1 d_s & c_s c_1 - b_1 d_s &      &     \\
                    a_1               &  b_1              & c_1  &     \\
                                      &  a_2              & b_2  & c_2 \\
                                      &                   &      & \ddots  \\
               \end{array} \right]
   &{\mbox{\hspace{5pt}}}
    T = \left[ \begin{array}{c}
                  T_s^{m+1} \\
                  T_1^{m+1} \\
                  T_2^{m+1} \\
                  \vdots     \\
               \end{array}
        \right].
   \end{array}

As for case I, this system of equations must be solved iteratively.

Case III: Snow accumulated with melting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Case III describes melting conditions in the presence of a snow layer at
the surface. Here a temperature boundary condition is used, which
simplifies the solution because the first row in Eqs. [setI] is not
needed and :math:`T_s=T_{melt}=0^\circ`\ C in the second row. Hence the
complete set of coupled equations is identical to Eqs. [setI] for layers
1 to L, with the addition of an equation for the snow layer,

.. math::

   \rho_s c_s T_0^m + T_{melt} {\Delta t \over h_s } 
         (\alpha + \beta)k_0 =
               T_0^{m+1}\left[ \rho_s c_s + {\Delta t \over h_s }
                      (k_1+\alpha k_0 ) \right]
             - T_1^{m+1} {\Delta t \over h_s } (k_1-\beta k_0).

This set of equations can be written in tridiagonal form, without the
need to eliminate any terms, as was required in cases I and II. However,
the solution must still be iterated.

Case IV: No snow with melting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like case III, case IV describes melting conditions, but here the sea
ice is snow free. Hence, the first two rows of Eqs. [setI] are not
needed, and :math:`T_s=T_{melt}` for :math:`l=1`. The set of coupled
equations comprises those from Eqs. [setI] for layers 2 to L and the
following equation for layer 1:

.. math::

   T_1^m + \chi_1^{m+1} I_1^m + T_{melt} \chi_1^{m+1} k_1 {8 \over 3} = 
             T_1^{m+1}\left(1+\chi_1^{m+1} k_2 + 3 \chi_1^{m+1} k_1 \right)
           + T_2^{m+1}\left(-\chi_1^{m+1} k_2 - 
             {1 \over 3}\chi_1^{m+1} k_1 \right).

As in case III, this set of equations can immediately be written in the
tridiagonal form and solved iteratively.

Temperature Adjustment Due to Melt/Growth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: figures/figure6-2.jpg
   :align: center

   Diagram showing energy content before (a) and after (b)
   changing the layer spacing for an ice model with four vertical layers
   that experiences melt at the top surface and growth at the bottom
   surface. From Bitz (2000)

The energy of melting of the ice and snow layers needs to be adjusted
when the layer spacing changes after growth/melt,
evaporation/sublimation, and flooding (see Figure [fig:adjust]). This
calculation is only made when |cam| is coupled to a mixed layer ocean. The
adjusted energy of melting is

.. math::
   :label: eq:adjust

   
   q_l'= \begin{cases} 
      \sum_{k=1}^L w_{k,1} q_k - q_{\rm flood} {z_{int} \over \Delta h'} ; & l=1 \\
      \sum_{k=1}^L w_{k,l} q_k; & 1<l<L, \\
      \sum_{k=1}^L w_{k,L} q_k + q_b 
        {\rm max}({\left. \delta h \right|_{\rm basal} \over \Delta
          h'},0); & l=L \end{cases}

where :math:`w_{k,l}` are weights computed from the relative overlap of
layer :math:`l` with each layer :math:`k` from the old layer spacing and
:math:`\Delta h'` is the new layer spacing.

.. [1]
   Mid-month concentrations are input and then interpolated to daily
   values. The input data are constructed to correctly recover the
   observed monthly means value using the method of Taylor, Williamson,
   and Zwiers (2001)
