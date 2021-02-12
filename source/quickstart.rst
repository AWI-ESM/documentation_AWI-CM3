.. _chap_quickstart

Step by step
************

########################
esm_tools (python tools)
########################

TBA (changes too quickly till release 5.1 of esm_tools to include here)

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
