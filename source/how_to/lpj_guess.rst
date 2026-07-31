*********
LPJ-GUESS
*********

Branch off from existing LPJGuess restart
=========================================
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
