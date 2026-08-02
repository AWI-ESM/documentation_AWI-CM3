.. _chap_before_you_start:

****************
Before you start
****************

In order to run AWI-CM3 or AWI-ESM3 a few steps must be taken that are outlined here. Some of them are optional others are not.

Licencing
=========

Which of these apply to you depends on which components your setup contains. See :doc:`model_family` if you are not sure what you are running.

Every setup needs:

- **OpenIFS**: ensure that your research institute or university is in possession of a valid OpenIFS licence. The licence can be obtained from the European Centre for Medium-Range Weather Forecasts (ECMWF) free of charge, but will only be issued on an institutional basis, not to individuals. https://confluence.ecmwf.int/display/OIFS/Request+OpenIFS+license
- **FESOM2**: no action needed. The repository ships a GPL-3.0 text as ``LICENSE.txt`` and an LGPL-3.0 text as ``COPYING.LESSER.txt``, and states nowhere which of the two governs, so ask the FESOM2 developers if you need to be certain. https://github.com/FESOM/fesom2
- **OASIS3-MCT**: LGPL, no registration. http://www.cerfacs.fr/oa4web/oasis3-mct_4.0/oasis3mct_UserGuide/node5.html
- **XIOS**: CeCILL v2, no registration. AWI-CM3 v3.0 has no IO server, every later version does. http://forge.ipsl.jussieu.fr/ioserver/browser/XIOS/trunk/Licence.txt

AWI-ESM3 and both its variants add:

- **LPJ-GUESS**: Mozilla Public License 2.0, downloaded from Zenodo, with no agreement to sign. The developers ask that you notify them by email once you have it, so they can pass on updates and bug fixes. https://web.nateko.lu.se/lpj-guess/download.html

AWI-ESM3-is adds:

- **PISM**: GPL-3.0, no registration. https://github.com/pism/pism
- **dEBM**: MIT, no registration. https://github.com/ukrebska/dEBM

AWI-ESM3-cc adds:

- **REcoM**: carries no licence file at the time of writing, so ask the REcoM developers before redistributing anything built from it. https://github.com/RECOM-Regulated-Ecosystem-Model/REcoM

Repository registration
=======================
Since OpenIFS can not be distributed without lincence from the ECMWF, registration with https://gitlab.dkrz.de is required to obtain all required source code. Membership to the repositories can be granted by AWI staff (Jan.Streffing@awi.de, Paul.Gierz@awi.de, Christian.Stepanek@awi.de or Dmitry.Sidorenko@awi.de), provided you are a member of an `OpenIFS licenced institute <https://confluence.ecmwf.int/display/OIFS/OpenIFS+licensed+institutions>`_

Supported HPCs
==============
While the model can be run on a home computer, it is more commonly used on high performance computers. The model is currently supported on albedo@awi.de, levante@dkrz.de, juwels@fz-juelich.de, aleph@ipcc.kr, blogin@hlrn.de, glogin@hlrn.de. Simulations at other computing centers may require a bit more setup work (environment, library & compiler settings, download of inital & boundary conditions as well as meshes). To ensure that on your HPC system the library toolchain for AWI-CM3 and AWI-ESM3 is installed with the required options and library versions, we suggest to use: https://github.com/AWI-ESM/install_libs
