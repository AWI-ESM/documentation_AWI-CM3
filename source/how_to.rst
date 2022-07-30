.. _how_to

How to
******

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

Generate OASIS3MCT remapping weights for large grids (offline and MPI+OMP parallel)
=========

Note: This method is meant for Atmosphere-Ocean grid combinations in excess of ~1*10^12, where automatic weight generation on single cores becomes prohibitivly time consuming. 

Before you start, make sure that you:
 
- Obtain the FESOM2 mesh and generate the mesh distribution you would like to use.
- Use the `ocp-tool <https://github.com/JanStreffing/ocp-tool>`_  to match the FESOM2 mesh to the atmosphere files (really just means cutting caspian out of the OIFS land sea mask)
- Copy the ocp-tool modified OpenIFS input files, as well as the Oasis input files (areas.nc, grids.nc, masks.nc) and the runoff_mapper input files into the sub-directories of the pool dir that you use.

Steps towards the ``rmp_`` files:

- Start a coupled simulation with the desired FESOM2 mesh ``dist``. OIFS ``nproc`` may be as small as minimum memory for loading the grid demands.
- Wait until the FESOM2 mesh information was added to the ``areas.nc, grids.nc, masks.nc`` files.
- Wait until the BICUBIC remapping files have been generated. (they are much fast than the GAUSWGT ones, and this will cut the manual work in half later)
- Cancel the job allocation since generating the GAUSWGT ``rmp_`` files would take days to months.
- Change the COUPLE path in ``awicm-3.1/oasis/util/make_dir/make.${your_config}_``
- Set the path to ${your_config} in ``awicm-3.1/oasis/util/make_dir/make.inc_``
- Go to ``awicm-3.1/oasis/examples/test_interpolation``
- Add your ``areas.nc, grids.nc, masks.nc`` files to ``awicm-3.1/oasis/examples/test_interpolation/data_frontiers``
- Modify the ``awicm-3.1/oasis/examples/test_interpolation/run_frontiersinterp.sh`` to add your machine, if it's not included already.
-  Extract the first of the ``GAUSWGT`` couplings (FESOM->OIFS) from the namcouple in your work folder where you generated the ``BICUBIC`` ``rmp_`` files.
- Create a namcouple containing only this one remapping in ``awicm-3.1/oasis/examples/test_interpolation/data_frontiers`` For an example, see: ``awicm-3.1/oasis/examples/test_interpolation/data_frontiers/namcouple_feom_A160_gauswgt``
- Configure `awicm-3.1/oasis/examples/test_interpolation/run_frontiersinterp.sh` to generate this remapping with OpenMP parallelization.
- Generate the first GAUSWGT remapping by starting ``run_frontiersinterp.sh`` on the batch queue.
- Go to Step 9 and repeat for second ``GAUSWGT`` remapping (Runoff-mapper -> FESOM).
- Copy all ``rmp_`` files into the respective pool dir folder (e.g. ``input/oasis/cy43r3/{OIFS_RES}-${FESOM_RES}/${FESOM_DIST}``).
- Start a coupled simulation.


Select an SSP or RCP scenario
=========
CMIP6
---------
Control is possible through the namelist file fort.4. Inside you will find the namelist NAERAD, which contains the options for CMIP5 and CMIP6 greenhouse gas forcing. To activate CMIP6 forcing set the logic switch ``LCMIP6 = .true.``. When NCMIPFIXYR is set to a value >0, it is interpreted as a fix forcing year. In the example below we use constant 1850 GHG forcing. If NCMIPFIXYR=0 the actual model year is used, and forcing changes from year to year. Note, that currently only greenhouse gases and solar radiation are set through this namelist. Work on the implementation of controlable anthopogenic aerosols is still ongoing (status: 30th of June 2022).

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
