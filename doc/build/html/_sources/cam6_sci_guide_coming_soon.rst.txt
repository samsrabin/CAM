.. on documentation master file, created by
   sphinx-quickstart on Tue Jan 31 19:46:36 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _scientific-guide:

#####################################
CAM6 Scientific Guide
#####################################

CAM6 contains substantial modifications of every atmospheric physics parameterization except for radiative
transfer.   The Cloud Layers Unified by Binormals (CLUBB, :cite:`golaz2002` , :cite:`bogen2013` ) scheme has replaced earlier schemes for boundary
layer turbulence, shallow convection and cloud macrophysics. CLUBB is a prognostic moist turbulence scheme
that calculates joint higher-order moments of subgrid vertical velocity,  water content and liquid water
potential temperature.  Equations for these moments are closed using assumed joint binormal probability
density functions (PDFs)  for these quantities.  In addition to calculating subgrid vertical fluxes,
CLUBB’s PDF closure is also used to calculate large-scale condensation and cloud fraction.
An improved two-moment prognostic cloud microphysics (MG2, :cite:`gettelman2015`) has also been introduced.  The major innovation
in MG2 is to carry prognostic precipitation species – rain and snow – in addition to cloud condensates.
MG2 interacts with the MAM4 aerosol microphysics scheme to calculate condensate mass fractions and number
concentrations. Deep convection (:cite:`zhang95`) has been significantly retuned to increase the sensitivity to convective
inhibition. Both schemes to calculate subgrid orographic drag have been substantially modified.
Topographic orientation (ridges) and low-level flow blocking effects have been incorporated into the
orographic gravity wave scheme.  The previous parameterization of boundary layer form drag – turbulent
mountain stress (TMS) – has been replaced with the scheme of Beljaars et al. currently used in the
European Center forecast model.   In addition to these physics updates, new infrastructure for traceable
generation of topographic forcing files has been developed.

**Complete CAM6 scientific documentation is under development and is expected to be available by September 2018.**  

References
=============

.. bibliography:: refs.bib
