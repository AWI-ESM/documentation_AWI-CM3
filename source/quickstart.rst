.. _chap_quickstart:

************
Step by step
************

1. Install esm_tools by following instructions at: https://esm-tools.readthedocs.io/en/latest/installation.html#esm-tools
2. Create folder ``~/model_codes``
3. In ``~/model_codes`` install the model with ``esm_master install-awicm3-v3.4.0``, or the target for whichever setup you want. :doc:`model_family` lists them all.
4. Go to the folder containing runscripts ``esm_tools/runscripts/awicm3/v3.4.0``.
5. Modify one of the existing templates for your needs (e.g. change project name & folder).
6. Run a simulation by executing ``esm_runscripts awicm3-v3.4.0-levante-TCO95L91-CORE2_1d.yaml -e my_first_awicm3_run``

AWI-ESM3 works the same way, with ``awiesm3`` in place of ``awicm3`` in both the install target and the runscript path.

Not every installable version ships runscripts of its own. AWI-CM3 ``v3.4.1`` and ``v3.4.2`` install but have no runscript folder, so start from the ``v3.4.0`` ones and change the version in the yaml. AWI-ESM3 has a folder for each of the three.

AWI-ESM3-cc
===========

Install ``awiesm3-develop-cc``. It has no runscript folder yet either, so take one from ``esm_tools/runscripts/awiesm3/develop/`` and set ``version: develop-cc`` in it. Dedicated runscripts arrive with v3.5.0.

AWI-ESM3-is
===========

Install ``awiesm3-develop-is``. Starting a run here is not one runscript and one command, because PISM is coupled iteratively and runs as its own chain. You launch a driver runscript, which names the AWI-ESM3 and PISM runscripts as its ``model1`` and ``model2``:

.. code-block:: bash

   esm_runscripts spinup_couplePI_core3_concurrent.yaml -e <experiment_id> --coupling-chain all

The same command starts, restarts and recovers the run. ``--coupling-chain awiesm3`` or ``--coupling-chain pism`` drives one chain on its own, which is what you want when only one of the two needs redoing. The runscripts live in ``esm_tools/runscripts/awiesm3/develop-is/``.
