.. _dynamics:

.. |cam| replace:: CAM6.0

Dynamics
========

.. _sec-finite-volume:

Finite Volume Dynamical Core
----------------------------

.. _fv-overview:

Overview
~~~~~~~~

This document describes the Finite-Volume (FV) dynamical core that was
initially developed and used at the NASA Data Assimilation Office (DAO)
for data assimilation, numerical weather predictions, and climate
simulations. The finite-volume discretization is local and entirely in
physical space. The horizontal discretization is based on a conservative
“*flux-form semi-Lagrangian*” scheme described by :cite:`lin96`
(hereafter LR96) and :cite:`lin97b` (hereafter LR97). The vertical
discretization can be best described as *Lagrangian* with a conservative
re-mapping, which essentially makes it *quasi-Lagrangian*. The
*quasi-Lagrangian* aspect of the vertical coordinate is transparent to
model users or physical parameterization developers, and it functions
exactly like the :math:`\eta -coordinate` (a hybrid :math:`\sigma -p` coordinate) used by other dynamical cores within CAM.

In the current implementation for use in CAM, the FV dynamics and
physics are “time split” in the sense that all prognostic variables are
updated sequentially by the “dynamics” and then the “physics”. The time
integration within the FV dynamics is fully explicit, with sub-cycling
within the 2D Lagrangian dynamics to stabilize the fastest wave (see
section [FVvdisc]). The transport for tracers, however, can take a much
larger time step (*e.g.*, 30 minutes as for the physics).

The governing equations for the hydrostatic atmosphere
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For reference purposes, we present the continuous differential equations
for the hydrostatic 3D atmospheric flow on the sphere for a general
vertical coordinate :math:`\zeta` (*e.g*., :cite:`kasahara74`). Using
standard notations, the hydrostatic balance equation is given as
follows:

.. math::
   :label: hydro
   
   \frac{1}{\rho }\frac{\partial p}{\partial z}+g=0 ,

where :math:`\rho` is the density of the air, *p* the pressure, and
*g* the gravitational constant. Introducing the “*pseudo-density*”
:math:`\pi =\frac{\partial p}{\partial \zeta }` (*i.e.*, the vertical pressure gradient in the general coordinate),
from the hydrostatic balance equation the *pseudo-density* and the true
density are related as follows:

.. math::
   :label: (hodrostatic-pi
   
   \pi =-\frac{\partial \Phi }{\partial \zeta }\rho ,

where :math:`\Phi =gz` is the geopotential. Note that :math:`\pi`
reduces to the “true density” if :math:`\zeta =-gz`, and the “surface
pressure” :math:`P_{s}` if :math:`\zeta =\sigma` (:math:`\sigma =\frac{p}{P_{s}}`). 
The conservation of total air mass using :math:`\pi` as the prognostic variable can be written as

.. math::
   :label: mass-pi
   
   \frac{\partial }{\partial t}\pi +\nabla \cdot
   \left(\overrightarrow{V}\pi \right) =0 ,

where :math:`\overrightarrow{V}=(u,v,\frac{d\zeta }{dt})`. Similarly,
the mass conservation law for tracer species (or water vapor) can be
written as

.. math::
   :label: tracer-pi
   
   \frac{\partial }{\partial t}(\pi q)+\nabla \cdot
   \left(\overrightarrow{V}\pi q\right) =0 ,

where *q* is the mass mixing ratio (or specific humidity) of the tracers
(or water vapor).

Choosing the (virtual) potential temperature :math:`\Theta` as the
thermodynamic variable, the first law of thermodynamics is written as

.. math::
   :label: thermo-pi
   
   \frac{\partial }{\partial t}(\pi \Theta )+\nabla \cdot \left(
   \overrightarrow{V}\pi \Theta \right) =0 .

Letting :math:`(\lambda ,\theta )` denote the (longitude, latitude)
coordinate, the momentum equations can be written in the
“vector-invariant form” as follows:

.. math::
   :label: u-pi

   \frac{\partial }{\partial t}u=\Omega v-\frac{1}{Acos\theta }\left[
     \frac{\partial }{\partial \lambda }\left( \kappa +\Phi -\nu D\right)
     +\frac{1}{\rho }\frac{\partial }{\partial \lambda }p\right]
   -\frac{d\zeta }{dt}\frac{\partial u}{\partial \zeta } ,

.. math::
   :label: v-pi
   
   \frac{\partial }{\partial t}v=-\Omega u-\frac{1}{A}\left[
     \frac{\partial }{\partial \theta }\left( \kappa +\Phi -\nu D\right)
     +\frac{1}{\rho }\frac{\partial }{\partial \theta }p\right]
   -\frac{d\zeta }{dt}\frac{\partial v}{\partial \zeta } ,

where *A* is the radius of the earth, :math:`\nu` is the coefficient
for the optional divergence damping, *D* is the horizontal divergence

.. math::

   D=\frac{1}{Acos\theta }\left[ \frac{\partial
   }{\partial \lambda }(u)+\frac{\partial }{\partial \theta }(v\,
   cos\theta )\right] ,

.. math:: \kappa =\frac{1}{2}\left( u^{2}+v^{2}\right) ,

and :math:`\Omega`, the vertical component of the absolute vorticity,
is defined as follows:

.. math::

   \Omega =2\omega \, sin\theta +\frac{1}{A\, cos\theta }\left[
   \frac{\partial }{\partial \lambda }v-\frac{\partial }{\partial \theta
   }(u\, cos\theta )\right] ,

where :math:`\omega` is the angular velocity of the earth. Note that
the last term in :eq:`u-pi` and :eq:`v-pi` vanishes if the vertical
coordinate :math:`\zeta` is a conservative quantity (*e.g*., entropy
under adiabatic conditions :cite:`hsu90` or an imaginary
conservative tracer), and the 3D divergence operator becomes 2D along
constant :math:`\zeta` surfaces. The discretization of the 2D
horizontal transport process is described in section [FVhdisc]. The
complete dynamical system using the Lagrangian control-volume vertical
discretization is described in section [FVvdisc] and section [sec:damp]
describes the explicit diffusion operators available in CAM5. A mass,
momentum, and total energy conservative mapping algorithm is described
in section [FVmap] and in section [sec:geo] an alternative geopotential
conserving vertical remapping method is described. Sections
[FVqconserve] and [sec:neg] are on the adjusctment of pressure to
include the change in mass of water vapor and on the negative tracer
fixer in CAM, respectively. Last the global energy fixer is described
(section [sec:Global-Energy-Fixer]).

.. _FVhdisc:

Horizontal discretization of the transport process on the sphere
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since the vertical transport term would vanish after the introduction of
the vertical Lagrangian control-volume discretization (see section
[FVvdisc]), we shall present here only the 2D (horizontal) forms of the
FFSL transport algorithm for the transport of density :eq:`mass-pi` and
mixing ratio-like quantities :eq:`tracer-pi` on the sphere. The governing
equation for the pseudo-density :eq:`mass-pi` becomes

.. math::
   :label: pi-2d
   
   \frac{\partial }{\partial t}\pi +\frac{1}{Acos\theta }\left[
   \frac{\partial }{\partial \lambda }(u\pi )+\frac{\partial }{\partial
   \theta }(v\pi \, cos\theta )\right] =0 .

The finite-volume (*integral*) representation of the continuous
:math:`\pi` field is defined as follows:

Given the *exact* 2D wind field :math:`\overrightarrow{V}(t;\lambda ,\theta )=(U,V)` the 2D integral
representation of the conservation law for :math:`\widetilde{\pi }`
can be obtained by integrating :eq:`pi-2d` in time and in space

The above 2D transport equation is still *exact* *for the finite-volume
under consideration*. To carry out the contour integral, certain
approximations must be made. LR96 essentially decomposed the flux
integral using two orthogonal 1D flux-form transport operators.
Introducing the following difference operator

.. math:: \delta _{x}q=q(x+\frac{\Delta x}{2})-q(x-\frac{\Delta x}{2}),

and assuming :math:`(u^{*},v^{*})` is the time-averaged (from time
:math:`t` to time :math:`t+\Delta t`) :math:`\overrightarrow{V}` on the
C-grid (*e.g*., Fig. 1 in LR96), the 1-D finite-volume flux-form
transport operator *F* in the :math:`\lambda`-direction is

.. math::
   :label: xtp
   
   F(u^{*},\Delta t,\widetilde{\pi })=-\frac{1}{A\Delta \lambda cos\theta
   }\, \delta _{\lambda }\left[ \int _{t}^{t+\Delta t}\pi U\, dt\right]
   =-\frac{\Delta t}{A\Delta \lambda cos\theta }\, \delta _{\lambda
   }\left[ \chi (u^{*},\Delta t;\pi )\right] ,

where :math:`\chi` , the time-accumulated (from *t* to *t*\ +\ :math:`\Delta`\ t) mass flux across the cell wall, is
defined as follows,

.. math::
   :label: xmass
   
   \chi (u^{*},\Delta t;\pi )=\frac{1}{\Delta t}\int _{t}^{t+\Delta t}\pi
   U\, dt\equiv u^{*}\pi ^{*}(u^{*},\Delta t,\widetilde{\pi }) ,

and

.. math::
   :label: pi-

   
   \pi ^{*}(u^{*},\Delta t;\widetilde{\pi })\approx \frac{1}{\Delta
   t}\int _{t}^{t+\Delta t}\pi \, dt

can be interpreted as a time mean (from time :math:`t` to time :math:`
t+\Delta t`) pseudo-density value of all material that passed through
the cell edge from the upwind direction.

Note that the above *time integration* is to be carried out along the
*backward-in-time* trajectory of the cell edge position from
:math:`t=t+\Delta t` (the arrival point; (*e.g*., point B in Fig. 3 of
LR96) back to time :math:`t` (the departure point; *e.g*., point B’ in
Fig. 3 of LR96). The very essence of the 1D finite-volume algorithm is
to construct, based on the given initial cell-mean values of :math:`
\widetilde{\pi }`, an approximated subgrid distribution of the true
:math:`\pi` field, to enable an analytic integration of :eq:`pi-`.
Assuming there is no error in obtaining the time-mean wind
:math:`(u^{\*})`, the only error produced by the 1D transport scheme
would be solely due to the approximation to the continuous distribution
of :math:`\pi` within the subgrid under consideration (this is not the
case in 2D; Lauritzen, Ullrich, and Nair (2010)). From this perspective,
it can be said that the 1D finite-volume transport algorithm combines
the time-space discretization in the approximation of the time-mean
cell-edge values :math:`\pi ^{*}`. The physically correct way of
approximating the integral :eq:`pi-` must be “upwind”, in the sense that
it is integrated along the backward trajectory of the cell edges. For
example, a center difference approximation to :eq:`pi-` would be
physically incorrect, and consequently numerically unstable unless
artificial numerical diffusion is added.

Central to the accuracy and computational efficiency of the
finite-volume algorithms is the degrees of freedom that describe the
subgrid distribution. The first order upwind scheme, for example, has
zero degrees of freedom within the volume as it is assumed that the
subgrid distribution is piecewise constant having the same value as the
given volume-mean. The second order finite-volume scheme (*e.g*., :cite:`lin94`) 
assumes a piece-wise linear subgrid distribution, which
allows one degree of freedom for the specification of the “slope” of the
linear distribution to improve the accuracy of integrating :eq:`pi-`.
The Piecewise Parabolic Method (PPM, :cite:`colella84`) has
two degrees of freedom in the construction of the second order
polynomial within the volume, and as a result, the accuracy is
significantly enhanced. The PPM appears to strike a good balance between
computational efficiency and accuracy. Therefore, the PPM is the basic
1D scheme we chose (see, e.g., :cite:`machenhauer98`). Note that the
subgrid PPM distributions are compact, and do not extend beyond the
volume under consideration. The accuracy is therefore significantly
better than the order of the chosen polynomials implies. While the PPM
scheme possesses all the desirable attributes (mass conserving,
monotonicity preserving, and high-order accuracy) in 1D, it is important
that a solution be found to avoid the directional splitting in the
multi-dimensional problem of modeling the dynamics and transport
processes of the Earth’s atmosphere.

The first step for reducing the splitting error is to apply the two
orthogonal 1D flux-form operators in a directionally symmetric way.
After symmetry is achieved, the “inner operators” are then replaced with
corresponding advective-form operators (in CAM5 the “inner operators”
are based on constant cell-average values and not the PPM). A stability
analysis of the consequences of using different inner and outer
operators in the LR96 scheme is given in Lauritzen (2007). A consistent
advective-form operator in the :math:`\lambda -`\ direction can be
derived from its flux-form counterpart (:math:`F)` as follows:

.. math::
   :label: xadv

   
   f(u^{*},\Delta t,\widetilde{\pi })=F(u^{*},\Delta t,\widetilde{\pi
   })+\widetilde{\rho }\, F(u^{*},\Delta t,\widetilde{\pi }\equiv
   1)=F(u^{*},\Delta t,\widetilde{\pi })+\widetilde{\pi }\,
   C_{def}^{\lambda } ,

.. math::
   :label: xdef

   
   C^{\lambda }_{def}=\frac{\Delta t\, \delta _{\lambda }u^{*}}{A\Delta
   \lambda cos\theta } ,

where :math:`C_{def}^{\lambda }` is a dimensionless number indicating
the degree of the flow deformation in the :math:`\lambda`-direction.
The above derivation of :math:`f` is slightly different from LR96’s
approach, which adopted the traditional 1D advective-form
semi-Lagrangian scheme. The advantage of using :eq:`xadv` is that
computation of winds at cell centers (Eq. 2.25 in LR96) are avoided.

Analogously, the **1D flux-form transport operator** *G* **in the
latitudinal (:math:`\theta`) direction is derived as follows:**

.. math::
   :label: ytp
   
   G(v^{*},\Delta t,\widetilde{\pi })=-\frac{1}{A\Delta \theta cos\theta
   }\, \delta _{\theta }\left[ \int _{t}^{t+\Delta t}\pi Vcos\theta \,
   dt\right] =-\frac{\Delta t}{A\Delta \theta cos\theta }\, \delta
   _{\theta }\left[ v^{*}cos\theta \, \pi ^{*}\right] ,

and likewise the advective-form operator,

.. math::
   :label: yadv

   
   g(v^{*},\Delta t,\widetilde{\pi })=G(v^{*},\Delta t,\widetilde{\pi
   })+\widetilde{\pi }\, C_{def}^{\theta } ,

where

.. math::
   :label: ydef

   
   C^{\theta }_{def}=\frac{\Delta t\, \delta _{\theta }\left[
   v^{*}cos\theta \right] }{A\Delta \theta cos\theta } .

To complete the construction of the 2D algorithm on the sphere, we
introduce the following short hand notations:

.. math::
   :label: def-1

   
   (\, )^{\theta }=(\, )^{n}+\frac{1}{2}g\left[ v^{*},\Delta t,\, (\,
   )^{n}\right] ,

.. math::
   :label: def-2

   
   (\, )^{\lambda }=(\, )^{n}+\frac{1}{2}f\left[ u^{*},\Delta t,\, (\,
   )^{n}\right] .

The 2D transport algorithm (*cf*, Eq. 2.24 in LR96) can then be written
as

.. math::
   :label: den-gf

   
   \widetilde{\pi }^{n+1}=\widetilde{\pi }^{n}+F\left[ u^{*},\Delta
   t,\widetilde{\pi }^{\theta }\right] +G\left[ v^{*},\Delta
   t,\widetilde{\pi }^{\lambda }\right] .

Using explicitly the mass fluxes :math:`\left( \chi ,Y\right)`,
:eq:`den-gf` is rewritten as

.. math::
   :label: air

   
   \widetilde{\pi }^{n+1}=\widetilde{\pi }^{n}-\frac{\Delta t}{Acos\theta
   }\left\{ \frac{1}{\Delta \lambda }\delta _{\lambda }\left[ \chi
   (u^{*},\Delta t;\widetilde{\pi }^{\theta })\right] +\frac{1}{\Delta
   \theta }\delta _{\theta }\left[ cos\theta \, Y(v^{*},\Delta
   t;\widetilde{\pi }^{\lambda })\right] \right\} ,

where :math:`Y`, the mass flux in the meridional direction, is
defined in a similar fashion as :math:`\chi` :eq:`xmass`. The ability of
the LR96 scheme to approximate the exact geometry of the fluxes for
deformational flows is discussed in Machenhauer, Kaas, and Lauritzen
(2009) and Lauritzen, Ullrich, and Nair (2010).

It can be verified that in the special case of constant density flow
(:math:`\widetilde{\pi
}=constant)` the above equation degenerates to the finite-difference
representation of the *incompressibility condition* of the “time mean”
wind field :math:`(u^{*},v^{*})`, *i.e*.,

.. math::
   :label: div=0

   
   \frac{1}{\Delta \lambda }\delta _{\lambda }u^{*}+\frac{1}{\Delta
   \theta }\delta _{\theta }\left( v^{*}cos\theta \right) =0 .

The fulfillment of the above *incompressibility condition* for constant
density flows is crucial to the accuracy of the 2D flux-form
formulation. For transport of volume mean mixing ratio-like quantities
:math:`(\widetilde{q})` the mass fluxes :math:`(\chi ,Y)` as defined
previously should be used as follows

.. math::
   :label: tracer
   
   \widetilde{q}^{n+1}=\frac{1}{\widetilde{\pi }^{n+1}}\left[
   \widetilde{\pi }^{n}\widetilde{q}^{n}+F(\chi ,\Delta
   t,\widetilde{q}^{\theta })+G(Y,\Delta t,\widetilde{q}^{\lambda
   })\right] .

Note that the above form of the tracer transport equation consistently
degenerates to :eq:`den-gf` if :math:`\widetilde{q}\equiv 1` (*i.e*.,
the tracer density equals to the background air density), which is
another important condition for a flux-form transport algorithm to be
able to avoid generation of noise (*e.g*., creation of artificial
gradients) and to maintain mass conservation.

.. _FVvdisc:

A *vertically Lagrangian* and *horizontally Eulerian* control-volume discretization of the hydrodynamics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The very idea of using Lagrangian vertical coordinate for formulating
governing equations for the atmosphere is not entirely new. :cite:`starr45`) 
is likely the first to have formulated, in the *continuous
differential form*, the governing equations using a Lagrangian
coordinate. Starr did not make use of the *discrete* Lagrangian
control-volume concept for discretization nor did he present a solution
to the problem of computing the pressure gradient forces. In the
*finite-volume discretization* to be described here, the Lagrangian
surfaces are treated as the bounding material surfaces of the Lagrangian
control-volumes within which the finite-volume algorithms developed in
LR96, LR97, and L97 will be directly applied.

To use a vertical Lagrangian coordinate system to reduce the 3D
governing equations to the 2D forms, one must first address the issue of
whether it is an inertial coordinate or not. For hydrostatic flows, it
is. This is because both the right-hand-side and the left-hand-side of
the vertical momentum equation vanish for purely hydrostatic flows.

Realizing that the earth’s surface, for all practical modeling purposes,
can be regarded as a non-penetrable material surface, it becomes
straightforward to construct a terrain-following Lagrangian
control-volume coordinate system. In fact, any commonly used
terrain-following coordinates can be used as the starting reference
(*i.e*., fixed, Eulerian coordinate) of the floating Lagrangian
coordinate system. To close the coordinate system, the model top (at a
prescribed constant pressure) is also assumed to be a Lagrangian
surface, which is the same assumption being used by practically all
global hydrostatic models.

The basic idea is to start the time marching from the chosen
terrain-following Eulerian coordinate (*e.g*., pure :math:`\sigma` or
hybrid :math:`\sigma` -p), *treating the initial coordinate surfaces as
material surfaces*, the finite-volumes bounded by two coordinate
surfaces, *i.e*., the Lagrangian control-volumes, are free vertically,
to float, compress, or expand with the flow as dictated by the
hydrostatic dynamics.

By choosing an imaginary conservative tracer :math:`\zeta` that is a
monotonic function of height and constant on the initial reference
coordinate surfaces (*e.g*., the value of “:math:`\eta`” in the hybrid
:math:`\sigma -p` coordinate used in CAM), the 3D governing equations
written for the general vertical coordinate in section 1.2 can be
reduced to 2D forms. After factoring out the constant :math:`\delta \zeta`, :eq:`mass-pi`, the conservation law for the pseudo-density
(:math:`\pi=\frac{\delta p}{\delta \zeta }`), becomes

.. math::
   :label: mass-lcv

   
   \frac{\partial }{\partial t}\delta p+\frac{1}{Acos\theta }\left[
   \frac{\partial }{\partial \lambda }(u\delta p)+\frac{\partial
   }{\partial \theta }(v\delta p\, cos\theta )\right] =0 ,

where the symbol :math:`\delta` represents the vertical difference
between the two neighboring Lagrangian surfaces that bound the finite
control-volume. From :eq:`hydro`, the pressure thickness
:math:`\delta p` of that control-volume is proportional to the total
mass, *i.e*., :math:`\delta p=-\rho g\delta z`. Therefore, it can be said that the
Lagrangian control-volume vertical discretization has the hydrostatic
balance built-in, and :math:`\delta p` can be regarded as the
“pseudo-density” for the discretized Lagrangian vertical coordinate
system.

Similarly, :eq:`tracer-pi`, the mass conservation law for all tracer
species, is

.. math::
   :label: tracer-lcv

   
   \frac{\partial }{\partial t}(q\delta p)+\frac{1}{Acos\theta }\left[
   \frac{\partial }{\partial \lambda }(uq\delta p)+\frac{\partial
   }{\partial \theta }(vq\delta p\, cos\theta )\right] =0,

the thermodynamic equation, :eq:`thermo-pi`, becomes

.. math::
   :label: Thermo-lcv

   
   \frac{\partial }{\partial t}(\Theta \delta p)+\frac{1}{Acos\theta
   }\left[ \frac{\partial }{\partial \lambda }(u\Theta \delta
   p)+\frac{\partial }{\partial \theta }(v\Theta \delta p\, cos\theta
   )\right] =0,

and :eq:`u-pi` and :eq:`v-pi`, the momentum equations, are reduced to

.. math::
   :label: u-lcv

   
   \frac{\partial }{\partial t}u=\Omega v-\frac{1}{Acos\theta }\left[
   \frac{\partial }{\partial \lambda }\left( \kappa +\Phi -\nu D\right)
   +\frac{1}{\rho }\frac{\partial }{\partial \lambda }p\right] ,

.. math::
   :label: v-lcv

   
   \frac{\partial }{\partial t}v=-\Omega u-\frac{1}{A}\left[
   \frac{\partial }{\partial \theta }\left( \kappa +\Phi -\nu D\right)
   +\frac{1}{\rho }\frac{\partial }{\partial \theta }p\right] .

Given the prescribed pressure at the model top :math:`P_{\infty }`,
the position of each Lagrangian surface :math:`P_{l}` (horizontal
subscripts omitted) is determined in terms of the hydrostatic pressure
as follows:

.. math::
   :label: L-coord

   
   P_{l}=P_{\infty }+\sum ^{l}_{k=1}\delta P_{k},\, \, \, \, \, (for\,
   l=1,\, 2,\, 3,\, ...,\, N) ,

where the subscript :math:`l` is the vertical index ranging from 1
at the lower bounding Lagrangian surface of the first (the highest)
layer to :math:`N` at the Earth’s surface. There are :math:`N`\ +1
Lagrangian surfaces to define a total number of :math:`N` Lagrangian
layers. The surface pressure, which is the pressure at the lowest
Lagrangian surface, is easily computed as :math:`P_{N}` using
:eq:`L-coord`. The surface pressure is needed for the physical
parameterizations and to define the reference Eulerian coordinate for
the mapping procedure (to be described in section :ref:`FVmap`).

With the exception of the pressure-gradient terms and the addition of a
thermodynamic equation, the above 2D Lagrangian dynamical system is the
same as the shallow water system described in LR97. The conservation law
for the depth of fluid :math:`h` in the shallow water system of LR97
is replaced by :eq:`mass-lcv` for the pressure thickness :math:`\delta p`. 
The ideal gas law, the mass conservation law for air mass,
the conservation law for the potential temperature :eq:`Thermo-lcv`,
together with the modified momentum equations :eq:`u-lcv` and :eq:`v-lcv`
close the 2D Lagrangian dynamical system, which are vertically coupled
only by the hydrostatic relation (see :eq:`hydro-PT`), section [FVmap].

The time marching procedure for the 2D Lagrangian dynamics follows
closely that of the shallow water dynamics fully described in LR97. For
computational efficiency, we shall take advantage of the stability of
the FFSL transport algorithm by using a much larger time step
(:math:`\Delta t)` for the transport of all tracer species (including
water vapor). As in the shallow water system, the Lagrangian dynamics
uses a relatively small time step, :math:`\Delta \tau =\Delta t/m`, where :math:`m` is the number of the sub-cycling needed
to stabilize the fastest wave in the system. We shall describe here this
time-split procedure for the *prognostic variables* 
:math:`\left[ \delta p,\Theta ,u,v;q\right]` on the D-grid. Discretization on
the C-grid for obtaining the *diagnostic variables*, the time-averaged
winds :math:`(u^{*},v^{*})`, is analogous to that of the D-grid (see also LR97).

Introducing the following short hand notations (*cf*, :eq:`def-1` and
:eq:`def-2`):

.. math::

   (\, )_{i}^{\theta }=(\,
   )^{n+\frac{i-1}{m}}+\frac{1}{2}g[v_{i}^{*},\Delta \tau ,(\,
   )^{n+\frac{i-1}{m}}],

.. math::

   (\, )_{i}^{\lambda }=(\,
   )^{n+\frac{i-1}{m}}+\frac{1}{2}f[u_{i}^{*},\Delta \tau ,(\,
   )^{n+\frac{i-1}{m}}],

and applying directly :eq:`air`, the update of “pressure thickness”
:math:`\delta p`, using the fractional time step
:math:`\Delta \tau =\Delta
t/m`, can be written as

.. math::
   :label: mass

   
   \delta p^{n+\frac{i}{m}}=\delta p^{n+\frac{i-1}{m}}-\frac{\Delta \tau
   }{Acos\theta }\left\{ \frac{1}{\Delta \lambda }\delta _{\lambda
   }\left[ x_{i}^{*}(u_{i}^{*},\Delta \tau ;\delta p_{i}^{\theta
   })\right] +\frac{1}{\Delta \theta }\delta _{\theta }\left[ cos\theta
   \, y_{i}^{*}(v_{i}^{*},\Delta \tau ;\delta p_{i}^{\lambda })\right]
   \right\}

.. math:: (for\, i=1,...,m),

where :math:`\left[ x_{i}^{*},y_{i}^{*}\right]` are the background
air mass fluxes, which are then used as input to Eq. 24 for transport of
the potential temperature :math:`\Theta`:

.. math::
   :label: pt

   
   \Theta ^{n+\frac{i}{m}}=\frac{1}{\delta p^{n+\frac{i}{m}}}\left[
   \delta p^{n+\frac{i-1}{m}}\Theta ^{n+\frac{i-1}{m}}+F(x_{i}^{*},\Delta
   \tau ;\Theta _{i}^{\theta })+G(y_{i}^{*},\Delta \tau ,\Theta
   _{i}^{\lambda })\right] .

The discretized momentum equations for the shallow water system (*cf*,
Eq. 16 and Eq. 17 in LR97) are modified for the pressure gradient terms
as follows:

.. math::
   :label: u

   
   u^{n+\frac{i}{m}}=u^{n+\frac{i-1}{m}}+\Delta \tau \, \left[
   y_{i}^{*}\left( v_{i}^{*},\Delta \tau ;\Omega ^{\lambda }\right)
   -\frac{1}{A\Delta \lambda cos\theta }\delta _{\lambda }(\kappa
   ^{*}-\nu D^{*})+\widehat{P_{\lambda }}\right] ,

.. math::
   :label: v

   
   v^{n+\frac{i}{m}}=v^{n+\frac{i-1}{m}}-\Delta \tau \, \left[
   x_{i}^{*}\left( u_{i}^{*},\Delta \tau ;\Omega ^{\theta }\right)
   +\frac{1}{A\Delta \theta }\delta _{\theta }(\kappa ^{*}-\nu
   D^{*})-\widehat{P_{\theta }}\right] ,

where :math:`\kappa ^{*}` is the upwind-biased “kinetic energy” (as
defined by Eq. 18 in LR97), and :math:`D^{*}`, the horizontal
divergence on the D-grid, is discretized as follows:

.. math::

   D^{*}=\frac{1}{Acos\theta }\left[ \frac{1}{\Delta \lambda }\delta
   _{\lambda }u^{n+\frac{i-1}{m}}+\frac{1}{\Delta \theta }\delta _{\theta
   }\left( v^{n+\frac{i-1}{m}}cos\theta \right) \right] .

The finite-volume mean pressure-gradient terms in :eq:`u` and :eq:`v` are
computed as follows:

.. math::
   :label: px

   
   \widehat{P_{\lambda }}=\frac{\oint _{\Pi \rightleftharpoons \lambda
   }\phi d\Pi }{Acos\theta \, \oint _{\Pi \rightleftharpoons \lambda }\Pi
   d\lambda } ,

.. math::
   :label: py

   
   \widehat{P_{\theta }}=\frac{\oint _{\Pi \rightleftharpoons \theta
   }\phi d\Pi }{A\, \oint _{\Pi \rightleftharpoons \theta }\Pi d\theta } ,

where :math:`\Pi =p^{\kappa }\, (\kappa =R/C_{p})`, and the symbols “:math:`\Pi \rightleftharpoons \lambda`” and 
“:math:`\Pi`\ :math:`\rightleftharpoons \theta`” indicate that the contour integrations are
to be carried out, using the finite-volume algorithm described in L97, in the :math:`(\Pi ,\lambda )` and :math:`(\Pi ,\theta )` space, respectively.

To complete one time step, equations :eq:`mass`-[v], together with their
counterparts on the C-grid are cycled :math:`m` times using the
fractional time step :math:`\Delta \tau`, which are followed by the
tracer transport using :eq:`tracer-lcv` with the large-time-step
:math:`\Delta t`.

Mass fluxes :math:`(x^{*},y^{*})` and the winds
:math:`(u^{*},v^{*})` on the C-grid are accumulated for the
large-time-step transport of tracer species (including water vapor)
:math:`q` as

.. math::
   :label: tracers

   
   q_{}^{n+1}=\frac{1}{\delta p^{n+1}}\left[ q_{}^{n}\delta
   p^{n}+F(X^{*},\Delta t,q_{}^{\theta })+G(Y^{*},\Delta t,q_{}^{\lambda
   })\right] ,

where the time-accumulated mass fluxes :math:`(X^{*},Y^{*})` are
computed as

.. math::
   :label: x-mass

   
   X^{*}=\sum ^{m}_{i=1}x_{i}^{*}(u_{i}^{*},\, \Delta \tau ,\, \delta
   p_{i}^{\theta }) ,

.. math::
   :label: y-mass

   
   Y^{*}=\sum _{i=1}^{m}y_{i}^{*}(v_{i}^{*},\, \Delta \tau ,\, \delta
   p_{i}^{\lambda }) .

The time-averaged winds :math:`(U^{*},V^{*})`, defined as follows, are
to be used as input for the computations of :math:`q^{\lambda }` and
:math:`
q^{\theta }:`

.. math::
   :label: u-wind

   U^{*}=\frac{1}{m}\sum ^{m}_{i=1}u_{i}^{*} ,

.. math::
   :label: v-wind

   V^{*}=\frac{1}{m}\sum ^{m}_{i=1}v_{i}^{*} .

The use of the time accumulated mass fluxes and the time-averaged winds
for the large-time-step tracer transport in the manner described above
ensures the conservation of the tracer mass and maintains the highest
degree of consistency possible given the time split integration
procedure. A graphical illustration of the different levels of
sub-cycling in CAM5 is given on Figure [fig:subc].

.. _figure-1:

.. figure:: figures/dt.jpg
   :align: center
   
   Figure 3.1: A graphical illustration of the different levels of sub-cycling in CAM5.

The algorithm described here can be readily applied to a regional model
if appropriate boundary conditions are supplied. There is formally no
Courant number related time step restriction associated with the
transport processes. There is, however, a stability condition imposed by
the gravity-wave processes. For application on the whole sphere, it is
computationally advantageous to apply a polar filter to allow a dramatic
increase of the size of the small time step :math:`\Delta
\tau`. The effect of the polar filter is to stabilize the
short-in-wavelength (and high-in-frequency) gravity waves that are being
unnecessarily and unidirectionally resolved at very high latitudes in
the zonal direction. To minimize the impact to meteorologically
significant larger scale waves, the polar filter is highly scale
selective and is applied only to the diagnostic variables on the
auxiliary C-grid and the tendency terms in the D-grid momentum
equations. No polar filter is applied directly to any of the prognostic
variables.

The design of the polar filter follows closely that of :cite:`suarez95`
for the C-grid Arakawa type dynamical core (*e.g*., :cite:`arakawa81`). 
For the |cam| the fast-fourier transform component of the polar
filtering has replaced the algebraic form at all filtering latitudes.
Because our prognostic variables are computed on the D-grid and the fact
that the FFSL transport scheme is stable for Courant number greater than
one, in realistic test cases the maximum size of the time step is about
two to three times larger than a model based on Arakawa and Lamb’s
C-grid differencing scheme. It is possible to avoid the use of the polar
filter if, for example, the “Cubed grid” is chosen, instead of the
current latitude-longitude grid. rewrite of the rest of the model codes
including physics parameterizations, the land model, and most of the
post processing packages.

The size of the small time step for the Lagrangian dynamics is only a
function of the horizontal resolution. Applying the polar filter, for
the 2-degree horizontal resolution, a small-time-step size of 450
seconds can be used for the Lagrangian dynamics. From the
large-time-step transport perspective, the small-time-step integration
of the 2D Lagrangian dynamics can be regarded as a very accurate
iterative solver, with *m* iterations, for computing the time mean winds
and the mass fluxes, analogous in functionality to a semi-implicit
algorithm’s elliptic solver (*e.g*., :cite:`ringler00`). Besides accuracy, the merit of an “explicit” versus
“semi-implicit” algorithm ultimately depends on the computational
efficiency of each approach. In light of the advantage of the explicit
algorithm in parallelization, we do not regard the explicit algorithm
for the Lagrangian dynamics as an impedance to computational efficiency,
particularly on modern parallel computing platforms.

Optional diffusion operators in CAM5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ‘CD’-grid discretization method used in the CAM finite-volume
dynamical core provides explicit control over the rotational modes at
the grid scale, due to monotonicity constraint in the PPM-based
advection, but there is no explicit control over the divergent modes at
the grid scale Skamarock (see, e.g., 2010). Therefore divergence damping
terms appear on the right-hand side of the momentum equations :eq:`u-lcv`
and :eq:`v-lcv`:

.. math::
   :label: eq:div2u
   
   -\frac{1}{Acos\theta }\left[
   \frac{\partial }{\partial \lambda }\left( -\nu D\right) \right]

and

.. math::
   :label: eq:div2v

   
   -\frac{1}{A}\left[
   \frac{\partial }{\partial \theta }\left( -\nu D\right)
   \right] ,

respectively, where the strength of the divergence damping is
controlled by the coefficient :math:`\nu` given by

.. math::
   :label: eq:nu2

   
   \nu  = \frac{\nu_2\, (A^2\Delta \lambda \Delta \theta)}{\Delta t},

where :math:`\nu_2=1/128` throughout the atmosphere except in the top
model levels where it monotonically increases to approximately
:math:`4/128` at the top of the atmosphere. The divergence damping
described above is referred to as ‘second-order’ divergence damping as
it effectively damps divergence with a :math:`\nabla^2` operator.

In CAM5 optional ‘fourth-order’ divergence damping has been implemented
where the divergence is effectively damped with a
:math:`\nabla^4`-operator which is usually more scale selective than
‘second-order’ damping operators. For ‘fourth-order’ divergence damping
the terms

.. math::
   :label: eq:div4u

   
   -\frac{1}{Acos\theta }\left[
   \frac{\partial }{\partial \lambda }\left( -\nu_4 \nabla^2 D\right) \right]

and

.. math::
   :label: eq:div4v

   
   -\frac{1}{A}\left[
   \frac{\partial }{\partial \theta }\left( -\nu_4\nabla^2 D\right)
   \right] ,

are added to the right-hand side of ([u-lcv]) and ([v-lcv]),
respectively. The horizontal Laplacian :math:`\nabla^2`-operator in
spherical coordinates for a scalar :math:`\psi` is given by

.. math:: \nabla^2\psi=\frac{1}{A^2\cos^2 \theta}\frac{\partial^2 \psi}{\partial^2 \lambda}+\frac{1}{A^2\cos \theta}\frac{\partial }{\partial \theta}\left( \cos \theta \frac{\partial \psi}{\partial \theta}\right).

The fourth-order divergence damping coefficient is given by

.. math::
   :label: eq:nu4

   
   \nu_{4}=0.01\,  \left(A^2 \cos(\theta) \Delta \lambda \Delta \theta\right)^2/\Delta t.

Since divergence damping is added explicitly to the equations of motion
it is unstable if the time-step is too large or the damping coefficients
(:math:`\nu` or :math:`\nu_4`) are too large. To stabilize the
fourth-order divergence damping the winds used to compute the divergence
are filtered using the same FFT filtering which is applied to stabilize
the gravity waves.

To control potentially excessive polar night jets in high-resolution
configurations of CAM, Laplacian damping of the wind components has been
added as an option in CAM5. That is, the terms

.. math::
   :label: eq:del2u

   
   \nu_{del2}\nabla^2 u

and

.. math::
   :label: eq:del2v

   
   \nu_{del2}\nabla^2 v

are added to the right-hand side of the momentum equations ([u-lcv])
and ([v-lcv]), respectively. The damping coefficient :math:`\nu_{del2}`
is zero throughout the atmosphere except in the top layers where it
increases monotonically and smoothly from zero to approximately four
times a user-specified damping coefficient at the top of the atmosphere
(the user-specified damping coefficient is typically on the order of
:math:`2.5\times 10^5` m\ :math:`^2`\ sec\ :math:`^{-1}`).

.. _FVmap:

A mass, momentum, and total energy conserving mapping algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Lagrangian surfaces that bound the finite-volume will eventually
deform, particularly in the presence of persistent diabatic
heating/cooling, in a time scale of a few hours to a day depending on
the strength of the heating and cooling, to a degree that it will
negatively impact the accuracy of the
horizontal-to-Lagrangian-coordinate transport and the computation of the
pressure gradient forces. Therefore, a key to the success of the
Lagrangian control-volume discretization is an accurate and conservative
algorithm for mapping the deformed Lagrangian coordinate back to a fixed
reference Eulerian coordinate.

There are some degrees of freedom in the design of the vertical mapping
algorithm. To ensure conservation, our current (and recommended) mapping
algorithm is based on the reconstruction of the “mass” (pressure
thickness :math:`\delta p`), zonal and meridional “winds”, “tracer
mixing ratios”, and “total energy” (volume integrated sum of the
internal, potential, and kinetic energy), using the monotonic Piecewise
Parabolic sub-grid distributions with the hydrostatic pressure (as
defined by ([L-coord])) as the mapping coordinate. We outline the
mapping procedure as follows.

    **Step 1**: Define a suitable Eulerian reference coordinate as a
    target coordinate. The mass in each layer (:math:`\delta p`) is
    then distributed vertically according to the chosen Eulerian
    coordinate. The surface pressure typically plays an “anchoring” role
    in defining the terrain following Eulerian vertical coordinate. The
    hybrid :math:`\eta -coordinate` used in the NCAR CCM3 (:cite:`kiehl96`) is adopted in the
    current model setup.

    **Step 2**: Construct the piece-wise continuous vertical subgrid
    profiles of tracer mixing ratios (:math:`q`), zonal and meridional
    winds (*u* and *v*), and total energy (:math:`\Gamma`) in the
    Lagrangian control-volume coordinate, or the source coordinate. The
    total energy :math:`\Gamma` is computed as the sum of the
    finite-volume integrated geopotential :math:`\phi`, internal energy :math:`(C_{v}T_{v})`, and the kinetic
    energy (:math:`K`) as follows:

    .. math::
       :label: int-t
       
       \Gamma =\frac{1}{\delta p}\int \left[ C_{v}T_{v}+\phi +\frac{1}{2}\left(
       u^{2}+v^{2}\right) \right] dp .

    Applying integration by parts and the ideal gas law, the above
    integral can be rewritten as

    .. math::
       :label: TE_fv

       \begin{aligned}
       \Gamma & = & \frac{1}{\delta
       p}\left\{\int\left[C_{p}T_{v}+\frac{1}{2}\left(u^{2}+v^{2}\right)\right]
       dp + \int d\left(p\phi\right)\right\} \nonumber \\
       & = & C_{p}\overline{T_{v}}+\frac{1}{\delta p}\delta \left( p\phi
       \right) +K ,\end{aligned}

    where :math:`\overline{T_{v}}` is the layer mean virtual
    temperature, :math:`K` is the layer mean kinetic energy, :math:`p` is the pressure at
    layer edges, and :math:`C_{v}` and :math:`C_{p}` are the
    specific heat of the air at constant volume and at constant
    pressure, respectively. The total energy in each grid cell is
    calculated as

    .. math::

       \begin{aligned}
       \Gamma_{i,j,k} & = & C_{p}T_{v_{i,j,k}}+\frac{1}{\delta p_{i,j,k}}\left(p_{i,j,k+\frac{1}{2}}
       \phi_{i,j,k+\frac{1}{2}}-p_{i,j,k-\frac{1}{2}}\phi_{i,j,k-\frac{1}{2}}
       \right)+ \nonumber \\
       & &\frac{1}{2}\left(\frac{u^{2}_{i,j-\frac{1}{2},k}+u^{2}_{i,j+\frac{1}{2},k}}{2}+
       \frac{v^{2}_{i-\frac{1}{2},j,k}+v^{2}_{i+\frac{1}{2},j,k}}{2}\right) \nonumber\end{aligned}

    The method employed to create subgrid profiles is set by the flag
    :math:`te\_method`. For :math:`te\_method` = 0 (default), the
    Piece-wise Parabolic Method (PPM, :cite:`colella84`) over
    a pressure coordinate is used and for :math:`te\_method = 1` a
    cublic spline over a logarithmic pressure coordinate is used.

    **Step 3**: Layer mean values of :math:`q`, (*u*, *v*), and
    :math:`\Gamma` in the Eulerian coordinate system are obtained by
    integrating analytically the sub-grid distributions, in the vertical
    direction, from model top to the surface, layer by layer. Since the
    hydrostatic pressure is chosen as the mapping coordinate, tracer
    mass, momentum, and total energy are locally and globally conserved.
    In mapping a variable from the source coordinate to the target
    coordinate, different limiter constraints may be used and they are
    controlled by two flags, :math:`iv` and :math:`kord`. For winds on
    D-grid, :math:`iv` should be set to -1. For tracers, :math:`iv`
    should be set to 0. For all others, :math:`iv = 1`. :math:`kord`
    directly controls which limiter constraint is used. For
    :math:`kord \ge 7`, Huynh’s 2nd constraint is used. If
    :math:`kord = 7`, the original quasi-monotonic constraint is used.
    If :math:`kord > 7`, a full monotonic constraint is used. If
    :math:`kord` is less than 7, the variable, :math:`lmt`, is
    determined by the following:

    .. math::

       \begin{aligned}
       lmt & = & kord - 3, \nonumber \\
       lmt & = & \mathrm{max}(0,lmt), \nonumber \\
       \mathrm{if} (iv = 0) \quad lmt & = & \mathrm{min}(2,lmt). \nonumber \nonumber\end{aligned}

    If :math:`lmt = 0`, a standard PPM constraint is used. If
    :math:`lmt = 1`, an improved full monotonicity constraint is used. If
    :math:`lmt = 2`, a positive definite constraint is used. If
    :math:`lmt = 3`, the algorithm will do nothing.

    **Step 4**: Retrieve virtual temperature in the Eulerian (target)
    coordinate. Start by computing kinetic energy in the Eulerian
    coordinate system for each layer. Then substitute kinetic energy and
    the hydrostatic relationship into ([TE:sub:`f`\ v]). The layer mean
    temperature :math:`\overline{T_{v}}_{k}` for layer :math:`k` in the Eulerian
    coordinate is then retrieved from the reconstructed total energy
    (done in Step 3) by a fully explicit integration procedure starting
    from the surface up to the model top as follows:

    .. math::
       :label: map-t

       \overline{T_{v}}_{k}=\frac{\Gamma _{k}-K_{k}-\phi
       _{k+\frac{1}{2}}}{C_{p}\left[ 1-\kappa \, p_{k-\frac{1}{2}}\frac{ln\,
       p_{k+\frac{1}{2}}-ln\,
       p_{k-\frac{1}{2}}}{p_{k+\frac{1}{2}}-p_{k-\frac{1}{2}}}\right] },

    where :math:`\kappa = R_{d}/C_{p}` and :math:`R_{d}` is the gas
    constant for dry air.

To convert the potential virtual temperature :math:`\Theta_{v}` to the
layer mean temperature the conversion factor is obtained by equating the
following two equivalent forms of the hydrostatic relation for :math:`\Theta` and :math:`\overline{T_{v}}:`

.. math::
   :label: hydro-PT

   \delta \phi =-C_{p}\Theta_{v} \, \delta \Pi ,

.. math::
   :label: hydro-T

   \delta \phi =-R_{d}\overline{T_{v}}\, \delta ln\, p ,

where :math:`\Pi =p^{\kappa }`. The conversion formula between layer
mean temperature and layer mean potential temperature is obtained as
follows:

.. math::
   :label: convt
   
   \Theta_{v} =\kappa \frac{\delta ln p }{\delta \Pi }\overline{T_{v}} .

The physical implication of retrieving the layer mean temperature from
the total energy as described in Step 3 is that the dissipated kinetic
energy, if any, is locally converted into internal energy via the
vertically sub-grid mixing (dissipation) processes. Due to the
monotonicity preserving nature of the sub-grid reconstruction the
column-integrated kinetic energy inevitably decreases (dissipates),
which leads to local frictional heating. The frictional heating is a
physical process that maintains the conservation of the total energy in
a closed system.

As viewed by an observer riding on the Lagrangian surfaces, the mapping
procedure essentially performs the physical function of the
relative-to-the-Eulerian-coordinate vertical transport, by vertically
redistributing (air and tracer) mass, momentum, and total energy from
the Lagrangian control-volume back to the Eulerian framework.

As described in section [FVvdisc], the model time integration cycle
consists of :math:`m` small time steps for the 2D Lagrangian dynamics
and one large time step for tracer transport. The mapping time step can
be much larger than that used for the large-time-step tracer transport.
In tests using the Held-Suarez forcing (:cite:`held94`), a
three-hour mapping time interval is found to be adequate. In the full
model integration, one may choose the same time step used for the
physical parameterizations so as to ensure the input state variables to
physical parameterizations are in the usual “Eulerian” vertical
coordinate. In CAM5, vertical remapping takes place at each physics time
step.

A geopotential conserving mapping algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An alternative vertical mapping approach is available in CAM5. Instead
of retrieving temperature by remapped total energy in the Eulerian
coordinate, the alternative approach maps temperature directly from the
Lagrangian coordinate to the Eulerian coordinate. Since geopotential is
defined as

.. math::

   \begin{aligned}
   \delta \phi = -C_{p} \Theta_{v} \delta \Pi = -R_{d} T_{v} \delta ln\,p, \nonumber\end{aligned}

mapping :math:`\Theta_{v}` over :math:`\Pi` or :math:`T_{v}` over
:math:`ln\,p` preserves the geopotential at the model lid. This approach
prevents the mapping procedure from generating spurious pressure
gradient forces at the model lid. Unlike the energy-conserving algorithm
which could produce substantial temperature fluctuations at the model
lid, the geopotential conserving approach guarantees a smooth
(potential) temperature profile. However, the geopotential conserving
does not conserve total energy in the remapping procedure. This may be
resolved by a global energy fixer already implemented in the model (see
section [sec:Global-Energy-Fixer]).

.. _FVqconserve:

Adjustment of pressure to include change in mass of water vapor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The physics parameterizations operate on a model state provided by the
dynamics, and are allowed to update specific humidity. However, the
surface pressure remains fixed throughout the physics updates, and since
there is an explicit relationship between the surface pressure and the
air mass within each layer, the total air mass must remain fixed as well
throughout the physics updates. If no further correction were made, this
would imply that the dry air mass changed if the water vapor mass
changed in the physics updates. Therefore the pressure field is changed
to include the change in water vapor mass due to the physics updates. We
impose the restrictions that dry air mass and water mass are conserved
as follows:

The total pressure :math:`p` is

.. math:: p = d + e .

with dry pressure :math:`d`, water vapor pressure :math:`e`. The
specific humidity is

.. math:: q = \frac{e}{p} = \frac{e}{d+e}, \qquad d = (1-q) p .

We define a layer thickness as :math:`\delta^k p \equiv p^{k+1/2} -
p^{k-1/2}`, so

.. math:: \delta^k d = (1-q^k)\delta^k p .

We are concerned about 3 time levels: :math:`q_n` is input to physics,
:math:`q_{n*}` is output from physics, :math:`q_{n+1}` is the adjusted
value for dynamics.

Dry mass is the same at :math:`n` and :math:`n+1` but not at :math:`n*`.
To conserve dry mass, we require that

.. math:: \delta^k d_n	= \delta^k d_{n+1}

or

.. math::
   :label: eq:drydif

   (1-q^k_n)\delta^k p_n = (1-q^k_{n+1})\delta^k p_{n+1}
      .

Water mass is the same at :math:`n*` and :math:`n+1`, but not at
:math:`n`. To conserve water mass, we require that

.. math:: 
   :label: eq:wetdif

   q^k_{n*} \delta^k p_n = q^k_{n+1}\delta^k p_{n+1}  .

Substituting ([eq:wetdif]) into ([eq:drydif]),

.. math:: (1-q^k_n)\delta^k p_n  = \delta^k p_{n+1} - q^k_{n*} \delta^k p_n

.. math:: \delta^k p_{n+1} = (1 - q^k_n +  q^k_{n*})\delta^k p_n

which yields a modified specific humidity for the dynamics:

.. math::

   q^k_{n+1} = q^k_n \frac{\delta^k p_n}{\delta^k p_{n+1}} =
    \frac{q^k_{n*}}{1 - q^k_n +  q^k_{n*}} .

We note that this correction as implemented makes a small change to the
water vapor as well. The pressure correction could be formulated to
leave the water vapor unchanged.

Negative Tracer Fixer
~~~~~~~~~~~~~~~~~~~~~

In the Finite Volume dynamical core, neither the monotonic transport nor
the conservative vertical remapping guarantee that tracers will remain
positive definite. Thus the Finite Volume dynamical core includes a
negative tracer fixer applied before the parameterizations are
calculated. For negative mixing ratios produced by horizontal transport,
the model will attempt to borrow mass from the east and west neighboring
cells. In practice, most negative values are introduced by the vertical
remapping which does not guarantee positive definiteness in the first
and last layer of the vertical column.

A minimum value :math:`q_{min}` is defined for each tracer. If the
tracer falls below that minimum value, it is set to that minimum value.
If there is enough mass of the tracer in the layer immediately above,
tracer mass is removed from that layer to conserve the total mass in the
column. If there is not enough mass in the layer immediately above, no
compensation is applied, violating conservation. Usually such
computational sources are very small.

The amount of tracer needed from the layer above to bring :math:`q_k` up
to :math:`q_{min}` is

.. math:: q_{fill} = \left(q_{min} - q_k \right){\Delta p_k \over \Delta p_{k-1}}

where :math:`k` is the vertical index, increasing downward. After the
filling

.. math:: q_{k_{FILLED}} = q_{min}

.. math:: q_{{k-1}_{FILLED}} = q_{k-1} - q_{fill}

Currently :math:`q_{min} = 1.0 \times 10^{-12}` for water vapor,
:math:`q_{min} = 0.0` for CLDLIQ, CLDICE, NUMLIQ and NUMICE, and
:math:`q_{min} = 1.0 \times 10^{-36}` for the remaining constituents.

Global Energy Fixer
~~~~~~~~~~~~~~~~~~~

The finite-volume dynamical core as implemented in CAM and described
here conserves the dry air and all other tracer mass exactly without a
“mass fixer”. The vertical Lagrangian discretization and the associated
remapping conserves the total energy exactly. The only remaining issue
regarding conservation of the total energy is the horizontal
discretization and the use of the “diffusive” transport scheme with
monotonicity constraint. To compensate for the loss of total energy due
to horizontal discretization, we apply a global fixer to add the loss in
kinetic energy due to “diffusion” back to the thermodynamic equation so
that the total energy is conserved. The loss in total energy (in flux
unit) is found to be around 2 :math:`(W/m^{2}`) with the 2 degrees
resolution.

The energy fixer is applied following the negative tracer fixer. The
fixer is applied on the unstaggered physics grid rather than on the
staggered dynamics grid. The energies on these two grids are difficult
to relate because of the nonlinear terms in the energy definition and
the interpolation of the state variables between the grids. The energy
is calculated in the parameterization suite before the state is passed
to the finite volume core as described in the beginning of Chapter
[chap:model:sub:`p`\ hysics]. The fixer is applied just before the
parameterizations are calculated. The fixer is a simplification of the
fixer in the Eulerian dynamical core described in section [energyfixer].

Let minus sign superscript :math:`(~~)^-` denote the values at the
beginning of the dynamics time step, i.e. after the parameterizations
are applied, let a plus sign superscript :math:`(~~)^+` denote the
values after fixer is applied, and let a hat :math:`\hat{(~~)}^+` denote
the provisional value before adjustment. The total energy over the
entire computational domain after the fixer is

.. math::

   E^+
    =\int_{p_t}^{p_s}\int_{0}^{2\pi}\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}} {1 \over g} \left[ C_p T^+ + \Phi + {1 \over 2}
     \left( {u^+}^2 + {v^+}^2 \right)+\left(L_v + L_i\right) q^+_v + L_i q^+_\ell \right] A^2\cos\theta \,d\theta
    \,d\lambda\,dp,

where :math:`L_v` is the latent heat of vaporation, :math:`L_i` is the
latent heat of fusion, :math:`q_v` is water vapor mixing ratio, and
:math:`q_\ell` is cloud water mixing ratio. :math:`E^+` should equal the
energy at the beginning of the dynamics time step

.. math::

   E^-
    =\int_{p_t}^{p_s}\int_{0}^{2\pi}\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}{1 \over g} \left[ c_p T^- + \Phi + {1 \over 2}
     \left( {u^-}^2 + {v^-}^2 \right)+\left(L_v + L_i\right) q^-_v + L_i q^-_\ell \right]  A^2\cos\theta \,d\theta
    \,d\lambda\,dp.

Let :math:`\hat E^+` denote the energy of the provisional state
provided by the dynamical core before the adjustment.

.. math::

   \hat E^+
    =\int_{p_t}^{p_s}\int_{0}^{2\pi}\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}
     {1 \over g} \left[ c_p \hat T^+ + \hat \Phi^+ + {1 \over 2}
     \left( {\hat u}^{+^2} + {\hat v}^{+^2} \right)+ \left(L_v +
     L_i\right) \hat q^+_v + L_i \hat q^+_\ell\right] A^2\cos\theta \,d\theta
    \,d\lambda\,dp.

Thus, the total energy added into the system by the dynamical core is
:math:`\hat E^+ - E^-`. The energy fixer then changes dry static energy
(:math:`s = C_p T + \Phi`) by a constant amount over each grid cell to
conserve total energy in the entire computational domain. The dry static
energy added to each grid cell may be expressed as

.. math::

   \Delta s = \frac{E^- - \hat
   E^+}{\int_{p_t}^{p_s}\int_{0}^{2\pi}\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}
   A^2\cos\theta \,d\theta
    \,d\lambda\,\frac{dp}{g}}.

Therefore,

.. math:: s^+ = \hat s^+ + \Delta s,

or

.. math::
   :label: dry_static_eqn

   
   C_p T^+ + \Phi^+ = \hat s^+ + \Delta s.

This will ensure :math:`E^+ = E^-`.

By hydrostatic approximation, the geopotential equation is

.. math:: d\Phi = -R_d T_v d\,lnp,

and for any arbitrary point between :math:`p_{k+\frac{1}{2}}` and
:math:`p_{k-\frac{1}{2}}` the geopotential may be written as

.. math::

   \begin{aligned}
   \int^{\Phi}_{\Phi_{k+\frac{1}{2}}}\,d\Phi' & = & -R_d T_v
   \int^{p}_{p_{k+\frac{1}{2}}}\,d\,lnp', \\
   \Phi & = & \Phi_{k+\frac{1}{2}}+R_d T_v \left(lnp_{k+\frac{1}{2}}-lnp\right).\end{aligned}

The geopotential at the mid point of a model layer between
:math:`p_{k+\frac{1}{2}}` and :math:`p_{k-\frac{1}{2}}`, or the layer
mean, is

.. math::

   \begin{aligned}
   \Phi_k & = &
   \frac{\int_{p_k-\frac{1}{2}}^{p_k+\frac{1}{2}}\Phi\,dp}{\int_{p_k-\frac{1}{2}}^{p_k+\frac{1}{2}}\,dp}
   \nonumber \\
   & = & \frac{\int_{p_k-\frac{1}{2}}^{p_k+\frac{1}{2}} \left[\Phi_{k+\frac{1}{2}}+R_d T_v \left(lnp_{k+\frac{1}{2}}-lnp\right)
   \right]
   \,dp}{\int_{p_k-\frac{1}{2}}^{p_k+\frac{1}{2}}\,dp} \nonumber \\
   & = & \Phi_{k+\frac{1}{2}}+R_d T_v lnp_{k+\frac{1}{2}} -
    \frac{\int_{p_k-\frac{1}{2}}^{p_k+\frac{1}{2}}lnp
    \,dp}{p_{k+\frac{1}{2}}-p_{k-\frac{1}{2}}} \nonumber \\
   & = & \Phi_{k+\frac{1}{2}}+R_d T_v
    \left(1-p_{k-\frac{1}{2}}\frac{lnp_{k+\frac{1}{2}}-lnp_{k-\frac{1}{2}}}{p_{k+\frac{1}{2}}
   -p_{k-\frac{1}{2}}}\right)\end{aligned}

For layer :math:`k`, the energy fixer will solve the following equation
based on ([dry:sub:`s`\ tatic\ :sub:`e`\ qn]),

.. math::

   \begin{aligned}
   C_p T^+_k + \Phi^+_{k+\frac{1}{2}}+R_d T_{k}^+\left(1+\epsilon q^+_{v_{k}}\right)
   \left(1-p^+_{k-\frac{1}{2}}\frac{lnp^+_{k+\frac{1}{2}}-lnp^+_{k-\frac{1}{2}}}{p^+_{k+\frac{1}{2}}
   -p^+_{k-\frac{1}{2}}}\right)  =  \hat s^+ +\Delta s.\end{aligned}

Since the energy fixer will not alter the water vapor mixing ratio and
the pressure field,

.. math::

   \begin{aligned}
   q^+_v & = & \hat q^+_v, \\
   p^+ & = & \hat p^+.\end{aligned}

Therefore,

.. math::

   T^+_k = \frac{\left(\hat s^+ +\Delta s\right) - \Phi^+_{k+\frac{1}{2}}}{C_p+R_d\left(1+\epsilon
   \hat q^+_{v_{k}}\right)\left(1-\hat p^+_{k-\frac{1}{2}}\frac{ln\hat
   p^+_{k+\frac{1}{2}}-ln\hat p^+_{k-\frac{1}{2}}}{\hat p^+_{k+\frac{1}{2}}
   -\hat p^+_{k-\frac{1}{2}}}\right)}.

The energy fixer starts from the Earth’s surface and works its way up to
the model top in adjusting the temperature field. At the surface layer,
:math:`\Phi^+_{k+\frac{1}{2}} = \Phi_s`. After the temperature is
adjusted in a grid cell, the geopotential at the upper interface of the
cell is updated which is needed for the temperature adjustment in the
grid cell above.

Further discussion
~~~~~~~~~~~~~~~~~~

There are still aspects of the numerical formulation in the finite
volume dynamical core that can be further improved. For example, the
choice of the horizontal grid, the computational efficiency of the
split-explicit time marching scheme, the choice of the various
monotonicity constraints, and how the conservation of total energy is
achieved.

The impact of the non-linear diffusion associated with the monotonicity
constraint is difficult to assess. All discrete schemes must address the
problem of subgrid-scale mixing. The finite-volume algorithm contains a
non-linear diffusion that mixes strongly when monotonicity principles
are locally violated. However, the effect of nonlinear diffusion due to
the imposed monotonicity constraint diminishes quickly as the resolution
matches better to the spatial structure of the flow. In other numerical
schemes, however, an explicit (and tunable) linear diffusion is often
added to the equations to provide the subgrid-scale mixing as well as to
smooth and/or stabilize the time marching.

Specified Dynamics Option 
~~~~~~~~~~~~~~~~~~~~~~~~~~

In CAM4 the capability included to perform simulations using specified
dynamics, where offline meteorological fields are nudged to the online
calculated meteorology. This procedure was originally used in the Model
of Atmospheric Transport and Chemistry (MATCH) (Rasch et al., 1997). In
this procedure the horizontal wind components, air temperature, surface
temperature, surface pressure, sensible and latent heat flux, and wind
stress are read into the model simulation from the input meteorological
dataset. The nudging coefficient can be chosen to be 1 (for 100%
nudging) or smaller. The desired percentage of the offline meteorology
and the remaining percent from the internally calcuated meteorology is
used every timestep to prescribe the meteorological parameters. In
addition, the model solves the model internal advection equations for
the mass flux every sub-step. In this way, some inconsistencies between
the inserted and model-computed velocity and mass fields subsequently
used for tracer transport are dampended. The mass flux at each sub-step
is accumulated to produce the net mass flux over the entire time step. A
graphical explanation of the sub-cycling is given in Lauritzen et al.
(2011).

A nudging coefficent of 100 can be used to allow for more precise
comparisons between measurements of atmospheric composition and model
output for example using CAM-Chem (Lamarque et al., 2012). A reduced
nudging coefficent is used for instant for WACCM simulations, if more of
the internal transport parameters needs to be contained, while the
meteorology is still close to the analysied fields (e.g., Brakebusch et
al., 2012).

Currently, we recommend for input offline meteorology interpolated from
0.5x0.6 degree fields of the NASA Goddard Global Modeling and
Assimilation Office (GMAO) GEOS-5 and Modern Era Retrospective-Analysis
For Research And Applications (MERRA) generated meteorology. These
fields are available on the Earth System Grid
(http://www.earthsystemgrid.org/home.htm) for the CAM resolution of
1.9\ :math:`^\circ`\ x2.5\ :math:`^\circ`. These files were generated
from the original resolution by using a conservative regridding
procedure based on the same 1-D operators as used in the transport
scheme of the finite-volume dynamical core used in GEOS-5 and CAM (S.-J.
Lin, personal communication, 2009). Note that because of a difference in
the sign convention of the surface wind stress (TAUX and TAUY) between
CESM and GEOS5/MERRA, these fields in the interpolated datasets have
been reversed from the original files supplied by GMAO. In addition, it
is important for users to recognize the importance of specifying the
correct surface geopotential height (PHIS) to ensure consistency with
the input dynamical fields, which is important to prevent unrealistic
vertical mixing.

Further discussion
~~~~~~~~~~~~~~~~~~

.. _s-intro:

Spectral Element Dynamical Core
-------------------------------

The CAM includes an optional dynamical core from HOMME, NCAR's
High-Order Method Modeling Environment :cite:`dennis05`.  The stand-alone
HOMME is used for research in several different types of dynamical
cores.  The dynamical core incorporated into CAM4 uses HOMME's
continuous Galerkin spectral finite element method 
:cite:`taylor97`,:cite:`fournier04`,:cite:`thomas05`,:cite:`wang07`,:cite:`taylor10b`,
here abbreviated to the spectral element method (SEM).  This method
is designed for fully unstructured quadrilateral meshes.  The current
configurations in the CAM are based on the cubed-sphere grid.  The main
motivation for the inclusion of HOMME is to improve the scalability of
the CAM by introducing quasi-uniform grids which require no polar
filters :cite:`taylor08`.  HOMME is also the first dynamical core
in the CAM which locally conserves energy in
addition to mass and two-dimensional potential vorticity :cite:`taylor10a`.

HOMME represents a large change in the horizontal grid as compared to
the other dynamical cores in CAM.  Almost all other aspects of HOMME
are based on a combination of well-tested approaches from the Eulerian
and FV dynamical cores.  For tracer advection, HOMME is modeled as
closely as possible on the FV core.  It uses the same
conservation form of the transport equation and the same vertically
Lagrangian discretization :cite:`lin04`.  The HOMME dynamics are
modeled as closely as possible on Eulerian core.  They share
the same vertical coordinate, vertical discretization, hyper-viscosity
based horizontal diffusion, top-of-model dissipation, and solve the
same moist hydrostatic equations.  The main differences are that HOMME
advects the surface pressure instead of its logarithm (in order to
conserve mass and energy), and HOMME uses the vector-invariant form of
the momentum equation instead of the vorticity-divergence formulation.
Several dry dynamical cores including HOMME are evaluated in
:cite:`lauritzen09` using a grid-rotated version of the
baroclinic instability test case :cite:`jablonowski06`.  


The timestepping in HOMME is a form of dynamics/tracer/physics
subcycling, achieved through the use of multi-stage 2nd order accurate
Runge-Kutta methods. The tracers and dynamics use the same timestep
which is controlled by the maximum anticipated wind speed, but the
dynamics uses more stages than the tracers in order to maintain
stability in the presence of gravity waves. The forcing is applied using
a time-split approach. The optimal forcing strategy in HOMME has not yet
been determined, so HOMME supports several options. The first option is
modeled after the FV dynamical core and the forcing is applied as an
adjustment at each physics timestep. The second option is to convert all
forcings into tendencies which are applied at the end of each
dynamics/tracer timestep. If the physics timestep is larger than the
tracer timestep, then the tendencies are held fixed and only updated at
each physics timestep. Finally, a hybrid approach can be used where the
tracer tendencies are applied as in the first option and the dynamics
tendencies are applied as in the second option.

Continuum Formulation of the Equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HOMME uses a conventional vector-invariant form of the moist primitive
equations. For the vertical discretization it uses the hybrid
:math:`\eta` pressure vertical coordinate system modeled after
[eul:terrain] The formulation here differs only in that surface pressure
is used as a prognostic variable as opposed to its logarithm.

In the :math:`\eta`-coordinate system, the pressure is given by

.. math:: p(\eta) = A(\eta) p_0 + B(\eta) p_s.

The hydrostatic approximation
:math:`\partial p / \partial z  = - g \rho` is used to replace the
mass density :math:`\rho` by an :math:`\eta`-coordinate pseudo-density
:math:`\partial p / \partial \eta`. The material derivative in
:math:`\eta`-coordinates can be written (e.g. (e.g. :cite:`satoh04`, Sec.3.3),

.. math:: \frac{ D X }{D t} = {{\frac{\partial {X}}{\partial t}}} + {{{\smash[t]{\vec{u}}}}}\cdot {\nabla}X + {{\dot\eta}}{\frac{\partial {X}}{\partial \eta}}

where the :math:`{\nabla}()` operator (as well as
:math:`{\nabla\cdot}()` and :math:`{{{\nabla}\times}}()` below) is the
two-dimensional gradient on constant :math:`\eta`-surfaces,
:math:`\partial / \partial \eta` is the vertical derivative,
:math:`{{\dot\eta}}= D\eta/Dt` is a vertical flow velocity and
:math:`{{{\smash[t]{\vec{u}}}}}` is the horizontal velocity component
(tangent to constant :math:`z`-surfaces, not :math:`\eta`-surfaces).

The :math:`\eta`-coordinate atmospheric primitive equations, neglecting
dissipation and forcing terms can then be written as

.. math::
   :label: E:PEmom

   \begin{aligned}
   {{\frac{\partial {{{{\smash[t]{\vec{u}}}}}}}{\partial t}}} + \left( {{\mathbf{\zeta}}}+ f \right) {\hat{k}}{{\times}}{{{\smash[t]{\vec{u}}}}}+
   {\nabla}\left( \frac12 {{{\smash[t]{\vec{u}}}}}^2 + \Phi \right)  +
   {{\dot\eta}}{\frac{\partial {{{{\smash[t]{\vec{u}}}}}}}{\partial \eta}} + \frac{RT_v}{p} {\nabla}p &= 0 
    \\
   {{\frac{\partial {T}}{\partial t}}} + {{{\smash[t]{\vec{u}}}}}\cdot {\nabla}T + {{\dot\eta}}{\frac{\partial {T}}{\partial \eta}} - 
   \frac{RT_v}{c^*_p p} \omega  &= 0 
   \\
   {{\frac{\partial {}}{\partial t}}}\left({\frac{\partial {p}}{\partial \eta}}\right) + {\nabla\cdot}\left( {\frac{\partial {p}}{\partial \eta}}{{{\smash[t]{\vec{u}}}}}\right) + 
   {\frac{\partial {}}{\partial \eta}} \left( {{\dot\eta}}{\frac{\partial {p}}{\partial \eta}}\right) &= 0  
   \\
   {{\frac{\partial {}}{\partial t}}} \left( {\frac{\partial {p}}{\partial \eta}}q \right) +  {\nabla\cdot}\left( {\frac{\partial {p}}{\partial \eta}}q {{{\smash[t]{\vec{u}}}}}\right) + 
   {\frac{\partial {}}{\partial \eta}} \left( {{\dot\eta}}{\frac{\partial {p}}{\partial \eta}}q \right) &= 0.
   \end{aligned}

These are prognostic equations for :math:`{{{\smash[t]{\vec{u}}}}}`, the
temperature :math:`T`, density
:math:`{\frac{\partial {p}}{\partial \eta}}`, and
:math:`{\frac{\partial {p}}{\partial \eta}}q` where :math:`q` is the
specific humidity. The prognostic variables are functions of time
:math:`t`, vertical coordinate :math:`\eta` and two coordinates
describing the surface of the sphere. The unit vector normal to the
surface of the sphere is denoted by :math:`{\hat{k}}`. This formulation
has already incorporated the hydrostatic equation and the ideal gas law,
:math:`p = \rho R T_v`. There is a no-flux (:math:`{{\dot\eta}}= 0`)
boundary condition at :math:`\eta=1` and :math:`\eta=\eta_\text{top}`.
The vorticity is denoted by
:math:`\zeta = {\hat{k}}\cdot {{{\nabla}\times}}{{{\smash[t]{\vec{u}}}}}`,
:math:`f` is a Coriolis term and :math:`\omega = Dp/Dt` is the pressure
vertical velocity. The virtual temperature :math:`T_v` and
variable-of-convenience :math:`c^*_p` are defined as in [eul:terrain].

The diagnostic equations for the geopotential height field :math:`\Phi`
is

.. math::
   :label: E:hydrostatic

   \Phi = \Phi_s + \int_{\eta}^{1} \frac{R T_v }{p} {\frac{\partial {p}}{\partial \eta}}\, d\eta
   

where :math:`\Phi_s` is the prescribed surface geopotential height
(given at :math:`\eta=1`). To complete the system, we need diagnostic
equations for :math:`{{\dot\eta}}` and :math:`\omega`, which come from
integrating with respect to :math:`\eta`. In fact, can be replaced by a
diagnostic equation for
:math:`{{\dot\eta}}{\frac{\partial {p}}{\partial \eta}}` and a
prognostic equation for surface pressure :math:`p_s`

.. math::
   :label: E:PEcont2a

   \begin{aligned}
   &{{\frac{\partial {}}{\partial t}}}p_s +  \int_{\eta_\text{top}}^{1} {\nabla\cdot}\left( {\frac{\partial {p}}{\partial \eta}}{{{\smash[t]{\vec{u}}}}}\right) \, d\eta = 0
    
   \\
   &{{\dot\eta}}{\frac{\partial {p}}{\partial \eta}}= - {{\frac{\partial {p}}{\partial t}}} - \int_{\eta_\text{top}}^\eta {\nabla\cdot}\left( {\frac{\partial {p}}{\partial \eta'}}{{{\smash[t]{\vec{u}}}}}\right) \, d\eta',
   \end{aligned}

where is evaluated at the model bottom (:math:`\eta=1`) after using
that
:math:`\partial p / \partial t = B(\eta) \partial p_s / \partial t` and
:math:`{{\dot\eta}}(1)=0, B(1)=1`. Using Eq [E:PEcont2c], we can derive
a diagnostic equation for the pressure vertical velocity
:math:`\omega = Dp/Dt`,

.. math::

   \omega =   {{\frac{\partial {p}}{\partial t}}} +  {{{\smash[t]{\vec{u}}}}}\cdot {\nabla}p + {{\dot\eta}}{\frac{\partial {p}}{\partial \eta}}=
   {{{\smash[t]{\vec{u}}}}}\cdot {\nabla}p  - \int_{\eta_\text{top}}^\eta {\nabla\cdot}\left( {\frac{\partial {p}}{\partial \eta}}{{{\smash[t]{\vec{u}}}}}\right) \, d\eta'

Finally, we rewrite as

.. math::
   :label: E:PEcont2b

   {{\dot\eta}}{\frac{\partial {p}}{\partial \eta}}= B(\eta) \int_{\eta_\text{top}}^{1} {\nabla\cdot}\left( {\frac{\partial {p}}{\partial \eta}}{{{\smash[t]{\vec{u}}}}}\right) \, d\eta
   - \int_{\eta_\text{top}}^\eta {\nabla\cdot}\left( {\frac{\partial {p}}{\partial \eta'}}{{{\smash[t]{\vec{u}}}}}\right) \, d\eta',
   

Conserved Quantities
~~~~~~~~~~~~~~~~~~~~

The equations have infinitely many conserved quantities, including mass,
tracer mass, potential temperature defined by

.. math:: M_X =   \iint {\frac{\partial {p}}{\partial \eta}}X \, d\eta {d\mathcal{A}}

with (:math:`X = 1, q` or :math:`(p/p_0)^{-\kappa} T`) and the total
moist energy :math:`E` defined by

.. math::
   :label: E:E1

   E =  
   \iint {\frac{\partial {p}}{\partial \eta}}\left( \frac12 {{{\smash[t]{\vec{u}}}}}^2 + c_p^* T  \right) \, d\eta {d\mathcal{A}}+
   \int p_s \Phi_s \, {d\mathcal{A}}

where :math:`{d\mathcal{A}}` is the spherical area measure. To compute
these quantities in their traditional units they should be divided by
the constant of gravity :math:`g`. We have omitted this scaling since
:math:`g` has also been scaled out from –. We note that in this
formulation of the primitive equations, the pressure :math:`p` is a
moist pressure, representing the effects of both dry air and water
vapor. The unforced equations conserve both the moist air mass
(:math:`X=1` above) and the dry air mass (:math:`X=1-q` ). However, in
the presence of a forcing term in (representing sources and sinks of
water vapor as would be present in a full model) a corresponding forcing
term must be added to to ensure that dry air mass is conserved.

The energy is specific to the hydrostatic equations. We have omitted
terms from the physical total energy which are constant under the
evolution of the unforced hydrostatic equations (:cite:`staniforth03`).
It can be converted into a more universal form involving
:math:`\tfrac12 {{{\smash[t]{\vec{u}}}}}^2 + c^*_v T + \Phi`, with
:math:`c^*_v` defined similarly to :math:`c^*_p`, so that
:math:`c^*_v = c_v + (c_{vv}-c_v) q` where :math:`c_v` and
:math:`c_{vv}` are the specific heats of dry air and water vapor defined
at constant volume. We note that :math:`c_p = R + c_v` and
:math:`c_{pv} =  R_v + c_{vv}` so that
:math:`c_p^* T = c_v^* T + R T_v`. Expanding :math:`c_p^* T` with this
expression, integrating by parts with respect to :math:`\eta` and making
use of the fact that the model top is at a constant pressure

.. math::

   \int {\frac{\partial {p}}{\partial \eta}}R T_v   \, d\eta = 
   -\int p \frac{\partial \Phi}{\partial \eta}   \, d\eta = 
   \int {\frac{\partial {p}}{\partial \eta}}\Phi    \, d\eta 
    - \left(  p \Phi  \right)   \Big| ^{\eta=1}_{\eta=\eta_\text{top}}

and thus

.. math::
   :label: E:E2

   E = 
    \iint {\frac{\partial {p}}{\partial \eta}}\left( \frac12 {{{\smash[t]{\vec{u}}}}}^2 + c^*_v T  + \Phi \right) 
   \, d\eta {d\mathcal{A}}+   \int  p_\text{top} \Phi(\eta_\text{top})  \,  {d\mathcal{A}}. 
   

The model top boundary term in vanishes if :math:`p_\text{top}=0`.
Otherwise it must be included to be consistent with the hydrostatic
equations. It is present due to the fact that the hydrostatic momentum
equation neglects the vertical pressure gradient.

Horizontal Discretization: Functional Spaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the finite element method, instead of constructing discrete
approximations to derivative operators, one constructs a discrete
functional space, and then finds the function in this space which solves
the equations of interest in a minimum residual sense. As compared to
finite volume methods, there is less choice in how one constructs the
discrete derivative operators in this setting, since functions in the
discrete space are represented in terms of known basis functions whose
derivatives are known, often analytically.

Let :math:`x^\alpha` and
:math:`{{\smash[t]{\vec{x}}}}=x^1{\smash[t]{\vec{e}}}_1 + x^2{\smash[t]{\vec{e}}}_2`
be the Cartesian coordinates and position vector of a point in the
reference square :math:`{{[-1,1]^2}}` and let :math:`r^\alpha` and
:math:`{{\smash[t]{\vec{r}}}}` be the coordinates and position vector of
a point on the surface of the sphere, denoted by :math:`\Omega`. We mesh
:math:`\Omega` using the cubed-sphere grid (Fig. :ref:`f-sphere4`) first used
in :cite:`sadourny72`. Each cube face is mapped to the surface of the
sphere with the equal-angle gnomonic projection (:cite:`rancic96`).
The map from the reference element :math:`[-1,1]^2` to
the cube face is a translation and scaling. The composition of these two
maps defines a :math:`{\mathcal C^{1}}` map from the spherical elements
to the reference element :math:`{{[-1,1]^2}}`. We denote this map and
its inverse by

.. math::
   :label: e:map

   {{\smash[t]{\vec{r}}}}= {{\smash[t]{\vec{r}}}}({{\smash[t]{\vec{x}}}};m), \qquad  {{\smash[t]{\vec{x}}}}= {{\smash[t]{\vec{x}}}}({{\smash[t]{\vec{r}}}};m).
   
.. _f-sphere4:

.. figure:: figures/figure3-2.jpg
   :align: center

   Figure 3.2: Tiling the surface of the sphere with quadrilaterals. An inscribed cube is projected to the surface of the sphere. 
   The faces of the cubed sphere are further subdivided to form a quadrilateral grid of the desired resolution. Coordinate lines from the
   gnomonic equal-angle projection are shown. 

We now define the discrete space used by the SEM. First we denote the
space of polynomials up to degree :math:`d` in :math:`{{[-1,1]^2}}` by

.. math::

   {\mathcal P_d}=  {\mathop{\mathrm{span}}}_{i,j=0}^d (x^1)^i (x^2)^j    

.. todo:: The above equation is not correct - the following part did not translate correctly and needs to be fixed  {\mathop{\mathrm{span}}}\limits_{{\smash[t]{\vec{\imath}}}\in\mathbb{I}}\phi_{{\smash[t]{\vec{\imath}}}}({{\smash[t]{\vec{x}}}),


where :math:`\mathbb{I} = \{0,\ldots,d\}^2` contains all the degrees and
:math:`\phi_{{\smash[t]{\vec{\imath}}}}({{\smash[t]{\vec{x}}}})= \varphi_{i^1}(x^1) \varphi_{i^2}(x^2)`,
:math:`i^\alpha=0,\dots,d`, are the cardinal functions, namely
polynomials that interpolate the tensor-product of degree-\ :math:`d`
Gauss-Lobatto-Legendre (GLL) nodes
:math:`{{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}} =  \xi_{i^1}{\smash[t]{\vec{e}}}_1 + \xi_{i^2}{\smash[t]{\vec{e}}}_2`.
The GLL nodes used within an element for :math:`d=3` are shown in
Fig. [f:GLLnodes]. The cardinal-function expansion coefficients of a
function :math:`g` are its GLL nodal values, so we have

.. math::
   :label: e:cfvec

   g({{\smash[t]{\vec{x}}}})= \sum_{{\smash[t]{\vec{\imath}}}\in\mathbb{I}} g({{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}})  \phi_{{\smash[t]{\vec{\imath}}}}({{\smash[t]{\vec{x}}}}).
   

We can now define the piecewise-polynomial SEM spaces
:math:`{\mathcal V^{0}_{}}` and :math:`{\mathcal V^{1}_{}}` as

.. math::
   :label: e:Hzero

   \begin{aligned}
   {\mathcal V^{0}_{}}&=  \{f \in{\mathcal L^2}(\Omega) :  f({{\smash[t]{\vec{r}}}}(\cdot;m)) \in {\mathcal P_d}, \forall m\}
   ={\mathop{\mathrm{span}}}_{m=1}^M\{\phi_{{\smash[t]{\vec{\imath}}}}({{\smash[t]{\vec{x}}}}(\cdot;m))\}_{{\smash[t]{\vec{\imath}}}\in\mathbb{I}}
   \\
   \text{and}\qquad{\mathcal V^{1}_{}}&= {\mathcal C^{0}}(\Omega)\cap{\mathcal V^{0}_{}}.
   \end{aligned}

Functions in :math:`{\mathcal V^{0}_{}}` are polynomial within each
element but may be discontinuous at element boundaries and
:math:`{\mathcal V^{1}_{}}` is the subspace of continuous function in
:math:`{\mathcal V^{0}_{}}`. We take
:math:`M_d = \dim {\mathcal V^{0}_{}} = (d+1)^3 M`, and
:math:`L = \dim {\mathcal V^{1}_{}} <  M_d`. We then construct a set of
:math:`L` unique points by

.. math::
   :label: e:GlInt

   \{{{\smash[t]{\vec{r}}}}_\ell\}_{\ell=1}^L = \bigcup_{m=1}^M{{\smash[t]{\vec{r}}}}(\{{{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}}\}_{{\smash[t]{\vec{\imath}}}\in\mathbb{I}};m),
   

For every point :math:`{{\smash[t]{\vec{r}}}}_\ell`, there exists at
least one element :math:`\Omega_m` and at least one GLL node
:math:`{{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}}={{\smash[t]{\vec{x}}}}({{\smash[t]{\vec{r}}}}_\ell;m)`.
In 2D, if :math:`{{\smash[t]{\vec{r}}}}_\ell` belongs to exactly one
:math:`\Omega_m` it is an element-interior node. If it belongs to
exactly two :math:`\Omega_m`\ s, it is an element-edge interior node.
Otherwise it is a vertex node.

[l]2.0in

2.5in

We also define similar spaces for 2D vectors. We introduce two families
of spaces, with a subscript of either *con* or *cov*, denoting if the
contravariant or covariant components of the vectors are piecewise
polynomial, respectively.

.. math::

   \begin{aligned}
   {{\mathcal V^{0}_{\rm con}}}&=  \{{{{\smash[t]{\vec{u}}}}}\in{\mathcal L^2}(\Omega)^2 :  u^\alpha \in {\mathcal V^{0}_{}},\;\alpha=1,2\}
   \\
   \text{and}\qquad{{\mathcal V^{1}_{\rm con}}}&= {\mathcal C^{0}}(\Omega)^2\cap{{\mathcal V^{0}_{\rm con}}},
   \end{aligned}

where :math:`u^1, u^2` are the contravariant components of
:math:`{{{\smash[t]{\vec{u}}}}}` defined below. Vectors in
:math:`{{\mathcal V^{1}_{\rm con}}}` are globally continuous and their
contravariant components are polynomials in each element. Similarly,

.. math::

   \begin{aligned}
   {{{\mathcal V^{0}_{\rm cov}}}}&=  \{{{{\smash[t]{\vec{u}}}}}\in{\mathcal L^2}(\Omega)^2 :  u_\beta \in {\mathcal V^{0}_{}},\;\beta=1,2\}
   \\
   \text{and}\qquad{{{\mathcal V^{1}_{\rm cov}}}}&= {\mathcal C^{0}}(\Omega)^2\cap{{{\mathcal V^{0}_{\rm cov}}}}.
   \end{aligned}

The SEM is a Galerkin method with respect to the
:math:`{\mathcal V^{1}_{}}` subspace and it can be formulated solely in
terms of functions in :math:`{\mathcal V^{1}_{}}`. In CAM-HOMME, the
typical configuration is to run with :math:`d=3` which achieves a 4th
order accurate horizontal discretization (:cite:`taylor10b`). All
variables in the CAM-HOMME initial condition and history files as well
as variables passed to the physics routines are represented by their
grid point values at the points
:math:`\{{{\smash[t]{\vec{r}}}}_\ell\}_{\ell=1}^L`. However, for some
intermediate quantities and internally in the dynamical core it is
useful to consider the larger :math:`{\mathcal V^{0}_{}}` space, where
variables are represented by their grid point values at the :math:`M_d`
mapped GLL nodes. This later representation can also be considered as
the cardinal-function expansion of a function :math:`f` local to each
element,

.. math::
   :label: e:localexpand

   f({{\smash[t]{\vec{r}}}})  =
   \sum_{{\smash[t]{\vec{\imath}}}\in\mathbb{I}} f({{\smash[t]{\vec{r}}}}({{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}};m)) \phi_{{\smash[t]{\vec{\imath}}}}({{\smash[t]{\vec{x}}}}({{\smash[t]{\vec{r}}}};m))
   

since the expansion coefficients are the function values at the mapped
GLL nodes. Functions :math:`f` in :math:`{\mathcal V^{0}_{}}` can be
multiple-valued at GLL nodes that are *redundant* (i.e., shared by more
than one element), while for :math:`f \in {\mathcal V^{1}_{}}`, the
values at any redundant points must all be the same.

Horizontal Discretization: Differential Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use the standard curvilinear coordinate formulas for vector operators
following :cite:`heinbockel01`. Given the :math:`2\times2` Jacobian of the
the mapping from :math:`{{[-1,1]^2}}` to :math:`\Omega_m`, we denote its
determinant-magnitude by

.. math::
   :label: e:Jd

   {J}=\left| {\frac{\partial {{{\smash[t]{\vec{r}}}}}}{\partial {{\smash[t]{\vec{x}}}}}} \right|.
   

A vector :math:`{{{\smash[t]{\vec{v}}}}}` may be written in terms of
physical or covariant or contravariant components,
:math:`{\renewcommand\arraystretch{.2}v[\begin{array}{@{}l@{}}\vphantom{\scriptstyle\alpha}\\\scriptstyle\gamma\\\vphantom{\scriptstyle\alpha}\end{array}]}`
or :math:`v_\beta` or :math:`v^\alpha`,

.. math::
   :label: e:3comps

   {{{\smash[t]{\vec{v}}}}}=\sum_{\gamma=1}^3{\renewcommand\arraystretch{.2}v[\begin{array}{@{}l@{}}\vphantom{\scriptstyle\alpha}\\\scriptstyle\gamma\\\vphantom{\scriptstyle\alpha}\end{array}]}{\frac{\partial {{{\smash[t]{\vec{r}}}}}}{\partial r^\gamma}}=
   \sum_{\beta=1}^3v_\beta{{\smash[t]{\vec{g}}}}^\beta=
   \sum_{\alpha=1}^3v^\alpha{{\smash[t]{\vec{g}}}}_\alpha,
   

that are related by
:math:`v_\beta={{{\smash[t]{\vec{v}}}}}{\mathbin{\mathbf{\cdot}}}{{\smash[t]{\vec{g}}}}_\beta`
and
:math:`v^\alpha={{{\smash[t]{\vec{v}}}}}{\mathbin{\mathbf{\cdot}}}{{\smash[t]{\vec{g}}}}^\alpha`,
where :math:`{{\smash[t]{\vec{g}}}}^\alpha={\nabla}x^\alpha` is a
contravariant basis vector and
:math:`{{\smash[t]{\vec{g}}}}_\beta={\frac{\partial {{{\smash[t]{\vec{r}}}}}}{\partial x^\beta}}`
is a covariant basis vector.

The dot product and contravariant components of the cross product are
:cite:`heinbockel01` Table 1

.. math::
   :label: e:dotandcross

   {{{\smash[t]{\vec{u}}}}}{\mathbin{\mathbf{\cdot}}}{{{\smash[t]{\vec{v}}}}}=  \sum_{\alpha=1}^3 u_\alpha v^\alpha\qquad\text{and}\qquad
   \left( {{{\smash[t]{\vec{u}}}}}{{\times}}{{{\smash[t]{\vec{v}}}}}\right)^\alpha  = 
   \frac 1 {J}\sum_{\beta,\gamma=1}^3\epsilon^{\alpha \beta \gamma } u_\beta v_\gamma
   

where :math:`\epsilon^{\alpha\beta\gamma}\in\{0,\pm1\}` is the
Levi-Civita symbol. The divergence, covariant coordinates of the
gradient and contravariant coordinates of the curl are 
:cite:`heinbockel01` [eqs.\ 2.1.1, 2.1.4 and 2.1.6]

.. math::
   :label: e:divgradcurl

   {\nabla\cdot}{{{\smash[t]{\vec{v}}}}}= \frac 1 {J}\sum_\alpha{\frac{\partial {}}{\partial x^\alpha}}({J}v^\alpha),
   \quad
   \left( {\nabla}f \right)_\alpha = {\frac{\partial {f}}{\partial x^\alpha}}
   \quad\text{and}\quad
   \left( {{{\nabla}\times}}{{{\smash[t]{\vec{v}}}}}\right)^\alpha =  \frac 1 {J}\sum_{\beta,\gamma}
   \epsilon^{\alpha \beta \gamma} {\frac{\partial {v_\gamma}}{\partial x^\beta}}.
   

In the SEM, these operators are all computed in terms of the
derivatives with respect to :math:`{{\smash[t]{\vec{x}}}}` in the
reference element, computed exactly (to machine precision) by
differentiating the local element expansion . For the gradient, the
covariant coordinates of :math:`{\nabla}f, f \in
{\mathcal V^{0}_{}}` are thus computed exactly within each element. Note
that :math:`{\nabla}f \in {{{\mathcal V^{0}_{\rm cov}}}}`, but may not
be in :math:`{{{\mathcal V^{1}_{\rm cov}}}}` even for
:math:`f \in {\mathcal V^{1}_{}}` due to the fact that its components
will be multi-valued at element boundaries because :math:`{\nabla}f`
computed in adjacent elements will not necessarily agree along their
shared boundary. In the case where :math:`{J}` is constant within each
element, the SEM curl of
:math:`{{{\smash[t]{\vec{v}}}}}\in {{{\mathcal V^{0}_{\rm cov}}}}` and
the divergence of
:math:`{{{\smash[t]{\vec{u}}}}}\in {{\mathcal V^{0}_{\rm con}}}` will
also be exact, but as with the gradient, multiple-valued at element
boundaries.

For non-constant :math:`{J}`, these operators may not be computed
exactly by the SEM due to the Jacobian factors in the operators and the
Jacobian factors that appear when converting between covariant and
contravariant coordinates. We follow :cite:`thomas00`  and evaluate
these operators in the form shown in . The quadratic terms that appear
are first projected into :math:`{\mathcal V^{0}_{}}` via interpolation
at the GLL nodes and then this interpolant is differentiated exactly
using . For example, to compute the divergence of
:math:`{{{\smash[t]{\vec{v}}}}}\in {{\mathcal V^{0}_{\rm con}}}`, we
first compute the interpolant
:math:`{\mathcal I}({J}v^\alpha)\in{\mathcal V^{0}_{}}` of
:math:`{J}v^\alpha`, where the GLL interpolant of a product :math:`fg`
derives simply from the product of the GLL nodal values of :math:`f` and
:math:`g`. This operation is just a reinterpretation of the nodal values
and is essentially free in the SEM. The derivatives of this interpolant
are then computed exactly from . The sum of partial derivatives are then
divided by :math:`{J}` at the GLL nodal values and thus the SEM
divergence operator :math:`{{\nabla_{\rm h} \cdot }}()` is given by

.. math::
   :label: e:SEMdiv

   {\nabla\cdot}{{{\smash[t]{\vec{v}}}}}\approx {{\nabla_{\rm h} \cdot }}{{{\smash[t]{\vec{v}}}}}= {\mathcal I}\left( 
   \frac 1 {J}\sum_\alpha{\frac{\partial {{\mathcal I}( {J}v^\alpha)}}{\partial x^\alpha}} 
   \right)  \in {\mathcal V^{0}_{}}.
   

Similarly, the gradient and curl are approximated by

.. math::
   :label: e:hgrad

   \begin{aligned}
   \left ( {\nabla}f \right)_\alpha  \approx
   \left( {{\nabla_{\rm h}}}f \right)_\alpha & = 
   {\frac{\partial {f}}{\partial x^\alpha}} 
   \\
   \text{and}\qquad
   \left( {{{\nabla}\times}}{{{\smash[t]{\vec{v}}}}}\right)^\alpha \approx
   \left( {{{\nabla_{\rm h}}}{{\times}}}{{{\smash[t]{\vec{v}}}}}\right)^\alpha  &  = 
   \sum_{\beta,\gamma}
   \epsilon^{\alpha \beta \gamma} {\mathcal I}\left(\frac 1 {J}{\frac{\partial {v_\gamma}}{\partial x^\beta}}\right)
   \end{aligned}

with :math:`{{\nabla_{\rm h}}}f \in{{{\mathcal V^{0}_{\rm cov}}}}` and
:math:`{{{\nabla_{\rm h}}}{{\times}}}{{{\smash[t]{\vec{v}}}}}\in{{\mathcal V^{0}_{\rm con}}}`.
The SEM is well known for being quite efficient in computing these types
of operations. The SEM divergence, gradient and curl can all be
evaluated at the :math:`(d+1)^3` GLL nodes within each element in
:math:`\mathcal{O}(d)` operations per node using the tensor-product
property of these points  :cite:`deville02`,:cite:`karniadakis05`.

Horizontal Discretization: Discrete Inner-Product
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of using exact integration of the basis functions as in a
traditional finite-element method, the SEM uses a GLL quadrature
approximation for the integral over :math:`\Omega`, that we denote by
:math:`{\langle}\cdot {\rangle}`. We can write this integral
as a sum of area-weighted integrals over the set of elements
:math:`\{ \Omega_m \}_{m=1}^M` used to decompose the domain,

.. math:: \int f g \,{d\mathcal{A}}= \sum_{m=1}^M\int_{\Omega_m} f g \, {d\mathcal{A}}.

The integral over a single element :math:`\Omega_m` is written as an
integral over :math:`{{[-1,1]^2}}` by

.. math::
   :label: e:el2sq

   \int_{\Omega_m} f g \, {d\mathcal{A}}= \iint_{{{[-1,1]^2}}}f({{\smash[t]{\vec{r}}}}(\cdot;m))g({{\smash[t]{\vec{r}}}}(\cdot;m)){J}_m \,d x^1 \,d x^2 
   \approx{\langle}fg{\rangle}_{\Omega_m},
   

where we approximate the integral over :math:`{{[-1,1]^2}}` by GLL
quadrature,

.. math::
   :label: E:intomega

   {\langle}f g {\rangle}_{\Omega_m} =
   \sum_{{\smash[t]{\vec{\imath}}}\in\mathbb{I}}w_{i^1}w_{i^2}{J}_m({{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}})
   f({{\smash[t]{\vec{r}}}}({{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}};m))g({{\smash[t]{\vec{r}}}}({{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}};m))
   

The SEM approximation to the global integral is then naturally defined
as

.. math::
   :label: e:dip

   \int f g \,{d\mathcal{A}}\approx  \sum_{m=1}^M {\langle}f g {\rangle}_{\Omega_m}
   ={\langle}fg{\rangle}

When applied to the product of functions
:math:`f,g \in {\mathcal V^{0}_{}}`, the quadrature approximation
:math:`{\langle}f g {\rangle}` defines a discrete
inner-product in the usual manner.

Horizontal Discretization: The Projection Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let :math:`{{P}}: {\mathcal V^{0}_{}} \rightarrow {\mathcal V^{1}_{}}`
be the unique orthogonal (self-adjoint) projection operator from
:math:`{\mathcal V^{0}_{}}` onto :math:`{\mathcal V^{1}_{}}` w.r.t. the
SEM discrete inner product . The operation :math:`{{P}}` is essentially
the same as the common procedure in the SEM described as *assembly*
:cite:`karniadakis05` [p.7] or *direct stiffness summation*
:cite:`deville02` [eq.\ 4.5.8]. Thus the SEM assembly
procedure is not an ad-hoc way to remove the redundant degrees of
freedom in :math:`{\mathcal V^{0}_{}}`, but is in fact the natural
projection operator :math:`{{P}}`. Applying the projection operator in a
finite element method requires inverting the finite element mass matrix.
A remarkable fact about the SEM is that with the GLL based discrete
inner product and the careful choice of global basis functions, the mass
matrix is diagonal :cite:`maday87`. The resulting projection
operator then has a very simple form: at element interior points, it
leaves the nodal values unchanged, while at element boundary points
shared by multiple elements it is a Jacobian-weighted average over all
redundant values (:cite:`taylor10b`).

To apply the projection
:math:`{{P}}: {{{\mathcal V^{0}_{\rm cov}}}} \rightarrow {{{\mathcal V^{1}_{\rm cov}}}}`
to vectors :math:`{{{\smash[t]{\vec{u}}}}}`, one cannot project the
covariant components since the corresponding basis vectors
:math:`{{\smash[t]{\vec{g}}}}_\beta` and
:math:`{{\smash[t]{\vec{g}}}}^\alpha` do not necessarily agree along
element faces. Instead we must define the projection as acting on the
components using a globally continuous basis such as the
latitude-longitude unit vectors :math:`\hat\theta` and
:math:`\hat\lambda`,

.. math::

   {{P}}({{{\smash[t]{\vec{u}}}}}) = 
   {{P}}( {{{\smash[t]{\vec{u}}}}}\cdot \hat\lambda) \hat\lambda 
   +
   {{P}}( {{{\smash[t]{\vec{u}}}}}\cdot \hat\theta) \hat\theta.

Horizontal Discretization: Galerkin Formulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SEM solves a Galerkin formulation of the equations of interest.
Given the discrete differential operators described above, the primitive
equations can be written as an ODE for a generic prognostic variable
:math:`U` and right-hand-side (RHS) terms

.. math:: {{\frac{\partial {U}}{\partial t}}} = {\rm RHS}.

The SEM solves this equation in integral form with respect to the SEM
inner product. That is, for a :math:`\rm{RHS} \in {\mathcal V^{0}_{}}`,
the SEM finds the unique
:math:`{{\frac{\partial {U}}{\partial t}}} \in {\mathcal V^{1}_{}}` such
that

.. math:: {\langle}\phi  {{\frac{\partial {U}}{\partial t}}}  {\rangle}= {\langle}\phi \, {\rm RHS} {\rangle}\qquad \forall \phi \in {\mathcal V^{1}_{}}.

As the prognostic variable is assumed to belong to
:math:`{\mathcal V^{1}_{}}`, the RHS will in general belong to
:math:`{\mathcal V^{0}_{}}` since it contains derivatives of the
prognostic variables, resulting in the loss of continuity at the element
boundaries. If one picks a suitable basis for
:math:`{\mathcal V^{1}_{}}`, this discrete integral equation results in
a system of :math:`L` equations for the :math:`L` expansion coefficients
of :math:`{{\frac{\partial {U}}{\partial t}}}`. The SEM solves these
equations exactly, and the solution can be written in terms of the SEM
projection operator as

.. math:: {{\frac{\partial {U}}{\partial t}}} = {{P}}\left(  {\rm RHS} \right).

The projection operator commutes with any time-stepping scheme, so the
equations can be solved in a two step process, illustrated here for
simplicity with the forward Euler method

-  Step 1:

   .. math:: U^* = U^t + \Delta t  \, {\rm RHS} \qquad U^* \in {\mathcal V^{0}_{}}

-  Step 2:

   .. math:: U^{t+1} = {{P}}\left( U^* \right)  \qquad U^{t+1} \in {\mathcal V^{1}_{}}

For compactness of notation, we will denote this two step procedure in
what follows by

.. math:: {{P}}^{-1} {{\frac{\partial {U}}{\partial t}}} =   {\rm RHS}.

Note that :math:`{{P}}` maps a :math:`M_d` dimensional space
:math:`{\mathcal V^{0}_{}}` into a :math:`L` dimensional space
:math:`{\mathcal V^{1}_{}}`, so here :math:`{{P}}^{-1}` denotes the left
inverse of :math:`{{P}}`. This inverse will never be computed, it is
only applied as in step 2 above.

This two step Galerkin solution process represents a natural separation
between computation and communication for the implementation of the SEM
on a parallel computer. The computations in step 1 are all local to the
data contained in a single element. Assuming an element-based
decomposition so that each processor contains at least one element, no
inter-processor communication is required in step 1. All inter-processor
communication in HOMME is isolated to the projection operator step, in
which element boundary data must be exchanged between adjacent elements.

Vertical Discretization
~~~~~~~~~~~~~~~~~~~~~~~

The vertical coordinate system uses a Lorenz staggering of the variables
as shown in :ref:`figure-1`. Let :math:`K` be the total number of layers,
with variables :math:`{{{\smash[t]{\vec{u}}}}}, T, q, \omega, \Phi` at
layer mid points denoted by :math:`k=1,2,\dots,K`. We denote layer
interfaces by :math:`k+\tfrac12,  k=0,1,\dots,K`, so that
:math:`\eta_{1/2}=\eta_\text{top}` and :math:`\eta_{K+1/2}=1`. The
:math:`\eta`-integrals will be replaced by sums. We will use
:math:`{ \mathop{\delta_\eta}}` to denote the discrete
:math:`\partial / \partial \eta` operator. The
:math:`{ \mathop{\delta_\eta}}` operator uses centered differences to
compute derivatives with respect to :math:`\eta` at layer mid point from
layer interface values,
:math:`{ \mathop{\delta_\eta}}(X)_k = (X_{k+1/2} - X_{k-1/2})/(\eta_{k+1/2}-\eta_{k-1/2})`.
We will use the over-bar notation for vertical averaging,
:math:`\overline q_{k+1/2} = (q_{k+1}+q_k)/2`. We also introduce the
symbol :math:`{\pi}` to denote the discrete pseudo-density
:math:`{\frac{\partial {p}}{\partial \eta}}` given by

.. math:: {\pi}_{k} = { \mathop{\delta_\eta}}( p )_k

.

We will use :math:`{ \mathop{\overline{ {{\dot\eta}}\delta_\eta }}}` to
denote the discrete form of the
:math:`{{\dot\eta}}\partial / \partial\eta` operator. We use the
discretization given in [eul:econserve]. This operator acts on
quantities defined at layer mid-points and returns a result also at
layer mid-points,

.. math::
   :label: E:dnhprimealt

   { \mathop{\overline{ {{\dot\eta}}\delta_\eta }}}(X)_k = 
   \frac1{2 {\pi}_k \Delta\eta_k}
   \left[ 
   ( {{\dot\eta}}{\pi})_{k+1/2}  \left(  X_{k+1} - X_k  \right)
   + 
   ( {{\dot\eta}}{\pi})_{k-1/2} (  X_{k} - X_{k-1} ) 
   \right]
   

where :math:`\Delta\eta_k = \eta_{k+1/2} - \eta_{k-1/2}`. We use the
over-bar notation since the formula can be seen as a
:math:`{\pi}`-weighted average of a layer interface centered difference
approximation to :math:`{{\dot\eta}}\partial/\partial \eta`. This
formulation was constructed in :cite:`simmons81b` in order to
ensure mass and energy conservation. Here we will use an equivalent
expression that can be written in terms of
:math:`{ \mathop{\delta_\eta}}`,

.. math::
   :label: E:dnhprime

   { \mathop{\overline{ {{\dot\eta}}\delta_\eta }}}(X)_k = 
   \frac1{{\pi}_k} \Big[ { \mathop{\delta_\eta}}\left( {{\dot\eta}}{\pi}\overline X \right)_k - X { \mathop{\delta_\eta}}\left( {{\dot\eta}}{\pi}\right)_k \Big]
   .
   

Discrete formulation: Dynamics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We discretize the equations exactly in the form shown in , , and ,
obtaining

.. math::
   :label: E:PEmomD

   \begin{aligned}
   {{P}}^{-1}
   {{\frac{\partial {{{{\smash[t]{\vec{u}}}}}}}{\partial t}}} &= 
   -
   \left( {{\mathbf{\zeta}}}+ f \right) {\hat{k}}{{\times}}{{{\smash[t]{\vec{u}}}}}+ {\nabla_{\rm h}}\left( \frac12 {{{\smash[t]{\vec{u}}}}}^2 + \Phi \right)
     - { \mathop{\overline{ {{\dot\eta}}\delta_\eta }}}({{{\smash[t]{\vec{u}}}}})  - \frac{RT_v}{p} {\nabla_{\rm h}}( p )
    \\
   {{P}}^{-1}
   {{\frac{\partial {T}}{\partial t}}} &= 
   - {{{\smash[t]{\vec{u}}}}}\cdot {\nabla_{\rm h}}( T  )  - { \mathop{\overline{ {{\dot\eta}}\delta_\eta }}}(T)  + \frac{RT_v}{c^*_p p} \omega
   \\
   {{P}}^{-1}
   {{\frac{\partial {p_s}}{\partial t}}} &= 
   -  \sum_{j = 1}^{K} {\nabla_{\rm h} \cdot }\left( {\pi}{{{\smash[t]{\vec{u}}}}}\right)_{j} \Delta\eta_{j}
   \\
   \left( {{\dot\eta}}{\pi}\right)_{i+1/2} &=
   B(\eta_{i+1/2}) 
    \sum_{j = 1}^{K} {\nabla_{\rm h} \cdot }\left( {\pi}{{{\smash[t]{\vec{u}}}}}\right)_{j} \Delta\eta_{j}
   - \sum_{j=1}^i {\nabla_{\rm h} \cdot }\left( {\pi}{{{\smash[t]{\vec{u}}}}}\right)_{j} \Delta\eta_{j}.
   \end{aligned}

We consider :math:`({{\dot\eta}}{\pi})` a single quantity given at layer
interfaces and defined by . The no-flux boundary condition is
:math:`({{\dot\eta}}{\pi})_{1/2} = ({{\dot\eta}}{\pi})_{K+1/2} = 0`. In
, we used a midpoint quadrature rule to evaluate the indefinite integral
from . In practice :math:`\Delta\eta` can be eliminated from the
discrete equations by scaling :math:`{\pi}`, but here we retain them so
as to have a direct correspondence with the continuum form of the
equations written in terms of
:math:`{\frac{\partial {p}}{\partial \eta}}`.

Finally we give the approximations for the diagnostic equations. We
first integrate to layer interface :math:`i-\frac12` using the same
mid-point rule as used to derive , and then add an additional term
representing the integral from :math:`i-\tfrac12` to :math:`i`:

.. math::
   :label: E:omegaD1

   \begin{aligned}
   \omega_i &=   ({{{\smash[t]{\vec{u}}}}}\cdot {\nabla_{\rm h}}p)_i  - 
   \sum_{j=1}^{i-1} {\nabla_{\rm h} \cdot }\left( {\pi}{{{\smash[t]{\vec{u}}}}}\right)_j \Delta\eta_j
   +  {\nabla_{\rm h} \cdot }\left( {\pi}{{{\smash[t]{\vec{u}}}}}\right)_i \frac{\Delta\eta_i}{2}
   
   \\
   &=   ({{{\smash[t]{\vec{u}}}}}\cdot {\nabla_{\rm h}}p)_i  - \sum_{j=1}^{K} C_{ij} {\nabla_{\rm h} \cdot }\left( {\pi}{{{\smash[t]{\vec{u}}}}}\right)_j
   \end{aligned}

where

.. math::

   C_{ij} = 
   \begin{cases}
   \Delta\eta_j &  \quad i>j\\
   {\Delta\eta_j}/{2} &  \quad i = j \\
   0&  \quad i<j\\
   \end{cases}

and similar for :math:`\Phi`,

.. math::
   :label: E:Phi

   \begin{aligned}
   (\Phi - \Phi_s)_i &=   
   \left( \frac{R T_v}{p} {\pi}\right)_i  \frac{\Delta\eta_i}{2}
   + \sum_{j=i+1}^{K} \left( \frac{R T_v}{p} {\pi}\right)_j \Delta\eta_j
   \\
    &=    \sum_{j=1}^{K} H_{ij} \left( \frac{R T_v}{p} {\pi}\right)_j
   \end{aligned}

where

.. math::

   H_{ij} = 
   \begin{cases}
   \Delta\eta_j &  \quad i<j\\
   {\Delta\eta_j}/{2} &  \quad i = j \\
   0&  \quad i>j\\
   \end{cases}

Similar to [eul:econserve], we note that

.. math::
   :label: E:quadconsistency

   \Delta\eta_i \, C_{ij}  = \Delta\eta_j \, H_{ji} 
   

which ensures energy conservation (:cite:`taylor10a`).

Consistency
~~~~~~~~~~~

It is important that the discrete equations be as consistent as
possible. In particular, we need a discrete version of , the
non-vertically averaged continuity equation. Equation implicitly implies
such an equation. To see this, apply :math:`{ \mathop{\delta_\eta}}` to
and using that
:math:`\partial p / \partial t = B(\eta) \partial p_s / \partial t`
then we can derive, at layer mid-points,

.. math::
   :label: E:PEcontD

   {{P}}^{-1} {{\frac{\partial {{\pi}}}{\partial t}}} = -{\nabla_{\rm h} \cdot }\left( {\pi}{{{\smash[t]{\vec{u}}}}}\right) - 
   { \mathop{\delta_\eta}}\left( {{\dot\eta}}{\pi}\right).
   

A second type of consistency that has been identified as important is
that , the discrete equation for :math:`\omega`, be consistent with ,
the discrete continuity equation (:cite:`williamson94`). The
two discrete equations should imply a reasonable discretization of
:math:`\omega = Dp/Dt`. To show this, we take the average of at layers
:math:`i-1/2` and :math:`i+1/2` and combine this with (at layer
mid-points :math:`i`) and assuming that
:math:`B(\eta_i) = B(\eta_{i-1/2}) +  B(\eta_{i+1/2})` we obtain

.. math::

   {{P}}^{-1} {{\frac{\partial {p}}{\partial t}}}  = \omega_i -  ({{{\smash[t]{\vec{u}}}}}\cdot {\nabla_{\rm h}}p)_i
   - \frac12 \left( ({{\dot\eta}}{ \mathop{\delta_\eta}})_{i-1/2} + ({{\dot\eta}}{ \mathop{\delta_\eta}})_{i+1/2} \right).

which, since :math:`{{{\smash[t]{\vec{u}}}}}\cdot {\nabla_{\rm h}}p` is
given at layer mid-points and :math:`{{\dot\eta}}{\pi}` at layer
interfaces, is the SEM discretization of
:math:`w  = \partial p / \partial t + {{{\smash[t]{\vec{u}}}}}\cdot {\nabla_{\rm h}}p + {{\dot\eta}}{\pi}`.

Time Stepping
~~~~~~~~~~~~~

Applying the SEM discretization to - results in a system of ODEs. These
are solved with an :math:`N`-stage Runge-Kutta method. This method
allows for a gravity-wave based CFL number close to :math:`N-1`,
(normalized so that the largest stable timestep of the Robert filtered
Leapfrog method has a CFL number of 1.0). The value of :math:`N` is
chosen large enough so that the dynamics will be stable at the same
timestep used by the tracer advection scheme. To determine :math:`N`, we
first note that the tracer advection scheme uses a less efficient (in
terms of maximum CFL) strong stability preserving Runge-Kutta method
described below. It is stable at an advective CFL number of 1.4. Let
:math:`u_0` be a maximum wind speed and :math:`c_0` be the maximum
gravity wave speed. The gravity wave and advective CFL conditions are

.. math::

   \Delta t \le (N-1) \Delta x / c_0,
   \qquad
   \Delta t \le 1.4 \Delta x / u_0.

In the case where :math:`\Delta t` is chosen as the largest stable
timestep for advection, then we require :math:`N \ge 1 + 1.4 c_0/u_0`
for a stable dynamics timestep. Using a typical values :math:`u_0=120`
m/s and :math:`c_0 = 340`\ m/s gives :math:`N=5`. CAM places additional
restrictions on the timestep (such as that the physics timestep must be
an integer multiple of :math:`\Delta t`) which also influence the choice
of :math:`\Delta t` and :math:`N`.

Dissipation
~~~~~~~~~~~

A horizontal hyper-viscosity operator, modeled after [eul:hdiff] is
applied to the momentum and temperature equations. It is applied in a
time-split manor after each dynamics timestep. The hyper-viscosity step
for vectors can be written as

.. math:: {{\frac{\partial {{{{\smash[t]{\vec{u}}}}}}}{\partial t}}} = -\nu \Delta^2 {{{\smash[t]{\vec{u}}}}}.

An integral form of this equation suitable for the SEM is obtained using
a mixed finite element formulation (:cite:`giraldo99`) which
writes the equation as a system of equations involving only first
derivatives. We start by introduced an auxiliary vector
:math:`{{\smash[t]{\vec{f}}}}` and using the identity
:math:`\Delta {{{\smash[t]{\vec{u}}}}}= {\nabla}( {\nabla\cdot}{{{\smash[t]{\vec{u}}}}}) - {{{\nabla}\times}}( {{{\nabla}\times}}{{{\smash[t]{\vec{u}}}}})`,

.. math::
   :label: E:HV1

   \begin{aligned}
   {{\frac{\partial {{{{\smash[t]{\vec{u}}}}}}}{\partial t}}} &= -\nu \left( {\nabla}( {\nabla\cdot}{{\smash[t]{\vec{f}}}}) - {{{\nabla}\times}}{\hat{k}}({{{\nabla}\times}}{{\smash[t]{\vec{f}}}}) \right)
    \\
   {{\smash[t]{\vec{f}}}}&=   {\nabla}({\nabla\cdot}{{{\smash[t]{\vec{u}}}}}) - {{{\nabla}\times}}({{{\nabla}\times}}{{{\smash[t]{\vec{u}}}}}) {\hat{k}}.
   \end{aligned}

Integrating the gradient and curl operators by parts gives

.. math::
   :label: E:weakHV1

   \begin{aligned}
   \iint {{\smash[t]{\vec{\phi}}}}\cdot {{\frac{\partial {{{{\smash[t]{\vec{u}}}}}}}{\partial t}}} \,{d\mathcal{A}}&= \nu \iint 
   \left[ 
   ({\nabla\cdot}{{\smash[t]{\vec{\phi}}}}) ( {\nabla\cdot}{{\smash[t]{\vec{f}}}}) 
   + ({{{\nabla}\times}}{{\smash[t]{\vec{\phi}}}}) \cdot   {\hat{k}}( {{{\nabla}\times}}{{\smash[t]{\vec{f}}}}) 
   \right]
   \,{d\mathcal{A}} \\
   \iint {{\smash[t]{\vec{\phi}}}}\cdot {{\smash[t]{\vec{f}}}}\,{d\mathcal{A}}&=  
   - \iint \left[ ({\nabla\cdot}{{\smash[t]{\vec{\phi}}}}) ({\nabla\cdot}{{{\smash[t]{\vec{u}}}}}) + ({{{\nabla}\times}}{{\smash[t]{\vec{\phi}}}})\cdot {\hat{k}}({{{\nabla}\times}}{{{\smash[t]{\vec{u}}}}})
   \right] \, {d\mathcal{A}}.
   \\\end{aligned}

The SEM Galerkin solution of this integral equation is most naturally
written in terms of an inverse mass matrix instead of the projection
operator. It can be written in terms of the SEM projection operator by
first testing with the product of the element cardinal functions and the
contravariant basis vector
:math:`{{\smash[t]{\vec{\phi}}}}= \phi_{{\smash[t]{\vec{\imath}}}} {{\smash[t]{\vec{g}}}}_\alpha`.
With this type of test function, the RHS of can be defined as a weak
Laplacian operator
:math:`{{\smash[t]{\vec{f}}}}= D({{{\smash[t]{\vec{u}}}}}) \in {{{\mathcal V^{0}_{\rm cov}}}}`.
The covariant components of :math:`{{\smash[t]{\vec{f}}}}` given by
:math:`f_\alpha = {{\smash[t]{\vec{f}}}}\cdot {{\smash[t]{\vec{g}}}}_\alpha`
are then

.. math::

   f_\alpha ({{\smash[t]{\vec{r}}}}({{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}} ; m) ) = \frac{-1}{w_{i^1}w_{i^2}{J}_m({{\smash[t]{\vec{\xi}}}}_{{\smash[t]{\vec{\imath}}}})} 
   {\langle}({{\nabla_{\rm h} \cdot }}\phi_{{\smash[t]{\vec{\imath}}}} {{\smash[t]{\vec{g}}}}_{\alpha}) ({{\nabla_{\rm h} \cdot }}{{{\smash[t]{\vec{u}}}}}) 
   + ({{{\nabla_{\rm h}}}{{\times}}}\phi_{{\smash[t]{\vec{\imath}}}} {{\smash[t]{\vec{g}}}}_\alpha )\cdot {\hat{k}}({{{\nabla_{\rm h}}}{{\times}}}{{{\smash[t]{\vec{u}}}}}).
   {\rangle}

Then the SEM solution to and is given by

.. math::

   {{{\smash[t]{\vec{u}}}}}(t + \Delta t)   = {{{\smash[t]{\vec{u}}}}}(t) - \nu \Delta t {{P}}\Bigg(  D 
   \Big( {{P}}\big( D({{{\smash[t]{\vec{u}}}}})  \big) 
   \Big ) 
   \Bigg).

Because of the SEM tensor product decomposition, the expression for
:math:`D` can be evaluated in only :math:`O(d)` operations per grid
point, and in CAM-HOMME typically :math:`d=3`.

Following [eul:hdiff], a correction term is added so the hyper-viscosity
does not damp rigid rotation. The hyper-viscosity formulation used for
scalars such as :math:`T` is much simpler, since instead of the vector
Laplacian identity we use :math:`\Delta T = {\nabla\cdot}{\nabla}T`. Otherwise the approach is identical to that
used above so we omit the details. The correction for terrain following
coordinates given in [eul:hdiff] is not yet implemented in CAM-HOMME.

Discrete formulation: Tracer Advection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All tracers, including specific humidity, are advected with a
discretized version of . HOMME uses the vertically Lagrangian approach
(see [FVvdisc]) from :cite:`lin04`. At the beginning of each timestep, the
tracers are assumed to be given on the :math:`\eta`-coordinate layer mid
points. The tracers are advanced in time on a moving vertical coordinate
system :math:`\eta'` defined so that :math:`{{\dot\eta}}' = 0`. At the
end of the timestep, the tracers are remapped back to the
:math:`\eta`-coordinate layer mid points using the monotone remap
algorithm from :cite:`zerroukat05`.

The horizontal advection step consists of using the SEM to solve

.. math::
   :label: E:PEqDlagrange

   {{\frac{\partial {}}{\partial t}}} \left( {\pi}q \right) = 
   - {\nabla_{\rm h} \cdot }\left( {\overline{\left({\pi}{{{\smash[t]{\vec{u}}}}}\right)}}q  \right)  
   

on the surfaces defined by the :math:`\eta'` layer mid points. The
quantity :math:`{\overline{\left({\pi}{{{\smash[t]{\vec{u}}}}}\right)}}`
is the mean flux computed during the dynamics update. The mean flux used
in , combined with a suitable mean vertical flux used in the remap stage
allows HOMME to preserve mass/tracer-mass consistency: The tracer
advection of :math:`{\pi}q` with :math:`q=1` will be identical to the
advection of :math:`{\pi}` implied from . The mass/tracer-mass
consistency capability is not in the version of HOMME included in CAM
4.0, but should be in all later versions.

The equation is discretized in time using the optimal 3 stage strong
stability preserving (SSP) second order Runge-Kutta method from :cite:`spiteri02`.  
The RK-SSP method is chosen because it will preserve
the monotonicity properties of the horizontal discretization. RK-SSP
methods are convex combinations of forward-Euler timesteps, so each
stage :math:`s` of the RK-SSP timestep looks like

.. math::
   :label: E:PEqDlagrange2

   \left( {\pi}q \right)^{s+1} = 
   \left( {\pi}q \right)^s 
   -  \Delta t {\nabla_{\rm h} \cdot }\left( {\overline{\left({\pi}{{{\smash[t]{\vec{u}}}}}\right)}}q^s  \right)  
   

Simply discretizing this equation with the SEM will result in locally
conservative, high-order accurate but oscillatory transport scheme. A
limiter is added to reduce or eliminate these oscillations (:cite:`taylor09`). HOMME supports both monotone and
sign-preserving limiters, but the most effective limiter for HOMME has
not yet been determined. The default configuration in CAM4 is to use the
sign-preserving limiter to prevent negative values of :math:`q` coupled
with a sign-preserving hyper-viscosity operator which dissipates
:math:`q^2`.

Conservation and Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SEM is compatible, meaning it has a discrete version of the
divergence theorem, Stokes theorem and curl/gradient annihilator
properties :cite:`taylor10b`. The divergence theorem is the key
property of the horizontal discretization that is needed to show
conservation. For an arbitrary scalar :math:`h` and vector
:math:`{{{\smash[t]{\vec{u}}}}}` at layer mid-points, the divergence
theorem (or the divergence/gradient adjoint relation) can be written

.. math:: \int h {\nabla\cdot}{{{\smash[t]{\vec{u}}}}}\,{d\mathcal{A}}+ \int {{{\smash[t]{\vec{u}}}}}{\nabla}h \,{d\mathcal{A}}= 0.

The discrete version obeyed by the SEM discretization, using , is given
by

.. math::
   :label: E:IBPDA1

   {\langle}h {\nabla_{\rm h} \cdot }{{{\smash[t]{\vec{u}}}}}{\rangle}+ {\langle}{{{\smash[t]{\vec{u}}}}}\cdot {\nabla_{\rm h}}h {\rangle}= 0.
   

The discrete divergence and Stokes theorem apply locally at the element
with the addition of an element boundary integral. The local form is
used to show local conservation of mass and that the horizontal
advection operator locally conserves the two-dimensional potential
vorticity (\citep{taylor10b}).

In the vertical, :cite:`simmons81b` showed that the
:math:`{ \mathop{\delta_\eta}}` and
:math:`{ \mathop{\overline{ {{\dot\eta}}\delta_\eta }}}` operators
needed to satisfy two integral identities to ensure conservation. For
any :math:`{{\dot\eta}}` layer interface velocity which satisfies
:math:`{{\dot\eta}}_{1/2}={{\dot\eta}}_{K+1/2}=0` and :math:`f,g`
arbitrary functions of layer mid points. The first identity is the
adjoint property (compatibility) for :math:`{ \mathop{\delta_\eta}}` and
:math:`{\pi}`,

.. math::
   :label: E:IBPDN1

   \sum_{i=1}^K \Delta \eta_i\,   {\pi}_i { \mathop{\overline{ {{\dot\eta}}\delta_\eta }}}(f)  
   + 
   \sum_{i=1}^K \Delta \eta_i\,  f_i { \mathop{\delta_\eta}}( {{\dot\eta}}{\pi})
   =0
   

which follows directly from the definition of the
:math:`{ \mathop{\overline{ {{\dot\eta}}\delta_\eta }}}` difference
operator given in . The second identity we write in terms of
:math:`{ \mathop{\delta_\eta}}`,

.. math::
   :label: E:IBPDN2

   \sum_{i=1}^K \Delta\eta_i \,  
    f g { \mathop{\delta_\eta}}( {{\dot\eta}}{\pi})  = 
   \sum_{i=1}^K \Delta\eta_i \,  
   f  { \mathop{\delta_\eta}}( {{\dot\eta}}{\pi}\overline g) 
   +
   \sum_{i=1}^K \Delta\eta_i \,  
   g  { \mathop{\delta_\eta}}( {{\dot\eta}}{\pi}\overline f)
   

which is a discrete integrated-by-parts analog of :math:`
\partial (fg) = f \partial g + g \partial f.
` Construction of methods with both properties on a staggered unequally
spaced grid is the reason behind the complex definition for
:math:`{ \mathop{\overline{ {{\dot\eta}}\delta_\eta }}}` in .

The energy conservation properties of CAM-HOMME were studied in :cite:`taylor10a`)
using the aqua planet test case (:cite:`neale01a,neale01b`). CAM-HOMME uses

.. math::

   E =   
   {\langle}\sum_{i=1}^K \Delta \eta_i {\pi}_i  \left( \frac12 {{{\smash[t]{\vec{u}}}}}^2 + c_p^* T  \right)_i
   {\rangle}+
   {\langle}p_s \Phi_s 
   {\rangle}

as the discretization of the total moist energy . The conservation of
:math:`E` is *semi-discrete*, meaning that the only error in
conservation is the time truncation error. In the adiabatic case (with
no hyper-viscosity and no limiters), running from a fully spun up
initial condition, the error in conservation decreases to machine
precision at a second-order rate with decreasing timestep. In the full
non-adiabatic case with a realistic timestep,
:math:`dE/dt \sim 0.013 \text{W/m}^2`.

The CAM physics conserve a dry energy :math:`E_{\text dry}` from :cite:`boville03`
which is not conserved by the moist primitive
equations. Although :math:`E-E_{\text dry}` is small, adiabatic
processes in the primitive equations result in a net heating
:math:`dE_{\text dry}/dt \sim 0.5 \text{W/m}^2` (:cite:`taylor10a`). If it is
desired that the dynamical core conserve :math:`E_\text{dry}` instead of
:math:`E`, HOMME uses the energy fixer from :ref:`energyfixer`.

Eulerian Dynamical Core
-----------------------

The hybrid vertical coordinate that has been implemented in {\cam} is
described in this section. The hybrid coordinate was developed by
:cite:`simmons81a` in order to provide a general framework for a
vertical coordinate which is terrain following at the Earth's surface,
but reduces to a pressure coordinate at some point above the
surface. The hybrid coordinate is more general in concept than the
modified :math:`sigma` scheme of :cite:`sangster60`, which is used in the
GFDL SKYHI model. However, the hybrid coordinate is normally specified
in such a way that the two coordinates are identical.

The following description uses the same general development as
:cite:`simmons81a`, who based their development on the generalized
vertical coordinate of :cite:`kasahara74`.  A specific form of the
coordinate (the hybrid coordinate) is introduced at the latest
possible point. The description here differs from :cite:`simmons81a` in
allowing for an upper boundary at finite height (nonzero pressure), as
in the original development by Kasahara.  Such an upper boundary may
be required when the equations are solved using vertical finite
differences.


Generalized terrain-following vertical coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deriving the primitive equations in a generalized terrain-following
vertical coordinate requires only that certain basic properties of the
coordinate be specified. If the surface pressure is :math:`\pi`, then we
require the generalized coordinate :math:`\eta(p,\pi)` to satisfy:

#. :math:`\eta(p,\pi)` is a monotonic function of :math:`p`.

#. :math:`\eta(\pi,\pi)=1`

#. :math:`\eta(0,\pi)=0`

#. :math:`\eta(p_t,\pi)=\eta_t` where :math:`p_t` is the top of the
   model.

The latter requirement provides that the top of the model will be a
pressure surface, simplifying the specification of boundary conditions.
In the case that :math:`p_t=0`, the last two requirements are identical
and the system reduces to that described in :cite:`simmons81a`.
The boundary conditions that are required to close the system are:

.. math::
   :label: 3.a.1

   \dot\eta(\pi,\pi) = 0,  

.. math::
   :label: 3.a.2

   \dot\eta(p_t,\pi) =  \omega(p_t) = 0.  

Given the above description of the coordinate, the continuous system of
equations can be written following \citet{kasahara74} and
:cite:`simmons81a`. The prognostic equations are:

.. math::
   :label: 3.a.3

    \frac{\partial\zeta}{\partial t}
    = {\boldsymbol{k}}\cdot\nabla\times ({\boldsymbol{n}}/\cos\phi) +
    F_{\zeta_H} ,  

.. math::
   :label: 3.a.4

   \frac{\partial\delta}{\partial t}
    = \nabla\cdot ({\boldsymbol{n}}/\cos\phi)
   -\nabla^2\left(E+\Phi \right) + F_{\delta_H} ,  

.. math::
   :label: 3.a.5

   \frac{\partial T}{\partial t}  = \frac{-1}{a\cos^2\phi}
   \left[\frac{\partial}{\partial\lambda} (UT) + \cos\phi
   \frac{\partial}{\partial\phi} (VT) \right] + T\delta - \dot\eta
   \frac{\partial T}{\partial\eta} + \frac{R}{c_p^*}{T_v}
   \frac{\omega}{p} \nonumber  
   \phantom{=}  + Q + F_{T_H} + F_{F_H} ,

.. math::
   :label: 3.a.6

   \frac{\partial q}{\partial t}  = 
   \frac{-1}{a\cos^2\phi} \left[ \frac{\partial}{\partial\lambda} (Uq) +
   \cos\phi \frac{\partial}{\partial\phi } (Vq) \right] + q\delta
   - \dot\eta \frac{\partial q}{\partial\eta} + S , 

.. math::
   :label: 3.a.7

   \frac{\partial \pi}{\partial t}  = \int_1^{\eta_t}
   {\mathbf{\nabla}\cdot} \left( \frac{\partial p}{\partial\eta}
   {\boldsymbol{V}} \right) d\eta . 

The notation follows standard conventions, and the following terms have
been introduced with :math:`{\boldsymbol{n}} = (n_U,n_V)`:

.. math::
   :label: 3.a.8

   n_U = + (\zeta+f)V
   - \dot\eta \frac{\partial U}{\partial\eta} R\frac{T_v}{p}\frac{1}{a}
   - \frac{\partial p}{\partial\lambda}
   + F_U \, ,  

.. math::
   :label: 3.a.9

   n_V = - (\zeta+f)U
   - \dot\eta \frac{\partial V}{\partial\eta}
   - R\frac{T_v}{p}\frac{\cos\phi}{a} \frac{\partial p}{\partial\phi}
   + F_V \, ,   

.. math::
   :label: 3.a.10

   E = \frac{U^2+V^2}{2\cos^2\phi} \, ,

.. math::
   :label: 3.a.11

   (U,V) = (u,v)\cos\phi \, , 

.. math::
   :label: 3.a.12

   {T_v} = \left[ 1 + \left( \frac{R_v}{R} -1 \right) q \right] T \, ,
   
.. math::
   :label: 3.a.13

   c_p^* = \left[ 1 + \left( \frac{c_{p_v}}{c_p} -1
	   \right) q \right] c_p \, . 

The terms :math:`F_U, F_V, Q`, and :math:`S` represent the sources and
sinks from the parameterizations for momentum (in terms of :math:`U` and
:math:`V`), temperature, and moisture, respectively. The terms
:math:`F_{\zeta_H}` and :math:`F_{\delta_H}` represent sources due to
horizontal diffusion of momentum, while :math:`F_{T_H}` and
:math:`F_{F_H}` represent sources attributable to horizontal diffusion
of temperature and a contribution from frictional heating (see sections
on horizontal diffusion and horizontal diffusion correction).

In addition to the prognostic equations, three diagnostic equations are
required:

.. math::
   :label: 3.a.14

   \Phi = \Phi_s + R\int_{p(\eta)}^{p(1)}{T_v} d\ln p , 

.. math::
   :label: 3.a.15

   \dot\eta \frac{\partial p}{\partial\eta}  = -\frac{\partial
   p}{\partial t}
    - \int^\eta_{\eta_t} {\mathbf{\nabla}\cdot}\left(\frac{\partial
   p}{\partial\eta}{\boldsymbol{V}}\right) d\eta ,  

.. math::
   :label: 3.a.16

   \omega
    = {\boldsymbol{V} \cdot\nabla}p
   - \int^\eta_{\eta_t} {\mathbf{\nabla}\cdot} \left( \frac{\partial
    p}{\partial\eta} {\boldsymbol{V}} \right) d\eta . 

Note that the bounds on the vertical integrals are specified as values
of :math:`\eta` (:math:`\eta_t`, 1) or as functions of :math:`p`
(:math:`p` (1), which is the pressure at :math:`\eta = 1`).

Conversion to final form
~~~~~~~~~~~~~~~~~~~~~~~~

Equations :eq:`3.a.1` - :eq:`3.a.16` are the complete set which must be solved
by a GCM. However, in order to solve them, the function
:math:`\eta(p,\pi)` must be specified. In advance of actually specifying
:math:`\eta(p,\pi)`, the equations will be cast in a more convenient
form. Most of the changes to the equations involve simple applications
of the chain rule for derivatives, in order to obtain terms that will be
easy to evaluate using the predicted variables in the model. For
example, terms involving horizontal derivatives of :math:`p` must be
converted to terms involving only :math:`\partial p/\partial\pi` and
horizontal derivatives of :math:`\pi`. The former can be evaluated once
the function :math:`\eta(p,\pi)` is specified.

The vertical advection terms in :eq:`3.a.5`, :eq:`3.a.6`, :eq:`3.a.8`, and
:eq:`3.a.9` may be rewritten as:

.. math::
   :label: 3.a.17

   \dot\eta \frac{\partial \psi}{\partial\eta} = \dot\eta \frac{\partial
    p}{\partial\eta}
   \frac{\partial\psi}{\partial p}\, , 

since :math:`\dot\eta {\partial p/\partial\eta}` is given by :eq:`3.a.15` .
Similarly, the first term on the right-hand side of :eq:`3.a.15`  can be
expanded as

.. math::
   :label: 3.a.18

   \frac{\partial p}{\partial t} = \frac{\partial p}{\partial\pi}
    \frac{\partial\pi}{\partial t} ,

and :eq:`3.a.7`  invoked to specify :math:`\partial\pi/\partial t`.

The integrals which appear in :eq:`3.a.7` , :eq:`3.a.15` , and :eq:`3.a.16`  can
be written more conveniently by expanding the kernel as

.. math::
   :label: 3.a.19

   {\mathbf{\nabla}\cdot} \left( \frac{\partial p}{\partial\eta}
    {\boldsymbol{V}} \right) = {\boldsymbol{V}\cdot\nabla} \left(\frac{\partial
    p}{\partial\eta}\right) + \frac{\partial p}{\partial\eta}
    {\mathbf{\nabla}\cdot\boldsymbol{V}} \ .

The second term in :eq:`3.a.19`  is easily treated in vertical integrals,
since it reduces to an integral in pressure. The first term is expanded
to:

.. math::
   :label: 3.a.20

   \begin{aligned}
   {\boldsymbol{V}\cdot\nabla} \left(\frac{\partial p}{\partial\eta}\right)
   & = {\boldsymbol{V}\cdot}\frac{\partial}{\partial\eta}\left(\nabla
   p\right) \nonumber \\
   & = {\boldsymbol{V}\cdot}\frac{\partial}{\partial\eta}
         \left(\frac{\partial p}{\partial\pi}\nabla\pi\right) \nonumber
         \\
   & = {\boldsymbol{V}\cdot}\frac{\partial}{\partial\eta}
         \left(\frac{\partial p}{\partial\pi}\right) \nabla\pi
    + {\boldsymbol{V}\cdot}\frac{\partial p}{\partial\pi}
        \nabla\left(\frac{\partial\pi}{\partial\eta}\right)\,
        . \end{aligned}

The second term in :eq:`3.a.20`  vanishes because
:math:`\partial\pi/\partial\eta=0`, while the first term is easily
treated once :math:`\eta(p,\pi)` is specified. Substituting :eq:`3.a.20` 
into :eq:`3.a.19` , one obtains:

.. math::
   :label: 3.a.21

   {\mathbf{\nabla}\cdot} \left( \frac{\partial p}{\partial\eta}
    {\boldsymbol{V}} \right)
    = \frac{\partial}{\partial\eta} \left(\frac{\partial
         p}{\partial\pi}\right) {\boldsymbol{V}\cdot\nabla}\pi
    + \frac{\partial p}{\partial\eta} {\mathbf{\nabla}\cdot V} \,
    . 

Using :eq:`3.a.21`  as the kernel of the integral in :eq:`3.a.7`, :eq:`3.a.15`,
and :eq:`3.a.16`, one obtains integrals of the form

.. math::
   :label: 3.a.22

   \begin{aligned}
   \int {\mathbf{\nabla}\cdot} \left( \frac{\partial p}{\partial\eta}
    {\boldsymbol{V}}\right) d\eta
   & = \int \left[ \frac{\partial}{\partial\eta}
      \left(\frac{\partial p}{\partial\pi}\right)
       {\boldsymbol{V}\cdot\nabla}\pi + \frac{\partial p}{\partial\eta}
       {\mathbf{\nabla}\cdot V}
      \right] d\eta \nonumber \\
   & = \int {\boldsymbol{V}\cdot\nabla}\pi d\left(\frac{\partial
    p}{\partial\pi}\right) + \int \delta dp. \end{aligned}

The original primitive equations :eq:`3.a.3` -:eq:`3.a.7`, together with
:eq:`3.a.8`, :eq:`3.a.9`, and :eq:`3.a.14` -:eq:`3.a.16`  can now be rewritten
with the aid of :eq:`3.a.17`, :eq:`3.a.18`, and :eq:`3.a.22`.

.. math::
   :label: 3.a.23

    \frac{\partial\zeta}{\partial t} = {\boldsymbol{k}}\cdot\nabla\times
   ({\boldsymbol{n}}/\cos\phi) + F_{\zeta_H} \ ,  

.. math::
   :label: 3.a.24

   \frac{\partial\delta}{\partial t} = {\mathbf{\nabla}\cdot
   (\boldsymbol{n}/\cos\phi)}
    -\nabla^2\left(E+\Phi \right) + F_{\delta_H} \ , 

.. math::
   :label: 3.a.25

   \begin{aligned}
   \frac{\partial T}{\partial t} &=& \frac{-1}{a\cos^2\phi}
   \left[ \frac{\partial}{\partial\lambda} (UT) + \cos\phi
   \frac{\partial}{\partial\phi} (VT) \right] + T\delta
   - \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial
   T}{\partial p} + \frac{R}{c_p^*}{T_v}\frac{\omega}{p} \nonumber \\
   &\phantom{=}& + Q + F_{T_H} + F_{F_H} \\ 
   \end{aligned}

.. math::
   :label: 3.a.26

   \frac{\partial q}{\partial t} = \frac{-1}{a\cos^2\phi}
   \left[ \frac{\partial}{\partial\lambda} (Uq) + \cos\phi
   \frac{\partial}{\partial\phi} (Vq) \right]
   + q\delta - \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial
   q}{\partial p} + S ,  

.. math::
   :label: 3.a.27

   \frac{\partial \pi}{\partial t} = -\int_{(\eta_t)}^{(1)} {\boldsymbol{V}\cdot\nabla}\pi
   d\left(\frac{\partial p}{\partial\pi}\right)
   -\int_{p(\eta_t)}^{p(1)} \delta dp ,   

.. math::
   :label: 3.a.28

   n_U = + (\zeta+f)V
      - \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial
      - U}{\partial p}
      - R\frac{T_v}{a}\frac{1}{p} \frac{\partial p}{\partial\pi}
         \frac{\partial\pi}{\partial\lambda}
      + F_U ,  \\ 

.. math::
   :label: 3.a.29

   n_V = - (\zeta+f)U
   - \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial
   - V}{\partial p} R\frac{{T_v}\cos \phi}{a} \frac{1}{p}
   \frac{\partial p}{\partial\pi} \frac{\partial\pi}{\partial\phi} +  F_V , 

.. math::
   :label: 3.a.30

   \Phi = \Phi_s + R\int_{p(\eta)}^{p(1)}{T_v} d\ln p , 

.. math::
   :label: 3.a.31

   \begin{aligned}
   \dot\eta \frac{\partial p}{\partial\eta}
   &=& \frac{\partial p}{\partial\pi}
   \left[ \int_{(\eta_t)}^{(1)} {\boldsymbol{V}}\cdot\nabla\pi
   d\left(\frac{\partial p}{\partial\pi}\right)
   +\int_{p(\eta_t)}^{p(1)} \delta dp \right] \\ \nonumber
   &\phantom{=}& -\int_{(\eta_t)}^{(\eta)} {\boldsymbol{V}}\cdot\nabla\pi
   d\left( \frac{\partial p}{\partial\pi}\right)
   -\int_{p(\eta_t)}^{p(\eta)} \delta dp ,  
   \end{aligned}

.. math::
   :label: 3.a.32

   \omega = \frac{\partial p}{\partial\pi} {\boldsymbol{V} \cdot\nabla}\pi
   - \int_{(\eta_t)}^{(\eta)} {\boldsymbol{V}\cdot\nabla}\pi
    d\left(\frac{\partial p}{\partial\pi}\right)
   - \int_{p(\eta_t)}^{p(\eta)} \delta dp . 

Once :math:`\eta(p,\pi)` is specified, then
:math:`\partial p/\partial\pi` can be determined and
:eq:`3.a.23` - :eq:`3.a.32` can be solved in a GCM.

In the actual definition of the hybrid coordinate, it is not necessary
to specify :math:`\eta(p,\pi)` explicitly, since :eq:`3.a.23` -:eq:`3.a.32`
only requires that :math:`p` and :math:`\partial
p/\partial\pi` be determined. It is sufficient to specify
:math:`p(\eta,\pi)` and to let :math:`\eta` be defined implicitly. This
will be done in section [ssec:finitediffeqs]. In the case that
:math:`p(\eta,\pi)=\sigma\pi` and :math:`\eta_t=0`,
:eq:`3.a.23` - :eq:`3.a.32` can be reduced to the set of equations solved by
CCM1.

Continuous equations using :math:`\partial\ln(\pi)/\partial t`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In practice, the solutions generated by solving the above equations are
excessively noisy. This problem appears to arise from aliasing problems
in the hydrostatic equation :eq:`3.a.30`. The :math:`\ln p` integral
introduces a high order nonlinearity which enters directly into the
divergence equation :eq:`3.a.24`. Large gravity waves are generated in the
vicinity of steep orography, such as in the Pacific Ocean west of the
Andes.

The noise problem is solved by converting the equations given above,
which use :math:`\pi` as a prognostic variable, to equations using
:math:`\Pi=\ln(\pi)`. This results in the hydrostatic equation becoming
only quadratically nonlinear except for moisture contributions to
virtual temperature. Since the spectral transform method will be used to
solve the equations, gradients will be obtained during the transform
from wave to grid space. Outside of the prognostic equation for
:math:`\Pi`, all terms involving :math:`\nabla\pi` will then appear as
:math:`\pi\nabla\Pi`.

Equations :eq:`3.a.23` -:eq:`3.a.32`  become:

.. math::
   :label: 3.a.33

   \frac{\partial\zeta}{\partial t} = {\boldsymbol{k}\cdot\nabla\times
   (\boldsymbol{n}/\cos\phi)} + F_{\zeta_H} ,  

.. math::
   :label: 3.a.34

   \frac{\partial\delta}{\partial t} = {\mathbf{\nabla}\cdot
   (\boldsymbol{n}/\cos\phi)}
      -\nabla^2\left(E+\Phi \right) + F_{\delta_H} ,  

.. math::
   :label: 3.a.35

   \frac{\partial T}{\partial t}
   = \frac{-1}{a\cos^2\phi} \left[ \frac{\partial}{\partial\lambda}
      (UT) + \cos\phi\frac{\partial}{\partial\phi} (VT) \right] + T\delta
      - \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial
      T}{\partial p} + \frac{R}{c_p^*}{T_v}\frac{\omega}{p} \nonumber
   \phantom{=} + Q + F_{T_H} + F_{F_H} ,  

.. math::
   :label: 3.a.36

   \frac{\partial q}{\partial t}
   = \frac{-1}{a\cos^2\phi} \left[ \frac{\partial}{\partial\lambda}
      (Uq) + \cos\phi \frac{\partial}{\partial\phi} (Vq) \right]
     + q\delta - \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial
    q}{\partial p}
   + S , 

.. math::
   :label: 3.a.37

   \frac{\partial \Pi}{\partial t}
   =-\int_{(\eta_t)}^{(1)} {\boldsymbol{V}\cdot\nabla}\Pi
      d\left(\frac{\partial p}{\partial\pi}\right)
     -\frac{1}{\pi}\int_{p(\eta_t)}^{p(1)} \delta dp ,  

.. math::
   :label: 3.a.38

   n_U = + (\zeta+f)V
      - \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial
      - U}{\partial p} R \frac{T_v}{a} \frac{\pi}{p}
      \frac{\partial p}{\partial\pi} \frac{\partial\Pi}{\partial\lambda}
      + F_U , 

.. math::
   :label: 3.a.39

   n_V = - (\zeta+f)U
      - \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial
      - V}{\partial p} R\frac{{T_v}\cos\phi}{a} \frac{\pi}{p}
       \frac{\partial p}{\partial\pi} \frac{\partial\Pi}{\partial\phi} +
      F_V ,  

.. math::
   :label: 3.a.40

   \Phi = \Phi_s + R\int_{p(\eta)}^{p(1)}{T_v} d\ln p , 
   
.. math::
   :label: 3.a.41

   \begin{aligned}
   \dot\eta \frac{\partial p}{\partial\eta}
   &=& \frac{\partial p}{\partial\pi} \left[ \int_{(\eta_t)}^{(1)} \pi
     {\boldsymbol{V}}\cdot\nabla\Pi d\left(\frac{\partial
     p}{\partial\pi}\right)
    +\int_{p(\eta_t)}^{p(1)} \delta dp \right] \\ \nonumber
     &\phantom{=}& -\int_{(\eta_t)}^{(\eta)} \pi
      {\boldsymbol{V}}\cdot\nabla\Pi d\left(\frac{\partial
      p}{\partial\pi}\right) -\int_{p(\eta_t)}^{p(\eta)} \delta dp ,
   \end{aligned}

.. math::
   :label: 3.a.42

   \omega = \frac{\partial p}{\partial\pi} \pi {\boldsymbol{V}
   \cdot\nabla}\Pi
      - \int_{(\eta_t)}^{(\eta)} \pi {\boldsymbol{V}\cdot\nabla}\Pi
       d\left(\frac{\partial p}{\partial\pi}\right)
      - \int_{p(\eta_t)}^{p(\eta)} \delta dp .

The above equations reduce to the standard :math:`\sigma` equations used
in CCM1 if :math:`\eta=\sigma` and :math:`\eta_t=0`. (Note that in this
case :math:`\partial p / \partial\pi = p/\pi = \sigma`.)

.. _eulSemiImplicit:

Semi-implicit formulation
~~~~~~~~~~~~~~~~~~~~~~~~~

The model described by :eq:`3.a.33` -:eq:`3.a.42` , without the horizontal
diffusion terms, together with boundary conditions :eq:`3.a.1`  and
:eq:`3.a.2` , is integrated in time using the semi-implicit leapfrog scheme
described below. The semi-implicit form of the time differencing will be
applied to :eq:`3.a.34`  and :eq:`3.a.35`  without the horizontal diffusion
sources, and to :eq:`3.a.37` . In order to derive the semi-implicit form,
one must linearize these equations about a reference state. Isolating
the terms that will have their linear parts treated implicitly, the
prognostic equations :eq:`3.a.33` , :eq:`3.a.34` , and :eq:`3.a.37`  may be
rewritten as:

.. math::
   :label: 3.a.43

   \frac{\partial\delta}{\partial t} = - {R{T_v}} \nabla^2 \ln p
   -\nabla^2\Phi + X_1 ,  

.. math::
   :label: 3.a.44

   \frac{\partial T}{\partial t}
   = + \frac{R}{c_p^*}{T_v}\frac{\omega}{p}
    - \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial T}{\partial
    p} + Y_1 , 

.. math::
   :label: 3.a.45

   \frac{\partial\Pi}{\partial t}  = -
   \frac{1}{\pi}\int_{p(\eta_t)}^{p(1)} \delta dp + Z_1 , 

where :math:`X_1, Y_1, Z_1` are the remaining nonlinear terms not
explicitly written in :eq:`3.a.43` -:eq:`3.a.45` . The terms involving
:math:`\Phi` and :math:`\omega` may be expanded into vertical integrals
using :eq:`3.a.40`  and :eq:`3.a.42` , while the :math:`\nabla^2 \ln p` term
can be converted to :math:`\nabla^2\Pi`, giving:

.. math::
   :label: 3.a.46

   \frac{\partial\delta}{\partial t} = -{RT}
   \frac{\pi}{p}\frac{\partial p}{\partial \pi} \nabla^2 \Pi
     -R\nabla^2\int_{p(\eta)}^{p(1)}T d\ln p\ + X_2 ,  

.. math::
   :label: 3.a.47

   \frac{\partial T}{\partial t}
   = - \frac{R}{c_p}\frac{T}{p}
      \int_{p(\eta_t)}^{p(\eta)}\delta dp - \left[ \frac{\partial
       p}{\partial\pi}
      \int_{p(\eta_t)}^{p(1)} \delta dp
     - \int_{p(\eta_t)}^{p(\eta)} \delta dp \right] \frac{\partial
      T}{\partial p}
     + Y_2 ,

.. math::
   :label: 3.a.48

   \frac{\partial\Pi}{\partial t}  = -
   \frac{1}{pi}\int_{p(\eta_t)}^{p(1)} \delta dp + Z_2 .

Once again, only terms that will be linearized have been explicitly
represented in :eq:`3.a.46` -:eq:`3.a.48` , and the remaining terms are
included in :math:`X_2`, :math:`Y_2`, and :math:`Z_2`. Anticipating the
linearization, :math:`T_v` and :math:`c_p^*` have been replaced by
:math:`T` and :math:`c_p` in :eq:`3.a.46`  and :eq:`3.a.47`. Furthermore, the
virtual temperature corrections are included with the other nonlinear
terms.

In order to linearize :eq:`3.a.46` - :eq:`3.a.48`, one specifies a reference
state for temperature and pressure, then expands the equations about the
reference state:

.. math::
   :label: 3.a.49

   T  = T^r + T^\prime ,   

.. math::
   :label: 3.a.50

   \pi = \pi^r + \pi^\prime ,
   
.. math::
   :label: 3.a.51

   p  = p^r(\eta,\pi^r) + p^\prime . 

In the special case that :math:`p(\eta,\pi)=\sigma\pi`,
:eq:`3.a.46` - :eq:`3.a.48`  can be converted into equations involving only
:math:`\Pi=\ln\pi` instead of :math:`p`, and :eq:`3.a.50`  and :eq:`3.a.51` 
are not required. This is a major difference between the hybrid
coordinate scheme being developed here and the :math:`\sigma` coordinate
scheme in CCM1.

Expanding :eq:`3.a.46` -:eq:`3.a.48`  about the reference state
:eq:`3.a.49` -:eq:`3.a.51`  and retaining only the linear terms explicitly,
one obtains:

.. math::
   :label: 3.a.52

   \frac{\partial\delta}{\partial t}
   = -R\nabla^2 \left[ T^{r} \frac{\pi^r}{p^r} \left(\frac{\partial
     p}{\partial\pi} \right)^r \Pi
    + \int_{p^r(\eta)}^{p^r(1)}T^\prime d\ln p^r
    + \int_{p^\prime(\eta)}^{p^\prime(1)}\frac{T^r}{p^r} dp^\prime
      \right]
    + X_3 ,   

.. math::
   :label: 3.a.53

   \frac{\partial T}{\partial t}
   = - \frac{R}{c_p}\frac{T^r}{p^r}
       \int_{p^r(\eta_t)}^{p^r(\eta)}\delta dp^r
     - \left[ \left(\frac{\partial p}{\partial\pi}\right)^r
       \int_{p^r(\eta_t)}^{p^r(1)} \delta dp^r
      - \int_{p^r(\eta_t)}^{p^r(\eta)} \delta dp^r \right] \frac{\partial
       T^r}{\partial p^r}
     + Y_3, 

.. math::
   :label: 3.a.54

   \frac{\partial \Pi}{\partial t} = -
   \frac{1}{\pi^r}\int_{p^r(\eta_t)}^{p^r(1)} \delta dp^r + Z_3
   . 

The semi-implicit time differencing scheme treats the linear terms in
:eq:`3.a.52` -:eq:`3.a.54`  by averaging in time. The last integral in
:eq:`3.a.52`  is reduced to purely linear form by the relation

.. math::
   :label: 3.a.55

   dp^\prime = \pi^\prime d \left(\frac{\partial p}{\partial\pi}\right)^r
   + x \, . 

In the hybrid coordinate described below, :math:`p` is a linear
function of :math:`\pi`, so :math:`x` above is zero.

We will assume that centered differences are to be used for the
nonlinear terms, and the linear terms are to be treated implicitly by
averaging the previous and next time steps. Finite differences are used
in the vertical, and are described in the following sections. At this
stage only some very general properties of the finite difference
representation must be specified. A layering structure is assumed in
which field values are predicted on :math:`K` layer midpoints denoted by
an integer index, :math:`\eta_k` (see Figure :ref:`figure-1`). The interface
between :math:`\eta_k` and :math:`\eta_{k+1}` is denoted by a
half-integer index, :math:`\eta_{k+1/2}`. The model top is at
:math:`\eta_{1/2}=\eta_t`, and the Earth’s surface is at
:math:`\eta_{K+1/2}=1`. It is further assumed that vertical integrals
may be written as a matrix (of order :math:`K`) times a column vector
representing the values of a field at the :math:`\eta_k` grid points in
the vertical. The column vectors representing a vertical column of grid
points will be denoted by underbars, the matrices will be denoted by
bold-faced capital letters, and superscript :math:`T` will denote the
vector transpose.

.. figure:: figures/figure3-1.jpg
   :align: center

   Vertical structure of |cam|

The finite difference forms of :eq:`3.a.52` -:eq:`3.a.54`  may then be written
down as:

.. math::
   :label: 3.a.56

   \begin{aligned}
   \underline{\delta}^{n+1}
   & = &\underline{\delta}^{n-1} + 2\Delta t \underline{X}^n \nonumber \\
   &\phantom{=}& - 2\Delta t R \underline{b}^r \nabla^2 \left(
         \frac{\Pi^{n-1} + \Pi^{n+1}}{2} - \Pi^{n} \right) \nonumber \\
   &\phantom{=}& - 2\Delta t R{\boldsymbol{H}}^r \nabla^2 \left(
         \frac{(\underline{T}^\prime)^{n-1} +
         (\underline{T}^\prime)^{n+1}}{2}
         - (\underline{T}^\prime)^{n} \right) \nonumber \\
   &\phantom{=}& - 2\Delta t R \underline{h}^r \nabla^2
         \left( \frac{\Pi^{n-1} + \Pi^{n+1}}{2} - \Pi^{n}
         \right) ,  \\ \underline{T}^{n+1}
   & = & \underline{T}^{n-1} + 2 \Delta t \underline{Y}^n
    - 2\Delta t {\boldsymbol{D}}^r \left( \frac{\underline{\delta}^{n-1} +
          \underline{\delta}^{n+1}}{2}
               - \underline{\delta}^n \right)
   , \\ \Pi^{n+1}
   & = & \Pi^{n-1} + 2\Delta t Z^n
    - 2\Delta t \left( \frac{\underline{\delta}^{n-1} +
        \underline{\delta}^{n+1}}{2}
             - \underline{\delta}^n \right)^T \frac{1}{\Pi^r}
      \underline{\Delta p}^r
   , \end{aligned}

where :math:`()^n` denotes a time varying value at time step :math:`n`.
The quantities :math:`\underline{X}^n, \underline{Y}^n,` and :math:`Z^n`
are defined so as to complete the right-hand sides of
:eq:`3.a.43` -:eq:`3.a.45`. The components of :math:`\underline{\Delta
p}^r` are given by
:math:`\Delta p^r_k = p^r_{k + \frac{1}{2}} - p^r_{k -
\frac{1}{2}}`. This definition of the vertical difference operator
:math:`\Delta` will be used in subsequent equations. The reference
matrices :math:`{\boldsymbol{H}}^r` and :math:`{\boldsymbol{D}}^r`,
and the reference column vectors :math:`\displaystyle\underline{b}^r`
and :math:`\displaystyle\underline{h}^r`, depend on the precise
specification of the vertical coordinate and will be defined later.

.. _eul-econserve:

Energy conservation
~~~~~~~~~~~~~~~~~~~

We shall impose a requirement on the vertical finite differences of the
model that they conserve the global integral of total energy *in the
absence of sources and sinks*. We need to derive equations for kinetic
and internal energy in order to impose this constraint. The momentum
equations (more painfully, the vorticity and divergence equations)
without the :math:`F_U, F_V, F_{\zeta_H}` and :math:`F_{\delta_H}`
contributions, can be combined with the continuity equation

.. math::
   :label: 3.a.59

   \frac{\partial}{\partial t} \left( \frac{\partial p}{\partial\eta}
         \right)
    + \nabla\cdot \left( \frac{\partial p}{\partial\eta} {\boldsymbol{V}}
         \right)
    + \frac{\partial}{\partial \eta} \left( \frac{\partial
         p}{\partial\eta} \dot\eta \right)
    = 0 

to give an equation for the rate of change of kinetic energy:

.. math::
   :label: 3.a.60

   \begin{aligned}
   \frac{\partial}{\partial t} \left( \frac{\partial p}{\partial\eta} E
         \right)
   &=& -\nabla\cdot \left( \frac{\partial p}{\partial\eta} E
         {\boldsymbol{V}} \right)
    - \frac{\partial}{\partial \eta} \left( \frac{\partial
         p}{\partial\eta} E \dot\eta \right) \nonumber \\
   &\phantom{=}&- \frac{R{T_v}}{p} \frac{\partial p}{\partial\eta}
   {\boldsymbol{V}}\cdot\nabla p
    - \frac{\partial p}{\partial\eta} {\boldsymbol{V}}\cdot\nabla\Phi \,
    - . \end{aligned}

The first two terms on the right-hand side of :eq:`3.a.60`  are transport
terms. The horizontal integral of the first (horizontal) transport term
should be zero, and it is relatively straightforward to construct
horizontal finite difference schemes that ensure this. For spectral
models, the integral of the horizontal transport term will not vanish in
general, but we shall ignore this problem.

The vertical integral of the second (vertical) transport term on the
right-hand side of :eq:`3.a.60`  should vanish. Since this term is obtained
from the vertical advection terms for momentum, which will be finite
differenced, we can construct a finite difference operator that will
ensure that the vertical integral vanishes.

The vertical advection terms are the product of a vertical velocity
(:math:`\dot\eta \partial p/\partial\eta`) and the vertical derivative
of a field (:math:`\partial\psi/\partial p`). The vertical velocity is
defined in terms of vertical integrals of fields :eq:`3.a.41` , which are
naturally taken to interfaces. The vertical derivatives are also
naturally taken to interfaces, so the product is formed there, and then
adjacent interface values of the products are averaged to give a
midpoint value. It is the definition of the average that must be correct
in order to conserve kinetic energy under vertical advection in
:eq:`3.a.60` . The derivation will be omitted here, the resulting vertical
advection terms are of the form:

.. math::
   :label: 3.a.61

   \left( \dot\eta \frac{\partial p}{\partial\eta} \frac{\partial
         \psi}{\partial p} \right)_{k}
   = \frac{1}{2\Delta p_k}
      \left[ \left( \dot\eta \frac{\partial p}{\partial\eta}
           \right)_{k+1/2} \left( \psi_{k+1} - \psi_k \right)
         + \left( \dot\eta \frac{\partial p}{\partial\eta}
           \right)_{k-1/2} \left( \psi_k - \psi_{k-1} \right)
      \right] ,  

.. math::
   :label: 3.a.62

   \Delta p_k = p_{k+1/2} - p_{k-1/2}
   .

The choice of definitions for the vertical velocity at interfaces is not
crucial to the energy conservation (although not completely arbitrary),
and we shall defer its definition until later. The vertical advection of
temperature is not required to use :eq:`3.a.61`  in order to conserve mass
or energy. Other constraints can be imposed that result in different
forms for temperature advection, but we will simply use :eq:`3.a.61`  in
the system described below.

The last two terms in :eq:`3.a.60`  contain the conversion between kinetic
and internal (potential) energy and the form drag. Neglecting the
transport terms, under assumption that global integrals will be taken,
noting that :math:`\nabla p/p = \frac{\pi}{p} \frac{\partial
p}{\partial\pi} \nabla \Pi`, and substituting for the geopotential using
:eq:`3.a.40` , :eq:`3.a.60`  can be written as:

.. math::
   :label: 3.a.63

   \begin{aligned}
   \frac{\partial}{\partial t} \left( \frac{\partial p}{\partial\eta} E
         \right)
   &=&- {R{T_v}} \frac{\partial p}{\partial\eta} {\boldsymbol{V}} \cdot
      \left( \frac{\pi}{p} \frac{\partial p}{\partial\pi} \nabla \Pi
      \right) \\
   \nonumber &\phantom{=}& - \frac{\partial p}{\partial\eta}
   {\boldsymbol{V}}\cdot\nabla\Phi_s
    - \frac{\partial p}{\partial\eta} {\boldsymbol{V}}\cdot\nabla
         \int_{p(\eta)}^{p(1)}R{T_v} d\ln p
    + \, \ldots \end{aligned}

The second term on the right-hand side of :eq:`3.a.63`  is a source (form
drag) term that can be neglected as we are only interested in internal
conservation properties. The last term on the right-hand side of
:eq:`3.a.63`  can be rewritten as

.. math::
   :label: 3.a.64

   \frac{\partial p}{\partial\eta} {\boldsymbol{V}}\cdot\nabla
         \int_{p(\eta)}^{p(1)}R{T_v} d\ln p
   = \nabla\cdot
        \left\{ \frac{\partial p}{\partial\eta} {\boldsymbol{V}}
           \int_{p(\eta)}^{p(1)}R{T_v} d\ln p
        \right\}
   - \nabla\cdot
        \left( \frac{\partial p}{\partial\eta} {\boldsymbol{V}}
        \right) \int_{p(\eta)}^{p(1)}R{T_v} d\ln p \, . 

The global integral of the first term on the right-hand side of
:eq:`3.a.64`  is obviously zero, so that :eq:`3.a.63`  can now be written as:

.. math::
   :label: 3.a.65

   \frac{\partial}{\partial t} \left( \frac{\partial p}{\partial\eta} E
         \right)
   =- {R{T_v}} \frac{\partial p}{\partial\eta} {\boldsymbol{V}} \cdot \left(
      \frac{\pi}{p} \frac{\partial p}{\partial\pi} \nabla \Pi \right)
   + \nabla\cdot \left( \frac{\partial p}{\partial\eta} {\boldsymbol{V}}
        \right) \int_{p(\eta)}^{p(1)}R{T_v} d\ln p
    + ...  

We now turn to the internal energy equation, obtained by combining the
thermodynamic equation :eq:`3.a.35` , without the :math:`Q`,
:math:`F_{T_H}`, and :math:`F_{F_H}` terms, and the continuity equation
:eq:`3.a.59` :

.. math::
   :label: 3.a.66

   \frac{\partial}{\partial t} \left( \frac{\partial p}{\partial\eta}
         c_p^* T \right)
   = -\nabla\cdot \left( \frac{\partial p}{\partial\eta} c_p^* T
         {\boldsymbol{V}} \right)
    - \frac{\partial}{\partial \eta} \left( \frac{\partial
         p}{\partial\eta} c_p^* T \dot\eta \right)
   + {R{T_v}} \frac{\partial p}{\partial\eta} \frac{\omega}{p} \, .
   

As in :eq:`3.a.60` , the first two terms on the right-hand side are
advection terms that can be neglected under global integrals. Using
:eq:`3.a.16` , :eq:`3.a.66`  can be written as:

.. math::
   :label: 3.a.67

   \frac{\partial}{\partial t} \left( \frac{\partial p}{\partial\eta}
         c_p^* T \right)
   = {R{T_v}} \frac{\partial p}{\partial\eta} {\boldsymbol{V}} \cdot \left(
     \frac{\pi}{p} \frac{\partial p}{\partial\pi} \nabla \Pi \right)
   - {R{T_v}} \frac{\partial p}{\partial\eta} \frac{1}{p}
        \int_{\eta_t}^{\eta} \nabla\cdot
        \left( \frac{\partial p}{\partial\eta} {\boldsymbol{V}}
        \right) d\eta + ... 

The rate of change of total energy due to internal processes is obtained
by adding :eq:`3.a.65`  and :eq:`3.a.67`  and must vanish. The first terms on
the right-hand side of :eq:`3.a.65`  and :eq:`3.a.67`  obviously cancel in the
continuous form. When the equations are discretized in the vertical, the
terms will still cancel, providing that the same definition is used for
:math:`(1/p\,\,\partial p/\partial\pi)_k` in the nonlinear terms of the
vorticity and divergence equations :eq:`3.a.38`  and :eq:`3.a.39` , and in the
:math:`\omega` term of :eq:`3.a.35`  and :eq:`3.a.42` .

The second terms on the right-hand side of :eq:`3.a.65`  and :eq:`3.a.67` 
must also cancel in the global mean. This cancellation is enforced
locally in the horizontal on the column integrals of :eq:`3.a.65`  and
:eq:`3.a.67` , so that we require:

.. math::
   :label: 3.a.68

   \int^1_{\eta_t} \left\{ \nabla\cdot
        \left( \frac{\partial p}{\partial\eta} {\boldsymbol{V}}
        \right) \int_{p(\eta)}^{p(1)}R{T_v} d\ln p
   \right\} d\eta
   =\int^1_{\eta_t} \left\{ {R{T_v}} \frac{\partial p}{\partial\eta}
        \frac{1}{p} \int_{\eta_t}^{\eta} \nabla\cdot
        \left( \frac{\partial p}{\partial\eta^\prime} {\boldsymbol{V}}
        \right) d\eta^\prime \right\} d\eta . 

The inner integral on the left-hand side of :eq:`3.a.68`  is derived from
the hydrostatic equation :eq:`3.a.40` , which we shall approximate as

.. math::
   :label: 3.a.69

   \Phi_k = \Phi_s + R\sum_{\ell=k}^K H_{k\ell}{T_v}_\ell , \nonumber
   \\  = \Phi_s + R\sum_{\ell=1}^K H_{k\ell}{T_v}_\ell , 

.. math::
   :label: 3.a.70

   \underline{\Phi} = \Phi_s \underline{1} + R {\boldsymbol{H}}
   \underline {T_v} , 

where :math:`H_{k\ell}=0` for :math:`\ell<k`. The quantity
:math:`\underline{1}` is defined to be the unit vector. The inner
integral on the right-hand side of :eq:`3.a.68`  is derived from the
vertical velocity equation :eq:`3.a.42` , which we shall approximate as

.. math::
   :label: 3.a.71

   \left( \frac{\omega}{p} \right)_k
   = \left( \frac{\pi}{p} \frac{\partial p}{\partial\pi} \right)_k
            {\boldsymbol{V}}_k \cdot \nabla\Pi
   - \sum_{\ell=1}^K C_{k\ell}
         \left[ \delta_\ell \Delta p_\ell
            + \pi \left({\boldsymbol{V}}_\ell \cdot \nabla \Pi \right)
              \Delta \left( \frac{\partial p}{\partial\pi} \right)_\ell
         \right] , 

where :math:`C_{k\ell}=0` for :math:`\ell>k`, and :math:`C_{k\ell}` is
included as an approximation to :math:`1/p_k` for :math:`\ell \leq k`
and the symbol :math:`\Delta` is similarly defined as in :eq:`3.a.62` .
:math:`C_{k\ell}` will be determined so that :math:`\omega` is
consistent with the discrete continuity equation following 
:cite:`williamson94a`. Using :eq:`3.a.69`  and :eq:`3.a.71` , the
finite difference analog of :eq:`3.a.68`  is

.. math::
   :label: 3.a.72

   \begin{aligned}
   \nonumber\lefteqn{\sum_{k=1}^K
     \left\{ \frac{1}{\Delta\eta_k}
         \left[ \delta_k \Delta p_k
            + \pi \left({\boldsymbol{V}}_k \cdot \nabla \Pi \right) \Delta
              \left( \frac{\partial p}{\partial\pi} \right)_k
         \right] R\sum_{\ell=1}^K H_{k\ell}{T_v}_\ell
     \right\} \Delta\eta_k } \\
   & & \mbox{} = \sum_{k=1}^K
     \left\{ R {T_v}_k \frac{\Delta p_k}{\Delta\eta_k}
         \sum_{\ell=1}^K C_{k\ell}
            \left[ \delta_\ell \Delta p_\ell
               + \pi \left( {\boldsymbol{V}}_\ell \cdot \nabla \Pi \right)
                 \Delta \left( \frac{\partial p}{\partial\pi}
                 \right)_\ell
            \right] \right\} \Delta\eta_k , \end{aligned}

where we have used the relation

.. math::

   \nabla\cdot {\boldsymbol{V}}(\partial p/\partial\eta )_k =[\delta_k\Delta
   p_k + \\
   \pi\left( {\boldsymbol{V}}_k\cdot\nabla\Pi \right) \Delta \left(\partial
       p/\partial\pi\right)_k ]/\Delta\eta_k

(see [3.a.22]). We can now combine the sums in :eq:`3.a.72`  and simplify
to give

.. math::
   :label: 3.a.73

   \begin{aligned}
   \nonumber\lefteqn{\sum_{k=1}^K \sum_{\ell=1}^K
     \left\{
         \left[ \delta_k \Delta p_k
            + \pi \left({\boldsymbol{V}}_k \cdot \nabla \Pi \right) \Delta
              \left( \frac{\partial p}{\partial\pi} \right)_k
         \right] H_{k\ell}{T_v}_\ell
     \right\}} \\
   & & \mbox{} = \sum_{k=1}^K \sum_{\ell=1}^K
     \left\{
         \left[ \delta_\ell \Delta p_\ell
            + \pi \left( {\boldsymbol{V}}_\ell \cdot \nabla \Pi \right)
              \Delta \left( \frac{\partial p}{\partial\pi} \right)_\ell
         \right] \Delta p_k C_{k\ell}{T_v}_k
     \right\} . \end{aligned}

Interchanging the indexes on the left-hand side of :eq:`3.a.73`  will
obviously result in identical expressions if we require that

.. math:: 
   :label: 3.a.74

   H_{k\ell} = C_{\ell k} \Delta p_\ell .

Given the definitions of vertical integrals in :eq:`3.a.70`  and :eq:`3.a.71` 
and of vertical advection in :eq:`3.a.61`  and :eq:`3.a.62`  the model will
conserve energy as long as we require that :math:`\boldsymbol{C}` and
:math:`\boldsymbol{H}` satisfy :eq:`3.a.74` . We are, of course, still
neglecting lack of conservation due to the truncation of the horizontal
spherical harmonic expansions.

.. _eul-hdiff:

Horizontal diffusion
~~~~~~~~~~~~~~~~~~~~

|cam| contains a horizontal diffusion term for :math:`T, \zeta`, and
:math:`\delta` to prevent spectral blocking and to provide reasonable
kinetic energy spectra. The horizontal diffusion operator in |cam| is also
used to ensure that the CFL condition is not violated in the upper
layers of the model. The horizontal diffusion is a linear
:math:`\nabla^2` form on :math:`\eta` surfaces in the top three levels
of the model and a linear :math:`\nabla^4` form with a partial
correction to pressure surfaces for temperature elsewhere. The
:math:`\nabla^2` diffusion near the model top is used as a simple sponge
to absorb vertically propagating planetary wave energy and also to
control the strength of the stratospheric winter jets. The
:math:`\nabla^2` diffusion coefficient has a vertical variation which
has been tuned to give reasonable Northern and Southern Hemisphere polar
night jets.

In the top three model levels, the :math:`\nabla^2` form of the
horizontal diffusion is given by

.. math::
   :label: 3.a.75

   F_{\zeta_H} = K^{(2)} \left[ \nabla^2 \left(\zeta + f \right) +
   2\left(\zeta + f \right)/a^2 \right] ,  

.. math::
   :label: 3.a.76

   F_{\delta_H}
   = K^{(2)} \left[ \nabla^2 \delta + 2(\delta/a^2)\right] ,

.. math::
   :label: 3.a.77

   F_{T_H} = K^{(2)} \nabla^2T . 

Since these terms are linear, they are easily calculated in spectral
space. The undifferentiated correction term is added to the vorticity
and divergence diffusion operators to prevent damping of uniform
:math:`(n=1)` rotations (:cite:`orszag74,bourke77`). The
:math:`\nabla^2` form of the horizontal diffusion is applied *only* to
pressure surfaces in the standard model configuration.

The horizontal diffusion operator is better applied to pressure surfaces
than to terrain-following surfaces (applying the operator on isentropic
surfaces would be still better). Although the governing system of
equations derived above is designed to reduce to pressure surfaces above
some level, problems can still occur from diffusion along the lower
surfaces. Partial correction to pressure surfaces of harmonic horizontal
diffusion (:math:`\partial\xi/\partial t =
K\nabla^2\xi`) can be included using the relations:

.. math::
   :label: 3.a.78

   \begin{aligned}
   \nabla_p\xi & = \nabla_\eta\xi - p \frac{\partial\xi}{\partial p}
   \nabla_\eta \ln p \nonumber \\ \nabla^2_p\xi & = \nabla^2_\eta\xi
   - p \frac{\partial\xi}{\partial p} \nabla^2_\eta \ln p
   - 2\nabla_\eta\left( \frac{\partial\xi}{\partial p}
     \right)\cdot\nabla_\eta p
   + \frac{\partial^2\xi}{\partial^2 p} \nabla^2_\eta p \,
   . \end{aligned}

Retaining only the first two terms above gives a correction to the
:math:`\eta` surface diffusion which involves only a vertical derivative
and the Laplacian of log surface pressure,

.. math::
   :label: 3.a.79

   \nabla^2_p\xi = \nabla^2_\eta\xi
     - \pi \frac{\partial\xi}{\partial p} \frac{\partial p}{\partial\pi}
         \nabla^2 \Pi + \ldots 

Similarly, biharmonic diffusion can be partially corrected to pressure
surfaces as:

.. math::
   :label: 3.a.80

   \nabla^4_p\xi = \nabla^4_\eta\xi
     - \pi \frac{\partial\xi}{\partial p} \frac{\partial p}{\partial\pi}
         \nabla^4 \Pi + \ldots 

The bi-harmonic :math:`\nabla^4` form of the diffusion operator is
applied at all other levels (generally throughout the troposphere) as

.. math::
   :label: 3.a.81

   F_{\zeta_H} = -K^{(4)} \left[\nabla^4 \left(\zeta + f \right) -
   \left(\zeta + f \right) \left( 2/a^2\right)^2 \right] , 

.. math::
   :label: 3.a.82

   F_{\delta_H} = -K^{(4)} \left[\nabla^4 \delta - \delta (2/a^2)^2
   \right],

.. math::
   :label: 3.a.83

   F_{T_H} = -K^{(4)} \left[ \nabla^4 T - \pi \frac{\partial
   T}{\partial p} \frac{\partial p}{\partial \pi} \nabla^4 \Pi \right]
   .

The second term in :math:`F_{T_H}` consists of the leading term in the
transformation of the :math:`\nabla^4` operator to pressure surfaces. It
is included to offset partially a spurious diffusion of :math:`T` over
mountains. As with the :math:`\nabla^2` form, the :math:`\nabla^4`
operator can be conveniently calculated in spectral space. The
correction term is then completed after transformation of :math:`T` and
:math:`\nabla^4 \Pi` back to grid–point space. As with the
:math:`\nabla^2` form, an undifferentiated term is added to the
vorticity and divergence diffusion operators to prevent damping of
uniform rotations.

.. _ssec-finitediffeqs:

Finite difference equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The governing equations are solved using the spectral method in the
horizontal, so that only the vertical and time differences are presented
here. The dynamics includes horizontal diffusion of :math:`T,
(\zeta + f)`, and :math:`\delta`. Only :math:`T` has the leading term
correction to pressure surfaces. Thus, equations that include the terms
in this time split sub-step are of the form

.. math::
   :label: 3.a.84

   \frac{\partial \psi}{\partial t} = {\rm Dyn} \left( \psi \right) -
   (-1)^i K^{(2i)} \nabla^{2i}_\eta \psi \, , 

for :math:`(\zeta + f)` and :math:`\delta`, and

.. math::
   :label: 3.a.85

   \frac{\partial T}{\partial t} = {\rm Dyn} \left( T \right) - (-1)^i
   K^{(2i)} \left\{ \nabla^{2i}_\eta T - \pi \frac{\partial T} {\partial
   p} \, \frac{\partial p}{\partial \pi} \nabla^{2i} \Pi \right\}\, ,
   

where :math:`i = 1` in the top few model levels and :math:`i = 2`
elsewhere (generally within the troposphere). These equations are
further subdivided into time split components:

.. math::
   :label: 3.a.86

   \psi^{n+1} = \psi^{n-1} + 2\Delta t \ {\rm Dyn} \left( \psi^{n+1},
   	\psi^n, \psi^{n-1} \right) \ ,  

.. math::
   :label: 3.a.87

   \psi^*  = \psi^{n+1} - 2\Delta t \ (-1)^i K^{(2i)} \nabla^{2i}_\eta
   	\left( {\psi}^{*n+1} \right) \ , 

.. math::
   :label: 3.a.88

   \hat \psi^{n+1} & = \psi^* \ ,

for :math:`\left( \zeta + f \right)` and :math:`\delta`, and

.. math::
   :label: 3.a.89

   T^{n+1} = T^{n-1} + 2\Delta t \ {\rm Dyn} \left( T^{n+1}, T^n,
   T^{n-1} \right) \,  

.. math::
   :label: 3.a.90

   T^*  = T^{n+1} - 2\Delta t \
   \left( -1 \right)^i K^{(2i)} \nabla^{2i}\eta \left( T^* \right) \ ,

.. math::
   :label: 3.a.91

   \hat T^{n+1}  = T^* + 2\Delta t \ \left( -1
   \right)^i K^{(2i)} \pi \, \frac{\partial T^*}{\partial p} \,
   \frac{\partial p}{\partial \pi} \, \nabla^{2i} \, \Pi \ ,

for :math:`T`, where in the standard model :math:`i` only takes the
value 2 in :eq:`3.a.91` . The first step from
:math:`\left( \hskip 5pt \right)^{n-1}` to
:math:`\left( \hskip 5pt \right)^{n+1}` includes the transformation to
spectral coefficients. The second step from :math:`\left( \hskip 5pt
\right)^{n+1}` to :math:`\left( \hat{\hskip 5pt} \right)^{n+1}` for
:math:`\delta` and :math:`\zeta \,`, or
:math:`\left( \hskip 5pt \right)^{n+1}` to :math:`\left( \hskip
5pt \right)^*` for :math:`T`, is done on the spectral coefficients, and
the final step from :math:`\left( \hskip 5pt \right)^*` to
:math:`\left( \hat{\hskip
5pt} \right)^{n+1}` for :math:`T` is done after the inverse transform to
the grid point representation.

The following finite-difference description details only the forecast
given by :eq:`3.a.86`  and :eq:`3.a.89` . The finite-difference form of the
forecast equation for water vapor will be presented later in Section 3c.
The general structure of the complete finite difference equations is
determined by the semi-implicit time differencing and the energy
conservation properties described above. In order to complete the
specification of the finite differencing, we require a definition of the
vertical coordinate. The actual specification of the generalized
vertical coordinate takes advantage of the structure of the equations
:eq:`3.a.33` -:eq:`3.a.42` . The equations can be finite-differenced in the
vertical and, in time, without having to know the value of :math:`\eta`
anywhere. The quantities that must be known are :math:`p` and
:math:`\partial p/\partial\pi` at the grid points. Therefore the
coordinate is defined implicitly through the relation:

.. math:: p(\eta,\pi) = A(\eta)p_0 + B(\eta)\pi \, , 
	  :label: 3.a.92

which gives

.. math:: \frac{\partial p}{\partial\pi} = B(\eta) \, . 
	  :label: 3.a.93

A set of levels :math:`\eta_k` may be specified by specifying
:math:`A_k` and :math:`B_k`, such that :math:`\eta_k \equiv A_k + B_k`,
and difference forms of :eq:`3.a.33` -:eq:`3.a.42`  may be derived.

The finite difference forms of the Dyn operator :eq:`3.a.33` -:eq:`3.a.42` ,
including semi-implicit time integration are:

.. math::
   :label: 3.a.94

   \underline{\zeta}^{n+1}
    =  \underline{\zeta}^{n-1} + 2\Delta t
    {\boldsymbol{k}\cdot\nabla\times}\left(\underline{\boldsymbol{n}}^n/\cos\phi\right)
   ,  

.. math::
   :label: 3.a.95

   \begin{aligned}
   \underline{\delta}^{n+1}
   & = & \underline{\delta}^{n-1}
    + 2\Delta t \left[ {\nabla\cdot
          \left(\underline{\boldsymbol{n}}^n/\cos\phi\right)}
        - \nabla^2 \left( \underline{E}^n + \Phi_s \underline{1} +
              R{\boldsymbol{H}}^n (\underline{T_v}^{'})^n \right)
      \right] \nonumber \\
   &\phantom{=}& - 2\Delta t R{\boldsymbol{H}}^r \nabla^2 \left(
        \frac{(\underline{T}^\prime)^{n-1} +
        (\underline{T}^\prime)^{n+1}}{2}
              - (\underline{T}^\prime)^{n} \right) \nonumber \\
   &\phantom{=}& - 2\Delta t R\left( \underline{b}^r + \underline{h}^r
         \right) \nabla^2
         \left( \frac{\Pi^{n-1} + \Pi^{n+1}}{2} - \Pi^{n}
         \right) ,
   \end{aligned}

.. math::
   :label: 3.a.96

   \begin{aligned}
   (\underline{T}^{'})^{n+1} & = & (\underline{T}^{'})^{n-1}
    - 2 \Delta t \left[ \frac{1}{a\cos^2\phi}
           \frac{\partial}{\partial\lambda} \left( \underline{UT}^\prime
           \right)^n
         + \frac{1}{a\cos\phi} \frac{\partial}{\partial\phi} \left(
           \underline{VT}^\prime \right)^n
         - \underline{\Gamma}^n \right] \\ \nonumber
   &\phantom{=}& - 2\Delta t {\boldsymbol{D}}^r \left(
          \frac{\underline{\delta}^{n-1} + \underline{\delta}^{n+1}}{2}
               - \underline{\delta}^n \right) \,
   \end{aligned}

.. math::
   :label: 3.a.97

   \begin{aligned}
   \Pi^{n+1} & = & \Pi^{n-1}
    - 2\Delta t \frac{1}{\pi^n} \left( \left(\underline{\delta}^n
         \right)^T \underline{\Delta p}^n
       + \left(\underline{\boldsymbol{V}}^n \right)^T \cdot \nabla \Pi^n
   	\pi^n \underline{\Delta B}
   \right) \nonumber \\
   &\phantom{=}& - 2\Delta t \left( \frac{\underline{\delta}^{n-1} +
          \underline{\delta}^{n+1}}{2}
             - \underline{\delta}^n \right)^T \frac{1}{\pi^r}
      \underline{\Delta p}^r
   , 
   \end{aligned}

.. math::
   :label: 3.a.98

   \begin{aligned}
   \left( n_U \right)_k & = & \left( \zeta_k + f \right) V_k
    - R{T_v}_k \left( \frac{1}{p} \frac{\partial p}{\partial\pi}
      \right)_k \pi \frac{1}{a} \frac{\partial \Pi}{\partial\lambda}
      \nonumber \\
   &\phantom{=}& - \frac{1}{2\Delta p_k}
      \left[ \left( \dot\eta \frac{\partial p}{\partial\eta}
            \right)_{k+1/2} \left( U_{k+1} - U_k \right)
          + \left( \dot\eta \frac{\partial p}{\partial\eta}
            \right)_{k-1/2} \left( U_k - U_{k-1} \right)
      \right] \nonumber \\ &\phantom{=}& + \left( F_U \right)_k \ ,
   \end{aligned}
   

.. math::
   :label: 3.a.99

   \begin{aligned}
   \left( n_V \right)_k & = & - \left( \zeta_k + f \right) U_k
    - R{T_v}_k \left( \frac{1}{p} \frac{\partial p}{\partial\pi}
      \right)_k \pi \frac{\cos \phi}{a} \frac{\partial \Pi}{\partial\phi}
      \nonumber \\
   &\phantom{=}& - \frac{1}{2\Delta p_k}
      \left[ \left( \dot\eta \frac{\partial p}{\partial\eta}
           \right)_{k+1/2} \left( V_{k+1} - V_k \right)
         + \left( \dot\eta \frac{\partial p}{\partial\eta}
           \right)_{k-1/2} \left( V_k - V_{k-1} \right)
      \right]\nonumber \\ &\phantom{=}& + \left( F_V \right)_k \ ,
   \end{aligned}

.. math::
   :label: 3.a.100

   \begin{aligned}
   \Gamma_k
   & = & T^{\prime}_k \delta_k + \frac{R{T_v}_k}{(c_p^*)_k} \left(
    \frac{\omega}{p} \right)_k - Q \nonumber \\
   &\phantom{=}& - \frac{1}{2\Delta p_k}
      \left[ \left( \dot\eta \frac{\partial p}{\partial\eta}
           \right)_{k+1/2} \left( T_{k+1} - T_k \right)
         + \left( \dot\eta \frac{\partial p}{\partial\eta}
           \right)_{k-1/2} \left( T_k - T_{k-1} \right)
      \right] , 
   \end{aligned}

.. math::
   :label: 3.a.101

   E_k = \left(u_k \right)^2 + \left(v_k \right)^2 ,  

.. math::
   :label: 3.a.102

   \frac{R {T_v}_{k}}{(c^*_p)_k}
   = \frac{R}{c_p}
      \left( \frac{T^r_k + {T_v}_k^\prime} {1 + \left(
           \frac{c_{p_v}}{c_p}- 1 \right) q_k}
      \right) ,

.. math::
   :label: 3.a.103

   \left( \dot\eta \frac{\partial p}{\partial\eta} \right)_{k+1/2}
   = B_{k+1/2} \sum^K_{\ell=1}
         \left[ \delta_\ell \Delta p_\ell
            + {\boldsymbol{V}}_\ell \cdot \pi \nabla \Pi \Delta B_\ell
         \right] \nonumber \\
   \phantom{=} - \sum^k_{\ell=1}
         \left[ \delta_\ell \Delta p_\ell
            + {\boldsymbol{V}}_\ell \cdot \pi \nabla \Pi \Delta B_\ell
         \right] ,

.. math::
   :label: 3.a.104

   \left( \frac{\omega}{p} \right)_k
   = \left( \frac{1}{p} \frac{\partial p}{\partial\pi} \right)_k
            {\boldsymbol{V}}_k \cdot \pi \nabla\Pi
   - \sum^k_{\ell=1} C_{k\ell}
         \left[ \delta_\ell \Delta p_\ell
            + {\boldsymbol{V}}_\ell \cdot \pi \nabla \Pi \Delta B_\ell
         \right] ,

.. math::
   :label: 3.a.105

   C_{k\ell}
   = \left\{ \begin{array}{ll} \frac{1}{p_k},  \ell < k \\[6pt]
       \frac{1}{2 p_k},  \ell = k ,
       \end{array} \right.

.. math::
   :label: 3.a.106

   H_{k\ell} = C_{\ell k}\Delta p_\ell,

.. math::
   :label: 3.a.107

   \begin{aligned}
   D^r_{k\ell} & =& {\Delta p^r_\ell} \frac{R}{c_p } T^r_k C^r_{\ell k}
   + \frac{\Delta p^r_\ell}{2\Delta p^r_k}
          \left( T^r_k - T^r_{k-1} \right)
                \left(\epsilon_{k\ell+1}-B_{k-1/2}\right) \nonumber \\
   &\phantom{=}& + \frac{\Delta p^r_\ell}{2\Delta p^r_k}
          \left( T^r_{k+1} - T^r_k \right)
                \left(\epsilon_{k\ell}-B_{k+1/2}\right)
   ,
   \end{aligned}

.. math::
   :label: 3.a.108

   \begin{aligned}
   \frac{ \epsilon_{k\ell}}{R}
   = \left\{\begin{array}{ll} 1, & \ell \leq k \\
   	0, & \ell > k, \end{array} \right.  
   \end{aligned}

where notation such as :math:`\left( \underline{UT}^\prime \right)^n`
denotes a column vector with components :math:`\left( U_k T_k^\prime
\right)^n`. In order to complete the system, it remains to specify the
reference vector :math:`\underline{h}^r`, together with the term
:math:`(1/p\, \partial p/\partial\pi)`, which results from the pressure gradient
terms and also appears in the semi-implicit reference vector
:math:`\underline{b}^r`:

.. math::
   :label: 3.a.109

   \left( \frac{1}{p} \frac{\partial p}{\partial\pi} \right)_k
   =\left( \frac{1}{p} \right)_k \left( \frac{\partial p}{\partial\pi}
    \right)_k = \frac{B_k}{p_k}
   ,  

.. math::
   :label: 3.a.110

   \underline{b}^r = \underline{T}^r , 

.. math::
   :label: 3.a.111

   \underline{h}^r = 0 . 

The matrices :math:`{\boldsymbol{C}}^n` and
:math:`{\boldsymbol{H}}^n` ( with components :math:`C_{k\ell}` and
:math:`H_{k \ell}`) must be evaluated at each time step and each point
in the horizontal. It is more efficient computationally to substitute
the definitions of these matrices into :eq:`3.a.95`  and :eq:`3.a.104`  at the
cost of some loss of generality in the code. The finite difference
equations have been written in the form :eq:`3.a.94` -:eq:`3.a.111`  because
this form is quite general. For example, the equations solved by :cite:`simmons81a` 
at ECMWF can be obtained by changing only the
vectors and hydrostatic matrix defined by :eq:`3.a.108` -:eq:`3.a.111` .

Time filter
~~~~~~~~~~~

The time step is completed by applying a recursive time filter
originally designed by :cite:`robert66` and later studied by
:cite:`asselin72`.

.. math::

   \overline \psi^n = \psi^n + \alpha \left( \overline{\psi}^{n-1}
    - 2 \psi^n + \psi^{n+1} \right)

Spectral transform
~~~~~~~~~~~~~~~~~~

The spectral transform method is used in the horizontal exactly as in
CCM1. As shown earlier, the vertical and temporal aspects of the model
are represented by finite–difference approximations. The horizontal
aspects are treated by the spectral–transform method, which is described
in this section. Thus, at certain points in the integration, the
prognostic variables :math:`\left(\zeta + f \right),
\delta, T,` and :math:`\Pi` are represented in terms of coefficients of
a truncated series of spherical harmonic functions, while at other
points they are given by grid–point values on a corresponding Gaussian
grid. In general, physical parameterizations and nonlinear operations
are carried out in grid–point space. Horizontal derivatives and linear
operations are performed in spectral space. Externally, the model
appears to the user to be a grid–point model, as far as data required
and produced by it. Similarly, since all nonlinear parameterizations are
developed and carried out in grid–point space, the model also appears as
a grid–point model for the incorporation of physical parameterizations,
and the user need not be too concerned with the spectral aspects. For
users interested in diagnosing the balance of terms in the evolution
equations, however, the details are important and care must be taken to
understand which terms have been spectrally truncated and which have
not.  The algebra involved in the spectral transformations has been presented in several
publications :cite:`daley76,bourke77,machenhauer79`.  In this report,
we present only the details relevant to the model code; for more
details and general philosophy, the reader is referred to these
earlier papers.

Spectral algorithm overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The horizontal representation of an arbitrary variable :math:`\psi`
consists of a truncated series of spherical harmonic functions,

.. math::
   :label: 3.b.1

   \psi(\lambda, \mu) = \sum^M_{m=-M} \; \; \sum^{{\mathcal N} \left( m
   \right)}_{n=|m|} \psi^m_n P^m_n (\mu) e^{im \lambda} , 

where :math:`\mu = \sin \phi, \ M` is the highest Fourier wavenumber
included in the east–west representation, and :math:`{\mathcal N}\left( m
\right)` is the highest degree of the associated Legendre polynomials
for longitudinal wavenumber :math:`m`. The properties of the spherical
harmonic functions used in the representation can be found in the
review by :cite:`machenhauer79`. The model is coded for a general
pentagonal truncation, illustrated in Figure [figure:2], defined by
three parameters: :math:`M, K`, and :math:`N`, where :math:`M` is
defined above, :math:`K` is the highest degree of the associated
Legendre polynomials, and :math:`N` is the highest degree of the
Legendre polynomials for :math:`m= 0`. The common truncations are
subsets of this pentagonal case:

.. math::
   :label: 3.b.2

   \begin{aligned}
   \mathrm{Triangular:} \; &M = N = K , \nonumber \\ \mathrm{Rhomboidal:}
   \; &K = N + M ,  \\ \mathrm{Trapezoidal:} \; &N = K > M
   . \nonumber\end{aligned}

The quantity :math:`{\mathcal N} \left( m \right)` in :eq:`3.b.1` 
represents an arbitrary limit on the two-dimensional wavenumber
:math:`n`, and for the pentagonal truncation described above is
simply given by

  :math:`{\mathcal N} \left( m \right) = \min\left(N + \vert m \vert , K \right)`.

The associated Legendre polynomials used in the model are normalized
such that

.. math:: 
   :label: 3.b.3

   \int^1_{-1} \left[P^m_n(\mu)\right]^2 d\mu = 1 .  

With this normalization, the Coriolis parameter :math:`f` is

.. math:: 
   :label: 3.b.4

   f = \frac{\Omega}{\sqrt {0.375}} P^o_1 , 

which is required for the absolute vorticity.

The coefficients of the spectral representation :eq:`3.b.1`  are given by

.. math::
   :label: 3.b.5

   \psi^m_n = \int^1_{-1} \frac{1}{2 \pi} \int^{2 \pi}_0 \psi (\lambda,
   \mu) e^{-im\lambda} d \lambda P^m_n (\mu) d \mu . 

The inner integral represents a Fourier transform,

.. math::
   :label: 3.b.6

   \psi^m (\mu) = \frac{1}{2 \pi} \int^{2 \pi}_0 \psi (\lambda, \mu)
   e^{-im\lambda} d \lambda , 

which is performed by a Fast Fourier Transform (FFT) subroutine. The
outer integral is performed via Gaussian quadrature,

.. math::
   :label: 3.b.7

   \psi^m_n = \sum^J_{j=1} \psi^m (\mu_j) P^m_n (\mu_j) w_j ,
   

where :math:`\mu_j` denotes the Gaussian grid points in the meridional
direction, :math:`w_j` the Gaussian weight at point :math:`\mu_j`, and
:math:`J` the number of Gaussian grid points from pole to pole. The
Gaussian grid points (:math:`\mu_j`) are given by the roots of the
Legendre polynomial :math:`P_J(\mu)`, and the corresponding weights are
given by

.. math::
   :label: 3.b.8

   w_j = \frac{2(1 - \mu_j^2)}{\left[J\; P_{J-1} (\mu_j) \right]^2}
   . 

The weights themselves satisfy

.. math:: 
   :label: 3.b.9

   \sum^J_{j=1} w_j = 2.0 \ . 

The Gaussian grid used for the north–south transformation is generally
chosen to allow un-aliased computations of quadratic terms only. In this
case, the number of Gaussian latitudes :math:`J` must satisfy

.. math::
   :label: 3.b.10

   {2} J \geq (2N + K + M + 1)/2  \quad \hbox{for}\> M  \leq 2(K - N)\>,

.. math::
   :label: 3.b.11

   J \geq (3K + 1)/2  \quad \hbox{for}\> M & \geq 2(K - N)\> . 

For the common truncations, these become

.. math::
   :label: 3.b.12

   {2}
   J \geq (3K + 1)/2  \quad  \mathrm{for \; triangular \; and \;
   trapezoidal} ,  

.. math::
   :label: 3.b.13

   J \geq (3N + 2M + 1)/2  \quad
   \mathrm{for \; rhomboidal} . 

In order to allow exact Fourier transform of quadratic terms, the
number of points :math:`P` in the east–west direction must satisfy

.. math:: 
   :label: 3.b.14

   P \geq 3M + 1 \ . 

The actual values of :math:`J` and :math:`P` are often not set equal to
the lower limit in order to allow use of more efficient transform
programs.

Although in the next section of this model description, we continue to
indicate the Gaussian quadrature as a sum from pole to pole, the code
actually deals with the symmetric and antisymmetric components of
variables and accumulates the sums from equator to pole only. The model
requires an even number of latitudes to easily use the symmetry
conditions. This may be slightly inefficient for some spectral
resolutions. We define a new index, which goes from :math:`-I` at the
point next to the south pole to :math:`+I` at the point next to the
north pole and not including 0 (there are no points at the equator or
pole in the Gaussian grid), *i.e.,* let :math:`I = J/2` and
:math:`i = j - J/2` for :math:`j
\geq J/2+1` and :math:`i = j - J/2 - 1` for :math:`j \leq J/2`; then the
summation in :eq:`3.b.7`  can be rewritten as

.. math::
   :label: 3.b.15

   \psi^m_n = \sum \limits^{I}_{i = -I, \;i \neq 0} \psi^m (\mu_i) P^m_n
   (\mu_i) w_i .
   

The symmetric (even) and antisymmetric (odd) components of
:math:`\psi^m` are defined by

.. math::

   \left(\psi_E\right)^m_i = \frac{1}{2} \left( \psi^m_i + \psi^m_{-i}
   \right),

.. math::
   :label: 3.b.16

   \left(\psi_O\right)^m_i = \frac{1}{2} \left(\psi^m_i - \psi^m_{-i}
   \right) .
   

Since :math:`w_i` is symmetric about the equator, :eq:`3.b.15`  can be
rewritten to give formulas for the coefficients of even and odd
spherical harmonics:

.. math::
   :label: 3.b.17

   \psi^{m}_{n} =
   \begin{cases}
    \sum \limits ^I_{i=1} \left(\psi_E\right)^m_i(\mu_i) P^m_n(\mu_i)
    2w_i & \text{for $n-m$ even},\\ \sum \limits ^I_{i=1}
    \left(\psi_O\right)^m_i (\mu_i) P^m_n (\mu_i) 2w_i & \text{for $n-m$
    odd}.
   \end{cases}
   

The model uses the spectral transform method (\citep{machenhauer79}) for all
nonlinear terms. However, the model can be thought of as starting from
grid–point values at time :math:`t` (consistent with the spectral
representation) and producing a forecast of the grid–point values at
time :math:`t + \Delta t` (again, consistent with the spectral
resolution). The forecast procedure involves computation of the
nonlinear terms including physical parameterizations at grid points;
transformation via Gaussian quadrature of the nonlinear terms from
grid–point space to spectral space; computation of the spectral
coefficients of the prognostic variables at time :math:`t + \Delta t`
(with the implied spectral truncation to the model resolution); and
transformation back to grid–point space. The details of the equations
involved in the various transformations are given in the next section.

Combination of terms
~~~~~~~~~~~~~~~~~~~~

In order to describe the transformation to spectral space, for each
equation we first group together all undifferentiated explicit terms,
all explicit terms with longitudinal derivatives, and all explicit terms
with meridional derivatives appearing in the Dyn operator. Thus, the
vorticity equation :eq:`3.a.94`  is rewritten

.. math::
   :label: 3.b.18

   \underline{\left(\zeta + f \right)}^{n+1} = \underline{{\hbox{\sffamily\slshape V}}} +
   \frac{1} {a(1 - \mu^2)} \left[ \frac{\partial}{\partial \lambda}
   (\underline{{\hbox{\sffamily\slshape V}}}_\lambda) - (1 - \mu^2) \frac{\partial}{\partial
   \mu} (\underline{{\hbox{\sffamily\slshape V}}}_\mu) \right] , 

where the explicit forms of the vectors
:math:`\underline{{\hbox{\sffamily\slshape V}}},
\underline{{\hbox{\sffamily\slshape V}}}_\lambda,` and
:math:`\underline{{\hbox{\sffamily\slshape V}}}_\mu` are given as

.. math::
   :label: A.1

   \underline{{\hbox{\sffamily\slshape V}}} = \underline{(\zeta+f)}^{n-1} ,  

.. math::
   :label: A.2

   \underline{{\hbox{\sffamily\slshape V}}}_\lambda = 2 \Delta t\, \underline{n}^{n}_{V} , 

.. math::
   :label: A.3

   \underline{{\hbox{\sffamily\slshape V}}}_{\mu} = 2 \Delta t\,\underline{n}^{n}_{U}. 

The divergence equation :eq:`3.a.95`  is

.. math::
   :label: 3.b.19

   \begin{aligned}
   \underline{\delta}^{n+1} &=& \underline{{\hbox{\sffamily\slshape D}}} + \frac{1}{a(1 -
   \mu^2)} \left[ \frac{\partial}{\partial \lambda}
   (\underline{{\hbox{\sffamily\slshape D}}}_\lambda) + (1 - \mu^2) \frac{\partial}{\partial
   \mu} (\underline{{\hbox{\sffamily\slshape D}}}_\mu) \right] - \nabla^2
   \underline{{\hbox{\sffamily\slshape D}}}_\nabla \nonumber \\ &\phantom{=}& - \Delta t
   \nabla^2 (R {\boldsymbol{H}}^r \underline{T}^{\prime \, n+1} + R
   \left(\underline{b}^r + \underline{h}^r \right) \Pi^{n+1}) .
   \end{aligned}

The mean component of the temperature is not included in the
next–to–last term since the Laplacian of it is zero. The thermodynamic
equation :eq:`3.a.96`  is

.. math::
   :label: 3.b.20

   \underline{T}^{\prime \, n+1} = \underline{{\hbox{\sffamily\slshape T}}} - \frac{1}{a (1 -
   \mu^2)} \left[ \frac{\partial}{\partial \lambda}
   (\underline{{\hbox{\sffamily\slshape T}}}_\lambda) + (1
   - \mu^2) \frac{\partial}{\partial \mu} (\underline{{\hbox{\sffamily\slshape T}}}_\mu)
   - \right] -
   \Delta t {\boldsymbol{D}}^r \; \underline{\delta}^{n+1} . 

The surface–pressure tendency :eq:`3.a.97`  is

.. math::
   :label: 3.b.21

   \Pi^{n+1} = {{\hbox{\sffamily\slshape P}}{\hbox{\sffamily\slshape S}}} - \frac{\Delta t}{\pi^r} \left(
   \underline{\Delta p}^r \right)^T \underline{\delta}^{n+1}
   . 

The grouped explicit terms in :eq:`3.b.19` –:eq:`3.b.21`  are given as
follows. The terms of :eq:`3.b.19`  are

.. math::
   :label: A.4

   \underline{{\hbox{\sffamily\slshape D}}} = \underline{\delta}^{n-1} ,  

.. math::
   :label: A.5

   \underline{{\hbox{\sffamily\slshape D}}}_\lambda = 2 \Delta t \, \underline{n}^{n}_{U} , 

.. math::
   :label: A.6

   \underline{{\hbox{\sffamily\slshape D}}}_\mu = 2 \Delta t \, \underline{n}^{n}_{V} , 

.. math::
   :label: A.7

   \begin{aligned}
   \nonumber\lefteqn{\underline{{\hbox{\sffamily\slshape D}}}_\nabla = 2 \Delta t \left[ \underline{E}^n +
   \Phi_s \underline{1} + R {\boldsymbol{H}}^{r} \underline{{\mathcal T}}^{'n} \right]} \\
   & & \mbox{} + \Delta t \left[ R {\boldsymbol{H}}^{r} \left( {( \underline{T}^{'} )}^{n-1} 
   - 2 {(\underline{T}^\prime)}^n \right)
   + R \left( \underline{b}^{r} + \underline{h}^{r}
   \right) \left( {\Pi}^{n-1} - 2 {\Pi}^{n} \right) \right] \ . \end{aligned}

The terms of :eq:`3.b.20`  are

.. math::
   :label: A.8

   \underline{{\hbox{\sffamily\slshape T}}} = \left(\underline{T}'\right)^{n-1} + 2 \Delta t \,
   \underline{\Gamma}^{n} \, - \Delta t {\boldsymbol{D}}^{r}
   \left[\underline{\delta}^{n-1} - 2\underline{\delta}^{n} \right] \ ,

.. math::
   :label: A.9

   \underline{{\hbox{\sffamily\slshape T}}}_{\lambda} = 2 \Delta t \underline{\left(UT'\right)}^n , 

.. math::
   :label: A.10

   \underline{{\hbox{\sffamily\slshape T}}}_\mu = 2 \Delta t  \underline{\left(VT'\right)}^n . 

The nonlinear term in :eq:`3.b.21`  is

.. math::
   :label: A.11

   \begin{aligned}
   &\nonumber {{\hbox{\sffamily\slshape P}}{\hbox{\sffamily\slshape S}}} = \Pi^{n-1} - 2 \Delta t \frac{1}{\pi^n} \left[ \left(
   \underline{\delta}^n \right)^T \left( \underline{\Delta p}^n \right) +
   \left( \underline{\boldsymbol{V}}^n \right)^T \nabla \Pi^n \pi^n
   \underline{\Delta B} \right]& \\
   &\mbox{} - \Delta t \left[ \left(\underline{\Delta p}^r \right)^T \frac{1}{\pi^r}
   \right] \left[ \underline{\delta}^{n-1} -
   2 \underline{\delta}^n \right] \ .& 
   \end{aligned}

Transformation to spectral space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Formally, Equations :eq:`3.b.18` -:eq:`3.b.21`  are transformed to spectral
space by performing the operations indicated in :eq:`3.b.22`  to each term.
We see that the equations basically contain three types of terms, for
example, in the vorticity equation the undifferentiated term
:math:`\underline{{\hbox{\sffamily\slshape V}}}`, the longitudinally
differentiated term
:math:`\underline{{\hbox{\sffamily\slshape V}}}_\lambda`, and the
meridionally differentiated term
:math:`\underline{{\hbox{\sffamily\slshape V}}}_\mu`. All terms in the
original equations were grouped into one of these terms on the Gaussian
grid so that they could be transformed at once.

Transformation of the undifferentiated term is obtained by
straightforward application of :eq:`3.b.5` -:eq:`3.b.7` ,

.. math::
   :label: 3.b.22

   \left\{ \underline{{\hbox{\sffamily\slshape V}}} \right\}^m_n = \sum^J_{j=1}
   \underline{{\hbox{\sffamily\slshape V}}}^m(\mu_j) P^m_n(\mu_j) w_j , 

where :math:`\underline{{\hbox{\sffamily\slshape V}}}^m(\mu_j)` is the
Fourier coefficient of :math:`\underline{{\hbox{\sffamily\slshape V}}}`
with wavenumber :math:`m` at the Gaussian grid line :math:`\mu_j`. The
longitudinally differentiated term is handled by integration by parts,
using the cyclic boundary conditions,

.. math::
   :label: 3.b.23

   \begin{aligned}
   \left\{ \frac{\partial}{\partial \lambda}
   (\underline{{\hbox{\sffamily\slshape V}}}_\lambda) \right\}^m & = \frac{1}{2 \pi} \int
   ^{2\pi}_o \frac{\partial \underline{{\hbox{\sffamily\slshape V}}}_\lambda} {\partial
   \lambda} e^{-im\lambda} d \lambda ,\\ & = im \frac{1}{2 \pi} \int^{2
   \pi}_o \underline{{\hbox{\sffamily\slshape V}}}_\lambda e^{-im\lambda} d\lambda , \\
   \end{aligned}

so that the Fourier transform is performed first, then the
differentiation is carried out in spectral space. The transformation to
spherical harmonic space then follows :eq:`3.b.25` :

.. math::
   :label: 3.b.24

   \left \{ \frac{1}{a(1 - \mu^2)} \frac{\partial}{\partial \lambda}
   (\underline{{\hbox{\sffamily\slshape V}}}_\lambda) \right \}^m_n = im \sum^J_{j=1}
   \underline{{\hbox{\sffamily\slshape V}}}_\lambda^m (\mu_j) \frac{P^m_n(\mu_j)}{a(1 -
   \mu^2_j)} w_j , 

where
:math:`\underline{{\hbox{\sffamily\slshape V}}}_\lambda^m (\mu_j)` is
the Fourier coefficient of
:math:`\underline{{\hbox{\sffamily\slshape V}}}_\lambda` with wavenumber
:math:`m` at the Gaussian grid line :math:`\mu_j`.

The latitudinally differentiated term is handled by integration by parts
using zero boundary conditions at the poles:

.. math::
   :label: 3.b.25

   \begin{aligned}
   \left \{ \frac{1}{a(1 - \mu^2)} (1 - \mu^2) \frac{\partial}{\partial
   \mu} (\underline{{\hbox{\sffamily\slshape V}}}_\mu) \right \}^m_n & = \int^1_{-1}
   \frac{1}{a(1 - \mu^2)} (1 - \mu^2) \frac{\partial} {\partial \mu}
   (\underline{{\hbox{\sffamily\slshape V}}}_\mu)^m P^m_n d\mu ,\\ & = - \int^1_{-1}
   \frac{1}{a(1 - \mu^2)} (\underline{{\hbox{\sffamily\slshape V}}}_\mu)^m (1 - \mu^2)
   \frac{dP^m_n}{d\mu} d\mu .
      \end{aligned}

Defining the derivative of the associated Legendre polynomial by

.. math:: H^m_n = (1 - \mu^2) \frac{dP^m_n}{d\mu} , 
	  :label: 3.b.26

:eq:`3.b.28`  can be written

.. math::
   :label: 3.b.27

   \left \{ \frac{1}{a(1 - \mu^2)} (1 - \mu^2) \frac{\partial}{\partial
   \mu} (\underline{{\hbox{\sffamily\slshape V}}}_\mu) \right \}^m_n = - \sum^J_{j=1}
   (\underline{{\hbox{\sffamily\slshape V}}}_\mu)^m \frac{H^m_n(\mu_j)}{a(1 - \mu^2_j)} w_j
   . 

Similarly, the :math:`\nabla^2` operator in the divergence equation can
be converted to spectral space by sequential integration by parts and
then application of the relationship

.. math::
   :label: 3.b.28

   \nabla^2 P^m_n( \mu) e^{im \lambda} = \frac{-n (n+1)}{a^2} P^m_n(\mu)
   e^{im \lambda}, 

to each spherical harmonic function individually so that

.. math::
   :label: 3.b.29

   \left \{ \nabla^2 \underline{{\hbox{\sffamily\slshape D}}}_\nabla \right \}^m_n =
   \frac{-n(n+1)} {a^2} \sum^J_{j=1} \underline{{\hbox{\sffamily\slshape D}}}_\nabla^m
   (\mu_j) P^m_n(\mu_j) w_j ,
   

where :math:`\underline{{\hbox{\sffamily\slshape D}}}_\nabla^m (\mu)`
is the Fourier coefficient of the original grid variable
:math:`\underline{{\hbox{\sffamily\slshape D}}}_\nabla`.

Solution of semi-implicit equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The prognostic equations can be converted to spectral form by summation
over the Gaussian grid using :eq:`3.b.22` , :eq:`3.b.24` , and :eq:`3.b.27` . The
resulting equation for absolute vorticity is

.. math::
   :label: 3.b.30

   \underline{\left(\zeta + f \right)}^m_n = \underline
   {{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}_n^m ,

where :math:`\underline{\left(\zeta + f \right)}_n^m` denotes a
spherical harmonic coefficient of
:math:`\underline{\left(\zeta + f \right)}^{n+1}`, and the form of
:math:`\underline{{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}_n^m`,
as a summation over the Gaussian grid, is given as

.. math::
   :label: A.12

   \underline{{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}^m_n = \sum^J_{j=1} \left [ \underline {{\hbox{\sffamily\slshape V}}}^m(\mu_j) P^m_n 
   (\mu_j) + im \underline{{\hbox{\sffamily\slshape V}}}^m_\lambda (\mu_j) \frac{P^m_n (\mu_j)}{a(1 - 
   \mu^2_j)} + \underline{{\hbox{\sffamily\slshape V}}}^m_\mu (\mu_j) \frac{H^m_n (\mu_j)}{a(1 - \mu^2_j)}  
   \right] w_j . 

The spectral form of the divergence equation :eq:`3.b.19`  becomes

.. math::
   :label: 3.b.31

   \underline{\delta}^m_n = \underline{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}^m_n + \Delta t
   \frac{n(n+1)} {a^2} \left[ R {\boldsymbol{H}}^r \underline{T}^{\prime \,
   m}_n + R \left( \underline{b}^r + \underline{h}^r \right) \Pi^m_n
   \right] ,
   

where :math:`\underline{\delta}^m_n, \;\underline{T}'^m_n, \;` and
:math:`\Pi^m_n` are spectral coefficients of
:math:`\underline{\delta}^{n+1}, \;
\underline{T}^{\prime \, n+1}`, and :math:`\Pi^{n+1}`. The Laplacian of
the total temperature in :eq:`3.b.19`  is replaced by the equivalent
Laplacian of the perturbation temperature in :eq:`3.b.31` .
:math:`\underline{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}^m_n`
is given by

.. math::
   :label: A.13

   \begin{aligned}
   \nonumber\underline{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}^m_n = \sum^J_{j=1} \Biggl \{ \left[ \underline {{\hbox{\sffamily\slshape D}}}^m 
   (\mu_j) + \frac{n(n+1)}{a^2} \underline {{\hbox{\sffamily\slshape D}}}^m_\nabla (\mu_j) \right] 
   P^m_n (\mu_j) \\
   + im \underline {{\hbox{\sffamily\slshape D}}}^m_\lambda (\mu_j) \frac{P^m_n (\mu_j)} 
   {a(1 - \mu_j^2)} - \underline {{\hbox{\sffamily\slshape D}}}^m_\mu (\mu_j) \frac{H^m_n (\mu_j)} 
   {a(1 - \mu^2_j)} \Biggr \} w_j . \end{aligned}

The spectral thermodynamic equation is

.. math::
   :label: 3.b.32

   \underline{T}'^m_n = \underline{{\hbox{\sffamily\slshape T}}{\hbox{\sffamily\slshape S}}}^m_n - \Delta t
   {\boldsymbol{D}}^r \underline{\delta}^m_n , 

with
:math:`\underline{{\hbox{\sffamily\slshape T}}{\hbox{\sffamily\slshape S}}}^m_n`
defined as

.. math::
   :label: A.14

   \underline{{\hbox{\sffamily\slshape T}}{\hbox{\sffamily\slshape S}}}^m_n = \sum^J_{j=1} \left[ \underline{{\hbox{\sffamily\slshape T}}}^m (\mu_j) P^m_n
   (\mu_j) - im \underline{{\hbox{\sffamily\slshape T}}}^m_\lambda (\mu_j) \frac{P^m_n (\mu_j)}{a (1 
   - \mu^2_j)} + \underline{{\hbox{\sffamily\slshape T}}}^m_\mu (\mu_j) \frac{H^m_n (\mu_j)}{a (1 -
   \mu^2_j)} \right ] w_j , 

while the surface pressure equation is

.. math::
   :label: 3.b.33

   \Pi^m_n = {{\hbox{\sffamily\slshape P}}{\hbox{\sffamily\slshape S}}}^m_n - \underline{\delta}^m_n
   \left(\underline{\Delta p}^r \right)^T \frac{\Delta t}{\pi^r} ,
   

where
:math:`{{\hbox{\sffamily\slshape P}}{\hbox{\sffamily\slshape S}}}^m_n`
is given by

.. math:: {{\hbox{\sffamily\slshape P}}{\hbox{\sffamily\slshape S}}}^m_n = \sum^J_{j=1} {{\hbox{\sffamily\slshape P}}{\hbox{\sffamily\slshape S}}}^m (\mu_j) P^m_n (\mu_j) w_j . 
	  :label: A.15

Equation :eq:`3.b.30`  for vorticity is explicit and complete at this
point. However, the remaining equations :eq:`3.b.31` –:eq:`3.b.33`  are
coupled. They are solved by eliminating all variables except
:math:`\underline{\delta}^m_n`:

.. math::
   :label: 3.b.34

   {\boldsymbol{A}}_n \underline{\delta}^m_n =
   \underline{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}^m_n + \Delta t \frac{n(n+1)}{a^2} \left[
   R {\boldsymbol{H}}^r (\underline{{\hbox{\sffamily\slshape T}}{\hbox{\sffamily\slshape S}}})^m_n + R \left(
   \underline{b}^r + \underline{h}^r \right) ({{\hbox{\sffamily\slshape P}}{\hbox{\sffamily\slshape S}}})^m_n
   \right ] , 

.. math::
   :label: 3.b.35

   [-1.0em] \intertext{where}\nonumber\\[-2.0em] {\boldsymbol{A}}_n = {\boldsymbol{I}}
   + \Delta t^2 \frac{n(n+1)}{a^2} \left [ R {\boldsymbol{H}}^r
   {\boldsymbol{D}}^r + R \left( \underline{b}^r + \underline{h}^r \right)
   \left( \left( \underline{\Delta p^r} \right)^T \, \frac{1}{\pi^r}
   \right) \right ] , 

which is simply a set of :math:`K` simultaneous equations for the
coefficients with given wavenumbers (:math:`m,n`) at each level and is
solved by inverting :math:`{\boldsymbol{A}}_n`. In order to prevent
the accumulation of round–off error in the global mean divergence (which
if exactly zero initially, should remain exactly zero)
:math:`\left({\boldsymbol{A}}_o\right)^{-1}` is set to the null matrix
rather than the identity, and the formal application of :eq:`3.b.34`  then
always guarantees :math:`\underline{\delta}^o_o = 0`. Once
:math:`\delta^m_n` is known, :math:`\underline{T}'^m_n` and
:math:`\Pi^m_n` can be computed from :eq:`3.b.32`  and :eq:`3.b.33` ,
respectively, and all prognostic variables are known at time
:math:`n\!+\!1` as spherical harmonic coefficients. Note that the mean
component :math:`\underline{T}'^o_o` is not necessarily zero since the
perturbations are taken with respect to a specified
:math:`\underline{T}^r`.

Horizontal diffusion
~~~~~~~~~~~~~~~~~~~~

As mentioned earlier, the horizontal diffusion in :eq:`3.a.87`  and
:eq:`3.a.90`  is computed implicitly via time splitting after the
transformations into spectral space and solution of the semi-implicit
equations. In the following, the :math:`\zeta` and :math:`\delta`
equations have a similar form, so we write only the :math:`\delta`
equation:

.. math::
   :label: 3.b.36

   \begin{aligned}
   \left(\delta^*\right)^m_n & = \left(\delta^{n+1}\right)^m_n - \left(
   -1
   \right)^i 2 \Delta t K^{(2i)} \left[ \nabla^{2i}
   	\left(\delta^*\right)^m_n - \left( - 1 \right)^i
   	\left(\delta^*\right)^m_n \left(2/a^2 \right)^i \right] ,
       \\
   \end{aligned}

.. math::
   :label: 3.b.37

   \left(T^*\right)^m_n & = \left(T^{n+1}\right)^m_n - \left( -1\right)^i
   2 \Delta t K^{(2i)} \left[ \nabla^{2i} \left(T^*\right)^m_n \right] \
   .

The extra term is present in :eq:`3.b.36` , :eq:`3.b.40`  and :eq:`3.b.42`  to
prevent damping of uniform rotations. The solutions are just

.. math::
   :label: 3.b.38

   \left(\delta^*\right)^m_n  = K^{(2i)}_n \left(\delta\right)
   \left(\delta^{n+1}\right)^m_n ,  

.. math::
   :label: 3.b.39

   \left(T^*\right)^m_n
   = K^{(2i)}_n \left(T \right) \left(T^{n+1}\right)^m_n ,

.. math::
   :label: 3.b.40

   K^{(2)}_n \left(\delta \right) = \left\{ 1 + 2
   \Delta t D_n K^{(2)} \left[ \left( \frac{n(n + 1)}{a^2} \right) -
   \frac{2}{a^2} \right] \right\}^{-1} \ , 

.. math::
   :label: 3.b.41

   K^{(2)}_n
   \left( T \right) = \left\{ 1 + 2\Delta t D_n K^{(2)} \left(
   \frac{n(n + 1)}{a^2} \right) \right\}^{-1} \ , 

.. math::
   :label: 3.b.42

   K^{(4)}_n \left(\delta\right) = \left\{ 1 + 2 \Delta t D_n K^{(4)}
   	\left[ \left( \frac{n(n+1)}{a^2} \right)^2 - \frac{4}{a^4}
   	\right] \right\}^{-1} , 

.. math::
   :label: 3.b.43

   K^{(4)}_n \left(T \right) = \left\{ 1 + 2 \Delta t D_n K^{(4)} \left(
   	\frac{n(n+1)}{a^2} \right)^2 \right\}^{-1} . 

:math:`K^{(2)}_n \left(\delta \right)` and
:math:`K^{(4)}_n \left(\delta \right)` are both set to 1 for :math:`n` = 0. 
The quantity :math:`D_n` represents the “Courant number limiter”,
normally set to 1. However, :math:`D_n` is modified to ensure that the
CFL criterion is not violated in selected upper levels of the model. If
the maximum wind speed in any of these upper levels is sufficiently
large, then :math:`D_n = 1000` in that level for all :math:`n > n_c`,
where :math:`n_c = a \Delta t \big/ \max \vert {\boldsymbol{V}} \vert`. This condition is applied whenever the wind
speed is large enough that :math:`n_c < K`, the truncation parameter in
:eq:`3.b.2` , and temporarily reduces the effective resolution of the model
in the affected levels. The number of levels at which this “Courant
number limiter” may be applied is user-selectable, but it is only used
in the top level of the 26 level |cam| control runs.

The diffusion of :math:`T` is not complete at this stage. In order to
make the partial correction from :math:`\eta` to :math:`p` in :eq:`3.a.81` 
local, it is not included until grid–point values are available. This
requires that :math:`\nabla^4 \Pi` also be transformed from spectral to
grid–point space. The values of the coefficients :math:`K^{(2)}` and
:math:`K^{(4)}` for the standard T42 resolution are
:math:`2.5 \times 10^5`\ m\ :math:`^2`\ sec\ :math:`^{-1}` and
:math:`1.0 \times 10^{16}`\ m\ :math:`^4`\ sec\ :math:`^{-1}`, respectively.

Initial divergence damping
~~~~~~~~~~~~~~~~~~~~~~~~~~

Occasionally, with poorly balanced initial conditions, the model
exhibits numerical instability during the beginning of an integration
because of excessive noise in the solution. Therefore, an optional
divergence damping is included in the model to be applied over the first
few days. The damping has an initial e-folding time of :math:`\Delta t`
and linearly decreases to 0 over a specified number of days,
:math:`t_D`, usually set to be 2. The damping is computed implicitly via
time splitting after the horizontal diffusion.

.. math::
   :label: 3.b.44

   r = \max \left[ \frac{1}{\Delta t} (t_D - t) / t_D , ~ 0 \right]

.. math::
   :label: 3.b.45

   \left(\delta^*\right)^m_n = \frac{1}{1 + 2\Delta t r} \left(\delta^*\right)^m_n

Transformation from spectral to physical space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After the prognostic variables are completed at time :math:`n+1` in
spectral space :math:`\left(\underline{(\zeta + f)^*}\right)^m_n`,
:math:`\left(\underline{\delta^*}\right)^m_n`,
:math:`\left(\underline{T^*}\right)^m_n`,
:math:`\left(\Pi^{n+1}\right)^m_n` they are transformed to grid space.
For a variable :math:`\psi`, the transformation is given by

.. math::
   :label: 3.b.46

   \psi( \lambda, \mu) = \sum^M_{m=-M} \left [ \sum^{{\mathcal N}(m)}_{n=|m|}
   \psi^m_n P^m_n (\mu) \right ] e^{im\lambda} . 

The inner sum is done essentially as a vector product over :math:`n`,
and the outer is again performed by an FFT subroutine. The term needed
for the remainder of the diffusion terms, :math:`\nabla^4 \Pi`, is
calculated from

.. math::
   :label: 3.b.47

   \nabla^4 \Pi^{n+1} = \sum^M_{m=-M} \left [\sum^{{\mathcal N}(m)}_{n=|m|}
   \left( \frac{n(n+1)}{a^2} \right )^2 \left(\Pi^{n+1} \right)^m_n P^m_n
   (\mu) \right ] e^{im\lambda} . 

In addition, the derivatives of :math:`\Pi` are needed on the grid for
the terms involving :math:`\nabla \Pi` and
:math:`{\boldsymbol{V}} \cdot \nabla \Pi`,

.. math::
   :label: 3.b.48

   {\boldsymbol{V}} \cdot \nabla \Pi = \frac{U}{a(1 - \mu^2)} \frac{\partial
   \Pi} {\partial \lambda} + \frac{V}{a(1 - \mu^2)} (1 - \mu^2)
   \frac{\partial \Pi}{\partial \mu}. 

These required derivatives are given by

.. math::
   :label: 3.b.49

   \frac{\partial \Pi}{\partial \lambda} = \sum^M_{m=-M} im \left[
   \sum^{{\mathcal N}(m)}_{n=\vert m \vert} \Pi^m_n P^m_n (\mu) \right]
   e^{im\lambda} ,  

.. math::
   :label: 3.b.50

   \intertext{and using (\ref{3.b.26}),
   }\nonumber\\[-2.0em] (1 - \mu^2) \frac{\partial \Pi}{\partial \mu} =
   \sum^M_{m=-M} \left [ \sum^{{\mathcal N}(m)}_{n=\vert m \vert} \Pi^m_n
   H^m_n (\mu) \right ] e^{im \lambda} , 

which involve basically the same operations as :eq:`3.b.47` . The other
variables needed on the grid are :math:`U` and :math:`V`. These can be
computed directly from the absolute vorticity and divergence
coefficients using the relations

.. math::
   :label: 3.b.51

   \left(\zeta + f \right)^m_n = - \frac{n(n+1)}{a^2} \psi^m_n + f^m_n,

.. math::
   :label: 3.b.52

   \delta^m_n = - \frac{n(n+1)}{a^2} \chi^m_n , 

in which the only nonzero :math:`f^m_n` is
:math:`f^o_1 = \Omega/ \sqrt{.375},` and

.. math::
   :label: 3.b.53

   \begin{aligned}
   U & = \frac{1}{a} \frac{\partial \chi}{\partial \lambda} - \frac{(1 -
   \mu^2)}{a} \frac{\partial \psi}{\partial \mu} ,  \\ V &
   = \frac{1}{a} \frac{\partial \psi}{\partial \lambda} + \frac{(1 -
   \mu^2)} {a} \frac{\partial \chi}{\partial \mu} . \end{aligned}

Thus, the direct transformation is

.. math::
   :label: 3.b.55

   \begin{aligned}
   U &=& - \sum^M_{m=-M} a \sum^{{\mathcal N}(m)}_{n=|m|} \left [ \frac{im}
   {n(n+1)} \delta^m_n P^m_n (\mu) - \frac{1}{n(n+1)} (\zeta + f)^m_n
   H^m_n (\mu) \right] e^{im \lambda} \nonumber \\ &\phantom{=}& -
   \>\frac{a}{2} \frac{\Omega}{\sqrt{0.375}} H^o_1 ,  
   \end{aligned}

.. math::
   :label: 3.b.56

   V = - \sum^M_{m=-M} a \sum^{{\mathcal N}(m)}_{n=|m|} \bigg
   [\frac{im}{n(n+1)} (\zeta + f)^m_n P^m_n (\mu) + \frac{1}{n(n+1)}
   \delta^m_n H^m_n (\mu) \bigg ] e^{im\lambda}.  

The horizontal diffusion tendencies are also transformed back to grid
space. The spectral coefficients for the horizontal diffusion tendencies
follow from :eq:`3.b.36`  and :eq:`3.b.37` :

.. math::
   :label: 3.b.57

   F_{T_H}\left(T^*\right)^m_n  = \left(-1\right)^{i+1} K^{2i} \left[
   	\nabla^{2i} \left(T^*\right) \right]^m_n ,  

.. math::
   :label: 3.b.58

   F_{\zeta_H} \left(\left(\zeta + f \right)^* \right)^m_n  =
   \left(-1\right)^{i+1} K^{2i} \left \{\nabla^{2i} \left(\zeta +
   f\right)^* - \left(-1\right)^i \left(\zeta + f \right)^* \left(2/a^2
   \right)^i \right \} , 

.. math::
   :label: 3.b.59

   F_{\delta_H}
   \left(\delta^*\right)^m_n  = \left(-1\right) K^{2i} \left\{
   \nabla^{2i} \left(\delta ^*\right) - \left(-1\right)^i \delta^*
   \left(2/a^2 \right)^i \right\}, 

using :math:`i = 1` or 2 as appropriate for the :math:`\nabla^2` or
:math:`\nabla^4` forms. These coefficients are transformed to grid space
following :eq:`3.b.1`  for the :math:`T` term and :eq:`3.b.55`  and :eq:`3.b.56` 
for vorticity and divergence. Thus, the vorticity and divergence
diffusion tendencies are converted to equivalent :math:`U` and :math:`V`
diffusion tendencies.

Horizontal diffusion correction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After grid–point values are calculated, frictional heating rates are
determined from the momentum diffusion tendencies and are added to the
temperature, and the partial correction of the :math:`\nabla^4`
diffusion from :math:`\eta` to :math:`p` surfaces is applied to
:math:`T`. The frictional heating rate is calculated from the kinetic
energy tendency produced by the momentum diffusion

.. math::
   :label: 3.b.60

   F_{F_H} = -u^{n-1} F_{u_H} (u^*)/c_p^* -v^{n-1} F_{v_H} (v^*)/c^*_p ,
   

where :math:`F_{u_H}`, and :math:`F_{v_H}` are the momentum equivalent
diffusion tendencies, determined from :math:`F_{\zeta_H}` and
:math:`F_{\delta_H}` just as :math:`U` and :math:`V` are determined from
:math:`\zeta` and :math:`\delta`, and

.. math::
   :label: 3.b.61

   c^*_p = c_p \left[ 1 + \left(\frac{c_{p_v}}{c_p} -1 \right) q^{n+1}
   \right ] . 

These heating rates are then combined with the correction,

.. math::
   :label: 3.b.62

   \hat {T}^{n+1}_k = T^*_k + \left( 2 \Delta t F_{F_H}\right)_k + 2
   \Delta t \left( \pi B \frac{\partial T^*}{\partial p} \right)_k
   K^{(4)} \nabla^4 \Pi^{n+1} .  

The vertical derivatives of :math:`T^*` (where the :math:`^*` notation
is dropped for convenience) are defined by

.. math::
   :label: 3.b.63

   \begin{aligned}
   \left( \pi B \frac{\partial T}{\partial p} \right)_1 & = \frac{\pi}
   	{2\Delta p_1} \left[ B_{1+\frac{1}{2}} \left( T_2 - T_1
   	\right) \right] \ , \\
   \left(\pi B \frac{\partial T}{\partial p} \right)_k & = \frac{\pi}
   	{2\Delta p_k} \left[ B_{k + \frac{1}{2}} \left( T_{k+1} - T_k
   	\right) + B_{k - \frac{1}{2}} \left( T_k - T_{k-1} \right)
   	\right] \ , \\
   \left(\pi B \frac{\partial T}{\partial p} \right)_K & = \frac{\pi}
   	{2\Delta p_K} \left[ B_{K - \frac{1}{2}} \left( T_K - T_{K-1}
   	\right) \right] .  \end{aligned}

The corrections are added to the diffusion tendencies calculated earlier
:eq:`3.b.57`  to give the total temperature tendency for diagnostic
purposes:

.. math::
   :label: 3.b.64

   \hat{F}_{T_H}(T^*)_k = F_{T_H}(T^*)_k + \left( 2 \Delta t F_{F_H}
   \right)_k + 2 \Delta t B_k \left(\pi \frac{\partial T^*}{\partial p}
   \right)_k K^{(4)} \nabla^4 \Pi^{n+1} . 

Semi-Lagrangian Tracer Transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The forecast equation for water vapor specific humidity and constituent
mixing ratio in the :math:`\eta` system is from :eq:`3.a.36`  excluding
sources and sinks.

.. math::
   :label: 3.c.1

   \frac{dq}{dt} = \frac{\partial q}{\partial t} + {\boldsymbol{V}} \cdot
   	\nabla q + \dot\eta \, \frac{\partial p}{\partial \eta} \,
   	\frac{\partial q} {\partial p} = 0  \\[-1.0em]
   \intertext{or}\nonumber\\

.. math::
   :label: 3.c.2

   [-2.0em] \frac{dq}{dt} = \frac{\partial
   q}{\partial t} + {\boldsymbol{V}} \cdot \nabla q + \dot\eta \,
   \frac{\partial q}{\partial \eta} = 0 . 

Equation :eq:`3.c.2`  is more economical for the semi-Lagrangian vertical
advection, as :math:`\Delta \eta` does not vary in the horizontal, while
:math:`\Delta p` does. Written in this form, the :math:`\eta` advection
equations look exactly like the :math:`\sigma` equations.

The parameterizations are time-split in the moisture equation. The
tendency sources have already been added to the time level
:math:`\left( n -
1 \right)`. The semi-Lagrangian advection step is subdivided into
horizontal and vertical advection sub-steps, which, in an Eulerian form,
would be written

.. math::
   :label: 3.c.3

   q^* = q^{n-1} + 2\Delta t \left( {\boldsymbol{V}} \cdot \nabla q
   \right)^n
    \\[-1.0em]
   \intertext{and}\nonumber\\

.. math::
   :label: 3.c.4

   [-2.0em] q^{n+1} = q^* + 2\Delta t \left(
   \dot\eta \frac{\partial q}{\partial n} \right)^n . 

In the semi-Lagrangian form used here, the general form is

.. math::
   :label: 3.c.5

   q^*  = {\rm L}_{\lambda \varphi} \left( q^{n-1} \right) ,

.. math::
   :label: 3.c.6

   q^{n+1}  = {\rm L}_\eta \left( q^* \right) .

Equation :eq:`3.c.5`  represents the horizontal interpolation of
:math:`q^{n-1}` at the departure point calculated assuming
:math:`\dot\eta = 0`. Equation :eq:`3.c.6`  represents the vertical
interpolation of :math:`q^*` at the departure point, assuming
:math:`{\boldsymbol{V}} = 0`.

The horizontal departure points are found by first iterating for the
mid-point of the trajectory, using winds at time :math:`n`, and a first
guess as the location of the mid-point of the previous time step

.. math::
   :label: 3.c.7

   \lambda^{k+1}_M  = \lambda_A - \Delta t u^n \left( \lambda^k_M,
   	\varphi^k_M \right) \big/a \cos \varphi^k_M ,  

.. math::
   :label: 3.c.8

   \varphi^{k+1}_M  = \varphi_A - \Delta t v^n \left( \lambda^k_M,
   \varphi^k_M \right)/a , 

where subscript :math:`A` denotes the arrival (Gaussian grid) point and
subscript :math:`M` the midpoint of the trajectory. The velocity
components at :math:`\left( \lambda_M^k, \varphi^k_M \right)` are
determined by Lagrange cubic interpolation. For economic reasons, the
equivalent Hermite cubic interpolant with cubic derivative estimates is
used at some places in this code. The equations will be presented later.

Once the iteration of :eq:`3.c.7`  and :eq:`3.c.8`  is complete, the departure
point is given by

.. math::
   :label: 3.c.9

   \lambda_D  = \lambda_A - 2 \Delta t u^n \left( \lambda_M, \varphi_M
   	\right) \big/a \cos \varphi_M ,  \\

.. math::
   :label: 3.c.10
   
   \varphi_D  = \lambda_A - 2 \Delta t v^n \left( \lambda_M, \varphi_M
   	\right)/a , 

where the subscript :math:`D` denotes the departure point.

The form given by :eq:`3.c.7` -:eq:`3.c.10`  is inaccurate near the poles and
thus is only used for arrival points equatorward of 70\ :math:`^\circ`
latitude. Poleward of 70\ :math:`^\circ` we transform to a local
geodesic coordinate for the calculation at each arrival point. The local
geodesic coordinate is essentially a rotated spherical coordinate system
whose equator goes through the arrival point. Details are provided in
:cite:`williamson89`. The transformed system is rotated about the
axis through :math:`\left( \lambda_A - \frac{\pi}{2}, 0
\right)` and :math:`\left( \lambda_A + \frac{\pi}{2}, 0 \right)`, by an
angle :math:`\varphi_A` so the equator goes through
:math:`\left( \lambda_A,
\varphi_A \right)`. The longitude of the transformed system is chosen to
be zero at the arrival point. If the local geodesic system is denoted by
:math:`\left( \lambda^\prime, \varphi^\prime \right)`, with velocities
:math:`\left( u^\prime, v^\prime \right)`, the two systems are related
by

.. math::
   :label: 3.c.11

   \sin \phi^\prime  = \sin \phi \cos \phi_A - \cos \phi \sin \phi_A
   	\cos \left( \lambda_A - \lambda \right) ,  

.. math::
   :label: 3.c.12

   \sin \phi  =  \sin \phi^\prime \cos \phi_A + \cos \phi^\prime \sin
   \prime_A \cos \lambda^\prime \ , 

.. math::
   :label: 3.c.13

   \sin \lambda^\prime
   \cos \phi^\prime  =  -\sin \left( \lambda_A
   -\lambda \right) \cos \phi \ , 

.. math::
   :label: 3.c.14

   \begin{aligned}
   v^\prime \cos \phi^\prime & = & v \left[ \cos \phi \cos \phi_A + \sin
   \phi \sin \phi_A \cos \left( \lambda_A - \lambda \right) \right]
   \nonumber \\ &\phantom{=}& - u \sin \phi_A \sin \left( \lambda_A -
   \lambda \right), 
   \end{aligned}

.. math::
   :label: 3.c.15

   u^\prime \cos \lambda^\prime -
   v^\prime \sin \lambda^\prime \sin \phi^\prime  =  u \cos \left(
   \lambda_A - \lambda \right) + v \sin \phi \sin \left( \lambda_A -
   \lambda \right) \ . 

The calculation of the departure point in the local geodesic system is
identical to :eq:`3.c.7` -:eq:`3.c.10`  with all variables carrying a prime.
The equations can be simplified by noting that 
:math:`\left( \lambda^\prime_A, \varphi_A^\prime \right) = \left( 0, 0 \right)` by
design and 

.. math::

   u^\prime \left( \lambda^\prime_A, \varphi_A^\prime \right)
   = u\left( \lambda_A, \varphi_A \right) 

and 

.. math::

   v^\prime \left(
   \lambda^\prime_A, \varphi_A^\prime \right) = v\left( \lambda_A,
   \varphi_A \right). 

The interpolations are always done in global spherical coordinates.

The interpolants are most easily defined on the interval 0 :math:`\leq \theta \leq 1`. Define

.. math::
   :label: 3.c.16

   \theta = \left( x_D - x_i \right) \big/ \left( x_{i+1} - x_i \right),

where :math:`x` is either :math:`\lambda` or :math:`\varphi` and the
departure point :math:`x_D` falls within the interval
:math:`\left( x_i, x_{i+1} \right)`. Following (23) of (:cite:`rasch90`) 
with :math:`r_i=3` the Hermite cubic interpolant is
given by

.. math::
   :label: 3.c.17

   \begin{aligned}
   q_D & = & q_{i+1} \left[ 3-2\theta \right]\theta^2
    - d_{i+1} \left[ h_i \theta^2 \left( 1-\theta \right) \right]
      \nonumber \\
   &\phantom{=}& + q_i \left[ 3-2\left(1-\theta\right) \right]
                                   \left(1-\theta \right)^2
    + d_i \left[ h_i \theta \left( 1-\theta \right)^2 \right]
   \end{aligned}

where :math:`q_i` is the value at the grid point :math:`x_i`,
:math:`d_i` is the derivative estimate given below, and
:math:`h_i = x_{i+1} - x_i`.

Following (3.2.12) and (3.2.13) of :cite:`hildebrand56`, the Lagrangian
cubic polynomial interpolant used for the velocity interpolation, is
given by

.. math::
   :label: 3.c.18

   f_{D\phantom{\dot D}} = \sum^2_{j=-1} \ell_j \left( x_D \right)
   f_{i+j}
          

where

.. math::
   :label: 3.c.19

   \ell_j \left( x_D \right) =
          \frac{ \left( x_D - x_{i-1} \right) \ldots \left( x_D -
              x_{i+j-1} \right) \left( x_D - x_{i+j+1} \right) \ldots
              \left( x_D - x_{i+2} \right) }
            { \left( x_{i+j} - x_{i-1} \right) \ldots \left( x_{i+j} -
              x_{i+j-1} \right) \left( x_{i+j} - x_{i+j+1} \right) \ldots
              \left( x_{i+j} - x_{i+2} \right) } 

where :math:`f` can represent either :math:`u` or :math:`v`, or their
counterparts in the geodesic coordinate system.

The derivative approximations used in :eq:`3.c.17`  for :math:`q` are
obtained by differentiating :eq:`3.c.18`  with respect to :math:`x_D`,
replacing :math:`f` by :math:`q` and evaluating the result at
:math:`x_D` equal :math:`x_{i}` and :math:`x_{i+1}`. With these
derivative estimates, the Hermite cubic interpolant :eq:`3.c.17`  is
equivalent to the Lagrangian :eq:`3.c.18` . If we denote the four point
stencil :math:`\left(
x_{i-1},x_{i},x_{i+1},x_{i+2} \right)` by :math:`\left( x_1,x_2,x_3,x_4,
\right)` the cubic derivative estimates are

.. math::
   :label: 3.c.20

   \begin{aligned}
   d_2 & = \left[ \frac{(x_2 - x_3)( x_2 - x_4 )} {(x_1 - x_2)(x_1 -
                      x_3)(x_1 - x_4)} \right] q_1 \\
       & - \left[ \frac{1}{(x_1 - x_2)} - \frac{1}{(x_2 - x_3)}
               - \frac{1}{(x_2 - x_4)} \right] q_2 \\
       & + \left[ \frac{(x_2 - x_1)(x_2 - x_4)} {(x_1 - x_3)(x_2 -
                       x_3)(x_3 - x_4)}\right] q_3 \\
       & - \left[ \frac{(x_2 - x_1)(x_2 - x_3)} {(x_1 - x_4)(x_2 -
                       x_4)(x_3 - x_4)} \right] q_4
   \end{aligned}
   
.. math::
   :label: 3.c.21

   \begin{aligned}
   [-1.0em]
   \intertext{and}\nonumber\\[-2.0em]
   d_3 & = \left[ \frac{(x_3 - x_2)(x_3 - x_4)} {(x_1 - x_2)(x_1 -
                       x_3)(x_1 - x_4)} \right] q_1 \\
       & - \left[ \frac{(x_3 - x_1)(x_3 - x_4)} {(x_1 - x_2)(x_2 -
                       x_3)(x_2 - x_4)} \right] q_2 \\
       & - \left[ \frac{1}{(x_1 - x_3)} + \frac{1}{(x_2 - x_3)} -
               \frac{1}{(x_3 - x_4)} \right] q_3 \\
       & - \left[ \frac{(x_3 - x_1)(x_3 - x_2)} {(x_1 - x_4)(x_2 -
                       x_4)(x_3 - x_4)} \right] q_4
   \end{aligned}

The two dimensional :math:`\left( \lambda, \varphi \right)` interpolant
is obtained as a tensor product application of the one-dimensional
interpolants, with :math:`\lambda` interpolations done first. Assume the
departure point falls in the grid box :math:`(\lambda_i,\lambda_{i+1})`
and :math:`(\varphi_i,\varphi_{i+1})`. Four :math:`\lambda`
interpolations are performed to find :math:`q` values at
:math:`(\lambda_D,\varphi_{j-1})`, :math:`(\lambda_D,\varphi_j)`,
:math:`(\lambda_D,\varphi_{j+1})`, and :math:`(\lambda_D,
\varphi_{j+2})`. This is followed by one interpolation in
:math:`\varphi` using these four values to obtain the value at
:math:`(\lambda_D,
\varphi_D)`. Cyclic continuity is used in longitude. In latitude, the
grid is extended to include a pole point (row) and one row across the
pole. The pole row is set equal to the average of the row next to the
pole for :math:`q` and to wavenumber 1 components for :math:`u` and
:math:`v`. The row across the pole is filled with the values from the
first row below the pole shifted :math:`\pi` in longitude for :math:`q`
and minus the value shifted by :math:`\pi` in longitude for :math:`u`
and :math:`v`.

Once the departure point is known, the constituent value of :math:`q^* = q^{n-1}_D` 
is obtained as indicated in :eq:`3.c.5`  by Hermite cubic
interpolation :eq:`3.c.17` , with cubic derivative estimates :eq:`3.c.18`  and
:eq:`3.c.19`  modified to satisfy the Sufficient Condition for Monotonicity
with C\ :math:`^\circ` continuity (SCMO) described below. Define
:math:`\Delta_i q` by

.. math:: 
   :label: 3.c.28
   
   \Delta_i q = \frac{q_{i+1} - q_i}{x_{i+1} - x_i} \ . 

First, if :math:`\Delta_i q= 0` then

.. math:: 
   :label: 3.c.29

   d_i = d_{i+1} = 0 \ . 

Then, if either

.. math:: 
   :label: 3.c.30
		  
   0 \leq \frac{d_i}{\Delta_i q} \leq 3 

or

.. math:: 
   :label: 3.c.31

   0 \leq \frac{d_{i+1}}{\Delta_i q} \leq 3 

is violated, :math:`d_i` or :math:`d_{i+1}` is brought to the
appropriate bound of the relationship. These conditions ensure that the
Hermite cubic interpolant is monotonic in the interval
:math:`\left[ x_i, x_{i+1} \right]`.

The horizontal semi-Lagrangian sub-step :eq:`3.c.5`  is followed by the
vertical step :eq:`3.c.6` . The vertical velocity :math:`\dot \eta` is
obtained from that diagnosed in the dynamical calculations :eq:`3.a.93`  by

.. math::
   :label: 3.c.32

   \left( \dot\eta \right)_{k+\frac{1}{2}} = \left( \dot\eta \,
   \frac{\partial p}{\partial \eta} \right)_{k+\frac{1}{2}} \Bigg/
   \left(\frac{p_{k+1}
   -p_k}{\eta_{k+1} - \eta_k} \right) , 

with :math:`\eta_k= A_k + B_k`. Note, this is the only place that the
model actually requires an explicit specification of :math:`\eta`. The
mid-point of the vertical trajectory is found by iteration

.. math::
   :label: 3.c.33

   \eta^{k+1}_M = \eta_A - \Delta t \dot\eta^n \left( \eta^k_M \right) .
   
Note, the arrival point :math:`\eta_A` is a mid-level point where
:math:`q` is carried, while the :math:`\dot\eta` used for the
interpolation to mid-points is at interfaces. We restrict :math:`\eta_M`
by

.. math:: 
   :label: 3.c.34

   \eta_1 \leq \eta_M \leq \eta_K , 

which is equivalent to assuming that :math:`q` is constant from the
surface to the first model level and above the top :math:`q` level. Once
the mid-point is determined, the departure point is calculated from

.. math::
   :label: 3.c.35

   \eta_D = \eta_A - 2 \Delta t \dot\eta^n \left( \eta_M \right) , 

with the restriction

.. math:: 
   :label: 3.c.36

   \eta_1 \leq \eta_D \leq \eta_K . 

The appropriate values of :math:`\dot\eta` and :math:`q` are determined
by interpolation :eq:`3.c.17` , with the derivative estimates given by
:eq:`3.c.18`  and :eq:`3.c.19`  for :math:`i = 2` to :math:`K - 1`. At the top
and bottom we assume a zero derivative (which is consistent with
:eq:`3.c.34`  and :eq:`3.c.36` ), :math:`d_i = 0` for the interval
:math:`k=1`, and :math:`\delta_{i+1} = 0` for the interval
:math:`k = K - 1`. The estimate at the interior end of the first and
last grid intervals is determined from an uncentered cubic
approximation; that is :math:`d_{i+1}` at the :math:`k=1` interval is
equal to :math:`d_i` from the :math:`k=2` interval, and :math:`d_i` at
the :math:`k=K-1` interval is equal to :math:`d_{i+1}` at the
:math:`k = K -2` interval. The monotonic conditions :eq:`3.c.30`  to
:eq:`3.c.31`  are applied to the :math:`q` derivative estimates.

Mass fixers
~~~~~~~~~~~

This section describes original and modified fixers used for the
Eulerian and semi-Lagrangian dynamical cores.

Let :math:`\pi^0`, :math:`\Delta p^0` and :math:`q^0` denote the values
of air mass, pressure intervals, and water vapor specific humidity at
the beginning of the time step (which are the same as the values at the
end of the previous time step.)

:math:`\pi^+`, :math:`\Delta p^+` and :math:`q^+` are the values after
fixers are applied at the end of the time step.

:math:`\pi^-`, :math:`\Delta p^-` and :math:`q^-` are the values after
the parameterizations have updated the moisture field and tracers.

Since the physics parameterizations do not change the surface pressure,
:math:`\pi^-` and :math:`\Delta p^-` are also the values at the
beginning of the time step.

The fixers which ensure conservation are applied to the dry atmospheric
mass, water vapor specific humidity and constituent mixing ratios. For
water vapor and atmospheric mass the desired discrete relations,
following :cite:`williamson94a` are

.. math::
   :label: 3.d.1

   \int\limits_2 \, \pi^+ - \int\limits_3 \, q^+ \Delta p^+ =
   {\boldsymbol{P}} ,   

.. math::
   :label: 3.d.2

   \int\limits_3 \, q^+ \Delta p^+ =
   \int\limits_3 \, q^- \Delta p^- ,

where :math:`\boldsymbol{P}` is the dry mass of the atmosphere. From
the definition of the vertical coordinate,

.. math:: \Delta p = p_0 \Delta A + \pi \Delta B, 
	  :label: 3.d.3

and the integral :math:`\int\limits_2` denotes the normal Gaussian
quadrature while :math:`\int\limits_3` includes a vertical sum followed
by Gaussian quadrature. The actual fixers are chosen to have the form

.. math::
   :label: 3.d.4

   \pi^+ \left( \lambda, \varphi \right) = {\boldsymbol{M}} \hat \pi^+
   \left( \lambda, \varphi \right) , 

preserving the horizontal gradient of :math:`\Pi`, which was calculated
earlier during the inverse spectral transform, and

.. math::
   :label: 3.d.5

   q^+ \left( \lambda, \varphi, \eta \right) = \hat q^+ + \alpha\eta \hat
   q^+ \vert \hat q^+ - q^- \vert . 

In :eq:`3.d.4`  and :eq:`3.d.5`  the :math:`\hat{\left(\hskip 10pt \right)}` 
denotes the provisional value before adjustment. The form
:eq:`3.d.5`  forces the arbitrary corrections to be small when the mixing
ratio is small and when the change made to the mixing ratio by the
advection is small. In addition, the :math:`\eta` factor is included to
make the changes approximately proportional to mass per unit volume
(:cite:`rasch95`). Satisfying :eq:`3.d.1`  and :eq:`3.d.2` 
gives

.. math::
   :label: 3.d.6

   \alpha = \frac{\int\limits_3 \, q^- \Delta p^- - \int\limits_3 \, \hat
   q^+ p_0\Delta A - M\int\limits_3\hat q^+ \hat\pi^+ \Delta B}
   {\int\limits_3 \eta \hat q^+ \vert \hat q^+ - q^- \vert \, p_0\Delta A
   + M \int\limits_3\eta\hat q^+ \vert \hat q^+ - q^- \vert \hat\pi^+
   \Delta B} 

and

.. math::
   :label: 3.d.7

   {\boldsymbol{M}} = \left({\boldsymbol{P}} + \int\limits_3 \, q^- \Delta p^-
   \right) \Bigg/ \int\limits_2 \, \hat \pi^+ \ . 

Note that water vapor and dry mass are corrected simultaneously.
Additional advected constituents are treated as mixing ratios normalized
by the mass of dry air. This choice was made so that as the water vapor
of a parcel changed, the constituent mixing ratios would not change.
Thus the fixers which ensure conservation involve the dry mass of the
atmosphere rather than the moist mass as in the case of the specific
humidity above. Let :math:`\chi` denote the mixing ratio of
constituents. Historically we have used the following relationship for
conservation:

.. math::
   :label: 3.d.8

   \int\limits_3\chi^+ (1-q^+) \Delta p^+ = \int\limits_3 \chi^-
   (1-q^-)\Delta p^- \ .
   
The term :math:`(1-q)\Delta p` defines the dry air mass in a layer.
Following :cite:`rasch95` the change made by the
fixer has the same form as :eq:`3.d.5` 

.. math::
   :label: 3.d.9

   \chi^+ \left( \lambda, \varphi, \eta \right) = \hat \chi^+ +
   \alpha_\chi \eta \hat \chi^+ \vert \hat \chi^+ - \chi^- \vert
   \ .

Substituting :eq:`3.d.9`  into :eq:`3.d.8`  and using :eq:`3.d.4`  through
:eq:`3.d.7`  gives

.. math::
   :label: 3.d.10

   \alpha_\chi = \frac{ \int\limits_3 \chi^- (1-q^-) \Delta p^- -
   		\int\limits_{A,B}\hat\chi^+ (1-\hat q^+)\Delta\hat p^+
   		+ \alpha\int\limits_{A,B}\hat\chi^+ \eta \hat q^+
   			\vert\hat q^+ - q^-\vert\Delta p}
   		{\int\limits_{A,B} \eta\hat\chi^+ \vert\hat\chi^+ -
   			\chi^-\vert(1-\hat q^+)\Delta p
   		- \alpha \int\limits_{A,B}\eta\hat\chi^+
   		\vert\hat\chi^+ - \chi^-\vert \eta\hat q^+ \vert \hat
   		q^+ - q^-\vert\Delta p}
    \ ,

where the following shorthand notation is adopted:

.. math::
   :label: 3.d.11

   \int\limits_{A,B} (~~)\Delta p = \int\limits_3 (~~) p_0 \Delta A +
   M\int\limits_3 (~~) p_s \Delta B
    \ .

We note that there is a small error in :eq:`3.d.8` . Consider a situation
in which moisture is transported by a physical parameterization, but
there is no source or sink of moisture. Under this circumstance
:math:`q^- \ne q^0`, but the surface pressure is not allowed to change.
Since :math:`(1- q^-)\Delta p^- \ne
(1-q^0)\Delta p^0`, there is an implied change of dry mass of dry air in
the layer, and even in circumstances where there is no change of dry
mixing ratio :math:`\chi` there would be an implied change in mass of
the tracer. The solution to this inconsistency is to define a dry air
mass *only once* within the model time step, and use it consistently
throughout the model. In this revision, we have chosen to fix the dry
air mass in the model time step where the surface pressure is updated,
e.g. at the end of the model time step. Therefore, we now replace
:eq:`3.d.8`  with

.. math::
   :label: 3.d.8a

   \int\limits_3\chi^+ (1-q^+) \Delta p^+ = \int\limits_3 \chi^-
   (1-q^0)\Delta p^0
    \ .

There is a corresponding change in the first term of the numerator of
:eq:`3.d.10`  in which :math:`q^-` is replace by :math:`q^0`. |cam| uses
:eq:`3.d.10`  for water substances and constituents affecting the
temperature field to prevent changes to the IPCC simulations. In the
future, constituent fields may use a *corrected* version of :eq:`3.d.10` .

.. _energyfixer:

Energy Fixer
~~~~~~~~~~~~

Following notation in section [massfixers], the total energy integrals
are

.. math::

   \begin{aligned}
   &\int\limits_3 {1 \over g} \left[ c_p T^+ + \Phi_s + {1 \over 2}
     \left( {u^+}^2 + {v^+}^2 \right) \right] \Delta p^+
   = {\boldsymbol{E}} \\
    {\boldsymbol{E}} = &\int\limits_3 {1 \over g} \left[ c_p T^- + \Phi_s +
        {1 \over 2} \left( {u^-}^2 + {v^-}^2 \right) \right] \Delta p^-
   + {\boldsymbol{S}}\end{aligned}

.. math::

   {\boldsymbol{S}} = \int\limits_2 \left[ \left( FSNT - FLNT \right)
     -        \left( FSNS - FLNS - SHFLX - \rho_{H_2O} L_v PRECT \right)
     -        \right] \Delta t

.. math::

   \begin{aligned}
   {\boldsymbol{S}} &=&\int\limits_2 \left[ \left( FSNT - FLNT \right)
     -        \left( FSNS - FLNS - SHFLX \right)
              \right] \Delta t \\
                 &+&\int\limits_2 \left[\rho_{H_2O} L_v \left( PRECL + PRECC \right)
                                + \rho_{H_2O} L_i \left( PRESL + PRESC \right)
                      \right] \Delta t\end{aligned}

where :math:`{\boldsymbol{S}}` is the net source of energy from the
parameterizations. :math:`FSNT` is the net downward solar flux at the
model top, :math:`FLNT` is the net upward longwave flux at the model
top, :math:`FSNS` is the net downward solar flux at the surface,
:math:`FLNS` is the net upward longwave flux at the surface,
:math:`SHFLX` is the surface sensible heat flux, and :math:`PRECT` is
the total precipitation during the time step. From equation :eq:`3.d.4` 

.. math::

   \pi^+ \left( \lambda, \varphi \right) = {\boldsymbol{M}} \hat \pi^+
   \left( \lambda, \varphi \right)

and from :eq:`3.d.3` 

.. math:: \Delta p = p_0 \Delta A + \pi \Delta B

The energy fixer is chosen to have the form

.. math::

   \begin{aligned}
   T^+ \left( \lambda, \varphi, \eta \right) &=& \hat T^+ + \beta \\ 
   u^+ \left( \lambda, \varphi, \eta \right) &=& \hat u^+ \\ 
   v^+ \left( \lambda, \varphi, \eta \right) &=& \hat v^+\end{aligned}

Then

.. math::

   \beta = { g{\boldsymbol{E}}
    - \int\limits_3 \,
    \left[ c_p \hat T^+ + \Phi_s + {1 \over 2} \left( {\hat u}^{+^2} +
     {\hat v}^{+^2} \right) \right]
    p_0\Delta A - {\boldsymbol{M}}\int\limits_3
    \left[ c_p \hat T^+ + \Phi_s + {1 \over 2} \left( {\hat u}^{+^2} +
     {\hat v}^{+^2} \right) \right]
    \hat\pi^+ \Delta B
   \over \int\limits_3 c_p \, p_0\Delta A + {\boldsymbol{M}} \int\limits_3 c_p \hat\pi^+ \Delta B }

.. _statcalc:

Statistics Calculations
~~~~~~~~~~~~~~~~~~~~~~~

At each time step, selected global average statistics are computed for
diagnostic purposes when the model is integrated with the Eulerian and
semi-Lagrangian dynamical cores. Let :math:`\int_3` denote a global and
vertical average and :math:`\int_2` a horizontal global average. For an
arbitrary variable :math:`\psi`, these are defined by

.. math::
   :label: 8.a.1

   \int_3 \psi d V = \sum^K_{k=1} \sum^J_{j=1} \sum^I_{i=1} 
   \psi_{ijk} w_j \left(\frac{\Delta p_k}{\pi} \right) \bigg/ 2I , 

.. math::
   :label: 8.a.2

   *[-1.0em]
   \intertext{and}\nonumber\\*[-2.0em]
   \int_2 \psi dA = \sum^J_{j=1} \sum^I_{i=1} \psi_{ijk} w_j/2I , 

where recall that

.. math:: 
   :label: 8.a.3

   \sum^J_{j=1} w_j = 2 . 

The quantities monitored are:

.. math::
   :label: 8.a.4

   \begin{aligned}
   \text{global rms} \; (\zeta+f) (\mathrm{s}^{-1}) & = \left[ \int_3
   (\zeta^n + f)^2 dV \right]^{1/2} ,  \\
   \text{global rms} \; \delta (\mathrm{s}^{-1}) & = \left [\int_3 (\delta^n)^2 dV
   \right]^{1/2} ,  \\
   \text{global rms} \; T \; (\mathrm{K}) \; & = \left[ \int_3 (T^r + T'^n)^2 dV
   \right]^{1/2} , \\
   \text{global average mass times} \; g \; (\mathrm{Pa}) & = \int_2
   \pi^{n} dA , \\
   \text{global average mass of moisture} \; (\mathrm{kg \; m}^{-2}) 
   & = \int_3 \pi^{n} q^{n}/g dV . \end{aligned}

Reduced grid
~~~~~~~~~~~~

The Eulerian core and semi-Lagrangian tracer transport can be run on
reduced grids. The term reduced grid generally refers to a grid based on
latitude and longitude circles in which the longitudinal grid increment
increases at latitudes approaching the poles so that the longitudinal
distance between grid points is reasonably constant. Details are
provided in (:cite:`williamson00`). This option provides a
saving of computer time of up to 25%.

.. _sec-semi-lagrange:

Semi-Lagrangian Dynamical Core
------------------------------

Introduction
~~~~~~~~~~~~

The two-time-level semi-implicit semi-Lagrangian spectral transform
dynamical core in |cam| evolved from the three-time-level CCM2 semi-Lagrangian
version detailed in :cite:`williamson94a` hereafter
referred to as W&O94. As a first approximation, to convert from a
three-time-level scheme to a two-time-level scheme, the time level index
n-1 becomes n, the time level index n becomes n+\ :math:`\frac{1}{ 2}`,
and :math:`2\Delta t` becomes :math:`\Delta t`. Terms needed at
n+\ :math:`\frac{1}{ 2}` are extrapolated in time using time n and n-1
terms, except the Coriolis term which is implicit as the average of time
n and n+1. This leads to a more complex semi-implicit equation to solve.
Additional changes have been made in the scheme to incorporate advances
in semi-Lagrangian methods developed since W&O94. In the following,
reference is made to changes from the scheme developed in W&O94. The
reader is referred to that paper for additional details of the
derivation of basic aspects of the semi-Lagrangian approximations. Only
the details of the two-time-level approximations are provided here.

Vertical coordinate and hydrostatic equation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The semi-Lagrangian dynamical core adopts the same hybrid vertical
coordinate (:math:`\eta`) as the Eulerian core defined by

.. math:: 
   :label: sld.1

   p(\eta, p_s) = A (\eta)p_o + B(\eta) p_s \; , 

where :math:`p` is pressure, :math:`p_s` is surface pressure, and
:math:`p_o` is a specified constant reference pressure. The coefficients
:math:`A` and :math:`B` specify the actual coordinate used. As mentioned
by :cite:`simmons81b` and implemented by :cite:`simmons81a`
and :cite:`simmons83`, the coefficients :math:`A` and
:math:`B` are defined only at the discrete model levels. This has
implications in the continuity equation development which follows.

In the :math:`\eta` system the hydrostatic equation is approximated in a
general way by

.. math:: 
   :label: sld.2

   \Phi_k = \Phi_s + R \sum^K_{l=k} H_{kl}\, (p)\, T_{vl} 

where k is the vertical grid index running from 1 at the top of the
model to :math:`K` at the first model level above the surface,
:math:`\Phi_k` is the geopotential at level :math:`k`, :math:`\Phi_s` is
the surface geopotential, :math:`T_v` is the virtual temperature, and R
is the gas constant. The matrix :math:`H`, referred to as the
hydrostatic matrix, represents the discrete approximation to the
hydrostatic integral and is left unspecified for now. It depends on
pressure, which varies from horizontal point to point.

Semi-implicit reference state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The semi-implicit equations are linearized about a reference state with
constant :math:`T^r` and :math:`p_s^r`. We choose

.. math:: T^r = 350 {\rm K},~~~~~ p_s^r = 10^5 {\rm Pa}

Perturbation surface pressure prognostic variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To ameliorate the mountain resonance problem, :cite:`ritchie_tanguay96` 
introduce a perturbation :math:`{\rm ln}\,p_{s}` surface pressure
prognostic variable

.. math::

   \begin{aligned}
   {\rm ln}\,p'_{s} &=& {\rm ln}\,p_{s} - {\rm ln}\,p_{s}^* \\ {\rm
   ln}\,p_{s}^* &=& - \frac{\Phi_s}{R T^r}\end{aligned}

The perturbation surface pressure, :math:`{\rm ln}\,p'_{s}`, is never
actually used as a grid point variable in the |cam| code. It is only used for
the semi-implicit development and solution. The total :math:`{\rm
ln}\,p_{s}` is reclaimed in spectral space from the spectral
coefficients of :math:`\Phi_s` immediately after the semi-implicit
equations are solved, and transformed back to spectral space along with
its derivatives. This is in part because
:math:`\nabla ^4{\rm ln}\,p_{s}` is needed for the horizontal diffusion
correction to pressure surfaces. However the semi-Lagrangian |cam| default is
to run with no horizontal diffusion.

Extrapolated variables
~~~~~~~~~~~~~~~~~~~~~~

Variables needed at time (:math:`n+\frac{1}{2}`) are obtained by
extrapolation

.. math::

   \left(~~~\right)^{n+\frac{1}{2}} = \frac{3}{2} \left(~~~\right)^{n}
                      - \frac{1}{2} \left(~~~\right)^{n-1}

Interpolants
~~~~~~~~~~~~

Lagrangian polynomial quasi-cubic interpolation is used in the
prognostic equations for the dynamical core. Monotonic Hermite
quasi-cubic interpolation is used for tracers. Details are provided in
the Eulerian Dynamical Core description. The trajectory calculation uses
tri-linear interpolation of the wind field.

Continuity Equation
~~~~~~~~~~~~~~~~~~~

The discrete semi-Lagrangian, semi-implicit continuity equation is
obtained from (16) of W&O94 modified to be spatially uncentered by a
fraction :math:`\epsilon`, and to predict :math:`{\rm ln}\,p_{s}'`

.. math::

   \begin{aligned}
   \Delta B_{_{l}} &\left\{ \left({\rm
             ln}\,p_{s{_{l}}}'\right)^{n+1}_{_{A}}
     - \left[ \left({\rm ln}\,p_{s{_{l}}} \right)^{n}
            + { \Phi_s \over RT^r } \right] _{D_{2}} \right\} \, \Bigg/
                    \, \Delta t = \nonumber \\
   	& - {1\over 2} \bigg\lbrace \left[ \left(1 + \epsilon \right)
                    \Delta \left({1 \over p_s}
   	\dot\eta {\partial p \over
         \partial\eta}\right)_l\right]^{n+1}_A + \left[ \left(1 -
         \epsilon \right)\Delta \left({1 \over p_s}
   	\dot\eta {\partial p \over
   	\partial\eta}\right)_l\right]^{n}_{D_{2}}\bigg\rbrace \\
   &-\left({1 \over p_s} \delta_{_{l}} \Delta p_{_{l}} \right)^{n+{1\over
   	2}}_{M_{2}} 
    +{\Delta B_{_{l}} \over RT^r} \left( {\boldsymbol{V}}_{_{l}} \cdot
         \nabla \;\Phi_s \right)^{n+{1\over 2}}_{M_2} \nonumber\\
   &-\bigg\lbrace{1 \over 2}
         \left[ \left(1 + \epsilon \right) \left({1 \over p^r_s}
                \delta_{_{l}} \Delta p_{_{l}}^r
   	\right)^{n+1}_A
       + \left(1 - \epsilon \right) \left({1 \over p^r_s} \delta_{_{l}}
                \Delta p_{_{l}}^r
   	\right)^{n}_{D_{2}}\right]
       - \left({1 \over p^r_s} \delta_{_{l}} \Delta p_{_{l}}^r
   	\right)^{n+{1\over 2}}_{M_{2}}\bigg\rbrace \nonumber\end{aligned}

where

.. math::
   :label: sld.3

   \begin{aligned}
   \Delta (~~~~)_l \,&=\, (~~~~)_{l+ {1 \over 2}} -\, (~~~~)_{l - {1
   \over 2}}\\[-1.0em]
   \intertext{and}\nonumber\\[-2.0em]
    \left(~~~~ \right)^{n+{1\over 2}}_{M_{2}} &=
   	 {1\over 2} \left[ \left(1 + \epsilon \right)\left(~~~~
                          \right)^{n+{1\over 2}}_{A}
                      + \left(1 - \epsilon \right)\left(~~~~
                        \right)^{n+{1\over 2}}_{D_{2}} \right]
   \end{aligned}

:math:`\Delta (~~~~)_l` denotes a vertical difference, :math:`l`
denotes the vertical level, :math:`A` denotes the arrival point,
:math:`D_2` the departure point from horizontal (two-dimensional)
advection, and :math:`M_2` the midpoint of that trajectory.

The surface pressure forecast equation is obtained by summing over all
levels and is related to (18) of W&O94 but is spatially uncentered and
uses :math:`{\rm ln}\,p_{s}'`

.. math::

   \begin{aligned}
    \left({\rm ln}\,p'_s \right)^{n+1}_{_{A}} & =& \sum^K_{l=1} \Delta
   	B_l
   	\left[ \left({\rm ln}\,p_{s{_{l}}} \right)^{n} + { \Phi_s
          \over RT^r } \right] _{D_{2}}
   	 - {1 \over 2} \Delta t \sum^K_{l=1}\left[ \left(1 - \epsilon
               \right)\Delta \left({1 \over p_s}
   	\dot\eta {\partial p \over
   	\partial\eta}\right)_l\right]^{n}_{D_{2}} \nonumber \\
   &\phantom{=}& - \Delta t \sum^K_{l=1}\left({1 \over p_s} \delta_l
   	\Delta p_{_{l}} \right)^{n+{1\over 2}}_{M_{2}}
   + \Delta t \sum^K_{l=1} {\Delta B_{_{l}} \over RT^r} \left(
         {\boldsymbol{V}}_{_{l}} \cdot \nabla \;\Phi_s \right)^{n+{1\over
         2}}_{M_2} \\
       &\phantom{=}&- \Delta t \sum^K_{l=1} {1 \over p^r_s}
   	\bigg\lbrace{1 \over 2}
   	\left[ \left(1 + \epsilon \right)
                   \left(\delta_l\right)^{n+1}_{_{A}}
               + \left(1 - \epsilon \right)
                   \left(\delta_l\right)^{n}_{_{D_{2}}}
   	\right]
                  - \left(\delta_l\right)^{n+{1\over 2}}_{_{M_{2}}}
             \bigg\rbrace \Delta p^r_{_{l}} \nonumber\end{aligned}

The corresponding :math:`\left({1 \over p_s} \dot\eta {\partial p \over
\partial \eta}\right)` equation for the semi-implicit development
follows and is related to (19) of W&O94, again spatially uncentered and
using :math:`{ln}\,p_{s}'`.

.. math::

   \begin{aligned}
   \left(1 + \epsilon \right) \left({1 \over p_s} \dot\eta {\partial p
   \over \partial
   \eta}\right)^{n+1}_{k+{1 \over 2}} = &- {2 \over \Delta t}
   	\bigg\lbrace B_{k+ {1\over 2}} \left({\rm ln}\; p'_s
   	\right)^{n+1}_{_A} -
   	\sum^k_{l=1} \Delta B_l \left[ \left({\rm ln}\; p_{s_l}
              \right)^{n} + { \Phi_s \over RT^r } \right] _{D_2}
              \bigg\rbrace \nonumber \\
            &- \sum^k_{l=1}\left[ \left(1 - \epsilon \right)\Delta
               \left({1 \over p_s}
           \dot\eta {\partial p \over \partial\eta}\right)_l
                 \right]^{n}_{D_{2}}\\
   &- 2 \sum^k_{l=1} \left({1 \over p_s} \delta_l \Delta p_l
   	\right)^{n+{1\over 2}}_{M_2}
   + 2 \sum^k_{l=1}{\Delta B_{_{l}} \over RT^r} \left(
         {\boldsymbol{V}}_{_{l}} \cdot \nabla \;\Phi_s \right)^{n+{1\over
         2}}_{M_2} \nonumber \\
       &- 2 \sum^k_{l=1} {1 \over p^r_s} \bigg\lbrace{1 \over 2}
           \left[ \left(1 + \epsilon \right)
                   \left(\delta_l\right)^{n+1}_{_{A}}
               + \left(1 - \epsilon \right)
                   \left(\delta_l\right)^{n}_{_{D_{2}}}
           \right]
                   - \left(\delta_l\right)^{n+{1\over 2}}_{_{M_{2}}}
             \bigg\rbrace \Delta p^r_{_{l}} \nonumber\end{aligned}

This is not the actual equation used to determine
:math:`\left({1 \over p_s}
\dot\eta {\partial p \over \partial \eta}\right)` in the code. The
equation actually used in the code to calculate
:math:`\left({1 \over p_s}
\dot\eta {\partial p \over \partial \eta}\right)` involves only the
divergence at time (:math:`n+1`) with
:math:`\left({\rm ln}\; p'_s \right)^{n+1}` eliminated.

.. math::

   \begin{aligned}
   \left(1 + \epsilon \right) &\left({1 \over p_s} \dot\eta {\partial p
   \over \partial
   \eta}\right)^{n+1}_{k+{1 \over 2}} = \nonumber \\
     {2 \over \Delta t}
       &\left[ \sum^k_{l=1} ~-~ B_{k+{1\over 2}}\sum^K_{l=1}\right]
              \Delta B_l \left[ \left({\rm ln}\; p_{s_l} \right)^{n} + {
              \Phi_s \over RT^r } \right] _{D_2} \nonumber \\
    - &\left[ \sum^k_{l=1} ~-~ B_{k+{1\over 2}}\sum^K_{l=1}\right]
           \left[ \left(1 - \epsilon \right) \Delta \left({1 \over p_s}
              \dot\eta {\partial p \over \partial
   	\eta}\right)_l\right]^{n}_{D_2} \nonumber \\
    - 2 &\left[ \sum^k_{l=1} ~-~ B_{k+{1\over 2}}\sum^K_{l=1}\right]
           \left({1
   	\over p_s} \delta_l \Delta p_l \right)^{n+{1\over 2}}_{M_2} \\
    + 2 &\left[ \sum^k_{l=1} ~-~ B_{k+{1\over 2}}\sum^K_{l=1}\right]
         {\Delta B_{_{l}} \over RT^r} \left( {\boldsymbol{V}}_{_{l}} \cdot
         \nabla \;\Phi_s \right)^{n+{1\over 2}}_{M_2} \nonumber \\
    - 2 &\left[ \sum^k_{l=1} ~-~ B_{k+{1\over 2}}\sum^K_{l=1}\right]
          {1 \over p_s^r}\bigg\lbrace {1 \over 2}
             \left[ \left(1 + \epsilon \right)
                \left(\delta_l\right)^{n+1}_{_A}
              + \left(1 - \epsilon \right) \left(\delta_l
             \right)^{n}_{_{D_2}} \right]
                                    - \left(\delta_l \right)^{n+{1\over
   	2}}_{_{M_2}} \bigg\rbrace \Delta p^r_l \nonumber\end{aligned}

The combination

.. math::

   \left[ \left({\rm ln}\,p_{s{_{l}}} \right)^{n} + 
   { \Phi_s \over RT^r} + {1 \over 2} {\Delta t \over RT^r} \left( {\boldsymbol{V}} \cdot \nabla \;\Phi_s \right)^{n+{1\over 2}}
   \right] _{D_{2}}

is treated as a unit, and follows from :eq:`sld.3` .

Thermodynamic Equation
~~~~~~~~~~~~~~~~~~~~~~

The thermodynamic equation is obtained from (25) of W&O94 modified to be
spatially uncentered and to use :math:`{\rm ln}\,p_{s}'`. In addition
Hortal’s modification (\citep{tempertonetal01}) is included,
in which

.. math::

   {d \over dt} \left[
   -\left(p_s B {\partial T \over \partial p}\right)_{ref}
   { \Phi_s \over RT^r } \right]

is subtracted from both sides of the temperature equation. This is akin
to horizontal diffusion which includes the first order term converting
horizontal derivatives from eta to pressure coordinates, with
:math:`\left({\rm ln}\;p_s\right)` replaced by
:math:`-{ \Phi_s \over RT^r}`, and :math:`\left(p_s B {\partial T \over \partial p}\right)_{ref}`
taken as a global average so it is invariant with time and can commute
with the differential operators.

.. math::

   \begin{aligned}
   {T_A^{n+1} - T_D^{n} \over \Delta t} &=&
   \left\{ \left\{\left[
   -\left(p_s B(\eta) {\partial T \over \partial p}\right)_{ref}
   { \Phi_s \over RT^r } \right]_A^{n+1} - \left[
   -\left(p_s B(\eta) {\partial T \over \partial p}\right)_{ref}
   { \Phi_s \over RT^r } \right]_D^{n} \right\} \Bigg/ \Delta t \right.
   \nonumber \\
   &\phantom{=}& \left. +{ 1 \over RT^r }\left[
   \left(p_s B(\eta) {\partial T \over \partial p}\right)_{ref}
    {\boldsymbol{V}} \cdot \nabla \;\Phi_s
   + \Phi_s \dot\eta {\partial \over \partial \eta} \left(p_s B(\eta)
   {\partial T \over \partial p}\right)_{ref} \right]_M^{n+{1\over 2}}
   \right\}
     \nonumber \\
   &\phantom{=}&+\left({RT_v \over c_p^*} {\omega \over p}
   	\right)^{n+{1\over 2}}_M + Q^{n}_M \nonumber \\
   &\phantom{=}&+ {RT^r \over c_p} {p_s^r \over p^r}\left[ B(\eta)
   	{d_2\;{\rm ln}\;p_s' \over dt} + \overline{\left({1 \over p_s}
   	\dot \eta {\partial p \over \partial \eta} \right)}^t \right]
   	\\
   &\phantom{=}&- {RT^r \over c_p} {p_s^r \over p^r} \left[\left({p \over
           p_s}\right) \left( {\omega \over p} \right) \right]^{n+{1\over
           2}}_M \nonumber \\
   &\phantom{=}&- {RT^r \over c_p} {p_s^r \over p^r} B(\eta) \left[ {1
             \over RT^r} {\boldsymbol{V}} \cdot \nabla \;\Phi_s
             \right]^{n+{1\over 2}}_{M_2} \nonumber\end{aligned}

Note that :math:`Q^{n}` represents the heating calculated to advance
from time :math:`n` to time :math:`n+1` and is valid over the interval.

The calculation of :math:`\left(p_s B {\partial T \over \partial
p}\right)_{ref}` follows that of the ECMWF (Research Manual 3, ECMWF
Forecast Model, Adiabatic Part, ECMWF Research Department, 2nd edition,
1/88, pp 2.25-2.26) Consider a constant lapse rate atmosphere

.. math::

   \begin{aligned}
   T &=& T_0\left({p\over p_0}\right)^{R \gamma / g} \\ {\partial T \over
   \partial p} &=& {1 \over p}{R \gamma \over g} T_0\left({p\over
   p_0}\right)^{R \gamma / g} \\ p_s B {\partial T \over \partial p} &=&
   B {p_s \over p}{R \gamma \over g} T \\
   \left( p_s B {\partial T \over \partial p} \right)_{ref} &=& B_k
    {(p_s)_{ref} \over (p_k)_{ref}}
   {R \gamma \over g} (T_k)_{ref} ~~\hbox{for}~~ (T_k)_{ref} > T_C \\
   \left( p_s B {\partial T \over \partial p} \right)_{ref} &=& 0 ~~for~~
    (T_k)_{ref} \leq T_C \\
   (p_k)_{ref} &=& A_k p_0 + B_k (p_s)_{ref} \\ (T_k)_{ref} &=&
   T_0\left({(p_k)_{ref} \over (p_s)_{ref} }\right)^{R \gamma / g} \\
   (p_s)_{ref} &=& 1013.25 {\rm mb} \\ T_0 &=& 288 {\rm K} \\ p_0 &=&
   1000 {\rm mb} \\ \gamma &=& 6.5 {\rm K / km} \\ T_C &=& 216.5 {\rm K}\end{aligned}

Momentum equations
~~~~~~~~~~~~~~~~~~

The momentum equations follow from (3) of W&O94 modified to be spatially
uncentered, to use :math:`{\rm ln}\,p_{s}'`, and with the Coriolis term
implicit following :cite:`cote_staniforth88` and :cite:`temperton97`. The
semi-implicit, semi-Lagrangian momentum equation at level :math:`k` (but
with the level subscript :math:`k` suppressed) is

.. math::

   \begin{aligned}
   {{\boldsymbol{V}}^{n+1}_{_{A}} - {\boldsymbol{V}}^{n}_{_{D}} \over \Delta
   t}& = &
           -{1 \over 2}\bigg\lbrace \,
              \left(1 + \epsilon \right) \left[f{\mathbf{{\hat{k}}}}
                  \times {\boldsymbol{V}}
           \right]^{n+1}_{_{A}}
           + \left(1 - \epsilon \right) \left[f{\mathbf{{\hat{k}}}}
                  \times {\boldsymbol{V}}
           \right]^{n}_{_{D}}\bigg\rbrace + {\boldsymbol{F}}^n_M \nonumber
           \\
           &\phantom{=}& -{1 \over 2}\bigg\lbrace\, \left(1 + \epsilon
             \right)
            \left[ \nabla \left(\Phi_s + R {\boldsymbol{H}}_k \cdot
           {\boldsymbol{T}}_v \right)
           + RT_v {B \over p} p_s \nabla\,{\rm ln}\,p_s
             \right]^{n+{1\over 2}}_{_{A}} \nonumber \\
           &\phantom{=}&\phantom{-{1 \over 2}} + \left(1 - \epsilon
              \right)
            \left[ \nabla \left(\Phi_s + R {\boldsymbol{H}}_k \cdot
           {\boldsymbol{T}}_v \right)
           + RT_v {B \over p} p_s \nabla\,{\rm ln}\,p_s
             \right]^{n+{1\over 2}}_{_{D}}\bigg\rbrace
            \nonumber \\ &\phantom{=}& - {1 \over 2} \bigg\lbrace\,
          \left(1 + \epsilon \right) \nabla \left[ R {\boldsymbol{H}}_k^r
                  \cdot {\boldsymbol{T}}
   	       + RT^r\,{\rm ln}\,p_s' \right]^{n+1}_{_{A}} \\
          &\phantom{=}& \phantom{- {1 \over 2}} - \left(1 + \epsilon
             \right)
             \nabla \left[\Phi_s + R {\boldsymbol{H}}_k^r \cdot
                  {\boldsymbol{T}} + RT^r\,{\rm ln}\,p_s\right]^{n+{1\over
                  2}}_{_{A}} \nonumber \\
           &\phantom{=}& \phantom{- {1 \over 2}} + \left(1 - \epsilon
             \right)
             \nabla\left[\Phi_s + R {\boldsymbol{H}}_k^r \cdot {\boldsymbol{T}}
                  + RT^r\,{\rm ln}\,p_s\right]^{n}_{_{D}}\nonumber \\
          &\phantom{=}& \phantom{- {1 \over 2}}- \left(1 - \epsilon
             \right)
             \nabla\left[\Phi_s + R {\boldsymbol{H}}_k^r \cdot {\boldsymbol{T}}
                  + RT^r\,{\rm ln}\,p_s\right]^{n+{1\over
                  2}}_{_{D}}\bigg\rbrace \nonumber\end{aligned}

The gradient of the geopotential is more complex than in the
:math:`\sigma` system because the hydrostatic matrix
:math:`\boldsymbol{H}` depends on the local pressure:

.. math::

   \nabla\left({\boldsymbol{H}}_k \cdot {\boldsymbol{T}}_v \right) =
   {\boldsymbol{H}}_k \cdot \left[\left(1 + \epsilon_v
   	 {\boldsymbol{q}}\right)\nabla {\boldsymbol{T}} +
   	 \epsilon_v {\boldsymbol{T}}\nabla {\boldsymbol{q}} \right] +
            {\boldsymbol{T}}_v \cdot \nabla {\boldsymbol{H}}_k

where :math:`\epsilon_v` is :math:`(R_v/R - 1)` and :math:`R_v` is the
gas constant for water vapor. The gradient of :math:`T` is calculated
from the spectral representation and that of :math:`q` from a discrete
cubic approximation that is consistent with the interpolation used in
the semi-Lagrangian water vapor advection. In general, the elements of
:math:`\boldsymbol{H}` are functions of pressure at adjacent discrete
model levels

.. math:: H_{kl} = f_{kl}(p_{l+1/2},p_l,p_{l-1/2})

The gradient is then a function of pressure and the pressure gradient

.. math::

   \nabla H_{kl} = g_{kl}(p_{_{l+1/2}},\; p_{_{l}},\; p_{_{l-1/2}},
         \nabla p_{_{l+1/2}}, \nabla p_{_{l}}, \nabla p_{_{l-1/2}})

The pressure gradient is available from :eq:`sld.1`  and the surface
pressure gradient calculated from the spectral representation

.. math:: \nabla p_{_{l}} = B_l\nabla p_s = B_l p_s \nabla\,{\rm ln}\,p_s

Development of semi-implicit system equations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The momentum equation can be written as

.. math::
   :label: vmeq

   \begin{aligned}
   {{\boldsymbol{V}}^{n+1}_{_{A}} - {\boldsymbol{V}}^{n}_{_{D}} \over \Delta t}
   =
           -{1 \over 2}\bigg\lbrace
             &\left(1 + \epsilon \right) \left[f{\mathbf{{\hat{k}}}}
                  \times {\boldsymbol{V}}
           \right]^{n+1}_{_{A}}
           + \left(1 - \epsilon \right) \left[f{\mathbf{{\hat{k}}}}
                  \times {\boldsymbol{V}}
           \right]^{n}_{_{D}}\bigg\rbrace \nonumber \\
            - {1 \over 2} \bigg\lbrace
          &\left(1 + \epsilon \right) \nabla \left[ R {\boldsymbol{H}}_k^r
                  \cdot {\boldsymbol{T}}
   	       + RT^r\,{\rm ln}\,p_s' \right]^{n+1}_{_{A}}\bigg\rbrace
          + RHS_{\boldsymbol{V}}
   
   ~,\end{aligned}

where :math:`RHS_{\boldsymbol{V}}` contains known terms at times
(:math:`{n+{1\over 2}}`) and (:math:`n`).

By combining terms, [vmeq] can be written in general as

.. math::
   :label: dw8

   {\mathcal U}^{^{n+1}}_{_{A}} {\bf {\hat{i}}}_{_{A}} + {\mathcal
     V}^{^{n+1}}_{_{A}} {\bf {\hat{j}}}_{_{A}} = {\mathcal U}_{_{A}} {\bf
     {\hat{i}}}_{_{A}} + {\mathcal V}_{_{A}} {\bf {\hat{j}}}_{_{A}} + {\mathcal U}_{_{D}}
     {\bf {\hat{i}}}_{_{D}} + {\mathcal V}_{_{D}} {\bf {\hat{j}}}_{_{D}}
   ~,

where :math:`\bf{{\hat{i}}}` and :math:`\bf{{\hat{j}}}` denote the
spherical unit vectors in the longitudinal and latitudinal directions,
respectively, at the points indicated by the subscripts, and
:math:`\mathcal U` and :math:`\mathcal V` denote the appropriate combinations of
terms in [vmeq]. Note that :math:`{\mathcal U}^{^{n+1}}_{_{A}}` is distinct
from the :math:`{\mathcal U}_{_{A}}`. Following :cite:`batesetal90`,
equations for the individual components are obtained by relating the
unit vectors at the departure points
(:math:`{\bf {\hat{i}}}_{_{D}}`,\ :math:`{\bf {\hat{j}}}_{_{D}}`) to
those at the arrival points
(:math:`{\bf {\hat{i}}}_{_{A}}`,\ :math:`{\bf {\hat{j}}}_{_{A}}`):

.. math::

   \begin{aligned}
     {\bf {\hat{i}}}_{_{D}} = \alpha^u_{_{A}}{\bf {\hat{i}}}_{_{A}} +
     \beta^u_{_{A}}{\bf {\hat{j}}}_{_{A}} \\ {\bf {\hat{j}}}_{_{D}} =
     \alpha^v_{_{A}}{\bf {\hat{i}}}_{_{A}} + \beta^v_{_{A}}{\bf {\hat{j}}}_{_{A}}
   ~,\end{aligned}

in which the vertical components (:math:`{\bf {\hat{k}}}`) are ignored.
The dependence of :math:`\alpha`\ ’s and :math:`\beta`\ ’s on the
latitudes and longitudes of the arrival and departure points is given in
the Appendix of :cite:`batesetal90`.

W&O94 followed :cite:`batesetal90` which ignored rotating the vector to
remain parallel to the earth’s surface during translation. We include
that factor by keeping the length of the vector written in terms of
:math:`\left({\mathbf{{\hat{i}}}}_{_{A}},{\mathbf{{\hat{j}}}}_{_{A}}\right)`
the same as the length of the vector written in terms of
:math:`\left({\mathbf{{\hat{i}}}}_{_{D}},{\mathbf{{\hat{j}}}}_{_{D}}\right)`.
Thus, (10) of W&O94 becomes

.. math::

   \begin{aligned}
     {\mathcal U}^{^{n+1}}_{_{A}} &= {\mathcal U}_{_{A}} +
     \gamma\alpha^u_{_{A}}{\mathcal U}_{_{D}} + \gamma\alpha^v_{_{A}}{\mathcal
     V}_{_{D}} \nonumber \\ {\mathcal V}^{^{n+1}}_{_{A}} &= {\mathcal V}_{_{A}} +
     \gamma\beta^u_{_{A}}{\mathcal U}_{_{D}} + \gamma\beta^v_{_{A}}{\mathcal
     V}_{_{D}}\end{aligned}

where

.. math::

   \gamma = \left[
       { {\mathcal U}_{_{D}}^2 + {\mathcal V}_{_{D}}^2 \over \left({\mathcal
         U}_{_{D}}\alpha^u_{_{A}} + {\mathcal
         V}_{_{D}}\alpha^v_{_{A}}\right)^2 + \left({\mathcal
         U}_{_{D}}\beta^u_{_{A}} + {\mathcal V}_{_{D}}\beta^v_{_{A}}\right)^2
         }
       \right]^{1 \over 2}

After the momentum equation is written in a common set of unit vectors

.. math::

   {\boldsymbol{V}}^{n+1}_{_{A}} + \left({1 + \epsilon \over 2}\right)
     \Delta t
     \left[f{\mathbf{{\hat{k}}}} \times {\boldsymbol{V}}
       \right]^{n+1}_{_{A}}
     + \left({1 + \epsilon \over 2}\right) \Delta t
     \nabla \left[ R {\boldsymbol{H}}_k^r \cdot {\boldsymbol{T}} + RT^r\,{\rm
       ln}\,p_s' \right]^{n+1}_{_{A}}
     = {{\mathcal R}}_{\boldsymbol{V}}^*

Drop the :math:`(~~~)^{n+1}_A` from the notation, define

.. math:: \alpha = \left(1 + \epsilon\right) \Delta t \Omega

and transform to vorticity and divergence

.. math::

   \begin{aligned}
     \zeta + \alpha \sin \varphi \delta + {\alpha \over a} v \cos\varphi
   	&=& {1 \over a\cos\varphi} \left[ {\partial{{\mathcal R}}_v^* \over
   	\partial \lambda}
   	  - {\partial \over \partial\varphi}\left({{\mathcal R}}_u^*
   	\cos\varphi\right)\right] \\ \delta - \alpha \sin \varphi
   	\zeta + {\alpha \over a} u \cos\varphi
   	& +& \left( {1 + \epsilon \over 2} \right) \Delta t \nabla^2
           \left[ R {\boldsymbol{H}}_k^r \cdot {\boldsymbol{T}}
   	  + RT^r\,{\rm ln}\,p_s' \right]^{n+1}_{_{A}} \nonumber \\ &=&
   	{1 \over a\cos\varphi}
   	\left[ {\partial{{\mathcal R}}_u^* \over \partial \lambda} + {\partial
   	  \over \partial\varphi}\left({{\mathcal R}}_v^* \cos\varphi\right)\right]\end{aligned}

Note that

.. math::

   \begin{aligned}
     u\cos\varphi &=& {1 \over a} {{\partial}\over{\partial}\lambda}\left(\nabla^{-2}
     \delta \right) - {\cos\varphi \over a}
     {{\partial}\over{\partial}\varphi}\left(\nabla^{-2} \zeta \right) \\ v\cos\varphi
     &=& {1 \over a} {{\partial}\over{\partial}\lambda}\left(\nabla^{-2} \zeta \right) +
     {\cos\varphi \over a} {{\partial}\over{\partial}\varphi}\left(\nabla^{-2} \delta
     \right)\end{aligned}

Then the vorticity and divergence equations become

.. math::

   \begin{aligned}
     \zeta + \alpha \sin \varphi \delta + {\alpha \over
     a^2}{{\partial}\over{\partial}\lambda}\left(\nabla^{-2} \zeta \right)
     &+&{\alpha\cos\varphi \over a^2}{{\partial}\over{\partial}\varphi}\left(\nabla^{-2}
     \delta \right) \nonumber \\ &=&{1 \over a\cos\varphi} \left[
     {{\partial}{{\mathcal R}}_v^* \over {\partial}\lambda}
       - {{\partial}\over {\partial}\varphi}\left({{\mathcal R}}_u^* \cos\varphi\right)\right] =
     {{\mathcal L}}\\ \delta - \alpha \sin \varphi \zeta + {\alpha \over
     a^2}{{\partial}\over{\partial}\lambda}\left(\nabla^{-2} \delta \right)
     &-&{\alpha\cos\varphi \over a^2}{{\partial}\over{\partial}\varphi}\left(\nabla^{-2}
     \zeta \right) + \left( {1 + \epsilon \over 2}\right) \Delta t
     \nabla^2 \left[ R {\boldsymbol{H}}_k^r \cdot {\boldsymbol{T}} + RT^r\,{\rm
       ln}\,p_s' \right]^{n+1}_{_{A}} \nonumber \\
     &=& {1 \over a\cos\varphi}
     \left[ {{\partial}{{\mathcal R}}_u^* \over {\partial}\lambda} + {{\partial}\over
       {\partial}\varphi}\left({{\mathcal R}}_v^* \cos\varphi\right)\right]
     = {{\mathcal M}}\end{aligned}

Transform to spectral space as described in the description of the
Eulerian spectral transform dynamical core. Note, from (4.5b) and (4.6)
on page 177 of :cite:`machenhauer79`

.. math::

   \begin{aligned}
     \mu P_n^m &=& D_{n+1}^m P_{n+1}^m + D_{n}^m P_{n-1}^m \\ D_{n}^m &=&
     \left({n^2-m^2 \over 4n^2-1}\right)^{1 \over 2}\end{aligned}

and from (4.5a) on page 177 of :cite:`machenhauer79`

.. math::

   \left( 1 - \mu^2\right) {{\partial}\over{\partial}\mu}P_n^m = -nD_{n+1}^m P_{n+1}^m
     + \left (n+1 \right) D_{n}^m P_{n-1}^m

Then the equations for the spectral coefficients at time :math:`n+1` at
each vertical level are

.. math::

   \begin{aligned}
     \zeta_n^m \left( 1 - {im\alpha \over n\left(n+1\right)}\right) +
     \delta_{n+1}^m \alpha \left({n\over n+1}\right) D_{n+1}^m +
     \delta_{n-1}^m \alpha \left({n+1\over n}\right) D_{n}^m &=& {{\mathcal L}}_n^m
     \\ \delta_n^m \left( 1 - {im\alpha \over n\left(n+1\right)}\right)
     - \zeta_{n+1}^m \alpha \left({n\over n+1}\right) D_{n+1}^m
     - \zeta_{n-1}^m \alpha \left({n+1\over n}\right) D_{n}^m && \\
     - \left({1 + \epsilon \over 2}\right) \Delta t
     {n\left(n+1\right) \over a^2} \left[ R {\boldsymbol{H}}_k^r \cdot
       {\boldsymbol{T}_n^m} + RT^r\,{\rm ln}\,{p_s'}_n^m \right]
     &=& {{\mathcal M}}_n^m \nonumber\end{aligned}

.. math::

   \begin{aligned}
     {{\rm ln} p'_s}^m_n &=& {\rm PS}^m_n - \left({ 1 + \epsilon \over
     2}\right) {\Delta t\over p^r_s} \left(\underline{\Delta p^r}
     \right)^T \underline{\delta}^m_n \\ \underline{T}^m_n &=&
     \underline{\rm TS}^m_n - \left({ 1 + \epsilon \over 2}\right) \Delta
     t {\boldsymbol{D}}^r \underline{\delta}^m_n\end{aligned}

The underbar denotes a vector over vertical levels. Rewrite the
vorticity and divergence equations in terms of vectors over vertical
levels.

.. math::

   \begin{aligned}
     \underline{\delta}_n^m \left( 1 - {im\alpha \over
     n\left(n+1\right)}\right)
     - \underline{\zeta}_{n+1}^m \alpha \left({n\over n+1}\right)
     - D_{n+1}^m \underline{\zeta}_{n-1}^m \alpha \left({n+1\over
     - n}\right) D_{n}^m && \\
     - \left({1 + \epsilon \over 2}\right) \Delta t
     {n\left(n+1\right) \over a^2} \left[ R {\boldsymbol{H}}^r
       \underline{T}_n^m + R\underline{T}^r\,{\rm ln}\,{p_s'}_n^m \right]
     &=& \underline{DS}_n^m \nonumber \\ \underline{\zeta}_n^m \left( 1 -
     {im\alpha \over n\left(n+1\right)}\right) +
     \underline{\delta}_{n+1}^m \alpha \left({n\over n+1}\right)
     D_{n+1}^m + \underline{\delta}_{n-1}^m \alpha \left({n+1\over
     n}\right) D_{n}^m &=& \underline{VS}_n^m\end{aligned}

Define :math:`\underline{h}_n^m` by

.. math::

   \begin{aligned}
     g\underline{h}_n^m &= R {\boldsymbol{H}}^r T_n^m +
   	       R\underline{T}^r\,{\rm ln}\,{p_s'}_n^m\\[-1.0em]
   \intertext{and}\nonumber\\[-2.0em] {{\mathcal A}}_n^m &= 1 - {im\alpha \over
   n\left(n+1\right)} \\ {{{\mathcal B}}^+}_n^m & = \alpha\left({n\over n+1}\right)
   D_{n+1}^m \\ {{{\mathcal B}}^-}_n^m & = \alpha\left({n+1\over n}\right) D_{n}^m\end{aligned}

Then the vorticity and divergence equations are

.. math::

   \begin{aligned}
   {{\mathcal A}}_n^m \underline{\zeta}_n^m + {{{\mathcal B}}^+}_n^m \underline{\delta}_{n+1}^m +
   {{{\mathcal B}}^-}_n^m \underline{\delta}_{n-1}^m &=&
   \underline{{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}_n^m \\ {{\mathcal A}}_n^m \underline{\delta}_n^m
   - {{{\mathcal B}}^+}_n^m \underline{\zeta}_{n+1}^m {{{\mathcal B}}^-}_n^m
   - \underline{\zeta}_{n-1}^m
   -\left({1 + \epsilon \over 2}\right) \Delta t {n\left(n+1\right) \over
      a^2} g\underline{h}_n^m
   &=& \underline{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}_n^m\end{aligned}

Note that these equations are uncoupled in the vertical, i.e. each
vertical level involves variables at that level only. The equation for
:math:`\underline{h}_n^m` however couples all levels.

.. math::

   g\underline{h}_n^m = -\left({1 + \epsilon \over 2}\right) \Delta t
   \left[
   R {\boldsymbol{H}}^r {\boldsymbol{D}}^r + R\underline{T}^r
     {\left(\underline{\Delta p^r} \right)^T \over p^r_s} \right]
   \underline{\delta}_n^m + R {\boldsymbol{H}}^r
   \underline{{\hbox{\sffamily\slshape T}}{\hbox{\sffamily\slshape S}}}_n^m + R\underline{T}^r {\rm PS}_n^m

Define :math:`{\boldsymbol{C}}^r` and
:math:`\underline{{\hbox{\sffamily\slshape H}}{\hbox{\sffamily\slshape S}}}_n^m`
so that

.. math::

   g\underline{h}_n^m = -\left({1 + \epsilon \over 2}\right) \Delta t
   {{\hbox{\sffamily\slshape C}}}^r\underline{\delta}_n^m + \underline{{\hbox{\sffamily\slshape H}}{\hbox{\sffamily\slshape S}}}_n^m

Let :math:`g{\rm D}_\ell` denote the eigenvalues of
:math:`{\boldsymbol{C}}^r` with corresponding eigenvectors
:math:`\underline{\Phi}_\ell` and :math:`{\mathbf{\Phi}}` is the
matrix with columns :math:`\underline{\Phi}_\ell`

.. math::

   {\mathbf{\Phi}}= \left( \begin{array}{*{3}{c@{\:}}c} \underline{\Phi}_1 &
      \underline{\Phi}_2 & \dots & \underline{\Phi}_L \\
    \end{array}\right)

and :math:`g{\boldsymbol{D}}` the diagonal matrix of corresponding
eigenvalues

.. math::

   \begin{aligned}
   g{\boldsymbol{D}} &=& g \left(
    \begin{array}{*{3}{c@{\:}}c}
   {\rm D}_1 & 0 & \cdots & 0 \\ 0 & {\rm D}_2 & \cdots & 0 \\ \vdots &
   \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & {\rm D}_L \\
   \end{array}
   \right) \\ {\boldsymbol{C}}^r {{\mathbf{\Phi}}} &=& {{\mathbf{\Phi}}} g {\boldsymbol{D}} \\
   {{\mathbf{\Phi}}}^{-1}{\boldsymbol{C}}^r {{\mathbf{\Phi}}} &=& g {\boldsymbol{D}}\end{aligned}

Then transform

.. math::

   \begin{aligned}
   {2}
   \underline{\tilde\zeta}_n^m &= {\mathbf{\Phi}}^{-1} \underline{\zeta}_n^m
   &\quad,\quad \underline{\widetilde{{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}}_n^m &=
   {\mathbf{\Phi}}^{-1} \underline{{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}_n^m\\
   \underline{\tilde\delta}_n^m &= {\mathbf{\Phi}}^{-1} \underline{\delta}_n^m
   &\quad,\quad \underline{\widetilde{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}}_n^m &=
   {\mathbf{\Phi}}^{-1} \underline{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}_n^m\\ \underline{\tilde
   h}_n^m &= {\mathbf{\Phi}}^{-1} \underline{ h}_n^m &\quad,\quad
   \underline{\widetilde{{\hbox{\sffamily\slshape H}}{\hbox{\sffamily\slshape S}}}}_n^m &= {\mathbf{\Phi}}^{-1}
   \underline{{\hbox{\sffamily\slshape H}}{\hbox{\sffamily\slshape S}}}_n^m\end{aligned}

.. math::

   \begin{aligned}
   {{\mathcal A}}_n^m \underline{\tilde\zeta}_n^m + {{{\mathcal B}}^+}_n^m
   \underline{\tilde\delta}_{n+1}^m + {{{\mathcal B}}^-}_n^m
   \underline{\tilde\delta}_{n-1}^m &=&
   \underline{\widetilde{{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}}_n^m \\ {{\mathcal A}}_n^m
   \underline{\tilde\delta}_n^m
   - {{{\mathcal B}}^+}_n^m \underline{\tilde\zeta}_{n+1}^m {{{\mathcal B}}^-}_n^m
   - \underline{\tilde\zeta}_{n-1}^m
   -\left({1 + \epsilon \over 2}\right) \Delta t {n\left(n+1\right) \over
      a^2} g\underline{\tilde h}_n^m
   &=& \underline{\widetilde{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}}_n^m \\ g\underline{\tilde
   h}_n^m + \left({1 + \epsilon \over 2}\right) \Delta t
   {\mathbf{\Phi}}^{-1}{\boldsymbol{C}}^r{\mathbf{\Phi}}{\mathbf{\Phi}}^{-1}\underline{\delta}_n^m &=&
   \underline{\widetilde{{\hbox{\sffamily\slshape H}}{\hbox{\sffamily\slshape S}}}}_n^m \\ \underline{\tilde
   h}_n^m + \left({1 + \epsilon \over 2}\right) \Delta t
   {\boldsymbol{D}}\underline{\tilde \delta}_n^m &=& {1 \over g}
   \underline{\widetilde{{\hbox{\sffamily\slshape H}}{\hbox{\sffamily\slshape S}}}}_n^m\end{aligned}

Since :math:`{\boldsymbol{D}}` is diagonal, all equations are now
uncoupled in the vertical.

For each vertical mode, i.e. element of
:math:`(\underline{\tilde{~~}})_n^m`, and for each Fourier wavenumber
:math:`m` we have a system of equations in :math:`n` to solve. In
following we drop the Fourier index :math:`m` and the modal element
index :math:`(~~)_\ell` from the notation.

.. math::

   \begin{aligned}
   {{\mathcal A}}_n {\tilde\zeta}_n + {{{\mathcal B}}^+}_n {\tilde\delta}_{n+1} + {{{\mathcal B}}^-}_n
   {\tilde\delta}_{n-1} &=& {\widetilde{{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}}_n \\ {{\mathcal A}}_n
   {\tilde\delta}_n
   - {{{\mathcal B}}^+}_n {\tilde\zeta}_{n+1} {{{\mathcal B}}^-}_n {\tilde\zeta}_{n-1}
   -\left({1 + \epsilon \over 2}\right) \Delta t {n\left(n+1\right) \over
      a^2} g{\tilde h}_n
   &=& {\widetilde{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}}_n \\ {\tilde h}_n + \left({1 +
   \epsilon \over 2}\right) \Delta t {\rm D}_\ell{\tilde \delta}_n &=& {1
   \over g} {\widetilde{{\hbox{\sffamily\slshape H}}{\hbox{\sffamily\slshape S}}}}_n\end{aligned}

The modal index :math:`(~~)_\ell` was included in the above equation on
:math:`{\rm D}` only as a reminder, but will also be dropped in the
following.

Substitute :math:`{\tilde\zeta}` and :math:`{\tilde h}` into the
:math:`{\tilde\delta}` equation.

.. math::

   \begin{aligned}
   \left[ {{\mathcal A}}_n + \left( {1 + \epsilon \over 2}\right)^2 \left(\Delta t
          \right) ^2 {n\left(n+1\right) \over a^2} g{\rm D}
   + {{{\mathcal B}}^+}_n {{\mathcal A}}_{n+1}^{-1} {{{\mathcal B}}^-}_{n+1} + {{{\mathcal B}}^-}_n {{\mathcal A}}_{n-1}^{-1}
   {{{\mathcal B}}^+}_{n-1} \right] & {\tilde\delta}_{n}  + \left( {{{\mathcal B}}^+}_n
   {{\mathcal A}}_{n+1}^{-1} {{{\mathcal B}}^+}_{n+1} \right) {\tilde\delta}_{n+2} ~~+~~ \left(
   {{{\mathcal B}}^-}_n {{\mathcal A}}_{n-1}^{-1} {{{\mathcal B}}^-}_{n-1} \right) {\tilde\delta}_{n-2}
   ~~~~~~~~~~~~~~~~~~~& \\
   = \widetilde{{\hbox{\sffamily\slshape D}}{\hbox{\sffamily\slshape S}}}_n
   + \left({1 + \epsilon \over 2}\right) \Delta t {n\left(n+1\right)
                  \over a^2} \widetilde{{\hbox{\sffamily\slshape H}}{\hbox{\sffamily\slshape S}}}_n
   + {{{\mathcal B}}^+}_n {{\mathcal A}}_{n+1}^{-1} \widetilde{{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}_{n+1} + {{{\mathcal B}}^-}_n
   {{\mathcal A}}_{n-1}^{-1} \widetilde{{\hbox{\sffamily\slshape V}}{\hbox{\sffamily\slshape S}}}_{n-1} \nonumber\end{aligned}

which is just two tri-diagonal systems of equations, one for the even
and one for the odd :math:`n`\ ’s, and :math:`m \le n \le N`

At the end of the system, the boundary conditions are

.. math::

   \begin{aligned}
   {2}
   n & = m, & \quad{{{\mathcal B}}^-}_n &= {{{\mathcal B}}^-}_m^m = 0 \\ n & = m+1,& \quad
   {{{\mathcal B}}^-}_{n-1} &= {{{\mathcal B}}^-}_m^m = {{{\mathcal B}}^-}_{(m+1)-1}^m = 0 \nonumber\end{aligned}

the :math:`{\tilde\delta}_{n-2}` term is not present, and from the
underlying truncation

.. math:: \tilde\delta_{N+1}^m = \tilde\delta_{N+2}^m = 0

For each :math:`m` and :math:`\ell` we have the general systems of
equations

.. math::

   \begin{aligned}
   -A_n {\tilde\delta}_{n+2} + B_n {\tilde\delta}_{n} -C_n
   -{\tilde\delta}_{n-2} &=& D_n \;,
   \left\{
   \begin{array}{c}
     n=m,m+2,..., \left\{
   \begin{array}{c}
      N+1 \\ {\rm or} \\ N+2 \\
   \end{array}
   \right.~~~~~ \\ n=m+1,m+3,..., \left\{
   \begin{array}{c}
      N+1 \\ {\rm or} \\ N+2 \\
   \end{array}
   \right. \\
   \end{array}
   \right. \\ C_m = C_{m+1} &=& 0 \\ \tilde\delta_{N+1} =
   \tilde\delta_{N+2} &=& 0\end{aligned}

Assume solutions of the form

.. math:: \tilde\delta_n = E_n \tilde\delta_{n+2} + F_n

then

.. math::

   \begin{aligned}
   E_m &=& {A_m \over B_m} \\ F_M &=& {D_m \over B_m}\end{aligned}

.. math::

   \begin{aligned}
   E_n &=& {A_n \over B_n - C_nE_{n-2}}~~,~~~ n=m+2,m+4,..., \left\{
                               \begin{array}{c}
                                 N-2 \\ {\rm or} \\ N-3 \\
                               \end{array} 
                            \right. \\
   F_n &=& {D_n + C_nF_{n-2} \over B_n - C_nE_{n-2}}~~,~~~ n=m+2,m+4,...,
                            \left\{
                               \begin{array}{c}
                                 N \\ {\rm or} \\ N-1 \\
                               \end{array} 
                            \right.\end{aligned}

.. math:: \tilde\delta_N = F_N~~~~{\rm or}~~~~\tilde\delta_{N-1} = F_{N-1} \;,

.. math::

   \tilde\delta_n = E_n\tilde\delta_{n+2} + F_n \;,~~ \left\{
        \begin{array}{c}
           n=N-2,N-4,..., \left\{
                        \begin{array}{c}
                             m \\ {\rm or} \\ m+1 \\
                        \end{array} \right.
            \\ n=N-3,N-5,..., \left\{
                         \begin{array}{c}
                             m+1 \\ {\rm or} \\ m \\
                         \end{array} \right.
            \\
        \end{array}
    \right.

Divergence in physical space is obtained from the vertical mode
coefficients by

.. math:: \underline{\delta}_n^m = {\mathbf{\Phi}}\underline{\tilde\delta}_n^m

The remaining variables are obtained in physical space by

.. math::

   \begin{aligned}
   \zeta_n^m \left( 1 - {im\alpha \over n\left(n+1\right)}\right) &=&
   {{\mathcal L}}_n^m
   - \delta_{n+1}^m \alpha \left({n\over n+1}\right) D_{n+1}^m
   - \delta_{n-1}^m \alpha \left({n+1\over n}\right) D_{n}^m \\
   \underline{T}^m_n &=& \underline{\rm TS}^m_n
          - \left({ 1 + \epsilon \over 2}\right) \Delta t {\boldsymbol{D}}^r
              \underline{\delta}^m_n \\
   {{\rm ln} p'_s}^m_n &=& {\rm PS}^m_n
                       - \left({ 1 + \epsilon \over 2}\right)
                            {\Delta t\over p^r_s} \left(\underline{\Delta
                             p^r} \right)^T \underline{\delta}^m_n\end{aligned}

Trajectory Calculation
~~~~~~~~~~~~~~~~~~~~~~

The trajectory calculation follows :cite:`hortal99` Let
:math:`{\boldsymbol{R}}` denote the position vector of the parcel,

.. math:: {d{\boldsymbol{R}} \over dt} = {\boldsymbol{V}}

which can be approximated in general by

.. math::

   {\boldsymbol{R}}_D^n = {\boldsymbol{R}}_A^{n+1} - \Delta t
   {\boldsymbol{V}}_M^{n+{1 \over 2}}

Hortal’s method is based on a Taylor’s series expansion

.. math::

   {\boldsymbol{R}}_A^{n+1} = {\boldsymbol{R}}_D^n + \Delta t \left( {d
   {\boldsymbol{R}} \over d t} \right)_D^n +{\Delta t^2 \over 2} \left( {d^2
   {\boldsymbol{R}} \over d t^2} \right)_D^{n} + \dots

or substituting for :math:`{d {\boldsymbol{R}} / d t}`

.. math::

   {\boldsymbol{R}}_A^{n+1} = {\boldsymbol{R}}_D^n + \Delta t {\boldsymbol{V}}_D^n
   +{\Delta t^2 \over 2} \left( {d {\boldsymbol{V}} \over d t} \right)_D^{n}
   + \dots

Approximate

.. math::

   \begin{aligned}
   \left( {d {\boldsymbol{V}} \over d t} \right)_D^{n} &\approx
   {{\boldsymbol{V}}_A^n - {\boldsymbol{V}}_D^{n-1} \over \Delta t}\\[-1.0em]
   \intertext{giving}\nonumber\\[-2.0em] {\boldsymbol{V}}_M^{n+{1 \over 2}}
   &= {1 \over
   2}\left[\left(2{\boldsymbol{V}}^n-{\boldsymbol{V}}^{n-1}\right)_D +
   {\boldsymbol{V}}_A^n\right]\end{aligned}

for the trajectory equation.

Mass and energy fixers and statistics calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The semi-Lagrangian dynamical core applies the same mass and energy
fixers and statistical calculations as the Eulerian dynamical core.
These are described in sections [massfixers], [energyfixer], and
[statcalc].
