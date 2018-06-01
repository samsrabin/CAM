.. _model_physics:

.. |cam| replace:: CAM6.0

Model Physics
=============

As stated in chapter [chap:coupling], the total parameterization package
in |cam| consists of a sequence of components, indicated by

.. math::

   P = \{ M,R,S,T \} ~,

where :math:`M` denotes (Moist) precipitation processes, :math:`R`
denotes clouds and Radiation, :math:`S` denotes the Surface model, and
:math:`T` denotes Turbulent mixing. Each of these in turn is subdivided
into various components: :math:`M` includes an optional dry adiabatic
adjustment normally applied only in the stratosphere, moist penetrative
convection, shallow convection, and large-scale stable condensation;
:math:`R` first calculates the cloud parameterization followed by the
radiation parameterization; :math:`S` provides the surface fluxes
obtained from land, ocean and sea ice models, or calculates them based
on specified surface conditions such as sea surface temperatures and sea
ice distribution. These surface fluxes provide lower flux boundary
conditions for the turbulent mixing :math:`T` which is comprised of the
planetary boundary layer parameterization, vertical diffusion, and
gravity wave drag.

The updating described in the preceding paragraph of all variable except
temperature is straightforward. Temperature, however, is a little more
complicated and follows the general procedure described by Boville and
:cite:`boville03` involving dry static energy. The state variable
updated after each time-split parameterization component is the dry
static energy :math:`s_i`. Let :math:`i` be the index in a sequence of
:math:`I` time-split processes. The dry static energy at the end of the
:math:`i`\ th process is :math:`s_i`. The dry static energy is updated
using the heating rate :math:`Q` calculated by the :math:`i`\ th
process:

.. math:: s_i = s_{i-1} + \left(\Delta t\right) Q_i(s_{i-1},T_{i-1},\Phi_{i-1},q_{i-1}, ...)

In processes not formulated in terms of dry static energy but rather in
terms of a temperature tendency, the heating rate is given by
:math:`Q_i = \left( T_i - T_{i-1} \right) / \left( C_p \Delta t \right)`.

The temperature, :math:`T_i`, and geopotential, :math:`\Phi_i`, are
calculated from :math:`s_i` by inverting the equation for :math:`s`

.. math:: s = C_pT + gz = C_pT + \Phi

with the hydrostatic equation

.. math:: \Phi_k = \Phi_s + R\sum_{l=k}^{K} H_{kl}{T_v}_l

substituted for :math:`\Phi`. The temperature tendencies for each
process are also accumulated over the processes. For processes
formulated in terms of dry static energy the temperature tendencies are
calculated from the dry static energy tendency. Let
:math:`\Delta T_i / \Delta t` denote the total accumulation at the end
of the :math:`i`\ th process. Then

.. math::

   \frac{\Delta T_i}{\Delta t} = \frac{\Delta T_{i-1}}{\Delta t}
   + \frac{\Delta s_i}{\Delta t} / C_p

.. math::

   \frac{\Delta s_i}{\Delta t} / C_p =
   \frac{\left( s_i - s_{i-1}\right)}{\Delta t} / C_p

which assumes :math:`\Phi` is unchanged. Note that the inversion of
:math:`s` for :math:`T` and :math:`\Phi` changes :math:`T` and
:math:`\Phi`. This is not included in the
:math:`{\Delta T_i / \Delta t}` above for processes formulated to give
dry static energy tendencies.. In processes not formulated in terms of
dry static energy but rather in terms of a temperature tendency, that
tendency is simply accumulated.

After the last parameterization is completed, the dry static energy of
the last update is saved. This final column energy is saved and used at
the beginning of the next physics calculation following the Finite
Volume dynamical update to calculate the global energy fixer associated
with the dynamical core. The implication is that the energy
inconsistency introduced by sending the :math:`T` described above to the
FV rather than the :math:`T` returned by inverting the dry static energy
is included in the fixer attributed to the dynamics. The accumulated
physics temperature tendency is also available after the last
parameterization is completed, :math:`{\Delta T_I / \Delta t}`. An
updated temperature is calculated from it by adding it to the
temperature at the beginning of the physics.

.. math:: T_I = T_0 + \frac{\Delta T_I}{\Delta t}*\Delta t

This temperature is converted to virtual potential temperature and
passed to the Finite Volume dynamical core. The temperature tendency
itself is passed to the spectral transform Eulerian and semi-Lagrangian
dynamical cores. The inconsistency in the use of temperature and dry
static energy apparent in the description above should be eliminated in
future versions of the model.

.. _ssec-wetanddry:

Conversion to and from dry and wet mixing ratios for trace constituents in the model
------------------------------------------------------------------------------------

There are trade offs in the various options for the representation of
trace constituents :math:`\chi` in any general circulation model:

#. When the air mass in a model layer is defined to include the water
   vapor, it is frequently convenient to represent the quantity of trace
   constituent as a “moist” mixing ratio :math:`\chi^m`, that is, the
   mass of tracer per mass of moist air in the layer. The advantage of
   the representation is that one need only multiply the moist mixing
   ratio by the moist air mass to determine the tracer air mass. It has
   the disadvantage of implicitly requiring a change in :math:`\chi^m`
   whenever the water vapor :math:`q` changes within the layer, even if
   the mass of the trace constituent does not.

#. One can also utilize a “dry” mixing ratio :math:`\chi^d` to define
   the amount of constituent in a volume of air. This variable does not
   have the implicit dependence on water vapor, but does require that
   the mass of water vapor be factored out of the air mass itself in
   order to calculate the mass of tracer in a cell.

NCAR atmospheric models have historically used a combination of dry and
moist mixing ratios. Physical parameterizations (including convective
transport) have utilized moist mixing ratios. The resolved scale
transport performed in the Eulerian (spectral), and semi-Lagrangian
dynamics use dry mixing ratios, specifically to prevent oscillations
associated with variations in water vapor requiring changes in tracer
mixing ratios. The finite volume dynamics module utilizes moist mixing
ratios, with an attempt to maintain internal consistency between
transport of water vapor and other constituents.

There is no “right” way to resolve the requirements associated with the
simultaneous treatment of water vapor, air mass in a layer and tracer
mixing ratios. But the historical treatment significantly complicates
the interpretation of model simulations, and in the latest version of
CAM we have also provided an “alternate” representation. That is, we
allow the user to specify whether any given trace constituent is
interpreted as a “dry” or “wet” mixing ratio through the specification
of an “attribute” to the constituent in the physics state structure. The
details of the specification are described in the users manual, but we
do identify the interaction between state quantities here.

At the end of the dynamics update to the model state, the surface
pressure, specific humidity, and tracer mixing ratios are returned to
the model. The physics update then is allowed to update specific
humidity and tracer mixing ratios through a sequence of operator
splitting updates *but the surface pressure is not allowed to evolve*.
Because there is an explicit relationship between the surface pressure
and the air mass within each layer we assume that water mass can change
within the layer by physical parameterizations *but dry air mass
cannot*. We have chosen to define the dry air mass in each layer at the
beginning of the physics update as

.. math:: \delta p^d_{i,k} = (1-q^0_{i,k}) \delta^m_{i,k}

for column :math:`i`, level :math:`k`. Note that the specific humidity
used is the value defined at the beginning of the physics update. We
define the transformation between dry and wet mixing ratios to be

.. math:: \chi^d_{i,k} = (\delta p^d_{i,k} / \delta p^m_{i,k}) \chi^m_{i,k}

We note that the various physical parameterizations that operate on
tracers on the model (convection, turbulent transport, scavenging,
chemistry) will require a specification of the air mass within each cell
as well as the value of the mixing ratio in the cell. We have modified
the model so that it will use the correct value of :math:`\delta p`
depending on the attribute of the tracer, that is, we use couplets of
:math:`(\chi^m, \delta p^m)` or :math:`(\chi^d, \delta p^d)` in order to
assure that the process conserves mass appropriately.

We note further that there are a number of parameterizations
(convection, vertical diffusion) that transport species using a
continuity equation in a flux form that can be written generically as

.. math::
   :label: wetdry1

   {\partial \chi \over \partial t} = {\partial F(\chi) \over \partial p}
   

where :math:`F` indicates a flux of :math:`\chi`. For example, in
convective transports :math:`F(\chi)` might correspond to
:math:`M_u \chi` where :math:`M_u` is an updraft mass flux. In
principle one should adjust :math:`M_u` to reflect the fact that it may
be moving a mass of dry air or a mass of moist air. We assume these
differences are small, and well below the errors required to produce
equation :eq:`wetdry1` in the first place. The same is true for the
diffusion coefficients involved in turbulent transport. All processes
using equations of such a form still satisfy a conservation relationship

.. math:: {\partial \over \partial t} \sum_k{\chi_k \delta p_k}  = F_{kbot} - F_{ktop}

provided the appropriate :math:`\delta p` is used in the summation.

.. _ssec-deep-convection:

Deep Convection
---------------

The process of deep convection is treated with a parameterization
scheme developed by :cite:`zhang95` and modified with the addition of
convective momentum transports by :cite:`richter08` and a modified
dilute plume calculation following  :cite:`raymond86,raymond92`. The
scheme is based on a plume ensemble approach where it is assumed that
an ensemble of convective scale updrafts (and the associated saturated
downdrafts) may exist whenever the atmosphere is conditionally
unstable in the lower troposphere.  The updraft ensemble is comprised
of plumes sufficiently buoyant so as to penetrate the unstable layer,
where all plumes have the same upward mass flux at the bottom of the
convective layer.  Moist convection occurs only when there is
convective available potential energy (CAPE) for which parcel ascent
from the sub-cloud layer acts to destroy the CAPE at an exponential
rate using a specified adjustment time scale.  For the convenience of
the reader we will review some aspects of the formulation, but refer
the interested reader to :cite:`zhang95` for additional detail,
including behavioral characteristics of the parameterization scheme.
Evaporation of convective precipitation is computed following the
procedure described in section `conv_evap`_.

The large-scale budget equations distinguish between a cloud and
sub-cloud layer where temperature and moisture response to convection in
the cloud layer is written in terms of bulk convective fluxes as

.. math::
   :label: 4.g.1

   c_p \left( \frac{\partial T}{\partial t} \right)_{cu} =
   - \frac{1}{\rho} \frac{\partial}{\partial z} \left(
   M_u S_u + M_d S_d - M_c S \right) + L(C - E) \,  

.. math::
   :label: 4.g.2

   \left( \frac{\partial q}{\partial t} \right)_{cu} =
   - \frac{1}{\rho} \frac{\partial}{\partial z} \left(
   M_u q_u + M_d q_d - M_c q \right) + E - C 
   ~,

for :math:`z\ge z_b`, where :math:`z_b` is the height of the cloud base.
For :math:`z_s<z<z_b`, where :math:`z_s` is the surface height, the
sub-cloud layer response is written as

.. math::
   :label: 4.g.3

   c_p {\left( \rho \frac{\partial T}{\partial t} \right)}_{m} =
   - \frac{1}{z_b-z_s} \left( M_b [S(z_b) - S_u (z_b)]
   + M_d [S(z_b) - S_d (z_b)] \right) \,  

.. math::
   :label: 4.g.4

   {\left(\rho \frac{\partial q}{\partial t} \right)}_{m}  =
   - \frac{1}{z_b-z_s} \left( M_b [q(z_b) - q_u (z_b)]
   + M_d [q(z_b) - q_d (z_b)] \right) 
   ~,

where the net vertical mass flux in the convective region, :math:`M_c`,
is comprised of upward, :math:`M_u`, and downward, :math:`M_d`,
components, :math:`C` and :math:`E` are the large-scale condensation and
evaporation rates, :math:`S`, :math:`S_u`, :math:`S_d`, :math:`q`,
:math:`q_u`, :math:`q_d`, are the corresponding values of the dry static
energy and specific humidity, and :math:`M_b` is the cloud base mass
flux.

Updraft Ensemble
~~~~~~~~~~~~~~~~

The updraft ensemble is represented as a collection of entraining
plumes, each with a characteristic fractional entrainment rate
:math:`\lambda`. The moist static energy in each plume :math:`h_c` is
given by

.. math::
   :label: zmhc1

   \frac{\partial h_c}{\partial z} = \lambda (h - h_c), \quad
        z_b<z<z_D 
   ~.

Mass carried upward by the plumes is detrained into the environment in a
thin layer at the top of the plume, :math:`z_D`, where the detrained air
is assumed to have the same thermal properties as in the environment
(:math:`S_c=S`). Plumes with smaller :math:`\lambda` penetrate to larger
:math:`z_D`. The entrainment rate :math:`\lambda_D` for the plume which
detrains at height :math:`z` is then determined by solving :eq:`zmhc1` ,
with lower boundary condition :math:`h_c(z_b)=h_b`:

.. math::

   \begin{aligned}
     \frac{\partial h_c}{\partial (z-z_b)} &=& \lambda_D (h - h_b) -
       \lambda_D (h_c - h_b) \\
     \frac{\partial (h_c - h_b)}{\partial (z-z_b)} - \lambda_D (h_c -
       h_b) &=& \lambda_D (h - h_b) \\
     \frac{\partial (h_c - h_b)e^{\lambda_D(z-z_b)}}{\partial (z-z_b)}
       &=& \lambda_D (h - h_b)e^{\lambda_D(z-z_b)} \\
     (h_c - h_b)e^{\lambda_D(z-z_b)} &=& \int_{z_b}^z \lambda_D (h -
       h_b)e^{\lambda_D(z^\prime-z_b)} dz^\prime \\
     (h_c - h_b) &=&\lambda_D \int_{z_b}^z (h -
       h_b)e^{\lambda_D(z^\prime-z)} dz^\prime
   ~.\end{aligned}

Since the plume is saturated, the detraining air must have
:math:`h_c=h^*`, so that

.. math::
   :label: zmhc2

   (h_b - h^*) =\lambda_D \int_{z_b}^z (h_b -
       h)e^{\lambda_D(z^\prime-z)} dz^\prime 
   ~.

Then, :math:`\lambda_D` is determined by solving :eq:`zmhc2`  iteratively
at each :math:`z`.

The top of the shallowest of the convective plumes, :math:`z_0` is
assumed to be no lower than the mid-tropospheric minimum in saturated
moist static energy, :math:`h^*`, ensuring that the cloud top
detrainment is confined to the conditionally stable portion of the
atmospheric column. All condensation is assumed to occur within the
updraft plumes, so that :math:`C = C_u`. Each plume is assumed to have
the same value for the cloud base mass flux :math:`M_b`, which is
specified below. The vertical distribution of the cloud updraft mass
flux is given by

.. math::
   :label: 4.g.5

   M_u = M_b \int^{\lambda_D}_0 \frac{1}{\lambda_0} e^{\lambda (z -
         z_b)}d\lambda = M_b \frac{e^{\lambda_D (z - z_b)} - 1}{\lambda_0
         (z - z_b)}
    
   ~,

where :math:`\lambda_0` is the maximum detrainment rate, which occurs
for the plume detraining at height :math:`z_0`, and :math:`\lambda_D` is
the entrainment rate for the updraft that detrains at height :math:`z`.
Detrainment is confined to regions where :math:`\lambda_D` decreases
with height, so that the total detrainment :math:`D_u = 0` for
:math:`z < z_0`. Above :math:`z_0`,

.. math::
   :label: 4.g.6b

   D_u = - \frac{M_b}{\lambda_0} \frac{\partial \lambda_D}{\partial z}
           
   ~.

The total entrainment rate is then just given by the change in mass
flux and the total detrainment,

.. math::
   :label: 4.g.6c

   E_u = \frac{\partial M_u}{\partial z} - D_u
           
   ~.

The updraft budget equations for dry static energy, water vapor mixing
ratio, moist static energy, and cloud liquid water, :math:`\ell`, are:

.. math::
   :label: 4.g.7

   \frac{\partial}{\partial z} \left ( M_u S_u \right ) = \left ( E_u -  D_u \right ) S + \rho LC_u 

.. math::
   :label: 4.g.8

   \frac{\partial}{\partial z}  \left ( M_u q_u \right ) = E_u q - D_u q^* + \rho C_u 

.. math::
   :label: 4.g.8b

   \frac{\partial}{\partial z} \left ( M_u h_u \right )  =  E_u h - D_u  h^* 

.. math::
   :label: 4.g.9

   \frac{\partial}{\partial z} \left ( M_u \ell \right ) =  - D_u \ell_d + \rho C_u - \rho R_u ~,

where :eq:`4.g.8b`  is formed from :eq:`4.g.7`  and :eq:`4.g.8`  and detraining
air has been assumed to be saturated (:math:`q=q^*` and :math:`h=h^*`).
It is also assumed that the liquid content of the detrained air is the
same as the ensemble mean cloud water (:math:`\ell_d = \ell`). The
conversion from cloud water to rain water is given by

.. math::
   :label: 4.g.10

   \rho R_u = c_0 M_u \ell 
   ~,

following Lord, Chao, and Arakawa (1982), with
:math:`c_0 = 2 \times 10^{-3}\ {\rm m}^{-1}`.

Since :math:`M_u`, :math:`E_u` and :math:`D_u` are given by
:eq:`4.g.5` - :eq:`4.g.6c`, and :math:`h` and :math:`h^*` are environmental
profiles, :eq:`4.g.8b`  can be solved for :math:`h_u`, given a lower
boundary condition. The lower boundary condition is obtained by adding a
:math:`0.5` K temperature perturbation to the dry (and moist) static
energy at cloud base, or :math:`h_u = h +
c_p\times 0.5` at :math:`z=z_b`. Below the lifting condensation level
(LCL), :math:`S_u` and :math:`q_u` are given by :eq:`4.g.7`  and :eq:`4.g.8` .
Above the LCL, :math:`q_u` is reduced by condensation and :math:`S_u` is
increased by the latent heat of vaporization. In order to obtain to
obtain a saturated updraft at the temperature implied by :math:`S_u`, we
define :math:`\Delta T` as the temperature perturbation in the updraft,
then:

.. math::
   :label: zm10.1

   h_u = S_u + L q_u   

.. math::
   :label: zm10.2

   S_u = S + c_p \Delta T

.. math::
   :label: zm10.3

   q_u = q^* + \frac{d q^*}{dT}\Delta  T ~.

Substituting :eq:`zm10.2`  and :eq:`zm10.3`  into :eq:`zm10.1` ,

.. math::
   :label: zm10.4

   \begin{aligned}
     h_u &=& S + L q^* + c_p \left(1 + \frac{L}{c_p}\frac{d q^*}{dT}
            \right)\Delta T  \\
         &=& h^* + c_p\left(1+\gamma \right)\Delta T  \\
     \gamma &\equiv& \frac{L}{c_p}\frac{d q^*}{dT} \\
     \Delta T &=& \frac{1}{c_p}\frac{h_u - h^*}{1+\gamma}
   ~.\end{aligned}

The required updraft quantities are then

.. math::
   :label: zm10.7

   \begin{aligned}
     S_u &=& S + \frac{h_u - h^*}{1+\gamma}  \\ q_u &=& q^*
     + \frac{\gamma}{L} \frac{h_u - h^*}{1+\gamma} 
   ~.\end{aligned}

With :math:`S_u` given by :eq:`zm10.7` , :eq:`4.g.7`  can be solved for
:math:`C_u`, then :eq:`4.g.9`  and :eq:`4.g.10`  can be solved for
:math:`\ell` and :math:`R_u`.

The expressions above require both the saturation specific humidity to
be

.. math::
   :label: zm10.10

   q^* = \frac{\epsilon e^*}{p-e^*}, \qquad e^* < p 
   ~,

where :math:`e^*` is the saturation vapor pressure, and its dependence
on temperature (in order to maintain saturation as the temperature
varies) to be

.. math::

   \begin{aligned}
   \frac{d q^*}{d T} &=& \frac{\epsilon}{p-e^*} \frac{d e^*}{d T}
        - \frac{\epsilon e^*}{(p-e^*)^2}\frac{d (p-e^*)}{d T} \\
      &=& \frac{\epsilon}{p-e^*}\left(1 + \frac{1}{p-e^*}\right) \frac{d
             e^*}{d T} \\
      &=& \frac{\epsilon}{p-e^*}\left(1 + \frac{q^*}{\epsilon e^*}\right)
             \frac{d e^*}{d T}
   ~.\end{aligned}

The deep convection scheme does not use the same approximation for the
saturation vapor pressure :math:`e^*` as is used in the rest of the
model. Instead,

.. math::
   :label: zm10.9

   e^* = c_1 \exp\left[\frac{c_2(T - T_f)}{(T-T_f+c_3)} \right]
    
   ~,

where :math:`c_1=6.112`, :math:`c_2=17.67`, :math:`c_3=243.5` K and
:math:`T_f=273.16` K is the freezing point. For this approximation,

.. math::
   :label: zm10.9b

   \begin{aligned}
     \frac{d e^*}{d T} &=& e^* \frac{d}{dT} \left[\frac{c_2(T -
       T_f)}{(T-T_f+c_3)} \right] \\ &=& e^*
       \left[\frac{c_2}{(T-T_f+c_3)}
               - \frac{c_2(T - T_f)}{(T-T_f+c_3)^2} \right] \\ &=& e^*
       \frac{c_2 c_3}{(T-T_f+c_3)^2}  \\
   \end{aligned}

.. math::
   :label: zm10.11

   \begin{aligned}
     \frac{d q^*}{d T}
       &=& q^*\left(1+ \frac{q^*}{\epsilon e^*}\right) \frac{c_2
                       c_3}{(T-T_f+c_3)^2} 
   ~.\end{aligned}

We note that the expression for :math:`\gamma` in the code gives

.. math::
   :label: zm10.12

   \frac{d q^*}{d T} = \frac{c_p}{L}\gamma
         = q^*\left(1+ \frac{q^*}{\epsilon}\right) \frac{\epsilon
                       L}{RT^2} 
   ~.

The expressions for :math:`{d q^*}/{d T}` in :eq:`zm10.11`  and
:eq:`zm10.12`  are not identical. Also, :math:`T-T_f+c_3 \neq T` and
:math:`c_2
c_3 \neq \epsilon L/R`.

Downdraft Ensemble
~~~~~~~~~~~~~~~~~~

Downdrafts are assumed to exist whenever there is precipitation
production in the updraft ensemble where the downdrafts start at or
below the bottom of the updraft detrainment layer. Detrainment from the
downdrafts is confined to the sub-cloud layer, where all downdrafts have
the same mass flux at the top of the downdraft region. Accordingly, the
ensemble downdraft mass flux takes a similar form to :eq:`4.g.5`  but
includes a “proportionality factor” to ensure that the downdraft
strength is physically consistent with precipitation availability. This
coefficient takes the form

.. math::
   :label: 4.g.11

   \alpha = \mu \left [ \frac{P}{P + E_d} \right ] 
   ~,

where :math:`P` is the total precipitation in the convective layer and
:math:`E_d` is the rain water evaporation required to maintain the
downdraft in a saturated state. This formalism ensures that the
downdraft mass flux vanishes in the absence of precipitation, and that
evaporation cannot exceed some fraction, :math:`\mu`, of the
precipitation, where :math:`\mu` = 0.2.

Closure
~~~~~~~

The parameterization is closed, i.e., the cloud base mass fluxes are
determined, as a function of the rate at which the cumulus consume
convective available potential energy (CAPE). Since the large-scale
temperature and moisture changes in both the cloud and sub-cloud layer
are linearly proportional to the cloud base updraft mass flux (see eq.
:eq:`4.g.1` – :eq:`4.g.4`), the CAPE change due to convective activity can be
written as

.. math::
   :label: 4.g.12

   \left( \frac{\partial A}{\partial t} \right)_{cu} = -M_b F
   
   ~,

where :math:`F` is the CAPE consumption rate per unit cloud base mass
flux. The closure condition is that the CAPE is consumed at an
exponential rate by cumulus convection with characteristic adjustment
time scale :math:`\tau = 7200 s`:

.. math::
   :label: 4.g.13

   M_b = \frac{A}{\tau F} 
   ~.

Numerical Approximations
~~~~~~~~~~~~~~~~~~~~~~~~

The quantities :math:`M_{u,d}`, :math:`\ell`, :math:`S_{u,d}`,
:math:`q_{u,d}`, :math:`h_{u,d}` are defined on layer interfaces, while
:math:`D_u`, :math:`C_u`, :math:`R_u` are defined on layer midpoints.
:math:`S`, :math:`q`, :math:`h`, :math:`\gamma` are required on both
midpoints and interfaces and the interface values :math:`\psi^{k\pm}` 
are determined from the midpoint values :math:`\psi^k` as

.. math::
   :label: zm_int1

   \psi^{k-} = \log\left(\frac{\psi^{k-1}}{\psi^k}\right)
                  \frac{\psi^{k-1} \psi^k}{\psi^{k-1} - \psi^k}
                  
   ~.

All of the differencing within the deep convection is in height
coordinates. The differences are naturally taken as

.. math::

   \frac{\partial \psi}{\partial z} = \frac{\psi^{k-} - \psi^{k+}}{z^{k-}
   - z^{k+}}
   ~,

where :math:`\psi^{k-}` and :math:`\psi^{k+}` represent values on the
upper and lower interfaces, respectively for layer :math:`k`. The
convention elsewhere in this note (and elsewhere in the code) is
:math:`\delta^k\psi = \psi^{k+}
- \psi^{k-}`. Therefore, we avoid using the compact :math:`\delta^k`
notation, except for height, and define

.. math::

   d^kz \equiv z^{k-} - z^{k+} = -\delta^k z
   ~,

so that :math:`d^kz` corresponds to the variable dz(k) in the deep
convection code.

Although differences are in height coordinates, the equations are cast
in flux form and the tendencies are computed in units
:math:`\rm kg\ m^{-3}\
s^{-1}`. The expected units are recovered at the end by multiplying by
:math:`g\delta z/\delta p`.

The environmental profiles at midpoints are

.. math::

   \begin{aligned}
     S^k &=& c_p T^k + g z^k \\ h^k &=& S^k + L q^k \\ h^{*k} &=& S^k + L
     q^{*k} \\ q^{*k} &=& \epsilon e^{*k} / (p^k - e^{*k}) \\ e^{*k} &=&
     c_1 \exp\left[\frac{c_2(T^k - T_f)}{(T^k-T_f+c_3)} \right] \\
     \gamma^k &=& q^{*k}\left(1+ \frac{q^{*k}}{\epsilon}\right)
                       \frac{\epsilon L^2}{c_pR{T^k}^2}
   ~.\end{aligned}

The environmental profiles at interfaces of :math:`S`, :math:`q`,
:math:`q^*`, and :math:`\gamma` are determined using :eq:`zm_int1` 
if :math:`|\psi^{k-1}-\psi^{k}|` is large enough. 
**However, there are inconsistencies in what happens if** :math:`|\psi^{k-1}-\psi^{k}|` 
**is not large enough**. For :math:`S` and :math:`q` the condition is

.. math::

   \psi^{k-} = (\psi^{k-1}+\psi^k)/2, \quad
       \frac{|\psi^{k-1}-\psi^{k}|}{\max(\psi^{k-1}-\psi^{k})} \leq
       10^{-6}
   ~.

For :math:`q^*` and :math:`\gamma` the condition is

.. math::

   \psi^{k-} = \psi^{k}, \quad |\psi^{k-1}-\psi^{k}| \leq 10^{-6}
   ~.

Interface values of :math:`h` are not needed and interface values of
:math:`h^*` are given by

.. math::

   \begin{aligned}
     h^{*k-} &=& S^{k-} + L q^{*k-}
   ~.\end{aligned}

The unitless updraft mass flux (scaled by the inverse of the cloud base
mass flux) is given by differencing :eq:`4.g.5`  as

.. math::

   M_u^{k-} = \frac{1}{\lambda_0(z^{k-}-z_b)} \left( e^{\lambda_D^k
                  (z^{k-}-z_b)} -1 \right)
   ~,

with the boundary condition that :math:`M_u^{M+} =1`. The entrainment
and detrainment are calculated using

.. math::

   \begin{aligned}
     m_u^{k-} &=& \frac{1}{\lambda_0(z^{k-}-z_b)} \left(
                  e^{\lambda_D^{k+1} (z^{k-}-z_b)} -1 \right) \\
     E_u^k &=& \frac{m_u^{k-} - M_u^{k+}}{d^kz} \\ D_u^k &=&
     \frac{m_u^{k-} - M_u^{k-}}{d^kz}
   ~.\end{aligned}

Note that :math:`M_u^{k-}` and :math:`m_u^{k-}` differ only by the
value of :math:`\lambda_D`.

The updraft moist static energy is determined by differencing :eq:`4.g.8b` 

.. math::
   :label: zm_hu_d1

   \frac{M_u^{k-}h_u^{k-} - M_u^{k+}h_u^{k+}}{d^kz} = E_u^k h^k - D_u^k  h^{*k} 

.. math::
   :label: zm_hu_d2

   h_u^{k-} = \frac{1}{M_u^{k-}}\left[M_u^{k+} h_u^{k+} + d^kz\left( E_u^k h^k - D_u^k h^{*k} \right)\right] ~,

with :math:`h_u^{M-} = h^M + c_p/2`, where :math:`M` is the layer of
maximum :math:`h`.

Once :math:`h_u` is determined, the lifting condensation level is found
by differencing :eq:`4.g.7`  and :eq:`4.g.8`  similarly to :eq:`4.g.8b` :

.. math::
   :label: zm_su_d2

   S_u^{k-} = \frac{1}{M_u^{k-}}\left[M_u^{k+} S_u^{k+} + d^kz\left( E_u^k S^k - D_u^k S^{k} \right)\right] 

.. math::
   :label: zm_qu_d2

   q_u^{k-} = \frac{1}{M_u^{k-}}\left[M_u^{k+} q_u^{k+} + d^kz\left(  E_u^k q^k - D_u^k q^{*k} \right)\right] 

The detrainment of :math:`S_u` is given by :math:`D_u^kS^k` not by
:math:`D_u^kS_u^k`, since detrainment occurs at the environmental value
of :math:`S`. The detrainment of :math:`q_u` is given by
:math:`D_u^k q^{*k}`, even though the updraft is not yet saturated. The
LCL will usually occur below :math:`z_0`, the level at which detrainment
begins, but this is not guaranteed.

The lower boundary conditions, :math:`S_u^{M-} = S^M + c_p/2` and
:math:`q_u^{M-}= q^M`, are determined from the first midpoint values in the plume,
rather than from the interface values of :math:`S` and :math:`q`. The
solution of :eq:`zm_su_d2`  and :eq:`zm_qu_d2`  continues upward until the updraft is
saturated according to the condition

.. math::

   \begin{aligned}
     q_u^{k-} &>& q^{*}(T_u^{k-}), \\ T_u^{k-} &=& \frac{1}{c_p}\left(
     S_u^{k-} - gz^{k-}\right)
   ~.\end{aligned}

The condensation (in units of m\ :math:`^{-1}`) is determined by a
centered differencing of :eq:`4.g.7` :

.. math::

   \frac{M_u^{k-}S_u^{k-} - M_u^{k+}S_u^{k+}}{d^kz} = (E_u^k - D_u^k)
       S^k + L C_u^k

.. math::

   \begin{aligned}
     C_u^k &=& \frac{1}{L} \left[ \frac{M_u^{k-}S_u^{k-} -
             M_u^{k+}S_u^{k+}}{d^kz}
             - (E_u^k - D_u^k) S^k \right]
   ~.\end{aligned}

The rain production (in units of m\ :math:`^{-1}`) and condensed liquid
are then determined by differencing :eq:`4.g.9`  as

.. math::

   \frac{M_u^{k-}\ell^{k-} - M_u^{k+}\ell^{k+}}{d^kz} = -D_u^k
       \ell^{k+} + C_u^k - R_u^k
   ~,

and :eq:`4.g.10`  as

.. math::

   R_u^k = c_0 M_u^{k-} \ell^{k-}
   ~.

Then

.. math::

   \begin{aligned}
     M_u^{k-}\ell^{k-} &=& M_u^{k+}\ell^{k+} - d^kz \left( D_u^k
       \ell^{k+} - C_u^k + c_0 M_u^{k-} \ell^{k-} \right) \\
     M_u^{k-}\ell^{k-} \left(1 + c_0 d^kz \right) &=& M_u^{k+}\ell^{k+} +
       d^kz \left( D_u^k \ell^{k+} - C_u^k \right) \\
     \ell^{k-} &=& \frac{1}{M_u^{k-}\left(1 + c_0 d^kz \right)} \left[
       M_u^{k+}\ell^{k+} - d^kz \left(D_u^k \ell^{k+} - C_u^k \right)
       \right]
   ~.\end{aligned}

.. _ssec-convection-cmt:

Deep Convective Momentum Transports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sub-grid scale Convective Momentum Transports (CMT) have ben added to
the existing deep convection parameterization following Richter and
Rasch (2008) and the methodology of Gregory, Kershaw, and Inness (1997).
The sub-grid scale transport of momentum can be cast in the same manner
as :eq:`4.g.2` . Expressing the grid mean horizontal velocity vector,
:math:`\boldsymbol{V}`, tendency due to deep convection transport
following Kershaw and Gregory (1997) gives

.. math::
   :label: 4.cmt.1

   \begin{aligned}
   \left( \frac{\partial \boldsymbol{V}}{\partial t} \right)_{cu} &=
   - \frac{1}{\rho} \frac{\partial}{\partial z} \left(
   M_u \boldsymbol{V}_u + M_d \boldsymbol{V}_d - M_c \boldsymbol{V} \right)  
   ~,\end{aligned}

and neglecting the contribution from the environment the updraft and
downdraft budget equation can similarly be written as

.. math::
   :label: 4.cmt.2

   \begin{aligned}
   -\frac{\partial}{\partial z} \left ( M_u  \boldsymbol{V}_u \right ) &=& E_u  \boldsymbol{V}-D_u\boldsymbol{V}_u  + \boldsymbol{P}^u_G   \\
   -\frac{\partial}{\partial z} \left ( M_d  \boldsymbol{V}_d \right ) &=& E_d \boldsymbol{V} + \boldsymbol{P}^d_G 
   ~,\end{aligned}

where :math:`\boldsymbol{P}^u_G` and :math:`\boldsymbol{P}^d_G` the
updraft and downdraft pressure gradient sink terms parameterized from
Gregory, Kershaw, and Inness (1997) as

.. math::
   :label: 4.cmt.4

   \boldsymbol{P}^u_G   = -C_u M_u\frac{\partial \boldsymbol{V}}{\partial z}  

.. math::
   :label: 4.cmt.5

   \boldsymbol{P}^d_G   = -C_d M_d\frac{\partial \boldsymbol{V}}{\partial z}. 

:math:`C_u` and :math:`C_d` are tunable parameters. In the |cam| 
implementation we use :math:`C_u = C_d = 0.4`. The value of :math:`C_u`
and :math:`C_d` control the strength of convective momentum transport.
As these coefiicients increase so do the pressure gradient terms, and
convective momentum transport decreases.

Deep Convective Tracer Transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The |cam| provides the ability to transport constituents via convection. The
method used for constituent transport by deep convection is a
modification of the formulation described in Zhang and McFarlane (1995).

We assume the updrafts and downdrafts are described by a steady state
mass continuity equation for a “bulk” updraft or downdraft

.. math::
   :label: eq:updraft

   {\partial (M_x q_x) \over \partial p} = E_x q_e - D_x
   q_x 
   ~.

The subscript :math:`x` is used to denote the updraft (:math:`u`) or
downdraft (:math:`d`) quantity. :math:`M_x` here is the mass flux in
units of Pa/s defined at the layer interfaces, :math:`q_x` is the mixing
ratio of the updraft or downdraft. :math:`q_e` is the mixing ratio of
the quantity in the environment (that part of the grid volume not
occupied by the up and downdrafts). :math:`E_x` and :math:`D_x` are the
entrainment and detrainment rates (units of s\ :math:`^{-1}`) for the
up- and down-drafts. Updrafts are allowed to entrain or detrain in any
layer. Downdrafts are assumed to entrain only, and all of the mass is
assumed to be deposited into the surface layer.

Equation :eq:`eq:updraft` is first solved for up and downdraft mixing ratios
:math:`q_u` and :math:`q_d`, assuming the environmental mixing ratio
:math:`q_e` is the same as the gridbox averaged mixing ratio
:math:`\bar q`.

Given the up- and down-draft mixing ratios, the mass continuity equation
used to solve for the gridbox averaged mixing ratio :math:`\bar q` is

.. math::
   :label: eq:masscon

   {\partial \bar q \over \partial t} = {\partial \over \partial p} (M_u
   (q_u-\bar q) + M_d (q_d-\bar q)) 
   ~.

These equations are solved for in subroutine CONVTRAN. There are a few
numerical details employed in CONVTRAN that are worth mentioning here as
well.

-  mixing quantities needed at interfaces are calculated using the
   geometric mean of the layer mean values.

-  simple first order upstream biased finite differences are used to
   solve :eq:`eq:updraft` and :eq:`eq:masscon`.

-  fluxes calculated at the interfaces are constrained so that the
   resulting mixing ratios are positive definite. *This means that this
   parameterization is not suitable for moving mixing ratios of
   quantities meant to represent perturbations of a trace constituent
   about a mean value* (in which case the quantity can meaningfully take
   on positive and negative mixing ratios). The algorithm can be
   modified in a straightforward fashion to remove this constraint, and
   provide meaningful transport of perturbation quantities if necessary.
   *the reader is warned however that there are other places in the
   model code where similar modifications are required because the model
   assumes that all mixing ratios should be positive definite
   quantities*.

.. _conv_evap:

Evaporation of convective precipitation
---------------------------------------

The |cam| employs a :cite:`sundqvist88` style evaporation of the convective
precipitation as it makes its way to the surface. This scheme relates
the rate at which raindrops evaporate to the local large-scale
subsaturation, and the rate at which convective rainwater is made
available to the subsaturated model layer

.. math::
   :label: 4.g.15

   E_{r_k} = K_E \; (1 - \text{RH}_k) \; {(\hat{R}_{r_k})}^{1/2} 

   ~.

where :math:`\text{RH}_k` is the relative humidity at level :math:`k`,
:math:`\hat{R}_{r_k}` denotes the total rainwater flux at level
:math:`k` (which can be different from the locally diagnosed rainwater
flux from the convective parameterization, as will be shown below), the
coefficient :math:`K_E` takes the value 0.2 :math:`\cdot`
10\ :math:`^{-5}` (kg m\ :math:`^{-2}`
s\ :math:`^{-1}`)\ :math:`^{-1/2}`\ s\ :math:`^{-1}`, and the variable
:math:`E_{r_k}` has units of s\ :math:`^{-1}`. The evaporation rate
:math:`E_{r_k}` is used to determine a local change in :math:`q_k` and
:math:`T_k`, associated with an evaporative reduction of
:math:`\hat{R}_{r_k}`. Conceptually, the evaporation process is invoked
after a vertical profile of :math:`R_{r_k}` has been evaluated. An
evaporation rate is then computed for the uppermost level of the model
for which :math:`R_{r_k} \not= 0` using :eq:`4.g.15` , where in this case
:math:`R_{r_k} \equiv \; \hat{R}_{r_k}`. This rate is used to evaluate
an evaporative reduction in :math:`R_{r_k}` which is then accumulated
with the previously diagnosed rainwater flux in the layer below,

.. math::
   :label: 4.g.16

   \hat{R}_{r_{k+1}} = \hat{R}_{r_k} - \left({{\Delta p_k} \over g}\right) \; E_{r_k} + R_{r_{k+1}}
   
   ~.

A local increase in the specific humidity :math:`q_k` and a local
reduction of :math:`T_k` are also calculated in accordance with the net
evaporation

.. math::
   :label: 4.g.17

   q_k = q_k + E_{r_k} \; 2 \Delta t \;
   
   ~,

and

.. math::
   :label: 4.g.18

   T_k = T_k - \left( {L \over c_p} \right) E_{r_k} \; 2 \Delta t \;
   
   ~.

The procedure, :eq:`4.g.15` -:eq:`4.g.18` , is then successively repeated for
each model level in a downward direction where the final convective
precipitation rate is that portion of the condensed rainwater in the
column to survive the evaporation process

.. math::
   :label: 4.g.19

   P_s = \left( \hat{R}_{r_{K}} - \left({{\Delta p_K} \over g}\right) \;  E_{r_K} \right) /\rho_{H_{2}0}
   
   ~.

In global annually averaged terms, this evaporation procedure produces
a very small reduction in the convective precipitation rate where the
evaporated condensate acts to moisten the middle and lower troposphere.

.. _ssec-prognostic-water:

Prognostic Condensate and Precipitation Parameterization
--------------------------------------------------------

Introductory comments
~~~~~~~~~~~~~~~~~~~~~

The parameterization of non-convective cloud processes in |cam| is described
in :cite:`rasch98` and :cite:`zhang03`. The original
formulation is introduced in Rasch and Kristjánsson (1998). Revisions to
the parameterization to deal more realistically with the treatment of
the condensation and evaporation under forcing by large scale processes
and changing cloud fraction are described in Zhang et al. (2003). The
equations used in the formulation are discussed here. The papers contain
a more thorough description of the formulation and a discussion of the
impact on the model simulation.

The formulation for cloud condensate combines a representation for
condensation and evaporation with a bulk microphysical parameterization
closer to that used in cloud resolving models. The parameterization
replaces the diagnosed liquid water path of CCM3 with evolution
equations for two additional predicted variables: liquid and ice phase
condensate. At one point during each time step, these are combined into
a total condensate and partitioned according to temperature (as
described in section :ref:`microscale`), but elsewhere function as
independent quantities. They are affected by both resolved (advective)
and unresolved (convective, turbulent) processes. Condensate can
evaporate back into the environment or be converted to a precipitating
form depending upon its in-cloud value and the forcing by other
atmospheric processes. The precipitate may be a mixture of rain and
snow, and is treated in diagnostic form, its time derivative has been
neglected.

The parameterization calculates the condensation rate more consistently
with the change in fractional cloudiness and in-cloud condensate than
the previous CCM3 formulation. Changes in water vapor and heat in a grid
volume are treated consistently with changes to cloud fraction and
in-cloud condensate. Condensate can form prior to the onset of grid-box
saturation and can require a significant length of time to convert (via
the cloud microphysics) to a precipitable form. Thus a substantially
wider range of variation in condensate amount than in the CCM3 is
possible.

The new parameterization adds significantly to the flexibility in the
model and to the range of scientific problems that can be studied. This
type of scheme is needed for quantitative treatment of scavenging of
atmospheric trace constituents and cloud aqueous and surface chemistry.
The addition of a more realistic condensate parameterization closely
links the radiative properties of the clouds and their formation and
dissipation. These processes must be treated for many problems of
interest today (e.g. anthropogenic aerosol-climate interactions).

The parameterization has two components: 1) a macroscale component that
describes the exchange of water substance between the condensate and the
vapor phase and the associated temperature change arising from that
phase change Zhang et al. (2003); and 2) a bulk microphysical component
that controls the conversion from condensate to precipitate (Rasch and
Kristjánsson 1998). These components are discussed in the following two
sections.

Cloud Microphysics
------------------

The base parameterization of stratiform cloud microphysics is described
by Gettelman and Morrison (2015), and is version 2 of the scheme
described by Morrison and Gettelman (2008). Details of the CAM implementation are
described by Gettelman et al (2015) and :cite:`gettelman2008`. Modifications to
handle ice nucleation and ice supersaturation are described by Gettelman
and others (2010).

The scheme seeks the following:

-  A more flexible, self-consistent, physically-based treatment of cloud
   physics.

-  A reasonable level of simplicity and computational efficiency.

-  Treatment of both number concentration and mixing ratio of cloud
   particles to address indirect aerosol effects and cloud-aerosol
   interaction.

-  Representation of precipitation number concentration, mass, and phase
   to better treat wet deposition and scavenging of aerosol and chemical
   species.

-  The achievement of equivalent or better results relative to the CAM3
   microphysics parameterization when compared to observations.

The novel aspects of the scheme are an explicit representation of
sub-grid cloud water distribution for calculation of the various
microphysical process rates, and the diagnostic two-moment treatment of
rain and snow.

Overview of the microphysics scheme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The two-moment scheme is based loosely on the approach of Morrison,
Curry, and Khvorostyanov (2005). This scheme predicts the number
concentrations (Nc, Ni) and mixing ratios (qc, qi) of cloud droplets
(subscript c) and cloud ice (subscript i). Hereafter, unless stated
otherwise, the cloud variables Nc, Ni, qc, and qi represent
grid-averaged values; prime variables represent mean in-cloud quantities
(e.g., such that Nc = Fcld NcÕ, where Fcld is cloud fraction); and
double prime variables represent local in-cloud quantities. The
treatment of sub-grid cloud variability is detailed in section 2.1.

The cloud droplet and ice size distributions :math:`\phi` are
represented by gamma functions:

.. math::
   :label: eq:MG1

                     
   \phi(D)=N_0 D^\mu \exp^{-\lambda D}

where :math:`D`\ is diameter, :math:`N_0` is the ÔinterceptÕ parameter,
:math:`\lambda` is the slope parameter, and :math:`\mu = 1 / \eta^2 -1`
is the spectra shape parameter; :math:`\eta` is the relative radius
dispersion of the size distribution. The parameter :math:`\eta` for
droplets is specified following Martin, Johnson, and Spice (1994). Their
observations of maritime versus continental warm stratocumulus have been
approximated by the following :math:`\eta -
N^{\prime\prime}_c` relationship:

.. math::
   :label: eq:mg2

    
   \eta = 0.0005714 N^{\prime\prime}_c + 0.2714

where :math:`N^{\prime\prime}_c` has units of cm\ :math:`^{-3}`. The
upper limit for :math:`\eta` is 0.577, corresponding with
a\ :math:`N^{\prime\prime}_c` of 535 cm\ :math:`^{-3}`. Note that this
expression is uncertain, especially when applied to cloud types other
than those observed by Martin, Johnson, and Spice (1994). In the current
version of the scheme, :math:`\mu`\ = 0 for cloud ice.

The spectral parameters :math:`N_0` and :math:`\lambda` are derived from
the predicted :math:`N^{\prime\prime}` and :math:`q^{\prime\prime}` and
specified :math:`\mu`:

.. math::
   :label: eq:MG3

    
    \lambda = \left[\frac{\pi \rho N^{\prime\prime}\Gamma(\mu + 4)}{6q^{\prime\prime}\Gamma(\mu +1)}\right]^{(1/3)}

.. math::
   :label: eq:MG4

    
   N_0 = \frac{N^{\prime\prime}\lambda^{\mu + 1}}{\Gamma(\mu +1)}

where :math:`\Gamma` is the Euler gamma function. Note that :eq:`eq:MG3` and
:eq:`eq:MG4` assume spherical cloud particles with bulk density :math:`\rho`
= 1000 kg m\ :math:`^{-3}` for droplets and :math:`\rho`\ = 500 kg
m\ :math:`^{-3}` for cloud ice following Reisner, Rasmussen, and
Bruintjes (1998).

The effective size for cloud ice needed by the radiative transfer scheme
is obtained directly by dividing the third and second moments of the
size distribution given by :eq:`eq:MG1` and accounting for differenceds in
cloud ice density and that of pure ice. After rearranging terms, this
yields

.. math::
   :label: eq:dei

   	
   d_ei = \frac{3 \rho}{\lambda \rho _i}

where :math:`\rho _i = 917` kg m-2 is the bulk density of pure ice. Note
that optical properties for cloud droplets are calculated using a lookup
table from the :math:`N_0` and :math:`\lambda` parameters. The droplet
effective radius, which is used for output purposes only, is given by

.. math::
   :label: eq:MG5

   	
   r_ec = \frac{\Gamma(\mu+4)}{2\lambda\Gamma(\mu +3)}

The time evolution of q and N is determined by grid-scale advection,
convective detrainment, turbulent diffusion, and several microphysical
processes:

.. math::
   :label: eq:MG6

   
   \frac{\partial N}{\partial t} + \frac{1}{\rho} \nabla \cdot [\rho \mathbf{u} N] =  \left(\frac{\partial N}{\partial t}\right)_{nuc} + \left(\frac{\partial N}{\partial t}\right)_{evap} + \left(\frac{\partial N}{\partial t}\right)_{auto} + \left(\frac{\partial N}{\partial t}\right)_{acer} + \left(\frac{\partial N}{\partial t}\right)_{accs} + \left(\frac{\partial N}{\partial t}\right)_{het} +\left(\frac{\partial N}{\partial t}\right)_{hom} + \left(\frac{\partial N}{\partial t}\right)_{mlt} + \left(\frac{\partial N}{\partial t}\right)_{mult} + \left(\frac{\partial N}{\partial t}\right)_{sed} + \left(\frac{\partial N}{\partial t}\right)_{det} +D(N)

.. math::
   :label: eq:MG7

   
   \frac{\partial q}{\partial t} + \frac{1}{\rho} \nabla \cdot [\rho \mathbf{u} q] =  \left(\frac{\partial q}{\partial t}\right)_{cond} + \left(\frac{\partial q}{\partial t}\right)_{evap} + \left(\frac{\partial q}{\partial t}\right)_{auto} + \left(\frac{\partial q}{\partial t}\right)_{acer} + \left(\frac{\partial q}{\partial t}\right)_{accs} + \left(\frac{\partial q}{\partial t}\right)_{het} +\left(\frac{\partial q}{\partial t}\right)_{hom} + \left(\frac{\partial q}{\partial t}\right)_{mlt} + \left(\frac{\partial q}{\partial t}\right)_{mult} + \left(\frac{\partial q}{\partial t}\right)_{sed} + \left(\frac{\partial q}{\partial t}\right)_{det} +D(N)

where t is time, :math:`\mathbf{u}` is the 3D wind vector, :math:`\rho`
is the air density, and D is the turbulent diffusion operator. The
symbolic terms on the right hand side of :eq:`eq:MG6` and :eq:`eq:MG7` represent
the grid-average microphysical source/sink terms for N and q. Note that
the source/sink terms for q and N are considered separately for cloud
water and ice (giving a total of four rate equations), but are
generalized here using :eq:`eq:MG6` and :eq:`eq:MG7` for conciseness. These
terms include activation of cloud condensation nuclei or
deposition/condensation-freezing nucleation on ice nuclei to form
droplets or cloud ice (subscript nuc; N only); ice multiplication via
rime-splintering on snow (subscript mult); condensation/deposition
(subscript cond; q only), evaporation/sublimation (subscript evap),
autoconversion of cloud droplets and ice to form rain and snow
(subscript auto), accretion of cloud droplets and ice by rain (subscript
accr), accretion of cloud droplets and ice by snow (subscript accs),
heterogeneous freezing of droplets to form ice (subscript het),
homogeneous freezing of cloud droplets (subscript hom), melting
(subscript mlt), ice multiplication (subsrcipt mult), sedimentation
(subscript sed), and convective detrainment (subscript det). The
formulations for these processes are detailed in section 3. Numerical
aspects in solving :eq:`eq:MG6` and :eq:`eq:MG7` are detailed in section 4.

Sub-grid cloud variability
^^^^^^^^^^^^^^^^^^^^^^^^^^

Sub-grid variability is considered for cloud water but neglected for
cloud ice and precipitation at present; furthermore, we neglect sub-grid
variability of droplet number concentration for simplicity. We assume
that the PDF of in-cloud cloud water, :math:`P(q_c^{\prime\prime})`,
follows a gamma distribution function based on observations of optical
depth in marine boundary layer clouds (Barker 1996; Barker, Weilicki,
and Parker 1996; McFarlane and Klein 1999):

.. math::
   :label: eq:MG8

   
   P(q_c^{\prime\prime}) = \frac{q_c^{\prime\prime \nu -1 } \alpha^\nu}{\Gamma(\nu)} \exp^{-\alpha q_c^{\prime\prime}}

where :math:`\nu = 1/\sigma^2`;\ :math:`\sigma^2` is the relative
variance (i.e., variance divided by :math:`q_c^{\prime 2}`); and
:math:`\alpha = \nu
/q_c^{\prime}` (:math:`q_c^{\prime}` is the mean in-cloud cloud water
mixing ratio). Note that this PDF is applied to all cloud types treated
by the stratiform cloud scheme; the appropriateness of such a PDF for
stratiform cloud types other than marine boundary layer clouds (e.g.,
deep frontal clouds) is uncertain given a lack of observations.

Satellite retrievals described by Barker, Weilicki, and Parker (1996)
suggest that :math:`\nu >
1` in overcast conditions and :math:`\nu \sim 1` (corresponding to an
exponential distribution) in broken stratocumulus. The model assumes a
constant :math:`\nu = 1` for simplicity.

A major advantage of using gamma functions to represent sub-grid
variability of cloud water is that the grid-average microphysical
process rates can be derived in a straightforward manner as follows. For
any generic local microphysical process rate :math:`M_p =
xq_c^{\prime\prime y}`, replacing :math:`q_c^{\prime\prime}` with
:math:`P(q_c^{\prime\prime})` from :eq:`eq:MG8` and integrating over the PDF
yields a mean in-cloud process rate

.. math::
   :label: eq:MG9

   
   M_p^{\prime} = x \frac{\Gamma(\nu + y)}{\Gamma(\nu)\nu^y}q_c^{\prime y}

Thus, each cloud water microphysical process rate in :eq:`eq:MG6` and :eq:`eq:MG7` is multiplied by a factor

.. math::
   :label: eq:MG10

   
   E = \frac{\Gamma(\nu + y)}{\Gamma(\nu)\nu^y}

Diagnostic treatment of precipitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As described by Ghan and Easter (1992), diagnostic treatment of
precipitation allows for a longer time step, since prognostic
precipitation is constrained by the Courant criterion for sedimentation.
Furthermore, the neglect of horizontal advection of precipitation in the
diagnostic approach is reasonable given the large grid spacing
(:math:`\sim` 100 km) and long time step (:math:`\sim`\ 15-40 min) of
GCMs. A unique aspect of this scheme is the diagnostic treatment of both
precipitation mixing ratio :math:`q_p` and number concentration
:math:`N_p`. Considering only the vertical dimension, the grid-scale
time rates of change of :math:`q_p` and :math:`N_p` are:

.. math::
   :label: eq:MG11

   
   \frac{\partial q_p}{\partial t} = \frac{1}{\rho} \frac{\partial(V_q \rho q_p)}{\partial z} + S_q

.. math::
   :label: eq:MG12

   
   \frac{\partial N_p}{\partial t} = \frac{1}{\rho} \frac{\partial(V_N \rho N_p)}{\partial z} + S_N

where :math:`z` is height, :math:`V_q` and :math:`V_N` are the mass- and
number-weighted terminal fallspeeds, respectively, and :math:`S_q` and
:math:`S_N` are the grid-mean source/sink terms for :math:`q_p` and
:math:`N_p`, respectively:

.. math::
   :label: eq:MG13

   S_q=  \left(\frac{\partial q_p}{\partial t}\right)_{auto} + \left(\frac{\partial q_p}{\partial t}\right)_{accw} + \left(\frac{\partial q_p}{\partial t}\right)_{acci} + \left(\frac{\partial q_p}{\partial t}\right)_{het} + \left(\frac{\partial q_p}{\partial t}\right)_{hom} + \left(\frac{\partial q_p}{\partial t}\right)_{mlt} + \left(\frac{\partial q_p}{\partial t}\right)_{mult} +\left(\frac{\partial q_p}{\partial t}\right)_{evap} + \left(\frac{\partial q_p}{\partial t}\right)_{coll}

.. math::
   :label: eq:MG14

   
   S_N=  \left(\frac{\partial N_p}{\partial t}\right)_{auto} + \left(\frac{\partial N_p}{\partial t}\right)_{het} + \left(\frac{\partial N_p}{\partial t}\right)_{hom} + \left(\frac{\partial N_p}{\partial t}\right)_{mlt} + \left(\frac{\partial N_p}{\partial t}\right)_{evap} + \left(\frac{\partial N_p}{\partial t}\right)_{self} +\left(\frac{\partial N_p}{\partial t}\right)_{coll}

The symbolic terms on the right-hand sides of :eq:`eq:MG13` and :eq:`eq:MG14`
are autoconversion (subscript auto), accretion of cloud water (subscript
accw), accretion of cloud ice (subscript acci), heterogeneous freezing
(subscript het), homogeneous freezing (subscript hom), melting
(subscript mlt), ice multiplication via rime splintering (subsrcipt
mult; qp only), evaporation (subscript evap), and self-collection
(subscript self; collection of rain drops by other rain drops, or snow
crystals by other snow crystals; Np only), and collection of rain by
snow (subscript coll). Formulations for these processes are described in
section 3.

In the diagnostic treatment , :math:`(\partial q_p / \partial t )` =0
and :math:`(\partial N_p / \partial t )` =0 . This allows :eq:`eq:MG11` and
:eq:`eq:MG12` to be expressed as a function of z only. The :math:`q_p` and
:math:`N_p` are therefore determined by discretizing and numerically
integrating :eq:`eq:MG11` and :eq:`eq:MG12` downward from the top of the model
atmosphere following Ghan and Easter (1992):

.. math::
   :label: eq:MG15

   
   \rho_{a,k} V_{q,k} q_{p,k} = \rho_{a,k+1} V_{q,k+1} q_{p,k+1} + \frac{1}{2} [ \rho_{a,k} S_{q,k} \delta Z_{k} +  \rho_{a,k+1} S_{q,k+1} \delta Z_{k+1}]

.. math::
   :label: eq:MG16

   
   \rho_{a,k} V_{N,k} N_{p,k} = \rho_{a,k+1} V_{N,k+1} N_{p,k+1} + \frac{1}{2} [ \rho_{a,k} S_{N,k} \delta Z_{k} +  \rho_{a,k+1} S_{N,k+1} \delta Z_{k+1}]

where :math:`k` is the vertical level (increasing with height, i.e.,
:math:`k+1` is the next vertical level above :math:`k`). Since
:math:`V_{q,k}`, :math:`S_{q,k}`, :math:`V_{N,k}`, and :math:`S_{N,k}`
depend on :math:`q_{p,k}` and :math:`N_{p,k}`, :eq:`eq:MG15` and :eq:`eq:MG16`
must be solved by iteration or some other method. The approach of Ghan
and Easter (1992) uses values of :math:`q_{p,k}` and :math:`N_{p,k}`
from the previous time step as provisional estimates in order to
calculate :math:`V_{q,k}`, :math:`V_{N,k}`, :math:`S_{p,k}`, and
:math:`S_{N,k}`. “Final” values of :math:`q_{p,k}` and :math:`N_{p,k}`
are calculated from these values of :math:`V_{q,k}`, :math:`V_{N,k}`,
:math:`S_{q,k}` and :math:`S_{N,k}` using :eq:`eq:MG15` and :eq:`eq:MG16`. Here
we employ another method that obtains provisional values of
:math:`q_{p,k}` and :math:`N_{p,k}` from :eq:`eq:MG15` and :eq:`eq:MG16`
assuming :math:`V_{q,k} \sim V_{q,k+1}` and
:math:`V_{N,k} \sim V_{N,k+1}`. It is also assumed that all source/sink
terms in :math:`S_{q,k}` and :math:`S_{N,q}` can be approximated by the
values at :math:`k+1`, except for the autoconversion, which can be
obtained directly at the k level since it does not depend on
:math:`q_{p,k}` or :math:`N_{p,k}`. If there is no precipitation flux
from the level above, then the provisional :math:`q_{p.k}` and
:math:`N_{p,k}` are calculated using autoconversion at the k level in
:math:`S_{q,k}` and :math:`S_{N,k}`; :math:`V_{q,k}` and :math:`V_{N,k}`
are estimated assuming newly-formed rain and snow particles have
fallspeeds of 0.45 m/s for rain and 0.36 m/s for snow.

Rain and snow are considered separately, and both may occur
simultaneously in supercooled conditions (hereafter subscript p for
precipitation is replaced by subscripts r for rain and s for snow). The
rain/snow particle size distributions are given by :eq:`eq:MG1`, with the
shape parameter :math:`\mu` = 0, resulting in Marshall-Palmer
(exponential) size distributions. The size distribution parameters
:math:`\lambda` and :math:`N_0` are similarly given by :eq:`eq:MG3` and
:eq:`eq:MG4` with :math:`\mu` = 0. The bulk particle density (parameter
:math:`\rho` in :eq:`eq:MG3`) is :math:`\rho` = 1000 kg m\ :math:`^{-3}` for
rain and :math:`\rho` = 100 kg m\ :math:`^{-3}` for snow following
Reisner, Rasmussen, and Bruintjes (1998).

Cloud and precipitation particle terminal fallspeeds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The mass- and number-weighted terminal fallspeeds for all cloud and
precipitation species are obtained by integration over the particle size
distributions with appropriate weighting by number concentration or
mixing ratio:

.. math::
   :label: eq:MG17

   
   V_N = \frac{\int_0^\infty \left(\frac{\rho_a}{\rho_{a0}}\right)^{0.54} aD^b \phi (D) \mathrm{d}D}{\int_0^\infty \phi (D) \mathrm{d}D} = \frac{\left(\frac{\rho_a}{\rho_{a0}}\right)^{0.54} a\Gamma ( 1 + b + \mu)}{\lambda^b \Gamma (\mu + 1)}

.. math::
   :label: eq:MG18

   
   V_q = \frac{\int_0^\infty \frac{\pi \rho}{6} \left(\frac{\rho_a}{\rho_{a0}}\right)^{0.54} aD^{b+3} \phi (D) \mathrm{d}D}{\int_0^\infty \frac{\pi \rho}{6} D^3 \phi (D) \mathrm{d}D} = \frac{\left(\frac{\rho_a}{\rho_{a0}}\right)^{0.54} a\Gamma ( 4 + b + \mu)}{\lambda^b \Gamma (\mu + 4)}

where :math:`\rho^{a0}` is the reference air density at 850 mb and 0 C,
:math:`a` and :math:`b` are empirical coefficients in the
diameter-fallspeed relationship :math:`V=aD^b` , where :math:`V` is
terminal fallspeed for an individual particle with diameter :math:`D`.
The air density correction factor is from Heymsfield and Banseemer
(2007). :math:`V_N` and :math:`V_q` are limited to maximum values of 9.1
m/s for rain and 1.2 m/s for snow. The a and b coefficients for each
hydrometeor species are given in Table 2. Note that for cloud water
fallspeeds, sub-grid variability of q is considered by appropriately
multiplying the :math:`V_N` and :math:`V_q` by the factor :math:`E`
given by :eq:`eq:MG10`.

Ice Cloud Fraction
^^^^^^^^^^^^^^^^^^

Several modifications have been made to the determination of diagnostic
fractional cloudiness in the simulations. The ice and liquid cloud
fractions are now calculated separately. Ice and liquid cloud can exist
in the same grid box. Total cloud fraction, used for radiative transfer,
is determined assuming maximum overlap between the two.

The diagnostic ice cloud fraction closure is constructed using a total
water formulation of the Slingo (1987) scheme. There is an indirect
dependence of prognostic cloud ice on the ice cloud fraction since the
in-cloud ice content is used for all microphysical processes involving
ice. The new formulation of ice cloud fraction (:math:`CF_i`) is
calculated using relative humidity (RH) based on total ice water mixing
ratio, including the ice mass mixing ratio (:math:`q_i`) and the vapor
mixing ratio (:math:`q_v`). The RH based on total ice water
(:math:`RH_{ti}`) is then :math:`RH_{ti} = (q_v+q_i)/q_{sat}` where
:math:`q_{sat}` is the saturation vapor mixing ratio over ice. Because
this is for ice clouds only, we do not include :math:`q_l` (liquid
mixing ratio). We have tested that the inclusion of :math:`q_l` does not
substantially impact the scheme (since there is little liquid present in
this regime).

Ice cloud fraction is then given by :math:`CF_i= min(1,RH_d^2)` where

.. math:: RH_d = max\left(0,\frac{RH_{ti} - RHi_{min}}{RHi_{max}-RHi_{min}}\right)

:math:`RHi_{max}` and :math:`RHi_{min}` are prescribed maximum and
minimum threshold humidities with respect to ice, set at
:math:`RHi_{max}`\ =1.1 and :math:`RHi_{min}`\ =0.8. These are
adjustable parameters that reflect assumptions about the variance of
humidity in a grid box. The scheme is not very sensitive to
:math:`RHi_{min}`. :math:`RHi_{max}` affects the total ice
supersaturation and ice cloud fraction.

With :math:`RHi_{max} = 1` and :math:`q_i = 0` the scheme reduces to the
Slingo (1987) scheme. :math:`RH_{ti}` is preferred over :math:`RH` in
:math:`RH_d` because when :math:`q_i` increases due to vapor deposition,
it reduces :math:`q_v`, and without any precipitation or sedimentation
the decrease in :math:`RH` would change diagnostic cloud fraction,
whereas :math:`RH_{ti}` is constant.

Radiative Treatment of Ice
~~~~~~~~~~~~~~~~~~~~~~~~~~

The simulations use a self consistent treatment of ice in the radiation
code. The radiation code uses as input the prognostic effective diameter
of ice from the cloud microphysics (give eq. # from above). Ice cloud
optical properties are calculated based on the modified anomalous
diffraction approximation (MADA), described in Mitchell (2000; Mitchell
2002) and Mitchell et al. (2006). The mass-weighted extinction (volume
extinction coefficient/ice water content) and the single scattering
albedo, :math:`\omega_0`, are evaluated using a look-up table. For solar
wavelengths, the asymmetry parameter :math:`g` is determined as a
function of wavelength and ice particle size and shape as described in
Mitchell, Macke, and Liu (1996a) and Nousiainen and McFarquhar (2004)
for quasi-spherical ice crystals. For terrestrial wavelengths, :math:`g`
was determined following Yang et al. (2005). An ice particle shape
recipe was assumed when calculating these optical properties. The recipe
is described in Mitchell, d’Entremont, and Lawson (2006) based on
mid-latitude cirrus cloud data from Lawson et al. (2006) and consists of
50% quasi-spherical and 30% irregular ice particles, and 20% bullet
rosettes for the cloud ice (i.e. small crystal) component of the ice
particle size distribution (PSD). Snow is also included in the radiation
code, using the diagnosed mass and effective diameter of falling snow
crystals (MG2008). For the snow component, the ice particle shape recipe
was based on the crystal shape observations reported in Lawson et al.
(2006) at -45:math:`^\circ`\ C: 7% hexagonal columns, 50% bullet
rosettes and 43% irregular ice particles.

Formulations for the microphysical processes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Activation of cloud droplets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Activation of cloud droplets, occurs on a multi-modal lognormal aerosol
size distribution based on the scheme of Abdul-Razzak and Ghan (2000).
Activation of cloud droplets occurs if :math:`N_c` decreases below the
number of active cloud condensation nuclei diagnosed as a function of
aerosol chemical and physical parameters, temperature, and vertical
velocity (see Abdul-Razzak and Ghan (2000)), and if liquid condensate is
present. We use the existing Nc as a proxy for the number of aerosols
previously activated as droplets since the actual number of activated
aerosols is not tracked as a prognostic variable from time step to time
step (for coupling with prescribed aerosol scheme). This approach is
similar to that of Lohmann et al. (1999).

Since local rather than grid-scale vertical velocity is needed for
calculating droplet activation, a sub-grid vertical velocity
:math:`w_{sub}` is derived from the square root of the Turbulent Kinetic
Energy (TKE) following Morrison and Pinto (2005):

.. math::
   :label: eq:wsub

   
   w_{sub} = \sqrt{\frac{2}{3} TKE}

where TKE is defined using a steady state energy balance eqn :eq:`eq:MG17` and
:eq:`eq:MG28` in Bretherton and Park (2009))

In regions with weak turbulent diffusion, a minimum sub-grid vertical
velocity of 10 cm/s is assumed. Some models use the value of wÕ at cloud
base to determine droplet activation in the cloud layer (e.g., Lohmann
et al. (1999)); however, because of coarse vertical and horizontal
resolution and difficulty in defining the cloud base height in GCMÕs, we
apply the :math:`w_{sub}` calculated for a given layer to the droplet
activation for that layer. Note that the droplet number may locally
exceed the number activated for a given level due to advection of Nc.
Some models implicitly assume that the timescale for droplet activation
over a cloud layer is equal to the model time step (e.g., Lohmann et al.
(1999)), which could enhance sensitivity to the time step. This
timescale can be thought of as the timescale for recirculation of air
parcels to regions of droplet activation (i.e., cloud base), similar to
the timescale for large eddy turnover; here, we assume an activation
timescale of 20 min.

Primary ice nucleation
^^^^^^^^^^^^^^^^^^^^^^

Ice crystal nucleation is based on Liu et al. (2007), which includes
homogeneous freezing of sulfate competing with heterogeneous immersion
freezing on mineral dust in ice clouds (with temperatures below
-37:math:`^\circ`\ C) (Liu and Penner 2005). Because mineral dust at
cirrus levels is very likely coated (Wiacek and Peter 2009), deposition
nucleation is not explicitly included in this work for pure ice clouds.
Immersion freezing is treated for cirrus (pure ice), but not for mixed
phase clouds. The relative efficiency of immersion versus deposition
nucleation in mixed phase clouds is an unsettled problem, and the
omission of immersion freezing in mixed phase clouds may not be
appropriate (but is implicitly included in the deposition/condensation
nucleation: see below). Deposition nucleation may act at temperatures
lower than immersion nucleation (i.e. T\ :math:`<`-25:math:`^\circ`\ C)
(Field et al. 2006), and immersion nucleation has been inferred to
dominate in mixed phase clouds (Ansmann and others 2008; Ansmann et al.
2009; Hoose and Kristjansson 2010). We have not treated immersion
freezing on soot because while Liu and Penner (2005) assumed it was an
efficient mechanism for ice nucleation, more recent studies (Kärcher et
al. 2007) indicate it is still highly uncertain.

In the mixed phase cloud regime
(-37:math:`<`\ T\ :math:`<`\ 0\ :math:`^\circ`\ C),
deposition/condensation nucleation is considered based on Meyers,
DeMott, and Cotton (1992), with a constant nucleation rate for
T\ :math:`<`-20:math:`^\circ`\ C. The Meyers, DeMott, and Cotton (1992)
parameterization is assumed to treat deposition/condensation on dust in
the mixed phase. Since it is based on observations taken at water
saturation, it should include all important ice nucleation mechanisms
(such as the immersion and deposition nucleation discussed above) except
contact nucleation, though we cannot distinguish all the specific
processes. Meyers, DeMott, and Cotton (1992) has been shown to produce
too many ice nuclei during the Mixed Phase Arctic Clouds Experiment
(MPACE) by Prenni et al. (2007). Contact nucleation by mineral dust is
included based on Young (1974) and related to the coarse mode dust
number. It acts in the mixed phase where liquid droplets are present and
and includes Brownian diffusion as well as phoretic forces.
Hallet-Mossop secondary ice production due to accretion of drops by snow
is included following Cotton et al. (1986).

In the Liu and Penner (2005) scheme, the number of ice crystals
nucleated is a function of temperature, humidity, sulfate, dust and
updraft velocity, derived from fitting the results from cloud parcel
model experiments. A threshold :math:`RH_w` for homogeneous nucleation
was fitted as a function of temperature and updraft velocity (see Liu et
al. (2007), equation 6). For driving the parameterization, the sub-grid
velocity for ice (:math:`w_{sub}`) is derived following
ewuation :eq:`eq:wsub`. A minimum of 0.2 m s\ :math:`^{-1}` is set for ice
nucleation.

It is also implicitly assumed that there is some variation in humidity
over the grid box. For purposes of ice nucleation, nucleation rates for
a grid box are estimated based on the ‘most humid portion’ of the
grid-box. This is assumed to be the grid box average humidity plus a
fixed value (20% RH). This implies that the ‘local’ threshold
supersaturation for ice nucleation will be reached at a grid box mean
value 20% lower than the RH process threshold value. This represents
another gross assumption about the RH variability in a model grid box
and is an adjustable parameter in the scheme. In the baseline case,
sulfate for homogeneous freezing is taken as the portion of the Aitken
mode particles with radii greater than 0.1 microns, and was chosen to
better reproduce observations (this too can be adjusted to alter the
balance of homogeneous freezing). The size represents the large tail of
the Aitken mode. In the upper troposphere there is little sulfate in the
accumulation mode (it falls out), and almost all sulfate is in the
Aitken mode.

Deposition/sublimation of ice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Several cases are treated below that involve ice deposition in ice-only
clouds or mixed-phase clouds in which all liquid water is depleted
within the time step. Case [1] Ice only clouds in which
:math:`q_v > q_{vi}*` where :math:`q_v` is the grid mean water vapor
mixing ratio and :math:`q_{vi}*` is the local vapor mixing ratio at ice
saturation (:math:`q_{sat}`). Case [2] is the same as case [1]
(:math:`q_v > q_{vi}*`) but there is existing liquid water depleted by
the Bergeron-Findeisen process (:math:`ber`). Case [3], liquid water is
depleted by the Bergeron-Findeisen process and the local liquid is less
than local ice saturation (:math:`q_v* \le q_{vi}*`). In Case [4]
:math:`q_v < q_{vi}*` so sublimation of ice occurs.

Case [1]: If the ice cloud fraction is larger than the liquid cloud
fraction (including grid cells with ice but no liquid water), or if all
new and existing liquid water in mixed-phase clouds is depleted via the
Bergeron-Findeisen process within the time step, then vapor depositional
ice growth occurs at the expense of water vapor. In the case of a grid
cell where ice cloud fraction exceeds liquid cloud fraction, vapor
deposition in the pure ice cloud portion of the cell is calculated
similarly to eq. [21] in MG08:

.. math::
   :label: eq:dep

   
   \left(\frac{\partial q_i}{\partial t }\right)_{dep}=\frac{( q_v-q_{vi}*)}{\Gamma_p \tau}, q_v > q_{vi}*

where :math:`\Gamma_p = 1 + \frac{L_s}{c_p}\frac{dq_{vi}}{dT}` is the
psychrometric correction to account for the release of latent heat,
:math:`L_s` is the latent heat of sublimation, :math:`c_p` is the
specific heat at constant pressure, :math:`\frac{dq_{vi}}{dT}` is the
change of ice saturation vapor pressure with temperature, and
:math:`\tau` is the supersaturation relaxation timescale associated with
ice deposition given by eq. :eq:`22` in MG08 (a function of ice crystal
surface area and the diffusivity of water vapor in air). The assumption
for pure ice clouds is that the in-cloud vapor mixing ratio for
deposition is equal to the grid-mean value. The same assumption is used
in Liu et al. (2007), and while it is uncertain, it is the most
straightforward. Thus we do not consider sub-grid variability of water
vapor for calculating vapor deposition in pure ice-clouds.

The form of the deposition rate in equation :eq:`eq:dep` differs from that
used by Rotstayn, Ryan, and Katzfey (2000) and Liu et al. (2007) because
they considered the increase in ice mixing ratio :math:`q_i` due to
vapor deposition during the time step, and formulated an implicit
solution based on this consideration (see eq. :eq:`6` in Rotstayn, Ryan, and
Katzfey (2000)). However, these studies did not consider sinks for the
ice due to processes such as sedimentation and conversion to
precipitation when formulating their implicit solution; these sink terms
may partially (or completely) balance the source for the ice due to
vapor deposition. Thus, we use a simple explicit forward-in-time
solution that does not consider changes of :math:`q_i` within the
microphysics time step.

Case [2]: When all new and existing liquid water is depleted via the
Bergeron-Findeisen process (:math:`ber`) within the time step, the vapor
deposition rate is given by a weighted average of the values for growth
in mixed phase conditions prior to the depletion of liquid water (first
term on the right hand side) and in pure ice clouds after depletion
(second term on the right hand side):

.. math::
   :label: eq:dep2

   
   \left(\frac{\partial q_i}{\partial t }\right)_{dep}=\frac{q_c*}{\Delta t} + \left(1- \frac{q_c*}{\Delta t}\left(\frac{\partial q_i}{\partial t}\right)_{ber}^{-1}\right)\left(\frac{( q_v*-q_{vi}*)}{\Gamma_p \tau}\right), q_v > q_{vi}*

where :math:`q_c*` is the sum of existing and new liquid condensate
mixing ratio, :math:`\Delta t` is the model time step,
:math:`\left(\frac{\partial q_i}{\partial t}\right)_{ber}` is the ice
deposition rate in the presence of liquid water (i.e., assuming vapor
mixing ratio is equal to the value at liquid saturation) as described
above, and :math:`q_v*` is an average of the grid-mean vapor mixing
ratio and the value at liquid saturation.

Case [3]: If :math:`q_v* \leq q_{vi}*` then it is assumed that no
additional ice deposition occurs after depletion of the liquid water.
The deposition rate in this instance is given by:

.. math::
   :label: eq:dep3

   
   \left(\frac{\partial q_i}{\partial t}\right)_{dep}=\left(\frac{q_c*}{\Delta t}\right), q_v* \leq q_{vi}*

Case [4]: Sublimation of pure ice cloud occurs when the grid-mean water
vapor mixing ratio is less than value at ice saturation. In this case
the sublimation rate of ice is given by:

.. math::
   :label: eq:sub

   
   \left(\frac{\partial q_i}{\partial t}\right)_{sub}=\frac{( q_v-q_{vi}*)}{\Gamma_p \tau}, q_v < q_{vi}*

Again, the use of grid-mean vapor mixing ratio in equation :eq:`eq:sub`
follows the assumption of Liu et al. (2007) that the in-cloud
:math:`q_v` is equal to the grid box mean in pure ice clouds. Grid-mean
deposition and sublimation rates are given by the in-cloud values for
pure ice or mixed-phase clouds described above, multiplied by the
appropriate ice or mixed-phase cloud fraction. Finally, ice deposition
and sublimation are limited to prevent the grid-mean mixing ratio from
falling below the value for ice saturation in the case of deposition and
above this value in the case of sublimation.

Cloud water condensation and evaporation are given by the bulk closure
scheme within the cloud macrophysics scheme, and therefore not described
here.

Conversion of cloud water to rain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Autoconversion of cloud droplets and accretion of cloud droplets by rain
is given by a version of the Khairoutdinov and Kogan (2000) scheme that
is modified here to account for sub-grid variability of cloud water
within the cloudy part of the grid cell as described previously in
section 2.1. Note that the Khairoutdinov and Kogan scheme was originally
developed for boundary layer stratocumulus, but is applied here to all
stratiform cloud types.

The grid-mean autoconversion and accretion rates are found by replacing
the qc in Eqs. (29) and (33) of Khairoutdinov and Kogan (2000) with
:math:`P(q_c^{\prime\prime})` given by equation :eq:`eq:MG8` here,
integrating the resulting expressions over the cloud water PDF, and
multiplying by the cloud fraction. This yields

.. math::
   :label: eq:MG27

   
   \left(\frac{\partial q_c}{\partial t}\right)_{auto} = -F_{cld} \frac{\Gamma(\nu + 2.47)}{\Gamma(\nu)\nu^{2.47}} 1350 q_c^{\prime 2.47} N_c^{\prime -1.79}

.. math::
   :label: eq:MG28

   
   \left(\frac{\partial q_c}{\partial t}\right)_{accr} = -F_{cld} \frac{\Gamma(\nu + 1.15)}{\Gamma(\nu)\nu^{1.15}} 67 (q_c^{\prime} q_r^{\prime})^{1.15}

The changes in qr due to autoconversion and accretion are given by
:math:`(\partial q_r / \partial t)_{auto} = -(\partial q_c / \partial t)_{auto}`
and
:math:`(\partial q_r / \partial t)_{accr} = -(\partial q_c / \partial t)_{accr}`.
The changes in :math:`N_c` and :math:`N_r` due to autoconversion and
accretion :math:`(\partial N_c / \partial t)_{auto}`,
:math:`(\partial N_r / \partial t)_{auto}`,
:math:`(\partial N_c / \partial t)_{accr}`, are derived from Eqs. (32)
and (35) in Khairoutdinov and Kogan (2000). Since accretion is nearly
linear with respect to :math:`q_c`, sub-grid variability of cloud water
is much less important for accretion than it is for autoconversion.

Note that in the presence of a precipitation flux into the layer from
above, new drizzle drops formed by cloud droplet autoconversion would be
accreted rapidly by existing precipitation particles (rain or snow)
given collection efficiencies near unity for collision of drizzle with
rain or snow (e.g., Pruppacher and Klett (1997)). This may be especially
important in models with low vertical resolution, since they cannot
resolve the rapid growth of precipitation that occurs over distances
much less than the vertical grid spacing. Thus, if the rain or snow
mixing ratio in the next level above is greater than 10-6 g kg-1, we
assume that autoconversion produces an increase in rain mixing ratio but
not number concentration (since the newly-formed drops are assumed to be
rapidly accreted by the existing precipitation). Otherwise,
autoconversion results in a source of both rain mixing ratio and number
concentration.

Conversion of cloud ice to snow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The autoconversion of cloud ice to form snow is calculated by
integration of the cloud ice mass- and number-weighted size
distributions greater than some specified threshold size, and
transferring the resulting mixing ratio and number into the snow
category over some specified timescale, similar to Ferrier (1994). The
grid-scale changes in qi and Ni due to autoconversion are

.. math::
   :label: eq:MG29

   
   \left(\frac{\partial q_i}{\partial t}\right)_{auto} = -F \frac{\pi \rho_i N_{0i}}{6 \tau_{auto}}  \left[ \frac{D_{cs}^3}{\lambda_i} +  \frac{3D_{cs}^2}{\lambda_i^2}  + \frac{6D_{cs}}{\lambda_i^3} +\frac{6D}{\lambda_i^4} \right] \exp^{- \lambda_i D_{cs}}

.. math::
   :label: eq:MG30

   
   \left(\frac{\partial N_i}{\partial t}\right)_{auto} = -F \frac{N_{0i}}{\lambda_i \tau_{auto}}  \exp^{- \lambda_i D_{cs}}

where :math:`D_{cs}` = 200 :math:`\mu`\ m is the threshold size
separating cloud ice from snow, :math:`\rho_i` is the bulk density of
cloud ice, and :math:`\tau_{auto}` = 3 min is the assumed autoconversion
timescale. Note that this formulation assumes the shape parameter
:math:`\mu` = 0 for the cloud ice size distribution; different
formulation must be used for other values of :math:`\mu`. The changes in
:math:`q_s` and :math:`N_s` due to autoconversion are given by
:math:`(\partial q_s / \partial t)_{auto} = -(\partial q_i / \partial t)_{auto}`
and
:math:`(\partial N_s / \partial t)_{auto} = -(\partial N_i / \partial t)_{auto}`
.

Accretion of :math:`q_i` and :math:`N_i` by snow
:math:`(\partial q_i / \partial t)_{accs}`,
:math:`(\partial N_i/ \partial t)_{accs}`,
:math:`(\partial q_s / \partial t)_{acci}`, and
:math:`(\partial q_s / \partial t)_{acci} = -(\partial q_i / \partial t)_{accs}`
, are given by the continuous collection equation following Lin, Farley,
and Orville (1983), which assumes that the fallspeed of snow :math:`\gg`
cloud ice fallspeed. The collection efficiency for collisions between
cloud ice and snow is 0.1 following Reisner, Rasmussen, and Bruintjes
(1998). Newly- formed snow particles formed by cloud ice autoconversion
are not assumed to be rapidly accreted by existing snowflakes, given
aggregation efficiencies typically much less than unity (e.g., Field,
Heymsfield, and Bansemer (2007)).

Other collection processes
^^^^^^^^^^^^^^^^^^^^^^^^^^

The accretion of :math:`q_c` and :math:`N_c` by snow
:math:`(\partial q_c / \partial t)_{accs}`,
:math:`(\partial N_c/ \partial t)_{accs}`, and
:math:`(\partial q_s / \partial t)_{accw} = -(\partial q_c / \partial t)_{accs}`
are given by the continuous collection equation. The collection
efficiency for droplet-snow collisions is a function of the Stokes
number following Thompson, Rasmussen, and Manning (2004) and thus
depends on droplet size. Self-collection of snow,
:math:`(\partial N_s/ \partial t)_{self}` follows Reisner, Rasmussen,
and Bruintjes (1998) using an assumed collection efficiency of 0.1.
Self-collection of rain\ :math:`(\partial N_r/ \partial t)_{self}`
follows Beheng (1994). Collisions between rain and cloud ice, cloud
droplets and cloud ice, and self-collection of cloud ice are neglected
for simplicity. Collection of :math:`q_r` and :math:`N_r` by snow in
subfreezing conditions,
:math:`(\partial q_r / \partial t)_{coll} = -(\partial q_s / \partial t)_{coll}`
and :math:`(\partial N_r/ \partial t)_{coll}`, is given by Ikawa and
Saito (1990) assuming collection efficiency of unity.

Freezing of cloud droplets and rain and ice multiplication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Heterogeneous freezing of cloud droplets and rain to form cloud ice and
snow, respectively, occurs by immersion freezing following Bigg (1953),
which has been utilized in previous microphysics schemes (e.g., Reisner,
Rasmussen, and Bruintjes (1998), see Eq. A.22, A.55, A.56; Morrison,
Curry, and Khvorostyanov (2005); Thompson et al. (2008)). Here the
freezing rates are integrated over the mass- and number-weighted cloud
droplet and rain size distributions and the impact of sub-grid cloud
water variability is included as described previously. Homogeneous
freezing of cloud droplets to form cloud ice occurs instantaneously at
-40:math:`^\circ`\ C. All rain is assumed to freeze instantaneously at
-5:math:`^\circ`\ C.

Contact freezing of cloud droplets by mineral dust is included based on
Young (1974) and related to the coarse mode dust number. It acts in the
mixed phase where liquid droplets are present and includes Brownian
diffusion as well as phoretic forces. Hallet-Mossop ice multiplication
(secondary ice production) due to accretion of drops by snow is included
following Cotton et al. (1986). This represents a sink term for snow
mixing ratio and source term for cloud ice mixing ratio and number
concentration.

Melting of cloud ice and snow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For simplicity, detailed formulations for heat transfer during melting
of ice and snow are not included. Melting of cloud ice occurs
instantaneously at 0\ :math:`^\circ`\ C. Melting of snow occurs
instantaneously at +2\ :math:`^\circ`\ C. We have tested the sensitivity
of both single- column and global results to changing the specified snow
melting temperature from +2\ :math:`^\circ` to 0\ :math:`^\circ`\ C and
found no significant changes.

Evaporation/sublimation of precipitation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Evaporation of rain and sublimation of snow,
:math:`(\partial q_s / \partial t)_{evap}` and
:math:`(\partial q_r / \partial t)_{evap}`, are given by diffusional
mass balance in subsaturated conditions Lin, Farley, and Orville (1983),
including ventilation effects. Evaporation of precipitation occurs
within the region of the grid cell containing precipitation but outside
of the cloudy region. The fraction of the grid cell with evaporation of
precipitation is therefore , where :math:`F_{pre}` is the precipitation
fraction. :math:`F_{pre}` is calculated assuming maximum cloud overlap
between vertical levels, and neglecting tilting of precipitation shafts
due to wind shear (:math:`F_{pre} = F_{cld}` at cloud top). The
out-of-cloud water vapor mixing ratio is given by

.. math::
   :label: eq:MG31

   
   q_{clr} = \frac{q_v - F_{cld} q_s(T)}{1-F_{cld}}, F_{cld} < 1

where :math:`q_s(T)` is the in-cloud water vapor mixing ratio after bulk
condensation/evaporation of cloud water and ice as described previously.
As in the older CAM3 microphysics parameterization,
condensation/deposition onto rain/snow is neglected. Following Morrison,
Curry, and Khvorostyanov (2005), the evaporation/sublimation of
:math:`N_r` and :math:`N_s`, :math:`(\partial N_r / \partial t)_{evap}`
and :math:`(\partial N_s / \partial t)_{evap}` , is proportional to the
reduction of :math:`q_r` and :math:`q_s` during evaporation/sublimation.

Sedimentation of cloud water and ice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The time rates of change of q and N for cloud water and cloud ice due to
sedimentation, :math:`(\partial q_c / \partial t)_{sed}` ,
:math:`(\partial q_i / \partial t)_{sed}`,
:math:`(\partial N_c / \partial t)_{sed}`, and
:math:`(\partial N_i / \partial t)_{sed}` , are calculated with a
first-order forward-in-time-backward-in-space scheme. Numerical
stability for cloud water and ice sedimentation is ensured by
sub-stepping the time step, although these numerical stability issues
are insignificant for cloud water and ice because of the low terminal
fallspeeds (:math:`\ll` 1 m/s). We assume that the sedimentation of
cloud water and ice results in evaporation/sublimation when the cloud
fraction at the level above is larger than the cloud fraction at the
given level (i.e., a sedimentation flux from cloudy into clear regions),
with the evaporation/condensate rate proportional to the difference in
cloud fraction between the levels.

Convective detrainment of cloud water and ice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ratio of ice to total cloud condensate detrained from the convective
parameterizations, Fdet, is a linear function of temperature between
-40:math:`^\circ` C and -10:math:`^\circ` C; :math:`F_{det}` = 1 at T
:math:`<` -40:math:`^\circ` C, and Fdet = 0 at T :math:`>`
-10:math:`^\circ` C. Detrainment of number concentration is calculated
by assuming a mean volume radius of 8 and 32 micron for droplets and
cloud ice, respectively.

Numerical considerations
^^^^^^^^^^^^^^^^^^^^^^^^

To ensure conservation of both q and N for each species, the magnitudes
of the various sink terms are reduced if the provisional q and N are
negative after stepping forward in time. This approach ensures critical
water and energy balances in the model, and is similar to the approach
employed in other bulk microphysics schemes (e.g., Reisner, Rasmussen,
and Bruintjes (1998). Inconsistencies are possible because of the
separate treatments for N and q, potentially leading to unrealistic mean
cloud and precipitation particle sizes. For consistency, N is adjusted
if necessary so that mean (number-weighted) particle diameter ( )
remains within a specified range of values for each species. Limiting to
a maximum mean diameter can be thought of as an implicit
parameterization of particle breakup.

For the diagnostic precipitation, the source terms for q and N at a
given vertical level are adjusted if necessary to ensure that the
vertical integrals of the source terms (from that level to the model
top) are positive. In other words, we ensure that at any given level,
there isnÕt more precipitation removed (both in terms of mixing ratio
and number concentration) than is available falling from above (this is
also the case in the absence of any sources/sinks at that level). This
check and possible adjustment of the precipitation and cloud water also
ensures conservation of the total water and energy. Our simple
adjustment procedure to ensure conservation could potentially result in
sensitivity to time step, although as described in section 3, time
truncation errors are minimized with appropriate sub-stepping.

Melting rates of cloud ice and snow are limited so that the temperature
of the layer does not decrease below the melting point (i.e., in this
instance an amount of cloud ice or snow is melted so that the
temperature after melting is equal to the melting point). A similar
approach is applied to ensure that homogeneous freezing does increase
the temperature above homogeneous freezing threshold.

Parameterization of Cloud Fraction
----------------------------------

Cloud amount (or cloud fraction), and the associated optical properties,
are evaluated via a diagnostic method in |cam|. The basic approach is similar
to that employed in CAM3. The diagnosis of cloud fraction is a
generalization of the scheme introduced by Slingo (1987), with
variations described in Hack et al. (1993; Kiehl et al. 1998), and Rasch
and Kristjánsson (1998). Cloud fraction depends on relative humidity,
atmospheric stability, water vapor and convective mass fluxes. Three
types of cloud are diagnosed by the scheme: low-level marine stratus
(:math:`{{\mathcal C}}_{st}`), convective cloud (:math:`{{\mathcal C}}_{cir}`),
and layered cloud (:math:`{{\mathcal C}}_c`). Layered clouds form when the
relative humidity exceeds a threshold value which varies according to
pressure. The diagnoses of these cloud types are described in more
detail in the following paragraphs.

Marine stratocumulus clouds are diagnosed using an empirical
relationship between marine stratocumulus cloud fraction and the
stratification between the surface and 700mb derived by Klein and
Hartmann (1993). The CCM3 parameterization for stratus cloud fraction
over oceans has been replaced with

.. math::
   :label: 4.a.5

   {{\mathcal C}}_{st} = \min\biggl\lbrace 1., \max\bigl[0.,
               (\theta_{700}-\theta_s)*.057-.5573 \bigr] \biggr\rbrace
   

:math:`\theta_{700}` and :math:`\theta_s` are the potential temperatures
at 700 mb and the surface, respectively. The cloud is assumed to be
located in the model layer below the strongest stability jump between
750 mb and the surface. If no two layers present a stability in excess
of -0.125 K/mb, no cloud is diagnosed. In areas where terrain filtering
has produced non-zero ocean elevations, the sea surface temperature used
for this computation is reduced from the true sea surface elevation to
the model surface elevation according to the lapse rate of the U.S.
Standard Atmosphere (-6.5 :math:`^\circ`\ C/km).

Convective cloud fraction in the model is related to updraft mass flux
in the deep and shallow cumulus schemes according to a functional form
suggested by Xu and Krueger (1991):

.. math:: {{\mathcal C}}_{shallow} = k_{1,shallow} ln(1.0+k_2 M_{c,shallow},0.3 )

.. math:: {{\mathcal C}}_{deep}     = k_{1_deep} ln(1.0+k_2 M_{c,deep},0.6 )

where :math:`k_{1,shallow}` and :math:`k_{1,deep}` are adjustable
parameters given in Appendix [adjustableparameters], :math:`k_2 = 500`,
and :math:`M_c` is the convective mass flux at the given model level.
The combined convective cloud fraction :math:`C_{cir}`, is further
approximated as

.. math:: {{\mathcal C}}_{cir} ={\rm min} \left(0.8, {{\mathcal C}}_{shallow} + {{\mathcal C}}_{deep} \right).

The remaining cloud types are diagnosed on the basis of relative
humidity, according to

.. math::
   :label: 4.a.4

   {{\mathcal C}}_c = \left( \frac{RH - RH_{\min}} {1 - RH_{\min}} \right)^{2}
   

The threshold relative humidity :math:`RH_{\min}` is set according to
pressure :math:`p` as

.. math::

   RH_{\min} =
     \begin{cases}
       RH_{\min}^{low} & p > 750 mb \\ RH_{\min}^{low} +
       (RH_{\min}^{high}-RH_{\min}^{low})\frac{p - 750 mb}{p_{mid}-750
       mb} & p_{mid} < p < 750 mb \\ RH_{\min}^{high} & p < p_{mid}
     \end{cases}

where :math:`p_{mid}` in an adjustable parameter denoting the minimum
pressure for a linear ramp from the low cloud threshold to the high
cloud threshold. At present this ramp is implemented only in one
configuration of the model; other versions have a step function achieved
by setting :math:`p_{mid} = 750` mb. :math:`RH_{\min}^{low}`,
:math:`RH_{\min}^{high}`, and :math:`p_{mid}` are specified as in
Appendix [adjustableparameters]. Also, the parameter
:math:`RH_{\min}^{low}` is adjusted over land by :math:`-0.10`. This
distinction is made to account for the increased sub-grid-scale
variability of the water vapor field due to inhomogeneities in the land
surface properties and subgrid orographic effects. In |cam| a modification is
made to the layered cloud fraction to prevent extensive cloud decks that
have zero or near-zero condensate in cold climates. The adjustment is
based on Vavrus and Waliser (2008) and reduces the diagnosed low cloud
fraction if grid mean water vapor is less than 3 g/kg according to

.. math:: C_c^{low} = C_c^{low}max(0.15,min(1,{{\mathcal C}}{q_{v}}{0.003}))

This modifiation has a significant impact during winter time in high
latitude regions.

The total cloud :math:`{{\mathcal C}}_{tot}` within each volume is then
diagnosed as

.. math::

   {{\mathcal C}}_{tot} = {\rm min} \left( {\rm max}\left( {{\mathcal C}}_{c},{{\mathcal C}}_{st}\right)
                                  + {{\mathcal C}}_{cir},  1 \right) .

This is equivalent to a maximum overlap assumption of cloud types within
each gridbox. The condensate value is assumed uniform within any and all
types of cloud within each grid box. In order to prevent inconsistent
values of total cloud fraction and condensate being passed to the
radiation parameterization in the |cam| a second updated cloud fraction
calculation is performed. Cloud fraction and therefore relative humidity
are now consitent with condensate values on entry to the radiation
parameterization. This vastly reduces the frequency of ’empty clouds’
seen in the CAM3, where cloud condesate was zero and yet cloud had been
diagnosed to exists due to an inconsistant relative humidity.

Aerosols
--------

Two different modal representations of the aerosol were implemented in
CAM5. A 7-mode version of the modal aerosol model (MAM-7) serves as a
benchmark for the further simplification. It includes Aitken,
accumulation, primary carbon, fine dust and sea salt and coarse dust and
sea salt modes (:ref:`aero_species_mam7`). Within a single
mode, for example the accumulation mode, the mass mixing ratios of
internally-mixed sulfate, ammonium, secondary organic aerosol (SOA),
primary organic matter (POM) aged from the primary carbon mode, black
carbon (BC) aged from the primary carbon mode, sea salt, and the number
mixing ratio of accumulation mode particles are predicted. Primary
carbon (OM and BC) particles are emitted to the primary carbon mode and
aged to the accumulation mode due to condensation of
:math:`\mathrm{H_{2}SO_{4}}`, :math:`\mathrm{NH_{3}}` and SOA (gas) and
coagulation with Aitken and accumulation mode (see section below).

Aerosol particles exist in different attachment states. We mostly think
of aerosol particles that are suspended in air (either clear or cloudy
air), and these are referred to as interstitial aerosol particles.
Aerosol particles can also be attached to (or contained within)
different hydrometeors, such as cloud droplets. In CAM5, the
interstitial aerosol particles and the aerosol particles in stratiform
cloud droplets (referred to as cloud-borne aerosol particles) are both
explicitly predicted, as in (**???**). The interstitial aerosol particle
species are stored in the :math:`{q}` array of the state variable and
are transported in 3 dimensions. The cloud-borne aerosol particle
species are stored in the :math:`{qqcw}` array of the physics buffer and
are not transported (except for vertical turbulent mixing), which saves
computer time but has little impact on their predicted values (**???**).

Aerosol water mixing ratio associated with interstitial aerosol for each
mode is diagnosed following Kohler theory (see water uptake below),
assuming equilibrium with the ambient relative humidity. It also is not
transported in 3 dimensions, and is held in the :math:`{qaerwat}` array
of the physics buffer.

The size distributions of each mode are assumed to be log-normal, with
the mode dry or wet radius varying as number and total dry or wet volume
change, and standard deviation prescribed as given in
:ref:`aero_species_mam7`. The total number of transported
aerosol species is 31 for MAM-7. The transported gas species are
:math:`\mathrm{SO_{2}}`, :math:`\mathrm{H_{2}O_{2}}`, DMS,
:math:`\mathrm{H_{2}SO_{4}}`, :math:`\mathrm{NH_{3}}`, and SOA (gas).

For long-term (multiple century) climate simulations a 3-mode version of
MAM (MAM-3) is also developed which has only Aitken, accumulation and
coarse modes (`aero_species_mam3`_). For MAM-3 the
following assumptions are made: (1) primary carbon is internally mixed
with secondary aerosol by merging the primary carbon mode with the
accumulation mode; (2) the coarse dust and sea salt modes are merged
into a single coarse mode based on the assumption that the dust and sea
salt are geographically separated. This assumption will impact dust
loading over the central Atlantic transported from Sahara desert because
the assumed internal mixing between dust and sea salt there will
increase dust hygroscopicity and thus wet removal; (3) the fine dust and
sea salt modes are similarly merged with the accumulation mode; and (4)
sulfate is partially neutralized by ammonium in the form of
:math:`\mathrm{NH_{4}HSO_{4}}`, so ammonium is effectively prescribed
and :math:`\mathrm{NH_{3}}` is not simulated. We note that in MAM-3 we
predict the mass mixing ratio of sulfate aerosol in the form of
:math:`\mathrm{NH_{4}HSO_{4}}` while in MAM-7 it is in the form of
:math:`\mathrm{SO_{4}}`. The total number of transported aerosol tracers
in MAM-3 is 15.

The time evolution of the interstitial aerosol mass
(:math:`\mathrm{M^{a}_{i,j}}`) and number (:math:`\mathrm{N^{a}_{j}}`)
for the i-th species and j-th mode is described in the following
equations:

.. math::

   \begin{aligned}
   &&\frac{\partial M^{a}_{i,j}}{\partial t} + \frac{1}{\rho} \nabla \cdot [\rho \mathbf{u} M^{a}_{i,j}] =  
   \left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{conv} +
   \left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{diffus}  \\ \nonumber
   &&\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad  
   +\left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{nuc} + 
   \left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{cond} + 
   \left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{activ}  +
   \left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{resus} \\ \nonumber
   &&\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad  
   +\left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{emis} + 
   \left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{sedime} +
   \left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{drydep} +
   \left(\frac{\partial M^{a}_{i,j}}{\partial t}\right)_{imp\_scav} \\ \nonumber\end{aligned}

.. math::

   \begin{aligned}
   &&\frac{\partial N^{a}_{j}}{\partial t} + \frac{1}{\rho} \nabla \cdot [\rho \mathbf{u} N^{a}_{j}] =  
   \left(\frac{\partial N^{a}_{j}}{\partial t}\right)_{conv} +
   \left(\frac{\partial N^{a}_{j}}{\partial t}\right)_{diffus}  \\ \nonumber
   &&\quad\quad\quad\quad\quad\quad\quad\quad\quad
   +\left(\frac{\partial N^{a}_{j}}{\partial t}\right)_{nuc} +
   \left(\frac{\partial N^{a}_{j}}{\partial t}\right)_{coag} + 
   \left(\frac{\partial N^{a}_{j}}{\partial t}\right)_{activ}  +
   \left(\frac{\partial N^{a}_{j}}{\partial t}\right)_{resus} \\ \nonumber
   &&\quad\quad\quad\quad\quad\quad\quad\quad\quad
   +\left(\frac{\partial N^{a}_{j}}{\partial t}\right)_{emis} +
   \left(\frac{\partial N^{a}_{i,j}}{\partial t}\right)_{sedime} +
   \left(\frac{\partial N^{a}_{j}}{\partial t}\right)_{drydep} +
   \left(\frac{\partial N^{a}_{j}}{\partial t}\right)_{imp\_scav} \\ \nonumber\end{aligned}

Similarly, the time evolution for the cloud-borne aerosol mass
(:math:`\mathrm{M^{c}_{i,j}}`) and number (:math:`\mathrm{N^{c}_{j}}`)
is described as:

.. math::

   \begin{aligned}
   &&\frac{\partial M^{c}_{i,j}}{\partial t} =  
   \left(\frac{\partial M^{c}_{i,j}}{\partial t}\right)_{conv} +
   \left(\frac{\partial M^{c}_{i,j}}{\partial t}\right)_{diffus}  \\ \nonumber
   &&\quad\quad\quad
   +\left(\frac{\partial M^{c}_{i,j}}{\partial t}\right)_{chem} +
   \left(\frac{\partial M^{c}_{i,j}}{\partial t}\right)_{activ} +
   \left(\frac{\partial M^{c}_{i,j}}{\partial t}\right)_{resus} \\ \nonumber
   &&\quad\quad\quad 
   +\left(\frac{\partial M^{c}_{i,j}}{\partial t}\right)_{sedime} +
   \left(\frac{\partial M^{c}_{i,j}}{\partial t}\right)_{drydep} +
   \left(\frac{\partial M^{c}_{i,j}}{\partial t}\right)_{nuc\_scav} \\ \nonumber\end{aligned}

.. math::

   \begin{aligned}
   &&\frac{\partial N^{c}_{j}}{\partial t}  =  
   \left(\frac{\partial N^{c}_{j}}{\partial t}\right)_{conv} +
   \left(\frac{\partial N^{c}_{j}}{\partial t}\right)_{diffus}  \\ \nonumber
   &&\quad\quad
   +\left(\frac{\partial N^{c}_{j}}{\partial t}\right)_{activ} +
   \left(\frac{\partial N^{c}_{j}}{\partial t}\right)_{resus} \\ \nonumber
   &&\quad\quad
   +\left(\frac{\partial N^{c}_{j}}{\partial t}\right)_{sedime} + 
   \left(\frac{\partial N^{c}_{j}}{\partial t}\right)_{drydep} + 
   \left(\frac{\partial N^{c}_{j}}{\partial t}\right)_{nuc\_scav} \\ \nonumber\end{aligned}

where t is time, :math:`\mathbf{u}` is the 3D wind vector, and
:math:`\rho` is the air density. The symbolic terms on the right hand
side represent the source/sink terms for :math:`\mathrm{M_{i,j}}` and
:math:`\mathrm{N_{j}}` (**???**).

Emissions
~~~~~~~~~

Anthropogenic (defined here as originating from industrial, domestic and
agriculture activity sectors) emissions are from the (**???**) IPCC AR5
emission data set. Emissions of black carbon (BC) and organic carbon
(OC) represent an update of (**???**) and (**???**). Emissions of sulfur
dioxide are an update of Smith, Pitcher, and Wigley (2001; **???**).

The IPCC AR5 emission data set includes emissions for anthropogenic
aerosols and precursor gases: :math:`\mathrm{SO_{2}}`, primary OM (POM),
and BC. However, it does not provide injection heights and size
distributions of primary emitted particles and precursor gases for which
we have followed the AEROCOM protocols (**???**). We assumed that 2.5%
by molar of sulfur emissions are emitted directly as primary sulfate
aerosols and the rest as :math:`\mathrm{SO_{2}}` (**???**). Sulfur from
agriculture, domestic, transportation, waste, and shipping sectors is
emitted at the surface while sulfur from energy and industry sectors is
emitted at 100-300 m above the surface, and sulfur from forest fire and
grass fire is emitted at higher elevations (0-6 km). Sulfate particles
from agriculture, waste, and shipping (surface sources), and from
energy, industry, forest fire and grass fire (elevated sources) are put
in the accumulation mode, and those from domestic and transportation are
put in the Aitken mode. POM and BC from forest fire and grass fire are
emitted at 0-6 km, while those from other sources (domestic, energy,
industry, transportation, waste, and shipping) are emitted at surface.
Injection height profiles for fire emissions are derived from the
corresponding AEROCOM profiles, which vary spatially and temporally.
Mass emission fluxes for sulfate, POM and BC are converted to number
emission fluxes for Aitken and accumulation mode at surface or at higher
elevations based on AEROCOM prescribed lognormal size distributions as
summarized in Table :ref:`table_aerocom_emis`.

The IPCC AR5 data set also does not provide emissions of natural
aerosols and precursor gases: volcanic sulfur, DMS,
:math:`\mathrm{NH_{3}}`, and biogenic volatile organic compounds (VOCs).
Thus AEROCOM emission fluxes, injection heights and size distributions
for volcanic :math:`\mathrm{SO_{2}}` and sulfate and for DMS flux at
surface are used. The emission flux for :math:`\mathrm{NH_{3}}` is
prescribed from the MOZART-4 data set (**???**). Emission fluxes for
isoprene, monoterpenes, toluene, big alkenes, and big alkanes, which are
used to derive SOA (gas) emissions (see below), are prescribed from the
MOZART-2 data set (**???**). These emissions represent late 1990’s
conditions. For years prior to 2000, we use anthropogenic non-methane
volatile organic compound (NMVOC) emissions from IPCC AR5 data set and
scale the MOZART toluene, bigene, and big alkane emissions by the ratio
of year-of-interest NMVOC emissions to year 2000 NMVOC emissions.

The emission of sea salt aerosols from the ocean follows the
parameterization by (**???**) for aerosols with geometric diameter
:math:`<` 2.8 :math:`\mu`\ m. The total particle flux :math:`{F_{0}}` is
described by

.. math:: \frac{dF_{0}}{dlogD_{p}}=\Phi W =(A_{k}T_{w}+B_{k})W

where :math:`{D_{p}}` is the particle diameter, :math:`{T_{w}}` is the
water temperature and :math:`{A_{k}}` and :math:`{B_{k}}` are
coefficients dependent on the size interval. :math:`{W}` is the white
cap area:

.. math:: W=3.84\times 10^{-4}U^{3.41}_{10}

where :math:`{U_{10}}` is the wind speed at 10 m. For aerosols with a
geometric diameter :math:`>` 2.8 :math:`\mu`\ m, sea salt emissions
follow the parameterization by (**???**)

.. math:: \frac{dF_{0}}{dlogr}=1.373U^{3.41}_{10}r^{-3}(1+0.0057r^{1.05})\times 10^{1.19e^{-B^{2}}}

where :math:`{r}` is the radius of the aerosol at a relative humidity of
80% and :math:`{B}`\ =(0.380-log\ :math:`{r}`)/0.650. All sea salt
emissions fluxes are calculated for a size interval of
:math:`d\mathrm{log}{D}_{p}`\ =0.1 and then summed up for each modal
size bin. The cut-off size range for sea salt emissions in MAM-7 is
0.02-0.08 (Aitken), 0.08-0.3 (accumulation), 0.3-1.0 (fine sea salt),
and 1.0-10 :math:`\mu`\ m (coarse sea salt); for MAM-3 the range is
0.02-0.08 (Aitken), 0.08-1.0 (accumulation), and 1.0-10 :math:`\mu`\ m
(coarse).

Dry, unvegetated soils, in regions of strong winds generate soil
particles small enough to be entrained into the atmosphere, and these
are referred to here at desert dust particles. The generation of desert
dust particles is calculated based on the Dust Entrainment and
Deposition Model, and the implementation in the Community Climate System
Model has been described and compared to observations (**???**; **???**;
**???**). The only change to the CAM5 source scheme from the previous
studies is the increase in the threshold for leaf area index for the
generation of dust from 0.1 to 0.3 :math:`\mathrm{m^{2}/m^{2}}`, to be
more consistent with observations of dust generation in more productive
regions (**???**). The cut-off size range for dust emissions is 0.1-2.0
:math:`\mu`\ m (fine dust) and 2.0-10 :math:`\mu`\ m (coarse dust) for
MAM-7; and 0.1-1.0 :math:`\mu`\ m (accumulation), and 1.0-10
:math:`\mu`\ m (coarse) for MAM-3.

Chemistry
~~~~~~~~~

Simple gas-phase chemistry is included for sulfate aerosol. This
includes (1) DMS oxidation with OH and :math:`\mathrm{NO_{3}}` to form
:math:`\mathrm{SO_{2}}`; (2) :math:`\mathrm{SO_{2}}` oxidation with OH
to form :math:`\mathrm{H_{2}SO_{4}}` (gas); (3)
:math:`\mathrm{H_{2}O_{2}}` production
(:math:`\mathrm{HO_{2}}`\ +\ :math:`\mathrm{HO_{2}}`); and (4)
:math:`\mathrm{H_{2}O_{2}}` loss (:math:`\mathrm{H_{2}O_{2}}` photolysis
and :math:`\mathrm{H_{2}O_{2}}`\ +OH). The rate coefficients for these
reactions are provided from the MOZART model (**???**). Oxidant
concentrations (:math:`\mathrm{O_{3}}`, OH, :math:`\mathrm{HO_{2}}`, and
:math:`\mathrm{NO_{3}}`) are temporally interpolated from monthly
averages taken from MOZART simulations (**???**).

:math:`\mathrm{SO_{2}}` oxidation in bulk cloud water by
:math:`\mathrm{H_{2}O_{2}}` and :math:`\mathrm{O_{3}}` is based on the
MOZART treatment (**???**). The :math:`{p}`\ H value in the bulk cloud
water is calculated from the electroneutrality equation between the bulk
cloud-borne :math:`\mathrm{SO_{4}}` and :math:`\mathrm{NH_{4}}` ion
concentrations (summation over modes), and ion concentrations from the
dissolution and dissociation of trace gases based on the Henry’s law
equilibrium. Irreversible uptake of :math:`\mathrm{H_{2}SO_{4}}` (gas)
to cloud droplets is also calculated (**???**). The sulfate produced by
:math:`\mathrm{SO_{2}}` aqueous oxidation and
:math:`\mathrm{H_{2}SO_{4}}` (gas) uptake is partitioned to the
cloud-borne sulfate mixing ratio in each mode in proportion to the
cloud-borne aerosol number of the mode (i.e., the cloud droplet number
associated with each aerosol mode), by assuming droplets associated with
each mode have the same size. For MAM-7, changes to aqueous
:math:`\mathrm{NH_{4}}` ion from dissolution of :math:`\mathrm{NH_{3}}`
(g) are similarly partitioned among modes. :math:`\mathrm{SO_{2}}` and
:math:`\mathrm{H_{2}O_{2}}` mixing ratios are at the same time reduced
due to aqueous phase consumption.

Secondary Organic Aerosol
~~~~~~~~~~~~~~~~~~~~~~~~~

The simplest treatment of secondary organic aerosol (SOA), which is used
in many global models, is to assume fixed mass yields for anthropogenic
and biogenic precursor VOC’s, then directly emit this mass as primary
aerosol particles. MAM adds one additional step of complexity by
simulating a single lumped gas-phase SOA (gas) species. Fixed mass
yields for five VOC categories of the MOZART-4 gas-phase chemical
mechanism are assumed, as shown in Table
:ref:`table_soa_yields`. These yields have been increased
by an additional 50% for the purpose of reducing aerosol indirect
forcing by increasing natural aerosols. The total yielded mass is
emitted as the SOA (gas) species. MAM then calculates
condensation/evaporation of the SOA (gas) to/from several aerosol modes.
The condensation/evaporation is treated dynamically, as described later.
The equilibrium partial pressure of SOA (gas), over each aerosol mode m
is expressed in terms of Raoult’s Law as:

.. math:: P^{*}_{m}=(\frac{A^{SOA}_{m}}{A^{SOA}_{m}+0.1A^{POA}_{m}})P^{0}

where :math:`{{A}_{m}^{SOA}}` is SOA mass concentration in mode
:math:`{m}`, :math:`{{A}_{m}^{POA}}` is the primary organic aerosol
(POA) mass concentration in mode :math:`{m}` (10% of which is assumed to
be oxygenated), and :math:`{{P}^{0}}` is the mean saturation vapor
pressure of SOA whose temperature dependence is expressed as:

.. math:: P^{0}(T)=P^{0}(298K) \times exp[\frac{-\Delta H_{vap}}{R}(\frac{1}{T}-\frac{1}{298})]

where :math:`{{P}^{0}}` (298 K) is assumed at
:math:`\mathrm{1\times10^{-10}}` atm and the mean enthalpy of
vaporization :math:`\Delta{H}_{vap}` is assumed at 156 kJ
:math:`\mathrm{mol^{-1}}`.

Treatment of the gaseous SOA and explicit condensation/evaporation
provides (1) a realistic method for calculating the distribution of SOA
among different modes and (2) a minimal treatment of the temperature
dependence of the gas/aerosol partitioning.

Nucleation
~~~~~~~~~~

New particle formation is calculated using parameterizations of binary
:math:`\mathrm{H_{2}SO_{4}}`-:math:`\mathrm{H_{2}O}` homogeneous
nucleation, ternary
:math:`\mathrm{H_{2}SO_{4}}`-:math:`\mathrm{NH_{3}}`-:math:`\mathrm{H_{2}O}`
homogeneous nucleation, and boundary layer nucleation. A binary
parameterization (**???**) is used in MAM-3, which does not predict
:math:`\mathrm{NH_{3}}`, while a ternary parameterization (**???**) is
used in MAM-7. The boundary layer parameterization, which is used in
both versions, uses the empirical 1st order nucleation rate in
:math:`\mathrm{H_{2}SO_{4}}` from (**???**), with a first order rate
coefficient of :math:`\mathrm{1.0\times10^{-6} s^{-1}}` as in (**???**).
The new particles are added to the Aitken mode, and we use the
parameterization of (**???**) to account for loss of the new particles
by coagulation as they grow from critical cluster size to Aitken mode
size.

Condensation
~~~~~~~~~~~~

Condensation of :math:`\mathrm{H_{2}SO_{4}}` vapor,
:math:`\mathrm{NH_{3}}` (MAM-7 only), and the SOA (gas) to various modes
is treated dynamically, using standard mass transfer expressions
(**???**) that are integrated over the size distribution of each mode
(**???**). An accommodation coefficient of 0.65 is used for
:math:`\mathrm{H_{2}SO_{4}}` (**???**), and currently, for the other
species too. :math:`\mathrm{H_{2}SO_{4}}` and :math:`\mathrm{NH_{3}}`
condensation are treated as irreversible. :math:`\mathrm{NH_{3}}` uptake
stops when the :math:`\mathrm{NH_{4}}`/:math:`\mathrm{SO_{4}}` molar
ratio of a mode reaches 2. SOA (gas) condensation is reversible, with
the equilibrium vapor pressure over particles given by Eq. (4.296).

In MAM-7, condensation onto the primary carbon mode produces aging of
the particles in this mode. Various treatments of the aging process have
been used in other models (Cooke and Wilson 1996; **???**; **???**;
**???**). In CAM5 a criterion of 3 mono-layers of sulfate is used to
convert a fresh POM/BC particle to the aged accumulation mode. Using
this criterion, the mass of sulfate required to age all the particles in
the primary carbon mode, :math:`{M_{SO4,age-all}}`, is computed. If
:math:`{M_{SO4,cond}}` condenses on the mode during a time step, we
assume that a fraction :math:`{f_{age}}` = :math:`{M_{SO4,cond}}` /
:math:`{M_{SO4,age-all}}` has been aged. This fraction of the POM, BC,
and number in the mode is transferred to the accumulation mode, along
with the condensed soluble species. SOA is included in the aging
process. The SOA that condenses in a time step is scaled by its lower
hygroscopicity to give a condensed :math:`\mathrm{SO_{4}}` equivalent.

The two continuous growth processes (condensation and aqueous chemistry)
can result in Aitken mode particles growing to a size that is nominally
within the accumulation mode size range. Most modal aerosol treatments
thus transfer part of the Aitken mode number and mass (those particles
on the upper tail of the distribution) to the accumulation mode after
calculating continuous growth (**???**).

Coagulation
~~~~~~~~~~~

Coagulation of the Aitken, accumulation, and primary carbon modes is
treated. Coagulation within each of these modes reduces number but
leaves mass unchanged. For coagulation of Aitken with accumulation mode
and of primary-carbon with accumulation mode, mass is transferred from
Aitken or primary-carbon mode to the accumulation mode. For coagulation
of Aitken with primary-carbon mode in MAM-7, Aitken mass is first
transferred to the primary-carbon mode. This ages some of the
primary-carbon particles. An aging fraction is calculated as with
condensation, then the Aitken mass and the aged fraction of the
primary-carbon mass and number are transferred to the accumulation mode.
Coagulation rates are calculated using the fast/approximate algorithms
of the Community Multiscale Air Quality (CMAQ) model, version 4.6
(**???**).

Water Uptake
~~~~~~~~~~~~

Water uptake is based on the equilibrium Kohler theory (Ghan and Zaveri
2007) using the relative humidity and the volume mean hygroscopicity for
each mode to diagnose the wet volume mean radius of the mode from the
dry volume mean radius. The hygroscopity of each component is listed in
Table :ref:`table_hgroscopicity`. The hygroscopicities here are
equivalent to the :math:`\kappa` parameters of (**???**). Note that the
measured solubility of dust varies widely, from 0.03 to 0.26 (**???**).

[b]0.99

l c c r Emission Source &

l

| Geometric

| standard

| deviation, :math:`s_{g}`

&

l

| Number mode

| diameter,

| :math:`D_{gn}`\ (:math:`\mu`\ m)

&

l

| :math:`D_{emit}`

| (:math:`\mu`\ m)

| 
| BC/OM

| Forest fire/grass fire & 1.8 & 0.080 & 0.134

l

| Domestic/energy/industry/

| transportation/shipping/waste

| & See note & See note & 0.134
| :math:`\mathrm{SO_{4}}`

| Forest fire/grass fire/waste & 1.8 & 0.080 & 0.134

| Energy/industry/shipping & See note & See note & 0.261

| Domestic/transportation & 1.8 & 0.030 & 0.0504

| Continuous volcano, 50% in Aitken mode & 1.8 & 0.030 & 0.0504

| Continuous volcano, 50% in accum. mode & 1.8 & 0.080 & 0.134

.. _table_aerocom_emis:

+----------------+--------------+-------------+
| Species        | Mass yield   | Reference   |
+================+==============+=============+
| Big Alkanes    | 5%           | (**???**)   |
+----------------+--------------+-------------+
| Big Alkenes    | 5%           | assumed     |
+----------------+--------------+-------------+
| Toluene        | 15%          | (**???**)   |
+----------------+--------------+-------------+
| Isoprene       | 4%           | (**???**)   |
+----------------+--------------+-------------+
| Monoterpenes   | 25%          | (**???**)   |
+----------------+--------------+-------------+

Table: Assumed SOA (gas) yields

.. _table_soa_yields:

+----------------+-----------------+-----------------+-----------------+----------------+----------------+--------------------+-----------------+
| Seasalt        | sulfate         | nitrate         | ammonium        | SOA            | POM            | BC                 | dust            |
+================+=================+=================+=================+================+================+====================+=================+
| :math:`1.16`   | :math:`0.507`   | :math:`0.507`   | :math:`0.507`   | :math:`0.14`   | :math:`0.10`   | :math:`10^{-10}`   | :math:`0.068`   |
+----------------+-----------------+-----------------+-----------------+----------------+----------------+--------------------+-----------------+

Table: Hygroscopicity of aerosol components

.. _table_hgroscopicity:

Subgrid Vertical Transport and Activation/Resuspension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The vertical transport of interstitial aerosols and trace gases by deep
convective clouds, using updraft and downdraft mass fluxes from the
Zhang-McFarlane parameterization, is described in (**???**). Currently
this vertical transport is calculated separately from wet removal, but a
more integrated treatment is planned. Cloud-borne aerosols, which are
associated with large-scale stratiform cloud, are assumed to not
interact with the convective clouds. Vertical transport by shallow
convective clouds is treated similarly, using mass fluxes from the
shallow convection parameterization. Turbulent transport of the aerosol
is given a special treatment with respect to other tracers. To
strengthen the coupling between turbulent transport and aerosol
activation in stratiform clouds, the implicit time integration scheme
used for turbulent transport of heat, energy, and momentum is replaced
by an explicit scheme for droplets and aerosol. A sub-timestep is
calculated for each column based on the minimum turbulent transport time
in the column. Turbulent transport is integrated over the sub-time steps
using a forward time integration scheme.

Aerosol activation converts particles from the interstitial attachment
state to the cloud-borne state. In stratiform cloud, activation is
treated consistently with droplet nucleation, so that the total number
of particles activated and transferred to the cloud-borne state equals
to the number of droplets nucleated. Activation is parameterized in
terms of updraft velocity and the properties of all of the aerosol modes
(**???**), with both mass and number transferred to the cloud-borne
state. The updraft velocity is approximated by the square root of the
turbulence kinetic energy, with a minimum value of 0.2 m
:math:`\mathrm{s^{-1}}`. Activation is assumed to occur as updrafts
carry air into the base of the cloud (Ghan et al. 1997) and as cloud
fraction increases (**???**). In addition, activation is assumed to
occur as air is continuously cycled through clouds, assuming a cloud
regeneration time scale of one hour. Consider a model time step of 20
minutes, so that 1/3 of the cloud is regenerated in a time step. We
essentially dissipate then reform 1/3 of cloud each time step. During
dissipation, grid-cell mean cloud droplet number is reduced by 1/3, and
1/3 of the cloud-borne aerosols are resuspended and converted to the
interstitial state. During regeneration, interstitial aerosols are
activated in the “new” cloud, and cloud droplet number is increased
accordingly. The regeneration has small impact on shallow boundary layer
clouds, but it noticeably increases droplet number in deeper
free-tropospheric clouds where vertical turbulence mixing is slow.
Particles are resuspended as aerosol when droplets evaporate. This
process is assumed to occur as droplets are transferred below or above
cloud and as clouds dissipate.

Wet Deposition
~~~~~~~~~~~~~~

Aerosol wet removal is calculated using the CAM3.5 wet removal routine
(Rasch et al. 2000; Barth et al. 2000) with modifications for the
consistency with cloud macro- and microphysics. The routine treats
in-cloud scavenging (the removal of cloud-borne aerosol particles) and
below-cloud scavenging (the removal of interstitial aerosol particles by
precipitation particles through impaction and Brownian diffusion).

For in-cloud scavenging, the stratiform and convective cloud fraction,
cloud water, and precipitation production profiles are used to calculate
first-order loss rate profiles for cloud-water. These cloud-water
first-order loss rates are multiplied by “solubility factors” to obtain
aerosol first-order loss rates, which are applied to the aerosol
profiles. The solubility factors can be interpreted as (the fraction of
aerosols that are in cloud drops) :math:`\times` (an additional tuning
factor). In CAM3.5, where the cloud-borne aerosol is not explicitly
calculated, a value of 0.3 is used for solubility factors for all
aerosol types and sizes. Different values are used for the MAM. The
stratiform in-cloud scavenging only affects the stratiform-cloud-borne
aerosol particles, and these have solubility factors of 1.0. It does not
affect the interstitial aerosol particles, and these have solubility
factors of 0.0.

For convective in-cloud scavenging of MAM aerosols, both a solubility
factor and a within-convective-cloud activation fraction are passed to
the wet removal routine. For the stratiform-cloud-borne aerosol
particles, there is no wet removal by convective clouds, and these
factors are zero. For interstitial (with respect to stratiform cloud)
aerosol, the solubility factor is 0.5, and the activation fractions are
0.0 for the primary carbon mode, 0.4 for the fine and coarse dust modes,
and 0.8 for other modes. The lower values reflect lower hygroscopity.
These factors are applied to both number and mass species within each
mode, with one exception. In MAM-3, different activation fractions are
applied to the dust and sea salt of the coarse mode (0.4 and 0.8
respectively), and a weighted average is applied to the coarse mode
sulfate and number.

For below-cloud scavenging, the first-order removal rate is equal to 
[(solubility factor) :math:`\times` (scavenging coefficient)
:math:`\times` (precipitation rate) ]. Again, the solubility factor can
be viewed as a tuning factor. In CAM3.5, a solubility factor of 0.3 and
a scavenging coefficient of 0.1 :math:`\mathrm{mm^{-1}}` are used for
all aerosols. In MAM, the scavenging coefficient for interstitial
aerosol is explicitly calculated as in (**???**) and thus varies
strongly with particle size, with lowest values for the accumulation
mode; and the solubility factor is 0.1. For stratiform-cloud-borne
aerosol, there is no below-cloud scavenging, and the solubility factor
is 0.0.

Aerosol that is scavenged at one altitude can be resuspended at a lower
altitude if precipitation evaporates. In CAM5, as in CAM3.5, this
process is treated for aerosol removed by stratiform in-cloud
scavenging. A fraction of the in-cloud scavenged aerosol is resuspended,
and the resuspended fraction is equal to the fraction of precipitation
that evaporates below cloud.

Dry Deposition
~~~~~~~~~~~~~~

Aerosol dry deposition velocities are calculated using the (**???**)
parameterization with the CAM5 land-use and surface layer information.
Gravitational settling velocities are calculated at layers above the
surface (**???**). Both velocities depend on particle wet size and are
different for mass and number and between modes. The velocities for
cloud-borne aerosols are calculated based on droplet sizes. Aerosol
mixing ratio changes and fluxes from dry deposition and sedimentation
throughout a vertical column are then calculated using the CAM5 dust
deposition/sedimentation routine.

.. _aero_species_mam7:

.. figure:: figures/cam5_aero_fig1.jpg
   :align: center

   Predicted species for interstitial and cloud-borne component of each aerosol mode in MAM-7.
   Standard deviation for each mode is 1.6 (Aitken), 1.8 (accumulation), 1.6 (primary carbon), 1.8 (fine and coarse soil dust), 
   and 2.0 (fine and coarse sea salt)

.. _aero_species_mam3:

.. figure:: figures/cam5_aero_fig2.jpg
   :align: center
   
   Predicted species for interstitial and cloud-borne component of each aerosol mode in MAM-3.
   Standard deviation for each mode is 1.6 (Aitken), 1.8 (accumulation) and 1.8 (coarse mode)


Condensed Phase Optics
----------------------

Condensed phase (aerosols, liquid cloud droplets, hydrometeors, and ice
crystal) optics are provided as a mass-specific quantities in
m\ :math:`^2`/kg. These optics are specified for each band of the
shortwave and longwave radiation code. For the shortwave, unscaled
extinction, single-scattering albedo, and asymmetry parameter are
specified. For the longwave, the mass-specific absorption is specified.
Vertical optical depths are computed by multiplying by the mass-specific
quantities by the vertical mass path of the corresponding material.

For clouds, the in-cloud values of the mixing ratios are used to compute
the in-cloud values of cloud optical depths. The radiation does not use
grid-cell average optical depths of clouds.

Tropospheric Aerosol Optics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

While the radiation code supports a range of possible aerosol packages,
the modal aerosol package is the default configuration, and we will
discuss the optics treatment used in that package. Aerosol optical
properties for each mode are parameterized in terms of wet refractive
index and wet surface mode radius of the mode, as described by (Ghan and
Zaveri 2007), except that volume mixing rather than the Maxwell-Garnett
mixing rule is used to calculate the wet refractive index for mixtures
of insoluble and soluble particles (We found little difference between
the volume mixing treatment and the Maxwell-Garnett mixing rule.)
Refractive indices for water and for most aerosol components are taken
from OPAC (Koepke and Schult 1998), but for black carbon the value
(1.95,0.79i) from (Bond and Bergstrom 2006) is used for solar
wavelengths. Densities for each component are listed in
Table :ref:`table_aerdensity`.

.. _table_aerdensity: 

+-------------+-----------+-----------+------------+--------+--------+--------+--------+
| Sea salt    | Sulfate   | Nitrate   | Ammonium   | SOA    | POA    | BC     | Dust   |
+=============+===========+===========+============+========+========+========+========+
| 1900        | 1770      | 1770      | 1770       | 1000   | 1000   | 1700   | 2600   |
+-------------+-----------+-----------+------------+--------+--------+--------+--------+

Table Density (kg/m:math:`^3`) of aerosol material.

The wet volume mean radius for each mode is calculated from the dry
volume mean radius using equilibrium Kohler theory (Ghan and Zaveri
2007), the relative humidity and the volume mean hygroscopicity. The
hygroscopicity of each component is listed in Table [table:aerhygro].
Note that the measured solubility of dust varies widely, from 0.03 to
0.26 (Koehler et al. 2009). The wet surface mode radius is calculated
from the wet volume mean radius assuming a wet lognormal size
distribution with the same geometric standard deviation as the dry size
distribution. The geometric standard deviation is assumed to be constant
for each mode.

.. _table_aerohygro:

+-------------+-----------+-----------+------------+--------+----------+----------+---------+
| Sea salt    | Sulfate   | Nitrate   | Ammonium   | SOA    | POA      | BC       | Dust    |
+=============+===========+===========+============+========+==========+==========+=========+
| 1.16        | 0.507     | 0.507     | 0.507      | 0.14   | 1.e-10   | 1.e-10   | 0.068   |
+-------------+-----------+-----------+------------+--------+----------+----------+---------+

Table: Hygroscopicity of aerosol components.

Stratospheric Volcanic Aerosol Optics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

specifies the volcanic aerosol as a mass mixing ratio :math:`q_V` of wet
volcanic aerosol to dry air as a function of height, latitude, longitude
and time. also specifies a geometric mean radius :math:`r_g` of the
volcanic aerosol. The volcanic optics are stored as a lookup table as a
function of geometric mean radius.

The size distribution is defined by a log-normal size distribution with
a geometric mean radius :math:`r_g` and geometric standard deviation
:math:`\sigma_g`. For the standard version of the optics,

.. math::

   \begin{aligned}
   \sigma_g &=& 1.8 \\
   \mu&=&\ln(r_g )\\
   \mu &\in& [\mu_{\mathrm{min}}, \mu_{\mathrm{max}} ]\\
   \mu_{\mathrm{min}}&=&\ln (0.01*10^{-6} \exp(-5/2 * (\ln \sigma_g)^2)) \\
   \mu_{\mathrm{max}}&=&\ln (2.00*10^{-6} \exp(-5/2 * (\ln \sigma_g)^2)) \end{aligned}

In other words, :math:`r_{\mathrm{eff}}` spans the range [0.01,2.0]
:math:`\mu`\ m. The density of the sulfuric acid / water mixture at 75%
/ 25% at 215K is

.. math:: \rho = 1.75*10^3 \;\mathrm{kg/m}^3

The index of refraction is that specified by Biermann (Biermann, Luo,
and Peter 2000–1AD) and is available from the HITRAN (**???**) database.
The index at 75%/25% weight percent (sulfuric acid to water) and at 215K
is used.

The incomplete gamma weight,

.. math:: L(r)=\int_0^{r} r^{*2}n(r^*) dr^* / \int_0^\infty r^{*2}n(r^*) dr^*

can be used to define the mass-specific aerosol extinction, scattering,
and asymmetric scattering,

.. math::

   \begin{aligned}
   b_{\mathrm{ext}}=\frac{3}{4 \rho \; r_{\mathrm{eff}}} \int_{0}^{\infty}q_{\mathrm{ext}}(r) dL(r) \\
   b_{\mathrm{sca}}=\frac{3}{4 \rho \; r_{\mathrm{eff}}} \int_{0}^{\infty}q_{\mathrm{sca}}(r) dL(r) \\
   b_{\mathrm{asm}}=\frac{3}{4 \rho \; r_{\mathrm{eff}}} \int_{0}^{\infty}q_{\mathrm{gqsc}}(r) dL(r) \\
   b_{\mathrm{abs}}=\frac{3}{4 \rho \; r_{\mathrm{eff}}} \int_{0}^{\infty}  (q_{\mathrm{ext}}(r) - q_{\mathrm{sca}}(r)) dL(r)\end{aligned}

where
:math:`q_{\mathrm{ext}}(r), q_{\mathrm{sca}}(r), q_{\mathrm{gqsc}}(r)`
are efficiencies obtained from the MIEV0 program of Wiscombe (Wiscombe
1996).

These mass-specific properties are averaged over each frequency band of
RRTMG and parameterized in a lookup table with :math:`\mu = \ln(r_g)` as
the dependent variable.

The vertical optical depths are derived as the product of vertical mass
path with mass-specific aerosol properties at runtime.

.. math:: \tau_\mathrm{ext} = q_V*\frac{\Delta P_\mathrm{dry} }{ g} * b_{\mathrm{ext}}(\mu)

where :math:`q_V` is the mixing ratio of volcanic aerosol. The
corresponding scattering optical depth, asymmetric scattering optical
depth, and absorption optical depth are derived similarly.

Liquid Cloud Optics
~~~~~~~~~~~~~~~~~~~

For liquid clouds specifies the fraction of each grid cell occupied by
liquid cloud droplets :math:`C_\mathrm{liq}`, the ratio of mass of
condensed water to wet air in the cloud :math:`q_\mathrm{liq}`, and the
number-size distribution in terms of the 2 parameters, :math:`\mu` and
:math:`\lambda` of the gamma distribution,

.. math:: n(D) = \frac{dN}{dD} = \frac{\lambda^{\mu+1} }{\Gamma(\mu+1)} D^{\mu} e^{- \lambda D }

where :math:`D` is the diameter of the droplets.

Both the parameters, :math:`\mu` and :math:`\lambda` have limited
ranges:

.. math::
   :label: mulimit

   2.< \mu <15. 

.. math::
   :label: lambdalimit

   \frac{\mu+1}{50*10^{-6} \mathrm{m}} < \lambda&<\frac{\mu+1}{2*10^{-6} \mathrm{m}}

The liquid cloud optics are specified in terms of a lookup table in
:math:`\mu` and :math:`1/\lambda`. These optics are computed as
size-distribution and spectral-band averages of the quantities (e.g.,
:math:`Q_\mathrm{ext}`) computed by the MIEV0 program (Wiscombe 1996).

The size-integrated mass-specific extinction coefficient,
:math:`k_\mathrm{ext}`, (units m\ :math:`^{2}`/kg) is given by:

.. math::
   :label: extinctionsizeintegral

   k_\mathrm{ext}(\nu) = \frac{\frac{\pi}{4} \int_{0}^{\infty}\; D^2\; Q_\mathrm{ext}(D;\nu,m)\; n(D)\; dD}
                  {\frac{\pi}{6} \rho_w \int_{0}^{\infty}\; D^3\; n(D)\; dD} 

The corresponding quantities are used to compute mass-specific
absorption in the longwave as well as single-scattering albedo and
asymmetry parameter.

The in-cloud optical depth is then given by:

.. math:: \tau_\mathrm{liq}(\nu) = k_\mathrm{ext}(\nu) \; q_\mathrm{liq} \; \frac{\Delta P}{g}

where :math:`q_\mathrm{liq}` is the ratio of droplet mass to dry air
mass.

For RRTMG, the wavenumber average values of
:math:`\tau_\mathrm{liq}, \tau_\mathrm{liq}\omega_\mathrm{liq}, \tau_\mathrm{liq}\omega_\mathrm{liq} g_\mathrm{liq}`
on each SW band, and the wavenumber average value of the absorption
optical depth, :math:`\tau_\mathrm{liq}(1-\omega_\mathrm{liq})`, on each
longwave band.

In-cloud water path variability is not treated by the optics.

Ice Cloud Optics
~~~~~~~~~~~~~~~~

specifies an in-cloud ice water path, an ice cloud fraction, and an
effective diameter for ice particles in the cloud. The optics for ice
clouds are constructed as a lookup table as a function of effective
diameter for each of the shortwave and longwave bands in the radiation
code.

Ice cloud optical properties have been derived using two approaches: (1)
calculations of single ice crystal scattering properties based on
electrodynamic theory, followed by their application to assumed ice
particle size distributions (PSD) and the representation of PSD optical
properties through the effective diameter (:math:`D_e`) of the PSD, and
(2) parameterization of scattering/absorption processes in terms of ice
particle shape and size, and integrating these expressions over the PSD
to produce analytical expressions of PSD optical properties in terms of
ice crystal and PSD parameters. In the latter case, the PSD extinction
and absorption coefficients can be expressed as explicit functions of
the ice particle projected area- and mass-dimension power laws and the
PSD parameters of the gamma form. The modified anomalous diffraction
approximation (MADA) uses this second approach to calculate ice cloud
optical properties. The development of MADA was motivated by a desire to
explicitly represent ice optical properties in terms of the ice PSD and
ice crystal shape parameters, given that the ice PSD optical properties
cannot be uniquely defined by :math:`D_e`\ (Mitchell 2002).

MADA was developed from van de Hulst’s anomalous diffraction theory or
ADT (Hulst 1957) through a series of physical insights, which are:

#. The effective photon path through a particle by which its scattering
   properties can be predicted is given by the ratio of particle
   projected area/particle volume (Bryant and Latimer 1969; Mitchell and
   Arnott 1994), where volume is defined as particle mass/bulk density
   of ice (0.917 g/cm\ :math:`^3`).

#. The processes of internal reflection and refraction can be viewed as
   extending the photon path and can be parameterized using a MADA
   framework (Mitchell, Macke, and Liu 1996b).

#. The maximum contribution of wave resonance or photon tunneling to
   absorption and extinction can be estimated as a linear function of
   the real part of the refractive index for ice, :math:`n_r`. Photon
   tunneling can then be parameterized in terms of :math:`n_r`, size
   parameter :math:`x` and the other MADA parameters described above
   (Mitchell 2000).

#. Edge effects as surface wave phenomena pertain only to extinction and
   can be represented in terms of the size parameter :math:`x` as
   described by (Wu 1956) and modified by (Mitchell 2000). Based on a
   laboratory ice cloud study (Mitchell et al. 2001), edge effects for
   non-spherical ice crystals do not appear significant.

The first insight greatly simplified van de Hulst’s ADT, resulting in
analytic and integrable expressions for the PSD extinction and
absorption coefficients as shown in (Mitchell and Arnott 1994). This
simplified ADT may be more accurate than the original ADT (Mitchell et
al. 2006). This simplified ADT provided an analytical framework on which
the other three insights or processes were expressed. These processes
were represented analytically for a single ice particle, and then
integrated over the PSD to produce extinction and absorption
coefficients that account for these processes. These coefficients were
formulated in terms of ice particle shape (i.e. the ice particle area-
and mass-dimension power laws) and the three gamma PSD parameters. The
basic MADA equations formulated for ice clouds are given in the appendix
of (Mitchell 2002). Details regarding their derivation and their
physical basis are described in (Mitchell 2000) and (Mitchell, Macke,
and Liu 1996b).

The asymmetry parameter :math:`g` is not treated by MADA, but was
parameterized for solar wavelengths as a function of wavelength and ice
particle shape and size, based on ray-tracing calculations by Andreas
Macke, as described in (Mitchell, Macke, and Liu 1996b). The :math:`g`
parameterization for quasi-spherical ice particles is based on the phase
function calculations of (Nousiainen and McFarquhar 2004). These
parameterizations relate :math:`g` for a PSD to the ice particle size
that divides the PSD into equal projected areas (since scattering
depends on projected area). For terrestrial radiation, :math:`g` values
for ice are based on the :math:`g` parameterization described in (Yang
et al. 2005).

Tests of MADA
^^^^^^^^^^^^^

While this treatment of ice optical properties began and evolved through
van de Hulst’s original insights formulated in ADT, optical properties
predicted by MADA closely agree with those predicted by other ice optics
schemes based on electrodynamic theory. As described in (Mitchell et al.
2001; Mitchell et al. 2006), MADA has been tested in a laboratory ice
cloud experiment where the MADA extinction error was 3% on average
relative to the FTIR measured extinction efficiency over the 2-14
:math:`\mu`\ m wavelength range. These same laboratory PSD were used to
calculate the absorption efficiencies using MADA and T-matrix, which
differed by 6% on average over the wavelength range 2-18 :math:`\mu`\ m
(size parameter range 2-22). In corresponding T-matrix calculations of
the single-scattering albedo, the mean MADA error was 2.5%. In another
test, MADA absorption errors relative to the Finite Difference Time
Domain (FDTD) method (i.e. (Yang et al. 2005) over the wavelength range
3-100 :math:`\mu`\ m were no greater than 15% for six ice particle
shapes. Finally, the absorption coefficients predicted by MADA and the
(Fu, Yang, and Sun 1998) and the (Yang et al. 2005) ice optics schemes
generally agreed within 5%.

Application to 
^^^^^^^^^^^^^^^

The MADA-based ice optics scheme described above is not used explicitly
in , but was used to generate a look-up table of optical properties as a
function of effective diameter, :math:`D_e`. The PSD optical properties
consist of the mass-normalized extinction coefficient (volume extinction
coefficient / ice water content), the single-scattering albedo and the
asymmetry parameter for bands covering all solar and terrestrial
wavelengths. The radiation bands coincide with those used in RRTMG. The
ice refractive index values used are from (Warren and Brandt 2008).
Since MADA is formulated to accept any ice particle shape ÒrecipeÓ, a
shape recipe corresponding to that observed for mid-latitude cirrus
clouds at :math:`-45\,^{\circ}\mathrm{C}` (see (Lawson et al. 2006)) was
assumed for ice particles larger than 60 :math:`\mu`\ m: 7% hexagonal
columns, 50% bullet rosettes and 43% irregular ice particles. At smaller
sizes, the shape recipe consists of 50% quasi-spherical, 30% irregular
and 20% bullet rosette ice crystals, based on in-situ measurements in
tropical cirrus [P. Lawson, 2005, personal communication].

The effective diameter is defined in a way that is universal for both
ice and water clouds, which is essentially the photon path
characterizing the PSD (Mitchell 2002):

.. math:: De = \frac{3}{2} \frac{\mathrm{IWC}}{\rho_i A}

where :math:`\mathrm{IWC}` is the ice water content (g/cm:math:`^3`),
:math:`\rho_i` is the bulk ice density (0.917 g/cm\ :math:`^3`) and
:math:`A` is the total projected area of the PSD
(cm:math:`^2`/cm:math:`^3`).

Snow Cloud Optics
~~~~~~~~~~~~~~~~~

specifies snow as a cloud fraction of snow, an effective diameter of
snow, and an in-cloud mass mixing ratio of snow. The snow optics are
identical to the optics for ice clouds.

Radiative Transfer
------------------

Radiative transfer calculations in the longwave and shortwave are
provided by the radiation code RRTMG (Iacono et al. 2008; Mlawer et al.
1997). This is an accelerated and modified version of the correlated
:math:`k`-distribution model, RRTM. The condensed phase radiative
parameterizations are external to the radiation package, however the gas
optics and radiative transfer solver are provided within RRTMG.

Combination of Aerosol Radiative Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The number :math:`N_a` of aerosol species is arbitrary; however in the
standard configuration there are 3 modes. The radiative properties are
combined before being passed to the radiative transfer solver. If the
extinction optical depth of species :math:`i` in band :math:`b` is
:math:`\tau_{ib}` and the single-scattering albedo is
:math:`\omega_{ib}` and the asymmetry parameter is :math:`g_{ib}` then
the aerosol optics are combined as follows:

.. math::

   \begin{aligned}
   \tau_b &=& \sum_{i=1}^{N_a} \tau_{ib} \\
   \omega_b&=&\sum_{i=1}^{N_a}  \tau_{ib} \omega_{ib} / \tau_b\\
   g_b&=&\sum_{i=1}^{N_a}  \tau_{ib} \omega_{ib} g_{ib} / (\tau_b \omega_b)\end{aligned}

where :math:`\tau_b` is the total aerosol extinction optical depth in
band :math:`b`, :math:`\omega_b` is the total single-scattering albedo
in band :math:`b`, and :math:`g_b` is the asymmetry parameter in band
:math:`b`.

Combination of Cloud Optics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

are specifies three different types of clouds: ice clouds, liquid
clouds, and snow clouds. Each of these clouds has a separate cloud
fraction :math:`C_\mathrm{liq},C_\mathrm{ice},C_\mathrm{snow}`, as well
as an in-cloud radiative characterization in terms of optical depths
:math:`\tau_i`, single-scattering albedo :math:`\omega_i` and asymmetry
parameter :math:`g_i`. The optics are smeared together into a total
cloud fraction :math:`C` as follows:

.. math::

   \begin{aligned}
   C &=& \max\{C_\mathrm{liq},C_\mathrm{ice},C_\mathrm{snow} \} \\
   \tau_c &=& \sum_\mathrm{t \in type} \tau_t * C_t / C \\
   \omega_c&=&\sum_\mathrm{t\in type}  \tau_{tb} \omega_{tb} C_t / (\tau_c C)\\
   g_c&=&\sum_\mathrm{t \in type}  \tau_{tb} \omega_{tb} g_{tb} C_t / (\tau_c \omega_c C)\end{aligned}

where :math:`C,\tau_c, \omega_c, g_c` are the combined cloud radiative
parameters.

Radiative Fluxes and Heating Rates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Radiative fluxes and heating rates in are calculated using RRTMG(Iacono
et al. 2008).

This model utilizes the correlated :math:`k`-distribution technique to
calculate irradiance and heating rate efficiently in broad spectral
intervals, while realizing the objective of retaining a high level of
accuracy relative to measurements and high-resolution line-by-line
models. Sub-grid cloud characterization in RRTMG is treated in both the
longwave and shortwave spectral regions with McICA, the Monte-Carlo
Independent Column Approximation (Pincus and Morcrette 2003), using the
maximum-random cloud overlap assumption.

The thermodynamic state, gas concentrations, cloud fraction, condensed
phase optics, and aerosol properties are specified elsewhere. The
surface model provides both the surface albedo, area-averaged for each
atmospheric column, and the upward longwave surface flux, which
incorporates the surface emissivity, for input to the radiation. The
bulk aerosol package of CAM4 continues to be supported by this radiation
code as an option, however a description of this optional configuration
is not provided in this document.

To provide fluxes at the top of the atmosphere, RRTMG uses with an
additional layer above the model top in both the longwave and shortwave.
This extra layer is specified by replicating the composition of the
highest layer into a layer that extends from the top of the model to
:math:`10^{-4}` hPa. RRTMG does not treat non-LTE (local thermodynamic
equilibrium) effects in the upper atmosphere. It provides accurate
fluxes and heating rates up to about :math:`0.1` hPa, above which
non-LTE effects become more significant.

Shortwave Radiative Transfer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RRTMG divides the solar spectrum into 14 shortwave bands that extend
over the spectral range from 0.2 :math:`\mu`\ m to 12.2 :math:`\mu`\ m
(820 to 50000 cm\ :math:`^{-1}`). Modeled sources of extinction
(absorption and scattering) are H2O, O3, CO2, O2, CH4, N2, clouds,
aerosols, and Rayleigh scattering. The model uses a two-stream
:math:`\delta`-Eddington approximation assuming homogeneously mixed
layers, while accounting for both absorption and scattering in the
calculation of reflectance and transmittance. The model distinguishes
the direct solar beam from scattered (diffuse) radiation. The scattering
phase function is parameterized using the Henyey-Greenstein
approximation to represent the forward scattering fraction as a function
of the asymmetry parameter. This Òdelta-scalingÓ is applied to the total
irradiance as well as to the direct and diffuse components. The latter
are consistent with the direct and diffuse components of the surface
albedo, which are applied to the calculation of surface reflectance.

The shortwave version of RRTMG used in CAM5 is derived from RRTM\_SW
(Clough et al. 2005). It utilizes a reduced complement of 112 quadrature
points (g-points) to calculate radiative transfer across the 14 spectral
bands, which is half of the 224 g-points used in RRTM\_SW, to enhance
computational performance with little impact on accuracy. The number of
g-points needed within each band varies depending on the strength and
complexity of the absorption in each spectral interval. Total fluxes are
accurate to within 1-2 W/m\ :math:`^2` relative to the standard RRTM\_SW
(using DISORT with 16 streams) in clear sky and in the presence of
aerosols and within 6 W/m\ :math:`^2` in overcast sky. RRTM\_SW with
DISORT is itself accurate to within 2 W/m\ :math:`^2` of the
data-validated multiple scattering model, CHARTS (Moncet and Clough
1997). Input absorption coefficient data for the :math:`k`-distributions
used by RRTMG are obtained directly from the line-by-line radiation
model LBLRTM (Clough et al. 2005).

RRTMG shortwave utilizes McICA, the Monte-Carlo Independent Column
Approximation, to represent sub-grid scale cloud variability such as
cloud fraction and cloud overlap. An external sub-column generator is
used to define the stochastic cloud arrays used by the McICA technique.

The Kurucz solar source function is used in the shortwave model, which
assumes a total solar irradiance (TSI) at the top of the atmosphere of
1368.22 W/m\ :math:`^2`. However, this value is scaled in each spectral
band through the specification of a time-varying solar spectral
irradiance as discussed below. The TSI assumed in each RRTMG shortwave
band is listed in the table below, along with the spectral band
boundaries in :math:`\mu`\ m and wavenumbers.

Shortwave radiation is only calculated by RRTMG when the cosine of the
zenith angle is larger than zero, that is, when the sun is above the
horizon.

.. _table_SWBands:

+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| Band    | Band               | Band               | Band                | Band                | Solar             |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| Index   | Min                | Max                | Min                 | Max                 | Irradiance        |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
|         | (:math:`\mu`\ m)   | (:math:`\mu`\ m)   | (cm:math:`^{-1}`)   | (cm:math:`^{-1}`)   | (W/m:math:`^2`)   |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 1       | 3.077              | 3.846              | 2600                | 3250                | 12.11             |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 2       | 2.500              | 3.077              | 3250                | 4000                | 20.36             |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 3       | 2.150              | 2.500              | 4000                | 4650                | 23.73             |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 4       | 1.942              | 2.150              | 4650                | 5150                | 22.43             |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 5       | 1.626              | 1.942              | 5150                | 6150                | 55.63             |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 6       | 1.299              | 1.626              | 6150                | 7700                | 102.93            |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 7       | 1.242              | 1.299              | 7700                | 8050                | 24.29             |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 8       | 0.778              | 1.242              | 8050                | 12850               | 345.74            |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 9       | 0.625              | 0.778              | 12850               | 16000               | 218.19            |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 10      | 0.442              | 0.625              | 16000               | 22650               | 347.20            |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 11      | 0.345              | 0.442              | 22650               | 29000               | 129.49            |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 12      | 0.263              | 0.345              | 29000               | 38000               | 50.15             |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 13      | 0.200              | 0.263              | 38000               | 50000               | 3.08              |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+
| 14      | 3.846              | 12.195             | 820                 | 2600                | 12.89             |
+---------+--------------------+--------------------+---------------------+---------------------+-------------------+

Table: RRTMG_SW spectral band boundaries and the solar irradiance in each band.

Longwave Radiative Transfer
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The infrared spectrum in RRTMG is divided into 16 longwave bands that
extend over the spectral range from 3.1 :math:`\mu`\ m to 1000.0
:math:`\mu`\ m (10 to 3250 cm\ :math:`^{-1})`. The band boundaries are
listed in the table below. The model calculates molecular, cloud and
aerosol absorption and emission. Scattering effects are not presently
included. Molecular sources of absorption are H2O, CO2, O3, N2O, CH4,
O2, N2 and the halocarbons CFC-11 and CFC-12. CFC-11 is specified by
CAM5 as a weighed sum of multiple CFCs (other than CFC-12). The water
vapor continuum is treated with the CKD\_v2.4 continuum model. For
completeness, band 16 includes a small adjustment to add the infrared
contribution from the spectral interval below 3.1 :math:`\mu`\ m.

The longwave version of RRTMG (Iacono et al. 2008; Iacono et al. 2003;
Iacono et al. 2000) used in CAM5 has been modified from RRTM\_LW (Mlawer
et al. 1997) to enhance its computational efficiency with minimal effect
on the accuracy. This includes a reduction in the total number of
g-points from 256 to 140. The number of g-points used within each band
varies depending on the strength and complexity of the absorption in
each band. Fluxes are accurate to within 1.0 W/m\ :math:`^2` at all
levels, and cooling rate generally agrees within 0.1 K/day in the
troposphere and 0.3 K/day the stratosphere relative to the line-by-line
radiative transfer model, LBLRTM (Clough et al. 2005; Clough and Iacono
1995). Input absorption coefficient data for the :math:`k`-distributions
used by RRTMG are obtained directly from LBLRTM.

This model also utilizes McICA, the Monte-Carlo Independent Column
Approximation (Pincus and Morcrette 2003), to represent sub-grid scale
cloud variability such as cloud fraction and cloud overlap. An external
sub-column generator is used to define the stochastic cloud arrays
needed by the McICA technique.

Within the longwave radiation model, the surface emissivity is assumed
to be 1.0. However, the radiative surface temperature used in the
longwave calculation is derived with the Stefan-Boltzmann relation from
the upward longwave surface flux that is input from the land model.
Therefore, this value may include some representation of surface
emissivity less than 1.0 if this condition exists in the land model.
RRTMG longwave also provides the capability of varying the surface
emissivity within each spectral band, though this feature is not
presently utilized.

Longwave radiative transfer is performed over a single (diffusivity)
angle (secant =1.66) for one upward and one downward calculation. RRTMG
includes an accuracy adjustment in profiles with very high water vapor
that slightly varies the diffusivity angle in some bands as a function
of total column water vapor.

+---------+--------------------+--------------------+---------------------+---------------------+
| Band    | Band               | Band               | Band                | Band                |
+---------+--------------------+--------------------+---------------------+---------------------+
| Index   | Min                | Max                | Min                 | Max                 |
+---------+--------------------+--------------------+---------------------+---------------------+
|         | (:math:`\mu`\ m)   | (:math:`\mu`\ m)   | (cm:math:`^{-1}`)   | (cm:math:`^{-1}`)   |
+---------+--------------------+--------------------+---------------------+---------------------+
| 1       | 28.57              | 1000.0             | 10                  | 350                 |
+---------+--------------------+--------------------+---------------------+---------------------+
| 2       | 20.00              | 28.57              | 350                 | 500                 |
+---------+--------------------+--------------------+---------------------+---------------------+
| 3       | 15.87              | 20.00              | 500                 | 630                 |
+---------+--------------------+--------------------+---------------------+---------------------+
| 4       | 14.29              | 15.87              | 630                 | 700                 |
+---------+--------------------+--------------------+---------------------+---------------------+
| 5       | 12.20              | 14.29              | 700                 | 820                 |
+---------+--------------------+--------------------+---------------------+---------------------+
| 6       | 10.20              | 12.20              | 820                 | 980                 |
+---------+--------------------+--------------------+---------------------+---------------------+
| 7       | 9.26               | 10.20              | 980                 | 1080                |
+---------+--------------------+--------------------+---------------------+---------------------+
| 8       | 8.47               | 9.26               | 1080                | 1180                |
+---------+--------------------+--------------------+---------------------+---------------------+
| 9       | 7.19               | 8.47               | 1180                | 1390                |
+---------+--------------------+--------------------+---------------------+---------------------+
| 10      | 6.76               | 7.19               | 1390                | 1480                |
+---------+--------------------+--------------------+---------------------+---------------------+
| 11      | 5.56               | 6.76               | 1480                | 1800                |
+---------+--------------------+--------------------+---------------------+---------------------+
| 12      | 4.81               | 5.56               | 1800                | 2080                |
+---------+--------------------+--------------------+---------------------+---------------------+
| 13      | 4.44               | 4.81               | 2080                | 2250                |
+---------+--------------------+--------------------+---------------------+---------------------+
| 14      | 4.20               | 4.44               | 2250                | 2380                |
+---------+--------------------+--------------------+---------------------+---------------------+
| 15      | 3.85               | 4.20               | 2380                | 2600                |
+---------+--------------------+--------------------+---------------------+---------------------+
| 16      | 3.08               | 3.85               | 2600                | 3250                |
+---------+--------------------+--------------------+---------------------+---------------------+

Table: [table:LWBands]RRTMG\_LW spectral band boundaries.

Surface Radiative Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the shortwave, the surface albedoes are specified at every grid
point at every time step. The albedoes are partitioned for the spectral
ranges [2.0, 0.7]\ :math:`\mu`\ m and [0.7,12.0]:math:`\mu`\ m. In
addition they are partitioned between the direct and diffuse beam.

In the longwave, the surface is assumed to have an emissivity of 1.0
within the radiation model. However, the radiative surface temperature
used in the longwave calculation is derived with the Stefan-Boltzmann
relation from the upward longwave surface flux that is input from the
surface models. Therefore, this value may include some representation of
surface emissivity less than 1.0, if this condition exists in surface
models (e.g. the land model).

Time Sampling
~~~~~~~~~~~~~

Both the shortwave and longwave radiation is computed at hourly
intervals by default. The heating rates and fluxes are assumed to be
constant between time steps.

Diurnal Cycle and Earth Orbit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In |cam|, the diurnal cycle and earth orbit is computed using the method of
(Berger 1978). Using this formulation, the insolation can be determined
for any time within :math:`10^6` years of 1950 AD. The insolation at the
top of the model atmosphere is given by

.. math:: 
   :label: 4.b.1

   S_I = {S_0\,{\rho^{-2}}\,\cos\mu} , 

where :math:`S_0` is the solar constant, :math:`\mu` is the solar zenith
angle, and :math:`\rho^{-2}` is the distance factor (square of the ratio
of mean to actual distance that depends on the time of year). A time
series of the solar spectral irradiance at 1 a.u. for 1870-2100 based
upon (Wang, Lean, and Sheeley 2005) is included with the standard model
and is in section :ref:`sec-lean`.

We represent the annual and diurnal cycle of solar insolation with a
repeatable solar year of exactly 365 days and with a mean solar day of
exactly 24 hours, respectively. The repeatable solar year does not allow
for leap years. The expressions defining the annual and diurnal
variation of solar insolation are:

.. math::

   \begin{aligned}
   \cos\mu & =& \sin\phi \sin\delta - \cos\phi \cos\delta \cos(H) \\
   \delta & =& \arcsin(\sin\epsilon\sin\lambda) \\ 
   \rho & =& \frac{1-e^2}{1+e\,\cos(\lambda - {\tilde\omega})} \\ 
   {\tilde\omega}& =& \Pi + \psi\end{aligned}

where

.. math::

   \begin{aligned}
   \phi & = &{\rm latitude~in~radians} \nonumber \nonumber \\ 
   \delta & =& {\rm solar~declination~in~radians} \nonumber \\
    H & =& {\rm hour~angle~of~sun~during~the~day} \nonumber \\ 
    \epsilon & =& {\rm obliquity} \nonumber \\
   \lambda & =& {\rm true~longitude~of~the~earth~relative~to~vernal~equinox} \\
   e & =& {\rm eccentricity~factor} \nonumber \\ 
   {\tilde\omega}& = &{\rm longitude~of~the~perihelion}+ 180^\circ \nonumber \\ 
   \Pi & =& {\rm longitude~of~perihelion~based~on~the~fixed~equinox} \nonumber \\ 
   \psi & = &{\rm general~precession} \nonumber\end{aligned}

The hour angle :math:`H` in the expression for :math:`\cos\mu` depends
on the calendar day :math:`d` as well as model longitude:

.. math:: H = 2\,\pi\left(d + \frac{\theta}{360^\circ}\right) , 
	  :label: 4.b.2

where :math:`\theta` = model longitude in degrees starting from
Greenwich running eastward. Note that the calendar day :math:`d` varies
continuously throughout the repeatable year and is updated every model
time step. The values of :math:`d` at 0 GMT for January 1 and
December 31 are 0 and 364, respectively. This would mean, for example,
that a model calendar day :math:`d` having no fraction (such as 182.00)
would refer to local midnight at Greenwich, and to local noon at the
date line (:math:`180^\circ` longitude).

The obliquity :math:`\epsilon` may be approximated by an empirical
series expansion of solutions for the Earth’s orbit

.. math::

   \epsilon = \epsilon^* + \sum_{j=1}^{47} A_j\,\cos\left(f_j\,t +
                  \delta_j\right) \\

where :math:`A_j`, :math:`f_j`, and :math:`\delta_j` are determined by
numerical fitting. The term :math:`\epsilon^* = 23.320556^\circ`, and
:math:`t` is the time (in years) relative to 1950 AD.

Since the series expansion for the eccentricity :math:`e` is slowly
convergent, it is computed using

.. math:: e = \sqrt{\left(e\cos\Pi\right)^2+\left(e\sin\Pi\right)^2}

The terms on the right-hand side may also be written as empirical series
expansions:

.. math::

   e{\left\lbrace\begin{array}{c}\cos\\
   \sin\end{array}\right\rbrace}\Pi = \sum_{j=1}^{19} M_j\,{\left\lbrace\begin{array}{c}\cos\\
   \sin\end{array}\right\rbrace}\left(g_j\,t+\beta_j\right)

where :math:`M_j`, :math:`g_j`, and :math:`\beta_j` are estimated from
numerical fitting. Once these series have been computed, the longitude
of perihelion :math:`\Pi` is calculated using

.. math:: \Pi = \arctan\left(\frac{e\,\sin\Pi}{e\,\cos\Pi}\right)

The general precession is given by another empirical series expansion

.. math::

   \psi = \tilde\psi\,t + \zeta + \sum_{j=1}^{78} F_j\,\sin\left(f'_j\,t
          + \delta'_j\right)

where :math:`\tilde\psi = 50.439273''`, :math:`\zeta = 3.392506^\circ`,
and :math:`F_j`, :math:`f'_j`, and :math:`\delta'_j` are estimated from
the numerical solution for the Earth’s orbit.

The calculation of :math:`\lambda` requires first determining two mean
longitudes for the orbit. The mean longitude :math:`\lambda_{m0}` at the
time of the vernal equinox is :

.. math::

   \begin{aligned}
   \lambda_{m0} & = &
      2\left\lbrace \left(\frac{e}{2} + \frac{e^3}{8}\right)
                          (1+\beta)\sin({\tilde\omega}) \right.\nonumber \\
      & & \phantom{-2\left\lbrace\right.}
        -\frac{e^2}{4}\,\left(\frac{1}{2}+\beta\right)\,\sin(2\,{\tilde\omega})
      \\
      & & \phantom{-2\left\lbrace\right.}
         +\left.\frac{e^3}{8}\,\left(\frac{1}{3}+\beta\right)\,
          \sin(3\,{\tilde\omega}) \right\rbrace \nonumber\end{aligned}

where :math:`\beta = \sqrt{1-e^2}`. The mean longitude is

.. math:: \lambda_m = \lambda_{m0} + \frac{2\,\pi\,(d-d_{ve})}{365}

where :math:`d_{ve}=80.5` is the calendar day for the vernal equinox at
noon on March 21. The true longitude :math:`\lambda` is then given by:

.. math::

   \begin{aligned}
   \lambda = \lambda_m & + & \left(2\,e -
      \frac{e^3}{4}\right)\sin(\lambda_m-{\tilde\omega}) \nonumber \\ & + &
      \frac{5\,e^2}{4}\,\sin\left[2(\lambda_m-{\tilde\omega})\right] \\ & + &
      \frac{13\,e^3}{12}\sin\left[3(\lambda_m-{\tilde\omega})\right] \nonumber\end{aligned}

The orbital state used to calculate the insolation is held fixed over
the length of the model integration. This state may be specified in one
of two ways. The first method is to specify a year for computing
:math:`t`. The value of the year is held constant for the entire length
of the integration. The year must fall within the range of
:math:`1950 \pm
10^6`. The second method is to specify the eccentricity factor
:math:`e`, longitude of perihelion :math:`{\tilde\omega}- 180^\circ`,
and obliquity :math:`\epsilon`. This set of values is sufficient to
specify the complete orbital state. Settings for AMIP II style
integrations under 1995 AD conditions are :math:`\epsilon = 23.4441`,
:math:`e = 0.016715`, and :math:`{\tilde\omega}-
180 = 102.7`.

Solar Spectral Irradiance
~~~~~~~~~~~~~~~~~~~~~~~~~

The reference spectrum assumed by RRTMG is the Kurucz spectrum.
specifies the solar spectral irradiance in a file, based on the work of
Lean (Wang, Lean, and Sheeley 2005). The Kurucz spectrum can be seen in
figure [fig:kurucz]. The Lean data seen in figure [fig:lean] is
time-varying and the graphed values are an average over one solar cycle.
These two spectra postulate different values of the total solar
irradiance. A graph of the relative difference between them can be seen
in figure `fig_rel_sol`_.

.. _fig_rel_sol:

+------------------------+-----------+-----------+
| Solar Irradiance       | Kurucz    | Lean      |
+========================+===========+===========+
| Total                  | 1368.60   | 1366.96   |
+------------------------+-----------+-----------+
| In RRTMG bands         | 1368.14   | 1366.39   |
+------------------------+-----------+-----------+
| :math:`>12195` nm      | 0.46      | 0.46      |
+------------------------+-----------+-----------+
| :math:`[120,200]` nm   | 0         | 0.11      |
+------------------------+-----------+-----------+
| EUV                    | 0         | 0.0047    |
+------------------------+-----------+-----------+

[tbl:TSI]

+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| RRTMG        | :math:`\lambda_{high}`,   | :math:`\lambda_{low}`,   | Kurucz            | Lean              | Lean       | Relative   | Lean\ :math:`(t)` Max %   | Lean\ :math:`(t)` Max   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| Band Index   | nm                        | nm                       | W/m\ :math:`^2`   | W/m\ :math:`^2`   | - Kurucz   | %          | Variation                 | :math:`\Delta`\ Flux    |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 14           | 12195                     | 3846                     | 12.79             | 12.78             | -0.01      | -0.08      | 0.16                      | 0.020                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 1            | 3846                      | 3077                     | 12.11             | 11.99             | -0.12      | -1.00      | 0.02                      | 0.003                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 2            | 3077                      | 2500                     | 20.36             | 20.22             | -0.14      | -0.69      | 0.03                      | 0.007                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 3            | 2500                      | 2151                     | 23.73             | 23.49             | -0.24      | -1.02      | 0.02                      | 0.005                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 4            | 2151                      | 1942                     | 22.43             | 22.17             | -0.26      | -1.17      | 0.01                      | 0.003                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 5            | 1942                      | 1626                     | 55.63             | 55.61             | -0.02      | -0.04      | 0.02                      | 0.011                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 6            | 1626                      | 1299                     | 102.9             | 102.9             | 0.0        | 0.         | 0.02                      | 0.019                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 7            | 1299                      | 1242                     | 24.29             | 24.79             | 0.50       | 2.06       | 0.04                      | 0.011                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 8            | 1242                      | 778                      | 345.7             | 348.9             | 3.2        | 0.93       | 0.06                      | 0.226                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 9            | 778                       | 625                      | 218.1             | 218.2             | 0.1        | 0.05       | 0.11                      | 0.238                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 10           | 625                       | 441                      | 347.2             | 344.9             | -2.3       | -0.67      | 0.13                      | 0.463                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 11           | 441                       | 345                      | 129.5             | 130.0             | 0.5        | 0.39       | 0.26                      | 0.340                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 12           | 345                       | 263                      | 50.15             | 47.41             | -2.74      | -5.78      | 0.45                      | 0.226                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+
| 13           | 263                       | 200                      | 3.120             | 3.129             | 0.009      | 0.29       | 4.51                      | 0.141                   |
+--------------+---------------------------+--------------------------+-------------------+-------------------+------------+------------+---------------------------+-------------------------+

Table: Band-level ratio of Solar Irradiances, based on average of one
solar cycle

.. figure:: figures/kurucz.jpg
   :align: center

   Kurucz spectrum. ssf in W/m\ :math:`^2`/nm. Source Data: AER. Range from [20, 20000] nm.

.. figure:: figures/lean.jpg
   :align: center

   Lean spectrum. Average over 1 solar cycle, May 1, 1996 to Dec 31, 2006. 
   Source Data: Marsh. ssf in W/m\ :math:`^2`/nm. Range from [120, 99975] nm.

.. figure:: figures/relative_ssf.jpg
   :align: center

   Relative difference, :math:`\frac{\tt{Lean} - \tt{Kurucz}}{.5(\tt{Lean} + \tt{Kurucz}) }`
   between spectra. RRTMG band boundaries are marked with vertical lines.

The heating in each band :math:`b` is scaled by the ratio,
:math:`\frac{{\tt Lean}(t)_b}{{\tt Kurucz}_b}`, where
:math:`{\tt Kurucz}_b` is assumed by RRTMG as specified in
table `tbl_flux_diff`, and :math:`{\tt Lean}(t)_b` is the
solar irradiance specified by the time-dependent solar spectral
irradiance file. :math:`{\tt Lean}(t)_{14}` includes the Lean irradiance
longward of 12195 nm to capture irradiance in the very far infrared.

Surface Exchange Formulations
-----------------------------

The surface exchange of heat, moisture and momentum between the
atmosphere and land, ocean or ice surfaces are treated with a bulk
exchange formulation. We present a description of each surface exchange
separately. Although the functional forms of the exchange relations are
identical, we present the descriptions of these components as developed
and represented in the various subroutines in . The differences in the
exchange expressions are predominantly in the definition of roughness
lengths and exchange coefficients. The description of surface exchange
over ocean follows from Bryan et al. (1996), and the surface exchange
over sea ice is discussed in the sea-ice model documentation. Over
lakes, exchanges are computed by a lake model embedded in the land
surface model described in the following section.

Land
~~~~

In , the NCAR Land Surface Model (LSM) (Bonan 1996) has been replaced by
the Community Land Model CLM2 (Bonan et al. 2002). This new model
includes components treating hydrological and biogeochemical processes,
dynamic vegetation, and biogeophysics. Because of the increased
complexity of this new model and since a complete description is
available online, users of interested in CLM should consult this
documentation at . A discussion is provided here only of the component
of CLM which controls surface exchange processes.

Land surface fluxes of momentum, sensible heat, and latent heat are
calculated from Monin-Obukhov similarity theory applied to the surface
(i.e. constant flux) layer. The zonal :math:`\tau_x` and meridional
:math:`\tau_y` momentum fluxes
(kg m:math:`{}^{-1}`\ s\ :math:`{}^{-2}`), sensible heat :math:`H`
(W m:math:`{}^{-2}`) and water vapor :math:`E`
(kg m:math:`{}^{-2}`\ s\ :math:`{}^{-1}`) fluxes between the surface and
the lowest model level :math:`z_1` are:

.. math::

   \begin{aligned}
   {3}
   \tau_x &= - \rho_1 \overline {(u'w')} & &= - \rho_1 u_*^2 (u_1 /V_a )
   &&= \rho_1 \frac{{u_s - u_1 }}{{r_{am} }} \\ \tau_y &= - \rho_1
   \overline {(v'w')} & &= - \rho_1 u_*^2 (v_1 /V_a ) &&= \rho_1
   \frac{{v_s - v_1 }}{{r_{am} }} \\ H &= \phantom{-}\rho_1 c_p
   (\overline {w'\theta '} )& &= - \rho_1 c_p u_* \theta_* &&= \rho_1 c_p
   \frac{{\theta_{s} - \theta_1 }} {{r_{ah} }} \\ E &= \phantom{-}\rho_1
   (\overline {w'q'} )& &= - \rho_1 u_* q_* &&= \rho_1 \frac{{q_{s} - q_1
   }}{{r_{aw} }}\end{aligned}

.. math::

   \begin{aligned}
   r_{am} &= V_a /u_*^2 \\ r_{ah} &= (\theta_1 - \theta_s )/u_* \theta_*
   \\ r_{aw} &= (q_1 - q_s )/u_* q_*\end{aligned}

where :math:`\rho_1`, :math:`u_1`, :math:`v_1`, :math:`\theta_1` and
:math:`q_1` are the density (kg m:math:`^{-3}`), zonal wind
(m s:math:`^{-1}`), meridional wind (m s:math:`^{-1}`), air potential
temperature (K), and specific humidity (kg kg:math:`^{-1}`) at the
lowest model level. By definition, the surface winds :math:`u_s` and
:math:`v_s` equal zero. The symbol :math:`\theta_1` represents
temperature, and :math:`q_1` is specific humidity at surface. The terms
:math:`r_{am}`, :math:`r_{ah}`, and :math:`r_{aw}` are the aerodynamic
resistances (s m:math:`^{-1}`) for momentum, sensible heat, and water
vapor between the lowest model level at height :math:`z_1` and the
surface at height :math:`z_{0m}+d` [:math:`z_{0h}+d`\ ]. Here
:math:`z_{0m}` [:math:`z_{0h}`\ ] is the roughness length (m) for
momentum [scalar] fluxes, and :math:`d` is the displacement height (m).

For the vegetated fraction of the grid, :math:`\theta_s = T_{af}` and
:math:`q_s = q_{af}`, where :math:`T_{af}` and :math:`q_{af}` are the air temperature
and specific humidity within canopy space. For the non-vegetated
fraction, :math:`\theta_s = T_g` and :math:`q_s = q_g`, where
:math:`T_g` and :math:`q_g` are the air temperature and specific
humidity at ground surface. These terms are described by Dai et al.
(2001).

Roughness lengths and zero-plane displacement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The aerodynamic roughness :math:`z_{0m}` is used for wind, while the
thermal roughness :math:`z_{0h}` is used for heat and water vapor. In
general, :math:`z_{0m}` is different from :math:`z_{0h}`, because the
transfer of momentum is affected by pressure fluctuations in the
turbulent waves behind the roughness elements, while for heat and water
vapor transfer no such dynamical mechanism exists. Rather, heat and
water vapor must ultimately be transferred by molecular diffusion across
the interfacial sublayer. Over bare soil and snow cover, the simple
relation from Zilitinkevich (1970) can be used (Zeng and Dickinson
1998):

.. math::

   \begin{aligned}
   \ln \frac{{z_{0m} }} {{z_{0h} }} & = a\left( {\frac{{u_* z_{0m} }}
   {\nu }} \right)^{0.45} \\ a &= 0.13 \\ \nu &= 1.5 \times 10^{ - 5}
   {\text{m}}^2 {\text{s}}^{-1}\end{aligned}

Over canopy, the application of energy balance

.. math:: R_n - H - L_v\,E = 0

(where :math:`R_n` is the net radiation absorbed by the canopy) is
equivalent to the use of different :math:`z_{0m}` versus :math:`z_{0h}`
over bare soil, and hence thermal roughness is not needed over canopy
(Zeng, Zhao, and Dickinson 1998).

The roughness :math:`z_{0m}` is proportional to canopy height, and is
also affected by fractional vegetation cover, leaf area index, and leaf
shapes. The roughness is derived from the simple relationship
:math:`z_{0m}
= 0.07\,h_c`, where :math:`h_c` is the canopy height. Similarly, the
zero-plane displacement height :math:`d` is proportional to canopy
height, and is also affected by fractional vegetation cover, leaf area
index, and leaf shapes. The simple relationship :math:`d/h_c = 2/3` is
used to obtain the height.

Monin-Obukhov similarity theory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A length scale (the Monin-Obukhov length) :math:`L` is defined by

.. math:: L = \frac{{\theta_v u_*^2 }} {{kg\theta_{v*}}}

where :math:`k` is the von Kàrman constant, and :math:`g` is the
gravitational acceleration. :math:`L > 0` indicates stable conditions,
:math:`L < 0` indicates unstable conditions, and :math:`L = \infty`
applies to neutral conditions. The virtual potential temperature
:math:`\theta_v` is defined by

.. math::

   \theta_v = \theta_1 (1 + 0.61q_1 ) = T_a \left( {\frac{{p_s }} {{p_l
   }}} \right)^{R/c_p } (1 + 0.61q_1 )

where :math:`T_1` and :math:`q_1` are the air temperature and specific
humidity at height :math:`z_1` respectively, :math:`\theta_1` is the
atmospheric potential temperature, :math:`p_l` is the atmospheric
pressure, and :math:`p_s` is the surface pressure. The surface friction
velocity :math:`u_*` is defined by

.. math:: u_*^2 = [\overline {u'w'}^2 + \overline {v'w'}^2 ]^{1/2}

The temperature scale :math:`\theta_*` and :math:`\theta_{ * v}` and a
humidity scale :math:`q_*` are defined by

.. math::

   \begin{aligned}
   \theta_* &= - \overline {w'\theta '} /u_* \\ q_* &= - \overline {w'q'}
   /u_* \\ \theta_{v * } &= - \overline {w'\theta '_v } /u_* \nonumber \\
   & \approx - (\overline {w'\theta '} + 0.61\overline \theta \overline
   {w'q'} )/u_* \\ & = \theta_* + 0.61\overline \theta q_* \nonumber\end{aligned}

(where the mean temperature :math:`\overline \theta` serves as a
reference temperature in this linearized form of :math:`\theta_v` ).

The stability parameter is defined as

.. math:: \varsigma = \frac{{z_1 - d}}{L}\quad ,

with the restriction that :math:`- 100 \leqslant \varsigma \leqslant 2`.
The scalar wind speed is defined as

.. math::

   \begin{aligned}
   V_a^2 &= u_1^2 + v_1^2 + U_c^2 \\ U_c &= \left\{ \begin{array}{ll}
     0.1\>{\text{ms}}^{-1} & {\text{, if }}\varsigma \geqslant {\text{0
     (stable)}} \hfill \\ \beta w_* = \beta \left( {z_i \frac{g}
   {{\theta_v }}\theta_{v * } u_*} \right)^{1/3} & {\text{, if
   }}\varsigma < {\text{0 (unstable)}}\,. \hfill \\
   \end{array}  \right.\end{aligned}

Here :math:`w_*` is the convective velocity scale, :math:`z_i` is the
convective boundary layer height, and :math:`\beta` = 1. The value of
:math:`z_i` is taken as 1000 m

The flux-gradient relations are given by:

.. math::

   \begin{aligned}
   \frac{{k(z_1 - d)}} {{\theta_* }}\frac{{\partial \theta }} {{\partial
   z}} &= \phi_h (\varsigma ) \\ \frac{{k(z_1 - d)}} {{q_*
   }}\frac{{\partial q}} {{\partial z}} &= \phi_q (\varsigma ) \\
   \phi_h &= \phi_q \\
     \phi_m (\varsigma ) &=
               \left\{\begin{array}{ll} (1 - 16\varsigma )^{ - 1/4} &
                                        \mbox{for}~\varsigma < 0 \\ 1 +
                                        5\varsigma & \mbox{for}~0 <
                                        \varsigma < 1
               \end{array}\right. \\
     \phi_h (\varsigma ) &=
               \left\{\begin{array}{ll} (1 - 16\varsigma )^{ - 1/2} &
                                        \mbox{for}~\varsigma < 0 \\ 1 +
                                        5\varsigma & \mbox{for}~0 <
                                        \varsigma < 1
               \end{array}\right.\end{aligned}

Under very unstable conditions, the flux-gradient relations are taken
from Kader and Yaglom (1990):

.. math::

   \begin{aligned}
   \phi_m &= 0.7k^{2/3} ( - \varsigma )^{1/3} \\ \phi_h & = 0.9k^{4/3} (
   - \varsigma )^{ - 1/3}\end{aligned}

To ensure the functions :math:`\phi_m (\varsigma )` and
:math:`\phi_h (\varsigma
)` are continuous, the simplest approach (i.e., without considering any
transition regions) is to match the above equations at
:math:`\varsigma_m = - 1.574` for :math:`\phi_m (\varsigma )` and
:math:`\varsigma_h = -
0.465` for :math:`\phi_h (\varsigma )` .

Under very stable conditions (i.e., :math:`\varsigma > 1` ), the
relations are taken from Holtslag, Bruijn, and Pan (1990):

.. math:: \phi_m = \phi_h = 5 + \varsigma

Integration of the wind profile yields:

.. math::
   :label: eq:windprof

   \begin{aligned}
   {2}  
   V_a &= \frac{{u_* }} {k}f_M (\varsigma ) &&  \\ 
   f_M (\varsigma ) &= \left\{ {\left[ {\ln \left( {\frac{{\varsigma_m L}}
   {{z_{0m} }}} \right) - \psi_m (\varsigma_m )} \right] + 1.14[( -
   \varsigma )^{1/3} - ( - \varsigma_m )^{1/3} ]} \right\}\,, & \varsigma
   &< \varsigma_m = - 1.574 \\ 
   f_M (\varsigma ) &= \left[ {\ln \left( {\frac{{z_1 - d}} {{z_{0m} }}} \right) - \psi_m
   (\varsigma ) + \psi_m \left( {\frac{{z_{0m} }} {L}} \right)}
   \right]\,, & \varsigma_m &< \varsigma < 0 \\
   f_M (\varsigma ) &= \left[ {\ln \left( {\frac{{z_1 - d}} {{z_{0m} }}}
   \right) + 5\varsigma } \right]\,, & 0 &< \varsigma < 1 \\ 
   f_M (\varsigma ) &= \left\{ {\left[ {\ln
   \left( {\frac{L} {{z_{0m} }}} \right) + 5} \right] + [5\ln (\varsigma
   ) + \varsigma - 1]} \right\}\,, & \varsigma &> 1
   \end{aligned}

Integration of the potential temperature profile yields:

.. math::
   :label: eq:ptprof

   \begin{aligned}
   {2}
   \theta_1 - \theta_s & = \frac{{\theta_* }} {k}f_T (\varsigma ) &&
   \\ f_T (\varsigma ) & = \left\{ {\left[ {\ln \left(
   {\frac{{\varsigma_h L}} {{z_{0h} }}} \right) - \psi_h (\varsigma_h )}
   \right] + 0.8[( - \varsigma_h )^{ - 1/3} - ( - \varsigma )^{ - 1/3} ]}
   \right\}\,, & \varsigma & < \varsigma_h = - 0.465 \\ 
   f_T (\varsigma ) & = \left[ {\ln \left(
   {\frac{{z_1 - d}} {{z_{0h} }}} \right) - \psi_h (\varsigma ) + \psi_h
   \left( {\frac{{z_{0h} }} {L}} \right)} \right] \,, & \varsigma_h & <
   \varsigma < 0 \\ f_T (\varsigma ) & = \left[
   {\ln \left( {\frac{{z_1 - d}} {{z_{0h} }}} \right) + 5\varsigma }
   \right] \,, & 0 & < \varsigma < 1 \\ f_T
   (\varsigma ) & = \left\{ {\left[ {\ln \left( {\frac{L} {{z_{0h} }}}
   \right) + 5} \right] + [5\ln (\varsigma ) + \varsigma - 1]} \right\}
   \,, & \varsigma & > 1 \end{aligned}

The expressions for the specific humidity profiles are the same as those
for potential temperature except that (:math:`\theta_1 - \theta_s` ),
:math:`\theta_*` and :math:`z_{0h}` are replaced by (:math:`q_1 - q_s`
), :math:`q_*` and :math:`z_{0q}` respectively. The stability functions
for :math:`\varsigma < 0` are

.. math::

   \begin{aligned}
     \psi_m & = 2\ln\left( {\frac{{1 + \chi }}{2}} \right) + \ln\left(
                   {\frac{{1 + \chi^2 }}{2}} \right) -
                 2\tan^{ - 1} \chi + \frac{\pi }{2} \\ \psi_h & = \psi_q
     = 2\ln\left( {\frac{{1 + \chi^2 }}{2}} \right) \\
   \intertext{where} \chi &= (1 - 16\varsigma )^{1/4}\end{aligned}

Note that the CLM code contains extra terms involving :math:`z_{0m}
/\varsigma`, :math:`z_{0h} /\varsigma`, and :math:`z_{0q} /\varsigma`
for completeness. These terms are very small most of the time and hence
are omitted in Eqs. :eq:`eq:windprof` and :eq:`eq:ptprof`.

In addition to the momentum, sensible heat, and latent heat fluxes, land
surface albedos and upward longwave radiation are needed for the
atmospheric radiation calculations. Surface albedos depend on the solar
zenith angle, the amount of leaf and stem material present, their
optical properties, and the optical properties of snow and soil. The
upward longwave radiation is the difference between the incident and
absorbed fluxes. These and other aspects of the land surface fluxes have
been described by Dai et al. (2001).

Ocean
~~~~~

The bulk formulas used to determine the turbulent fluxes of momentum
(stress), water (evaporation, or latent heat), and sensible heat into
the atmosphere over ocean surfaces are

.. math::
   :label: eqn:turb1

   ( \boldsymbol{\tau}, E, H) = \rho_A \left|\Delta\,{{\boldsymbol{v}}}\right|(C_D
         \Delta\,{{\boldsymbol{v}}}, C_E \Delta\,q, C_p C_H \Delta\theta),
         

where :math:`\rho_A` is atmospheric surface density and :math:`C_p` is
the specific heat. Since does not allow for motion of the ocean surface,
the velocity difference between surface and atmosphere is
:math:`\Delta\,{{\boldsymbol{v}}}= {{\boldsymbol{v}}}_A`, the
velocity of the lowest model level. The potential temperature difference
is :math:`\Delta\theta =
\theta_A - T_s`, where :math:`T_s` is the surface temperature. The
specific humidity difference is :math:`\Delta\,q = q_A - q_s(T_s)`,
where :math:`q_s(T_s)` is the saturation specific humidity at the
sea-surface temperature.

In :eq:`eqn:turb1` , the transfer coefficients between the ocean surface
and the atmosphere are computed at a height :math:`Z_A` and are
functions of the stability, :math:`\zeta`:

.. math::
   :label: eqn:turb2

   C_{(D,E,H)} = \kappa^2 {\left[\ln\left(\frac{Z_A}{Z_{0m}}\right) -
                                 \psi_m\right]}^{-1}
                          {\left[\ln\left(\frac{Z_A}{Z_{0(m,e,h)}}\right)
                                 - \psi_{(m,s,s)}\right]}^{-1}
   

where :math:`\kappa = 0.4` is von Kármán’s constant and
:math:`Z_{0(m,e,h)}` is the roughness length for momentum, evaporation,
or heat, respectively. The integrated flux profiles, :math:`\psi_m` for
momentum and :math:`\psi_s` for scalars, under stable conditions
(:math:`\zeta >
0`) are

.. math:: 
   :label: eqn:turb3

   \psi_m(\zeta) = \psi_s(\zeta) = -5 \zeta. 

For unstable conditions (:math:`\zeta < 0`), the flux profiles are

.. math::
   :label: eqn:turb4

   \begin{aligned}
   \psi_m(\zeta) = &2 \ln[0.5(1 + X)] + \ln[0.5(1 + X^2 )] \nonumber \\ &
   - 2 \tan^{-1} X + 0.5 \pi,   
   . 
   \end{aligned}

.. math::
   :label: eqn:turb5

   \psi_s(\zeta) = 2 \ln[0.5(1 + X^2 )], 

.. math::
   :label: eqn:turb6

   X = (1 - 16 \zeta)^{1/4} . 

The stability parameter used in :eq:`eqn:turb3` –:eq:`eqn:turb6`  is

.. math::
   :label: eqn:turb7

   \zeta = \frac{\kappa\,g\,Z_A}{u^{*2}}\left(\frac{\theta^*}{\theta_v} +
                                        \frac{Q^*}{(\epsilon^{-1} +
                                        q_A)}\right),
   
where the virtual potential temperature is
:math:`\theta_v = \theta_A(1 +
\epsilon q_A)`; :math:`q_A` and :math:`\theta_A` are the lowest level
atmospheric humidity and potential temperature, respectively; and
:math:`\epsilon =
0.606`. The turbulent velocity scales in :eq:`eqn:turb7`  are

.. math::
   :label: eqn:turb8

   \begin{aligned}
   u^* = &C_D^{1/2} |\Delta\,{{\boldsymbol{v}}}|, \nonumber\\ (Q^*,\theta^*) =
   &C_{(E,H)}\frac{|\Delta\,{{\boldsymbol{v}}}|}{u^*}
   (\Delta\,q,\Delta\theta). \end{aligned}

Over oceans, :math:`Z_{0e} = 9.5 \times 10^{-5}` m under all conditions
and :math:`Z_{0h} = 2.2 \times 10^{-9}` m for :math:`\zeta > 0`,
:math:`Z_{0h} = 4.9 \times
10^{-5}` m for :math:`\zeta \le 0`, which are given in Large and Pond
(1982). The momentum roughness length depends on the wind speed
evaluated at 10 m as

.. math::
   :label: eqn:turb9

   \begin{aligned}
   Z_{om} &= 10\,\exp\left[-\kappa{\left(\frac{c_4}{U_{10}} + c_5 +
                           c_6\,U_{10}\right)}^{-1}\right]\,,
   \nonumber\\
   U_{10} &= U_A {\left[1 +
        \frac{\sqrt{C_{10}^N}}{\kappa}\ln\left(\frac{Z_A}{10} -
        \psi_m\right)\right]}^{-1}\,, \end{aligned}

where :math:`c_4 = 0.0027`  m s\ :math:`{}^{-1}`,
:math:`c_5 = 0.000142`, :math:`c_6 =
0.0000764` m:math:`{}^{-1}` s, and the required drag coefficient at 10-m
height and neutral stability is
:math:`C^{N}_{10} = c_4 U^{-1}_{10} + c_5 +
c_6 U_{10}` as given by Large, McWilliams, and Doney (1994).

The transfer coefficients in :eq:`eqn:turb1`  and :eq:`eqn:turb2`  depend on
the stability following :eq:`eqn:turb3` –:eq:`eqn:turb6` , which itself
depends on the surface fluxes :eq:`eqn:turb7`  and :eq:`eqn:turb8` . The
transfer coefficients also depend on the momentum roughness, which
itself varies with the surface fluxes over oceans :eq:`eqn:turb9` . The
above system of equations is solved by iteration.

Sea Ice
~~~~~~~

The fluxes between the atmosphere and sea ice are described in detail in
the sea-ice model documentation.

Dry Adiabatic Adjustment
------------------------

If a layer is unstable with respect to the dry adiabatic lapse rate, dry
adiabatic adjustment is performed. The layer is stable if

.. math:: \frac{\partial T}{\partial p} < \frac{\kappa T}{p}.  
	  :label: 4.j.1

In finite–difference form, this becomes

.. math::
   :label: 4.j.2

   \begin{aligned}
   T_{k+1} - T_k &< C1_{k+1} (T_{k+1} + T_k) + \delta ,
   \\[-1.0em] \intertext{where}\nonumber\\[-2.0em] C1_{k+1}&
   = \frac{\kappa (p_{k+1} - p_k)}{2 p_{k+1/2}}
   ~.\end{aligned}

If there are any unstable layers in the top three model layers, the
temperature is adjusted so that :eq:`4.j.2`  is satisfied everywhere in the
column. The variable :math:`\delta` represents a convergence criterion.
The adjustment is done so that sensible heat is conserved,

.. math::
   :label: 4.j.4

   c_p(\hat{T}_k \Delta p_k + \hat{T}_{k+1} \Delta p_{k+1}) = c_p (T_k
   \Delta p_k + T_{k+1} \Delta p_{k+1}) , 

and so that the layer has neutral stability:

.. math::
   :label: 4.j.5

   \hat{T}_{k+1} - \hat{T}_k = C1_{k+1} (\hat{T}_{k+1} + \hat{T}_k)\, .
   

As mentioned above, the hats denote the variables after adjustment.
Thus, the adjusted temperatures are given by

.. math::
   :label: 4.j.6

   \begin{aligned}
   \hat{T}_{k+1} &= \frac{\Delta p_k}{\Delta p_{k+1} + \Delta p_k
   C2_{k+1}} T_k + \frac{\Delta p_{k+1}}{\Delta p_{k+1} + \Delta p_k
   C2_{k+1}} T_{k+1},  \\[-1.0em]
   \intertext{and}\nonumber\\[-2.0em] \hat{T}_k &= C2_{k+1} \hat{T}_{k+1}
   , \\[-1.0em] \intertext{where}\nonumber\\[-2.0em]
   C2_{k+1} &= \frac{1 - C1_{k+1}}{1 + C1_{k+1}}
   ~.\end{aligned}

Whenever the two layers undergo dry adjustment, the moisture is assumed
to be completely mixed by the process as well. Thus, the specific
humidity is changed in the two layers in a conserving manner to be the
average value of the original values,

.. math::
   :label: 4.j.9

   \hat{q}_{k+1} = \hat{q}_k = (q_{k+1} \Delta p_{k+1} + q_k \Delta
   p_k)/(\Delta p_{k+1} + \Delta p_k) . 

The layers are adjusted iteratively. Initially, :math:`\delta = 0.01` in
the stability check :eq:`4.j.2` . The column is passed through from
:math:`k=1` to a user-specifiable lower level (set to 3 in the standard
model configuration) up to 15 times; each time unstable layers are
adjusted until the entire column is stable. If convergence is not
reached by the 15th pass, the convergence criterion is doubled, a
message is printed, and the entire process is repeated. If
:math:`\delta` exceeds 0.1 and the column is still not stable, the model
stops.

As indicated above, the dry convective adjustment is only applied to the
top three levels of the standard model. The vertical diffusion provides
the stabilizing vertical mixing at other levels. Thus, in practice,
momentum is mixed as well as moisture and potential temperature in the
unstable case.

Prognostic Greenhouse Gases
---------------------------

The principal greenhouse gases whose longwave radiative effects are
included in  are H\ :math:`_2`\ O, CO\ :math:`_2`, O\ :math:`_3`,
CH\ :math:`_4`, N\ :math:`_2`\ O, CFC11, and CFC12. The prediction of
water vapor is described elsewhere in this chapter, and
CO\ :math:`_2` is assumed to be well mixed. Monthly O\ :math:`_3` fields
are specified as input, as described in chapter [datafiles]. The
radiative effects of the other four greenhouse gases (CH\ :math:`_4`,
N\ :math:`_2`\ O, CFC11, and CFC12) may be included in  through
specified concentration distributions (Kiehl et al. 1998) or prognostic
concentrations (Boville et al. 2001).

The specified distributions are globally uniform in the troposphere.
Above a latitudinally and seasonally specified tropopause height, the
distributions are zonally symmetric and decrease upward, with a separate
latitude-dependent scale height for each gas.

Prognostic distributions are computed following Boville et al. (2001).
Transport equations for the four gases are included, and losses have
been parameterized by specified zonally symmetric loss frequencies:
:math:`\partial q / \partial t =  - \alpha ( y, z, t ) q`. Monthly
averaged loss frequencies, :math:`\alpha`, are obtained from the
two-dimensional model of Garcia and Solomon (1994).

We have chosen to specify globally uniform surface concentrations of the
four gases, rather than their surface fluxes. The surface sources are
imperfectly known, particularly for CH\ :math:`_4` and
N\ :math:`_2`\ O in preindustrial times. Even given constant sources and
reasonable initial conditions, obtaining equilibrium values for the
loading of these gases in the atmosphere can take many years.  was
designed for tropospheric simulation with relatively coarse vertical
resolution in the upper troposphere and lower stratosphere. It is likely
that the rate of transport into the stratosphere will be misrepresented,
leading to erroneous loading and radiative forcing if surface fluxes are
specified. Specifying surface concentrations has the advantage that we
do not need to worry much about the atmospheric lifetime. However, we
cannot examine observed features such as the interhemispheric gradient
of the trace gases. For climate change experiments, the specified
surface concentrations are varied but the stratospheric loss frequencies
are not.

Oxidation of CH\ :math:`_4` is an important source of water vapor in the
stratosphere, contributing about half of the ambient mixing ratio over
much of the stratosphere. Although CH\ :math:`_4` is not generally
oxidized directly into water vapor, this is not a bad approximation, as
shown by Le Texier, Solomon, and Garcia (1988). In , it is assumed that
the water vapor (volume mixing ratio) source is twice the
CH\ :math:`_4` sink. This approach was also taken by Mote et al. (1993)
for middle atmosphere studies with an earlier version of the CCM. This
part of the water budget is of some importance in climate change
studies, because the atmospheric CH\ :math:`_4` concentrations have
increased rapidly with time and this increase is projected to continue
into the next century (e.g., Alcamo et al. (1995)) The representation of
stratospheric water vapor in  is necessarily crude, since there are few
levels above the tropopause. However, the model is capable of capturing
the main features of the CH\ :math:`_4` and water distributions.
