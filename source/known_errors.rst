.. _chap_known_errors

Known errors
**********************
- **printf: -8: unknown option**
..  code-block:: bash

  {
  /tmp/slurmd/job8770219/slurm_script[73]: eval[73]: eval[393]: printf: -8: unknown option
  /tmp/slurmd/job8770219/slurm_script[73]: eval[73]: eval[393]: printf: -7: unknown option
  /tmp/slurmd/job8770219/slurm_script[73]: eval[73]: eval[393]: printf: -3: unknown option
  /tmp/slurmd/job8770219/slurm_script[73]: eval[73]: eval[393]: printf: -6: unknown option
  Usage: printf [ options ] format [string …]
  } 
..

  - **Situation**: This error likely appears when you restart the model after the previous leg did not finish successfully.
  - **Solution**: To fix it you need to substract NYEAR_awicm3 from INITIAL_DATE_awicm3. 
  - **Background**: The underlying reason is that AWICM3 currently contains a memory leak when the restart timesteps get large. As a stopgap measure the inital time is moved forward while the restart timestep is kept constant. When a run is started twice from the same restart time INITIAL_DATE_awicm3 is moved forward twice.
