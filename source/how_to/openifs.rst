*******
OpenIFS
*******

Change the number of OpenIFS processors between restarts
========================================================

OpenIFS restart files (``ICMSH``, ``ICMGG``, ``ICMGG INIUA``) are tied to the processor decomposition used when they were written. If you want to change the number of OpenIFS MPI tasks (``nproc``) between restarts, you need to regenerate the initial condition files from GRIB output using the ``oifs_grib_output_to_restart.sh`` script provided in ``esm_tools/configs/components/oifs/``.

Overview
--------

The procedure works by converting GRIB model output back into the initial condition file format that OpenIFS expects. These are not true restart files (some information is lost), but the result is close enough for most applications.

Prerequisites
-------------

- `ecCodes <https://confluence.ecmwf.int/display/ECC>`_ must be available (``module load eccodes`` on most HPC systems). The tools ``grib_copy`` and ``grib_filter`` are required.
- One day of GRIB output (not XIOS output) from the time step you want to restart from.

Step-by-step procedure
----------------------

1. **Produce GRIB output for the restart date.** Restart the model from existing restart files, but configure it to run for only one day and set ``LXIOS=false`` in the ``fort.4`` namelist. This forces OpenIFS to write classical GRIB output files (``ICMSH``, ``ICMGG``, ``ICMUA``) instead of going through XIOS. You can set this through the esm-tools runscript:

   .. code-block:: yaml

      oifs:
          add_namelist_changes:
              fort.4:
                  NAMCT0:
                      LXIOS: false

2. **Configure the conversion script.** Copy the script ``oifs_grib_output_to_restart.sh`` from ``esm_tools/configs/components/oifs/`` and edit the following variables at the top:

   .. code-block:: bash

      # Path to the workdir containing the GRIB output files
      indir="/path/to/workdir/with/grib/output/"
      # The EXPID used in the file names, e.g. ICMGG<EXPID>+YYYYMM
      expid="ECE3"
      # Date string in the GRIB file name, e.g. "197901" for Jan 1979
      indate="197901"
      # The exact date (YYYYMMDD) of the time step to extract
      # NOTE: There must be only one time step for this date in the file
      indate_cut="19790102"
      # Where the resulting initial condition files should be placed
      targetdir="/path/to/target/restart/directory/"
      # EXPID for the output files
      expid_tgt="ECE3"

3. **Run the script.** Execute the script on a login node or in an interactive session where ecCodes is available:

   .. code-block:: bash

      bash oifs_grib_output_to_restart.sh

   The script will:

   - Extract the selected date from the GRIB output using ``grib_copy``
   - Split the data by variable and level using ``grib_filter``
   - Reassemble the fields in the specific order OpenIFS expects for initial conditions
   - Produce three files: ``ICMGG<EXPID>INIT``, ``ICMGG<EXPID>INIUA``, and ``ICMSH<EXPID>INIT``

4. **Update the esm-tools runscript.** Change the number of OpenIFS processors to the desired value:

   .. code-block:: yaml

      oifs:
          nproc: <new_number_of_processors>

5. **Start the new simulation.** Place the generated ``ICM*`` files where esm-tools expects initial conditions and start the run with ``lresume: false`` (since these are initial condition files, not restart files). Make sure to set the correct start date matching the files you produced.

.. note::

   This procedure does not produce a true bit-reproducible restart. Small differences may occur compared to a continuous run, but results are physically consistent.

.. note::

   The script assumes 91 vertical model levels (L91) and the variable list of OpenIFS cy43r3. If you are using a different number of levels or cycle, you may need to adjust the level range and variable lists in the script.

Branch off from existing OpenIFS restart
========================================
In the esm_tools runscript yaml file, in the oifs section add:

.. code-block:: yaml

   oifs:
       lresume: true
       ini_restart_dir: "${general.ini_parent_dir}/restart/oifs/"
       ini_restart_exp_id: "${general.ini_parent_exp_id}"
       ini_restart_date: '1949-12-31T23:00:00'
       ini_pseudo_initial_date: "1949-12-01"
       prev_run_config_file: "${general.ini_parent_dir}/config/${general.ini_parent_exp_id}_finished_config.yaml_19491201-19491231"

Modify ``ini_restart_dir``, ``ini_restart_exp_id``, ``ini_restart_date``, ``ini_pseudo_initial_date``, and ``prev_run_config_file`` as needed for your use case. The ``ini_pseudo_initial_date`` should be set to one restart interval (e.g. 1 month or 1 year) before ``general.initial_date`` of the new experiment. This is used to trick OpenIFS into thinking it is always doing a short run, avoiding memory issues in long simulations.
