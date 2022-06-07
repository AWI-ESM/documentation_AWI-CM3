.. _how_to

How to
******

- **Measure which component is limiting the throughput of the coupled model**
   Coupled performance balancing can be performed with the oasis lucia tool. In the work folder where your experiment ran, execute ``$(model_install_dir)/awicm-3.1/oasis/util/lucia/lucia``. When executing lucia for the first time, a fortran compiler needs to be available in the environment. 
   The output,
   
   ..  code-block:: bash
  
     Component -         Calculations   -     Waiting time (s) - # cpl step :
     fesom                    1616.47                 45.08          4377
     oifs                     1263.30                397.72          4377
    
   ..
  
   can be interpreted as such. Fesom spend nearly all it's computing time on calculations, while oifs was waiting for about 1/4 of the time. Therefore fesom was the   limiting factor on this specific setup. Take note, that having zero waiting time in all components is no achievable, since the length of timesteps varies throughout the run, depending on output and called physics packages. For example the radiation is called every 2 hours in OpenIFS making this timesteps longer than the non-radiation ones in between. Modern versions of lucia also provide solutions for optimizing with this imbalance in mind.

- **Generate OASIS3MCT remapping weights for large grids (offline and MPI+OMP parallel)**
   Note: This method is meant for Atmosphere-Ocean grid combinations in excess of ~1*10^12, where automatic weight generation on single cores becomes prohibitivly time consuming. 
   
   Before you start, make sure that you:
 
   - Obtain the FESOM2 mesh and generate the mesh distribution you would like to use.
   - Use the [ocp-tool](https://github.com/JanStreffing/ocp-tool) to match the FESOM2 mesh to the atmosphere files (really just means cutting caspian out of the OIFS land sea mask)
   - Copy the ocp-tool modified OpenIFS input files, as well as the Oasis input files (areas.nc, grids.nc, masks.nc) and the runoff_mapper input files into the sub-directories of the pool dir that you use.

   Steps towards the ``rmp_`` files:

   1. Start a coupled simulation with the desired FESOM2 mesh dist. OIFS nproc may be as small as minimum memory for loading the grid demands.
   2. Wait until the FESOM2 mesh information was added to the ``areas.nc, grids.nc, masks.nc`` files.
   3. Wait until the BICUBIC remapping files have been generated. (they are much fast than the GAUSWGT ones, and this will cut the manual work in half later)
   4. Cancel the job allocation since generating the GAUSWGT ``rmp_`` files would take days to months.
   5. _change the COUPLE path in ``awicm-3.1/oasis/util/make_dir/make.${your_config}_``
   6. _set the path to ${your_config} in ``awicm-3.1/oasis/util/make_dir/make.inc_``
   7. Go to ``awicm-3.1/oasis/examples/test_interpolation``
   8. Add your ``areas.nc, grids.nc, masks.nc`` files to ``awicm-3.1/oasis/examples/test_interpolation/data_frontiers``
   9. Modify the ``awicm-3.1/oasis/examples/test_interpolation/run_frontiersinterp.sh`` to add your machine, if it's not included already.
   10.  Extract the first of the ``GAUSWGT`` couplings (FESOM->OIFS) from the namcouple in your work folder where you generated the ``BICUBIC`` ``rmp_`` files.
   11. Create a namcouple containing only this one remapping in ``awicm-3.1/oasis/examples/test_interpolation/data_frontiers`` For an example, see: ``awicm-3.1/oasis/examples/test_interpolation/data_frontiers/namcouple_feom_A160_gauswgt``
   12. Configure `awicm-3.1/oasis/examples/test_interpolation/run_frontiersinterp.sh` to generate this remapping with OpenMP parallelization.
   13. Generate the first GAUSWGT remapping by starting ``run_frontiersinterp.sh`` on the batch queue.
   14. Go to Step 9 and repeat for second ``GAUSWGT`` remapping (Runoff-mapper -> FESOM).
   15. Copy all ``rmp_`` files into the respective pool dir folder (e.g. ``input/oasis/cy43r3/{OIFS_RES}-${FESOM_RES}/${FESOM_DIST}``).
   16. Start a coupled simulation.
