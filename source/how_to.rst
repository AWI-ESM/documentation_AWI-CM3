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
