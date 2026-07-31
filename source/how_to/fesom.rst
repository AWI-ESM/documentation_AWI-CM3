******
FESOM2
******

Branch off from existing FESOM2 restart
=======================================
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
