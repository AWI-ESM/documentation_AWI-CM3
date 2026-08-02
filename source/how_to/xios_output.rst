***********
XIOS output
***********

Applies to: AWI-CM3 v3.1 and later, and every AWI-ESM3. AWI-CM3 v3.0 has no IO server.

Output is controlled via `XIOS <https://forge.ipsl.jussieu.fr/ioserver>`_, configured by the XML files in the work directory.

The XML in the work directory is generated
==========================================

Those XML files are rendered from Jinja templates under ``esm_tools/namelists/``, not copied from a fixed set. Editing ``file_def.xml`` in a finished work directory changes nothing about the next leg, because the next run renders a fresh copy over the top of it. Change the template, or change the switch that selects which template is used.

The templates live in two places, one per component:

- OpenIFS: ``esm_tools/namelists/oifs/{cycle}/xios/``, so ``43r3`` and ``48r1`` have their own sets.
- FESOM2: ``esm_tools/namelists/fesom2/xios_xml/``, with a second set in ``xios_xml_cmip7/``.

The other half of the trap is naming. The unsuffixed files are OpenIFS and the ``_fesom`` suffixed ones are FESOM2, so editing ``file_def_fesom.xml.j2`` when you meant OpenIFS output, or the reverse, is easy and silent.

Switch to the CMIP7 output set
==============================

Two switches, one per component, both off by default:

.. code-block:: yaml

   oifs:
       cmip7_cmor_output: true
   fesom:
       cmip7_cmor_output: true

For OpenIFS this swaps ``file_def``, ``field_def``, ``axis_def`` and ``grid_def`` for the set under ``xios/cmip7/``. For FESOM2 it swaps the whole template directory to ``xios_xml_cmip7``, which writes many variables at several frequencies in place of the default minimal monthly set of roughly 28 that mirrors upstream ``namelist.io``.

Do not confuse ``cmip7_cmor_output`` with ``oifs.mip``. ``mip`` chooses the forcing that goes in, the greenhouse gases, aerosols and ozone, from either the CMIP6 or the CMIP7 pool. ``cmip7_cmor_output`` chooses what comes out. They are independent switches and either combination runs.

Regridded output
----------------

Applies to: FESOM2 with ``cmip7_cmor_output``. The default file_def ignores both switches.

The CMIP7 FESOM2 templates can write regular latitude longitude output alongside the native unstructured output, at the same frequency as its native counterpart:

.. code-block:: yaml

   fesom:
       regrid_surface_output: true    # 2D fields
       regrid_3d_output: true         # temp, salt, unod, vnod, w, bolus_*, N2, Kv, Av, ...

Both default to true, because the cost was measured rather than guessed: the 2D set came out under one percent of wall time and under 1 GB per simulated year at half a degree, and adding the 3D set on top measured plus 0.4 percent wall time and plus 8 GB per simulated year. XIOS server rank asynchronous IO is what makes that nearly free. Turn them off for diagnostics style runs that do not want the regridded set. Both need ``xios.fesom_regular_res_lon``, ``xios.fesom_regular_res_lat`` and ``xios.interpolation_order``.

Ocean biogeochemistry output gates
----------------------------------

Applies to: AWI-ESM3-cc, which is the only setup with REcoM.

``file_def_fesom.xml.j2`` gates the biogeochemistry file blocks on three switches that mirror the REcoM ``&parecomsetup`` logicals, so a block is only enabled when the tracers it wants actually exist:

- ``fesom.recom_enable_3zoo2det``
- ``fesom.recom_enable_coccos``
- ``fesom.recom_ltra_diag``

AWI-ESM3 sets all three from ``recom_setting``, so you normally leave them alone. Their purpose is to stop XIOS writing files that would contain nothing but fill values.

Change the number of vertical levels for pressure level output of OpenIFS
=========================================================================

Applies to: AWI-CM3 v3.1 and later, and every AWI-ESM3. AWI-CM3 v3.0 has no IO server.

Output in controlled via `XIOS <https://forge.ipsl.jussieu.fr/ioserver>`_. The pressure levels onto which the data is interpolated from model levels is set in ``axis_def.xml``. In principle two options exist. Changing the number of levels for all 3D pressue level output fields and changing the number of levels only for some output fields.

For all fields
--------------

To change the number of layers for all 3D pressure level fields, in ``axis_def.xml`` in section ``<axis_group id="pl_axes" ...>``
modify ``n_glo="19"`` to the new number of layers, ``value="(0,18)`` to 0 nlayers-1 and subequently list the pressure levels in Pa.

For select fields
-----------------

For selective fitting, in the ``<axis id="pressure_levels_zoom"`` section, you can make a sub-selection of the levels previously defined in the ``<axis id="pressure_levels"`` section. In the existing example three layers are selected: ``<zoom_axis index="(0,2)[10 11 12]" />``. To write a field on this reduced vertical domain you have to define a new grid in ``grid_def.xml``, specifying as domain ``pressure_levels_zoom`` instead of ``pressure_levels``. With this new grid you go to ``file_def.xml`` and define a new file (copy paste from ``pressure level`` output to ``pressure level output zoom``, and select the new grid). Then you delete the variables that should not be written on all levels from the pressure level output and insert them at pressure level output zoom.
