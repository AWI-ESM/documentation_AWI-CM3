.. _chap_quickstart

Step by step
************

########################
esm_tools (python tools)
########################

1. Install esm_tools by following instructions at: https://esm-tools.readthedocs.io/en/latest/installation.html#esm-tools
2. Git check out the esm_tools branch awicm3-v3.0-release-candidate
3. Install AWI-CM3 with esm_master install-awicm3-v3.0. The default folder is ~/model_codes. Using the default folder will make your life easier.
4. Run a simulation by executing one of the run configurations in folder esm_tools/runscripts/awicm3/v3.0. For example: esm_runscripts awicm3-v3.0-ollie-TCO159L91-CORE2.yaml -e my_first_awicm3_run

##########################################
esm-master (ksh tools) (old & unsupported)
##########################################

1. Log into one of the supported HPC systems: mistral, ollie or juwels
2. Download esm-master: git clone https://gitlab.dkrz.de/esm-tools-old-stuff/esm-master.git
3. Configure esm-master and enter your DKRZ user id: cd esm-master; make
4. Check out the AWI-CM3 tag: git checkout awicm-3-deck
5. Download esm-environment: make get-esm-environment
6. Download esm-runscripts: make get-esm-runscripts
7. Downlaod AWI-CM3: make get-awicm-3.1
8. Compile AWI-CM3: make comp-awicm-3.1
9. Go to runscripts folder: cd esm-runscripts/runscripts/awicm
10. Modify/create your runscript & namelists as needed.
11. Start your run with a 4-digit name: ./your_runscript -e NAME
