.. |cam| replace:: CAM5.0

.. _extensions:

Extensions to CAM

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
