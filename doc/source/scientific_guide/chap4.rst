.. _model-physics:

*************
Model Physics
*************

As stated in chapter [chap:coupling], the total parameterization package
in consists of a sequence of components, indicated by

.. math::
   :label:

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

.. _chap-model-sub-physics:

The updating described in the preceding paragraph of all variable except
temperature is straightforward. Temperature, however, is a little more
complicated and follows the general procedure described by involving dry
static energy. The state variable updated after each time-split
parameterization component is the dry static energy :math:`s_i`. Let
:math:`i` be the index in a sequence of :math:`I` time-split processes.
The dry static energy at the end of the :math:`i`\ th process is
:math:`s_i`. The dry static energy is updated using the heating rate
:math:`Q` calculated by the :math:`i`\ th process:

.. math:: 
   :label:

   s_i = s_{i-1} + (\Delta t) Q_i(s_{i-1},T_{i-1},\Phi_{i-1},q_{i-1}, ...)

In processes not formulated in terms of dry static energy but rather in
terms of a temperature tendency, the heating rate is given by
:math:`Q_i = ( T_i - T_{i-1} ) / ( C_p \Delta t )`.

The temperature, :math:`T_i`, and geopotential, :math:`\Phi_i`, are
calculated from :math:`s_i` by inverting the equation for :math:`s`

.. math:: 
   :label:

   s = C_pT + gz = C_pT + \Phi

with the hydrostatic equation

.. math:: 
   :label:

   \Phi_k = \Phi_s + R\sum_{l=k}^{K} H_{kl}{T_v}_l

substituted for :math:`\Phi` as described in Section
[physics:diff:sub:`d`\ se].

The temperature tendencies for each process are also accumulated over
the processes. For processes formulated in terms of dry static energy
the temperature tendencies are calculated from the dry static energy
tendency. Let :math:`\Delta T_i / \Delta t` denote the total
accumulation at the end of the :math:`i`\ th process. Then

.. math::
   :label:

   \frac{\Delta T_i}{\Delta t} = \frac{\Delta T_{i-1}}{\Delta t} + \frac{\Delta s_i}{\Delta t} / C_p

.. math::
   :label:

   \frac{\Delta s_i}{\Delta t} / C_p = \frac{( s_i - s_{i-1})}{\Delta t} / C_p

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

Deep Convection
---------------

The process of deep convection is treated with a parameterization scheme
developed by and modified with the addition of convective momentum
transports by and a modified dilute plume calculation following . The
scheme is based on a plume ensemble approach where it is assumed that an
ensemble of convective scale updrafts (and the associated saturated
downdrafts) may exist whenever the atmosphere is conditionally unstable
in the lower troposphere. The updraft ensemble is comprised of plumes
sufficiently buoyant so as to penetrate the unstable layer, where all
plumes have the same upward mass flux at the bottom of the convective
layer. Moist convection occurs only when there is convective available
potential energy (CAPE) for which parcel ascent from the sub-cloud layer
acts to destroy the CAPE at an exponential rate using a specified
adjustment time scale. For the convenience of the reader we will review
some aspects of the formulation, but refer the interested reader to for
additional detail, including behavioral characteristics of the
parameterization scheme. Evaporation of convective precipitation is
computed following the procedure described in section
[conv:sub:`e`\ vap].

The large-scale budget equations distinguish between a cloud and
sub-cloud layer where temperature and moisture response to convection in
the cloud layer is written in terms of bulk convective fluxes as

.. math::
   :label:

   c_p ( \frac{\partial T}{\partial t} )_{cu} & = - \frac{1}{\rho} \frac{\partial}{\partial z} (
   M_u S_u + M_d S_d - M_c S ) + L(C - E) \,  \\[1ex]
   ( \frac{\partial q}{\partial t} )_{cu} & = - \frac{1}{\rho} \frac{\partial}{\partial z} (
   M_u q_u + M_d q_d - M_c q ) + E - C  ~,

for :math:`z\ge z_b`, where :math:`z_b` is the height of the cloud base.
For :math:`z_s<z<z_b`, where :math:`z_s` is the surface height, the
sub-cloud layer response is written as

.. math::
   :label:

   c_p {( \rho \frac{\partial T}{\partial t} )}_{m} & = - \frac{1}{z_b-z_s} ( M_b [S(z_b) - S_u (z_b)]
   + M_d [S(z_b) - S_d (z_b)] ) \,  \\[1ex] {(\rho \frac{\partial q}{\partial t} )}_{m} & =
   - \frac{1}{z_b-z_s} ( M_b [q(z_b) - q_u (z_b)] + M_d [q(z_b) - q_d (z_b)] )  ~,

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
   :label:

   \frac{\partial h_c}{\partial z} = \lambda (h - h_c), \quad
        z_b<z<z_D    ~.

Mass carried upward by the plumes is detrained into the environment in a
thin layer at the top of the plume, :math:`z_D`, where the detrained air
is assumed to have the same thermal properties as in the environment
(:math:`S_c=S`). Plumes with smaller :math:`\lambda` penetrate to larger
:math:`z_D`. The entrainment rate :math:`\lambda_D` for the plume which
detrains at height :math:`z` is then determined by solving ([zmhc1]),
with lower boundary condition :math:`h_c(z_b)=h_b`:

.. math::
   :label:

     \frac{\partial h_c}{\partial (z-z_b)} & = \lambda_D (h - h_b) -
       \lambda_D (h_c - h_b) \\
     \frac{\partial (h_c - h_b)}{\partial (z-z_b)} - \lambda_D (h_c -
       h_b) & = \lambda_D (h - h_b) \\
     \frac{\partial (h_c - h_b)e^{\lambda_D(z-z_b)}}{\partial (z-z_b)}
       & = \lambda_D (h - h_b)e^{\lambda_D(z-z_b)} \\
     (h_c - h_b)e^{\lambda_D(z-z_b)} & = \int_{z_b}^z \lambda_D (h -
       h_b)e^{\lambda_D(z^\prime-z_b)} dz^\prime \\
     (h_c - h_b) & =\lambda_D \int_{z_b}^z (h -
       h_b)e^{\lambda_D(z^\prime-z)} dz^\prime
   ~.

Since the plume is saturated, the detraining air must have
:math:`h_c=h^*`, so that

.. math::
   :label:

   (h_b - h^*) =\lambda_D \int_{z_b}^z (h_b - h)e^{\lambda_D(z^\prime-z)} dz^\prime ~.

Then, :math:`\lambda_D` is determined by solving ([zmhc2]) iteratively at each :math:`z`.

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
   :label:

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
   :label:

   D_u = - \frac{M_b}{\lambda_0} \frac{\partial \lambda_D}{\partial z}   ~.

The total entrainment rate is then just given by the change in mass flux and the total detrainment,

.. math::
   :label:

   E_u = \frac{\partial M_u}{\partial z} - D_u  ~.

The updraft budget equations for dry static energy, water vapor mixing
ratio, moist static energy, and cloud liquid water, :math:`\ell`, are:

.. math::
   :label:

   \frac{\partial}{\partial z}  ( M_u S_u  ) & =  ( E_u -
   D_u  ) S + \rho LC_u  \\ \frac{\partial}{\partial z}
    ( M_u q_u  ) & = E_u q - D_u q^* + \rho C_u  \\
   \frac{\partial}{\partial z}  ( M_u h_u  ) & = E_u h - D_u
   h^*  \\ \frac{\partial}{\partial z}  ( M_u \ell
    ) & =
   - D_u \ell_d + \rho C_u - \rho R_u  ~,

where ([4.g.8b]) is formed from ([4.g.7]) and ([4.g.8]) and detraining
air has been assumed to be saturated (:math:`q=q^*` and :math:`h=h^*`).
It is also assumed that the liquid content of the detrained air is the
same as the ensemble mean cloud water (:math:`\ell_d = \ell`). The
conversion from cloud water to rain water is given by

.. math::
   :label:

   \rho R_u = c_0 M_u \ell  ~,

following , with :math:`c_0 = 2 \times 10^{-3}\ {\rm m}^{-1}`.

Since :math:`M_u`, :math:`E_u` and :math:`D_u` are given by
([4.g.5]-[4.g.6c]), and :math:`h` and :math:`h^*` are environmental
profiles, ([4.g.8b]) can be solved for :math:`h_u`, given a lower
boundary condition. The lower boundary condition is obtained by adding a
:math:`0.5` K temperature perturbation to the dry (and moist) static
energy at cloud base, or :math:`h_u = h +
c_p\times 0.5` at :math:`z=z_b`. Below the lifting condensation level
(LCL), :math:`S_u` and :math:`q_u` are given by ([4.g.7]) and ([4.g.8]).
Above the LCL, :math:`q_u` is reduced by condensation and :math:`S_u` is
increased by the latent heat of vaporization. In order to obtain to
obtain a saturated updraft at the temperature implied by :math:`S_u`, we
define :math:`\Delta T` as the temperature perturbation in the updraft,
then:

.. math::
   :label:

     h_u & = S_u + L q_u  \\ S_u & = S + c_p \Delta T
      \\ q_u & = q^* + \frac{d q^*}{dT}\Delta T  ~.

Substituting ([zm10.2]) and ([zm10.3]) into ([zm10.1]),

.. math::
   :label:

     h_u     & = S + L q^* + c_p (1 + \frac{L}{c_p}\frac{d q^*}{dT} )\Delta T  \\
             & = h^* + c_p(1+\gamma )\Delta T  \\
	       \gamma & \equiv \frac{L}{c_p}\frac{d q^*}{dT}  \\
    \Delta T & = \frac{1}{c_p}\frac{h_u - h^*}{1+\gamma} ~.

The required updraft quantities are then

.. math::
   :label:

     S_u & = S + \frac{h_u - h^*}{1+\gamma}  \\ 
     q_u & = q^* + \frac{\gamma}{L} \frac{h_u - h^*}{1+\gamma} ~.

With :math:`S_u` given by ([zm10.7]), ([4.g.7]) can be solved for
:math:`C_u`, then ([4.g.9]) and ([4.g.10]) can be solved for
:math:`\ell` and :math:`R_u`.

The expressions above require both the saturation specific humidity to
be

.. math::
   :label:

   q^* = \frac{\epsilon e^*}{p-e^*}, \qquad e^* < p  ~,

where :math:`e^*` is the saturation vapor pressure, and its dependence
on temperature (in order to maintain saturation as the temperature
varies) to be

.. math::
   :label:

   \frac{d q^*}{d T} & = \frac{\epsilon}{p-e^*} \frac{d e^*}{d T}
        - \frac{\epsilon e^*}{(p-e^*)^2}\frac{d (p-e^*)}{d T} \\
      & = \frac{\epsilon}{p-e^*}(1 + \frac{1}{p-e^*}) \frac{d
             e^*}{d T} \\
      & = \frac{\epsilon}{p-e^*}(1 + \frac{q^*}{\epsilon e^*})
             \frac{d e^*}{d T}
   ~.

The deep convection scheme does not use the same approximation for the
saturation vapor pressure :math:`e^*` as is used in the rest of the
model. Instead,

.. math::
   :label:

   e^* = c_1 \exp[\frac{c_2(T - T_f)}{(T-T_f+c_3)} ]   ~,

where :math:`c_1=6.112`, :math:`c_2=17.67`, :math:`c_3=243.5` K and
:math:`T_f=273.16` K is the freezing point. For this approximation,

.. math::
   :label:

     \frac{d e^*}{d T} & = e^* \frac{d}{dT} [\frac{c_2(T -
       T_f)}{(T-T_f+c_3)} ] \\ & = e^*
       [\frac{c_2}{(T-T_f+c_3)}
               - \frac{c_2(T - T_f)}{(T-T_f+c_3)^2} ] \\ & = e^*
       \frac{c_2 c_3}{(T-T_f+c_3)^2}  \\
     \frac{d q^*}{d T}
       & = q^*(1+ \frac{q^*}{\epsilon e^*}) \frac{c_2
                       c_3}{(T-T_f+c_3)^2} 
   ~.

We note that the expression for :math:`\gamma` in the code gives

.. math::
   :label:

   \frac{d q^*}{d T} = \frac{c_p}{L}\gamma
         = q^*(1+ \frac{q^*}{\epsilon}) \frac{\epsilon L}{RT^2} ~.

The expressions for :math:`{d q^*}/{d T}` in ([zm10.11]) and
([zm10.12]) are not identical. Also, :math:`T-T_f+c_3 \neq T` and
:math:`c_2 c_3 \neq \epsilon L/R`.

Downdraft Ensemble
~~~~~~~~~~~~~~~~~~

Downdrafts are assumed to exist whenever there is precipitation
production in the updraft ensemble where the downdrafts start at or
below the bottom of the updraft detrainment layer. Detrainment from the
downdrafts is confined to the sub-cloud layer, where all downdrafts have
the same mass flux at the top of the downdraft region. Accordingly, the
ensemble downdraft mass flux takes a similar form to ([4.g.5]) but
includes a “proportionality factor” to ensure that the downdraft
strength is physically consistent with precipitation availability. This
coefficient takes the form

.. math::
   :label:

   \alpha = \mu  [ \frac{P}{P + E_d}  ]    ~,

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
[4.g.1] – [4.g.4]), the CAPE change due to convective activity can be
written as

.. math::
   :label:

   ( \frac{\partial A}{\partial t} )_{cu} = -M_b F   ~,

where :math:`F` is the CAPE consumption rate per unit cloud base mass
flux. The closure condition is that the CAPE is consumed at an
exponential rate by cumulus convection with characteristic adjustment
time scale :math:`\tau = 7200` s:

.. math::
   :label:

   M_b = \frac{A}{\tau F}    ~.

Numerical Approximations
~~~~~~~~~~~~~~~~~~~~~~~~

The quantities :math:`M_{u,d}`, :math:`\ell`, :math:`S_{u,d}`,
:math:`q_{u,d}`, :math:`h_{u,d}` are defined on layer interfaces, while
:math:`D_u`, :math:`C_u`, :math:`R_u` are defined on layer midpoints.
:math:`S`, :math:`q`, :math:`h`, :math:`\gamma` are required on both
midpoints and interfaces and the interface values :math:`\psi^{k\pm}`
are determined from the midpoint values :math:`\psi^k` as

.. math::
   :label:

   \psi^{k-} = \log(\frac{\psi^{k-1}}{\psi^k})
                  \frac{\psi^{k-1} \psi^k}{\psi^{k-1} - \psi^k}        
   ~.

All of the differencing within the deep convection is in height
coordinates. The differences are naturally taken as

.. math::
   :label:

   \frac{\partial \psi}{\partial z} = \frac{\psi^{k-} - \psi^{k+}}{z^{k-}
   - z^{k+}}  ~,

where :math:`\psi^{k-}` and :math:`\psi^{k+}` represent values on the
upper and lower interfaces, respectively for layer :math:`k`. The
convention elsewhere in this note (and elsewhere in the code) is
:math:`\delta^k\psi = \psi^{k+}- \psi^{k-}`. Therefore, we avoid using the compact :math:`\delta^k`
notation, except for height, and define

.. math::
   :label:

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
   :label:

     S^k & = c_p T^k + g z^k \\ h^k & = S^k + L q^k \\ h^{*k} & = S^k + L
     q^{*k} \\ q^{*k} & = \epsilon e^{*k} / (p^k - e^{*k}) \\ e^{*k} & =
     c_1 \exp[\frac{c_2(T^k - T_f)}{(T^k-T_f+c_3)} ] \\
     \gamma^k & = q^{*k}(1+ \frac{q^{*k}}{\epsilon})
                       \frac{\epsilon L^2}{c_pR{T^k}^2}   ~.

The environmental profiles at interfaces of :math:`S`, :math:`q`,
:math:`q^*`, and :math:`\gamma` are determined using ([zm:sub:`i`\ nt1])
if :math:`|\psi^{k-1}-\psi^{k}|` is large enough. **However, there are
inconsistencies in what happens if ** :math:`|\psi^{k-1}-\psi^{k}|` **is not
large enough**. For :math:`S` and :math:`q` the condition is

.. math::
   :label:

   \psi^{k-} = (\psi^{k-1}+\psi^k)/2, \quad
       \frac{|\psi^{k-1}-\psi^{k}|}{\max(\psi^{k-1}-\psi^{k})} \leq
       10^{-6}
   ~.

For :math:`q^*` and :math:`\gamma` the condition is

.. math::
   :label:

   \psi^{k-} = \psi^{k}, \quad |\psi^{k-1}-\psi^{k}| \leq 10^{-6}  ~.

Interface values of :math:`h` are not needed and interface values of
:math:`h^*` are given by

.. math::
   :label:

     h^{*k-} & = S^{k-} + L q^{*k-}  ~.

The unitless updraft mass flux (scaled by the inverse of the cloud base
mass flux) is given by differencing ([4.g.5]) as

.. math::
   :label:

   M_u^{k-} = \frac{1}{\lambda_0(z^{k-}-z_b)} ( e^{\lambda_D^k
                  (z^{k-}-z_b)} -1 )   ~,

with the boundary condition that :math:`M_u^{M+} =1`. The entrainment
and detrainment are calculated using

.. math::
   :label:

     m_u^{k-} & = \frac{1}{\lambda_0(z^{k-}-z_b)} (
                  e^{\lambda_D^{k+1} (z^{k-}-z_b)} -1 ) \\
     E_u^k & = \frac{m_u^{k-} - M_u^{k+}}{d^kz} \\ D_u^k & =
     \frac{m_u^{k-} - M_u^{k-}}{d^kz}
   ~.

Note that :math:`M_u^{k-}` and :math:`m_u^{k-}` differ only by the
value of :math:`\lambda_D`.

The updraft moist static energy is determined by differencing ([4.g.8b])

.. math::
   :label:

   \frac{M_u^{k-}h_u^{k-} - M_u^{k+}h_u^{k+}}{d^kz} = E_u^k h^k - D_u^k  h^{*k} 

.. math::
   :label:

   h_u^{k-} = \frac{1}{M_u^{k-}}[M_u^{k+} h_u^{k+} + d^kz(
       E_u^k h^k - D_u^k h^{*k} )]   ~,

with :math:`h_u^{M-} = h^M + c_p/2`, where :math:`M` is the layer of
maximum :math:`h`.

Once :math:`h_u` is determined, the lifting condensation level is found
by differencing ([4.g.7]) and ([4.g.8]) similarly to ([4.g.8b]):

.. math::
   :label:

   S_u^{k-} & = \frac{1}{M_u^{k-}}[M_u^{k+} S_u^{k+} + d^kz(E_u^k S^k - D_u^k S^{k} )]  \\
   q_u^{k-} & = \frac{1}{M_u^{k-}}[M_u^{k+} q_u^{k+} + d^kz(E_u^k q^k - D_u^k q^{*k} )]  ~.

The detrainment of :math:`S_u` is given by :math:`D_u^kS^k` not by
:math:`D_u^kS_u^k`, since detrainment occurs at the environmental value
of :math:`S`. The detrainment of :math:`q_u` is given by
:math:`D_u^k q^{*k}`, even though the updraft is not yet saturated. The
LCL will usually occur below :math:`z_0`, the level at which detrainment
begins, but this is not guaranteed.

The lower boundary conditions, :math:`S_u^{M-} = S^M + c_p/2` and
:math:`q_u^{M-}
= q^M`, are determined from the first midpoint values in the plume,
rather than from the interface values of :math:`S` and :math:`q`. The
solution of ([zm:sub:`s`\ u\ :sub:`d`\ 2]) and
([zm:sub:`q`\ u\ :sub:`d`\ 2]) continues upward until the updraft is
saturated according to the condition

.. math::
   :label:

     q_u^{k-} & > q^{*}(T_u^{k-}), \\ T_u^{k-} & = \frac{1}{c_p}(S_u^{k-} - gz^{k-})

The condensation (in units of m\ :math:`^{-1}`) is determined by a
centered differencing of ([4.g.7]):

.. math::
   :label:

   \frac{M_u^{k-}S_u^{k-} - M_u^{k+}S_u^{k+}}{d^kz} = (E_u^k - D_u^k) S^k + L C_u^k

.. math::
   :label:

     C_u^k & = \frac{1}{L} [ \frac{M_u^{k-}S_u^{k-} - M_u^{k+}S_u^{k+}}{d^kz} - (E_u^k - D_u^k) S^k ] ~.

The rain production (in units of m\ :math:`^{-1}`) and condensed liquid
are then determined by differencing ([4.g.9]) as

.. math::
   :label:

   \frac{M_u^{k-}\ell^{k-} - M_u^{k+}\ell^{k+}}{d^kz} = -D_u^k \ell^{k+} + C_u^k - R_u^k  ~,

and ([4.g.10]) as

.. math::
   :label:

   R_u^k = c_0 M_u^{k-} \ell^{k-}  ~.

 Then

.. math::
   :label:

     M_u^{k-}\ell^{k-} & = M_u^{k+}\ell^{k+} - d^kz ( D_u^k \ell^{k+} - C_u^k + c_0 M_u^{k-} \ell^{k-} ) \\
     M_u^{k-}\ell^{k-} (1 + c_0 d^kz ) & = M_u^{k+}\ell^{k+} + d^kz ( D_u^k \ell^{k+} - C_u^k ) \\
     \ell^{k-} & = \frac{1}{M_u^{k-}(1 + c_0 d^kz )} [ M_u^{k+}\ell^{k+} - d^kz (D_u^k \ell^{k+} - C_u^k ) ] ~.

Deep Convective Momentum Transports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sub-grid scale Convective Momentum Transports (CMT) have ben added to
the existing deep convection parameterization following and the
methodology of . The sub-grid scale transport of momentum can be cast in
the same manner as ([4.g.2]). Expressing the grid mean horizontal
velocity vector, :math:`\mathbf{V}`, tendency due to deep convection
transport following gives

.. math::
   :label:

   ( \frac{\partial \mathbf{V}}{\partial t} )_{cu} = - \frac{1}{\rho} \frac{\partial}{\partial z} (
   M_u \mathbf{V}_u + M_d \mathbf{V}_d - M_c \mathbf{V} )  ~,

and neglecting the contribution from the environment the updraft and
downdraft budget equation can similarly be written as

.. math::
   :label:

   -\frac{\partial}{\partial z}  ( M_u  \mathbf{V}_u  ) & = E_u  \mathbf{V}-D_u\mathbf{V}_u  + \mathbf{P}^u_G   \\
   -\frac{\partial}{\partial z}  ( M_d  \mathbf{V}_d  ) & = E_d \mathbf{V} + \mathbf{P}^d_G 
   ~,

where :math:`\mathbf{P}^u_G` and :math:`\mathbf{P}^d_G` the updraft
and downdraft pressure gradient sink terms parameterized from as

.. math::
   :label:

   \mathbf{P}^u_G   & = -C_u M_u\frac{\partial \mathbf{V}}{\partial z}  \\
   \mathbf{P}^d_G   & = -C_d M_d\frac{\partial \mathbf{V}}{\partial z}. 

:math:`C_u` and :math:`C_d` are tunable parameters. In the
implementation we use :math:`C_u = C_d = 0.4`. The value of :math:`C_u`
and :math:`C_d` control the strength of convective momentum transport.
As these coefiicients increase so do the pressure gradient terms, and
convective momentum transport decreases.

Deep Convective Tracer Transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The provides the ability to transport constituents via convection. The
method used for constituent transport by deep convection is a
modification of the formulation described in .

We assume the updrafts and downdrafts are described by a steady state
mass continuity equation for a “bulk” updraft or downdraft

.. math::
   :label:

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

Equation [eq:updraft] is first solved for up and downdraft mixing ratios
:math:`q_u` and :math:`q_d`, assuming the environmental mixing ratio
:math:`q_e` is the same as the gridbox averaged mixing ratio
:math:`\bar q`.

Given the up- and down-draft mixing ratios, the mass continuity equation
used to solve for the gridbox averaged mixing ratio :math:`\bar q` is

.. math::
   :label:

   {\partial \bar q \over \partial t} = {\partial \over \partial p} (M_u
   (q_u-\bar q) + M_d (q_d-\bar q))  ~.

These equations are solved for in subroutine CONVTRAN. There are a few
numerical details employed in CONVTRAN that are worth mentioning here as
well.

-  mixing quantities needed at interfaces are calculated using the
   geometric mean of the layer mean values.

-  simple first order upstream biased finite differences are used to
   solve [eq:updraft] and [eq:masscon].

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

Evaporation of convective precipitation
---------------------------------------

The employs a style evaporation of the convective precipitation as it
makes its way to the surface. This scheme relates the rate at which
raindrops evaporate to the local large-scale subsaturation, and the rate
at which convective rainwater is made available to the subsaturated
model layer

.. math::
   :label:

   E_{r_k} = K_E \; (1 - \text{RH}_k) \; {(\hat{R}_{r_k})}^{1/2} ~.

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
for which :math:`R_{r_k} \not= 0` using ([4.g.15]), where in this case
:math:`R_{r_k} \equiv \; \hat{R}_{r_k}`. This rate is used to evaluate
an evaporative reduction in :math:`R_{r_k}` which is then accumulated
with the previously diagnosed rainwater flux in the layer below,

.. math::
   :label:

   \hat{R}_{r_{k+1}} = \hat{R}_{r_k} - ({{\Delta p_k} \over g}) \; E_{r_k} + R_{r_{k+1}}  ~.

A local increase in the specific humidity :math:`q_k` and a local
reduction of :math:`T_k` are also calculated in accordance with the net
evaporation

.. math::
   :label:

   q_k = q_k + E_{r_k} \; 2 \Delta t \;
   
 and

.. math::
   :label:

   T_k = T_k - ( {L \over c_p} ) E_{r_k} \; 2 \Delta t \;

The procedure, ([4.g.15])-([4.g.18]), is then successively repeated for
each model level in a downward direction where the final convective
precipitation rate is that portion of the condensed rainwater in the
column to survive the evaporation process

.. math::
   :label:

   P_s = ( \hat{R}_{r_{K}} - ({{\Delta p_K} \over g}) \;
   E_{r_K} ) /\rho_{H_{2}0}
   
In global annually averaged terms, this evaporation procedure produces
a very small reduction in the convective precipitation rate where the
evaporated condensate acts to moisten the middle and lower troposphere.

Conversion to and from dry and wet mixing ratios for trace constituents in the model
------------------------------------------------------------------------------------

There are trade offs in the various options for the representation of
trace constituents :math:`\chi` in any general circulation model:

1. When the air mass in a model layer is defined to include the water
   vapor, it is frequently convenient to represent the quantity of trace
   constituent as a “moist” mixing ratio :math:`\chi^m`, that is, the
   mass of tracer per mass of moist air in the layer. The advantage of
   the representation is that one need only multiply the moist mixing
   ratio by the moist air mass to determine the tracer air mass. It has
   the disadvantage of implicitly requiring a change in :math:`\chi^m`
   whenever the water vapor :math:`q` changes within the layer, even if
   the mass of the trace constituent does not.

2. One can also utilize a “dry” mixing ratio :math:`\chi^d` to define
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

.. math:: 
   :label:

   \delta p^d_{i,k} = (1-q^0_{i,k}) \delta^m_{i,k}

for column :math:`i`, level :math:`k`. Note that the specific humidity
used is the value defined at the beginning of the physics update. We
define the transformation between dry and wet mixing ratios to be

.. math:: 
   :label:

   \chi^d_{i,k} = (\delta p^d_{i,k} / \delta p^m_{i,k}) \chi^m_{i,k}

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
   :label:

   {\partial \chi \over \partial t} = {\partial F(\chi) \over \partial p}
   

where :math:`F` indicates a flux of :math:`\chi`. For example, in
convective transports :math:`F(\chi)` might correspond to
:math:`M_u \chi` where :math:`M_u` is an updraft mass flux. In
principle one should adjust :math:`M_u` to reflect the fact that it may
be moving a mass of dry air or a mass of moist air. We assume these
differences are small, and well below the errors required to produce
equation [wetdry1] in the first place. The same is true for the
diffusion coefficients involved in turbulent transport. All processes
using equations of such a form still satisfy a conservation relationship

.. math:: {\partial \over \partial t} \sum_k{\chi_k \delta p_k}  = F_{kbot} - F_{ktop}
   :label:

provided the appropriate :math:`\delta p` is used in the summation.

Prognostic Condensate and Precipitation Parameterization
--------------------------------------------------------

Introductory comments
~~~~~~~~~~~~~~~~~~~~~

The parameterization of non-convective cloud processes in  is described
in and . The original formulation is introduced in . Revisions to the
parameterization to deal more realistically with the treatment of the
condensation and evaporation under forcing by large scale processes and
changing cloud fraction are described in . The equations used in the
formulation are discussed here. The papers contain a more thorough
description of the formulation and a discussion of the impact on the
model simulation.

The formulation for cloud condensate combines a representation for
condensation and evaporation with a bulk microphysical parameterization
closer to that used in cloud resolving models. The parameterization
replaces the diagnosed liquid water path of CCM3 with evolution
equations for two additional predicted variables: liquid and ice phase
condensate. At one point during each time step, these are combined into
a total condensate and partitioned according to temperature (as
described in section [microscale]), but elsewhere function as
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
phase change ; and 2) a bulk microphysical component that controls the
conversion from condensate to precipitate . These components are
discussed in the following two sections.

Description of the macroscale component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As in and , the controlling equations for the water vapor mixing ratio,
temperature, and total cloud condensate are written as

.. math::
   :label:

   \frac{{\partial q}}{{\partial t}} & = A_q - Q_{} + E_r  \\
   \frac{{\partial T}}{{\partial t}} & = A_T + \frac{L}{{c_p }}(Q - E_r )  \\
   \frac{{\partial l}}{{\partial t}} & = A_l + Q - R_l ~,

where :math:`A_q`, :math:`A_T`, and :math:`A_l` are tendencies of water
vapor, temperature, and cloud water from processes other than
large-scale condensation and evaporation of cloud and rain water.
:math:`A_q`, :math:`A_T` and :math:`A_l` include advective, expansive, radiative, turbulent,
and convective tendencies. The convective tendencies include evaporation
of convective cloud and convective precipitation. For simplicity, all
these processes are collectively called advective tendencies. They are
assumed to be uniform across the whole model grid cell, although this
assumption can be relaxed as discussed in . :math:`Q` is the
grid-averaged net stratiform condensation of cloud meteors (condensation
minus evaporation). :math:`E_r` is the grid-averaged evaporative rate
of rain and snow. :math:`R_l` is the conversion rate of cloud water to
rain and snow. This section is devoted to the determination of the term
:math:`Q` in equations ([mac1])–([mac3]).

The controlling equation of relative humidity :math:`U`, when written
on a pressure surface, can be derived from ([mac1]) and ([mac2]) as

.. math::
   :label:

   \frac{{\partial U}}{{\partial t}} & = \alpha \frac{{\partial
   q}}{{\partial t}} - \beta \frac{{\partial T}}{{\partial t}} \\ & =
   \alpha A_q - \beta A_T - \gamma (Q - E_r )  \\

where

.. math::
   :label:

   \nonumber\\[-2.0em] \alpha & = \frac{1}{{q_s }}, \\
   \beta & = \frac{q}{{q_s^2 }}\frac{{\partial q_s }}{{\partial T}}, \\
   \gamma & = \alpha + \frac{L}{{c_p }}\beta ~.

Note that :math:`\alpha`, :math:`\beta`, and :math:`\gamma` are all
positive. They can be viewed as the efficiencies of moisture advection,
cold advection, and net evaporation in changing the relative humidity
:math:`U`. Changing :math:`U` can alter the fractional cloud cover. As
in and , ice saturation is not separately considered here; rather, it is
approximated by a weighted average :math:`q_s (T)` of the saturation
mixing ratios over ice and water. The dependence of :math:`q_s` on
pressure is not made explicit since pressure enters into the calculation
only as a parameter.

Equations ([mac1])–([mac4]) are applicable on both the grid scale and
sub-grid scale as long as :math:`Q`, :math:`E_r`, and :math:`R_l` are
appropriately defined. In the following, a hat denotes variables in the
cloudy portion of a grid box to distinguish them from variables of the
whole grid box, and :math:`{\cal C}` denotes the fractional cloud
coverage. For the portion of the grid box that is cloudy before and
after the calculation of fractional condensation (i.e., the cloudy area
that does not experience clear-cloudy conversion), equation ([mac4])
becomes

.. math::
   :label:

   \alpha \hat A_q - \hat \beta \hat A_T - \hat \gamma \hat Q = 0.

This follows from the assumption that :math:`E_r= 0` and :math:`U = 1` in the saturated cloud interior. Thus the
condensation rate in this portion of the grid box is

.. math::
   :label:

   \hat Q = \frac{{\alpha \hat A_q - \hat \beta \hat A_T }}{{\hat \gamma }}
   

and the in-cloud condensate equation becomes

.. math::
   :label:

   \frac{{\partial \hat l}}{{\partial t}} = \hat A_l + \frac{{\alpha \hat
   A_q - \hat \beta \hat A_T }}{{\hat \gamma }} - \hat R_l . 

Since the total cloud water can be written as
:math:`l = {{\cal C}}\hat l`, it follows that

.. math::
   :label:

   \frac{{\partial l}}{{\partial t}} = {{\cal C}}\frac{{\partial \hat
   l}}{{\partial t}} + \hat l^* \frac{{\partial {{\cal C}}}}{{\partial t}}
   

The symbol :math:`\hat l^*` denotes the mean cloud condensate of the
newly formed or dissipated clouds within a time step. The first term on
the right hand side of the above equation represents the evolution of
cloud water within existing clouds, and the second term represents the
change in cloud water associated with expansion and contraction of cloud
boundaries. Theoretically, newly formed or dissipated clouds should have
zero cloud water content, except for detrained cloud from cumulus.
However, because of the finite time step in the integration of the cloud
water equation, the second term may be nonzero. set
:math:`\hat l^* = \hat l`, and the same closure is used in . Inserting
([mac6]) and the relations 
:math:`R_l = {\cal C}\hat{R_l}` as well as 
:math:`A_T = \hat A_T`, :math:`A_q = \hat{A_q}`, and
:math:`A_l =\hat{A_l}` into ([mac3]) yields:

.. math::
   :label:

   \hat l^* \frac{{\partial {{\cal C}}}}{{\partial t}} = (1 - {{\cal C}})A_l + Q
   - {{\cal C}}(\frac{{\alpha A_q - \hat \beta A_T }}{{\hat \gamma }})
   

This equation states that the condensation rate is linked with
fractional cloudiness change as required by the total water budget.
Equation ([mac8]) is not integrated in the present formulation. Instead,
it is used to calculate the condensation rate as follows.

The fractional cloud cover and grid-scale relative humidity are related
by

.. math::
   :label:

   {{\cal C}}= {{\cal C}}(U,b)
   

where :math:`b` denotes a generic variable describing vertical
stability, local Richardson number, cumulus mass flux, etc. The term
:math:`b` varies with space and time. This equation is assumed to be
valid when the relative humidity :math:`U` is larger than a threshold
value :math:`U_{00}`, which is the minimum grid-scale relative
humidity at which clouds are present.

Taking partial derivatives of the equation ([mac9]) with respect to time
gives

.. math::
   :label:

   \frac{{\partial {{\cal C}}}}{{\partial t}} = \frac{{\partial
   {{\cal C}}}}{{\partial U}}\frac{{\partial U}}{{\partial t}} +
   \frac{{\partial {{\cal C}}}}{{\partial b}}\frac{{\partial b}}{{\partial t}}

With the definitions

.. math::
   :label:

   F_a & = \frac{{\partial {{\cal C}}}}{{\partial U}} \\
   [-2.0em] \intertext{and }\nonumber\\[-2.0em] F_b & = 
   [(\frac{{\partial {{\cal C}}}}{{\partial b}})/(\frac{\partial {\cal C}}{\partial U})]\frac{\partial b}{\partial t} ~,

the time derivative of cloud amount becomes

.. math::
   :label:

   F_a^{ - 1} \frac{{\partial {{\cal C}}}}{{\partial t}} = \frac{{\partial  U}}{{\partial t}} + F_b
   

It is assumed that :math:`F_a` and :math:`F_b` can be calculated
without the knowledge of the condensation rate. Substituting the
relative humidity equation ([mac4]) into equation ([mac10]) yields

.. math::
   :label:

   F_a^{ - 1} \frac{{\partial {{\cal C}}}}{{\partial t}} = \alpha A_q - \beta A_T - \gamma (Q - E_r) + F_b

Eliminating :math:`{\partial {{\cal C}}}/{\partial t}` between ([mac8]) and ([mac11]) gives

.. math::
   :label:

   Q & = c_q A_q - c_T A_T - c_l A_l + c_r E_r + \sigma \hat l^* F_b  \\[-1.0em]
   \intertext{with}\nonumber\\[-2.0em] c_q & = 
   \frac{\alpha }{{\hat \gamma }}{{\cal C}}+ (1 - \frac{\gamma }{{\hat \gamma }}
   {{\cal C}})\sigma \alpha \hat l^* \\ c_T & = \frac{{\hat \beta }}{{\hat \gamma }}{{\cal C}}+ (1 - \frac{\gamma }{{\hat \gamma
   }}\frac{{\hat \beta }}{\beta }{{\cal C}})\sigma \beta \hat l^* \\
   c_l & = (1 - {{\cal C}})\sigma F_a^{ - 1} \\ c_r & = \sigma
   \gamma \hat l^* \\ \intertext{where}\nonumber\\[-2.0em] \sigma & =
   \frac{1}{{F_a^{ - 1} + \gamma \hat l^* }} ~.

All coefficient variables are positive, and all are non-dimensional
except for :math:`C_T` and :math:`\beta` which have units of 1/K.
Equation ([mac12]) is valid when :math:`U \ge U_{00}`. The terms in
the equation have the following physical interpretation. Moist advection
(positive :math:`A_q`) and cold advection (negative :math:`A_T`)
produce condensation. Evaporation of rain/snow water (positive
:math:`E_r`) also produces cloud condensation because it changes the mean relative
humidity, thus increasing cloud amount and cloud water. Import of cloud
water (positive :math:`A_l`) leads to evaporation. The reason is that
it increases cloud fraction, thus requiring a higher clear-sky relative
humidity which has to be generated by evaporation. The increase of cloud
fraction from a non-water source through :math:`F_b`, however, requires condensation.

To evaluate :math:`F_a`, the cloud routine is called twice each time
step with relative humidity perturbed by one percent (indicated by a
:math:`*` superscript) while holding all other variables in the model
fixed. Thus,

.. math::
   :label:

   F_a \approx \frac{{\Delta {{\cal C}}}}{{\Delta U}} = \frac{{{{\cal C}}^* -
   {{\cal C}}}}{{U^* - U}}.

In this implementation, all :math:`b` variables are assumed fixed in
the stratiform condensation calculation, and therefore :math:`F_b = 0`.
Since a top-hat distribution is adopted for the cloud water
distribution, :math:`\hat l_{}^* = \hat l`.

The effects of convection on cloud cover are introduced through the
convective tendencies. Detrainment of cloud water from the convection
scheme is used as input in the calculation of :math:`A_l`,
:math:`A_T` and :math:`A_q`. In the original version of the
parameterization, the detrained cloud water from convection was assumed
to evaporate.

The calculation is carried out by categorizing each model grid into one
of four cases:

-  If :math:`U = 1`, :math:`Q` is calculated from ([mac5]);

-  if :math:`1 > U \ge U_{00}`, :math:`Q` calculated from ([mac12]);

-  if :math:`U < U_{00}` but :math:`l > 0`, :math:`Q = - l`; and

-  if :math:`U < U_{00}` and :math:`l = 0`, :math:`Q = 0`.

The use of the threshold relative humidity follows from equation
([mac9]).

Description of the microscale component
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The condensation process has been determined by forcing terms and
closure assumptions described in the previous subsection rather than an
approach in which a supersaturation is calculated and CCN can nucleate
and grow. Therefore the whole microphysical calculation reduces to
modeling the process of conversion of cloud condensate to precipitation.
The microscale component of the parameterization determines the
evaporation :math:`E_R` and conversion of condensate to precipitate
:math:`R_l`.

The formulation follows closely the bulk microphysical formulations used
in smaller scale cloud resolving models rather than those of . A method
based upon cloud resolving models makes an explicit connection between
the formation of precipitate and individual physical quantities like
droplet or crystal number, shape of size distribution of precipitate,
etc. It also separates the various processes contributing to
precipitation more strongly, and makes diagnosis more straightforward.
Because these quantities must represent an ensemble of cloud types in
any given region (or grid volume) the new formulation still involves
gross approximations, but it is much easier to control the
parameterizations and understand their individual impact when the
processes are isolated from each other.

As in , the parameterization is expressed in terms of a single predicted
variable representing total suspended condensate. Within the
parameterization, however, there are four types of condensate expressed
as mixing ratios: a liquid and ice phase for suspended condensate with
minimal fall speed (:math:`q_l` and :math:`q_i`) and a liquid and ice
phase for falling condensate, i.e. precipitation (:math:`q_r` and
:math:`q_s`). Currently, only the suspended condensates (:math:`q_l` and
:math:`q_i`) are integrated in time; the other quantities are diagnosed
as described below.

Before beginning the microphysical calculation, the total condensate is
decomposed into liquid and ice phases assuming the fraction of ice is

.. math:: f_i = \frac{T - T_{max}}{T_{min}-T_{max}}, \quad T_{min} \leq T \leq T_{max}

with :math:`f_i(T<T_{min}) =1` and :math:`f_i(T>T_{max}) =0`. :math:`T`
is the grid volume temperature. The bounds are adjustable constants with
current settings :math:`T_{min}=-40^\circ` C and
:math:`T_{max}=-10^\circ` C. Observations and more detailed
microphysical models show a broad range of ratios of liquid to ice in
clouds, and it is difficult to be certain of an appropriate range for
this parameter.

Liquid and ice mass mixing ratios (:math:`\ell` and :math:`I`) are
independently advected, diffused, and transported by convection. The
detrained liquid from the ZM convection is all added to the cloud
liquid, since the ZM scheme does not have an ice phase. After the
convection and sedimentation (see below), the liquid and ice are
recalculated from the total cloud condensate

.. math::
   :label:

     \ell_{n\prime} & = (\ell_n + I_n)(1-f_i) \\
        I_{n\prime} & = (\ell_n + I_n)f_i \ .

The heating due to the change in cloud ice is

.. math:: Q^k = L_f \frac{I_n - I_{n\prime}}{\delta t}.

The stratiform cloud condensate tendency is computed and partitioned
according to :math:`f_i`. The excess heating due to cloud ice production
instead of cloud liquid production is included with the evaporation and
freezing of precipitation below.

The *in-cloud* liquid water mixing ratio is

.. math:: \hat q_l = (1-f_i) q_c / {{\cal C}}

and the *in-cloud* ice water mixing ratio is assumed to be

.. math:: \hat q_i = (f_i)q_c / {{\cal C}}.

 The grid volume mean quantities have been converted to in-cloud
quantities by dividing the mean mixing ratios by the cloud fraction.

The evaporation of precipitation is computed for each source of
precipitation using the same expressions, following . The precipitate
falling from above can be a mixture of snow and rain. The flux of total
precipitation :math:`F^{k+}` on each interface is

.. math:: F^{k+} = F^{k-} + \frac{\delta^k p}{g} (P^k - E^k)

where :math:`P^k` and :math:`E^k` are precipitation production and
evaporation, respectively. :math:`P^k` is determined by the convection
or stratiform microphysics routines and

.. math:: E^k = k_e (1 - c^k) (1-\min(1,\frac{q^k}{q_*^k})) (F^{k-})^{1/2}

where :math:`k_e` is an adjustable constant and :math:`c^k` is the
fractional cloud area. The :math:`(1 - c^k)` factor represents a random
overlap assumption; precipitation falling into the existing cloud in a
layer does not evaporate. For stratiform precipitation,
:math:`k_e=1\times 10^{-5}`, while for convective precipitation,
:math:`k_e` is considered to be an adjustable parameter and is specified
according to the table in appendix [adjustableparameters].

Two bounds are applied to :math:`E^k`:

#. :math:`E^k \leq \frac{q_*^k - q^k}{\delta t}`, to prevent supersaturation;

#. :math:`E^k \leq F^{k-}\frac{g}{\delta^k p}`, to prevent :math:`F^{k+}<0`. Note that precipitation is not permitted to evaporate in the layer in which it forms;

Exactly the same procedure is applied to snow,

.. math:: F_s^{k+} = F_s^{k-} + \frac{\delta^k p}{g} (P_s^k - E_s^k - M^k)

where :math:`P_s^k = f_{s} P^k` is the snow production, :math:`f_s(T)`
is the snow production fraction, :math:`M^k` is the melting rate and

.. math:: 
   :label:

   E_s^k = E^k F_s^{k-}/F^{k-}

so snow evaporates in proportion to the fraction of snow in the
precipitation flux on the upper interface.

The snow production fraction is simple function of temperature

.. math:: 
   :label:

   f_s =  \frac{T - T_{s,max}}{T_{s,min}-T_{s,max}}, \quad T_{min} \leq T \leq T_{max}

with :math:`f_s(T<T_{s,min}) =1` and :math:`f_s(T>T_{s,max}) =0`.
:math:`T` is the grid volume temperature. The bounds are adjustable
constants with current settings :math:`T_{min}=-5^\circ` C and
:math:`T_{max}=0^\circ` C.

Falling precipitation is not permitted to freeze. Snow is produced only
by the assumed snow fraction :math:`f_s` in the production term. Snow
does not melt unless it it falls into a layer with :math:`T^k>0` C, in
which case :math:`M^k = F_s^k
\frac{g}{\delta^k p}` so that all the snow melts.

The net heating rate due to freezing, melting and evaporation of
precipitation is

.. math:: 
   :label:

   Q^k = -L_v E^k + L_f(P_i^k - E_s^k - M^k)

This is the method by which the heating due to :math:`L_f` is included
for all condensation processes. For convective precipitation,
:math:`P_i^k \equiv P_s^k`, while for stratiform precipitation,
:math:`P_i = f_i C^k` where :math:`C^k` is the net condensation rate in
the cloud. Both the cloud ice fraction and the snow production fractions
are determined by :math:`f_i`, with :math:`P_s^k` coming from the cloud
ice. For stratiform precipitation, the above equations are iterated once
to allow the first estimate of the heating to change :math:`T` and
consequently :math:`q_*` (but not :math:`f_i`) for the 2nd iteration.

Cloud liquid and ice particles are allowed to sediment using independent
settling velocities, similar to the form described by . The liquid and
ice settling fluxes are computed at interfaces, from velocities and
concentrations at midpoints, using a *SPITFIRE* solver . The resulting
flux at each interface is constrained to be smaller than the mass of
liquid or ice in the layer above. This constraint does not allow for
particles falling into the layer from above.

Sedimenting particles evaporate if they fall into the cloud free portion
of a layer. No bound is applied to prevent supersaturation of the layer.
This will be accounted for in the subsequent cloud condensate tendency
calculation. Maximum overlap is assumed for stratiform clouds, so
particles only evaporate if the cloud fraction is larger in the layer
above. The overlapped fraction is

.. math:: 
   :label:

   f_o = \min(\frac{f_c^k}{f_c^{k-1}},1)

The ice velocity :math:`v_i` is a function only of the effective radius
:math:`R_e` (see Section [eff:sub:`r`\ ad] for more information and a
plot), which itself is a function only of :math:`T`. For
:math:`R_e < 40\times 10^{-6}` m, the Stokes terminal velocity equation
for a falling sphere is used

.. math:: v_i = \frac{2}{9} \frac{\rho_w g R_e^2}{\eta}

where :math:`\eta=1.7\times 10^{-5} \rm ~kg~m/s` is the viscosity of air
and the density of air has been neglected compared to the density of
water.

For :math:`R_e > 40\times 10^{-6}` m, the Stokes formula is no longer
valid and we use a linear dependence of :math:`v_i` on
:math:`r = 10^{-6}\times R_e`

.. math::
   :label:

   v_i(r) = v_i(40) + (r-40) \frac{v_{400} - v_i(40)}{400 - 40}

where :math:`v_{400} = 1.0` m/s is the assumed velocity of a 400 micron
sphere, close to the value suggested by .

The liquid particle velocity depends only on whether the cloud is over
land or ocean, as is true of the liquid effective radius. The net liquid
velocity :math:`v_l` is

.. math:: 
   :label:

   v_l = v_l^{land} f^{land} + v_l^{ocean} f^{ocean}

where :math:`f^{land}` and :math:`f^{ocean}` are the land and ocean
fractional areas of the cell, respectively. The ocean fraction may
contain sea ice. The velocities are :math:`v_l^{land} = 1.5` and
:math:`v_l^{ocean} = 2.8` cm/s.

It is assumed that there are five processes that convert condensate to
precipitate:

:math:`\bullet` The conversion of liquid water to rain (PWAUT) follows a
formulation originally suggested by :

.. math::
   :label:

   PWAUT = C_{l,aut} {\hat q_l}^2 \rho_a / \rho_w ( \hat q_l \rho_a /
   \rho_w N)^{1/3} H(r_{3l}-r_{3lc}).

Here :math:`\rho_a` and :math:`\rho_w` are the local densities of air
and water respectively, and :math:`N` is the assumed number density of
cloud droplets. :math:`C_{l,aut} = 0.55 \pi^{1/3}k (3/4)^{4/3} (1.1)^4`,
and :math:`k =
1.18 \times 10^6` cm\ :math:`^{-1}` sec\ :math:`^{-1}` is the Stokes
constant.

:math:`N` is set to :math:`400/cm^3` over land near the surface,
:math:`150 /cm^3` over ocean, and :math:`75 /cm^3` over sea ice. The
number density also varies with distance from land by a factor equal to
the distance to the nearest land point divided by 1000 km and multiplied
by the cosine of latitude. The provides a sharper transition from land
properties to ocean properties near the poles.

The terms :math:`r_{3l}` and :math:`r_{3lc}` are the mean volume radii
of the droplets and a critical value below which no auto-conversion is
allowed to take place, respectively. :math:`H` is the Heaviside function
with the definition :math:`H(x) = (0,1)` for :math:`x (<,\ge) 0`. The
volume radius :math:`r_{3l} = [(3 \rho_a q_l)/(4 \pi N\rho_w)]^{1/3}`.
The standard value for the critical mean volume radius at which
conversion begins is :math:`15\mu`\ m. has shown that this
parameterization results in collection rates that far exceed those
calculated in more realistic stochastic collection models. This is
because the parameterization is based upon a collection efficiency
corresponding to a cloud droplet distribution that has already been
substantially modified by precipitation. suggest that a much smaller
choice is appropriate prior to precipitation onset. Therefore the
parameterization is adjusted by making :math:`C_{l,aut}
arrow 0.1C_{l,aut}` when the precipitation flux leaving the grid
box is below 0.5 mm/day.

:math:`\bullet` The collection of cloud water by rain from above (PRACW)
follows

.. math:: PRACW = C_{racw}\rho^{3/2} \hat q_l q_r

where :math:`C_{racw} = 0.884 (g/(\rho_w \; 2.7 \times 10^{-4}))^{1/2}
s^{-1}` is derived by assuming a Marshall-Palmer distribution of
rainwater falling through a uniformly distributed cloud water field, and
:math:`q_r` is determined iteratively.

:math:`\bullet` The auto-conversion of ice to snow (PSAUT) is similar in
form to that originally proposed by for liquid processes and for ice.
However, it includes a temperature dependence similar to that proposed
in

.. math:: PSAUT = C_{i,aut} H(\hat q_i-q_{ic}).

The rate of conversion of ice (:math:`C_{i,aut}`) to snow is set to
:math:`10^{-3}
s^{-1}` when the ice mixing ratio exceeds a critical threshold
:math:`q_{ic}`. The threshold is set to :math:`q_{ic,warm}` at
:math:`T =
0^{\circ}C` and :math:`q_{ic,cold}` at :math:`T=-20^{\circ}C`. Values
for :math:`q_{ic,warm}` and :math:`q_{ic,cold}` are given in Appendix
[adjustableparameters]. The threshold varies linearly in temperature
between these two limits.

:math:`\bullet` The collection of ice by snow (PSACI) follows , although
it has been rewritten in the form:

.. math:: 
   :label:

   PSACI = C_{sac}e_i \hat q_i.

where :math:`e_i` (:math:`= 1`) is an ice collection efficiency. The
coefficient of collection is

.. math::

   C_{sac} = c_7 \rho^{c_8}_a \tilde P^{c_5}
  
Here, :math:`c_5`, :math:`c_7` and :math:`c_8` are constants arising
from the assumed shape of the snow distribution.

The coefficients of the equation ([e-sac]) arise from some algebraic
manipulation of the expressions appearing in . They in turn depend upon
the specification for parameters describing an exponential size
distribution for graupel-like snow. The parameter values used in are
adopted in the  implementation. The parameters are a slope parameter
:math:`d = 0.25`; an empirical parameter :math:`c =
152.93` controlling the fall speed of graupel-like snow; and the assumed
integrated number density of snow :math:`N_s =
3. \times 10^{-2}`. The constants appearing in equation ([e-sac]) can be
expressed as

.. math::
   :label:

   c_1 & = \pi N_s c \Gamma(3+d) / 4 \\ c_2 & = 6 (\pi \rho_s N_s)^{d+4} /
   \bigl[c \Gamma(4+d) \rho_0^{0.5}\bigr] \\ c_5 & = (3+d)/(4+d) \\ c_6 & =
   (3+d)/4 \\ c_7 & = c_1 \rho_0^{0.5} c_2^{c_5}/(\rho_s N_s)^{c_6} \\
   \intertext{and} c_8 & = -0.5/(4+d)
   ~.

Here :math:`\Gamma` is the Gamma function, :math:`\rho_s = 0.1` is the
density of snow, and :math:`\rho_0 = 1.275 \times 10^{-3}` is a
reference air density at the surface. All constants have been expressed
in CGS units. The constants follow from integrating the geometric
collection of a uniform distribution of suspended cloud liquid or ice
over the size distribution of snow.

The collection of liquid by snow (PSACW) also follows :

.. math:: 
   :label:

   PSACW = C_{sac}e_w \hat q_l.

where :math:`e_w` is the water collection efficiency. note that the work
by suggests that the riming process is too efficient using the standard
values. There the collection efficiency is reduced by an order of
magnitude to :math:`e_w =0.1`.

Dry Adiabatic Adjustment
------------------------

If a layer is unstable with respect to the dry adiabatic lapse rate, dry
adiabatic adjustment is performed. The layer is stable if

.. math:: 
   :label:

   \frac{\partial T}{\partial p} < \frac{\kappa T}{p}.  

In finite–difference form, this becomes

.. math::
   :label:

   T_{k+1} - T_k & < C1_{k+1} (T_{k+1} + T_k) + \delta ,
   \\[-1.0em] \intertext{where}\nonumber\\[-2.0em] C1_{k+1} &
   = \frac{\kappa (p_{k+1} - p_k)}{2 p_{k+1/2}}   ~.

If there are any unstable layers in the top three model layers, the
temperature is adjusted so that ([4.j.2]) is satisfied everywhere in the
column. The variable :math:`\delta` represents a convergence criterion.
The adjustment is done so that sensible heat is conserved,

.. math::
   :label:

   c_p(\hat{T}_k \Delta p_k + \hat{T}_{k+1} \Delta p_{k+1}) = c_p (T_k
   \Delta p_k + T_{k+1} \Delta p_{k+1}) , 

and so that the layer has neutral stability:

.. math::
   :label:

   \hat{T}_{k+1} - \hat{T}_k = C1_{k+1} (\hat{T}_{k+1} + \hat{T}_k)\, .
   

As mentioned above, the hats denote the variables after adjustment.
Thus, the adjusted temperatures are given by

.. math::
   :label:

   \hat{T}_{k+1} & = \frac{\Delta p_k}{\Delta p_{k+1} + \Delta p_k
   C2_{k+1}} T_k + \frac{\Delta p_{k+1}}{\Delta p_{k+1} + \Delta p_k
   C2_{k+1}} T_{k+1},  \\[-1.0em]
   \intertext{and}\nonumber\\[-2.0em] \hat{T}_k & = C2_{k+1} \hat{T}_{k+1}
   , \\[-1.0em] \intertext{where}\nonumber\\[-2.0em]
   C2_{k+1} & = \frac{1 - C1_{k+1}}{1 + C1_{k+1}}
   
   ~.

Whenever the two layers undergo dry adjustment, the moisture is assumed
to be completely mixed by the process as well. Thus, the specific
humidity is changed in the two layers in a conserving manner to be the
average value of the original values,

.. math::
   :label:

   \hat{q}_{k+1} = \hat{q}_k = (q_{k+1} \Delta p_{k+1} + q_k \Delta
   p_k)/(\Delta p_{k+1} + \Delta p_k) . 

The layers are adjusted iteratively. Initially, :math:`\delta = 0.01` in
the stability check ([4.j.2]). The column is passed through from
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

Parameterization of Cloud Fraction
----------------------------------

Cloud amount (or cloud fraction), and the associated optical properties,
are evaluated via a diagnostic method in . The basic approach is similar
to that employed in CAM3. The diagnosis of cloud fraction is a
generalization of the scheme introduced by , with variations described
in , and . Cloud fraction depends on relative humidity, atmospheric
stability, water vapor and convective mass fluxes. Three types of cloud
are diagnosed by the scheme: low-level marine stratus
(:math:`{{\cal C}}_{st}`), convective cloud (:math:`{{\cal C}}_{cir}`),
and layered cloud (:math:`{{\cal C}}_c`). Layered clouds form when the
relative humidity exceeds a threshold value which varies according to
pressure. The diagnoses of these cloud types are described in more
detail in the following paragraphs.

Marine stratocumulus clouds are diagnosed using an empirical
relationship between marine stratocumulus cloud fraction and the
stratification between the surface and 700mb derived by . The CCM3
parameterization for stratus cloud fraction over oceans has been
replaced with

.. math::
   :label:

   {{\cal C}}_{st} = \min\biggl\lbrace 1., \max\bigl[0.,
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
suggested by :

.. math:: {{\cal C}}_{shallow} = k_{1,shallow} ln(1.0+k_2 M_{c,shallow},0.3 )

.. math:: {{\cal C}}_{deep}     = k_{1_deep} ln(1.0+k_2 M_{c,deep},0.6 )

where :math:`k_{1,shallow}` and :math:`k_{1_deep}` are adjustable
parameters given in Appendix [adjustableparameters], :math:`k_2 = 500`,
and :math:`M_c` is the convective mass flux at the given model level.
The combined convective cloud fraction :math:`C_{cir}`, is further
approximated as

.. math:: {{\cal C}}_{cir} ={\rm min} (0.8, {{\cal C}}_{shallow} + {{\cal C}}_{deep} ).

The remaining cloud types are diagnosed on the basis of relative
humidity, according to

.. math::
   :label:

   {{\cal C}}_c = ( \frac{RH - RH_{\min}} {1 - RH_{\min}} )^{2}
   

The threshold relative humidity :math:`RH_{\min}` is set according to
pressure :math:`p` as

.. math::
   :label:

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
surface properties and subgrid orographic effects. In a modification is
made to the layered cloud fraction to prevent extensive cloud decks that
have zero or near-zero condensate in cold climates. The adjustment is
based on and reduces the diagnosed low cloud fraction if grid mean water
vapor is less than 3 g/kg according to

.. math:: C_c^{low} = C_c^{low}max(0.15,min(1,{{\cal C}}{q_{v}}{0.003}))

This modifiation has a significant impact duting winter time in high
latitude regions.

The total cloud :math:`{{\cal C}}_{tot}` within each volume is then
diagnosed as

.. math::
   :label:

   {{\cal C}}_{tot} = {\rm min} ( {\rm max}( {{\cal C}}_{c},{{\cal C}}_{st})
                                  + {{\cal C}}_{cir},  1 ) .

This is equivalent to a maximum overlap assumption of cloud types within
each gridbox. The condensate value is assumed uniform within any and all
types of cloud within each grid box. In order to prevent inconsistent
values of total cloud fraction and condensate being passed to the
radiation parameterization in the a second updated cloud fraction
calculation is performed. Cloud fraction and therefore relative humidity
are now consitent with condensate values on entry to the radiation
parameterization. This vastly reduces the frequency of ’empty clouds’
seen in the CAM3, where cloud condesate was zero and yet cloud had been
diagnosed to exists due to an inconsistant relative humidity.

Parameterization of Shortwave Radiation
---------------------------------------

Diurnal cycle
~~~~~~~~~~~~~

With standard name-list settings, both the longwave and shortwave
heating rates are evaluated every model hour. Between hourly
evaluations, the longwave and shortwave fluxes and flux divergences are
held constant.

In , insolation is computed using the method of . Using this
formulation, the insolation can be determined for any time within
:math:`10^6` years of 1950 AD. This facilitates using for paleoclimate
simulations. The insolation at the top of the model atmosphere is given
by

.. math:: 
   :label:

   S_I = {S_0\,{\rho^{-2}}\,\cos\mu} , 

where :math:`S_0` is the solar constant, :math:`\mu` is the solar zenith
angle, and :math:`\rho^{-2}` is the distance factor (square of the ratio
of mean to actual distance that depends on the time of year). In the
standard configuration, :math:`S_0 = 1367.0` W/m:math:`{}^2`.  includes
a mechanism for treating the slow variations in the solar constant over
the 11-year cycle and during longer secular trends. A time series of
:math:`S_0` for 1870-2100 based upon is included with the standard
model.

We represent the annual and diurnal cycle of solar insolation with a
repeatable solar year of exactly 365 days and with a mean solar day of
exactly 24 hours, respectively. The repeatable solar year does not allow
for leap years. The expressions defining the annual and diurnal
variation of solar insolation are:

.. math::
   :label:

   \cos\mu & = \sin\phi \sin\delta - \cos\phi \cos\delta \cos(H) \\
   \delta & = \arcsin(\sin\epsilon\sin\lambda) \\ \rho & =
   \frac{1-e^2}{1+e\,\cos(\lambda - {\tilde\omega})} \\ {\tilde\omega}& = \Pi + \psi
   \\[-1.0em] \intertext{where}\nonumber\\[-2.0em] \phi & = {\rm
   latitude~in~radians} \nonumber \nonumber \\ \delta & = {\rm
   solar~declination~in~radians} \nonumber \\ H & = {\rm
   hour~angle~of~sun~during~the~day} \nonumber \\ \epsilon & = {\rm
   obliquity} \nonumber \\
   \lambda & = {\rm true~longitude~of~the~earth~relative~to~vernal~equinox} \\
   e & = {\rm eccentricity~factor} \nonumber \\ {\tilde\omega}& = {\rm
   longitude~of~the~perihelion}+ 180^\circ \nonumber \\ \Pi & = {\rm
   longitude~of~perihelion~based~on~the~fixed~equinox} \nonumber \\ \psi
   & = {\rm general~precession} \nonumber
   ~.

Note that :math:`\Pi` is denoted by :math:`\pi` in .

The hour angle :math:`H` in the expression for :math:`\cos\mu` depends
on the calendar day :math:`d` as well as model longitude:

.. math:: H = 2\,\pi(d + \frac{\theta}{360^\circ}) , 

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
   :label:

   \epsilon = \epsilon^* + \sum_{j=1}^{47} A_j\,\cos(f_j\,t +
                  \delta_j) \\

where :math:`A_j`, :math:`f_j`, and :math:`\delta_j` are determined by
numerical fitting. The term :math:`\epsilon^* = 23.320556^\circ`, and
:math:`t` is the time (in years) relative to 1950 AD.

Since the series expansion for the eccentricity :math:`e` is slowly
convergent, it is computed using

.. math:: 
   :label:

   e = \sqrt{(e\cos\Pi)^2+(e\sin\Pi)^2}

The terms on the right-hand side may also be written as empirical series
expansions:

.. math::
   :label:

   e{\lbrace\begin{array}{c}\cos\\
   \sin\end{array}\rbrace}\Pi = \sum_{j=1}^{19} M_j\,{\lbrace\begin{array}{c}\cos\\
   \sin\end{array}\rbrace}(g_j\,t+\beta_j)

where :math:`M_j`, :math:`g_j`, and :math:`\beta_j` are estimated from
numerical fitting. Once these series have been computed, the longitude
of perihelion :math:`\Pi` is calculated using

.. math:: 
   :label:

   \Pi = \arctan(\frac{e\,\sin\Pi}{e\,\cos\Pi})

The general precession is given by another empirical series expansion

.. math::
   :label:

   \psi = \tilde\psi\,t + \zeta + \sum_{j=1}^{78} F_j\,\sin(f'_j\,t
          + \delta'_j)

where :math:`\tilde\psi = 50.439273''`, :math:`\zeta = 3.392506^\circ`,
and :math:`F_j`, :math:`f'_j`, and :math:`\delta'_j` are estimated from
the numerical solution for the Earth’s orbit.

The calculation of :math:`\lambda` requires first determining two mean
longitudes for the orbit. The mean longitude :math:`\lambda_{m0}` at the
time of the vernal equinox is :

.. math::
   :label:

   \lambda_{m0} & = 
      2\lbrace (\frac{e}{2} + \frac{e^3}{8})
                          (1+\beta)\sin({\tilde\omega}) .\nonumber \\
       & \phantom{-2\lbrace.}
        -\frac{e^2}{4}\,(\frac{1}{2}+\beta)\,\sin(2\,{\tilde\omega})
      \\
       & \phantom{-2\lbrace.}
         +.\frac{e^3}{8}\,(\frac{1}{3}+\beta)\,
          \sin(3\,{\tilde\omega}) \rbrace \nonumber

where :math:`\beta = \sqrt{1-e^2}`. The mean longitude is

.. math:: 
   :label:

   \lambda_m = \lambda_{m0} + \frac{2\,\pi\,(d-d_{ve})}{365}

where :math:`d_{ve}=80.5` is the calendar day for the vernal equinox at
noon on March 21. The true longitude :math:`\lambda` is then given by:

.. math::
   :label:

   \lambda = \lambda_m 
   & + (2\,e - \frac{e^3}{4})\sin(\lambda_m-{\tilde\omega}) \nonumber \\ 
   & + \frac{5\,e^2}{4}\,\sin[2(\lambda_m-{\tilde\omega})] \\ 
   & + \frac{13\,e^3}{12}\sin[3(\lambda_m-{\tilde\omega})] \nonumber

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
:math:`e = 0.016715`, and :math:`{\tilde\omega}- 180 = 102.7`.

Formulation of shortwave solution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :math:`\delta`-Eddington approximation of and has been adopted and
is described in . This approximation has been shown to simulate quite
well the effects of multiple scattering. The major differences between
the shortwave parameterizations in CCM3 and are

#. the new treatment of cloud vertical overlap ;

#. updated parameterization for near-infrared absorption by water vapor;
   and

#. inclusion of prescribed aerosol data sets for computing shortwave
   aerosol radiative forcing.

The solar spectrum is divided into 19 discrete spectral and
pseudo-spectral intervals (7 for :math:`\mathrm{O_{3}}`, 1 for the
visible, 7 for :math:`\mathrm{H_{2}O}`, 3 for :math:`\mathrm{CO_{2}}`,
and 1 for the near-infrared following ). The model atmosphere consists
of a discrete vertical set of horizontally homogeneous layers within
which radiative heating rates are to be specified (see
Figure [figure:1]). Each of these layers is considered to be a
homogeneous combination of several radiatively active constituents.
Solar irradiance, surface reflectivity for direct and diffuse radiation
in each spectral interval, and the cosine of the solar zenith angle are
specified. The surface albedo is specified in two wavebands
(0.2-0.7 :math:`\mu`\ m, and 0.7-5.0 \ :math:`\mu`\ m) and distinguishes
albedos for direct and diffuse incident radiation. Albedos for ocean
surfaces, geographically varying land surfaces, and sea ice surfaces are
distinguished.

The method involves evaluating the :math:`\delta`-Eddington solution for
the reflectivity and transmissivity for each layer in the vertical under
clear and overcast conditions. The layers are then combined together,
accounting for multiple scattering between layers, which allows
evaluation of upward and downward spectral fluxes at each interface
boundary between layers. This procedure is repeated for each spectral or
pseudo-spectral interval and binary cloud configuration (see “Cloud
vertical overlap” below) to accumulate broad band fluxes, from which the
heating rate can be evaluated from flux differences across each layer.
The :math:`\delta`-Eddington scheme is implemented so that the solar
radiation is evaluated once every model hour (in the standard
configuration) over the sunlit portions of the model earth.

The :math:`\delta`-Eddington approximation allows for gaseous absorption
by :math:`\mathrm{O_{3}}`, :math:`\mathrm{CO_{2}}`,
:math:`\mathrm{O_{2}}`, and :math:`\mathrm{H_{2}O}`. Molecular
scattering and scattering/absorption by cloud droplets and aerosols are
included. With the exception of :math:`\mathrm{H_{2}O}`, a summary of
the spectral intervals and the absorption/scattering data used in the
formulation are given in and . Diagnostic cloud amount is evaluated
every model hour just prior to the solar radiation calculation.

The absorption by water vapor of sunlight between 1000 and 18000
cm\ :math:`{}^{-1}` is treated using seven pseudo-spectral intervals. A
constant specific extinction is specified for each interval. These
extinctions have been adjusted to minimize errors in heating rates and
flux divergences relative to line-by-line (LBL) calculations for
reference atmospheres using GENLN3 combined with the radiative transfer
solver DISORT2 . The coefficients and weights have the same properties
as a k-distribution method , but this parameterization is essentially an
exponential sum fit (e.g., ). LBL calculations are performed with the
HITRAN2k line database and the Clough, Kneizys, and Davies (CKD) model
version 2.4.1 . The Rayleigh scattering optical depths in the seven
pseudo-spectral intervals have been changed for consistency with LBL
calculations of the variation of water-vapor absorption with wavelength.
The updated parameterization increases the absorption of solar radiation
by water vapor relative to the treatment used in CCM and CAM since its
introduction by .

For some diagnostic purposes, such as estimating cloud radiative forcing
a clear-sky absorbed solar flux is required. In , the clear-sky fluxes
and heating rates are computed using the same vertical grid as the
all-sky fluxes. This replaces the 2-layer diagnostic grid used in CCM3.

Aerosol properties and optics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Introduction
^^^^^^^^^^^^

The treatment of aerosols in replaces the uniform background
boundary-layer aerosol used in previous versions of CAM and CCM. The
optics for the globally uniform aerosol were identical to the sulfate
aerosols described by . In the visible, the uniform aerosol was
essentially a conservative scatterer. The new treatment introduces five
chemical species of aerosol, including sea salt, soil dust, black and
organic carbonaceous aerosols, sulfate, and volcanic sulfuric acid. The
new aerosols include two species, the soil dust and carbonaceous types,
which are strongly absorbing in visible wavelengths and hence increase
the shortwave diabatic heating of the atmosphere.

The three-dimensional time-dependent distributions of the five aerosol
species and the optics for each species are loaded into during the
initialization process. This provides considerable flexibility to:

-  Change the speciated aerosol climatology / time-series as aerosol
   modeling improves;

-  Vary the aerosol distributions for climates different from
   present-day conditions;

-  Examine the effects of individual aerosol species and arbitrary
   combinations of aerosol species; and

-  Change aerosol optical properties.

In its present configuration, CAM includes the direct and semi-direct
effects of tropospheric aerosols on shortwave fluxes and heating rates.
The first indirect effect, or effect, is not included in the standard
version of .

Description of aerosol climatologies and data sets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The data sets for the tropospheric and stratospheric aerosols are
treated separately in the model.

The annually-cyclic tropospheric aerosol climatology consists of
three-dimensional, monthly-mean distributions of aerosol mass for:

-  sulfate from natural and anthropogenic sources;

-  sea salt;

-  black and organic carbon derived from natural and anthropogenic
   sources; and

-  soil dust

There are four size categories of dust spanning diameters from 0.01 to
10 \ :math:`\mu`\ m, and the black and organic carbon are represented by
two tracers each for the hydrophobic (new) and hydrophilic (aged)
components. The climatology therefore contains ten types of aerosol: sea
salt, four size bins of soil dust, sulfate, new and aged black carbon,
and hydrophobic and hydrophilic organic carbon.

The climatology is produced using an aerosol assimilation system
integrated for present-day conditions. The system consists of the Model
for Atmospheric Chemistry and Transport (MATCH) and an assimilation of
satellite retrievals of aerosol optical depth. MATCH version 4 is
integrated using the National Centers for Environmental Prediction
(NCEP) meteorological reanalysis at T63 triangular truncation . The
satellite estimates of aerosol optical depth are from the NOAA
Pathfinder II data set .

The formulation of the sulfur cycle is described in and . The emissions
inventory for SO\ :math:`{}_2` is from . The sources for mineral dust
are based upon the approach of and . The emissions of carbonaceous
aerosols include contributions from biomass burning , fossil fuel
burning , and a source of natural organic aerosols resulting from
terpene emissions. The vertical profiles of sea salt are computed from
the 10m wind speed .

The monthly-mean mass path for each aerosol species in each layer is
computed in units of kg/m\ :math:`{}^2`. During the initialization of ,
the climatology is temporally interpolated from monthly-mean to
mid-month values. At each time step, the mid-month values bounding the
current time step are vertically interpolated onto the pressure grid of
and then time interpolated to the current time step. The interpolation
scheme in preserves the aerosol masses for each species to 1 part in
10\ :math:`{}^7` relative to the climatology, and it is guaranteed to
yield positive definite mass-mixing ratios for all aerosols.

The stratospheric volcanic aerosols are treated using a single species
in the standard model. Zonal variations in the stratospheric mass
loading are omitted. The volcanic input consists of the monthly-mean
masses in units of kg/m\ :math:`{}^2` on an arbitrary meridional and
vertical grid. The time series for the recent past is based upon
following .

Calculation of aerosol optical properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The three intrinsic optical properties stored for each of the eleven
aerosol types are specific extinction, single scattering albedo, and
asymmetry parameter. These properties are computed on the band structure
of using Chandrasekhar weighting with spectral solar insolation. The
aerosol types affected by hygroscopic growth are sulfate, sea salt, and
hydrophilic organic carbon. In previous versions of CCM and , the
relative humidity was held constant in calculations of hygroscopic
growth at 80%. In , the actual profiles of relative humidity computed
from the model state each radiation time step are used in the
calculation.

The optics for black and organic carbon are identical to the optics for
soot and water-soluble aerosols in the Optical Properties of Aerosols
and Clouds (OPAC) data set . The optics for dust are derived from Mie
calculations for the size distribution represented by each size bin .
The Mie calculations for sulfate assume that it is comprised of ammonium
sulfate with a log-normal size distribution. The dry size parameters are
a median radius of 0.05 \ :math:`\mu`\ m and a geometric standard
deviation of 2.0. The optical properties in the seven H\ :math:`{}_2`\ O
pseudo-spectral intervals are averaged consistently with LBL
calculations of the variation of water-vapor absorption with wavelength.
This averaging technique preserves the cross correlations among the
spectral variation of solar insolation, water vapor absorption, and the
aerosol optical properties. The volcanic stratospheric aerosols are
assumed to be comprised of 75% sulfuric acid and 25% water. The
log-normal size distribution has an effective radius of
0.426 \ :math:`\mu`\ m and a standard deviation of 1.25.

The bulk formulae of are used to combine the optical properties of the
individual aerosol species into a single set of bulk aerosol
extinctions, single-scattering albedos, and asymmetry parameters for
each layer.

Calculation of aerosol shortwave effects and radiative forcing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

includes a mechanism to scale the masses of each aerosol species by
user-selectable factors at runtime. These factors are global,
time-independent constants. This provides the flexibility to consider
the climate effects of an arbitrary combination of the aerosol species
in the climatology. It also facilitates simulation of climates different
from present-day conditions for which the only information available is
the ratio of globally averaged aerosol emissions or atmospheric
loadings. A mechanism to scale the carbonaceous aerosols with a
time-dependent unitless factor has been included to facilitate realistic
simulations of the recent past.

also includes a run-time option for computing a diagnostic set of
shortwave fluxes with an arbitrary combination of aerosols multiplied
with a separate set of user-selectable scale factors. This option can be
used to compute, for example, the aerosol radiative forcing relative to
an atmosphere containing no aerosols.

The diagnostic fields produced the aerosol calculation include the
column-integrated optical depth and column-averaged single-scattering
albedo, asymmetry parameter, and forward scattering parameter (in the
:math:`\delta`-Eddington approximation) for each aerosol species and
spectral interval. These fields are only computed for illuminated grid
points, and for non-illuminated points the fields are set to zero. The
fraction of the time that a given grid point is illuminated is also
recorded. Time averages of, for example, the optical depth can be
obtained by dividing the time-averaged optical depths in the history
files by the corresponding daylit fractions.

Globally uniform background sulfate aerosol
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The option of introducing a globally uniform background sulfate aerosol
is retained, although by default the optical depth of this aerosol is
set to zero. Its optical properties are computed using the same sulfate
optics as are used for the aerosol climatology. However, for consistency
with the uniform aerosol in previous versions of and CCM3, the relative
humidity used to compute hygroscopic growth is set to 80%.

Cloud Optical Properties
~~~~~~~~~~~~~~~~~~~~~~~~

Parameterization of effective radius
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Observational studies have shown a distinct difference between maritime,
polar, and continental effective cloud drop size, :math:`r_e`, for warm
clouds. For this reason, differentiates between the cloud drop effective
radius for clouds diagnosed over maritime and continental regimes , and
over pristine surfaces (sea ice, snow covered land). Over the ocean, the
cloud drop effective radius for liquid water clouds, :math:`r_{el}`, is
specified to be 14\ :math:`\mu`\ m. Over sea ice, where we presume
pristine conditions, :math:`r_{el}` is also specified to be
14\ :math:`\mu`\ m. Over land masses :math:`r_{el}` is determined using

.. math::

   r_{el} =
   \begin{cases}
   8 \; \mu{\rm m} & -10^\circ C < T \\
   8 - 6( ( \frac{10^\circ + T}{20^\circ} )\; \mu{\rm m} & -30^\circ C \le
   T \le -10^\circ C\\
   14 \; \mu{\rm m}  & -30^\circ C > T
   \end{cases}
   

This does not necessarily correspond to the range over which the cloud
ice fraction increases from 0 to 1. In addition, :math:`r_{el}` ramps
linearly toward the pristine value of 14\ :math:`\mu`\ m as water
equivalent snow depth over land goes from 0 to 0.1 m.

An ice particle effective radius, :math:`r_{ei}`, is also diagnosed by .
Following , the effective radius for ice clouds is now a function only
of temperature, as shown in Figure [figure:rei].

.. figure:: figures/ice
   :alt: [figure:rei]Ice effective radius and terminal velocity. Top,

   ice effective radius versus temperature. Bottom, ice velocity versus
   radius (left) and temperature (right); the Stokes terminal velocity
   is solid and the actual velocity is dashed.

   [figure:rei]Ice effective radius and terminal velocity. Top, ice
   effective radius versus temperature. Bottom, ice velocity versus
   radius (left) and temperature (right); the Stokes terminal velocity
   is solid and the actual velocity is dashed.

Dependencies involving effective radius
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For cloud scattering and absorption, the radiative parameterization of
for liquid water droplet clouds is employed. In this parameterization,
the optical properties of the cloud droplets are represented in terms of
the prognosed cloud water path (CWP, in units of kg m\ :math:`^{-2}`)
and effective radius :math:`r_e = \int r^3 n (r) dr / \int
r^2 n (r) dr`, where :math:`n(r)` is the cloud drop size distribution as
a function of radius :math:`r`.

Cloud radiative properties explicitly account for the phase of water.
For shortwave radiation we use the following generalization of the
expression used by for liquid water clouds. The cloud liquid optical
properties (extinction optical depth, single scattering albedo,
asymmetry parameter and forward scattering parameter) for each spectral
interval are defined as

.. math::

   \tau _l^c& =CWP[ a_l^{i}+\frac{b_l^i}{r_{el}} ] (
   1-f_{ice} )
    \\
   \omega _l^c& =1-c_l^i-d_l^ir_{el}
    \\
   g_l^c& =e_l^i+f_l^ir_{el}
    \\
   f_l^c& =( {g_l^c} )^2
   

where superscript :math:`i` denotes spectral interval. The spectral
intervals and coefficients for liquid water are defined in .

The radiative properties of ice cloud are defined by

.. math::

   \tau_i^c& =CWP[ a_i^i+ \frac{b_i^i}{r_{ei}} ] f_{ice}
    \\
   \omega _i^c& =1-c_i^i-d_i^ir_{ei}
    \\
   g_i^c& =e_i^i+f_i^ir_{ei}
    \\
   f_i^c& =( {g_i^c} )^2
   

where the subscript :math:`i` denotes ice radiative properties. The
values for the coefficients :math:`a_i-f_i` are based on the results of
for the four pseudo-spectral intervals (.25-.69 :math:`\mu`\ m,
.69-1.19 \ :math:`\mu`\ m, 1.19-2.38 \ :math:`\mu`\ m, and
2.38-4.00 \ :math:`\mu`\ m) employed in the shortwave radiation model.
Note that when :math:`0<f_{ice}<1`, then the combination of these
expressions in ([4.b.11] - [4.b.14]) represent the radiative properties
for a mixed phase cloud.

Cloud vertical overlap
~~~~~~~~~~~~~~~~~~~~~~

The treatment of cloud vertical overlap follows . The overlap
parameterization is designed to reproduce calculations based upon the
independent column approximation (ICA). The differences between the
results from the new parameterization and ICA are governed by a set of
parameters in the shortwave code (Table [table:swparams] on page and
section [ssec:methodbinary]). The differences can be made arbitrarily
small with appropriate settings of these parameters. The current
parameter settings represent a compromise between computational cost and
accuracy.

The new parameterizations can treat random, maximum, or an arbitrary
combination of maximum and random overlap between clouds. The type of
overlap is specified with the same two variables for the longwave and
shortwave calculations. These variables are the number of random-overlap
interfaces between adjacent groups of maximally-overlapped layers and a
vector of the pressures at each of the interfaces. The specification of
the overlap is completely separated from the radiative calculations, and
if necessary the type of overlap can change at each grid cell or time
step.

Conversion of cloud amounts to binary cloud profiles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The algorithm for cloud overlap first converts the vertical profile of
partial cloudiness into an equivalent collection of binary cloud
configurations. Let :math:`{{\cal C}}(i)` be the fractional amount of
cloud in layer :math:`i` in a profile with :math:`K` layers. The index
:math:`i = 1` corresponds to the top of the model atmosphere and
:math:`i = K` corresponds to the layer adjacent to the surface. Let
:math:`N_m` be the number of maximally-overlapped regions in the column
separated by random-overlap boundaries. If the entire column is
maximally overlapped, then :math:`N_m =
1`, and if the entire column is randomly overlapped, then
:math:`N_m = K`. Each region :math:`j` includes all layers :math:`i`
between :math:`{{i_{{j},\min}}}` and :math:`{{i_{{j},\max}}}`. Within
each region, identify the :math:`n_j` unique, non-zero cloud amounts and
sort them into a descending list :math:`{{{{\cal C}}_{{j},{k_{j}}{}}}}`
with :math:`1 \le k_j \le n_j`. Note than in , cloud amounts are not
allowed to be identically equal to 1. It is convenient to define
:math:`{{\cal C}}_{j,0} = 1` and :math:`{{\cal C}}_{j,{n_j+1}} = 0`. By
construction
:math:`{{{{\cal C}}_{{j},{k_{j}}{-1}}}}> {{{{\cal C}}_{{j},{k_{j}}{}}}}`
for :math:`1 \le k_j
\le {n_j+1}`.

The binary cloud configurations are defined in terms of the sorted cloud
amounts. The number of unique cloud binary configurations in region
:math:`j` is :math:`{n_j+1}`. The :math:`k_j^{\hbox{th}}` binary cloud
configuration :math:`{{\tilde{{{\cal C}}}_{{j},k_{j}}}}` in region
:math:`j` is given by

.. math::

   {{\tilde{{{\cal C}}}_{{j},k_{j}}}}(i) = \{ \begin{array}{ll}
                                 1 & \mbox{if ${{i_{{j},\min}}}\le i \le {{i_{{j},\max}}}$
                                           and ${{\cal C}}(i) \ge {{{{\cal C}}_{{j},{k_{j}}{-1}}}}$} \\
                                 0 & \mbox{otherwise}
                                \end{array} .
       

with :math:`1 \le k_j \le {n_j+1}`. The fractional area of this
configuration is

.. math:: {{\tilde{A}_{{j},k_{j}}}}= {{{{\cal C}}_{{j},{k_{j}}{-1}}}}- {{{{\cal C}}_{{j},{k_{j}}{}}}}

The binary cloud configurations for each maximum-overlap region can be
combined into cloud configurations for the entire column. Because of the
random overlap boundaries between regions, the number of column
configurations is

.. math::

   N_c = \prod_{j' = 1}^{N_m} (n_{j'}+1)
       

Let :math:`{\tilde{{{\cal C}}}[{k_1,\ldots,k_{N_m}}]}` represent the
column configuration with :math:`\tilde{{{\cal C}}}_{1,k_1}` in region
1, :math:`\tilde{{{\cal C}}}_{2,k_2}` in region 2, etc. The vertical
profile of binary cloud elements is given by:

.. math::

   {\tilde{{{\cal C}}}[{k_1,\ldots,k_{N_m}}]}(i) = \sum_{j' = 1}^{N_m} {\tilde{{{\cal C}}}_{{j'},k_{j'}}}(i)
       

 The area of this configuration is

.. math::

   {\tilde{A}[{k_1,\ldots,k_{N_m}}]} = \prod_{j' = 1}^{N_m} {\tilde{A}_{{j'},k_{j'}}}
       

Maximum-random overlap assumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The cloud overlap for radiative calculations in is maximum-random (M/R).
Clouds in adjacent layers are maximally overlapped, and groups of clouds
separated by one or more clear layers are randomly overlapped. The two
overlap parameters input to the radiative calculations are the number of
random-overlap interfaces, which equals :math:`N_m`, and a vector of
pressures :math:`\vec p` at each random-overlap interface. These
parameters are determined for each grid cell at each radiation time
step. Suppose there are :math:`M \ge 0` groups of vertically contiguous
clouds in a given grid cell. The first parameter
:math:`N_m = \max(M,1)`. Let :math:`p_j` represent the pressure at the
bottom interface of each group of contiguous clouds, and let :math:`p_s`
denote the surface pressure. Both :math:`j` and :math:`p_j` increase
from the top of the model downward. Then

.. math::

   \vec p = \{\begin{array}{ll} [ p_s ] & \hbox{if $M \le
                  1$} \\ [ p_1, \>\ldots\>, p_{M-1}, p_s ] &
                  \hbox{if $M \ge 2$}
                  \end{array} .
      

Low, medium and high cloud overlap assumptions (diagnostics)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For diagnostic purposes, the calculates three levels of cloud fraction
assuming the same maximum-random overlap as in the radiative
calculations. These diagnostics, denoted as low, middle, and high cloud,
are bounded by the pressure levels :math:`p_s` to 700 mb, 700 mb to
400 mb, and 400 mb to the model top.

Computation of fluxes and heating rates with overlap
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The solution for the shortwave fluxes is calculated by determining all
possible arrangements of binary clouds which are consistent with the
vertical profile of partial cloudiness, the overlap assumption, and the
parameters for accelerating the solution (Table [table:swparams] and
section [ssec:methodbinary]). The shortwave radiation within each of
these configurations is calculated using the same
:math:`\delta`-Eddington solver introduced in CCM3 . The all-sky fluxes
and heating rates for the original profile of partial cloudiness are
calculated as weighted sums of the corresponding quantities from each
configuration. The weights are equal to the horizontal fractional area
occupied by each configuration. The number of configurations is given by
eqn. ([eqn:nconfig]), and the area of each configuration is given by
eqn. ([eqn:aconfig]). There are two steps in the calculations: first,
the calculation of the cloud-free and overcast radiative properties for
each layer, and second the combination of these properties using the
adding method to calculate fluxes. These two processes are described
below.

:math:`\delta`-Eddington solution for a single layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Details of the implementation are as follows. The model atmosphere is
divided into :math:`K+1` layers in the vertical; an extra top layer
(with index 0, above the :math:`K` layers specified by ) is added. This
extra layer prevents excessive heating in the top layer when the top
pressure is not very low; also, as the model does not specify absorber
properties above its top layer, the optical properties of the top layer
must be used for the extra layer. In , clear-sky and all-sky solar
fluxes are calculated and output for the top of model (TOM) at layer 1
and the top of atmosphere (TOA) corresponding to layer 0. The TOM fluxes
are used to compute the model energetic balance, and the TOA fluxes are
output for diagnostic comparison against satellite measurements. The
provision of both sets of fluxes is new in . Layers are assumed to be
horizontally and vertically homogeneous for each model grid point and
are bounded vertically by layer interfaces. For each spectral band,
upward and downward fluxes are computed on the layer interfaces (which
include the surface and top interface). The spectral fluxes are summed
and differenced across layers to evaluate the solar heating rate. The
following discussion refers to each of the spectral intervals.

In general, several constituents absorb and/or scatter in each
homogeneous layer (e.g. cloud, aerosol, gases...). Every constituent is
defined in terms of a layer extinction optical depth :math:`\tau`,
single scattering albedo :math:`\omega`, asymmetry parameter :math:`g`,
and the forward scattering fraction :math:`f`. To define bulk layer
properties, the combination formulas of are used:

.. math::

   \tau & = \sum_i \tau_{i} ,  \\[1ex] \omega & = {\sum_i
   \omega_{i} \tau_{i}}{\tau} , \\[1ex] g & = \frac{\sum_i
   g_{i} \omega_{i} \tau_{i}}{\omega\tau} , \\[1ex] f & =
   \frac{\sum_i f_{i} \omega_{i} \tau_{i}}{\omega \tau} , 

where the sums are over all constituents.

The :math:`\delta`-Eddington solution for each layer requires scaled
properties for :math:`\tau`, :math:`\omega`, :math:`g`, given by the
expressions:

.. math::

   \tau^\ast & = \tau (1-\omega f) ,  \\[1ex] \omega^\ast & =
   \omega (\frac{1 - f}{1 - \omega f}) , \\[1ex]
   g^\ast & = \frac{g - f}{1 - f} . 

The scaling accounts for the scattering effects of the strong forward
peak in particle scattering. The :math:`\delta`-Eddington
nonconservative (:math:`\omega<1`) solutions for each layer for direct
radiation at cosine zenith angle :math:`\mu_0` are (following the
notation of :

.. math::

     R(\mu_0) & = (\alpha - \gamma) {\overline T}e^{{-\tau^\ast/\mu_0}} +
              (\alpha + \gamma) {\overline R} - (\alpha-\gamma) ,
              \\
     T(\mu_0) & = (\alpha + \gamma) {\overline T} + (\alpha -
               \gamma){\overline R}e^{{-\tau^\ast/\mu_0}} - (\alpha +
               \gamma - 1) e^{{-\tau^\ast/\mu_0}} , \\
     {\overline R} & = (u+1)(u-1)(e^{\lambda\tau^\ast} -
     e^{-\lambda\tau^\ast})
   N^{-1} ,  \\ {\overline T} & = 4u N^{-1} , 
     \\[-1.0em]
   \intertext{where}\nonumber\\[-2.0em]
     \alpha & = \frac{3}{4} \omega^\ast \mu_0 (
                           \frac{1+g^\ast(1-\omega^\ast)} {1 -
                           \lambda^2\mu_0^2} ) ,  \\
   \gamma & = \frac{1}{2} \omega^\ast
                      (\frac{1+3g^\ast(1-\omega^\ast)\mu_0^2} {1 -
                      \lambda^2\mu_0^2} ) ,  \\
     N & = (u+1)^2 e^{\lambda\tau^\ast} - (u-1)^2 e^{-\lambda\tau^\ast} ,
    \\
     u & = \frac{3}{2} ({1-\omega^\ast g^\ast}{\lambda}),
    \\
     \lambda & = \sqrt{3(1-\omega^\ast)(1-\omega^\ast g^\ast)} ,
     

where :math:`R(\mu_0)`, :math:`T(\mu_0)` are the layer reflectivity and
transmissivity to direct radiation respectively, and
:math:`\overline R`, :math:`\overline T` are the layer reflectivity and
transmissivity to diffuse radiation respectively. It should be noted
that in some cases of small but nonzero :math:`\omega`, the diffuse
reflectivity can be negative. For these cases, :math:`\overline R` is
set to 0, which produces negligible impact on fluxes and the heating
rate. Note that in the new overlap scheme, these properties are computed
separately for the clear and cloud-filled portions of each layer .

Combination of layers
~~~~~~~~~~~~~~~~~~~~~

To combine layers, it is assumed that radiation, once scattered, is
diffuse and isotropic (including from the surface). For an arbitrary
layer 1 (or combination of layers with radiative properties
:math:`R_1(\mu_0)`,
:math:`T_1(\mu_0)`,\ :math:`\overline{R}_1`,\ :math:`\overline{T}_1`)
overlaying layer 2 (or combination of layers with radiative properties
:math:`R_2(\mu_0)`, :math:`T_2(\mu_0)`, and
:math:`\overline{R}_2,\overline{T}_2`), the combination formulas for
direct and diffuse radiation incident from above are:

.. math::

   R_{12}(\mu_0) & = R_1(\mu_0) + \frac{\overline{T}_1 \{ (T_1(\mu_0) -
   e^{-\tau_1^\ast /\mu_0}) \overline{R}_2 +
   e^{-\tau_1^\ast/\mu_0}R_2(\mu_0) \}} {1 - \overline{R}_1
   \overline{R}_2} ,  \\ T_{12}(\mu_0) & =
   e^{-\tau_1^\ast/\mu_0} T_2(\mu_0)
   + \frac{\overline{T}_2 \{ (T_1(\mu_0) - e^{-\tau_1^\ast/ \mu_0}) +
     e^{-\tau_1^\ast/\mu_0}R_2(\mu_0) \overline{R}_1 \}}{1 -
     \overline{R}_1 \overline{R}_2} ,  \\
   \overline{R}_{12} & = \overline{R}_1 + \frac{\overline{T}_1
   \overline{R}_2 \overline{T}_1} {1 - \overline{R}_1 \overline{R}_2} ,
    \\ \overline{T}_{12} & = \frac{\overline{T}_1
   \overline{T}_2} {1 - \overline{R}_1 \overline{R}_2} . 

Note that the transmissions for each layer
(:math:`T_1(\mu_0),T_2(\mu_0)`) and for the combined layers
:math:`(T_{12}(\mu_0))` are total transmissions, containing both direct
and diffuse transmission. Note also that the two layers (or combination
of layers), once combined, are no longer a homogeneous system.

To combine the layers over the entire column, two passes are made
through the layers, one starting from the top and proceeding downward,
the other starting from the surface and proceeding upward. The result is
that for every interface, the following combined reflectivities and
transmissivities are available:

.. math::

   e^{-\tau^\ast/\mu_0} = \; & \text{direct beam transmission from
   top-of-atmosphere to the} \\ & \text{interface ($\tau^\ast$ is the
   scaled optical depth from top-of-atmosphere} \\ & \text{to the
   interface),} \\ R_{up}(\mu_0) = \; & \text{reflectivity to direct
   solar radiation of entire atmosphere} \\ & \text{\emph{below} the
   interface,} \\ T_{dn}(\mu_0) = \; & \text{total transmission to direct
   solar radiation incident from above} \\ & \text{to entire atmosphere
   \emph{above} the interface,} \\ {\overline R}_{up} = \; &
   \text{reflectivity of atmosphere \emph{below} the interface to
   diffuse} \\ & \text{radiation from above,} \\ {\overline R}_{dn} = \;
   & \text{reflectivity of atmosphere \emph{above} the interface to
   diffuse} \\ & \text{radiation from below.}

With these quantities, the upward and downward fluxes at every interface
can be computed. For example, the upward flux would be the directly
transmitted flux (:math:`e^{-\tau\ast/\mu_0}`) times the reflection of
the entire column below the interface to direct radiation
(:math:`R_{up}(\mu_0)`), plus the diffusely transmitted radiation from
above that reaches the interface
(:math:`T_{dn}(\mu_0) - e^{-\tau\ast/\mu_0}`) times the reflectivity of
the entire atmosphere below the interface to diffuse radiation from
above (:math:`\overline{R}_{up}`), all times a factor that accounts for
multiple reflections at the interface. A similar derivation of the
downward flux is straightforward. The resulting expressions for the
upward and downward flux are:

.. math::

   F_{up}
   & = \frac{e^{-\tau^\ast/\mu_0} R_{up}(\mu_0) + (T_{dn}(\mu_0) -
               e^{-\tau^\ast/\mu_0})\overline{R}_{up}} {1 -
               \overline{R}_{dn}\overline{R}_{up}},  \\
   F_{dn} & = e^{-\tau^\ast/\mu_0}
   + \frac{(T_{dn}(\mu_0) - e^{-\tau^\ast/\mu_0}) +
                e^{-\tau^\ast/\mu_0}R_{up}(\mu_0)\overline{R}_{dn}} {1 -
                \overline{R}_{dn}\overline{R}_{up}}. 

Note that in the new overlap scheme, the calculation of the combined
reflectivities, transmissions, and fluxes at layer interfaces are
computed for each binary cloud configuration, subject to techniques for
significantly accelerating these calculations (below) .

Acceleration of the adding method in all-sky calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If two or more configurations of binary clouds are identical between TOA
and a particular interface, then :math:`{T_{dir}}= e^{-\tau^*/\mu_0}`,
:math:`{T_{dn}}`, and :math:`{\bar{R}_{dn}}` are also identical at that
interface. The adding method is applied once and the three radiative
quantities are copied to all the identical configurations. This process
is applied at each interface by constructing a binary tree of identical
cloud configurations starting at TOA down to the surface. A similar
method is used for :math:`{R_{up}}` and :math:`{\bar{R}_{up}}`, which
are calculated using the adding method starting the surface and
continuing up to a particular interface. The copying of identical
radiative properties reduces the number of calculations of
:math:`{T_{dir}}`, :math:`{T_{dn}}`, and :math:`{\bar{R}_{dn}}` by 62%
and the number of calculations of :math:`{R_{up}}` and
:math:`{\bar{R}_{up}}` by 21% in  with M/R overlap.

Methods for reducing the number of binary cloud configurations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The computational cost of the shortwave code has two components: a fixed
cost for computing the radiative properties of each layer under clear
and overcast conditions, and a variable cost for applying the adding
method for each column configuration
:math:`{\tilde{{{\cal C}}}[{k_1,\ldots,k_{N_m}}]}`. The variable
component can be reduced by omitting configurations which contribute
small terms in the shortwave fluxes. Several mechanisms for selecting
configurations for omission have been included in the parameterization.
The parameters that govern the selection process are described in
Table [table:swparams].

| \|lllr@.ll\| & Symbol &Definition & &
|  & :math:`{{{\cal C}}_{\min}}` & Minimum cloud area &

| 0 & &
| **cldeps** & :math:`{{{\cal C}}_{eps}}` & Minimum cloud area
  difference & 0 & &
| **areamin** & :math:`{\tilde{A}_{\min}}` & Minimum configuration area
  & 0 & 01 &
| **nconfgmax** & :math:`{N_{c,\max}}` & Maximum # of configurations &
  15 & &

Any combination of the selection conditions may be imposed. If the
parameter :math:`{{{\cal C}}_{\min}}> 0`, cloud layers with
:math:`{{\cal C}}(i) \le {{{\cal C}}_{\min}}` are identified as
cloud-free layers. The configurations including these clouds are
excluded from the flux calculations. If the parameter
:math:`{{{\cal C}}_{eps}}> 0`, the cloud amounts are discretized by

.. math:: {{\cal C}}(i) arrow [{{{\cal C}}(i) \over {{{\cal C}}_{eps}}}] {{{\cal C}}_{eps}}

where :math:`[x]` represents rounding to the nearest integer less than
:math:`x`. This reduces the number of unique, non-zero cloud amounts
:math:`n_j` in each maximum-overlap region :math:`j`. For example, if
:math:`{{{\cal C}}_{eps}}= 0.01`, then two cloud amounts are
distinguished only if they differ by more than 0.01. If the parameter
:math:`{\tilde{A}_{\min}}> 0`, only configurations with
:math:`{\tilde{A}[{k_1,\ldots,k_{N_m}}]} \ge {\tilde{A}_{\min}}` are
retained in the calculation. The fluxes and heating rates are normalized
by the area of these configurations:

.. math::

   {\tilde{A}_{tot}}= {\sum_{k_1 = 1}^{n_1 + 1} \cdots \sum_{k_{N_m} =
                        1}^{n_{N_m} + 1} {\tilde{A}[{k_1,\ldots,k_{N_m}}]}} \;\;\theta({\tilde{A}[{k_1,\ldots,k_{N_m}}]} - {\tilde{A}_{\min}})
       

where :math:`\theta` is the Heaviside function. In ,
:math:`{\tilde{A}_{\min}}= 0.01`. Finally, if the number of
configurations :math:`N_c > {N_{c,\max}}`, then only the
:math:`{N_{c,\max}}` configurations with the largest values of
:math:`{\tilde{A}[{k_1,\ldots,k_{N_m}}]}` are retained. This is
equivalent to setting :math:`{\tilde{A}_{\min}}` so that the largest
:math:`{N_{c,\max}}` configurations are selected. The fluxes and heating
rates are normalized by :math:`{\tilde{A}_{tot}}` calculated with this
value of :math:`{\tilde{A}_{\min}}`. With the current cloud
parameterizations in and with :math:`{\tilde{A}_{\min}}= 0.01`, the mean
and RMS :math:`N_c` are approximately 5. :math:`{N_{c,\max}}` is set to
15, or 2 standard deviations above the mean :math:`N_c`. Only 5% of
cloud configurations in  have :math:`N_c \ge {N_{c,\max}}`. The errors
of the solutions relative to ICA are relatively insensitive to
:math:`{\tilde{A}_{tot}}` .

Computation of shortwave fluxes and heating rates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The upward and downward spectral fluxes at each interface are summed to
evaluate the spectrally integrated fluxes, then differenced to produce
the solar heating rate,

.. math::

   Q_{\rm sol} = \frac{g}{c_p} \frac{F_{dn}(p_{k+1}) - F_{up} (p_{k+1}) -
   F_{dn}(p_k) + F_{up}(p_k)} {p_{k+1} - p_k} 

which is added to the nonlinear term :math:`(Q)` in the thermodynamic
equation.

Parameterization of Longwave Radiation
--------------------------------------

The method employed in the to represent longwave radiative transfer is
based on an absorptivity/emissivity formulation

.. math::

   F^\downarrow (p)& =B(p_t)\varepsilon (p_t,p)+ \int\limits_{p_t}^p {\alpha
   (p,p')dB(p')}  \\ F^\uparrow
   (p)& =B(p_s)-\int\limits_p^{p_s} {\alpha (p,p')dB(p')}
   
   ~,

where :math:`B(p)=\sigma T(p)^4` is the Stefan-Boltzmann relation. The
pressures :math:`p_t` and :math:`p_s` refer to the top of the model and
the surface, respectively. :math:`\alpha` and :math:`\epsilon` are the
absorptivity and emissivity

.. math::

   \alpha (p,p')& =\frac{\int\limits_0^\infty { \{ dB_\nu (p')
   /dT(p') \} ( 1-{\cal T}_\nu (p,p')) \; d\nu}}{dB(p)/dT(p)}
    \\
   \varepsilon (p_t,p )& =\frac{\int\limits_0^\infty {B_\nu (p_t) ( 1-{\cal T}_\nu (p_t,p)) \; d\nu}}{B(p_t)}
   
   ,

where the integration is over wavenumber :math:`\nu`.
:math:`B_\nu(p) = B_\nu(T(p))` is the Planck function, and
:math:`{\cal T}_\nu` is the atmospheric transmission. Thus, to solve
for fluxes at each model layer we need solutions to the following:

.. math::

   \int\limits_0^\infty {( {1-{\cal T}_\nu } )}F(B_\nu )d\nu
   
   ,

where :math:`F(B_\nu )` is the Planck function for the emissivity, or
the derivative of the Planck function with respect to temperature for
the absorptivity.

The general method employed for the solution of ([4.b.38]) for a given
gas is based on the broad band model approach described by and . This
approach is based on the earlier work of . The broad band approach
assumes that the spectral range of absorption by a gas is limited to a
relatively small range in wavenumber :math:`\nu`, and hence can be
evaluated at the band center, i.e.

.. math::

   \int_{\nu_1}^{\nu_2} {(1-{\cal T}_\nu )F( {B_\nu } )d\nu
   \approx F( {B_{\bar \nu }} )\int_{\nu_1}^{\nu_2} {(1-{\cal
   T}_\nu )d\nu = F(B_{\bar\nu})A }}
   
   ,

where :math:`A` is the band absorptance (or equivalent width) in units
of cm\ :math:`^{- 1}`. Note that :math:`A`, in general, is a function of
the absorber amount, the local emitting temperature, and the pressure.
Thus, the broad band model is based on finding analytic expressions for
the band absorptance. proposed the following functional form for
:math:`A`:

.. math::

   A(u,T,P)=2A_{0} \ln \{ 1+\frac{u}{\sqrt {4+u(1+1/\beta)}}
   \}
   
   ,

where :math:`A_0` is an empirical constant. :math:`u` is the scaled
dimensionless path length

.. math::

   u=\int {\frac{S(T)}{A_0(T)}\mu\rho _adz}
   
   ,

where :math:`S(T)` is the band strength, :math:`\mu` is the mass mixing
ratio of the absorber, and :math:`\rho_a` is the density of air.
:math:`\beta` is a line width factor,

.. math::

   \beta = \frac{4}{ud}\int {\gamma (T)( \frac{P}{P_0} ) du}
   
   ,

where :math:`\gamma(T)` is the mean line halfwidth for the band,
:math:`P` is the atmospheric pressure, :math:`P_0` is a reference
pressure, and :math:`d` is the mean line spacing for the band. The
determination of :math:`\gamma`, :math:`d`, :math:`S` from spectroscopic
line databases, such as the FASCODE database, is described in detail in
. describe how ([4.b.40]) can be extended to account for sub-bands
within a spectral region. Essentially, the argument in the log function
is replaced by a summation over the sub-bands. This broad band formalism
is employed for CO\ :math:`_2`, O\ :math:`_3`, CH\ :math:`_4`,
N\ :math:`_2`\ O, and minor absorption bands of CO\ :math:`_2`, while
for the CFCs and stratospheric aerosols we employ the exponential
transmission approximation discussed by

.. math::

   T=\exp [ - D ( S(T) / \Delta\nu ) W ]
   
   ,

where :math:`\Delta\nu` is the band width, and :math:`W` is the
absorber path length

.. math::

   W=\int {\mu\rho _adz},
   

and :math:`D` is a diffusivity factor. The final problem that must be
incorporated into the broad band method is the overlap of one or more
absorbers within the same spectral region. Thus, for the wavenumber
range of interest, namely 500 to 1500 cm\ :math:`^{-1}`, the radiative
flux is determined in part by the integral

.. math::

   \int_{500}^{1500} { (1-{\cal T}_\nu)F(B_\nu)d\nu }
   
   ,

which can be re-formulated for given sub intervals in wavenumber as

.. math::

   \nonumber\int_{500}^{1500} { (1-{\cal T}_\nu)F(B_\nu) d\nu} =
   \int_{500}^{750} { (1-{\cal T}_{CO_2}^1{\cal T}_{N_2O}^1{\cal
   T}_{H_2O}{{\cal T}^{1}_{H_2SO_4}}) F(B_\nu) d\nu } \\[1ex] \nonumber+\int_{750}^{820} {
   (1-{\cal T}_{CFC11}^1{\cal T}_{H_2O}{{\cal T}^{*}_{H_2SO_4}})F(B_\nu) d\nu} \; \\[1ex] + \nonumber
   \int_{820}^{880} { (1-{\cal T}_{CFC11}^2{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}) F(B_\nu)
   d\nu}\\[1ex] \nonumber+ \int_{880}^{900} { (1-{\cal T}_{CFC12}^1{\cal
   T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}})F(B_\nu) d\nu} \; \\[1ex]\nonumber + \int_{900}^{1000} {(1-{\cal
   T}_{CO_2}^2{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}{\cal T}_{CFC11}^3 {\cal
   T}_{CFC12}^2)F(B_\nu)d\nu} \\[1ex] \nonumber+ \int_{1000}^{1120} {
   (1-{\cal T}_{CO_2}^3{\cal T}_{O_3}{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}} {\cal
   T}_{CFC11}^4{\cal T}_{CFC12}^3)F(B_\nu) d\nu} \\[1ex] + \nonumber
   \int_{1120}^{1170} { (1-{\cal T}_{CFC12}^4{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}{\cal
   T}_{N_2O}^2) F(B_\nu) d\nu} \; \\[1ex] +  \int_{1170}^{1500} { (1-{\cal
   T}_{CH_4}{\cal T}_{N_2O}^3{\cal T}_{H_2O}{{\cal T}^{5}_{H_2SO_4}}) F(B_\nu) d\nu}
   

The factors :math:`{{\cal T}^{i}_{H_2SO_4}}` represent the
transmissions through stratospheric volcanic aerosols. The transmissions
in each band are replaced by effective transmissions
:math:`{{\bar T}^{i}_{H_2SO_4}}` given by:

.. math:: {{\bar T}^{i}_{H_2SO_4}} = \exp(-D\,\kappa_{i,volc}\,W_{volc})

 where :math:`D = 1.66` is the diffusivity factor,
:math:`\kappa_{i,volc}` is an effective specific extinction for the
band, and :math:`W_{volc}` is the mass path of the volcanic aerosols.
For computing overlap with minor absorbers, methane, and carbon dioxide,
the volcanic extinctions are computed for five wavenumber intervals
given in table [table:volcext]. The transmissions for overlap with the
broadband absorption by water vapor are defined in
equation [eq:volcwater]. The volcanic transmission for the
798 cm\ :math:`{}^{-1}` band of N\ :math:`{}_2`\ O is

.. math:: {{\bar T}^{*}_{H_2SO_4}} = 0.7 {{\bar T}^{2}_{H_2SO_4}} + 0.3 {{\bar T}^{3}_{H_2SO_4}}

| \|cl\| Index & :math:`\nu_1-\nu_2`
| 1 & 500 - 650
| 2 & 650 - 800
| 3 & 800 - 1000
| 4 & 1000 - 1200
| 5 & 1200 - 2000

The sub-intervals in equation [4.b.46], in turn, can be reformulated in
terms of the absorptance for a given gas and the “overlap” transmission
factors that multiply this transmission. Note that in the broad band
formulation there is an explicit assumption that these two are
uncorrelated (see ). The specific parameterizations for each of these
sub-intervals depends on spectroscopic data particular to a given gas
and absorption band for that absorber.

Major absorbers
~~~~~~~~~~~~~~~

Details of the parameterization for the three major absorbers,
H\ :math:`_2`\ O, CO\ :math:`_2` and O\ :math:`_3`, are given in , , and
, respectively. Therefore, we only provide a brief description of how
these gases are treated in the . Note that the original parameterization
for H\ :math:`_2`\ O by has been replaced a new formulation in .

For CO\ :math:`_2`

.. math::

   \alpha_{CO_2}(p,p') = \frac{1}{4 \sigma T^3(p')} \frac{dB_{CO_2}}{dT'}
   (p') A_{CO_2} (p',p). 

:math:`B_{CO_2}` is evaluated for :math:`\tilde{\nu} = 667`
cm\ :math:`^{-1}`, where :math:`A_{CO_2} (p',p)` is the broad–band
absorptance from . Similarly,

.. math::

   \epsilon_{CO_2} (0,p) = \frac{1}{\sigma T^4(0)} B_{CO_2} (0) A_{CO_2}
   (0,p). 

 For ozone,

.. math::

   \alpha_{O_3}(p, p') & = \frac{1}{4 \sigma T^3(p')}
   \frac{dB_{O_3}}{dT'} (p') A_{O_3} (p',p), \\[-1.0em]
   \intertext{and}\nonumber\\[-2.0em] \epsilon_{O_3} (0,p) & =
   \frac{1}{\sigma T^4(0)} B_{O_3} (0) A_{O_3} (0,p), 

where :math:`A_{O_3}` is the ozone broad–band absorptance from . The
longwave absorptance formulation includes a Voigt line profile effects
for CO\ :math:`_2` and O\ :math:`_3`. For the mid-to-upper stratosphere
(:math:`p\lesssim 10`\ mb), spectral absorption lines are no longer
Lorentzian in shape. To account for the transition to Voigt lines a
method described in is employed. Essentially the pressure appearing in
the mean line width parameter, :math:`\gamma`,

.. math::

   \gamma & = \gamma_o \, \frac{p}{p_0} \\[-1.0em]
   \intertext{is replaced with}\nonumber\\[-2.0em] \gamma & = \gamma_0
   [ \frac{p}{p_0} + \delta \sqrt{\frac{T}{250}} ] ,
   

where :math:`\delta = 5.0 \times 10^{-3}` for CO\ :math:`_2` and
:math:`\delta = 2.5 \times 10^{-3}` for :math:`O_3`. These values insure agreement with
line-by-line cooling rate calculations up to :math:`p \approx 0.3` mb.

Water vapor
~~~~~~~~~~~

Water vapor cannot employ the broad–band absorptance method since
H\ :math:`_2`\ O absorption extends throughout the entire longwave
region. Thus, we cannot factor out the Planck function dependence as in
([4.b.39]). The method of is used for water–vapor absorptivities and
emissivities. This parameterization replaces the scheme developed by
used in previous versions of the model. The new formulation uses the
line-by-line radiative transfer model GENLN3 to generate the
absorptivities and emissivities for H\ :math:`{}_2`\ O. In this version
of GENLN3, the parameters for H\ :math:`_2`\ O lines have been obtained
from the HITRAN2k data base , and the continuum is treated with the
Clough, Kneizys, and Davies (CKD) model version 2.4.1 . To generate the
absorptivity and emissivity, GENLN is used to calculate the transmission
through homogeneous atmospheres for H\ :math:`_2`\ O lines alone and for
H\ :math:`_2`\ O lines and continuum. The calculation is done for a five
dimensional parameter space with coordinates equaling the emission
temperature, path temperature, precipitable water, effective relative
humidity, and pressure. The limits for each coordinate span the entire
range of instantaneous values for the corresponding variable from a
1-year control integration of . The resulting tables of absorptivity and
emissivity are then read into the model for use in the longwave
calculations. The overlap treatment between water vapor and other gases
is described in .

The absorptivity and emissivity can be split into terms for the window
and non-window portions of the infrared spectrum. The window is defined
as 800-1200 cm\ :math:`{}^{-1}`, and the non-window is the remainder of
the spectrum between 20 to 2200 cm\ :math:`{}^{-1}`. Outside the
mid-infrared window (the so-called non-window region), the
H\ :math:`_2`\ Ocontinuum is dominated by the foreign component . The
foreign continuum absorption has the same linear scaling with water
vapor path as line absorption, and thus in the non-window region the
line and continuum absorption are combined in a single expression. In
the window region, where the self-broadened component of the continuum
is dominant, the line and continuum absorption have different scalings
with the amount of water vapor and must be treated separately. The
formalism is identical for the absorptivity and emissivity, and for
brevity only the absorptivity is discussed in detail. The absorptivity
is decomposed into two terms:

.. math:: A(p_1,p_2) \simeq {A_{w}(p_1,p_2)}+ {A_{nw}(p_1,p_2)}\\ ,

where :math:`{A_{w}(p_1,p_2)}` is the window component and
:math:`{A_{nw}(p_1,p_2)}` is the non-window component for the portion of
the atmosphere bounded by pressures :math:`p_1` and :math:`p_2`.

Let :math:`{{\widetilde A}}_{nw}(i)` represent the total non-window
absorption for a homogeneous atmosphere characterized by a set of
scaling parameters :math:`i`. Scaling theory is a relationship between
an inhomogeneous path and an equivalent homogeneous path with nearly
identical line absorption for the spectral band under consideration .
Scaling theory is used to reduce the parameter space of atmospheric
conditions that have to be evaluated. The equivalent pressure,
temperature, and absorber amount are calculated using the standard
Curtis-Godson scaling theory for absorption lines . In addition, we
retain explicit dependence on the emission temperature of the radiation
following , and we introduce dependence on an equivalent relative
humidity. It follows from Curtis-Godson scaling theory that

.. math::

   {A_{nw}(p_1,p_2)}\simeq {{\widetilde A}}_{nw}(l_{nw})
       
   .

In the following expressions, a tilde denotes a parameter derived using
scaling theory for the equivalence between homogeneous and inhomogeneous
atmospheres. The subscript :math:`b` denotes a parameter which depends
upon the spectral band under consideration. The set of scaling
parameters that determine the total non-window absorption are labeled:

.. math::

   l_{nw} = [{\widetilde
   {U_{nw}}},{\widetilde {P_{nw}}},T_e,{\widetilde {T_p}},{\widetilde
   \rho}]
   .

Here :math:`{\widetilde
{U_{nw}}}` is the pressure-weighted precipitable water,
:math:`{\widetilde {P_{nw}}}` is the scaled atmospheric pressure,
:math:`T_e` is the emission temperature of radiation,
:math:`{\widetilde {T_p}}` is the absorber weighted path temperature,
and :math:`{\widetilde
\rho}` is the scaled relative humidity. The subscript :math:`(b=)nw`
indicates that the quantities are evaluated for the non-window.

The absorber-weighted path temperature is:

.. math::

   {\widetilde {T_p}}= {1 \over W} \> {\int_{p_1}^{p_2}}T(p)\> dW(p)
      
   ,

where :math:`T(p)` is the thermodynamic temperature of the atmosphere at
pressure :math:`p`. The H\ :math:`_2`\ O path or precipitable water is:

.. math::

       W & =  {\int_{p_1}^{p_2}}dW(p) \qquad [g/cm{}^{2}] \\ dW(p) & =  q(p)\> dp /
   g \nonumber ,

where :math:`q(p)` is the specific humidity at pressure :math:`p` and
:math:`g` is the acceleration of gravity. The H\ :math:`_2`\ O path and
pressure for a homogeneous atmosphere with equivalent line absorption
are

.. math::

      
      {{\widetilde {W_{b}}}}& =  {\int_{p_1}^{p_2}}{{{\phi_{b}}(T)} \over
      {{\phi_{b}}({\widetilde {T_p}})}}\>dW(p) \\
      
      {{\widetilde {P_{b}}}}& =  {1 \over {{{\widetilde {W_{b}}}}}} {\int_{p_1}^{p_2}}{{{\psi_{b}}(T)} \over
                                         {{\psi_{b}}({\widetilde {T_p}})}}\>p\>dW(p)
   ,

 where

.. math::

     {\phi_{b}}(T) & =  \sum_{k=1}^N S_k(T) \\
     {\psi_{b}}(T) & =  \lbrace\sum_{k=1}^N [ S_k(T)
                 \alpha_k(T)]^{1/2} \rbrace^2
   .

The factor :math:`S_k(T)` is the line strength for each line :math:`k`
in the spectral interval under consideration. The characteristic width
of each line at a reference pressure :math:`p_0` and specific humidity
:math:`q_0` is :math:`\alpha_k(T)`. It is convenient to calculate the
absorptance in terms of a pressure-weighted H\ :math:`_2`\ O path

.. math:: U = {\int_{p_1}^{p_2}}{p \over p_0} \> dW(p)

The equivalent pressure-weighted H\ :math:`_2`\ O path is simply

.. math::

   {{\widetilde
   {U_{b}}}}= {{{\widetilde {P_{b}}}}\over p_0} \> {{\widetilde {W_{b}}}}

Although the relative humidity (or H\ :math:`_2`\ O vapor pressure) is
not included in standard Curtis-Godson scaling theory, it must be
treated as an independent parameter since the vapor pressure determines
the self-broadening of lines and the strength of the self-continuum. The
effective relative humidity :math:`{\widetilde
\rho}` is defined in terms of an effective H\ :math:`_2`\ O specific
humidity :math:`{\widetilde {q}}` and saturation specific humidity
:math:`{\widetilde {q_s}}` along the path:

.. math::

     
     {\widetilde
   \rho}& =  {\widetilde {q}}\over {\widetilde {q_s}}\\ {\widetilde {q}}& =  {g \> W} \over {p_2 -
     p_1} \\
     {\widetilde {q_s}}& =  {\epsilon\> e_s({\widetilde {T_p}})} \over {\widetilde P - (1 -
                 \epsilon) e_s({\widetilde {T_p}})} \\
     \widetilde P & =  {p_0\>U \over W}

where :math:`e_s(T)` is the saturation vapor pressure at temperature
:math:`T`, :math:`\widetilde P` is an effective pressure, and
:math:`\epsilon = 0.622` is the ratio of gas constants for air and water
vapor.

The window term :math:`{A_{w}(p_1,p_2)}` requires a special provision
for the different path parameters for the lines and continuum. Let

.. math::

       
       {{\widetilde A}}_w(i) & =  \hbox{absorptivity for path parameters $i$, lines
       and continuum} \\ {{\widetilde A}}'_w(i) & =  \hbox{absorptivity for path
       parameters $i$, lines only} \nonumber

The set of parameters for the line absorption in the window region are:

.. math::

   l_w = [{\widetilde
   {U_{w}}},{\widetilde {P_{w}}},T_e,{\widetilde {T_p}},{\widetilde
   \rho}]

The set of scaling parameters that determine the continuum absorption
in the window are:

.. math::

   c_w = [U',{\widetilde {P_{w}}},T_e,{\widetilde {T_p}},{\widetilde
   \rho}]

For the continuum, the pressure-weighted path length is calculated
using:

.. math::

   
      U' = {\epsilon \over {\widetilde {q}}} \> {{C_s({{\bar\nu}},{T_{ref}})} \over
           {C_s({{\bar\nu}},{\widetilde {T_p}})}} \> U_c

 where :math:`{T_{ref}}= 296K` is a reference temperature,
:math:`{{\bar\nu}}` is a suitably chosen wavenumber inside the window,
:math:`U_c` is the self-continuum path length, and
:math:`{{{C_s(\nu,T)}}}` is the self continuum absorption coefficient.
The self-continuum path length may be approximated by

.. math::

   U_c = {\int_{p_1}^{p_2}}{q \over \epsilon} \> {p \over p_0} \>
             {{C_s({{\bar\nu}},T)} \over {C_s({{\bar\nu}},{T_{ref}})}} \> dW(p)
       

The lines-only absorptivity can be written in terms of a line
transmission factor :math:`L(i)` and an asymptotic absorptivity
:math:`{A_{w,\infty}}` in the limit of a black-body atmosphere.
:math:`{A_{w,\infty}}` is a function only of :math:`T_e` . The
relationship is

.. math::

   
       {{\widetilde A}}'_w(i) = {A_{w,\infty}}[1 - L(i)]

Define an effective continuum transmission :math:`C(i)` by setting

.. math::

   
       {{\widetilde A}}_w(i) = {A_{w,\infty}}[1 - L(i) C(i)]

We approximate the window absorptivity by:

.. math:: {A_{w}(p_1,p_2)}\simeq {A_{w,\infty}}[1 - L(l_w) C(c_w)]

 This approximation for :math:`{A_{w}(p_1,p_2)}` can be cast entirely in
terms of the absorptivities defined in equation [eq:awdef]. From
equations [eq:awline] and [eq:awcont], the line and continuum
transmission are:

.. math::

       L(l_w) & =  1 - {{{\widetilde A}}'_w(l_w) \over {A_{w,\infty}}}  \\
       C(c_w) & =  {{{A_{w,\infty}}- {{\widetilde A}}_w(c_w)} \over {{A_{w,\infty}}- {{\widetilde A}}'_w(c_w)}}
       \nonumber

In the presence of stratospheric volcanic aerosols, the expressions for
the absorptivity become:

.. math::

       {A_{nw}(p_1,p_2)}& \simeq & {A_{nw,\infty}}[1 - (1 - {{{\widetilde A}}_{nw}(l_{nw}) \over
                     {A_{nw,\infty}}} ) {{\cal T}^{nw}_{H_2SO_4}} ] \nonumber \\
       {A_{w}(p_1,p_2)}& \simeq & {A_{w,\infty}}[1 - L(l_w) C(c_w) {{\cal T}^{w}_{H_2SO_4}}] 

The volcanic transmission factor is

.. math::

   {{\cal T}^{b}_{H_2SO_4}} = {{\bar T}^{b}_{H_2SO_4}} = \exp(-D\,\kappa_{b,volc}\,W_{volc})
       

 where :math:`D = 1.66` is the diffusivity factor,
:math:`\kappa_{b,volc}` is an effective specific extinction for the
band, and :math:`W_{volc}` is the mass path of the volcanic aerosols.
The extinction :math:`\kappa_{b,volc}` has been adjusted iteratively to
reproduce the heating rates calculated using the spectral bands in the
original parameterization. This completes the set of approximations used
to calculate the absorptivity (and by extension the emissivity).

Trace gas parameterizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The radiative effects of methane are represented by the last term in
([4.b.46]). We re-write this in terms of the absorptivity due to
methane as

.. math::

   \nonumber\int_{1170}^{1500} { (1-{\cal T}_{CH_4}{\cal T}_{N_2O}^3{\cal
   T}_{H_2O}{{\cal T}^{5}_{H_2SO_4}})F(B_\nu)d\nu} = \int {(1-{\cal T}_{H_2O}{{\cal T}^{nw}_{H_2SO_4}})F(B_\nu)d\nu} + \\
   \int {{\cal A}_{CH_4}{\cal T}_{H_2O}{{\cal T}^{5}_{H_2SO_4}}F(B_\nu)d\nu} + \int {{\cal
   A}_{N_2O}^3{\cal T}_{CH_4}{\cal T}_{H_2O}{{\cal T}^{5}_{H_2SO_4}}F(B_\nu)d\nu}
     

Note that this expression also incorporates the absorptance due to the
7.7 micron band of nitrous oxide as well. The first term is due to the
rotation band of water vapor and is already accounted for in the
radiation model by the parameterization described in . The second term
in ([4.b.53]) accounts for the absorptance due to the 7.7 micron band
of methane. The spectroscopic parameters are from . In terms of the
broad band approximation we have,

.. math::

   \int {{\cal A}_{CH_4}{\cal T}_{H_2O}{{\cal T}^{5}_{H_2SO_4}}F(B_\nu)d\nu} \approx A_{CH_4}\bar
   T_{H_2O}{{\bar T}^{5}_{H_2SO_4}}F(B_{\bar \nu})
     

where according to ([4.b.40]),

.. math::

   A_{CH_4}=6.00444\sqrt {T_p}\ln \{ 1+\frac{u} {\sqrt {4+u(1+1/\beta)}} \}
     

where :math:`T_p` is a path weighted temperature,

.. math::

   T_p = \frac{\int {T(p)dp}}{\int {dp}}
     

The dimensionless path length is,

.. math::

   u = \frac{D \; 8.60957 \times 10^4}{g} \int {\frac{\mu_{CH_4}}{\sqrt T}dp}
     

and the mean line width factor is,

.. math::

   \beta =2.94449 \frac{\int { \frac{1}{T}( \frac{P}{P_0} )
   \mu_{CH_4}dp}}{\int {\frac{1}{\sqrt T}\mu_{CH_4}dp}}
     

where :math:`\mu_{CH_4}` is the mass mixing ratio of methane,
:math:`T` is the local layer temperature in Kelvin and :math:`P` is
the pressure in Pascals, and :math:`P_0` is :math:`1\times 10^5` Pa.
:math:`D` is a diffusivity factor of 1.66. The water vapor overlap
factor for this spectral region is,

.. math::

   \bar T_{H_2O}& ={\rm exp} (-U_{H_2O})
   \\[-1.0em]
   \intertext{where,}\nonumber\\[-2.0em] U_{H_2O}& = D \int
   {\mu_{H_2O}( \frac{P}{P_0} )\frac{dp}{g}}
     

   and :math:`\mu_{H_2O}` is the mass mixing ratio of water vapor.

For nitrous oxide there are three absorption bands of interest: 589,
1168 and 1285 cm\ :math:`^{-1}` bands. The radiative effects of the 1285
cm\ :math:`^{-1}` band is given by the last term in ([4.b.53]),

.. math::

   \int {{\cal A}_{N_2O}^3{\cal T}_{CH_4}{\cal T}_{H_2O}{{\cal T}^{5}_{H_2SO_4}}F(B_\nu)d\nu}
   \approx A_{N_2O}^3\bar T_{CH_4}\bar T_{H_2O}{{\bar T}^{5}_{H_2SO_4}}F(B_{\bar\nu})
   

The absorptance for the 1285 cm\ :math:`^{-1}` N\ :math:`_2`\ O band is
given by

.. math::

   A_{N_2O}^3=2.35558\sqrt {T_p}\ln \{ 1 + \frac{u_0^3}{\sqrt
   {4+u_0^3(1+1/\beta_0^3)}} + \frac{u_1^3}{\sqrt
   {4+u_1^3(1+1/\beta_1^3)}} \}
   

where :math:`u_0^3`, :math:`\beta_0^3` account for the fundamental
transition, while :math:`u_1^3`, :math:`\beta_1^3` account for the first
“hot” band transition. These parameters are defined as

.. math::

   u_0^3& =D \; 1.02346 \times 10^5\int {\frac{\mu_{N_2O}}{\sqrt
   {T}}\frac{dp}{g}}
   \\[-1.0em]
   \intertext{and,}\nonumber\\[-2.0em] \beta_0^3 & = 19.399 \frac{\int
   {\frac{1}{\sqrt {T}}( \frac{P}{P_0} )du_0}} {\int {du^3_0}}
   

While the “hot” band parameters are defined as

.. math::

   u_1^3 & = D \; 2.06646\times 10^5 \int {\frac{1}{\sqrt {T}}e^{-847.36/T} \mu_{N_2O}\frac{dp}{g}} \\
   [-1.0em] \intertext{and,}\nonumber\\[-2.0em] \beta_1^3 & = 19.399 \frac{ \int{ 
   \frac{1}{\sqrt {T}}( \frac{P}{P_{0}} ) du^3_1}}{\int {du^3_1}}
   

 The overlap factors in ([4.b.61]) due to water vapor is the same factor
defined by ([4.b.59]), while the overlap due to methane is obtained by
using the definition of the transmission factor in terms of the
equivalent width .

.. math::

   \bar T_{CH_4}=e^{-A_{CH_4}/2A_0}
   

Substitution of ([4.b.55]) into ([4.b.61]) leads to,

.. math::

   \bar T_{CH_4}=\frac{1}{1+0.02\frac{u}{\sqrt {4+u(1+1/\beta)}}}
   

where :math:`u` and :math:`\beta` are given by ([4.b.57]) and
([4.b.58]), respectively, and the 0.02 factor is an empirical constant
to match the overlap effect obtained from narrow band model benchmark
calculations. This factor can physically be justified as accounting for
the fact that the entire methane band does not overlap the
N\ :math:`_2`\ O band.

The 1168 cm\ :math:`^{-1}` N\ :math:`_2`\ O band system is represented
by the seventh term on the RHS of ([4.b.46]). This term can be
re-written as

.. math::

   \nonumber \int \limits_{1120}^{1170}{ (1-{\cal T}_{CFC12}^4{\cal
   T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}{\cal T}_{N_2O}^2)F(B_\nu)d\nu} = \int {(1-{\cal
   T}_{H_2O}{{\cal T}^{w}_{H_2SO_4}})F(B_\nu)d\nu} + \\[1ex] \int {{\cal A}_{CFC12}^4{\cal
   T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}F(B_\nu)d\nu} + \int {{\cal A}_{N_2O}^2{\cal
   T}_{CFC12}^4{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}F(B_\nu)d\nu}
   

where the last term accounts for the 1168 cm\ :math:`^{-1}`
N\ :math:`_2`\ O band. For the broad band formulation this expression
becomes,

.. math::

   \int {{\cal A}_{N_2O}^2{\cal T}_{CFC12}^4{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}F(B_\nu) d\nu}
   \approx A_{N_2O}^2\bar T_{CFC12}^4\bar T_{H_2O}{{\bar T}^{4}_{H_2SO_4}}F(B_{\bar \nu })
   

The band absorptance for the 1168 cm\ :math:`^{-1}`N\ :math:`_2`\ O band is given by

.. math::

   A_{N_2O}^2=2.54034\sqrt {T_p}\ln \{ 1+\frac{u_0^2} {\sqrt
   {4+u_0^2(1+1/{\beta_0^2}}} \}
   

where the fundamental band path length and mean line parameters can be
simply expressed in terms of the parameters defined for the 1285
cm\ :math:`^{-1}` band (eq. [4.b.63]-[4.b.64]).

.. math::

   u_0^2& =0.0333767u_0^3
   \\[-1.0em]
   \intertext{and,}\nonumber\\[-2.0em] \beta _0^2& =0.982143\beta_0^3
   

Note that the 1168 cm\ :math:`^{-1}` band does not include a “hot” band
transition. The overlap by water vapor includes the effects of water
vapor rotation lines, the so called “e-type” and “p-type” continua (e.g.). 
The combined effect of these three absorption features is,

.. math::

   \bar T_{H_2O}=\bar T_l\bar T_e\bar T_p
   

where the contribution by line absorption is modeled by a Malkmus model
formulation,

.. math::

   \bar T_l=\exp \{ -\delta_1 \bar \Pi ( \sqrt {1+\delta_2
   \frac{\bar u_l}{\bar \Pi}}-1 ) \}
   

where :math:`\delta_1` and :math:`\delta_2` are coefficients that are
obtained by fitting ([4.b.75]) to the averaged transmission from a 10
cm\ :math:`^{-1}` narrow band Malkmus. The path length :math:`\bar u_l`
is,

.. math::

   \bar u_l & = D \; \bar \Phi \int {\rho_w \frac{dP}{g}}
   \\[-1.0em]
   \intertext{and,}\nonumber\\[-2.0em] \bar \Pi & =( \frac{P}{P_0}
   )( \frac{\bar\Psi}{\bar\Phi} ),
   

where :math:`\bar\Phi` and :math:`\bar\Psi` account for the temperature
dependence of the spectroscopic parameters

.. math::

   \bar \Psi & = e^{-\alpha {T_p-250} -\beta {T_p-250} ^2} \\
   \bar \Phi & = e^{-\alpha {T_p-250} -\beta {T_p-250} ^2}
   

The coefficients for various spectral intervals are given in
Table [table:coeftdf]. The transmission due to the e-type continuum is
given by

.. math::

   \bar T_e& =e^{-\delta_3\bar u_e} \\
   [-1.0em] \intertext{where the path length is defined as}\nonumber\\[-2.0em]
   \bar u_e & =\frac{D}{P_0\varepsilon g} \int {e^{1800(\frac{1}{T}- \frac{1}{296}})w_{H_2O}^2PdP}
   

The p-type continuum is represented by

.. math::

   T_p& =e^{-\delta_4\bar u_p} \\
   [-1.0em] \intertext{where,}\nonumber\\[-2.0em] \bar u_p & = \frac{D}{gP_0} \int
   {e^{1800(\frac{1}{T}-\frac{1}{296})} w_{H_2O}PdP}
   
The factors :math:`\delta_1`, :math:`\delta_2`, :math:`\delta_3` and
:math:`\delta_4` are listed for specific spectral intervals in
Table [table:coefwv].

| \|cccccc\| Index & :math:`\nu_1-\nu_2` & :math:`\alpha` &
  :math:`\beta` & :math:`\alpha'` & :math:`\beta'`
| 1 & 750 - 820 & 2.9129e-2 & -1.3139e-4 & 3.0857e-2 & -1.3512e-4
| 2 & 820 - 880 & 2.4101e-2 & -5.5688e-5 & 2.3524e-2 & -6.8320e-5
| 3 & 880 - 900 & 1.9821e-2 & -4.6380e-5 & 1.7310e-2 & -3.2609e-5
| 4 & 900 - 1000 & 2.6904e-2 & -8.0362e-5 & 2.6661e-2 & -1.0228e-5
| 5 & 1000 - 1120 & 2.9458e-2 & -1.0115e-4 & 2.8074e-2 & -9.5743e-5
| 6 & 1120 - 1170 & 1.9892e-2 & -8.8061e-5 & 2.2915e-2 & -1.0304e-4

| \|cccccc\| Index & :math:`\nu_1-\nu_2` & :math:`\delta_1` &
  :math:`\delta_2` & :math:`\delta_3` & :math:`\delta_4`
| 1 & 750 - 820 & 0.0468556 & 14.4832 & 26.1891 & 0.0261782
| 2 & 820 - 880 & 0.0397454 & 4.30242 & 18.4476 & 0.0369516
| 3 & 880 - 900 & 0.0407664 & 5.23523 & 15.3633 & 0.0307266
| 4 & 900 - 1000 & 0.0304380 & 3.25342 & 12.1927 & 0.0243854
| 5 & 1000 - 1120 & 0.0540398 & 0.698935 & 9.14992 & 0.0182932
| 6 & 1120 - 1170 & 0.0321962 & 16.5599 & 8.07092 & 0.0161418

The final N\ :math:`_2`\ O band centered at 589 cm\ :math:`^{-1}` is
represented by the first term on the RHS of ([4.b.46]),

.. math::

   \nonumber eqn{\int\limits_{500}^{750} {(1 - {\cal
   T}_{CO_2}^1{\cal T}_{N_2O}^1{\cal T}_{H_2O}{{\cal T}^{1}_{H_2SO_4}}) F(B_\nu) d\nu} =} \\[1ex]
   & & \int {(1-{\cal T}_{CO_2}^1{\cal_T}_{H_2O}{{\cal T}^{1}_{H_2SO_4}})F(B_\nu)d\nu} + \int
   {{\cal A}_{N_2O}^1{\cal T}_{CO_2}^1{\cal T}_{H_2O}{{\cal T}^{1}_{H_2SO_4}}F(B_\nu)d\nu}
     

where the last term in ([4.b.84]) represents the radiative effects of
the 589 cm\ :math:`^{-1}` N\ :math:`_2`\ O band,

.. math::

   \int {{\cal A}_{N_2O}^1{\cal T}_{CO_2}^1{\cal T}_{H_2O}{{\cal T}^{1}_{H_2SO_4}}F(B_\nu)d\nu}
   \approx A_{N_2O}^1\bar T_{CO_2}^1\bar T_{H_2O}{{\bar T}^{1}_{H_2SO_4}}F(B_{\bar \nu })
     

The absorptance for this band includes both the fundamental and hot
band transitions,

.. math::

   A_{N_2O}^1 = 2.65581 \sqrt{T_p} \ln \{
   1 + \frac{u_0^1}{\sqrt{4+u_0^1(1 + 1/\beta_0^1)}} + \frac{u_1^1}{\sqrt{4+u_1^1(1 + 1/\beta_1^1)}} \}
     

where the path lengths for this band can also be defined in terms of
the 1285 cm\ :math:`^{-1}` band path length and mean lines parameters ([4.b.63] - [4.b.66]),

.. math::

   u_0^1 & = 0.100090u_0^3
   \\[-1.0em]
   \intertext{and,}\nonumber\\[-2.0em] \beta_0^1 & = 0.964282\beta_0^3
   \\[-1.0em]
   \intertext{and,}\nonumber\\[-2.0em] u_1^1 & = 0.0992746u_1^3
   \\[-1.0em]
   \intertext{and,}\nonumber\\[-2.0em] \beta _1^1 & = 0.964282\beta_1^3
    
The overlap effect of water vapor is given by the transmission factor
for the 500 to 800 cm\ :math:`^{-1}` spectral region defined by in
their Table A2. This expression is thus consistent with the
transmission factor for this spectral region employed for the water
vapor formulation of the first term on the right hand side of
([4.b.84]). The overlap factor due to the CO\ :math:`_2` bands near
589 cm\ :math:`^{-1}` is obtained from the formulation in ,

.. math::

   \bar T_{CO_2}^1 = \frac{1}{1 + 0.2\frac{u_{CO_2}}
   {\sqrt{4+u_{CO_2}(1+1/\beta_{CO_2})}}}
     

where the functional form is obtained in the same manner as the
transmission factor for CH\ :math:`_4` was determined in ([4.b.67]).
The 0.2 factor is empirically determined by comparing ([4.b.91]) with
results from 5 cm\ :math:`^{-1}` Malkmus narrow band calculations. The
path length parameters are given by

.. math::

   u_{CO_2}& =\frac{D \; 4.9411\times 10^4(1-e^{-960/T})^3} {\sqrt{T_p}}
   e^{-960/T} \int {w_{CO_2} \frac{dP}{g}}
   \\[-1.0em]
   \intertext{and,}\nonumber\\[-2.0em] \beta_{CO_2} & =
   \frac{5.3228}{\sqrt{T_p}} \{ \frac{P}{P_0} +5\times
   e^{-3}\sqrt{\frac{T}{250}\frac{T}{300}} \}
     
The effects of both CFC11 and CFC12 are included by using the approach
of . Thus, the band absorptance of the CFCs is given by

.. math::

   A_{CFC}=\Delta \nu ( 1-e^{-D\frac{S}{\Delta \nu}u_{CFC}} )
   

where :math:`\Delta \nu` is the width of the CFC absorption band,
:math:`S` is the band strength, :math:`u_{CFC}` is the abundance of CFC
(g cm\ :math:`^{-2}`),

.. math::

   u_{CFC}=\int {\mu_{CFC}\frac{dp}{g}}
   
where :math:`\mu_{CFC}` is the mass mixing ratio of either CFC11 or
CFC12. :math:`D` is the diffusivity factor. In the linear limit
:math:`D=2`, since ([4.b.94]) deviates slightly from the pure linear
limit we let :math:`D=1.8`. We account for the radiative effects of four
bands due to CFC11 and four bands due to CFC12. The band parameters used
in ([4.b.94]) for these eighth bands are given in Table [table:cfc].

The contribution by these CFC absorption bands is accounted for by the
following terms in ([4.b.46]).

.. math::

   \int\limits_{750}^{820} {(1-{\cal T}_{CFC11}^1{\cal T}_{H_2O}{{\cal T}^{\*}_{H_2SO_4}})
   F(B_\nu)d\nu} & = \int {(1-{\cal T}_{H_2O}{{\cal T}^{nw}_{H_2SO_4}})F(B_\nu)d\nu} \nonumber \\
   &+& \int {{\cal A}_{CFC11}^1{\cal T}_{H_2O}{{\cal T}^{\*}_{H_2SO_4}}F(B_\nu)d\nu} \\
   \int\limits_{820}^{880} {(1-{\cal T}_{CFC11}^2{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}})
   F(B_\nu)d\nu} & =\int {(1-{\cal T}_{H_2O}{{\cal T}^{w}_{H_2SO_4}})F(B_\nu)d\nu} \nonumber \\
   &+& \int {{\cal A}_{CFC11}^2{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}F(B_\nu)d\nu} \\
   \int\limits_{880}^{900} {(1-{\cal T}_{CFC12}^1{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}})
   F(B_\nu)d\nu} & =\int {(1-{\cal T}_{H_2O}{{\cal T}^{w}_{H_2SO_4}})F(B_\nu)d\nu} \nonumber \\
   & + int {{\cal A}_{CFC12}^1{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}F(B_\nu)d\nu} \\
   \int\limits_{900}^{1000} {(1 -{\cal T}_{CO_2}^2{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}{\cal
   T}_{CFC11}^3{\cal T}_{CFC12}^2) F(B_\nu)d\nu} & =\int {(1-{\cal
   T}_{H_2O}{{\cal T}^{w}_{H_2SO_4}})F(B_\nu)d\nu} \nonumber \\ + \int {{\cal A}_{CFC12}^2{\cal
   T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}F(B_\nu)d\nu} & + \int {{\cal A}_{CFC11}^3{\cal
   T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}{\cal T}_{CFC12}^2F(B_\nu)d\nu}  \\ & + \int {{\cal
   A}_{CO_2}^2{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}{\cal T}_{CFC11}^3{\cal T}_{CFC12}^2
   F(B_\nu)d\nu}
   \nonumber \\
   \int\limits_{1000}^{1120} {(1 -{\cal T}_{CO_2}^3{\cal T}_{O_3}{\cal
   T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}} {\cal T}_{CFC11}^4{\cal T}_{CFC12}^3)F(B_\nu)d\nu} & = \int
   {(1-{\cal T}_{H_2O}{{\cal T}^{w}_{H_2SO_4}})F(B_\nu)d\nu} \nonumber \\ + \int {{\cal
   A}_{O_3}{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}F(B_\nu)d\nu} & + \int {{\cal A}_{CO_2}^3{\cal
   T}_{O_3}{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}{\cal T}_{CFC11}^4{\cal
   T}_{CFC12}^3F(B_\nu)d\nu} \nonumber \\ + \int {{\cal A}_{CFC11}^4{\cal
   T}_{O_3}{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}F(B_\nu)d\nu} & + \int {{\cal A}_{CFC12}^3{\cal
   T}_{O_3}{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}F(B_\nu)d\nu} 

\|cccc\| Band Number & Band Center & :math:`\Delta\nu` & :math:`S/\Delta\nu` & (cm:math:`^{-1}`) & (cm:math:`^{-1}`) & (cm:math:`^2`
gm\ :math:`^{-1}`)
1\ :math:`^1` & 798 & 50 & 54.09
2\ :math:`^2` & 846 & 60 & 5130.03
3\ :math:`^1` & 933 & 60 & 175.005
4\ :math:`^2` & 1085 & 100 & 1202.18
1\ :math:`^1` & 889 & 45 & 1272.35
2\ :math:`^2` & 923 & 50 & 5786.73
3\ :math:`^2` & 1102 & 80 & 2873.51
4\ :math:`^2` & 1161 & 70 & 2085.59

Data are from .

Data are from .

For the 798 cm\ :math:`^{-1}` CFC11 band, the absorption effect is given
by the second term on the right hand side of ([4.b.96]),

.. math::

   \int {{\cal A}_{CFC11}^1{\cal T}_{H_2O}{{\cal T}^{*}_{H_2SO_4}}F(B_\nu)d\nu} \approx
   A_{CFC11}^1\bar T_{H_2O}{{\bar T}^{*}_{H_2SO_4}}F(B_{\bar \nu })
   

where the band absorptance for the CFC is given by ([4.b.94]) and the
overlap factor due to water vapor is given by ([4.b.74]) using the index
1 factors from Tables [table:coeftdf] and [table:coefwv]. Similarly, the
:math:`846~\rm{cm}^{-1}` CFC11 band is represented by the second term on
the RHS of ([4.b.97]),

.. math::

   \int {{\cal A}_{CFC11}^2{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}F(B_\nu)d\nu} \approx
   A_{CFC11}^2\bar T_{H_2O}{{\bar T}^{3}_{H_2SO_4}}F(B_{\bar\nu})
   

 where the H\ :math:`_2`\ O overlap factor is given by index 2 in
Tables [table:coeftdf] and [table:coefwv]. The 933 cm\ :math:`^{-1}`
CFC11 band is given by the third term on the RHS of ([4.b.99]),

.. math::

   \int {{\cal A}_{CFC11}^3{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}{\cal T}_{CFC12}^2F(B_\nu)d\nu}
   \approx A_{CFC11}^3\bar T_{H_2O}{{\bar T}^{3}_{H_2SO_4}}T_{CFC12}^2F(B_{\bar \nu})
   

where the H\ :math:`_2`\ O overlap factor is defined as index 4 in
Tables [table:coeftdf] and [table:coefwv], and the CFC12 transmission
factor is obtained from ([4.b.94]). The final CFC11 band centered at
1085 cm\ :math:`^{-1}` is represented by the fourth term on the RHS of
([4.b.100]),

.. math::

   \int{ {\cal A}_{CFC11}^4{\cal T}_{O_3}{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}F(B_\nu)d\nu}
   \approx A_{CFC11}^4\bar T_{O_3}\bar T_{H_2O}{{\bar T}^{4}_{H_2SO_4}}F(B_{\bar \nu})
   

where the transmission due to the 9.6 micron ozone band is defined
similar to ([4.b.91]) for CO\ :math:`_2` as

.. math::

   \bar T_{O_3}= \frac{1}{1+\sum\limits_{i=1}^2 \frac{u_{O_3}^i}
   {\sqrt{4+u_{O_3}^i(1 + 1/\beta_{O_3}^i)}}}
   

where the path lengths are defined in . The H\ :math:`_2`\ O overlap
factor is defined by index 5 in Tables [table:coeftdf] and
[table:coefwv].

For the 889 cm\ :math:`^{-1}` CFC12 band the absorption is defined by
the second term in ([4.b.98]) as

.. math::

   \int { {\cal A}_{CFC12}^1{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}F(B_\nu)d\nu} \approx
   A_{CFC12}^1\bar T_{H_2O}{{\bar T}^{3}_{H_2SO_4}}F(B_{\bar \nu })
   

where the H\ :math:`_2`\ O overlap factor is defined by index 3 of
Tables [table:coeftdf] and [table:coefwv], and the CFC absorptance is
given by ([4.b.94]). The 923 cm\ :math:`^{-1}` CFC12 band is described
by the second term in ([4.b.99]),

.. math::

   \int {{\cal A}_{CFC12}^2{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}F(B_\nu) d\nu} \approx
   A_{CFC12}^2\bar T_{H_2O}{{\bar T}^{3}_{H_2SO_4}}F(B_{\bar \nu})
   

where the H\ :math:`_2`\ O overlap is defined as index 4 in
Tables [table:coeftdf] and [table:coefwv]. The 1102 cm\ :math:`^{-1}`
CFC12 band is represented by the last term on the RHS of ([4.b.100]),

.. math::

   \int{ {\cal A}_{CFC12}^3{\cal T}_{O_3}{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}F(B_\nu) d\nu}
   \approx A_{CFC12}^3\bar T_{O_3}\bar T_{H_2O}{{\bar T}^{4}_{H_2SO_4}}F(B_{\bar \nu})
     

where the transmission by ozone is described by ([4.b.105]) and the
H\ :math:`_2`\ O overlap factor is represented by index 5 in
Tables [table:coeftdf] and [table:coefwv]. The final CFC12 band at
1161 cm\ :math:`^{-1}` is represented by the second term on the RHS of ([4.b.69]),

.. math::

   \int{{\cal A}_{CFC12}^4{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}F(B_\nu) d\nu} \approx
   A_{CFC12}^4\bar T_{H_2O}{{\bar T}^{4}_{H_2SO_4}}F(B_{\bar \nu})
     

where the H\ :math:`_2`\ O overlap factor is defined as index 6 in
Tables [table:coeftdf] and [table:coefwv].

There are two minor bands of carbon dioxide that were added to the CCM3
longwave model. These bands play a minor role in the present day
radiative budget, but are very important for high levels of
CO\ :math:`_2`, such as during the Archean. The first band we consider
is centered at 961 cm\ :math:`^{-1}`. The radiative contribution of this
band is represented by the last term in ([4.b.99]),

.. math::

   \int {{\cal A}_{CO_2}^2{\cal T}_{H_2O}{{\cal T}^{3}_{H_2SO_4}}{\cal T}_{CFC11}^3{\cal
   T}_{CFC12}^2 F(B_\nu) d\nu} \approx A_{CO_2}^2\bar T_{H_2O}{{\bar T}^{3}_{H_2SO_4}}\bar
   T_{CFC11}^3\bar T_{CFC12}^2F(B_{\bar \nu})
   

where the transmission factors for water vapor, CFC11 and CFC12 are
defined in the previous section for the 900 to 1000 cm\ :math:`^{-1}`
spectral interval. The absorptance due to CO\ :math:`_2` is given by

.. math::

   A_{CO_2}^2 = 3.8443\sqrt{T_p}\ln \{ 1+\sum\limits_{i=1}^3
   \frac{u_i}{\sqrt {4+u_i(1+1/\beta_i)}} \}
   

where the path length parameters are defined as

.. math::

   u_1 & = 3.88984 \times 10^3\alpha (T_{p}) we^{-1997.6/T} \\
   
   u_1 & = 3.88984 \times 10^3\alpha (T_{p}) we^{-1997.6/T}\\
   
   u_3 & = 6.50642\times 10^3\alpha(T_{p}) we^{-2989.7/T}
   

and the pressure parameter is,

.. math::

   \beta _1 & = 2.97558( \frac{P}{P_{0}} )\frac{1}{\sqrt{T}}  \\
   \beta_2  & = \beta_1  \\
   \beta_3  & = 2\beta_1
   
and,

.. math::

   \alpha (T_p) = \frac{( 1-e^{-1360.0/T_p} )^3}{\sqrt{T_p}}
   

The CO\ :math:`_2` band centered at 1064 cm\ :math:`^{-1}` is
represented by the third term on the RHS of ([4.b.100]),

.. math::

   \int {{\cal A}_{CO_2}^3{\cal T}_{O_3}{\cal T}_{H_2O}{{\cal T}^{4}_{H_2SO_4}}{\cal T}_{CFC11}^4
   {\cal T}_{CFC12}^3F(B_\nu) d\nu} \approx A_{CO_2}^3\bar T_{O_3}\bar
   T_{H_2O}{{\bar T}^{4}_{H_2SO_4}} \bar T_{CFC11}^4\bar T_{CFC12}^3F(B_{\bar \nu})
   

 where the transmission factors due to ozone, water vapor, CFC11 and
CFC12 are defined in the previous section. The absorptance due to the
1064 cm\ :math:`^{-1}` CO\ :math:`_2` band is given by

.. math::

   A_{CO_2}^3 = 3.8443\sqrt{T_p}\ln \{ 1+\sum\limits_{i=1}^3
   \frac{u_i}{\sqrt {4+u_i(1+1/\beta_i)}} \}
   

where the dimensionless path length is defined as

.. math::

   u_1 & = 3.42217\times 10^3\alpha (T_{p}) we^{-1849.7/T}    \\
   u_2 & = 6.02454\times 10^3\alpha (T_{p}) we^{-2782.1/T}    \\
   u_3 & = 5.53143\times 10^3\alpha (T_{p}) we^{-3723.2/T}    \\
   [-1.0em] \intertext{where }\nonumber\\[-2.0em] \alpha (T_p)& = \frac{(1-e^{-1540.0/T_p} )^3}{\sqrt{T_p}}
   
The pressure factor, :math:`\beta_1`, for ([4.b.120]) is the same as
defined in ([4.b.115]), while the other factors are,

.. math::

   \beta _2& =2\beta _1  \\
   \beta _3& =\beta _2

In the above expressions, :math:`w` is the column mass abundance of CO\ :math:`_2`,

.. math:: w=\int {\mu _{CO_2}\frac{dP}{g}} = \frac{\mu _{CO_2}}{g}\Delta P

 where :math:`\mu_{CO_2}` is the mass mixing ratio of CO\ :math:`_2` (assumed constant).

Mixing ratio of trace gases
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The mixing ratios of methane, nitrous oxide, CFC11 and CFC12 are
specified as zonally averaged quantities. The stratospheric mixing
ratios of these various gases do vary with latitude. This is to mimic
the effects of stratospheric circulation on these tracers. The exact
latitude dependence of the mixing ratio scale height was based on
information from a two dimensional chemical model (S. Solomon, personal
communication). In the troposphere the gases are assumed to be well
mixed,

.. math::

   \mu_{CH_4}^0& =0.55241w_{CH_4}    \\
   \mu_{N_2O}^0& =1.51913w_{N_2O}    \\
   \mu_{CFC11}^0& =4.69548w_{CFC11}    \\
   \mu_{CFC12}^0& =4.14307w_{CFC12}   

where :math:`w` denotes the volume mixing ratio of these gases. The
employs volume mixing ratios for the year 1992 based on ,
:math:`w_{CH_4} = 1.714 ~ppmv`, :math:`w_{N_2O}=0.311 ~ppmv`,
:math:`w_{CFC11} = 0.280 ~ppbv` and :math:`w_{CFC12}=0.503 ~ppbv`. The
pressure level (mb) of the tropopause is defined as

.. math::

   p_{trop}=250.0-150.0\cos ^2\phi
   

For :math:`p\leq p_{trop}`, the stratospheric mixing ratios are defined
as

.. math::

   \mu _{CH_4}& =\mu _{CH_4}^0( \frac{p}{p_{trop}}   )^{X_{CH_4}}    \\
   \mu _{N_2O}& =\mu _{N_2O}^0( \frac{p}{p_{trop}}   )^{X_{N_2O}}    \\
   \mu _{CFC11}& =\mu _{CFC11}^0( \frac{p}{p_{trop}}   )^{X_{CFC11}}    \\
   \mu _{CFC12}& =\mu _{CFC12}^0( \frac{p}{p_{trop}}   )^{X_{CFC12}}

where the mixing ratio scale heights are defined as

.. math::
   .
   \begin{matrix}
   X_{CH_4} & =  0.2353 \\ X_{N_2O} & =  0.3478+0.00116| \phi
   | \\ X_{CFC11} & =  0.7273+0.00606| \phi | \\
   X_{CFC12} & =  0.4000+0.00222| \phi | \\
   \end{matrix}
   \}| \phi |\le 45
   
and,

.. math::
   .
   \begin{matrix}
   X_{CH_4} & =  0.2353+0.22549| \phi | \\ X_{N_2O} & = 
   0.4000+0.01333| \phi | \\ X_{CFC11} & = 
   1.0000+0.01333| \phi | \\ X_{CFC12} & = 
   0.5000+0.02444| \phi | \\
   \end{matrix}
   \}| \phi |\ge 45
   

where :math:`\phi` is latitude in degrees.

Cloud emissivity
~~~~~~~~~~~~~~~~

The clouds in  are gray bodies with emissivities that depend on cloud
phase, condensed water path, and the effective radius of ice particles.
The cloud emissivity is defined as

.. math::

   \epsilon_{cld} =1-e^{-D\kappa _{abs}CWP}
   

where :math:`D` is a diffusivity factor set to 1.66,
:math:`\kappa_{abs}` is the longwave absorption coefficient
(:math:`m^2 g^{-1}`), and CWP is the cloud water path
(:math:`g m^{-2}`). The absorption coefficient is defined as

.. math::

   \kappa _{abs}=\kappa _l( {1-f_{ice}} )+\kappa _if_{ice}
   

where :math:`\kappa_l` is the longwave absorption coefficient for
liquid cloud water and has a value of 0.090361, such that
:math:`D\kappa_l` is 0.15. :math:`\kappa_i` is the absorption
coefficient for ice clouds and is based on a broad band fit to the
emissivity given by Ebert and Curry’s formulation,

.. math::

   \kappa_i=0.005 + \frac{1}{r_{ei}}.
   

Numerical algorithms and cloud overlap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The treatment of cloud overlap follows . The new parameterizations can
treat random, maximum, or an arbitrary combination of maximum and random
overlap between clouds. This scheme replaces the treatment in CCM3,
which was an exact treatment for random overlap of plane-parallel
infinitely-thin gray-body clouds. The new method is an exact treatment
for arbitrary overlap among the same type of clouds. It is therefore
more accurate than the original matrix method of and improved variants
of it .

If longwave scattering is omitted, the upwelling and downwelling
longwave fluxes are solutions to uncoupled ordinary differential
equations . The emission from clouds is calculated using the
Stefan-Boltzmann law applied to the temperatures at the cloud
boundaries. The cloud boundaries correspond to the interfaces of the
model layers. This approximation greatly simplifies the mathematical
form of the flux solutions since the clouds can be treated as boundary
conditions for the differential equations. The approximation becomes
more accurate as the clouds become more optically thick.

The solutions are formulated in terms of the same conversion of vertical
cloud distributions to binary cloud profiles used for the shortwave
calculations (p. ). First consider the flux boundary conditions for a
maximum-overlap region :math:`{j}`. The downward flux at the upper
boundary of the region is spatially heterogeneous and has terms
contributed by all the binary configurations above the region.
Similarly, the upward flux at the lower boundary of the region has terms
contributed by all the binary configurations below the region. The
fluxes within the region are area-weighted sums of the fluxes calculated
for all possible combinations of these boundary terms and the cloud
configurations within the region. Fortunately the arithmetic can be
simplified because the solutions to the longwave equations are linear in
the boundary conditions. Therefore the downward (upward) fluxes can be
computed by summing the solutions for each configuration in the region
for a single boundary condition given by the area-averaged fluxes at the
region interfaces denoted by
:math:`{{\bar{F}^{\downarrow}({{i_{{{j}},\min}}})}}`
(:math:`{{\bar{F}^{\uparrow}({{i_{{{j}},\max}}})}}`). The mathematics is
explained in . In the absorptivity-emissivity method, the boundary
conditions are included in the solution using the emissivity array. In
the standard formulation used in , this array is only defined for
boundary conditions at the top of the model domain for computational
economy. It is not possible to treat arbitrary flux boundary conditions
inside the domain (e.g.,
:math:`{{\bar{F}^{\downarrow}({{i_{{{j}},\min}}})}}`) using the
emissivity array. However, the flux boundary conditions
:math:`{{\bar{F}^{\downarrow}({{i_{{{j}},\min}}})}}` and
:math:`{{\bar{F}^{\uparrow}({{i_{{{j}},\max}}})}}` are mathematically
equivalent to the fluxes from a single “pseudo” cloud deck above and
below the region, respectively. The pseudo clouds have unit area and
occupy a single model layer. The vertical positions and emissivities of
these clouds are chosen so that the net area-mean fluxes incident on the
top and bottom of the region equal
:math:`{{\bar{F}^{\downarrow}({{i_{{{j}},\min}}})}}` and
:math:`{{\bar{F}^{\uparrow}({{i_{{{j}},\max}}})}}`. With the
introduction of the pseudo clouds, the fluxes inside each
maximum-overlap region can be calculated using the standard
absorptivity-emissivity formulation.

The total upward and downward mean fluxes at a layer :math:`i` within a
maximum-overlap region :math:`{j}` are given by:

.. math::

       {\bar{F}^{\uparrow}(i)} & =  \sum_{{k_{{j}}}= 1}^{n_{{j}}+1} {{\tilde{A}_{{{j}},k_{{j}}}}}{{\bar{F}[{k_{{j}}}]^{\uparrow}(i)}}\nonumber \\
       {\bar{F}^{\downarrow}(i)} & =  \sum_{{k_{{j}}}= 1}^{n_{{j}}+1} {{\tilde{A}_{{{j}},k_{{j}}}}}{{\bar{F}[{k_{{j}}}]^{\downarrow}(i)}}

where :math:`{{\bar{F}[{k_{{j}}}]^{\uparrow}(i)}}` and
:math:`{{\bar{F}[{k_{{j}}}]^{\downarrow}(i)}}` are the upward and
downwelling fluxes for the cloud configuration
:math:`{{\tilde{{{\cal C}}}_{{{j}},k_{{j}}}}}`. The symbols required to
write these fluxes are defined in Table [table:flxsym].

| \|ll\| :math:`\sigma` & Stefan-Boltzmann constant
| :math:`p` & pressure
| :math:`p_t(i)` & pressure at top of layer :math:`i`
| :math:`p_b(i)` & pressure at bottom of layer :math:`i`
  (:math:`p_b(i) > p_t(i)`)
| :math:`T(p)` & temperature at pressure :math:`p`
| :math:`B(p)` & :math:`\sigma\,T^4(p)`
| :math:`{{i_{p,{j}}^{\downarrow}}}` & layer containing pseudo cloud for
  :math:`{{\bar{F}^{\downarrow}({{i_{{{j}},\min}}})}}` b.c.
| :math:`{{i_{p,{j}}^{\uparrow}}}` & layer containing pseudo cloud for
  :math:`{{\bar{F}^{\uparrow}({{i_{{{j}},\max}}})}}` b.c.
| :math:`\epsilon_{cld}(i)` & emissivity of cloud in layer :math:`i`
| :math:`{\epsilon_{p,{j}}(i)}` & emissivity of pseudo clouds at
  :math:`i = {{i_{p,{j}}^{\downarrow}}}` and
  :math:`{{i_{p,{j}}^{\uparrow}}}`
| :math:`{\alpha(p,p')}` & clear-sky absorptivity from pressure
  :math:`p'` to :math:`p`
| :math:`{F_{clr}^\downarrow(i)}` & downwelling clear-sky flux at layer
  :math:`i`
| :math:`{F_{clr}^\uparrow(i)}` & upwelling clear-sky flux at layer
  :math:`i`
| :math:`{t_{{j},{k_{{j}}}}^{\uparrow\downarrow}(i)}` & weights for
  up/downwelling clear-sky flux at layer :math:`i`
| :math:`{T_{{j},{k_{{j}}}}^{\uparrow\downarrow}(i,i')}` & weights for
  up/downwelling flux at layer :math:`i` from cloud at :math:`i'`

The downward and upward fluxes for each configuration can be derived by
iterating the longwave equations from TOA and the surface to the layer
:math:`i`. At each iteration, the solutions are advanced between
successive cloud layers. The final form of the fluxes in configuration
:math:`{{\tilde{{{\cal C}}}_{{{j}},k_{{j}}}}}` is:

.. math::

      {{\bar{F}[{k_{{j}}}]^{\uparrow}(i)}}& =  {F_{clr}^\uparrow(i)}{t_{{j},{k_{{j}}}}^{\uparrow}(i)} + \\
              & \sum_{i' = i}^N
                    \{ B(p_t(i')) -
                            \int_{p_t(i)}^{p_t(i')}{\alpha(p_t(i),p')}
                            {dB(p') \over dp'} dp' \}
                            {T_{{j},{k_{{j}}}}^{\uparrow}(i,i')} \nonumber \\
      {{\bar{F}[{k_{{j}}}]^{\downarrow}(i)}}& =  {F_{clr}^\downarrow(i)}{t_{{j},{k_{{j}}}}^{\downarrow}(i)} + \\
              & \sum_{i' = 1}^i
                    \{ B(p_b(i')) +
                            \int_{p_b(i')}^{p_b(i)}{\alpha(p_b(i),p')}
                            {dB(p') \over dp'} dp' \}
                            {T_{{j},{k_{{j}}}}^{\downarrow}(i,i')} \nonumber
      

The clear-sky and cloudy-sky weights are:

.. math::

       {t_{{j},{k_{{j}}}}^{\uparrow}(i)} & =  \prod_{l = i}^N [1-{{\tilde{\epsilon}_{{{j}},k_{{j}}}(l)}}] \\
       {t_{{j},{k_{{j}}}}^{\downarrow}(i)} & =  \prod_{l = 1}^i [1-{{\tilde{\epsilon}_{{{j}},k_{{j}}}(l)}}]
       \\ {T_{{j},{k_{{j}}}}^{\uparrow}(i,i')} & =  {{\tilde{\epsilon}_{{{j}},k_{{j}}}(i')}}\prod_{l = i}^{i'-1}
       [1-{{\tilde{\epsilon}_{{{j}},k_{{j}}}(l)}}]\\ {T_{{j},{k_{{j}}}}^{\downarrow}(i,i')} & = 
       {{\tilde{\epsilon}_{{{j}},k_{{j}}}(i')}}\prod_{l = i'+1}^{i} [1-{{\tilde{\epsilon}_{{{j}},k_{{j}}}(l)}}]\\
       {{\tilde{\epsilon}_{{{j}},k_{{j}}}(l)}} & =  \{ \begin{array}{ll}
                                \epsilon_{cld}(l){{\tilde{{{\cal C}}}_{{{j}},k_{{j}}}}}(l) & \mbox{if
                                    ${{i_{{{j}},\min}}}\le l \le {{i_{{{j}},\max}}}$} \\
                                {\epsilon_{p,{j}}({{i_{p,{j}}^{\downarrow}}})} & \mbox{if $l = {{i_{p,{j}}^{\downarrow}}}$} \\
                                {\epsilon_{p,{j}}({{i_{p,{j}}^{\uparrow}}})} & \mbox{if $l = {{i_{p,{j}}^{\uparrow}}}$} \\ 0
                                 & \mbox{otherwise}
                                \end{array} .

The longwave atmospheric heating rate is obtained from

.. math::

   Q_{\ell w} (p_k) = \frac{g}{c_p} \frac{{\bar{F}^{\uparrow}(k+1)} -
   {\bar{F}^{\downarrow}(k+1)} - {\bar{F}^{\uparrow}(k)} +
   {\bar{F}^{\downarrow}(k)}}{p_{k+1} - p_k} . 

which is added to the nonlinear term :math:`(Q)` in the thermodynamic
equation.

The full calculation of longwave radiation (which includes heating rates
as well as boundary fluxes) is computationally expensive. Therefore,
modifications to the longwave scheme were developed to improve its
efficiency for the diurnal framework. For illustration, consider the
clear-sky fluxes defined in ([4.b.34]) and ([4.b.35]). Well over 90% of
the longwave computational cost involves evaluating the absorptivity
:math:`\alpha` and emissivity :math:`\epsilon`. To reduce this
computational burden, :math:`\alpha` and :math:`\epsilon` are computed
at a user defined frequency that is set to every 12 model hours in the
standard configuration, while longwave heating rates are computed at the
diurnal cycle frequency of once every model hour.

Calculation of :math:`\alpha` and :math:`\epsilon` with a period longer
than the evaluation of the longwave heating rates neglects the
dependence of these quantities on variations in temperature, water
vapor, and ozone. However, variations in radiative fluxes due to changes
in cloud amount are fully accounted for at each radiation calculation,
which is regarded to be the dominant effect on diurnal time scales. The
dominant effect on the heating rates of changes in temperature occurs
through the Planck function and is accounted for with this method.

The continuous equations for the longwave calculations require a
sophisticated vertical finite–differencing scheme due to the integral
term :math:`\int \alpha dB` in Equations ([4.b.34])–([4.b.35]). The
reason for the additional care in evaluating this integral arises from
the nonlinear behavior of :math:`\alpha` across a given model layer. For
example, if the flux at interface :math:`p_k` is required, an integral
of the form :math:`\int^{p_k}_{p_s} \alpha (p', p_k) dB(p')` must be
evaluated. For the nearest layer to level :math:`p_k`, the following
terms will arise:

.. math::

   \int^{p_k}_{p_{k+1}} {\alpha (p', p_k) dB (p')} = \frac{ [ \alpha
   (p_{k+1}, p_k) + \alpha(p_k, p_k) ]}{2}  [B(p_k) -
   B(p_{k+1})  ] , 

employing the trapezoidal rule. The problem arises with the second
absorptivity :math:`\alpha (p_k, p_k)`, since this term is zero. It is
also known that :math:`\alpha` is nearly exponential in form within a
layer. Thus, to accurately account for the variation of
:math:`\alpha (p,p')` across a layer, many more grid points are required
than are available in . The nearest layer must, therefore, be subdivided
and :math:`\alpha` must be evaluated across the subdivided layers. The
algorithm that is employed in is to use a trapezoid method for all
layers the nearest layer. For the nearest layer a subdivision, as
illustrated in Figure [figure:3], is employed.

.. figure:: figures/figure4-2
   :alt: [figure:3]Subdivision of model layers for radiation flux
   calculation

[figure:3]Subdivision of model layers for radiation flux calculation

For the upward flux, the nearest layer contribution to the integral is
evaluated from

.. math::

   \int^{p^{k+1}_H}_{p^k_H} \alpha dB(p') = \alpha_{22}
   [B(p^{k+1}_H) - B(p^k) ] + \alpha_{21} [B(p^k) -
   B(p^k_H) ] , 

while for the downward flux, the integral is evaluated according to

.. math::

   \int^{p^k_H}_{p^{k+1}_H} \alpha dB(p') = \alpha_{11} [B (p^k) -
   B(p^k_H) ] + \alpha_{12} [B(p^{k+1}_H) - B(p^k) ] .
   

The :math:`\alpha_{ij},\; i = 1, 2;\; j = 1, 2,` are absorptivities
evaluated for the subdivided paths shown in Figure [figure:3]. The
path–length dependence for the absorptivities arises from the dependence
on the absorptance :math:`A(p,p')` [*e.g.,* Eq. ([4.b.155])].
Temperatures are known at model levels. Temperatures at layer interfaces
are determined through linear interpolation in :math:`\log p` between
layer midpoint temperatures. Thus, :math:`B(p_k) = \sigma_B T^4_k` can
be evaluated at all required levels. The most involved calculation
arises from the evaluation of the fraction of layers shown in
Figure [figure:3]. In general, the absorptance of a layer can require
the evaluation of the following path lengths:

.. math::

   \xi (p_k, p_{k+1}) & = f(\overline {T}) \overline {p} \Delta p ,
    \\[-1.0em] \intertext{and}\nonumber\\[-2.0em] u(p_k,
   p_{k+1}) & = g (\overline {T}) \Delta p,  \\[-1.0em]
   \intertext{and}\nonumber\\[-2.0em] \beta (p_k, p_{k+1}) & = h
   (\overline {T}) \overline {p} , 

where :math:`f,\; g,` and :math:`h` are functions of temperature due to
band parameters (see , and :math:`\overline {T}` is an absorber
mass–weighted mean temperature.

These path lengths are used extensively in the evaluation of
:math:`A_{O_3}` and :math:`A_{CO_2}` and the trace gases. But path
lengths dependent on both :math:`p^2` (:math:`\xi`) and :math:`p`
(:math:`u`) are also needed in calculating the water–vapor absorptivity,
:math:`\alpha_{H_2O}` . To account for the subdivided layer, a
fractional layer amount must be multiplied by :math:`\xi` and :math:`u`,

.. math::

   \overline {\xi}_{11} & = \xi (p^k_H p^{k+1}_H) \times UINPL (1,k) ,
    \\ \overline {u}_{11} & = u(p^k_H, p^{k+1}_H) \times
   WINPL (1,k) ,
    \\[-1.0em]
   \intertext{and} \nonumber\\[-2.0em] \overline {\beta}_{11} & = \beta
   (p^k_H, p^{k+1}_H) \times PINPL (1,k) , 

where :math:`UINPL`, :math:`WINPL`, and :math:`PINPL` are factors to
account for the fractional subdivided layer amount. These quantities are
derived for the case where the mixing ratio is assumed to be constant
within a given layer (CO:math:`_2` and H\ :math:`_2`\ O). For ozone, the
mixing ratio is assumed to interpolate linearly in physical thickness;
thus, another fractional layer amount :math:`ZINPL` is required for
evaluating :math:`A_{O_3}(p,p')` across subdivided layers.

Consider the subdivided path for :math:`\alpha_{22}`; the total path
length from :math:`p^k_H` to :math:`p^{k+1}_H` for the :math:`p^2` path
length will be

.. math::

   \xi (p^k_H, p^{k+1}_H) \approx \overline{p}_H [p^k_H - p^{k+1}_H
   ] , 

where :math:`\overline {p}_H \equiv \frac{p^k_H + p^{k+1}_H}{2}`. The
layer path length is, therefore, proportional to

.. math::

   \xi (p^k_H, p^{k+1}_H) \approx \frac{1}{2} ((p^{k}_{H})^{2}
   - ( p^{k+1}_{H})^{2}).  

The path length :math:`\xi` for :math:`\alpha_{22}` requires the mean
pressure

.. math::

   \overline {p}_{22} &\approx \frac{1}{2}  \{ \frac{p^k +
   p^{k+1}_H}{2} + p^{k+1}_H  \} ,  \\
   \intertext{and the pressure difference}\nonumber\\[-2.0em] \Delta
   p_{22} &\approx \frac{p^k + p^{k+1}_H}{2} - p^{k+1}_H
   . 

 Therefore, the path :math:`\xi_{22}` is

.. math::

   \xi_{22} \approx \overline {p}_{22}\; \Delta p_{22} = \frac{1}{2}
    \{ ( \frac{p^k + p^{k+1}_H}{2} )^2 - ( p^{k+1}_H
   )^2  \} .  

The fractional path length is obtained by normalizing this by
:math:`\xi
(p^k_H, p^{k+1}_H)`,

.. math::

   UINPL (2,k) & = DAF3(k)  \{ ( \frac{p^k + p^{k+1}_H}{2}
    )^2 - ( p^{k+1}_H )^2  \} ,
   \\[-1.0em] \intertext{where}\nonumber\\[-2.0em] DAF3(k)
   & = \frac{1}{( p^{k}_{H} )^2 - ( p^{k+1}_{H})^2}
   . 

Similar reasoning leads to the following expressions for the remaining
fractional path lengths, for :math:`\alpha_{21}`,

.. math::

   UINPL (3,k) & = DAF3(k)  \{ ( \frac{p^k + p^k_H}{2} )^2
   - ( p^{k+1}_{H} )^2  \} , \\
   \intertext{for $\alpha_{11},$}\nonumber\\[-2.0em] UINPL (1,k) & =
   DAF3(k)  \{ (p^k_H )^2 - ( \frac{p^k + p^k_H}{2}
   )^2  \} ,  \\ \intertext{and for
   $\alpha_{12}$,}\nonumber\\[-2.0em] UINPL (4,k) & = DAF3(k)  \{
   (p^{k}_{H})^2 - ( \frac{p^k + p^{k+1}_H}{2} )^2
    \} . 

The :math:`UINPL` are fractional layer amounts for path length that
scale as :math:`p^2`, *i.e.,* :math:`\overline {\xi}_{ij}`.

For variables that scale linearly in :math:`p`,
:math:`\overline {u}_{ij}`, the following fractional layer amounts are
used:

.. math::

   WINPL (1,k) & = DAF4 (k) \{ \frac{p^k_H - p^k}{2}  \},
    \\ WINPL (2,k) & = DAF4 (k)  \{ \frac{p^k -
   p^{k+1}_H}{2}  \},  \\ WINPL (3,k) & = DAF4 (k)
    \{  ( \frac{p^k_H + p^k}{2} ) - p^{k+1}_H  \},
    \\[1ex] WINPL (4,k) & = DAF4 (k)  \{ p^k_H -
    ( {p^{k+1}_H + p^k}{2}  )  \} ,
   \\[-1.0em] \intertext{where}\nonumber\\[-2.0em] DAF4(k)
   & = \frac{1}{p^k_H - p^{k+1}_H} .  

These fractional layer amounts are directly analogous to the
:math:`UINPL,` but since :math:`\overline {u}` is linear in :math:`p`,
the squared terms are not present.

The variable :math:`\overline {\beta}_{ij}` requires a mean pressure for
the subdivided layer. These are

.. math::

   PINPL (1,k) & = \frac{1}{2}  \{ \frac{p^k + p^k_H}{2} + p^k_H
    \} ,  \\ PINPL (2,k) & = \frac{1}{2}  \{
   \frac{p^k + p^{k+1}_H}{2} + p^{k+1}_h  \} ,  \\
   PINPL (3,k) & = \frac{1}{2}  \{ \frac{p^k + p^k_H}{2} + p^{k+1}_H
    \} ,  \\ PINPL (4,k) & = \frac{1}{2}  \{
   \frac{p^k + p^{k+1}_H}{2} + p^k_H  \} . 

Finally, fractional layer amounts for ozone path lengths are needed,
since ozone is interpolated linearly in physical thickness. These are
given by

.. math::

   ZINPL (1,k) & = \frac{1}{2} \frac{\ln  ( \frac{p^k_H}{p_k} 
   )}{\ln  ( \frac{p^k_H}{p^{k+1}_H}  )} ,  \\
   ZINPL (2,k) & = \frac{1}{2} \frac{\ln  ( \frac{p^k}{p^{k+1}_H}
   )} {\ln ( \frac{p^k_H}{p^{k+1}_H} ) },
    \\ ZINPL (3,k) & = ZINPL (1,k) + 2 ZINPL (2,k),
    \\[1ex] ZINPL (4,k) & = ZINPL (2,k) + 2 ZINPL (1,k)
   . 

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
over ocean follows from , and the surface exchange over sea ice is
discussed in the sea-ice model documentation. Over lakes, exchanges are
computed by a lake model embedded in the land surface model described in
the following section.

Land
~~~~

In , the NCAR Land Surface Model (LSM) has been replaced by the
Community Land Model CLM2 . This new model includes components treating
hydrological and biogeochemical processes, dynamic vegetation, and
biogeophysics. Because of the increased complexity of this new model and
since a complete description is available online, users of interested in
CLM should consult this documentation at . A discussion is provided here
only of the component of CLM which controls surface exchange processes.

Land surface fluxes of momentum, sensible heat, and latent heat are
calculated from Monin-Obukhov similarity theory applied to the surface
(i.e. constant flux) layer. The zonal :math:`\tau_x` and meridional
:math:`\tau_y` momentum fluxes
(kg m:math:`{}^{-1}`\ s\ :math:`{}^{-2}`), sensible heat :math:`H`
(W m:math:`{}^{-2}`) and water vapor :math:`E`
(kg m:math:`{}^{-2}`\ s\ :math:`{}^{-1}`) fluxes between the surface and
the lowest model level :math:`z_1` are:

.. math::

   {3}
   \tau_x & = - \rho_1 \overline {(u'w')} & & = - \rho_1 u_*^2 (u_1 /V_a )
   && = \rho_1 \frac{{u_s - u_1 }}{{r_{am} }} \\ \tau_y & = - \rho_1
   \overline {(v'w')} & & = - \rho_1 u_*^2 (v_1 /V_a ) && = \rho_1
   \frac{{v_s - v_1 }}{{r_{am} }} \\ H & = \phantom{-}\rho_1 c_p
   (\overline {w'\theta '} )& & = - \rho_1 c_p u_* \theta_* && = \rho_1 c_p
   \frac{{\theta_{s} - \theta_1 }} {{r_{ah} }} \\ E & = \phantom{-}\rho_1
   (\overline {w'q'} )& & = - \rho_1 u_* q_* && = \rho_1 \frac{{q_{s} - q_1
   }}{{r_{aw} }}

.. math::

   r_{am} & = V_a /u_*^2 \\ r_{ah} & = (\theta_1 - \theta_s )/u_* \theta_*
   \\ r_{aw} & = (q_1 - q_s )/u_* q_*

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
:math:`q_s =
q_{af}`, where :math:`T_{af}` and :math:`q_{af}` are the air temperature
and specific humidity within canopy space. For the non-vegetated
fraction, :math:`\theta_s = T_g` and :math:`q_s = q_g`, where
:math:`T_g` and :math:`q_g` are the air temperature and specific
humidity at ground surface. These terms are described by .

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
relation from can be used :

.. math::

   \ln \frac{{z_{0m} }} {{z_{0h} }} & = a( {\frac{{u_* z_{0m} }}
   {\nu }} )^{0.45} \\ a & = 0.13 \\ \nu & = 1.5 \times 10^{ - 5}
   {\text{m}}^2 {\text{s}}^{-1}

Over canopy, the application of energy balance

.. math:: R_n - H - L_v\,E = 0

(where :math:`R_n` is the net radiation absorbed by the canopy) is
equivalent to the use of different :math:`z_{0m}` versus :math:`z_{0h}`
over bare soil, and hence thermal roughness is not needed over canopy .

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

   \theta_v = \theta_1 (1 + 0.61q_1 ) = T_a ( {\frac{{p_s }} {{p_l}}} )^{R/c_p } (1 + 0.61q_1 )

where :math:`T_1` and :math:`q_1` are the air temperature and specific
humidity at height :math:`z_1` respectively, :math:`\theta_1` is the
atmospheric potential temperature, :math:`p_l` is the atmospheric
pressure, and :math:`p_s` is the surface pressure. The surface friction
velocity :math:`u_*` is defined by

.. math:: u_*^2 = [\overline {u'w'}^2 + \overline {v'w'}^2 ]^{1/2}

The temperature scale :math:`\theta_*` and :math:`\theta_{ * v}` and a
humidity scale :math:`q_*` are defined by

.. math::

   \theta_* & = - \overline {w'\theta '} /u_* \\ q_* & = - \overline {w'q'}
   /u_* \\ \theta_{v * } & = - \overline {w'\theta '_v } /u_* \nonumber \\
   & \approx - (\overline {w'\theta '} + 0.61\overline \theta \overline
   {w'q'} )/u_* \\ & = \theta_* + 0.61\overline \theta q_* \nonumber

(where the mean temperature :math:`\overline \theta` serves as a
reference temperature in this linearized form of :math:`\theta_v` ).

The stability parameter is defined as

.. math:: \varsigma = \frac{{z_1 - d}}{L}\quad ,

with the restriction that :math:`- 100 \leqslant \varsigma \leqslant 2`.
The scalar wind speed is defined as

.. math::

   V_a^2 & = u_1^2 + v_1^2 + U_c^2 \\ U_c & = \{ \begin{array}{ll}
     0.1\>{\text{ms}}^{-1} & {\text{, if }}\varsigma \geqslant {\text{0
     (stable)}} \hfill \\ \beta w_* = \beta ( {z_i \frac{g}
   {{\theta_v }}\theta_{v * } u_*} )^{1/3} & {\text{, if
   }}\varsigma < {\text{0 (unstable)}}\,. \hfill \\
   \end{array}  .

Here :math:`w_*` is the convective velocity scale, :math:`z_i` is the
convective boundary layer height, and :math:`\beta` = 1. The value of
:math:`z_i` is taken as 1000 m

The flux-gradient relations are given by:

.. math::

   \frac{{k(z_1 - d)}} {{\theta_* }}\frac{{\partial \theta }} {{\partial
   z}} & = \phi_h (\varsigma ) \\ \frac{{k(z_1 - d)}} {{q_*
   }}\frac{{\partial q}} {{\partial z}} & = \phi_q (\varsigma ) \\
   \phi_h & = \phi_q \\
     \phi_m (\varsigma ) & =
               \{\begin{array}{ll} (1 - 16\varsigma )^{ - 1/4} &
                                        \mbox{for}~\varsigma < 0 \\ 1 +
                                        5\varsigma & \mbox{for}~0 <
                                        \varsigma < 1
               \end{array}. \\
     \phi_h (\varsigma ) & =
               \{\begin{array}{ll} (1 - 16\varsigma )^{ - 1/2} &
                                        \mbox{for}~\varsigma < 0 \\ 1 +
                                        5\varsigma & \mbox{for}~0 <
                                        \varsigma < 1
               \end{array}.

Under very unstable conditions, the flux-gradient relations are taken
from :

.. math::

   \phi_m & = 0.7k^{2/3} ( - \varsigma )^{1/3} \\ \phi_h & = 0.9k^{4/3} (- \varsigma )^{ - 1/3}

To ensure the functions :math:`\phi_m (\varsigma )` and
:math:`\phi_h (\varsigma)` are continuous, the simplest approach (i.e., without considering any
transition regions) is to match the above equations at
:math:`\varsigma_m = - 1.574` for :math:`\phi_m (\varsigma )` and :math:`\varsigma_h = -0.465` for :math:`\phi_h (\varsigma )` .

Under very stable conditions (i.e., :math:`\varsigma > 1` ), the relations are taken from :

.. math:: \phi_m = \phi_h = 5 + \varsigma

Integration of the wind profile yields:

.. math::
   :label: windprof

   {2}V_a           & = \frac{{u_* }} {k}f_M (\varsigma )  \\ 
   f_M (\varsigma ) & = \{ {[ {\ln ( {\frac{{\varsigma_m L}}
                         {{z_{0m} }}} ) - \psi_m (\varsigma_m )} ] + 1.14[( -
                         \varsigma )^{1/3} - ( - \varsigma_m )^{1/3} ]} \}\,, \varsigma < \varsigma_m = - 1.574 \\ 
   f_M (\varsigma ) & = [ {\ln ( {\frac{{z_1 - d}} {{z_{0m} }}} ) - \psi_m  (\varsigma ) + \psi_m ( {\frac{{z_{0m} }} {L}} )}]\,, 
                        \varsigma_m < \varsigma < 0 \\
   f_M (\varsigma ) & = [ {\ln ( {\frac{{z_1 - d}} {{z_{0m} }}}) + 5\varsigma } ]\,,  0 < \varsigma < 1  \\ 
   f_M (\varsigma ) & = \{ {[ {\ln ( {\frac{L} {{z_{0m} }}} ) + 5} ] + [5\ln (\varsigma ) + \varsigma - 1]} \}\,,  \varsigma > 1
                       
Integration of the potential temperature profile yields:

.. math::
   :label: tprof

   {2}\theta_1 - \theta_s & = \frac{{\theta_* }} {k}f_T (\varsigma ) \\ 
   f_T (\varsigma )  & = \{ {[ {\ln ({\frac{{\varsigma_h L}} {{z_{0h} }}} ) - \psi_h (\varsigma_h )}] 
                          + 0.8[( - \varsigma_h )^{ - 1/3} - ( - \varsigma )^{ - 1/3} ]}\}\,, \varsigma < \varsigma_h = - 0.465 \\ 
   f_T (\varsigma )  & = [ {\ln ({\frac{{z_1 - d}} {{z_{0h} }}} ) - \psi_h (\varsigma ) + \psi_h
                         ( {\frac{{z_{0h} }} {L}} )} ] \,,  \varsigma_h < \varsigma < 0  \\ 
   f_T (\varsigma )  & = [{\ln ( {\frac{{z_1 - d}} {{z_{0h} }}} ) + 5\varsigma }] \,,  0  < \varsigma < 1  \\ 
   f_T (\varsigma )  & = \{ {[ {\ln ( {\frac{L} {{z_{0h} }}}) + 5} ] + [5\ln (\varsigma ) + \varsigma - 1]} \} \,,  \varsigma > 1 

The expressions for the specific humidity profiles are the same as those
for potential temperature except that (:math:`\theta_1 - \theta_s` ),
:math:`\theta_*` and :math:`z_{0h}` are replaced by (:math:`q_1 - q_s`), 
:math:`q_*` and :math:`z_{0q}` respectively. The stability functions
for :math:`\varsigma < 0` are

.. math::

   \psi_m & = 2\ln( {\frac{{1 + \chi }}{2}} ) + \ln({\frac{{1 + \chi^2 }}{2}} ) - 2\tan^{ - 1} \chi + \frac{\pi }{2} \\ 
   \psi_h & = \psi_q = 2\ln( {\frac{{1 + \chi^2 }}{2}} ) \\
   \intertext{where} \chi & = (1 - 16\varsigma )^{1/4}

Note that the CLM code contains extra terms involving :math:`z_{0m}/\varsigma`, :math:`z_{0h} /\varsigma`, and :math:`z_{0q} /\varsigma`
for completeness. These terms are very small most of the time and hence
are omitted in Eqs. [eq:windprof] and [eq:ptprof].

In addition to the momentum, sensible heat, and latent heat fluxes, land
surface albedos and upward longwave radiation are needed for the
atmospheric radiation calculations. Surface albedos depend on the solar
zenith angle, the amount of leaf and stem material present, their
optical properties, and the optical properties of snow and soil. The
upward longwave radiation is the difference between the incident and
absorbed fluxes. These and other aspects of the land surface fluxes have
been described by .

Ocean
~~~~~

The bulk formulas used to determine the turbulent fluxes of momentum
(stress), water (evaporation, or latent heat), and sensible heat into
the atmosphere over ocean surfaces are

.. math::
   :label:

   ( \mathbf{\tau}, E, H) = \rho_A |\Delta\,{{\mathbf{v}}}|(C_D
         \Delta\,{{\mathbf{v}}}, C_E \Delta\,q, C_p C_H \Delta\theta),
         

where :math:`\rho_A` is atmospheric surface density and :math:`C_p` is
the specific heat. Since does not allow for motion of the ocean surface,
the velocity difference between surface and atmosphere is
:math:`\Delta\,{{\mathbf{v}}}= {{\mathbf{v}}}_A`, the velocity of
the lowest model level. The potential temperature difference is
:math:`\Delta\theta =
\theta_A - T_s`, where :math:`T_s` is the surface temperature. The
specific humidity difference is :math:`\Delta\,q = q_A - q_s(T_s)`,
where :math:`q_s(T_s)` is the saturation specific humidity at the
sea-surface temperature.

In ([eqn:turb1]), the transfer coefficients between the ocean surface
and the atmosphere are computed at a height :math:`Z_A` and are
functions of the stability, :math:`\zeta`:

.. math::
   :label:

   C_{(D,E,H)} = \kappa^2 {[\ln(\frac{Z_A}{Z_{0m}}) - \psi_m]}^{-1}
                          {[\ln(\frac{Z_A}{Z_{0(m,e,h)}}) - \psi_{(m,s,s)}]}^{-1}
   
where :math:`\kappa = 0.4` is von Kármán’s constant and
:math:`Z_{0(m,e,h)}` is the roughness length for momentum, evaporation,
or heat, respectively. The integrated flux profiles, :math:`\psi_m` for
momentum and :math:`\psi_s` for scalars, under stable conditions
(:math:`\zeta >
0`) are

.. math:: \psi_m(\zeta) = \psi_s(\zeta) = -5 \zeta. 

For unstable conditions (:math:`\zeta < 0`), the flux profiles are

.. math::
   :label:

   \psi_m(\zeta) = 2 \ln[0.5(1 + X)] + \ln[0.5(1 + X^2 )] \nonumber - 2 \tan^{-1} X + 0.5 \pi,  \\ 
   \psi_s(\zeta) = 2 \ln[0.5(1 + X^2 )],  \\ 
   X = (1 - 16 \zeta)^{1/4}  . 

 The stability parameter used in ([eqn:turb3])–([eqn:turb6]) is

.. math::
   :label:

   \zeta = \frac{\kappa\,g\,Z_A}{u^{\*2}}(\frac{\theta^*}{\theta_v} + \frac{Q^*}{(\epsilon^{-1} + q_A)}),
   

where the virtual potential temperature is
:math:`\theta_v = \theta_A(1 +
\epsilon q_A)`; :math:`q_A` and :math:`\theta_A` are the lowest level
atmospheric humidity and potential temperature, respectively; and
:math:`\epsilon =
0.606`. The turbulent velocity scales in ([eqn:turb7]) are

.. math::
   :label:

   u^* = C_D^{1/2} |\Delta\,{{\mathbf{v}}}|, \nonumber\\ (Q^*,\theta^*) = C_{(E,H)}\frac{|\Delta\,{{\mathbf{v}}}|}{u^*}
   (\Delta\,q,\Delta\theta). 

Over oceans, :math:`Z_{0e} = 9.5 \times 10^{-5}` m under all conditions
and :math:`Z_{0h} = 2.2 \times 10^{-9}` m for :math:`\zeta > 0`,
:math:`Z_{0h} = 4.9 \times
10^{-5}` m for :math:`\zeta \le 0`, which are given in . The momentum
roughness length depends on the wind speed evaluated at 10 m as

.. math::
   :label:

   Z_{om} & = 10\,\exp[-\kappa{(\frac{c_4}{U_{10}} + c_5 + c_6\,U_{10})}^{-1}]\,, \nonumber\\
   U_{10} & = U_A {[1 + \frac{\sqrt{C_{10}^N}}{\kappa}\ln(\frac{Z_A}{10} - \psi_m)]}^{-1}\,, 

where :math:`c_4 = 0.0027`  m s\ :math:`{}^{-1}`,
:math:`c_5 = 0.000142`, :math:`c_6 =
0.0000764` m:math:`{}^{-1}` s, and the required drag coefficient at 10-m
height and neutral stability is
:math:`C^{N}_{10} = c_4 U^{-1}_{10} + c_5 + c_6 U_{10}` as given by .

The transfer coefficients in ([eqn:turb1]) and ([eqn:turb2]) depend on
the stability following ([eqn:turb3])–([eqn:turb6]), which itself
depends on the surface fluxes ([eqn:turb7]) and ([eqn:turb8]). The
transfer coefficients also depend on the momentum roughness, which
itself varies with the surface fluxes over oceans ([eqn:turb9]). The
above system of equations is solved by iteration.

Sea Ice
~~~~~~~

The fluxes between the atmosphere and sea ice are described in detail in
the sea-ice model documentation.

Vertical Diffusion and Boundary Layer Processes
-----------------------------------------------

The vertical diffusion parameterization in  provides the interface to
the turbulence parameterization, computes the molecular diffusivities
(if necessary) and finally computes the tendencies of the input
variables. The diffusion equations are actually solved implicitly, so
the tendencies are computed from the difference between the final and
initial profiles.

In the near future, the gravity wave parameterization will also be
called from within the vertical diffusion. This will allow the turbulent
and, especially, the molecular diffusivity to be passed to the gravity
wave parameterization to damp vertically propagating waves. The gravity
wave parameterization may return additional diffusivities and tendencies
to be applied before the actual diffusion is applied.

As in CCM2 and CCM3, the turbulence parameterization in  includes
computation of diffusivities for the free atmosphere, based on the
gradient Richardson number, and an explicit, non-local Atmospheric
Boundary Layer (ABL) parameterization. The ABL parameterization includes
a determination of the boundary layer depth. In practice, the free
atmosphere diffusivities are calculated first at all levels. The ABL
scheme then determines the ABL depth and diffusivities and replaces the
free atmosphere values for all levels within the ABL, returning both the
updated diffusivities and the non-local transport terms. The
implementation of the ABL parameterization in CCM2 is discussed in ,
while the formalism only is discussed here. Following the ABL scheme,
molecular diffusivities are computed if the model top extends above
:math:`\sim`\ 90 km (0.1 Pa).

As described in , a general vertical diffusion parameterization can be
written in terms of the divergence of diffusive fluxes:

.. math::
   :label:

   \frac{\partial}{\partial t} (u,v,q) & = - \frac{1}{\rho} \frac{\partial}{\partial z} (F_u, F_v, F_q) \\
   \frac{\partial}{\partial t} s       & = - \frac{1}{\rho} \frac{\partial}{\partial z} F_H + D 

where :math:`s = c_p T + g z` is the dry static energy, :math:`z` is the
geopotential height above the local surface (does not include the
surface elevation) and :math:`D` is the heating rate due to the
dissipation of resolved kinetic energy in the diffusion process. The
diffusive fluxes are defined as:

.. math::
   :label:

   F_{u,v} & =-\rho K_m \frac{\partial}{\partial z}(u,v),  \\
   F_{q,H} & =-\rho K_{q,H} \frac{\partial}{\partial z}(q,s) +\rho K_{q,H}^t\gamma_{q,H} . 

The viscosity :math:`K_m` and diffusivities :math:`K_{q,H}` are the
sums of: turbulent components :math:`K_{m,q,H}^t`, which dominate below
the mesopause; and molecular components :math:`K_{m,q,H}`, which
dominate above  120 km. The turbulent diffusivities are the sum of two
components, free atmosphere and boundary layer diffusivities, defined
below. In the future, these terms also may include effective
diffusivities from the gravity wave parameterization. The non-local
transport terms :math:`\gamma_{q,H}` are given by the ABL
parameterization. Note that :math:`F_q`, as defined in ([eq:fluxz2]) and
implemented in , does not include the term which causes diffusive
separation of constituents of differing molecular weights. The molecular
diffusion in   is currently incomplete and should be used with caution.
The molecular viscosity and diffusivities are all currently defined as
:math:`3.55\times
10^{-7} T^{2/3}/\rho`. A more complete form, allowing separation of
constituents, will be implemented later.

The kinetic energy dissipation term :math:`D` in ([eq:contz3]) is
determined by forming the equation for total energy from
([eq:contz1]–[eq:contz3]):

.. math::
   :label:

   \frac{\partial E}{\partial t}
      & = u\frac{\partial u}{\partial t} + v\frac{\partial v}{\partial t}
          + \frac{\partial s}{\partial t} \\
      & = -\frac{1}{\rho} (u\frac{\partial F_u}{\partial z} +
          v\frac{\partial F_v}{\partial z} + \frac{\partial F_H}{\partial  z} ) + D \\ 
      & = -\frac{1}{\rho} (\frac{\partial F_{KE}}{\partial z} + \frac{\partial F_H}{\partial z}).

The diffusive kinetic energy flux in ([eq:energy2]) is

.. math:: 
   :label:

   F_{KE} \equiv u F_u + v F_v

and the kinetic energy dissipation is

.. math::
   :label:

   D \equiv -\frac{1}{\rho} ( F_u\frac{\partial u}{\partial z} +  F_v\frac{\partial v}{\partial z} ). 

To show that :math:`D` is positive definite, we use ([eq:fluxz1]) to
expand for :math:`F_u` and :math:`F_v`:

.. math::
   :label:

   D = (K_m^t + K_m^m) [ (\frac{\partial u}{\partial
                          z})^2 +(\frac{\partial v}{\partial
                          z})^2 ] \ge 0.  

We show that energy is conserved in the column by integrating
([eq:energy2]) in the vertical, from the surface (:math:`z=0`), to the
top of the model (:math:`z={z_{top}}`):

.. math::
   :label:

   \int_0^{z_{top}} \rho\frac{\partial E}{\partial t} dz = (F_{KE} + F_H)\vert_{z_{top}}^0.

Therefore, the vertically integrated energy will only change because of
the boundary fluxes of energy, of which only the surface heat flux,
:math:`F_H(z=0)`, is usually nonzero. It is typically assumed that the
surface wind vanishes, even over oceans and sea ice, giving
:math:`F_{KE}(z=0)=0`. Then, the surface stress :math:`F_{u,v}(z=0)`
does not change the total energy in the column, but does result in
kinetic energy dissipation and heating near the surface (see below) For
coupled models, nonzero surface velocities can be accommodated by
including :math:`F_{KE}` on both sides of the surface interface.

Free atmosphere turbulent diffusivities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The free atmospheric turbulent diffusivities are typically taken as
functions of length scales :math:`\ell_c` and local vertical gradients
of wind and virtual potential temperature,

.. math:: 
   :label:

   K_c = {{\ell_c}^2 S F_c(Ri)} . 

Here :math:`S` is the local shear, defined by

.. math::
   :label:

   S = \frac{\partial {\mathbf{V}}{\partial z} ,
   

and the mixing length :math:`\ell_c` is generally given by

.. math:: 
   :label:

   \frac{1}{\ell_c} = \frac{1}{k z} + \frac{1}{\lambda_c}, 

where :math:`k` is the Von Karman constant, and :math:`\lambda_c` is
the so-called asymptotic length scale, taken to be 30 m above the ABL.
Since the lowest model level is always greater than 30 m in depth,
:math:`\ell_c` is simply set to 30 m in . Furthermore, :math:`F_c(Ri)`
denotes a functional dependence of :math:`K_c` on the gradient
Richardson number:

.. math::
   :label:

   Ri = \frac{g}{\theta_v} \frac{\partial \theta_v / \partial z}{S^2},
             
 where :math:`\theta_v` is the virtual potential temperature,

.. math::
   :label:

   \theta_v = \theta [ 1 + ( \frac{R_v}{R} -1 ) q ]  . 

For simplicity, in the free atmosphere, we specify the same stability
functions :math:`F_c` for all :math:`c`. For unstable conditions
:math:`(Ri < 0)` we choose

.. math::
   :label:

   F_c(Ri)         & = {( 1 - 18 Ri )^{1/2}} ,  \\
   \intertext{and for stable conditions $(Ri > 0)$ we use. }\nonumber\\
   [-2.0em] F_c(Ri) & =\frac{1} {1 + 10 Ri(1 + 8 Ri )} , 

This means that no distinction is made between turbulent vertical
diffusion of heat, scalars and momentum outside the boundary layer.
However, separate coefficient arrays are maintained and other
parameterizations (such as gravity wave drag) may provide distinct
diffusivities. We also note the the turbulent diffusivity is the same
for all constituents, even within the ABL. However, the molecular
diffusivities differ for each constituent since they depend on it’s
molecular weight.

“Non-local” atmospheric boundary layer scheme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The free atmosphere turbulent diffusivities, described above, are an
example of the local diffusion approach. In such an approach, the
turbulent flux of a quantity is proportional to the local gradient of
that quantity (([eq:fluxz1])–([eq:fluxz2])). In addition, the eddy
diffusivity depends on local gradients of mean wind and mean virtual
temperature (see ([4.d.9])). These are reasonable assumptions when the
length scale of the largest turbulent eddies is smaller than the size of
the domain over which the turbulence extends. In the Atmospheric
Boundary Layer (ABL) this is typically true for neutral and stable
conditions only. For unstable and convective conditions, however, the
largest transporting eddies may have a size similar to the boundary
layer height itself, and the flux can be counter to the local gradient .
In such conditions a local diffusion approach is no longer appropriate,
and the eddy diffusivity is better represented with turbulent properties
characteristic of the ABL. We will refer to such an approach as
non-local diffusion.

To account for “non-local” transport by convective turbulence in the
ABL, the local diffusion term for constituent :math:`c` is modified as
in ([eq:fluxz2]):

.. math::
   :label:

   {\overline {w^\prime C^\prime}} = - {K_c ( \frac{\partial C}{\partial z} - \gamma_ c)}\ ,
    
where :math:`K_c` is the non-local eddy diffusivity for the quantity of
interest. The term :math:`\gamma_c` is a “non-local” transport term and
reflects non-local transport due to dry convection. Eq. ([4.d.15])
applies to static energy, water vapor, and passive scalars. No
countergradient term is applied to the wind components, so ([eq:fluxz1])
does not contain these terms. For stable and neutral conditions the
non-local term is not relevant for any of the quantities. The eddy
diffusivity formalism is, however, modified for all conditions.

In the non-local diffusion scheme the eddy diffusivity is given by

.. math:: K_c = k\ w_t\ z(1 - \frac{z}{h})^2\ ,

where :math:`w_t` is a turbulent velocity scale and :math:`h` is the
boundary layer height. Equation ([4.d.16]) applies for heat, water vapor
and passive scalars. The eddy diffusivity of momentum :math:`K_m`, is
also defined as ([4.d.16]) but with :math:`w_t` replaced by another
velocity scale :math:`w_m`. With proper formulation of :math:`w_t` (or
:math:`w_m`) and :math:`h`, it can be shown that equation ([4.d.16])
behaves well from very stable to very unstable conditions in
horizontally homogeneous and quasi-stationary conditions. For unstable
conditions :math:`w_t` and :math:`w_m` are proportional to the so-called
convective velocity scale :math:`w_\ast`, while for neutral and stable
conditions :math:`w_t` and :math:`w_m` are proportional to the friction
velocity :math:`u_\ast`.

The major advantage of the present approach over the local eddy
diffusivity approach is that large eddy transport in the ABL is
accounted for and entrainment effects are treated implicitly. Above the
ABL, :math:`\gamma_c=0` so ([4.d.15]) reduces to a local form with
:math:`K_c` given by ([4.d.9]). Near the top of the ABL we use the
maximum of the values by ([4.d.9]) and ([4.d.16]), although ([4.d.16])
almost always gives the larger value in practice.

The non-local transport term in ([4.d.15]), :math:`\gamma_c`, represents
non-local influences on the mixing by turbulence . As such, this term is
small in stable conditions, and is therefore neglected under these
conditions. For unstable conditions, however, most heat and moisture
transport is achieved by turbulent eddies with sizes on the order of the
depth :math:`h` of the ABL. In such cases, a formulation for
:math:`\gamma_c` consistent with the eddy formulation of ([4.d.15]) is
given by

.. math::
   :label:

   \gamma_c = a \frac{w_{\ast} (\overline{w^\prime C^\prime})_s} {{w_m}^2 h}\ ,

where :math:`a` is a constant and
:math:`(\overline{w^\prime C^\prime})_s` is the surface flux (in
kinematic units) of the transported scalar. The form of ([4.d.17]) is
similar to the one proposed in . The non-local correction vanishes under
neutral conditions, for which :math:`w_{\ast} = 0`.

The formulations of the eddy-diffusivity and the non-local terms are
dependent on the boundary layer height :math:`h`. The CCM2 configuration
of this non-local scheme made use of a traditional approach to
estimating the boundary layer depth by assuming a constant value for the
bulk Richardson number across the boundary layer depth so that :math:`h`
was iteratively determined using

.. math::

   h = \frac{Ri_{cr} \{u(h)^2 + v(h)^2\}}{(g / \theta_s) (\theta_v (h) - \theta_s)} \ , 

where :math:`Ri_{cr}` is a critical bulk Richardson number for the ABL;
:math:`u(h)` and :math:`v(h)` are the horizontal velocity components at
:math:`h`; :math:`g/\theta_s` is the buoyancy parameter and
:math:`\theta_v (h)` is the virtual temperature at :math:`h`. The
quantity :math:`\theta_s` is a measure of the surface air temperature,
which under unstable conditions was given by

.. math::
   :label:

   \theta_s = \theta_v (z_s) +  b\ \frac{(\overline{w^\prime \theta^\prime_v})_s}{w_m}\ ,

where :math:`b` is a constant,
:math:`(\overline{w^\prime \theta^\prime_v})_s` is the virtual heat flux
at the surface, :math:`\theta_v(z_s)` is a virtual
temperature in the atmospheric surface layer (nominally 10 m),
:math:`b\ {(\overline{w^\prime \theta^\prime_v})_s / {w_m}}` represents
a temperature excess (a measure of the strength of convective thermals
in the lower part of the ABL) and unstable conditions are determined by
:math:`(\overline{w^\prime \theta^\prime_v})_s >0`. The quantity
:math:`\theta_v(z_s)` was calculated from the temperature and
moisture of the first model level and of the surface by applying the
procedure in . The value of the critical bulk Richardson number
:math:`Ri_{cr}` in ([4.d.18]), which generally depends on the vertical
resolution of the model, was chosen as :math:`Ri_{cr}` = 0.5 for the
CCM2.

have recently studied the suitability of this formulation in the
context of field observations, large-eddy simulations , and an
:math:`E-\epsilon` turbulence closure model . They propose a revised
formulation which combines shear production in the outer region of the
boundary layer with surface friction, where the Richardson number
estimate is based on the differences in wind and virtual temperature
between the top of the ABL and a lower height that is well outside the
surface layer (20 m - 80 m). In addition to providing more realistic
estimates of boundary layer depth, the revised formulation provides a
smoother transition between stable and neutral boundary layers.
Consequently, employs the formulation for estimating the atmospheric
boundary layer height, which can be written as

.. math::
   :label:

   h = z_s + \frac{Ri_{cr} \{ (u(h) - u_{SL})^2 + (v(h) - v_{SL})^2
   + {\cal B}u^2_\ast \}}{(g / \theta_{SL}) (\theta_v(h) -
   \theta_{SL})} . 

The quantities :math:`u_{SL}`, :math:`v_{SL}`, and :math:`\theta_{SL}`
represent the horizontal wind components and virtual potential
temperature just above the surface layer (nominally 0.1\ :math:`h`). In
practice, the lowest model level values for these quantities are used to
iteratively determine :math:`h` for all stability conditions, where the
critical Richardson number, :math:`Ri_{cr}`, is assumed to be 0.3. The
disposable parameter :math:`{\cal B}` has been experimentally determined
to be equal to 100 (see ). The computation starts by calculating the
bulk Richardson number :math:`Ri` between the level of
:math:`\theta_{SL}` and subsequent higher levels of the model. Once
:math:`Ri` exceeds the critical value, the value of :math:`h` is derived
by linear interpolation between the level with :math:`Ri > Ri_{cr}` and
the level below.

Using the calculated value for :math:`h` and the surface fluxes, we
calculate the velocity scales, the eddy diffusivities with ([4.d.16]),
and the countergradient terms with ([4.d.17]), for each of the
transported constituents. Subsequently, the new profiles for
:math:`\theta`, :math:`q`, :math:`u`, and :math:`v` are calculated using
an implicit diffusion formulation.

The turbulent velocity scale of ([4.d.16]) depends primarily on the
relative height :math:`z/h` (:math:`h` is boundary layer height), and
the stability within the ABL. Here stability is defined with respect to
the surface virtual heat flux :math:`(\overline{w^\prime
\theta^\prime_v})_s`. Secondly, the velocity scales are also generally
dependent on the specific quantity of interest. We will assume that the
velocity scales for mixing of passive scalars and specific humidity are
equal to the one for heat, denoted by :math:`w_t`. For the wind
components, the velocity scale is different and denoted by :math:`w_m`.
The specification of :math:`w_t` and :math:`w_m` is given in detail by .
have rewritten the velocity scale, in terms of the more widely accepted
profile functions of , and have given a new formulation for very stable
conditions. Below we follow the latter approach.

For stable (:math:`(\overline{w^\prime \theta^\prime_v})_s < 0`) and
neutral surface conditions
(:math:`(\overline{w^\prime \theta^\prime_v})_s = 0`), the velocity
scale for scalar transport is

.. math:: 
   :label:

   w_t = \frac{u_\ast}{\phi_h}\ ,

where :math:`u_\ast` is the friction velocity defined by

.. math::
   :label:

   u_\ast = [ (\overline{u^\prime w^\prime})_s^2 +
           (\overline{v^\prime w^\prime})_s^2 ]^{1/4}.
           

Furthermore, :math:`\phi_h` is the dimensionless vertical temperature
gradient given by ,

.. math:: 
   :label:

   \phi_h = 1 + 5 \frac{z}{L}\ ,

for :math:`0 \leq z/L \leq 1`. Here :math:`L` is the Obukhov length,
defined by

.. math::
   :label:

   L = \frac{- u_{\ast}^3}{k (g/\theta_{v0})  (\overline{w^\prime\theta^\prime_v})_0}. 

For :math:`z/L > 1`,

.. math:: 
   :label:

   \phi_h = 5 + \frac{z}{L}\ ,

which matches ([4.d.23]) for :math:`z/L = 1`. Equation ([4.d.25]) is a
simple means to prevent :math:`\phi_h` from becoming too large (and
:math:`K_c` too small) in very stable conditions. In stable conditions,
the exchange coefficients for heat and momentum are often found to be
similar. Therefore we may use :math:`w_m`\ =\ :math:`w_t`.

For unstable conditions
:math:`(\overline{w^\prime \theta^\prime_v})_s > 0`, we have that
:math:`w_t` and :math:`w_m` differ in the surface layer :math:`(z/h \leq
0.1)` and in the outer layer of the ABL :math:`(z/h > 0.1)`. For the
surface layer, :math:`w_t` is given by ([4.d.21]) with

.. math:: 
   :label:

   \phi_h = (1 - 15 \frac{z}{L})^{-1/2}\ .

Similarly, :math:`w_m` is written as

.. math:: 
   :label:

   w_m = \frac{u_\ast}{\phi_m}\ ,

where :math:`\phi_m` is the dimensionless wind gradient given by

.. math:: 
   :label:

   \phi_m = (1 - 15 \frac{z}{L})^{-1/3}\ .

 In the surface layer, the scalar flux is normally given by

.. math::
   :label:

   (\overline{w^\prime c^\prime})_0 = - \frac{k u_{\ast} z}{\phi_h}
    ( \frac{\partial C}{\partial z} ) \ .
    

Comparison with ([4.d.15]) and ([4.d.16]) shows that, in the surface
layer, we should have :math:`a = 0` in ([4.d.17]) for consistency.

For the outer layer, :math:`w_t` and :math:`w_m` are given by

.. math::
   :label:

   w_t & = w_m/Pr\ ,\\[-1.0em]
   \intertext{where}\nonumber\\[-2.0em] w_m & = (u_\ast^3 + c_1
   w_\ast^3)^{1/3}\ ,\\[-1.0em]
   \intertext{and}\nonumber\\[-2.0em]
   w_\ast & = ((g/\theta_{v0})\
           (\overline{w^\prime\theta^\prime_v})_0 h)^{1/3}\ 

is the convective velocity scale. Furthermore, :math:`Pr` is the
turbulent Prandtl number and :math:`c_1` is a constant. The latter is
obtained by evaluating the dimensionless vertical wind gradient
:math:`\phi_m` by ([4.d.28]) at the top of the surface layer, as
discussed by . This results in :math:`c_1 = 0.6`. For very unstable
conditions (:math:`h \gg -L` or :math:`w_{\ast}/u_{\ast} \gg 0)`, it can
be shown with ([4.d.30]) that :math:`w_m` is proportional to
0.85 \ :math:`w_\ast`, while for the neutral case :math:`w_m = u_\ast`.
The turbulent Prandtl number :math:`Pr` :math:`(= K_m/K_h = w_m/w_t)` of
([4.d.30]) is evaluated from

.. math::
   :label:

   Pr = \frac{\phi_h}{\phi_m}\ ( \frac{z}{L}) + a k  \frac{z}{h} \frac{w_\ast}{w_m} 

for :math:`z = 0.1 h`. Equation ([4.d.33]) arises from matching
([4.d.15]), ([4.d.16]), ([4.d.17]), and ([4.d.29]) at the top of the
surface layer. As in Troen and Mahrt we assume that :math:`Pr` is
independent of height in the unstable outer layer. Its value decreases
from :math:`Pr = 1` for the neutral case (:math:`z/L =0` and
:math:`w_\ast =0`), to :math:`Pr = 0.6` for :math:`w_\ast/u_\ast \simeq 10` in very
unstable conditions.

In very unstable conditions, the countergradient term of ([4.d.17])
approaches

.. math:: 
   :label:

   \gamma_c = d \frac{\overline{wC}_0}{w_{\ast} h}\ ,

where :math:`d \simeq a/0.85^2`, because for very unstable conditions we
obtain :math:`w_m \simeq 0.85 w_{\ast}`. Since typically
:math:`d \simeq 10` , we have :math:`a = 7.2`. Similarly, the
temperature excess of ([4.d.19]) reads in this limit as :math:`d
(\overline{w^\prime\theta^\prime_v})_0/w_{\ast}`. This leads to
:math:`b` (= 0.85 :math:`d`) = 8.5 in ([4.d.19]).

Finally, using the velocity scales described above, the flux equation
([4.d.15]) is continuous in relative height (:math:`z/h`) and in the
boundary layer stability parameter (:math:`h/L` or
:math:`w_{\ast}/u_{\ast}`).

Discretization of the vertical diffusion equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In , as in previous version of the CCM, ([eq:contz1]–[eq:fluxz2]) are
cast in pressure coordinates, using

.. math:: 
   :label:

   dp = -\rho g dz, 

and discretized in a time-split form using an Euler backward time step.
Before describing the numerical solution of the diffusion equations, we
define a compact notation for the discrete equations. For an arbitrary
variable :math:`\psi`, let a subscript denote a discrete time level,
with current step :math:`\psi_n` and next step :math:`\psi_{n+1}`. The
model has :math:`L` layers in the vertical, with indexes running from
top to bottom. Let :math:`\psi^k` denote a layer midpoint quantity and
let :math:`\psi^{k-}` denote the value on the upper interface of layer
:math:`k` while :math:`\psi^{k+}` denotes the value on the lower
interface. The relevant quantities, used below, are then:

.. math::

   \psi^{k+}& =(\psi^{k}+\psi^{k+1})/2,\quad k\in (1,2,3,...,L-1)
   \nonumber\\ \psi^{k-}& =(\psi^{k-1}+\psi^{k})/2,\quad k\in
   (2,3,4...,L) \nonumber\\ \delta^{k}\psi & = \psi^{k+}-\psi^{k-},
   \nonumber\\ \delta^{k+}\psi & = \psi^{k+1}-\psi^{k}, \nonumber\\
   \delta^{k-}\psi & = \psi^{k}-\psi^{k-1}, \\
   \psi_{n+}& =(\psi_{n}+\psi_{n+1})/2, \nonumber\\ \delta_n\psi & =
   \psi_{n+1}-\psi_{n}, \nonumber\\ \delta t & = t_{n+1}-t_{n},
   \nonumber\\
   \Delta^{k,l} & = 1,\ k=l, \nonumber\\ & = 0,\ k\neq l.  \nonumber

Like the continuous equations, the discrete equations are required to
conserve momentum, total energy and constituents. The discrete forms of
([eq:contz1]–[eq:contz3]) are:

.. math::
   :label:

   \frac{\delta_n (u,v,q)^k}{\delta t} & = g \frac{\delta^k F_{u,v,q}}{\delta^k p}  \\
   \frac{\delta_n s^k}{\delta t} & = g \frac{\delta^k F_{H}}{\delta^k p} + D^k.  

For interior interfaces, :math:`1\le k \le L-1`,

.. math::
   :label:

   F_{u,v}^{k+} & = (g\rho^2 K_m)_n^{k+} \frac{\delta^{k+} (u,v)_{n+1}} {\delta^{k+} p}  \\
   F_{q,H}^{k+} & = (g\rho^2 K_{q,H})_n^{k+} \frac{\delta^{k+} (u,v)_{n+1}} {\delta^{k+} p} \nonumber \\
                &    + (\rho K_{q,H}^t \gamma_{q,H})_n^{k+}.
     

Surface fluxes :math:`F_{u,v,q,H}^{L+}` are provided explicitly at time
:math:`n` by separate surface models for land, ocean, and sea ice while
the top boundary fluxes are usually :math:`F_{u,v,q,H}^{1-}=0`. The
turbulent diffusion coefficients :math:`K_{m,q,H}^{t}` and non-local
transport terms :math:`\gamma_{q,H}` are calculated for time :math:`n`
by the turbulence model described above, which is identical to CCM3. The
molecular diffusion coefficients, described earlier, are only included
if the model top is above :math:`\sim 90` km, in which case nonzero top
boundary fluxes may be included for heat and some constituents.

The free atmosphere turbulent diffusivities :math:`{K}_{n}^{k+}`, given
by ([4.d.9]–[4.d.14b]), are discretized as

.. math::
   :label:

   {K}_{n}^{k+} = {K}_N^{k+} \cdot F_c\! (R_{I}^{k+}) \ge
   0.01. 

The stability function is:

.. math::
   :label:

   F_c(R_I) =
   \begin{cases}
   1/(1 + 10 R_I[1+8 R_I]) & \text{for} \ R_I \geq 0 \
   \text{(stable)} ,\\[1ex] \sqrt{1 - 18 R_I} & \text{for} \ R_I < 0 \
   \text{(unstable)} ,
   \end{cases}
   

The neutral :math:`K_N` is calculated by

.. math::
   :label:

   {K}_N^{k+} = \ell^2 \frac{[( \delta^{k+}{u}_{n} )^2 +
   ( \delta^{k+}{v}_{n} )^2 ]^{1/2}}{\delta^{k+} z_{n}},
   

with :math:`\ell=30` m. The Richardson number in the free atmosphere is
calculated from

.. math::
   :label:

   R_{I}^{k+} & = \frac{g} {\theta_{v}^{k+}} \times \frac{ \delta^{k+} z_n
   \delta^{k+} \theta_{v}} {(\delta^{k+} u_{n} )^2 +
   (\delta^{k+} v_{n} )^2}
   \\[-1.0em]
   \intertext{where}\nonumber\\[-2.0em] \theta^{k}_{v} & = \theta_{n}^{k}
   ( 1.0 + ( \frac{R_v}{R} -1 ) q_{n}^{k} ) \, .
   

Similarly to the continuous form ([eq:diss:sub:`h`\ eat]), :math:`D^k`
is determined by separating the kinetic energy change over a time step
into the kinetic energy flux divergence and the kinetic energy
dissipation. The discrete system is required to conserve energy exactly:

.. math::
   :label:

   eqn{\sum_{k=1}^L [(u_{n+1}^k)^2 + (v_{n+1}^k)^2 + s_{n+1}^k]\delta^k p & =} \\ 
       & \sum_{k=1}^L [(u_{n}^k)^2 + (v_{n}^k)^2 + s_{n}^k]\delta^k p + \delta t (F_H^{L+} +  F_H^{1-}), \nonumber

where we have assumed zero boundary fluxes for kinetic energy. This
leads to

.. math::
   :label:

   D^k & = \frac{g}{2\delta^k p}(d_u^{k+} + d_u^{k-} + d_v^{k+} +
   d_v^{k-}) \\ d_{u,v}^{k+} & = \delta^{k+}(u,v)_{n+}
   F_{u,v}^{k+},\quad 1\le k\le L-1 \\ d_{u,v}^{L+} & =
   -2 (u,v)_{n+}^L F_{u,v}^{L+} 

According to ([eq:dk]), the internal dissipation of kinetic energy in
each layer :math:`D^k` is the average of the dissipation on the bounding
interfaces :math:`d_{u,v}^{k\pm}`, given by ([eq:duvkp]) and
([eq:duvlp]). Expanding ([eq:duvkp]) using ([eq:vdfuv]) and recalling
that :math:`u_{n+} = (u_{n+1} + u_n)/2`,

.. math::
   :label:

   d_u^{k+} = \frac{(g\rho^2 K_m)^{k+}}{2\delta^{k+}p}
                [(\delta^{k+}u_{n+1})^2 + \delta^{k+}u_{n+1}\delta^{k+}u_{n}],
                   

for :math:`1\le k \le L-1` and similarly for :math:`d_v^{k+}`. The
discrete kinetic energy dissipation is not positive definite, because
the last term in ([eq:dukp]) is the product of the vertical difference
of momentum at two time levels. Although :math:`d_{u,v}^{k+}` will
almost always be :math:`>0`, values :math:`\le 0` may occur
occasionally. The kinetic energy dissipation at the surface is

.. math:: 
   :label:

   d_{u,v}^{L+} = - [(u,v)_{n+1}^L + (u,v)_n^L]F_{u,v}^{L+}.

Since the surface stress is opposed to the bottom level wind, the
surface layer is heated by the frictional dissipation. However,
:math:`d_{u,v}^{L+}` is not guaranteed to be positive, since it involves
the bottom level wind at two time levels.

Note that it has been assumed that the pressure does not change within
the vertical diffusion, even though there are boundary fluxes of
constituents, including water. This assumption has been made in all
versions of the CCM and is still made in . This assumption will be
removed in a future version of , since the implied horizontal fluxes of
dry air, to compensate for the boundary flux of water, cause implied
fluxes of other constituents.

Solution of the vertical diffusion equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A series of time-split operators is actually defined by
([eq:vduvq]–[eq:vdfqs]) and ([eq:dk]–[eq:duvlp]). Once the diffusivities
(:math:`K_{m,q,H}`) and the non-local transport terms
(:math:`\gamma_{q,H}`) have been determined, the solution of
([eq:vduvq]–[eq:vdfqs]), proceeds in several steps.

1. update the :math:`q` and :math:`s` profiles using :math:`\gamma_{q,H};`

2. update the bottom level values of :math:`u`, :math:`v`, :math:`q` and :math:`s` using the surface fluxes;

3. invert ([eq:vduvq]) and ([eq:vdfuv]) for :math:`u,v_{n+1}`;

4. compute :math:`D` and use to update the :math:`s` profile;

5. invert ([eq:vduvq],[eq:vds]) and ([eq:vdfqs]) for :math:`s_{n+1}` and  :math:`q_{n+1}`;

Note that since all parameterizations in  return tendencies rather than
modified profiles, the actual quantities returned by the vertical
diffusion are :math:`\delta_n (u,v,s,q) / \delta t`.

The non-local transport terms, :math:`\gamma_{q,H}`, given by
([4.d.17]), cannot be treated implicitly because they depend on the
surface flux, the boundary layer depth and the velocity scale, but not
explicitly on the profile of the transported quantity. Therefore,
application of :math:`\gamma_q` is not guaranteed to give a positive
value for :math:`q` and negative values may not be removed by the
subsequent implicit diffusion step. This problem is not strictly
numerical; it arises under highly non-stationary conditions for which
the ABL formulation is not strictly applicable. In practice, we evaluate

.. math::
   :label:

   q_{n*} = q_n + \frac{g\delta t}{\delta^k p} \delta^k[\rho K_{q}^t \gamma_{q}]_n

and check the :math:`q_{n*}` profile for negative values (actually for
:math:`q_{n*}^k < q_{min}`, where :math:`q_{min}` may be :math:`>0`). If
any negative values are found, we set :math:`q_{n*} = q_n` for that
constituent profile (but not for other constituents at the same point).

Equations ([eq:vduvq]–[eq:vdfqs]) constitute a set of four tridiagonal
systems of the form

.. math::
   :label:

   -A^k \psi^{k+1}_{n+1} + B^k\psi^k_{n+1} -C^k\psi^{k-1}_{n+1} =
           \psi^k_{n\prime},

where :math:`\psi_{n\prime}` indicates :math:`u`, :math:`v`, :math:`q`,
or :math:`s` after updating from time :math:`n` values with the nonlocal
and boundary fluxes. The super-diagonal (:math:`A^k`), diagonal
(:math:`B^k`) and sub-diagonal (:math:`C^k`) elements of ([eq:tridiag1])
are:

.. math::
   :label:

   A^k & = \frac{1}{\delta^{k} p} \frac{\delta
           t}{\delta^{k+}p}(g^2\rho^2 K)_n^{k+},\\
   B^k & = 1 + A^k + C^k, \\
   C^k & = \frac{1}{\delta^{k} p} \frac{\delta
           t}{\delta^{k-}p}(g^2\rho^2 K)_n^{k-}.

The solution of ([eq:tridiag1]) has the form

.. math:: \psi^k_{n+1} = E^k \psi^{k-1}_{n+1} + F^k, 

or,

.. math::
   :label:

   \psi^{k+1}_{n+1} = E^{k+1} \psi^{k}_{n+1} +
   F^{k+1}. 

Substituting ([eq:tridiag3]) into ([eq:tridiag1]),

.. math::
   :label:

   \psi^{k}_{n+1} = \frac{C^k}{B^k - A^k E^{k+1}} \psi^{k-1}_{n+1} +
           \frac{\psi^k_{n\prime} + A^k F^{k+1}}{B^k - A^k E^{k+1}}.
           

Comparing ([eq:tridiag2]) and ([eq:tridiag4]), we find

.. math::
   :label:

   E^k & = \frac{C^k} {B^k - A^k E^{k+1}}, \quad L>k>1,
            \\
   F^k & = \frac{\psi^k_{n\prime} + A^k F^{k+1}}{B^k - A^k E^{k+1}}, \quad L>k>1 .

The terms :math:`E^k` and :math:`F^k` can be determined upward from
:math:`k=L`, using the boundary conditions

.. math:: 
   :label:

   E^{L+1} = F^{L+1} = A^L = 0.

Finally, ([eq:tridiag4]) can be solved downward for
:math:`\psi^{k}_{n+1}`, using the boundary condition

.. math:: 
   :label:

   C^1 = 0 arrow E^1 = 0.

CCM1-3 used the same solution method, but with the order of the solution
reversed, which merely requires writing ([eq:tridiag3]) for
:math:`\psi^{k-1}_{n+1}` instead of :math:`\psi^{k+1}_{n+1}`. The order
used here is particularly convenient because the turbulent diffusivities
for heat and all constituents are the same but their molecular
diffusivities are not. Since the terms in ([eq:tridiag5]-[eq:tridiag6])
are determined from the bottom upward, it is only necessary to
recalculate :math:`A^k`, :math:`C^k`, :math:`E^k` and
:math:`1/({B^k - A^k E^{k+1}})` for each constituent within the region
where molecular diffusion is important. Note that including the
diffusive separation term for constituents (which will be in the next
version of ) adds additional terms to the definitions of :math:`A^k`,
:math:`B^k`, and :math:`C_k`, but does not otherwise change the solution
method.

Discrete equations for :math:`s`, :math:`T`, and :math:`z`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The dry static energy at step :math:`n` and level :math:`k` is

.. math:: 
   :label:

   s_{n}^k = c_p^d T_{n}^k + g z^k, 

which can be calculated from :math:`T_{n}` by integrating the
hydrostatic equation using the perfect gas law.

.. math::
   :label:

   g z \equiv \Phi = \Phi_s + \int_{p_s}^p R T d\ln p^\prime,
  
where :math:`\Phi` is the geopotential, :math:`\Phi_s` is the
geopotential at the Earth’s surface and :math:`p_s` is the surface
pressure. A fairly arbitrary discretization of ([eq:hydroint]) can be
represented using a triangular hydrostatic matrix :math:`H^{kl}`,

.. math:: 
   :label:

   \Phi^k = \Phi_s + \sum_{l=L}^{k} R^l H^{kl} T^l.  

Note that ([eq:phik]) is often written in terms of the virtual
temperature :math:`T_v = T R/R^d`. The apparent gas constant :math:`R`
includes the effect of water vapor and is defined as

.. math:: 
   :label:

   R = R^d + (R^w - R^d) q, 

where :math:`R^d` is the apparent gas constant for dry air and
:math:`R^w` is the gas constant for water vapor.

Using ([eq:phik]) in ([eq:sn1]), we have

.. math::
   :label:

   s_{n}^k & = c_p^d T_{n}^k + \sum_{l=L}^{k} R^l H^{kl} T_{n}^l,
                 \\
           & = (c_p^d + R^k H^{kk} ) T_{n}^k + \Phi_n^{k+}.
               

The interface geopotential in ([eq:sn2]) is defined as

.. math:: 
   :label:

   \Phi^{k+} = \sum_{l=L}^{k+1} R^k H^{kl} T^l, 

and :math:`R^k` is evaluated from ([eq:rappar]), using :math:`q^k_{n}`.
Although the correct boundary condition on ([eq:phiintr]) is
:math:`\Phi_{L+}=\Phi_s`, within the parameterization suite it is
usually sufficient to take :math:`\Phi_{L+}=0`.

The definition of the hydrostatic matrix :math:`H` depends on the
numerical method used in the dynamics and is subject to constraints from
energy and mass conservation. The definitions of :math:`H` for the three
dynamical methods used in  are given in the dynamics descriptions.

After :math:`s_n` is modified by diabatic heating in a time split
process, the new :math:`s_{n+1}=s_n+Q_n\delta t` can be converted into
:math:`T_{n+1}` and :math:`\Phi_{n+1}` using ([eq:sn2]):

.. math::
   :label:

   s_{n+1}^k & = (c_p^d + R^k H^{kk} ) T_{n+1}^k + \Phi_{n+1}^{k+} \\
   T_{n+1}^k & = (s_{n+1}^k - \Phi_{n+1}^{k+}) (c_p + R^k H^{kk})^{-1} 

with :math:`R^k` evaluated from using :math:`q_{n+1}^k`. Once :math:`H`
is defined, ([eq:phiintr]) and ([eq:stt]) can be solved for
:math:`T_{n+1}` and :math:`\Phi_{n+1}` from the bottom up. Since the
latter must normally recalculated if :math:`T` is modified, calculating
:math:`T` and :math:`\Phi` from :math:`s` involves the same amount of
computation as calculating :math:`\Phi` and :math:`s` from :math:`T`.

Sulfur Chemistry
----------------

It is also possible to set CAM to predict sulfate aerosols. These
aerosols can be run as passive (non-interacting) constituents, or the
model can be set to allow sulfate to interact with the radiative
transfer formulation. The CAM 3.0 release of the model allows only the
direct radiative effect of the aerosols, although it is a
straightforward modification of the model to allow indirect effects as
well.

The formulation for the parameterization follows closely that described
in and . The module was used to examine the influence of sulfate
aerosols on the atmospheric radiation budget in The standard emission
inventory used for prognostic aerosols is not the same as that used to
produce the climatological prescribed sulfate aerosols described in
section [section-aero-clim].

The sulfur chemistry represented in the model includes emissions,
transport, gas and aqueous reactions, and wet and dry deposition of DMS,
SO\ :math:`_2`, SO\ :math:`_4^{2-}`, and H\ :math:`_2`\ O\ :math:`_2`.
Sources and sinks represented in the description of the sulfur cycle
include emissions of DMS and anthropogenic sulfur, gas-phase oxidation
of DMS and SO\ :math:`_2`, gas-phase production and destruction of
H\ :math:`_2`\ O\ :math:`_2`, aqueous-phase oxidation of S(IV) by
H\ :math:`_2`\ O\ :math:`_2` and O\ :math:`_3`, dry deposition of
H\ :math:`_2`\ O\ :math:`_2`, SO\ :math:`_2`, and aerosol sulfate, and
wet deposition of H\ :math:`_2`\ O\ :math:`_2`, SO\ :math:`_2`, and
aerosol sulfate.

Transport processes of trace gases and aerosols include resolved-scale
advection and subgrid-scale convection and diffusion. The convective
transport of trace gases and aerosols is performed on the interstitial
fraction of these species in the cloudy volume and the fraction of
dissolved material in the cloud drops that do not undergo microphysical
transformation to precipitation. The species can be can be detrained at
higher levels in the model by the convective processes.

Emissions
~~~~~~~~~

Emissions of sulfur species in the model include anthropogenic emissions
of SO\ :math:`_2` and SO\ :math:`_4^{2-}` and oceanic emissions of DMS;
volcanic and biomass burning sources currently are excluded.
Anthropogenic emissions come from the inventory. The seasonally averaged
emissions data were provided at the surface and at 100 m and above to
accommodate emissions from industry stacks The anthropogenic emissions
are assumed to be 98% by mole SO\ :math:`_2` and 2% SO\ :math:`_4^{2-}`.
Since the emissions inventory supplied data at two levels and the height
of the interface between the bottom two model levels was generally above
100 m (average height was :math:`\sim`\ 120 m), we apportioned a
fraction of the emissions data from above 100 m to the bottom level of
the model. The fraction into the bottom level was determined as

.. math:: {{zi(1) - 100} \over {zi(2) - 100}},

where :math:`zi(1)` is the height of the top of the lowest level of the
model and :math:`zi(2)` is the height of the top of the second lowest
level of the model.

The emissions of DMS were obtained from the biogenic sulfur emissions
inventory of .

Chemical Reactions
~~~~~~~~~~~~~~~~~~

The order of the chemistry calculations is as follows. The aqueous
chemistry is performed after the cloud water mixing ratio is determined.
The new H\ :math:`_2`\ O\ :math:`_2`, SO\ :math:`_2`, and
SO\ :math:`_4^{2-}` concentrations are then used for the gas chemistry
calculations. The modified H\ :math:`_2`\ O\ :math:`_2`, SO\ :math:`_2`,
and SO\ :math:`_4^{2-}` concentrations then are used in the wet
deposition calculation. After the chemistry and wet deposition are
calculated, transport through subgrid convective cores is determined for
the interstitial fraction of each species (because of their high
solubility, sulfate aerosols are not convectively transported). Because
a centered time step is used, a time filter couples the concentrations
from the odd and even time step integrations. Then the emissions and dry
deposition calculations are performed.

The reactions used for the sulfur cycle are described in Table [tab:rxn].

p1.2cmp2.5cmp0.3cmp3.5cmlrr & :math:`k_{298}`\ & :math:`{E \over R}` &Reference
(R1) &SO\ :math:`_2`+ OH + M &:math:`arrow`&
SO\ :math:`_4^{2-}`+ M
&k\ :math:`_o`\ =3.0:math:`\times~10^{-31}`\ :math:`({T \over 300})^{-3.3}`
&& NASA97
& & & &k\ :math:`_{\infty}`\ =1.5:math:`\times~10^{-12}`&&
(R2) &DMS + OH &:math:`arrow`& :math:`\alpha`\ SO\ :math:`_2`+
(1 - :math:`\alpha`) MSA&&& Y90
(R3) &DMS + NO\ :math:`_3`&:math:`arrow`& SO\ :math:`_2`+
HNO\ :math:`_3`&1.0:math:`\times~10^{-12}`& 500. & NASA97
(R4) &HO\ :math:`_2`+ HO\ :math:`_2`&:math:`arrow`&
H\ :math:`_2`\ O\ :math:`_2`+
O\ :math:`_2`&8.6:math:`\times~10^{-12}`& -590. & NASA97
(R5) &H\ :math:`_2`\ O\ :math:`_2`+
h\ :math:`\nu`&:math:`arrow`& 2OH &see text & &
(R6) &H\ :math:`_2`\ O\ :math:`_2`+ OH &:math:`arrow`&
HO\ :math:`_2`+ H\ :math:`_2`\ O&1.7:math:`\times~10^{-12}`& 160. &
NASA97
(R7) &HSO\ :math:`_3^-`+
H\ :math:`_2`\ O\ :math:`_2`&:math:`arrow`& SO\ :math:`_4^{2-}`+
2H\ :math:`^+`+ H\ :math:`_2`\ O&2.7:math:`\times~10^7` & 4750.& HC85
(R8) &HSO\ :math:`_3^-`+ O\ :math:`_3`&:math:`arrow`&
SO\ :math:`_4^{2-}`+ H\ :math:`^+`+
O\ :math:`_2`&3.7:math:`\times~10^5`& 5300. & HC85
(R9) &SO\ :math:`_3^{2-}`+ O\ :math:`_3`&:math:`arrow`&
SO\ :math:`_4^{2-}`+ O\ :math:`_2`&1.5:math:`\times~10^9`& 5280. &
HC85
(R10) &H\ :math:`_2`\ O\ :math:`_2`(g) &:math:`leftharpoons`&
H\ :math:`_2`\ O\ :math:`_2`(aq) &7.4:math:`\times~10^4`& -6621. &
LK86
(R11) &O\ :math:`_3`(g) &:math:`leftharpoons`& O\ :math:`_3`(aq)
&1.15:math:`\times~10^{-2}`& -2560. & NBS65
(R12) &SO\ :math:`_2`(g) &:math:`leftharpoons`& SO\ :math:`_2`
(aq) &1.23 & -3120. & NBS65
(R13) &H\ :math:`_2`\ SO\ :math:`_3`&:math:`leftharpoons`&
HSO\ :math:`_3^-`+ H\ :math:`^+`&1.3:math:`\times~10^{-2}`& -2015. &
M82
(R14) &HSO\ :math:`_3^-`&:math:`leftharpoons`&
SO\ :math:`_3^{2-}`+ H\ :math:`^+`&6.3:math:`\times~10^{-8}`& -1505. &
M82

Gas-Phase Reactions
^^^^^^^^^^^^^^^^^^^

Oxidation of SO\ :math:`_2` to form sulfate, oxidation of DMS to form
SO\ :math:`_2`, and production and destruction of
H\ :math:`_2`\ O\ :math:`_2` are represented in the model.

In R1, it is assumed that the SO\ :math:`_2` + OH reaction is the
rate-limiting step of the multistep process of forming aerosol sulfate.
Concentrations of short-lived radicals OH, NO\ :math:`_3`, and
HO\ :math:`_2`  are prescribed using three-dimensional, monthly averaged
concentrations obtained from the Intermediate Model of Global Evolution
of Species (IMAGES) . The diurnal variation of these oxidants is not
included in our calculations, but instead, the diurnally averaged value
is used at each time step. The rate coefficient for (R2) follows , who
followed the work of . The rate of
H\ :math:`_2`\ O\ :math:`_2` photolysis is determined via a look-up
table method where the photolysis rate depends on the diurnally averaged
zenith angle and the height of the grid point, assuming that the albedo
for ultraviolet radiation is 0.3. Because R4 is nonlinear and the
diurnally averaged rate of reaction does not equal the reaction rate of
diurnally averaged HO\ :math:`_2` mixing ratios, the
HO\ :math:`_2` mixing ratios are adjusted by the amount of daylight at
any given latitude. The rates of the sulfur reactions are determined by
the effective first-order rate coefficient and using a quasi-steady
state approximation . The H\ :math:`_2`\ O\ :math:`_2` concentration
determined from the gas-phase reactions is calculated using an Euler
forward approximation.

Aqueous-Phase Reactions
^^^^^^^^^^^^^^^^^^^^^^^

Oxidation of aqueous SO\ :math:`_2` by O\ :math:`_3` and
H\ :math:`_2`\ O\ :math:`_2` to form SO\ :math:`_4^{2-}` aerosol is
included in the model (Table [tab:rxn]). The concentrations of
O\ :math:`_3` are prescribed using three-dimensional, monthly averaged
concentrations obtained from the IMAGES model. Prescribed species
(O\ :math:`_3`, OH, HO\ :math:`_2`, and NO\ :math:`_3`) are set
according to the linearly interpolated concentration for the location of
the grid point and the time of year.

The pH of the drops is determined diagnostically assuming an
NH\ :math:`_4^+` to SO\ :math:`_4^{2-}` molar ratio of 1.0.

.. math:: 
   :label:

   [H^+] = [HSO_3^-] + [SO_4^{2-}].

The liquid water content in a grid cell is determined by combining the
resolved-scale cloud water mixing ratio that is predicted, the
subgrid-scale deep convective and shallow convective cloud water mixing
ratios, and the resolved-scale rain mixing ratio that is diagnosed from
the precipitation rate using a mass-weighted fall speed, which is
determined assuming a Marshall Palmer size distribution for rain.
SO\ :math:`_2` and H\ :math:`_2`\ O\ :math:`_2` are depleted and
SO\ :math:`_4^{2-}` is produced only in the cloudy region of the grid
box. The grid box concentration of these species is found by multiplying
the cloudy region concentration times the cloud fraction and the clear
air concentration times the fraction of clear air in the grid box.

Because the rate of S(IV) (= SO\ :math:`_2` :math:`\cdot`
H\ :math:`_2`\ O + HSO\ :math:`_3^-` + SO\ :math:`_4^{2-}`) oxidation by
O\ :math:`_3` depends on the pH of the drops, the aqueous-phase
reactions are evaluated using a 2-min time step with an Euler forward
numerical approximation. At the end of each 2-min time step the hydrogen
ion concentration is recalculated so that the influence of pH on S(IV)
oxidation is captured.

Wet Deposition
~~~~~~~~~~~~~~

The wet deposition rates are calculated separately for gases and
aerosols. Cloud water and rain mixing ratios from both the resolved
clouds and the subgrid-scale clouds are determined for the cloudy volume
in each grid column. Trace gases are scavenged only by the liquid
hydrometeors, whereas aerosols can also be scavenged by snow.

The fraction of a trace gas that is in the liquid water is determined
through each species’ Henry’s law coefficient, which is temperature-
and/or pH-dependent. At any particular level in the model the flux of
the dissolved trace gas in the precipitation entering the grid cell from
above is found. The trace gas is reequilibrated with the current model
level’s properties. Then the flux of the dissolved trace gas exiting the
model level is determined. The rate of wet deposition is found from the
flux divergence, maintaining mass conservation.

The wet deposition of aerosols is performed in a similar flux method.
Any layer in the model can undergo both below-cloud and in-cloud
scavenging.

The *below-cloud scavenging* follows and . It is assumed that both rain
and snow, which has graupel-like characteristics (and therefore
characteristics similar to rain), scavenge the aerosol below cloud.
Removal is assumed to take place by a first-order loss process. That is,

.. math:: 
   :label:

   L_{W,bc} = 0.1P q

where :math:`L_{W,bc}` is the loss rate by below-cloud scavenging, 0.1
is the collection efficiency, :math:`P` is the precipitation flux
expressed in mm h\ :math:`^{-1}`, and :math:`q` is the species mass
mixing ratio.

*In-cloud scavenging* is performed assuming that the some fraction
(currently 30%) of the aerosol reside in the cloud water. That fraction
is then removed in proportion to the fraction of cloud water that is
converted to rain through coalescence and accretion processes. This
fraction of the aerosol is removed through wet deposition.

Evaporation of rain is accounted for in the wet deposition rate
calculation by releasing a proportionate mass of aerosol to the
atmosphere (i.e., if 10% of the precipitation evaporates, then 10% of
the sulfate aerosol is released back to the air). This last assumption
could lead to an overestimate of sulfate mixing ratios in the air
because the number of drops that completely evaporate (and therefore the
amount of sulfate aerosol released from the drop to the air) is not
necessarily proportional to the mass of rain that evaporates.

Dry Deposition
~~~~~~~~~~~~~~

In we used of dry deposition similar to that described by . The
deposition velocity of SO\ :math:`_2` is determined following the series
resistance method outlined by where the deposition velocity is inversely
proportional to the sum of the aerodynamic resistance, the resistance to
transport across the atmospheric sublayer in contact with surface
elements, and the surface resistance. The aerodynamic and sublayer
resistances are determined using boundary layer meteorological
parameters. The surface resistance is found through a parameterization
outlined by .

We are in the process of integrating this calculation with the surface
process characterization produced by the Common Land Model (CLM). When
complete, the internal consistency of the parameterization will be much
improved.

In the meantime, we have chosen to prescribe our deposition velocities
following . For SO\ :math:`_2` we use 0.6 cm/s for land, 0.8 cm/s over
ocean, and 0.1 cm/s over ice and snow. Deposition velocities for
SO\ :math:`_4^{2-}` are set to 0.2cm/s everywhere.

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
specified concentration distributions or prognostic concentrations .

The specified distributions are globally uniform in the troposphere.
Above a latitudinally and seasonally specified tropopause height, the
distributions are zonally symmetric and decrease upward, with a separate
latitude-dependent scale height for each gas.

Prognostic distributions are computed following . Transport equations
for the four gases are included, and losses have been parameterized by
specified zonally symmetric loss frequencies:
:math:`\partial q / \partial t =  - \alpha ( y, z, t ) q`. Monthly
averaged loss frequencies, :math:`\alpha`, are obtained from the
two-dimensional model of .

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
shown by . In , it is assumed that the water vapor (volume mixing ratio)
source is twice the CH\ :math:`_4` sink. This approach was also taken by
for middle atmosphere studies with an earlier version of the CCM. This
part of the water budget is of some importance in climate change
studies, because the atmospheric CH\ :math:`_4` concentrations have
increased rapidly with time and this increase is projected to continue
into the next century (e.g., ) The representation of stratospheric water
vapor in  is necessarily crude, since there are few levels above the
tropopause. However, the model is capable of capturing the main features
of the CH\ :math:`_4` and water distributions.
