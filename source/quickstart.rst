.. _chap_quickstart

Step by step
************

1. Install esm_tools by following instructions at: https://esm-tools.readthedocs.io/en/latest/installation.html#esm-tools
2. Create folder ``~/model_codes``
3. In ``~/model_codes`` install AWI-CM3 with the command ``esm_master install-awicm3-v3.1``.
4. Go to the folder containing runscripts ``esm_tools/runscripts/awicm3/v3.1``. 
5. Modify one of the existing templates for your needs (e.g. change project name & folder).
6. Run a simulation by executing one of the run configurations in folder: ``esm_runscripts awicm3-v3.1-levante-TCO95L91-CORE2.yaml -e my_first_awicm3_run``
