.. _chap_before_you_start

Before you start
****************

In order to run AWI-CM3 a few steps must be taken that will be outlined here. Some of them are optional others are not.

Licencing
=========
- OpenIFS must be licenced by ECMWF. The licence is free of charge but will only be issued to research institutes & Universities. https://confluence.ecmwf.int/display/OIFS/Request+OpenIFS+license
- FESOM2 is available under GPL-2.0 and requires no further action
- OASIS4 is available under LGPL and requires no registration http://www.cerfacs.fr/oa4web/oasis3-mct_4.0/oasis3mct_UserGuide/node5.html

Repository registration
=======================
Since OpenIFS can not be distributed freely registration with https://gitlab.dkrz.de is required to obtain all required source code. Membership to the repositories can be granted by AWI staff (Jan.Streffing@awi.de Christian.Stepanek@awi.de, Dirk.Barbi@awi.de or Dmitry.Sidorenko@awi.de), provided you are a member of an `OpenIFS licenced institute <https://confluence.ecmwf.int/display/OIFS/OpenIFS+licensed+institutions>`_

Supported HPCs
==============
While the model can be run on a home computer, typically it is used on a high performance computer. The model is currently supported on ollie@awi.de, mistral@dkrz.de, juwels@fz-juelich.de. Simulations at other computing centers may require a bit more setup work (environment & compiler settings, download of inital & boundary conditions as well as meshes)
