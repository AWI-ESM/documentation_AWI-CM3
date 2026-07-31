.. _model_family:

****************
The model family
****************

There is no single model documented here. There is a family that shares an atmosphere, an ocean, a coupler and an IO server, and differs in which further components are bolted on. The names are similar enough that people pick the wrong one, and similar enough that the mistake is not obvious until a run is well underway. This page is the map.

If you already know which setup you are on, you can leave. Everything else in this documentation is written to be read without it.

How the names work
==================

.. code-block:: text

   AWI-ESM3-v3.5.0-cc
       |    |      |
       |    |      +-- configuration: cc = carbon cycle, is = ice sheet
       |    +-- version: always three numbers
       +-- family: ESM3 builds LPJ-GUESS, CM3 does not

Three things about that, in the order people get them wrong:

- **The family is a component set.** AWI-ESM3 contains LPJ-GUESS and AWI-CM3 does not. They are separate setups in esm_tools, at ``configs/setups/awicm3/`` and ``configs/setups/awiesm3/``, and neither is a version of the other. Both are supported and both are still developed.
- **The version bundles component versions.** AWI-CM3-v3.4.2 and AWI-ESM3-v3.4.2 carry the same OpenIFS, FESOM2, XIOS, OASIS3-MCT and runoff mapper, and differ only in that the second also builds LPJ-GUESS. A shared version number means the shared components match, nothing more.
- **The suffix names a configuration, not a patch level.** ``-cc`` is not a bugfix of the plain version, and ``-is`` is not later than ``-cc``. They are three configurations sharing an ocean and an atmosphere, gated in esm_tools by feature switch rather than by version.

The esm_master target is the name lowercased with the family run together, followed by the exact version: ``awicm3-v3.2``, ``awiesm3-v3.4.2``.

Targets ending in ``develop`` follow a branch rather than a tag, so what they install changes under you over time. They are the right choice for model development work, and for the ``-cc`` and ``-is`` variants they are currently the only choice. See :doc:`contribute` for working that way.

AWI-CM3
=======

The atmosphere ocean model, with no land or ice sheet components.

- Components: OpenIFS, FESOM2, XIOS, OASIS3-MCT and the runoff mapper. At v3.4.2 esm_tools builds these from ``oifs-48r1v4``, ``fesom-2.7.7``, ``xios-2.5.3``, ``oasis3mct-5.2`` and ``rnfmap-v1.3``.
- Setup: ``awicm3``. Versions v3.0 through v3.4.2, plus ``develop``.
- Install: ``esm_master install-awicm3-v3.4.2``. Runscripts in ``esm_tools/runscripts/awicm3/v3.4.2/``.
- Cite: Streffing et al. (2022), https://doi.org/10.5194/gmd-15-6399-2022.

AWI-ESM3
========

AWI-CM3 plus interactive vegetation.

- Components: everything AWI-CM3 has, plus LPJ-GUESS.
- Setup: ``awiesm3``. Versions v3.4.0 through v3.4.2, plus ``develop``.
- Install: ``esm_master install-awiesm3-v3.4.2``. Runscripts in ``esm_tools/runscripts/awiesm3/v3.4.2/``.
- Cite: paper in preparation, expected 2027. Until it appears, cite Streffing et al. (2022) for the coupled core and the LPJ-GUESS references for the vegetation.

AWI-ESM3-cc
===========

AWI-ESM3 as a full carbon cycle model.

- Components: everything AWI-ESM3 has, plus REcoM ocean biogeochemistry inside FESOM2 and a prognostic CO2 tracer in OpenIFS.
- It also brings the OASIS coupling that actually closes the carbon cycle, which no other setup here has. CO2 is exchanged with the ocean through ``rst_co2_ao.nc`` and with the vegetation through ``rst_co2_av.nc``, so ``-cc`` runs with extra coupling fields and a larger OASIS restart set than everything else in this family.
- Setup: ``awiesm3``, version ``develop-cc``. In development and running; to be released with v3.5.0.
- Gated in esm_tools by ``with_co2_tracer``, ``with_co2_oce_coupling`` and ``with_co2_veg_coupling``, all set together by the version.
- Install: ``esm_master install-awiesm3-develop-cc``.
- Cite: paper in preparation, expected 2027.

AWI-ESM3-is
===========

AWI-ESM3 with a coupled ice sheet.

- Components: everything AWI-ESM3 has, plus PISM and dEBM. Couples orography, surface mass balance, the moving sub ice shelf cavity and icebergs.
- Setup: ``awiesm3``, version ``develop-is``. In development and running; to be released with v3.5.0.
- The dynamic mesh part is gated by ``interactive_mesh``, which is a feature switch and deliberately not tied to a version, so it is set in your runscript rather than chosen by the install target.
- Install: ``esm_master install-awiesm3-develop-is``.
- Starting a run is not one runscript and one command, as it is for every other setup here. PISM is iteratively coupled and runs as its own chain, so you need the driver form described in :doc:`quickstart`.
- Cite: paper in preparation, expected 2028.

``-cc`` and ``-is`` have not been combined and combining them is not on the near term plan, so there is currently no setup here that has both a carbon cycle and an ice sheet.

How this documentation marks what applies
=========================================

A section that applies to every setup says nothing about it. A section that does not opens with a single line naming the scope:

.. code-block:: text

   Applies to: any setup with LPJ-GUESS (AWI-ESM3 v3.4 and later).

The scope is written in terms of components and feature switches rather than model names wherever it can be, because that is how esm_tools gates them and because it stays correct if a new variant appears. A section marked as applying to setups with LPJ-GUESS applies to AWI-ESM3, to ``-cc`` and to ``-is`` without having to list all three and without having to be edited when a fourth arrives.

Versions do not update themselves
=================================

``awicm3-v3.2`` installs v3.2 and always will. It does not pick up ``v3.2.1`` or ``v3.2.2``, both of which are fixes on top of it, and no name anywhere tracks the newest patch in a line.

That is deliberate, because a version named in a paper has to resolve to the same source forever. The cost is that fixes do not travel on their own: the ``L1PCTCO2`` fix released as v3.1.3 is in neither v3.2 nor v3.2.1.

So check :doc:`releases` for the newest version in a line before you install, rather than assuming the shortest name is the newest.

Releases carry all three numbers from v3.3.0 onward. Where this documentation writes a two number version it means the line of releases, not something you can install.

What this page does not tell you
================================

It does not tell you which versions exist right now. That is ``available_versions`` in the setup YAML, and it moves faster than this page. It also does not tell you what changed between versions, which is :doc:`releases`.

Versions v3.5 and v3.6 are named throughout this documentation as the planned homes of ``-cc`` and ``-is``. Neither is released, and the version at which those variants actually land may move.
