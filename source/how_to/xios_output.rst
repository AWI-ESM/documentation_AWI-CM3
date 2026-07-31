***********
XIOS output
***********

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
