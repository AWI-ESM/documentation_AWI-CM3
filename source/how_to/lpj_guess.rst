*********
LPJ-GUESS
*********

Applies to: AWI-ESM3 and its variants. AWI-CM3 has no vegetation model.

There is no switch for dynamic vegetation. ``ECE_CPL_LPJG`` is on unconditionally in the AWI-ESM3 setup, so running AWI-ESM3 is running with LPJ-GUESS.

What OpenIFS gets from it
=========================

On every coupling exchange LPJ-GUESS returns the vegetation type, the cover fraction and the LAI, for the low and the high vegetation tile each, and OpenIFS uses those in place of what it read at initialisation. It also stops reading the monthly LAI climatology out of the ICMCL altogether.

So whatever vegetation is in the initial condition files decides only the first few steps. If you want a particular vegetation, you have to spin it up or bring it in as a restart, not write it into the ICMGG. :doc:`../paleo` covers the case where those initial fields come from a palaeogeographic reconstruction.

Spin up the vegetation
======================

A new equilibrium climate needs its own spinup, of about 2000 years, run with the ``lpjg-spinup`` setup. Vegetation and the fast soil pools reach equilibrium by integration in that time. The slow soil carbon pools would need far longer, so LPJ-GUESS does not integrate them: it records litter input and decomposition over a window early in the spinup, solves the pools analytically once, and lets the rest of the run settle around the result. That is why 2000 years is enough for something whose timescale is much longer than 2000 years.

The first ``freenyears`` years, 100 in the spinups run so far, deliberately run without nitrogen limitation so that a nitrogen pool can build up first.

You do not need a spinup when an experiment genuinely branches from another, a scenario continuing a historic run being the obvious case. Then you take the state across, as below.

The ``.ins`` files are LPJ-GUESS's own configuration and are not a knob to reach for. In practice nobody changes them, and if you are going to, you want to know the vegetation model rather than this page.

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
