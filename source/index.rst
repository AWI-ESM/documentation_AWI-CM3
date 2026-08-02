.. AWI-CM3 / AWI-ESM3 documentation master file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**********************************
AWI-CM3 and AWI-ESM3 documentation
**********************************

Welcome to the documentation of the Alfred Wegener Institute climate models AWI-CM3 and AWI-ESM3.

AWI-CM3 is a coupled atmosphere ocean general circulation model (AOGCM) based on `OpenIFS <https://www.ecmwf.int/en/research/projects/openifs>`_ and `FESOM2 <https://fesom.de/models/fesom20/>`_, and is one possible configuration of the larger `EC-Earth4 <http://www.ec-earth.org/>`_ model framework. AWI-ESM3 is AWI-CM3 with interactive vegetation from `LPJ-GUESS <https://web.nateko.lu.se/lpj-guess/>`_ added, and in its ``-cc`` and ``-is`` variants it becomes a full carbon cycle model or an ice sheet coupled model respectively.

These are not separate models with separate manuals. They share their atmosphere, their ocean, their coupler and almost all of their configuration, so this documentation covers all of them in one place. A section that does not apply to every setup opens with an ``Applies to:`` line; a section without one applies everywhere. If you are not sure which setup you are running, or what the difference between AWI-CM3-v3.4 and AWI-ESM3-v3.4 is, start at :doc:`model_family`.

Getting help
============

If the answer is not on this site, the components have their own public trackers, and asking the people who wrote the component is usually quicker than asking us:

- FESOM2: https://github.com/FESOM/fesom2/issues
- REcoM: https://github.com/RECOM-Regulated-Ecosystem-Model/REcoM/issues
- esm_tools: https://github.com/esm-tools/esm_tools/issues
- OpenIFS: ECMWF's OpenIFS space at https://confluence.ecmwf.int/display/OIFS

For anything specific to AWI-CM3 or AWI-ESM3 rather than to one of its components, and for the group's own discussions, see https://github.com/AWI-ESM/project_management. Several hundred past and present issues are collected there, so it is worth searching before you ask anywhere else. That repository is private, so ask one of the AWI staff named in :doc:`before_you_start` if you cannot reach it.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   model_family
   before_you_start
   quickstart
   releases
   contribute
   how_to
   paleo
   workfolder
