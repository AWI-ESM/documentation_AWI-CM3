.. _chap_Workfolder

Workfolder contents
************

Before the time integration of the model:

+---------------------------+-------------+-------------------------------------------------+
| File name                 | File type   | Description                                     |
+===========================+=============+=================================================+
| cdwavein                  | input       | input file from WAM wave model                  |
|                           |             | (Apparent surface humidity)                     |
+---------------------------+-------------+-------------------------------------------------+
| FESOM.mesh.diag           | input       | output of FESOM2 mesh diagnostics               |
+---------------------------+-------------+-------------------------------------------------+
| grids.nc                  | input       | center lon/lat for OASIS3MCT. Note: input file  |
|                           |             | for OIFS but output file for FESOM2             |
+---------------------------+-------------+-------------------------------------------------+
| masks.nc                  | input       | land sea mask for OASIS3MCT. Note: input file   |
|                           |             | for OIFS but output file for FESOM2             |
+---------------------------+-------------+-------------------------------------------------+
| areas.nc                  | input       | mesh area for OASIS3MCT. Note: input file       |
|                           |             | for OIFS but output file for FESOM2             |
+---------------------------+-------------+-------------------------------------------------+
| FESOM.x                   | bin         | FESOM2 executable                               |
+---------------------------+-------------+-------------------------------------------------+
| fort.4                    | ctrl        | OIFS namelists                                  |
+---------------------------+-------------+-------------------------------------------------+
| hostfile_srun             | ctrl        | controls the allocation of cores to MPI and OMP |
+---------------------------+-------------+-------------------------------------------------+

Additional files after the time integration of the model:

+---------------------------+-------------+-------------------------------------------------+
| debug.notroot*            | log         | OASIS3MCT logfile mostly empty                  |
+---------------------------+-------------+-------------------------------------------------+
| debug.root*               | log         | OASIS3MCT logfile containing debug              |
|                           |             | controlled via namcouple variable NLOGPRT       |
+---------------------------+-------------+-------------------------------------------------+
| drhook*                   | log         | debug info from DR_HOOK ECMWF debug tool        |
|                           |             | controlled via export DR_HOOK*                  |
+---------------------------+-------------+-------------------------------------------------+
| a2o*                      | output      | intermediate for gen of OASIS3MCT restart files |
|                           |             | (only if first leg and LRESUME_oasis3mct=0)     |
+---------------------------+-------------+-------------------------------------------------+
| A_*                       | output      | intermediate for gen of OASIS3MCT restart files |
|                           |             | (only if first leg and LRESUME_oasis3mct=0)     |
+---------------------------+-------------+-------------------------------------------------+
| *_FESOM_*                 | output      | intermediate for gen of OASIS3MCT restart files |
|                           |             | (only if first leg and LRESUME_oasis3mct=0)     |
+---------------------------+-------------+-------------------------------------------------+
| BLS*                      | restart     | restart file for WAM wave model                 |
+---------------------------+-------------+-------------------------------------------------+
| FESOM.${year}.ice*        | restart     | restart file for FESOM2 ice model               |
+---------------------------+-------------+-------------------------------------------------+
| FESOM.${year}.oce*        | restart     | restart file for FESOM2 ocean model             |
+---------------------------+-------------+-------------------------------------------------+
| FESOM.clock               | restart     | restart control file for FESOM2                 |
+---------------------------+-------------+-------------------------------------------------+

