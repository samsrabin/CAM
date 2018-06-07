Physical Constants
==================

Following the American Meteorological Society convention, the model
uses the International System of Units (SI) (see August 1974 *Bulletin
of the American Meteorological Society*, **Vol. 55**, No. 8, pp.
926-930).


.. math::

   \begin{aligned}
   \begin{array}{lcll}
   a & = & 6.37122 \times 10^{6} \quad\mathrm{m} & \mathrm{ Radius \: of \: earth} \\
   g & = & 9.80616 \quad\mathrm{m \: s^{-2}} & \mathrm{ Acceleration \: due \: to \: gravity}\\
   \pi & = & 3.14159265358979323846 & \mathrm{Pi} \\
   t_s & = & 86164.0 \quad\mathrm{s} & \mathrm{ Earth's \: sidereal \: day}\\
   \Omega & = & 2*\pi/t_s \quad\mathrm{[s^{-1}]} & \mathrm{ Earth's \: angular \: velocity}\\
   \sigma_{B} & = & 5.67 \times 10^{-8} \quad\mathrm{W \: m^{-2} \: K^{-4}} & \mathrm{ Stefan-Boltzmann \: constant}\\
   k & = & 1.38065 \times 10^{-23} \quad\mathrm{J K^{-1}} & \mathrm{ Boltzmann \: constant}\\
   N & = & 6.02214 \times 10^{26} & \mathrm{Avogadro's \: number}\\
   R^* & = & k\,N \quad\mathrm{[J K^{-1}]} & \mathrm{ Universal \: gas \: constant}\\
   m_{air} & = & 28.966 \quad\mathrm{kg} & \mathrm{ Molecular \: weight \: of \: dry \: air}\\
   R & = & R^*/m_{air} \quad\mathrm{[J \: kg^{-1} \: K^{-1}]} & \mathrm{ Gas \: constant \: for \: dry \: air}\\
   m_{v} & = & 18.016 \quad\mathrm{kg} & \mathrm{ Molecular \: weight \: of \: water \: vapor}\\
   R_{v} & = & R^*/m_{v} \quad\mathrm{[J \: kg^{-1} \: K^{-1}]} & \mathrm{ Gas \: constant \: for \: water \: vapor}\\
   c_{p} & = & 1.00464 \times 10^{3} \quad\mathrm{J \: kg^{-1} \: K^{-1}} & \mathrm{ Specific \: heat \: of \: dry \: air \: at \: constant \: pressure}\\
   \kappa & = & 2/5 & \mathrm{Von \: Karman \: constant} \\
   z_{vir} & = & R_{v}/R-1 & \mathrm{Ratio \:of \:gas \:constants \:for \:water \:vapor \:and \:dry \:air} \\
   L_{v} & = & 2.501 \times 10^{6} \quad\mathrm{J \: kg^{-1}} & \mathrm{ Latent \: heat \: of \: vaporization}\\
   L_{i} & = & 3.337 \times 10^{5} \quad\mathrm{J \: kg^{-1}} & \mathrm{ Latent \: heat \: of \: fusion}\\
   \rho_{H_{2}O} & = & 1.0 \times 10^{3} \quad\mathrm{kg \: m^{-3}} & \mathrm{ Density \: of \: liquid \: water}\\
   c_{pv} & = & 1.81 \times 10^{3} \quad\mathrm{J \: kg^{-1} \: K^{-1}} & \mathrm{ Specific \:heat \: of \: water \: vapor \: at \: constant \: pressure}\\
   T_{melt} & = & 273.16 \quad\mathrm{^{\circ}K} & \mathrm{ Melting \: point \: of \: ice}\\
   p_{std} & = & 1.01325 \times 10^{5} \quad\mathrm{Pa} & \mathrm{ Standard \: pressure}\\
   \rho_{air} & = & p_{std}/(R\,T_{melt}) \quad\mathrm{[kg m^{-3}]} & \mathrm{ Density \: of \: dry \: air \: at \: standard \: pressure/temperature}
   \end{array}\end{aligned}

The model code defines these constants to the stated accuracy. We do
not mean to imply that these constants are known to this accuracy nor
that the low-order digits are significant to the physical
approximations employed.

Bibliography
============

.. bibliography:: refs.bib
