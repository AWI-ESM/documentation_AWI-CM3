.. _chap_before_you_start

Before you start
****************

In order to run AWI-CM3 a few steps must be taken that are outlined here. Some of them are optional others are not.

Licencing
=========
- Ensure that your research institute or university is in possession of a valid OpenIFS licence. The licence can be obtained from the European Centre for Medium-Range Weather Forecasts (ECMWF) free of charge, but will only be issued to on an institutional basis, not to individuals. https://confluence.ecmwf.int/display/OIFS/Request+OpenIFS+license
- FESOM2 is available under GPL-2.0 and requires no further action https://github.com/FESOM/fesom2/blob/master/LICENSE.txt
- OASIS4 is available under LGPL and requires no registration http://www.cerfacs.fr/oa4web/oasis3-mct_4.0/oasis3mct_UserGuide/node5.html
- XIOS is available under CeCILL_V2 and requires no registration http://forge.ipsl.jussieu.fr/ioserver/browser/XIOS/trunk/Licence.txt

Repository registration
=======================
Since OpenIFS can not be distributed without lincence from the ECMWF, registration with https://gitlab.dkrz.de is required to obtain all required source code. Membership to the repositories can be granted by AWI staff (Jan.Streffing@awi.de, Paul.Gierz@awi.de, Christian.Stepanek@awi.de or Dmitry.Sidorenko@awi.de), provided you are a member of an `OpenIFS licenced institute <https://confluence.ecmwf.int/display/OIFS/OpenIFS+licensed+institutions>`_

Supported HPCs
==============
While the model can be run on a home computer, it is more commonly used on high performance computers. The model is currently supported on albedo@awi.de, levante@dkrz.de, juwels@fz-juelich.de, aleph@ipcc.kr, blogin@hlrn.de, glogin@hlrn.de. Simulations at other computing centers may require a bit more setup work (environment, library & compiler settings, download of inital & boundary conditions as well as meshes). To ensure that on your HPC system the library toolchain for AWI-CM3 is installed with the required options and library versions, we suggest to use: https://github.com/AWI-CM3/install_libs
