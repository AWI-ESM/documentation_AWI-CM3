.. _chap_workfolder:

*******************
Workfolder contents
*******************

What you find in ``run_{date}/work`` while a leg runs, grouped by the component that owns it. A coupled run leaves several thousand entries there, but nearly all of them are repeats of a handful of kinds, so this page lists kinds. ``{var}.fesom.{year}.nc`` is one entry here and several hundred on disk, and ``xios_client_{rank}.out`` is one entry and one file per client rank.

Types are ``input`` for something linked or copied in, ``ctrl`` for a namelist or configuration file, ``bin`` for an executable, ``output`` and ``restart`` for what the run produces, ``log`` for what you read afterwards and ``work`` for scratch that neither goes in nor comes out.

Only the components your setup contains appear. See :doc:`model_family` if you are not sure which those are. The logs worth reading first when a run fails are not here at all, they are in ``run_{date}/log`` and in the experiment's parent ``log`` directory.

OpenIFS
=======

+----------------------------------------+-----------+----------------------------------------------------------------+
| File name                              | Type      | Description                                                    |
+========================================+===========+================================================================+
| ``ICMGG{expid}INIT``                   | input     | grid point initial and boundary conditions                     |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ICMGG{expid}INIUA``                  | input     | upper atmosphere initial and boundary conditions               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ICMSH{expid}INIT``                   | input     | spherical harmonic initial and boundary conditions             |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ICMCL{expid}INIT``                   | input     | monthly albedo and LAI climatologies                           |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ifsdata``                            | input     | folder of default gas and aerosol climatologies                |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``composition``                        | input     | folder holding ``onlinedust_v4_rmp.nc``, the online dust       |
|                                        |           | climatology. OpenIFS on cy48r1 opens it at init whatever the   |
|                                        |           | MIP                                                            |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``{res}_{trunc}``                      | input     | folder of GRIB climate fields for that grid. The suffix is the |
|                                        |           | spectral truncation: ``_2`` linear, ``_3`` quadratic, ``_4``   |
|                                        |           | cubic octahedral, so ``319_4`` is TCO319                       |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``slt_TCO{res}.nc``                    | input     | soil type map for the grid                                     |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``co2_input4MIPs_*.nc``                | input     | CMIP greenhouse gas concentrations                             |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``*_MIDYR_CONC.txt``                   | input     | CMIP5 forcing files (CMIP6 is selected in fort.4 instead)      |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``cdwavein``                           | input     | WAM apparent surface humidity                                  |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``sfcwindin``                          | input     | WAM initial wind                                               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``specwavein``                         | input     | WAM initial temperature                                        |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``uwavein``                            | input     | WAM initial surface roughness                                  |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``wam_grid_tables``                    | input     | WAM GRIB code tables                                           |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``wam_subgrid_0 to _2``                | input     | WAM subgrid definitions                                        |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``fort.4``                             | ctrl      | every OpenIFS namelist, including NAERAD and NAMORB            |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``wam_namelist``                       | ctrl      | WAM settings                                                   |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``OpenIFS``                            | bin       | OpenIFS executable, launched as ``OpenIFS -v ecmwf -e          |
|                                        |           | {expid}``                                                      |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``NODE.001_01``                        | log       | the detailed OpenIFS run log                                   |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ifs.stat``                           | log       | one line per timestep, useful to see how far a run got         |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``meminfo.txt``                        | log       | EC_MEMINFO memory report                                       |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``gstats.xml``                         | log       | GSTATS timing report, one item per code region                 |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``drhook*``                            | log       | DR_HOOK traceback output, only when DR_HOOK is exported        |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ICMGG{expid}+{date}``                | output    | grid point output, if XIOS is not doing the writing            |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ICMSH{expid}+{date}``                | output    | spherical harmonic output                                      |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ICMUA{expid}+{date}``                | output    | upper atmosphere output                                        |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``rcf``                                | restart   | OpenIFS restart control file                                   |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``srf*``                               | restart   | OpenIFS restart, one per MPI task                              |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``waminfo``                            | restart   | WAM control file                                               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``BLS*, LAW*``                         | restart   | WAM restart files                                              |
+----------------------------------------+-----------+----------------------------------------------------------------+

FESOM2
======

+----------------------------------------+-----------+----------------------------------------------------------------+
| File name                              | Type      | Description                                                    |
+========================================+===========+================================================================+
| ``namelist.config``                    | ctrl      | general settings                                               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``namelist.oce``                       | ctrl      | ocean settings                                                 |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``namelist.ice``                       | ctrl      | sea ice settings                                               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``namelist.icepack``                   | ctrl      | Icepack sea ice thermodynamics settings                        |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``namelist.io``                        | ctrl      | output and diagnostic settings                                 |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``namelist.dyn``                       | ctrl      | dynamics settings                                              |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``namelist.tra``                       | ctrl      | tracer settings                                                |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``namelist.cvmix``                     | ctrl      | CVMix vertical mixing settings                                 |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``namelist.transit``                   | ctrl      | transient tracer settings                                      |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``namelist.forcing``                   | ctrl      | standalone forcing settings, unused when coupled               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``fesom``                              | bin       | FESOM2 executable                                              |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``fesom.clock``                        | restart   | the clock file. First number is the last written timestep,     |
|                                        |           | needed when changing timestep between runs                     |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``fesom.{year}.oce.restart``           | restart   | ocean restart, a directory of NetCDF files                     |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``fesom.{year}.ice.restart``           | restart   | sea ice restart, a directory of NetCDF files                   |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``{var}.fesom.{year}.nc``              | output    | one file per output variable per year                          |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``{var}.fesom_{y0}-{y1}.nc``           | output    | the same, for a multi year output interval                     |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``fesom.mesh.diag.nc``                 | output    | mesh diagnostics written on the first run                      |
+----------------------------------------+-----------+----------------------------------------------------------------+

OASIS3-MCT
==========

+----------------------------------------+-----------+----------------------------------------------------------------+
| File name                              | Type      | Description                                                    |
+========================================+===========+================================================================+
| ``namcouple``                          | ctrl      | the coupling itself: exchange fields, remapping method,        |
|                                        |           | frequencies, $NLOGPRT and $RUNTIME                             |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``grids.nc``                           | input     | cell centre longitudes and latitudes. Input for OpenIFS,       |
|                                        |           | written by FESOM2                                              |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``masks.nc``                           | input     | land sea masks. Same asymmetry as grids.nc                     |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``areas.nc``                           | input     | cell areas. Same asymmetry as grids.nc                         |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``rmp_*.nc``                           | input     | remapping weights. Generated on the fly if absent, which is    |
|                                        |           | slow on large grids                                            |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``rstas.nc``                           | restart   | atmosphere side coupling restart                               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``rstos.nc``                           | restart   | ocean side coupling restart                                    |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``vegin.nc``                           | restart   | vegetation side coupling restart                               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``rst_co2_ao.nc``                      | restart   | CO2 exchange with the ocean. AWI-ESM3-cc only                  |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``rst_co2_av.nc``                      | restart   | CO2 exchange with the vegetation. AWI-ESM3-cc only             |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``debug.root.{rank}``                  | log       | OASIS log from the root task, verbosity from $NLOGPRT          |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``debug.notroot.{rank}``               | log       | the same from non root tasks, usually near empty               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``nout.{rank}``                        | log       | OASIS parsing the namcouple                                    |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``timeline_{component}.nc``            | log       | per component event timeline: start and end of every PUT, GET, |
|                                        |           | MAP and restart write                                          |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``load_balancing_info.txt``            | log       | the lucia analysis, only with use_lucia. OASIS3-MCT 5 writes   |
|                                        |           | it directly                                                    |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``lucia.*``                            | log       | raw timing data on OASIS3-MCT 4, post-processed by the lucia   |
|                                        |           | tool                                                           |
+----------------------------------------+-----------+----------------------------------------------------------------+

XIOS
====

Applies to: AWI-CM3 v3.1 and later, and every AWI-ESM3. AWI-CM3 v3.0 has no IO server.

The unsuffixed files configure OpenIFS output and the ``_fesom`` ones configure FESOM2 output. That is historical, OpenIFS was wired up first, and it catches people out: editing ``file_def.xml`` to change FESOM2 output silently changes OpenIFS output instead.

+----------------------------------------+-----------+----------------------------------------------------------------+
| File name                              | Type      | Description                                                    |
+========================================+===========+================================================================+
| ``iodef.xml``                          | ctrl      | master configuration. Names the contexts and tunes the two     |
|                                        |           | level server                                                   |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``context_ifs.xml``                    | ctrl      | the OpenIFS context                                            |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``context_fesom.xml``                  | ctrl      | the FESOM2 context                                             |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``axis_def.xml``                       | ctrl      | vertical axes, including the pressure levels output is         |
|                                        |           | interpolated onto                                              |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``domain_def.xml``                     | ctrl      | horizontal domains                                             |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``grid_def.xml``                       | ctrl      | grids, combining domains and axes                              |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``field_def.xml``                      | ctrl      | every field XIOS can write                                     |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``file_def.xml``                       | ctrl      | which fields go to which file, at which frequency              |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``*_fesom.xml``                        | ctrl      | the FESOM2 counterpart of each of the five files above         |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``xios.x``                             | bin       | IO server executable                                           |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``xios_client_{rank}.out``             | log       | one pair of .out and .err per client rank                      |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``xios_server{N}_{rank}.out``          | log       | one pair per server rank, N is the server level                |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``distribute_file_{context}.dat``      | log       | how the primary server spread the output files over the        |
|                                        |           | secondary pools, with the estimated volume per file. Only      |
|                                        |           | written with two level servers                                 |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``xios_registry.bin``                  | log       | internal registry dump                                         |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``xios_interpolation_weights_*.nc``    | output    | interpolation weights XIOS generated for its own regridding    |
+----------------------------------------+-----------+----------------------------------------------------------------+

LPJ-GUESS
=========

Applies to: AWI-ESM3 and its variants. AWI-CM3 has no vegetation model.

+----------------------------------------+-----------+----------------------------------------------------------------+
| File name                              | Type      | Description                                                    |
+========================================+===========+================================================================+
| ``*.ins``                              | ctrl      | LPJ-GUESS instruction files. ``run_coupled_*.ins`` is the      |
|                                        |           | entry point and includes the others                            |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``lpjg_steps.yaml``                    | ctrl      | time stepping and run configuration, written by esm_tools from |
|                                        |           | a jinja template each leg                                      |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``guess``                              | bin       | LPJ-GUESS executable                                           |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ece_gridlist_TCO{res}.txt``          | input     | the grid list. Written and read by LPJ-GUESS, nothing else     |
|                                        |           | uses it                                                        |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``ndep``                               | input     | nitrogen deposition forcing                                    |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``landuse``                            | input     | land use forcing                                               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``fire``                               | input     | fire forcing                                                   |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``run{N}``                             | work      | one directory per LPJ-GUESS instance, each with its own copy   |
|                                        |           | of the .ins files                                              |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``lpjg_state_{year}``                  | restart   | the LPJ-GUESS state                                            |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``guess.log``                          | log       | LPJ-GUESS run log                                              |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``LPJ-GUESS_monthlyoutput.txt``        | output    | the monthly LAI and vegetation fractions handed to OpenIFS.    |
|                                        |           | Written by rank 0 on 31 December only, and not during LPJ-     |
|                                        |           | GUESS spinup, so a leg that does not reach the end of a year   |
|                                        |           | leaves it empty. That is not a fault                           |
+----------------------------------------+-----------+----------------------------------------------------------------+

Runoff mapper
=============

+----------------------------------------+-----------+----------------------------------------------------------------+
| File name                              | Type      | Description                                                    |
+========================================+===========+================================================================+
| ``namelist.runoffmapper``              | ctrl      | runoff mapper settings                                         |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``runoff_maps.nc``                     | input     | river basins and discharge areas                               |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``rnfma``                              | bin       | runoff mapper executable                                       |
+----------------------------------------+-----------+----------------------------------------------------------------+

Job control and shared files
============================

+----------------------------------------+-----------+----------------------------------------------------------------+
| File name                              | Type      | Description                                                    |
+========================================+===========+================================================================+
| ``hostfile_srun``                      | ctrl      | which executable runs on which core, by calling the prog       |
|                                        |           | scripts                                                        |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``hostlist``                           | ctrl      | every MPI task and the node it runs on                         |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``prog_{component}.sh``                | ctrl      | pins the component's ranks to core slots with taskset, then    |
|                                        |           | calls its script file. One per component                       |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``script_{component}.sh``              | ctrl      | sets OMP_NUM_THREADS and OASIS_OMP_NUM_THREADS, then launches  |
|                                        |           | the executable                                                 |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``batch_system.env``                   | ctrl      | the environment the batch system was given                     |
+----------------------------------------+-----------+----------------------------------------------------------------+
| ``lib``                                | work      | shared libraries the executables were built against            |
+----------------------------------------+-----------+----------------------------------------------------------------+

Which coupling files can be generated on the fly
================================================

+---------------------------+---------------------------------------------------------------+
| File name                 | Properties                                                    |
+===========================+===============================================================+
| Remapping files rmp\_     | - Can be generated on the fly for low resolutions             |
|                           | - Do depend on OpenIFS & FESOM2 resolution                    |
|                           | - Do depend on number of FESOM2 cores                         |
|                           | - Do not depend of number of OpenIFS cores                    |
|                           | - Do not depend on hpc system                                 |
|                           | - Shall be linked in if possible to save time.                |
|                           | - Stay constant throughout an experiment                      |
|                           | - Can be reordered for a new FESOM2 core count                |
+---------------------------+---------------------------------------------------------------+
| restart files rst         | - Can be generated only in lresume_oasis3mct:false runs       |
|                           | - If lresume_oasis3mct:true they have to be linked in         |
|                           | - Do depend on OpenIFS & FESOM2 resolution                    |
|                           | - Do depend on number of FESOM2 cores                         |
|                           | - Do not depend of number of OpenIFS cores                    |
|                           | - Do not depend on hpc system                                 |
|                           | - Shall be linked in if possible to save time.                |
|                           | - Change throughout an experiment and are part of the restart |
|                           | - Can be reordered for a new FESOM2 core count                |
+---------------------------+---------------------------------------------------------------+
| masks, grids, areas.nc    | - OpenIFS part can not be generated at runtime                |
|                           | - Do depend on OpenIFS & FESOM2 resolution                    |
|                           | - Do not depend on number of FESOM2 cores                     |
|                           | - Do not depend of number of OpenIFS cores                    |
|                           | - Do not depend on hpc system                                 |
|                           | - Nedd to be linked in                                        |
|                           | - Stay constant throughout an experiment                      |
+---------------------------+---------------------------------------------------------------+

Reordering for a new FESOM2 core count is done with the tool described in :doc:`how_to/coupling_oasis`, which permutes an existing set in seconds rather than regenerating it.
