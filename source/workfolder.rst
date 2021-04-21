.. _chap_workfolder

Workfolder contents
*******************

########################################
Before the time integration of the model
########################################

+---------------------------+-------------+-------------------------------------------------+
| File name                 | Type        | Description                                     |
+===========================+=============+=================================================+
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
| ifsdata                   | input       | folder containing default OIFS gas and          |
|                           |             | aerosol climatologies                           |
+---------------------------+-------------+-------------------------------------------------+
| *_MIDYR_CONC.txt          | input       | CMIP5 forcing files (optional CMIP6 via fort.4) |
+---------------------------+-------------+-------------------------------------------------+
| ICMGG{job_id}INIT         | input       | grid point inital and boundary conditions for   |
|                           |             | OIFS                                            |
+---------------------------+-------------+-------------------------------------------------+
| ICMGG{job_id}INIUA        | input       | upper atmosphere inital and boundary conditions |
|                           |             | for OIFS                                        |
+---------------------------+-------------+-------------------------------------------------+
| ICMSH{job_id}INIT         | input       | spherical harmonic inital and boundary          |
|                           |             | conditions for OIFS                             |
+---------------------------+-------------+-------------------------------------------------+
| rmp_*                     | input       | OASIS3MCT remapping weight files. (optional,    |
|                           |             | if not present they will be generated on the    |
|                           |             | fly. This will take some time.)                 |
+---------------------------+-------------+-------------------------------------------------+
| rtables                   | input       | OIFS grib code tables                           |
+---------------------------+-------------+-------------------------------------------------+
| wam_grid_tables           | input       | WAM grib code tables                            |
+---------------------------+-------------+-------------------------------------------------+
| *l_*                      | input       | Ozone cilmatology and old disused inital &      |
|                           |             | boundary conditions                             |
+---------------------------+-------------+-------------------------------------------------+
| runoff_maps.nc            | input       | contains river basins and discharge areas       |
+---------------------------+-------------+-------------------------------------------------+
| cdwavein                  | input       | input file from WAM wave model                  |
|                           |             | (Apparent surface humidity)                     |
+---------------------------+-------------+-------------------------------------------------+
| sfcwindin                 | input       | WAM inital wind                                 |
+---------------------------+-------------+-------------------------------------------------+
| specwavein                | input       | WAM inital temperature                          |
+---------------------------+-------------+-------------------------------------------------+
| uwavein                   | input       | WAM inital surface roughness                    |
+---------------------------+-------------+-------------------------------------------------+
| wam_subgrid_0             | input       | Something for WAM, not quite sure..             |
+---------------------------+-------------+-------------------------------------------------+
| temp, tmp1 tmp2           | input       | used for esm-ksh tools                          |
+---------------------------+-------------+-------------------------------------------------+
| *red_points.txt           | input       | disused should remove it..                      |
+---------------------------+-------------+-------------------------------------------------+
| fort.4                    | ctrl        | OIFS namelists                                  |
+---------------------------+-------------+-------------------------------------------------+
| hostfile_srun             | ctrl        | controls the allocation of cores to executables |
|                           |             | by calling prog* scripts                        |
+---------------------------+-------------+-------------------------------------------------+
| hostlist                  | ctrl        | contains list of all MPI tasks and the compute  | 
|                           |             | node they run on                                |
+---------------------------+-------------+-------------------------------------------------+
| prog*                     | ctrl        | calling script* files while calculation OpenMP  |
|                           |             | settings                                        |
+---------------------------+-------------+-------------------------------------------------+
| script*                   | ctrl        | calling executalbes with OpenMP settings        |
+---------------------------+-------------+-------------------------------------------------+
| namcouple                 | ctrl        | controls OASIS3MCT coupling fields, remapping   |
|                           |             | and timing                                      |
+---------------------------+-------------+-------------------------------------------------+
| namelist.config           | ctrl        | controls FESOM2 general settings                |
+---------------------------+-------------+-------------------------------------------------+
| namelist.forcing          | ctrl        | controls FESOM2 forcing settings (not needed)   |
+---------------------------+-------------+-------------------------------------------------+
| namelist.ice              | ctrl        | controls FESOM2 sea ice settings                |
+---------------------------+-------------+-------------------------------------------------+
| namelist.oce              | ctrl        | controls FESOM2 sea ocean settings              |
+---------------------------+-------------+-------------------------------------------------+
| namelist.io               | ctrl        | controls FESOM2 output and diagnostic settings  |
+---------------------------+-------------+-------------------------------------------------+
| namelist.runoffmapper     | ctrl        | controls runoff mapper settings                 |
+---------------------------+-------------+-------------------------------------------------+
| wam_namelist              | ctrl        | controls WAM settings                           |
+---------------------------+-------------+-------------------------------------------------+
| FESOM.x                   | bin         | FESOM2 executable                               |
+---------------------------+-------------+-------------------------------------------------+
| master.exe                | bin         | OIFS executable                                 |
+---------------------------+-------------+-------------------------------------------------+
| rnfmap.exe                | bin         | Runoff mapper executable                        |
+---------------------------+-------------+-------------------------------------------------+

########################################################
Additional files after the time integration of the model
########################################################

+---------------------------+-------------+-------------------------------------------------+
| debug.notroot*            | log         | OASIS3MCT logfile mostly empty                  |
+---------------------------+-------------+-------------------------------------------------+
| debug.root*               | log         | OASIS3MCT logfile containing debug              |
|                           |             | controlled via namcouple variable NLOGPRT       |
+---------------------------+-------------+-------------------------------------------------+
| drhook*                   | log         | debug info from DR_HOOK ECMWF debug tool        |
|                           |             | controlled via export DR_HOOK*                  |
+---------------------------+-------------+-------------------------------------------------+
| ifs.stat                  | log         | OIFS timestep length output                     |
+---------------------------+-------------+-------------------------------------------------+
| lucia*                    | log         | OASIS3MCT coupling timing information. use      |
|                           |             | lucia tool to analyise computational balance    |
+---------------------------+-------------+-------------------------------------------------+
| NODE.001_01               | log         | very detailed logfile of the OIFS simulation    |
+---------------------------+-------------+-------------------------------------------------+
| nout.000000               | log         | logfile of the OASIS3MCT interpreting the       |
|                           |             | namcouple file                                  |
+---------------------------+-------------+-------------------------------------------------+
| a2o*                      | output      | intermediate for gen of OASIS3MCT restart files |
|                           |             | (only if first leg and LRESUME_oasis3mct=0)     |
+---------------------------+-------------+-------------------------------------------------+
| A_*                       | output      | intermediate for gen of OASIS3MCT restart files |
|                           |             | (only if first leg and LRESUME_oasis3mct=0)     |
+---------------------------+-------------+-------------------------------------------------+
| *_fesom_*                 | output      | intermediate for gen of OASIS3MCT restart files |
|                           |             | (only if first leg and LRESUME_oasis3mct=0)     |
+---------------------------+-------------+-------------------------------------------------+
| *.fesom.*                 | output      | FESOM2 output file                              |
+---------------------------+-------------+-------------------------------------------------+
| ICMGG{job_id}+000000      | output      | timestep 0 OIFS output not all fields. deleted  |
+---------------------------+-------------+-------------------------------------------------+
| ICMGG{job_id}+{year}{mon} | output      | OIFS gridpoint output                           |
+---------------------------+-------------+-------------------------------------------------+
| ICMSH{job_id}+{year}{mon} | output      | OIFS spherical harmonic output                  |
+---------------------------+-------------+-------------------------------------------------+
| ICMUA{job_id}+{year}{mon} | output      | OIFS upper atmosphere output                    |
+---------------------------+-------------+-------------------------------------------------+
| MPP*                      | output      | WAM wave model output                           |
+---------------------------+-------------+-------------------------------------------------+
| BLS*                      | restart     | for WAM wave model                              |
+---------------------------+-------------+-------------------------------------------------+
| LAW*                      | restart     | for WAM wave model                              |
+---------------------------+-------------+-------------------------------------------------+
| FESOM.${year}.ice*        | restart     | for FESOM2 ice model                            |
+---------------------------+-------------+-------------------------------------------------+
| FESOM.${year}.oce*        | restart     | for FESOM2 ocean model                          |
+---------------------------+-------------+-------------------------------------------------+
| FESOM.clock               | restart     | control file for FESOM2                         |
+---------------------------+-------------+-------------------------------------------------+
| rst*                      | restart     | for OASIS3MCT if run with lag                   |
+---------------------------+-------------+-------------------------------------------------+
| rcf                       | restart     | control file for OIFS                           |
+---------------------------+-------------+-------------------------------------------------+
| srf*                      | restart     | for OIFS (one per MPI task)                     |
+---------------------------+-------------+-------------------------------------------------+
| waminfo                   | restart     | control file for WAM                            |
+---------------------------+-------------+-------------------------------------------------+

#################################################################################
Detailed description of coupling files and which ones can be generated on the fly
#################################################################################

+---------------------------+---------------------------------------------------------------+
| File name                 | Properties                                                    |
+===========================+===============================================================+
| Remapping files rmp_      | - Can be generated on the fly for low resolutions             |
|                           | - Do depend on OpenIFS & FESOM2 resolution                    |
|                           | - Do depend on number of FESOM2 cores                         |
|                           | - Do not depend of number of OpenIFS cores                    |
|                           | - Do not depend on hpc system                                 |
|                           | - Shall be linked in if possible to save time.                |
|                           | - Stay constant throughout an experiment                      |
+---------------------------+---------------------------------------------------------------+
| restart files rst         | - Can be generated only in lresume_oasis3mct:false runs       |
|                           | - If lresume_oasis3mct:true they have to be linked in         |
|                           | - Do depend on OpenIFS & FESOM2 resolution                    |
|                           | - Do depend on number of FESOM2 cores                         |
|                           | - Do not depend of number of OpenIFS cores                    |
|                           | - Do not depend on hpc system                                 |
|                           | - Shall be linked in if possible to save time.                |
|                           | - Change throughout an experiment and are part of the restart |
+---------------------------+---------------------------------------------------------------+
| masks, grids, areas.nc    | - OpenIFS part can not be generated at runtime                |
|                           | - Do depend on OpenIFS & FESOM2 resolution                    |
|                           | - Do not depend on number of FESOM2 cores                     |
|                           | - Do not depend of number of OpenIFS cores                    |
|                           | - Do not depend on hpc system                                 |
|                           | - Nedd to be linked in                                        |
|                           | - Stay constant throughout an experiment                      |
+---------------------------+---------------------------------------------------------------+
