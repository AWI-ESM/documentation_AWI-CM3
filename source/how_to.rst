.. _how_to

How to
******

Cite this model
=========

Streffing, J., Sidorenko, D., Semmler, T., Zampieri, L., Scholz, P., Andres-Martinez, M., . . . Jung, T. (2022). AWI-CM3 coupled climate model: description and evaluation experiments for a prototype post-CMIP6 model. Geoscientific Model Development, 15 (16), 6399–6427. Retrieved from https://gmd.copernicus.org/articles/15/6399/2022/ doi: 10.5194/gmd-15-6399-2022


Measure which component is limiting the throughput of the coupled model
=========

Coupled performance balancing can be performed with the oasis lucia tool. In the work folder where your experiment ran, execute ``$(model_install_dir)/awicm-3.1/oasis/util/lucia/lucia``. When executing lucia for the first time, a fortran compiler needs to be available in the environment. 
The output,
   
..  code-block:: bash
  
  Component -         Calculations   -     Waiting time (s) - # cpl step :
  fesom                    1616.47                 45.08          4377
  oifs                     1263.30                397.72          4377
 
..
  
can be interpreted as such. Fesom spend nearly all it's computing time on calculations, while oifs was waiting for about 1/4 of the time. Therefore fesom was the   limiting factor on this specific setup. Take note, that having zero waiting time in all components is no achievable, since the length of timesteps varies throughout the run, depending on output and called physics packages. For example the radiation is called every 2 hours in OpenIFS making this timesteps longer than the non-radiation ones in between. Modern versions of lucia also provide solutions for optimizing with this imbalance in mind.

Change the number of OpenIFS processors between restarts
=========

OpenIFS restart files (``ICMSH``, ``ICMGG``, ``ICMGG INIUA``) are tied to the processor decomposition used when they were written. If you want to change the number of OpenIFS MPI tasks (``nproc``) between restarts, you need to regenerate the initial condition files from GRIB output using the ``oifs_grib_output_to_restart.sh`` script provided in ``esm_tools/configs/components/oifs/``.

Overview
--------

The procedure works by converting GRIB model output back into the initial condition file format that OpenIFS expects. These are not true restart files (some information is lost), but the result is close enough for most applications.

Prerequisites
--------

- `ecCodes <https://confluence.ecmwf.int/display/ECC>`_ must be available (``module load eccodes`` on most HPC systems). The tools ``grib_copy`` and ``grib_filter`` are required.
- One day of GRIB output (not XIOS output) from the time step you want to restart from.

Step-by-step procedure
--------

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


Generate OASIS3MCT remapping weights for large grids (offline and MPI+OMP parallel)
=========

This section is about generating ``rmp_`` files from scratch, for a grid pair that has none. If what you actually want is the same grid pair at a different FESOM2 core count, and you already hold a working set of ``rmp_`` files for some other core count, skip all of this and see :ref:`oasis_reorder` instead. It does the same job in seconds.

Before you start, make sure that you:
 
- Obtain the FESOM2 mesh and generate the mesh distribution you would like to use.
- Use the `ocp-tool <https://github.com/AWI-ESM/ocp-tool2/>`_  to match the FESOM2 mesh to the atmosphere files (really just means cutting caspian out of the OIFS land sea mask)
- Copy the ocp-tool modified OpenIFS input files, as well as the Oasis input files (areas.nc, grids.nc, masks.nc) and the runoff_mapper input files into the sub-directories of the pool dir that you use.

Steps towards the ``rmp_`` files:

- Generate FESOM2 mesh description file with `SpheRlab <https://github.com/FESOM/spheRlab>`_
- Link SpheRlab grid description file into ocp-tool2/fesom_mesh
- Link OpenIFS ICMGG????INIT files into ocp-tools2/openifs_input_default
- Run prep_fesom.sh
- Install / load ocp-tools conda environment
- Configure and run ocp_tool.py
- Copy files from ``ocp-tool2/output/oasis3_mct/input`` and ``ocp-tool2/output/openifs_input_modfied`` back into the pool directories
- Start a coupled simulation with the desired FESOM2 mesh ``dist``. OIFS ``nproc`` may be as small as minimum memory for loading the grid demands.
- Wait until the FESOM2 mesh information was added to the ``areas.nc, grids.nc, masks.nc`` files.
- Wait until the BICUBIC remapping files have been generated. (they are much fast than the GAUSWGT ones, and this will cut the manual work in half later)

For small meshes you can also wait for the GAUSWGT remapping files to be created. For large meshes follow the next steps. This method is meant for Atmosphere-Ocean grid combinations in excess of ~1*10^12, where automatic weight generation on single cores becomes prohibitively time consuming. 

- Cancel the job allocation since generating the GAUSWGT ``rmp_`` files would take days to months.
- Change the COUPLE path in ``awicm-3.1/oasis/util/make_dir/make.${your_config}_``
- Set the path to ${your_config} in ``awicm-3.1/oasis/util/make_dir/make.inc_``
- Go to ``awicm-3.1/oasis/examples/test_interpolation``
- Add your ``areas.nc, grids.nc, masks.nc`` files to ``awicm-3.1/oasis/examples/test_interpolation/data_frontiers``
- Modify the ``awicm-3.1/oasis/examples/test_interpolation/run_frontiersinterp.sh`` to add your machine, if it's not included already.
- Extract the ``GAUSWGT`` couplings (FESOM->OIFS) from the namcouple in your work folder where you generated the ``BICUBIC`` ``rmp_`` files.
- Create one namcouple for every remapping in direction at ``awicm-3.1/oasis/examples/test_interpolation/data_frontiers`` For an example, see: ``awicm-3.1/oasis/examples/test_interpolation/data_frontiers/namcouple_feom_A160_gauswgt``
- Configure `awicm-3.1/oasis/examples/test_interpolation/run_frontiersinterp.sh` to generate these remappings with MPI and OpenMP parallelization.
- Generate the GAUSWGT remappings by starting ``run_frontiersinterp.sh`` on the batch queue.
- Copy all ``rmp_`` files into the respective pool dir folder (e.g. ``input/oasis/cy43r3/{OIFS_RES}-${FESOM_RES}/${FESOM_DIST}``).
- Start a day long coupled simulation with oasis ``lresume=false`` to generate oasis restart files
- Copy oasis restart files into pool dir
- Start full speed simulation with oasis ``lresume=true`` to generate oasis restart files


.. _oasis_reorder:

Reorder existing OASIS3MCT files for a different FESOM2 core count
==================================================================

The ``rmp_`` weight files and the OASIS restart files (``rstos``, ``rstas``) depend on the FESOM2 mesh partition, because the FESOM2 side of the coupling is addressed in PE contiguous order: the global nodes are listed rank by rank, in the order the partitioner assigned them. Change the ``dist`` and the addressing changes with it, even though the mesh, the atmosphere grid and the weight values themselves are all unchanged.

Regenerating the weights for the new core count is what the previous section describes, and on a large grid it costs hours to months of compute plus a fair amount of manual work. You only have to pay that once per grid pair. If you already have a working set of files for any FESOM2 core count on the same grid pair, the `oasis_reorder_tool <https://github.com/AWI-ESM/oasis_reorder_tool>`_ permutes the files you have into the ordering of the new partition instead. For the 3.1 million node ``dars2`` mesh, about 5 GB of NetCDF, that takes five to ten seconds.

The tool never computes a weight. It only rearranges values that are already in the files, so it can move you between core counts but not onto a new grid pair. See :ref:`oasis_reorder_limits` before you plan around it.

How it works
------------

Every FESOM2 mesh partition directory contains an ``rpart.out`` that maps global nodes onto ranks. Reading ``dist_OLD/rpart.out`` and ``dist_NEW/rpart.out`` gives, for each natural global node, its position in the old and in the new PE contiguous ordering. Composing the two yields the permutation, which is then applied file by file:

- In the ``rmp_`` files the ``src_address`` and ``dst_address`` integers are remapped value by value, but only where the matching ``*_grid_size`` equals ``nod2D``, that is, only on the FESOM2 side of the coupling. The remapping weights themselves are not touched.
- Any other variable that has a dimension of size ``nod2D``, the OASIS restarts for example, is permuted along that dimension. Both 1D and 2D variables are handled.
- Everything else is copied unchanged.

The file list is discovered at runtime and is fixed: ``rmp_*.nc``, ``rstos.nc``, ``rstos.nc_recv``, ``rstas.nc``, ``rstas.nc_recv`` and ``vegin.nc``. The ``rmp_`` glob is resolution and map agnostic, so it matches any grid names and any interpolation suffix (``GAUSWGT``, ``GAUSWGT_25``, ``BICUBIC``). Entries that do not exist in the input directory are skipped silently, and anything in the input directory that is not on the list is neither reordered nor copied.

Build
-----

The tool is a single Fortran source file using MPI and OpenMP, and NetCDF-Fortran is its only dependency, so moving it to another machine is a matter of swapping the modules. The build takes a couple of seconds. On levante:

.. code-block:: bash

   git clone https://github.com/AWI-ESM/oasis_reorder_tool
   cd oasis_reorder_tool
   module load intel-oneapi-compilers/2023.2.1-gcc-11.2.0
   module load intel-oneapi-mpi/2021.5.0-intel-2021.5.0
   module load netcdf-fortran/4.5.3-intel-oneapi-mpi-2021.5.0-intel-2021.5.0
   make

If you build it elsewhere, keep the ``-heap-arrays 64`` that the ``Makefile`` sets and run with ``ulimit -s unlimited``. Without both, NetCDF-Fortran is handed compiler generated stack temporaries that overflow and ``nf90_get_var`` segfaults, but only once the mesh reaches a few million nodes, so a small test mesh will not show it to you.

Run
---

Set the four paths at the top of ``submit.sh``:

.. code-block:: bash

   DIST_OLD=/work/ab0246/a270092/input/fesom2/dars2/dist_5120
   DIST_NEW=/work/ab0246/a270092/input/fesom2/dars2/dist_2560
   OASIS_IN=/work/ab0246/a270092/input/oasis/cy48r1/TCO319-DARS2/5120
   OASIS_OUT=/work/ab0246/a270092/input/oasis/cy48r1/TCO319-DARS2/2560

``DIST_OLD`` and ``DIST_NEW`` are the FESOM2 mesh partition directories, ``OASIS_IN`` is the pool directory holding the files you already have, and ``OASIS_OUT`` is where the reordered set is written. Set ``--account`` and ``--chdir`` to your own project and working directory as well, then submit:

.. code-block:: bash

   sbatch submit.sh

``run.sh`` carries the same launch logic for an interactive shell. Besides the paths, ``submit.sh`` also carries ``srun --mpi=pmi2`` and ``I_MPI_PMI_LIBRARY``, which is what levante needs to launch this binary at all, and ``--chdir``, without which ``srun`` execs from the spool directory and does not find it. The repository README explains each. Change only the paths unless you are on another machine. Afterwards point the experiment at ``OASIS_OUT`` and run with the new ``dist``.

A successful run reports the node count it deduced and the number of files it found, and then says nothing else:

.. code-block:: bash

  [rank 0] reading <DIST_OLD>/rpart.out
  [rank 0] reading <DIST_NEW>/rpart.out
  [rank 0] nod2D = <surface nodes>
  [rank 0] remap built (<seconds> s)
  [rank 0] processing <n> files round-robin across ranks

Check the node count against your mesh, and check the file count. There are two ways the setup can be wrong that the tool catches itself, both fatal:

.. code-block:: bash

  ERROR: nod2D mismatch between rpart.out files:   <old>   <new>
  ERROR: remap permutation is invalid

The first means ``DIST_OLD`` and ``DIST_NEW`` are partitions of different meshes. The second means an ``rpart.out`` is not a permutation of the global nodes, in practice a truncated or half written partition file. A file count of ``0`` is neither fatal nor reported as an error, so if the job finishes instantly, read that line: it means ``OASIS_IN`` held nothing the tool recognises, and ``OASIS_OUT`` is empty.

Check that it really worked
---------------------------

A reordered file cannot be compared byte by byte against an independently generated one, because reordering and a fresh SCRIP run differ both in file metadata and in floating point rounding. What has to hold instead is that every variable in the output contains exactly the same set of values as the input, only permuted. Comparing sorted hashes tests that:

.. code-block:: python

   import numpy as np, hashlib
   from netCDF4 import Dataset

   def vh(ds, vn):
       a = np.asarray(ds.variables[vn][...]).ravel()
       return hashlib.sha256(np.sort(a).tobytes()).hexdigest()[:16]

   a, b = Dataset(IN), Dataset(OUT)
   for vn in sorted(set(a.variables) & set(b.variables)):
       print(vn, vh(a, vn) == vh(b, vn))

For the ``dars2`` mesh this passes on all 7 variables of ``rstos.nc`` and all 19 of ``rmp_A320_to_feom_BICUBIC.nc``. A run that starts is not proof that the reordering was right: a wrong permutation gives you a model that couples happily and exchanges fluxes between the wrong points, which you will only notice in the fields.

.. _oasis_reorder_limits:

What the tool does not do
-------------------------

- It does not generate weights. Without an existing ``rmp_`` set for the same grid pair there is nothing to permute, and you are back to the offline generation in the previous section, or to a low resolution run that generates the weights on the fly.
- It does not help across a grid change. A new FESOM2 mesh or a new OpenIFS resolution is a new grid pair, even if the file names look familiar.
- It does not leave you a complete pool directory. ``areas.nc``, ``grids.nc``, ``masks.nc`` and everything else outside the file list are not copied into ``OASIS_OUT`` at all, so check what actually landed there and bring the rest over yourself. Those three do not depend on the FESOM2 core count, so the existing ones can be reused as they are.
- It does not check that the ``rmp_`` files you gave it belong to ``DIST_OLD``. The two ``rpart.out`` files are checked against each other, but nothing ties either of them to the contents of ``OASIS_IN``. Feed it weights from a different partition and it will happily write a wrongly permuted set. Keep the pool directories named after their core count, as in the paths above.


Select an SSP or RCP scenario
=========
CMIP6
---------
Control is possible through the namelist file fort.4. Inside you will find the namelist NAERAD, which contains the options for CMIP5 and CMIP6 greenhouse gas forcing. To activate CMIP6 forcing set the logic switch ``LCMIP6 = .true.``. When NCMIPFIXYR is set to a value >0, it is interpreted as a fix forcing year. In the example below we use constant 1850 GHG forcing. If NCMIPFIXYR=0 the actual model year is used, and forcing changes from year to year. Note, that currently only greenhouse gases and solar radiation are set through this namelist. Work on the implementation of controllable anthopogenic aerosols is still ongoing (status: 30th of June 2022).

The recommended way to ensure the namelist changes are made conistently, is to use the `add_namelist_changes <https://esm-tools.readthedocs.io/en/latest/cookbook.html?highlight=add_namelist_changes#changing-namelist-entries-from-the-runscript>`_ from esm-tools.

.. code-block:: Fortran
   
   &NAERAD
      LCMIP6 = .true.
      CMIP6DATADIR = 'PATH_TO_CMIP6_POOL'
      NCMIPFIXYR = 1850
      SSPNAME = 'historical'
      
Historic forcing is available for the years 1850 to 2014.
      
.. code-block:: Fortran
   
   &NAERAD
      LCMIP6 = .true.
      CMIP6DATADIR = 'PATH_TO_CMIP6_POOL'
      NCMIPFIXYR = 0
      SSPNAME = 'historical'
      
Available SSPs are: ``SSP1-1.9``, ``SSP1-2.6``, ``SSP2-4.5``, ``SSP3-7.0``, ``SSP3-LowNTCF``, ``SSP4-3.4``, ``SSP4-6.0``, ``SSP4-6.0``, ``SSP5-3.4-OS``, ``SSP5-8.5``. Covered years are 2015 to 2100.

.. code-block:: Fortran
   
   &NAERAD
      LCMIP6 = .true.
      CMIP6DATADIR = 'PATH_TO_CMIP6_POOL'
      NCMIPFIXYR = 0
      SSPNAME = 'SSP3-7.0'

The model also supports one percent increase per year and sudden four times incease of CO2 experiments through the additional logic switches ``L1PCTCO2`` and ``LA4XCO2``. The base value from which the the increase starts is set via ``NCMIPFIXYR``.

.. code-block:: Fortran
   
   &NAERAD
      LCMIP6 = .true.
      CMIP6DATADIR = 'PATH_TO_CMIP6_POOL'
      NCMIPFIXYR = 1850
      SSPNAME = 'historical'
      L1PCTCO2 = 'true'
      
For a more detailed look at the use of these forcing consult the source code file ``src/ifs/climate/updrgas.F90``

CMIP5
--------
Control is analogous to CMIP6 but we use ``LCMIP5``, ``CMIP5DATADIR``, and ``NRCP`` instead. Avaiable RCP are: 

.. code-block:: Fortran

    SELECT CASE (NRCP)
    CASE (0)
      FILENAME='ghg_histo.txt'
    CASE (1)
      FILENAME='ghg_rcp3PD.txt'
    CASE (2)
      FILENAME='ghg_rcp45.txt'
    CASE (3)
      FILENAME='ghg_rcp60.txt'
    CASE (4)
      FILENAME='ghg_rcp85.txt'

For a more detailed look at the use of these forcing consult the source code file ``src/ifs/climate/updrgas.F90``

Branch off from existing FESOM2 restart
=========
In the esm_tools runscript yaml file, in the fesom section add:

.. code-block:: yaml

   fesom:
       lresume: true
       ini_parent_exp_id: "sp1950c"
       ini_parent_date: "${prev_date}"
       ini_restart_dir: "/work/ab0995/a270210/runtime/awicm3-v3.1_refactoring/TCO95L91-CORE2/sp1950c/restart/fesom"
       choose_general.run_number:
           1:
               lasttime:
                   85200
               restart_in_sources:
                   par_oce_restart: /${ini_restart_dir}/fesom.1949.oce.restart/*.nc
                   par_ice_restart: /${ini_restart_dir}/fesom.1949.ice.restart/*.nc

Modify ``ini_parent_exp_id``, ``ini_parent_date``, ``ini_restart_dir``, ``par_oce_restart``, and ``par_ice_restart`` as needed for your use case. The variable ``lasttime`` is only needed when the FESOM2 timestep has changed between the old and new experiments. This could for example be the case for a spinup from a coldstart on medium and high resolution meshes. If you want to set ``lasttime``, you can find the correct value to set it to, as the first number in the fesom.clock file of the previous experiment (e.g. <path-to-previous-experiment>/config/fesom/fesom.clock):

.. code-block:: yaml

   85200 365 1949
   0.0000000000000 1 1950

Branch off from existing LPJGuess restart
=========
In the esm_tools runscript yaml file, in the lpj_guess: section add:

.. code-block:: yaml
    ini_parent_exp_id: "AWIESM3_NTest309_Spinup_NoNlimitation_NoPatchdisturbances"
    ini_parent_date: "${prev_date}"
    ini_restart_dir: "/work/bb1469/a270270/runtime/awiesm3-v3.4/AWIESM3_NTest309_Spinup_NoNlimitation_NoPatchdisturbances/restart/lpj_guess"
    choose_general.run_number:
        1:
            restart_in_sources:
                state: /${ini_restart_dir}/lpjg_state_2037/*
            restart_out_in_work:
                state: /${work_dir}/lpjg_state_$(date -u -d "${initial_date}" +%Y)/*

Modify ``ini_parent_exp_id``, ``ini_parent_date``, ``ini_restart_dir``, and ``state`` as needed for your use case.

Branch off from existing OpenIFS restart
=========
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

Control Aerosol Scaling (AWI-CM3 v3.2 and v3.3)
=========
Aerosol Scaling is a feature only available in AWI-CM3 v3.2 and above. For older versions it is not implemented (effectively deactivated). It is controlled via the ``fort.4`` namelist parameter ``NAERANT_SCALE`` in the ``NAERAD`` namelist. By default it is set to ``1`` (activated). If activated, the default aerosol levels (which have an annual cycle that does not change over the years) are scaled according to the spatio-temporal field given in ``ifsdata/aerosol_scale_1850_2085_r2005.nc``. This is supposed to model the anthropogenic influence on aerosol levels over time. For running paleo-simulations one might want to deactivate this. This is best done via an entry in the esm-tools runscript:

.. code-block:: yaml

   oifs:
       add_namelist_changes:
           fort.4:
               NAERAD:
                   NAERANT_SCALE: 0

For a more detailed look, consult the source code files, e.g. ``src/ifs/phys_ec/su_aer_scalefactor.F90``

Change the number of vertical levels for pressure level output of OpenIFS
=========
Output in controlled via `XIOS <https://forge.ipsl.jussieu.fr/ioserver>`_. The pressure levels onto which the data is interpolated from model levels is set in ``axis_def.xml``. In principle two options exist. Changing the number of levels for all 3D pressue level output fields and changing the number of levels only for some output fields.

For all fields
---------

To change the number of layers for all 3D pressure level fields, in ``axis_def.xml`` in section ``<axis_group id="pl_axes" ...>``
modify ``n_glo="19"`` to the new number of layers, ``value="(0,18)`` to 0 nlayers-1 and subequently list the pressure levels in Pa.

For select fields
---------

For selective fitting, in the ``<axis id="pressure_levels_zoom"`` section, you can make a sub-selection of the levels previously defined in the ``<axis id="pressure_levels"`` section. In the existing example three layers are selected: ``<zoom_axis index="(0,2)[10 11 12]" />``. To write a field on this reduced vertical domain you have to define a new grid in ``grid_def.xml``, specifying as domain ``pressure_levels_zoom`` instead of ``pressure_levels``. With this new grid you go to ``file_def.xml`` and define a new file (copy paste from ``pressure level`` output to ``pressure level output zoom``, and select the new grid). Then you delete the variables that should not be written on all levels from the pressure level output and insert them at pressure level output zoom.

.. _orbital_parameters:

Control orbital parameters
=========

The orbital parameters (eccentricity, obliquity, and longitude of perihelion) can be controlled through the namelist ``NAMORB`` inside the ``fort.4`` file. For details of the implementation, consider looking at yomorb.F90 and su0phy.F90.  Controllable orbital parameters are turned on with the logic switch: ``LCORBMD=true``, which is turned off by default. There are then three modes with which the orbital parameters can be controlled.

- Under ``ORBMODE=variable_year`` mode the orbital parameters are calculated according to Berger et al. 1978 for the current year of the simulation. This is the default. The calculation can be considered reliable within ~+-1 million years of the present.
- Under ``ORBMODE=fixed_year`` mode the orbital parameters are calculated according to Berger et al. 1978 for the fixed year set by the namelist variable ``ORBIY``. If you choose fixed year but set no year, the default is 1950.
- Under ``fixed_parameters`` you have manual control over the parameters ``ORBECCEN``, ``ORBOBLIQ`` and ``ORBMVELP``. If you choose fixed parameters but set no parameters, the default ones are for 1950.

Example for manual control:

.. code-block:: Fortran

   &NAMORB
      LCORBMD = true
      ORBMODE = 'fixed_parameters'
      ORBECCEN = 0.016715
      ORBOBLIQ = 23.4441
      ORBMVELP = 102.7
      

In order to have esm-tools create an openIFS namelist of that form one can adjust the simulation YAML. The following example would let openIFS compute top of the atmosphere insolation based on an LIG orbit whose parameters are as defined for PMIP4:

.. code-block:: yaml

   oifs:
       add_namelist_changes:
           fort.4:
               NAMORB:
                   LCORBMD: TRUE
                   ORBMODE: 'fixed_parameters'
                   ORBECCEN: 0.039378
                   ORBOBLIQ: 24.040
                   ORBMVELP: 275.41

The resulting anomaly of top of the atmosphere insolation shows the expected anomalies across latitudes over time:

.. image:: releases/3.1/insolation_anomaly_LIG-PI_openIFS.png
   :width: 600

Comparison of PI (1850) insolation for various relevant models
---------------------------------------------------------------
Differences between ECHAM6 and openIFS generated insolation can be deemed negligibly small. There is an overall offset of both ECHAM6 and openIFS with respect to the insolation computed from the PMIP4 PI orbit settings - that question may deserve further investigation. Note that ECHAM6 computes their modern insolation based on an internal orbit solution, i.e. the orbital parameters are never explicitly provided to the model as a forcing.

.. figure:: releases/3.1/insolation_absolute_PI_PMIP4.png
   :width: 600

   Insolation based on PMIP4 orbital parameters, computed based on climlab.

.. figure:: releases/3.1/insolation_absolute_PI_openIFS.png
   :width: 600

   OpenIFS computed PI insolation, monthly means.

.. figure:: releases/3.1/insolation_absolute_PI_ECHAM6_daily.png
   :width: 600

   ECHAM6 computed PI insolation, daily means.

.. figure:: releases/3.1/insolation_absolute_PI_ECHAM6_monthly.png
   :width: 600

   ECHAM6 computed PI insolation, monthly means, interpolated to openIFS grid.

.. figure:: releases/3.1/insolation_anomaly_PI_openIFS-ECHAM6_monthly.png
   :width: 600

   Anomaly of PI insolation, openIFS minus ECHAM6.

Files towards generation of the plots above are available in ``source/releases/3.1/``.


Use debug flags
=========

In case your model setup produces a segmentation fault it can be helpful to compile and run the model with debug flags. These can be set separatly for different executables in the coupled system. Here we mostly point you towards the locations that need to be modified in order to use debug flags. A comprehensive overview on which flags might help can be found at: https://doku.lrz.de/comparison-of-compiler-options-intel-vs-pgi-vs-gcc-11481685.html#ComparisonofCompilerOptions(intelvs.pgivs.gcc)-Diagnostics,RuntimeCheckingandDebugging

OpenIFS cy43r3 (AWI-CM3 v3.2 and below)
--------
You can replace the OpenIFS Fortran compile and linker flags through esm_tools under ``esm_tools/configs/components/oifs/oifs.env.yaml`` by modifying ``OIFS_FFLAGS``. E.g:

.. code-block:: yaml

   oifs:
      compiletime_environment_changes:
         levante:
            add_export_vars:
               OIFS_FFLAGS: '"-r8 -fp-model precise -align array32byte -O3 -qopenmp -g -traceback -convert big_endian -march=core-avx2 -mtune=core-avx2"'

Make sure you pick the right HPC system and use flags that fit to the compiler which is being used (see compiletime log output).


OpenIFS cy48r1 (AWI-CM3 v3.3 and above)
--------
TBA.


for FESOM2
--------
For FESOM2 it is currenty neccessary to modify the compiler settings in the source code folder inside the file ``awicm3-v3.2/fesom-2.5/src/CMakeLists.txt``. The exact path my vary with your model version. You will find inside a block with different FORTRAN flags depending on compiler ``Inter/GNU/Cray/NVHPC``, on whether FESOM2 is build as a library or executable, and sometimes on HPC system:

.. code-block:: CMake

   if(${CMAKE_Fortran_COMPILER_ID} STREQUAL  Intel )
      if(${BUILD_FESOM_AS_LIBRARY})
           target_compile_options(${PROJECT_NAME} PRIVATE -r8 -i4 -fp-model precise -no-prec-div -no-prec-sqrt -fimf-use-svml -xHost -ip -init=zero -no-wrap-margin -fpe0) # add -fpe0 for RAPS environment
      else()
           target_compile_options(${PROJECT_NAME} PRIVATE -r8 -i4 -fp-model precise -no-prec-div -no-prec-sqrt -fimf-use-svml -ip -init=zero -no-wrap-margin)
      endif()
      if(${FESOM_PLATFORM_STRATEGY} STREQUAL  levante.dkrz.de )
         target_compile_options(${PROJECT_NAME} PRIVATE -march=core-avx2 -mtune=core-avx2)
      elseif(${FESOM_PLATFORM_STRATEGY} STREQUAL  albedo)
         target_compile_options(${PROJECT_NAME} PRIVATE -march=core-avx2 -O3 -ip -fPIC -qopt-malloc-options=2 -qopt-prefetch=5 -unroll-aggressive) #NEC mpi option
      else()
         target_compile_options(${PROJECT_NAME} PRIVATE -xHost)
      endif()
   #    target_compile_options(${PROJECT_NAME} PRIVATE -g -traceback ) #-check all,noarg_temp_created,bounds,uninit ) #-ftrapuv ) #-init=zero)
   #    target_compile_options(${PROJECT_NAME} PRIVATE -qopenmp -r8 -i4 -fp-model precise -no-prec-div -no-prec-sqrt -fimf-use-svml -xHost -ip -g -traceback -check all,noarg_temp_created,bounds,uninit ) #-ftrapuv ) #-init=zero)
   #    target_compile_options(${PROJECT_NAME} PRIVATE -r8 -i4 -fp-model precise -no-prec-div -no-prec-sqrt -fimf-use-svml -ip -g -traceback -check all,noarg_temp_created,bounds,uninit ) #-ftrapuv ) #-init=zero)
   
   elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL  GNU )
   #    target_compile_options(${PROJECT_NAME} PRIVATE -O3 -finit-local-zero  -finline-functions -fimplicit-none  -fdefault-real-8 -ffree-line-length-none)
      target_compile_options(${PROJECT_NAME} PRIVATE -O2 -g -ffloat-store -finit-local-zero  -finline-functions -fimplicit-none  -fdefault-real-8 -ffree-line-length-none)
      if(CMAKE_Fortran_COMPILER_VERSION VERSION_GREATER_EQUAL 10 )
         target_compile_options(${PROJECT_NAME} PRIVATE -fallow-argument-mismatch) # gfortran v10 is strict about erroneous API calls: "Rank mismatch between actual argument at (1) and actual argument at (2) (scalar and rank-1)"
      endif()
   elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL Cray )
      if(${ENABLE_OPENMP})
         target_compile_options(${PROJECT_NAME} PRIVATE -c -emf -hbyteswapio -hflex_mp=conservative -hfp1 -hadd_paren -Ounroll0 -hipa0 -r am -s real64 -N 1023 -homp)
      else()
         target_compile_options(${PROJECT_NAME} PRIVATE -c -emf -hbyteswapio -hflex_mp=conservative -hfp1 -hadd_paren -Ounroll0 -hipa0 -r am -s real64 -N 1023 -hnoomp)
      endif()
   elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL NVHPC )
      target_compile_definitions(${PROJECT_NAME} PRIVATE ENABLE_NVHPC_WORKAROUNDS)
      target_compile_options(${PROJECT_NAME} PRIVATE -fast -fastsse -O3 -Mallocatable=95 -Mr8 -pgf90libs)
      if(${ENABLE_OPENACC})
         # additional compiler settings
         target_compile_options(${PROJECT_NAME} PRIVATE -acc -ta=tesla:${NV_GPU_ARCH} -Minfo=accel)
         set(CMAKE_EXE_LINKER_FLAGS "-acc -ta=tesla:${NV_GPU_ARCH}")
      endif()
      if(${ENABLE_OPENMP})
         target_compile_options(${PROJECT_NAME} PRIVATE -Mipa=fast)
      else()
         target_compile_options(${PROJECT_NAME} PRIVATE -Mipa=fast,inline)
      endif()
   endif()

In order to change the compiler settings you replace the ``target_compile_options`` that are currently used with the ones that you would like to have. Make sure you pick the right HPC system and use flags that fit to the compiler which is being used (see compiletime log output). Typical debug flags for e.g. Intel would be ``-g -traceback -check all,noarg_temp_created,bounds,uninit``. 

for XIOS
--------

For the IO server debug flags can be set inside the xios source code folder at: ``awicm3-v3.2/xios/arch.fcm``. The exact path may vary by model version. Here you want to add some of the DEV and DEBUG flags to the BASE flags for Fortran or C, as appropriate:

.. code-block:: CMake

   %BASE_CFLAGS    -std=c++11 -diag-disable 1125 -diag-disable 279 -D__XIOS_EXCEPTION
   %PROD_CFLAGS    -O3 -D BOOST_DISABLE_ASSERTS -march=core-avx2 -mtune=core-avx2
   %DEV_CFLAGS     -g -traceback
   %DEBUG_CFLAGS   -DBZ_DEBUG -g -traceback -fno-inline
   
   %BASE_FFLAGS    -D__NONE__
   %PROD_FFLAGS    -O3 -march=core-avx2 -mtune=core-avx2
   %DEV_FFLAGS     -g -O2 -traceback
   %DEBUG_FFLAGS   -g -traceback
