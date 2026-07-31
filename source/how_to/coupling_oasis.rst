******************
Coupling and OASIS
******************

Measure which component is limiting the throughput of the coupled model
=======================================================================

Coupled performance balancing can be performed with the oasis lucia tool. In the work folder where your experiment ran, execute ``$(model_install_dir)/awicm-3.1/oasis/util/lucia/lucia``. When executing lucia for the first time, a fortran compiler needs to be available in the environment. 
The output,
   
..  code-block:: bash
  
  Component -         Calculations   -     Waiting time (s) - # cpl step :
  fesom                    1616.47                 45.08          4377
  oifs                     1263.30                397.72          4377
 
..
  
can be interpreted as such. Fesom spend nearly all it's computing time on calculations, while oifs was waiting for about 1/4 of the time. Therefore fesom was the   limiting factor on this specific setup. Take note, that having zero waiting time in all components is no achievable, since the length of timesteps varies throughout the run, depending on output and called physics packages. For example the radiation is called every 2 hours in OpenIFS making this timesteps longer than the non-radiation ones in between. Modern versions of lucia also provide solutions for optimizing with this imbalance in mind.

Generate OASIS3MCT remapping weights for large grids (offline and MPI+OMP parallel)
===================================================================================

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

The ``rmp_`` weight files and the OASIS restart files depend on the FESOM2 mesh partition, because the FESOM2 side of the coupling is addressed in PE contiguous order: the global nodes are listed rank by rank, in the order the partitioner assigned them. Change the ``dist`` and the addressing changes with it, even though the mesh, the atmosphere grid and the weight values themselves are all unchanged.

Regenerating them, as above, is one way to get a set for the new core count, and on a large grid it costs hours to months. You only have to pay that once per grid pair. If you already hold a working set for any FESOM2 core count on the same grid pair, the `oasis_reorder_tool <https://github.com/AWI-ESM/oasis_reorder_tool>`_ permutes what you have into the ordering of the new partition instead. For the 3.1 million node ``dars2`` mesh, about 5 GB of NetCDF, that takes five to ten seconds. It reorders ``rmp_*.nc``, ``rstos*``, ``rstas*`` and ``vegin.nc``, and does not touch anything else in the directory.

The tool never computes a weight, it only rearranges values that are already in the files. So it moves you between core counts, and it is no help for a grid pair that has no ``rmp_`` files yet: a new FESOM2 mesh or a new OpenIFS truncation still needs the offline generation above, or a low resolution run that generates the weights on the fly.

It is one Fortran source file with NetCDF-Fortran as its only dependency, so moving it to another machine is a module swap. On levante:

.. code-block:: bash

   git clone https://github.com/AWI-ESM/oasis_reorder_tool
   cd oasis_reorder_tool
   module load intel-oneapi-compilers/2023.2.1-gcc-11.2.0
   module load intel-oneapi-mpi/2021.5.0-intel-2021.5.0
   module load netcdf-fortran/4.5.3-intel-oneapi-mpi-2021.5.0-intel-2021.5.0
   make

If you build it elsewhere, keep the ``-heap-arrays 64`` that the ``Makefile`` sets and run with ``ulimit -s unlimited``. Without both, ``nf90_get_var`` overflows the stack on compiler generated temporaries, and only once the mesh reaches a few million nodes, so a small test mesh will not show it to you.

Then set the four paths at the top of ``submit.sh``, the two FESOM2 mesh partition directories and the two OASIS pool directories, and submit it:

.. code-block:: bash

   DIST_OLD=/work/ab0246/a270092/input/fesom2/dars2/dist_5120
   DIST_NEW=/work/ab0246/a270092/input/fesom2/dars2/dist_2560
   OASIS_IN=/work/ab0246/a270092/input/oasis/cy48r1/TCO319-DARS2/5120
   OASIS_OUT=/work/ab0246/a270092/input/oasis/cy48r1/TCO319-DARS2/2560

Leave the rest of ``submit.sh`` as it is unless you are on another machine, since it carries the launcher settings levante needs and the repository README explains them. Afterwards ``esm_runscripts`` picks the reordered files up by itself once you ask for the new core count:

.. code-block:: yaml

   fesom:
       nproc: 2560

Do check the result, because a wrong permutation does not crash anything. It gives you a model that couples happily and exchanges fluxes between the wrong points, which you will only see in the fields. The sorted hash check in the README tests the property that matters, that every variable in the output holds the same set of values as the input and only their order changed.
