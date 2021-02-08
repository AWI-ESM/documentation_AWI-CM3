.. _chap_quickstart

Step by step
************

########################
esm_tools (python tools)
########################

1. Clone and install esm_tools (as in the `documentation <https://esm-tools.readthedocs.io/>`__)
2. In esm_tools package, checkout the feature/awicm3 branch (cd ~/esm_tools; git checkout feature/awicm3)
3. Clone the esm_runscripts package (for example, in your home directory: git clone https://github.com/esm-tools/esm_runscripts.git)
4. Checkout the feature/awicm3 branch in the esm_runscripts package (cd ~/esm_runscripts; git checkout feature/awicm3). Note that in the past, we used to checkout the develop branch, but because I don't want to interfere with the develop branch anymore, I created a feature/awicm3 branch also for esm_runscripts).
5. In esm_runscripts perform a local pip installation (cd ~/esm_runscripts; pip install -e .)

######################
esm-master (ksh tools)
######################

1. Log into one of the supported HPC systems: mistral, ollie or juwels
2. Download esm-master: git clone https://gitlab.dkrz.de/esm-tools-old-stuff/esm-master.git
3. Configure esm-master and enter your DKRZ user id: cd esm-master; make
4. Check out the AWI-CM-3 tag: git checkout awicm-3-deck
5. Download esm-environment: make get-esm-environment
6. Download esm-runscripts: make get-esm-runscripts
7. Downlaod AWI-CM-3: make get-awicm-3.1
8. Compile AWI-CM-3: make comp-awicm-3.1
9. Go to runscripts folder: cd esm-runscripts/runscripts/awicm
10. Modify/create your runscript & namelists as needed.
11. Start your run with a 4-digit name: ./your_runscript -e NAME
