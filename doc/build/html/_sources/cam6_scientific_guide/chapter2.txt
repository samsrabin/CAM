.. _chap-coupling:

.. |cam| replace:: CAM6.0

Coupling of Dynamical Core and Parameterization Suite
=====================================================

The |cam| cleanly separates the parameterization suite from the dynamical
core, and makes it easier to replace or modify each in isolation. The
dynamical core can be coupled to the parameterization suite in a purely
time split manner or in a purely process split one, as described below.

Consider the general prediction equation for a generic variable
:math:`\psi`,

.. math::
   :label: 1

   \frac {\partial \psi} {\partial t} = D\left(\psi\right)  + P\left(\psi\right) \;,
   

where :math:`\psi` denotes a prognostic variable such as temperature or
horizontal wind component. The dynamical core component is denoted
:math:`D` and the physical parameterization suite :math:`P`.

A three-time-level notation is employed which is appropriate for the
semi-implicit Eulerian spectral transform dynamical core. However, the
numerical characteristics of the physical parameterizations are more
like those of diffusive processes rather than advective ones. They are
therefore approximated with forward or backward differences, rather than
centered three-time-level forms.

The *Process Split* coupling is approximated by

.. math::
   :label: 3

   \psi^{n+1} = \psi^{n-1} + 2\Delta t D(\psi^{n+1},\psi^{n},\psi^{n-1})
                           + 2\Delta t P(\psi^*,\psi^{n-1}) \;,
   

where :math:`P(\psi^*,\psi^{n-1})` is calculated first from

.. math::
   :label: 4

   \psi^* = \psi^{n-1} + 2\Delta t P(\psi^*,\psi^{n-1}) \;.
   

The *Time Split* coupling is approximated by

.. math::
   :label: 5

   \psi^* = \psi^{n-1} + 2\Delta t D(\psi^*,\psi^{n},\psi^{n-1}) \;, 
   
.. math::
   :label: 6

   \psi^{n+1} = \psi^* + 2\Delta t P(\psi^{n+1},\psi^*) \;.

The distinction is that in the *Process Split* approximation the
calculations of :math:`D` and :math:`P` are both based on the same past
state, :math:`\psi^{n-1}`, while in the *Time Split* approximations
:math:`D` and :math:`P` are calculated sequentially, each based on the
state produced by the other.

As mentioned above, the Eulerian core employs the three-time-level
notation in :eq:`3`-:eq:`6`. Eqns. :eq:`3`-:eq:`6` also apply to two-time-level
finite volume, semi-Lagrangian and spectral element (HOMME) cores by
dropping centered :math:`n` term dependencies, and replacing :math:`n`-1
by :math:`n` and :math:`2 \Delta t` by :math:`\Delta t`.

The parameterization package can be applied to produce an updated field
as indicated in :eq:`4` and :eq:`6`. Thus :eq:`6` can be written with an
operator notation

.. math::
   :label: 7

   \psi^{n+1} = {\boldsymbol{P}}\left(\psi^*\right) \;,
   

where only the past state is included in the operator dependency for
notational convenience. The implicit predicted state dependency is
understood. The *Process Split* equation :eq:`3` can also be written in
operator notation as

.. math::
   :label: 8

   \psi^{n+1} = {\boldsymbol{D}}\left(\psi^{n-1},
         \frac {{\boldsymbol{P}}(\psi^{n-1})-\psi^{n-1}} {2 \Delta t} \right) \;,
   

where the first argument of :math:`{\boldsymbol{D}}` denotes the
prognostic variable input to the dynamical core and the second denotes
the forcing rate from the parameterization package, e.g. the heating
rate in the thermodynamic equation. Again only the past state is
included in the operator dependency, with the implicit predicted state
dependency left understood. With this notation the *Time Split* system
:eq:`5` and :eq:`6` can be written

.. math::
   :label: 9

   \psi^{n+1} = {\boldsymbol{P}}\left({\boldsymbol{D}}\left(\psi^{n-1},0\right)\right) \;.
   

The total parameterization package in |cam| consists of a sequence of
components, indicated by

.. math::
   :label: 10

   P = \{ M,R,S,T \} \;,
   

where :math:`M` denotes (Moist) precipitation processes, :math:`R`
denotes clouds and Radiation, :math:`S` denotes the Surface model, and
:math:`T` denotes Turbulent mixing. Each of these in turn is subdivided
into various components: :math:`M` includes an optional dry adiabatic
adjustment (normally applied only in the stratosphere), moist
penetrative convection, shallow convection, and large-scale stable
condensation; :math:`R` first calculates the cloud parameterization
followed by the radiation parameterization; :math:`S` provides the
surface fluxes obtained from land, ocean and sea ice models, or
calculates them based on specified surface conditions such as sea
surface temperatures and sea ice distribution. These surface fluxes
provide lower flux boundary conditions for the turbulent mixing
:math:`T` which is comprised of the planetary boundary layer
parameterization, vertical diffusion, and gravity wave drag.

Defining operators following :eq:`7` for each of the parameterization
components, the couplings in |cam| are summarized as:

TIME SPLIT

.. math::
   :label: 11

   \psi^{n+1} = {\boldsymbol{T}}\left({\boldsymbol{S}}\left({\boldsymbol{R}}\left({\boldsymbol{M}}\left(
                {\boldsymbol{D}}\left(\psi^{n-1},0\right)\right)\right)\right)\right)


PROCESS SPLIT

.. math:: 
   :label: 12

   \psi^{n+1} = {\boldsymbol{D}}\left(\psi^{n-1},\frac { 
   {\boldsymbol{T}}\left({\boldsymbol{S}}\left({\boldsymbol{R}}\left(
   {\boldsymbol{M}}\left(\psi^{n-1}\right)\right)\right)\right) - \psi^{n-1}}
   {2\Delta t}\right)

The labels *Time Split* and *Process Split* refer to the coupling of the
dynamical core with the complete parameterization suite. The components
within the parameterization suite are coupled via time splitting in both
forms.

The *Process Split* form is convenient for spectral transform models.
With *Time Split* approximations extra spectral transforms are required
to convert the updated momentum variables provided by the
parameterizations to vorticity and divergence for the Eulerian spectral
core, or to recalculate the temperature gradient for the semi-Lagrangian
spectral core. The *Time Split* form is convenient for the finite-volume
core which adopts a Lagrangian vertical coordinate. Since the scheme is
explicit and restricted to small time-steps by its non-advective
component, it sub-steps the dynamics multiple times during a longer
parameterization time step. With *Process Split* approximations the
forcing terms must be interpolated to an evolving Lagrangian vertical
coordinate every sub-step of the dynamical core. Besides the expense
involved, it is not completely obvious how to interpolate the
parameterized forcing, which can have a vertical grid scale component
arising from vertical grid scale clouds, to a different vertical grid.
:cite:`williamson02` compares simulations with the Eulerian spectral
transform dynamical core coupled to the CCM3 parameterization suite via
*Process Split* and *Time Split* approximations.
