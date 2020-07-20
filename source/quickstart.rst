.. _chap_quickstart

Step by step
************
1. Download esm-master: git clone https://gitlab.dkrz.de/esm-tools-old-stuff/esm-master.git
2. Configure esm-master: cd esm-master; make
3. Check out the AWI-CM-3 tag: git checkout awicm-3-deck
4. Download esm-environment: make get-esm-environment
5. Download esm-runscripts: make get-esm-runscripts
6. Downlaod AWI-CM-3: make get-awicm-3.1
7. Compile AWI-CM-3: make comp-awicm-3.1
8. Go to runscripts folder: cd esm-runscripts/runscripts/awicm
9. Modify/create your runscript & namelists as needed.
10. Start your run with a 4-digit name: ./your_runscript -e NAME
