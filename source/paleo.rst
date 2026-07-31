.. _paleo:

Paleo equilibrium climate
*************************

AWI-CM3 can be run for a paleo time slice by rebuilding the OpenIFS boundary
conditions from a palaeogeographic reconstruction. The atmosphere sees a
different land-sea mask, orography, ice sheets, soils, lakes and vegetation;
everything else about the model stays as it is.

The rebuild is done with the `ocp-tool <https://github.com/JanStreffing/ocp-tool>`_,
the same tool used to fit the OpenIFS land-sea mask to a FESOM2 mesh. Its paleo
steps replace the older bash/CDO scripts.

There are two levels to this, and they cost very different amounts of effort:

**Level 1**: a new model resolution for a time slice that already exists.
The reconstruction is unchanged; only the OpenIFS grid changes. This is a
configuration change and a rerun of the tool, and is the common case when you
move a published setup from, say, TCO95 to TCO319.

**Level 2**: a new time slice.
You supply a new reconstruction, and you also have to decide on the forcings
that make it an equilibrium climate: greenhouse gases, orbit, and sea surface
conditions. The tool handles the boundary condition files; the rest is a
modelling decision.

Both levels are described below. Read :ref:`what_the_tool_changes` first. It
tells you which files come out and what has to agree with what.

.. _what_the_tool_changes:

What the tool produces
======================

With ``paleo.enabled: true`` the pipeline runs four extra steps after the
normal ones, writing into ``output/TCO{res}_{grid}/openifs_input_modified/``:

- Step 13 writes ``ICMGG{expid}INIT_{grid}``: the land surface. Ice sheets and
  snow, lakes, soils and soil water, vegetation type, cover and LAI, and a
  distance-weighted fill of every other surface field over points that changed
  between ocean and land.
- Step 14 writes ``ICMSH{expid}INIT_{exp_id}``: the spectral orography, as a
  paleo minus modern anomaly added to the existing field.
- Step 14b writes ``ICMCL{expid}INIT_{exp_id}``: the monthly albedo and LAI
  climatologies, given the same fill as the surface fields so that they agree
  with the new mask.
- Step 15 adds the subgrid-scale orography (``sdor``, ``isor``, ``anor``,
  ``slor``) to the ICMGG via ``calnoro``. It is skipped unless
  ``calnoro_binary`` is set.

Alongside these, the normal steps write the OASIS files
(``grids.nc``, ``areas.nc``, ``masks.nc``) into ``output/TCO{res}_{grid}/oasis_mct3_input/``.
Use them. They carry the same land-sea mask as the ICMGG, and a coupled run
whose coupler mask disagrees with its atmosphere mask will exchange fluxes
across points that no longer exist.

Where the land-sea mask comes from
----------------------------------

This catches people out. The mask is taken from the ocean model grid when
one is configured, because for a coupled run the FESOM2 mesh defines where the
ocean is. The reconstruction ``*_LSM_*.nc`` is only used when there is no ocean
mesh, i.e. in AMIP mode.

So for a coupled paleo run you need a FESOM2 mesh built for that time slice.
Pointing a coupled configuration at a modern mesh gives you modern geography no
matter what the reconstruction says. If you have no paleo mesh yet, an AMIP
setup is the way to get the atmosphere side moving.

The environment
===============

The tool needs a coherent cartopy/matplotlib/cmocean set. On levante:

..  code-block:: bash

  source ~/loadconda.sh
  conda activate ocp-tool2

Running with a bare ``python3`` tends to pick up a newer matplotlib from
``~/.local``, which breaks the plotting step and, in coupled mode, the step
that appends the FESOM grid to the OASIS files. Both failures look like tool
bugs and are not.

Level 1: a new resolution for an existing time slice
====================================================

The reconstructions are supplied on a regular 1x1 degree grid and are
interpolated to whatever Gaussian grid you ask for, so **the reconstruction
files do not change with resolution**. What changes is the OpenIFS template
the modifications are applied to.

- Obtain the unmodified OpenIFS input files for the new resolution: the
  ``ICMGG{expid}INIT``, ``ICMGG{expid}INIUA`` and ``ICMSH{expid}INIT`` of a
  standard experiment at that grid, plus the matching ``ICMCL{expid}INIT``.
- Link them into ``input/openifs_input_default/``. The names must match
  ``atmosphere.experiment_name``.
- Copy the config of the existing time slice and change
  ``atmosphere.resolution_list`` to the new truncation.
- Check ``atmosphere.model_cycle`` against the template you just linked (see
  :ref:`model_cycle` below).
- Run the tool, then copy the output files into the pool directory for the new
  resolution.

..  code-block:: bash

  cd $OCP_TOOL_DIR
  python3 run_ocp_tool.py configs/your_config.yaml

Do not reuse the OASIS ``rmp_`` weight files from the old resolution. They are
grid pair specific and have to be regenerated; for large grids see
:doc:`how_to` for the offline parallel weight generation.

.. _model_cycle:

Match the OpenIFS cycle
-----------------------

CY43R3 and CY48R1 lay their surface fields out differently. CY43R3 has a
single snow layer; CY48R1 has a five layer snowpack in different units, and
additionally reads bare soil albedo, a C4 photosynthesis map and an urban
cover field. Feeding a CY43R3 file to a CY48R1 executable aborts at startup:

..  code-block:: bash

  GRIDPOINT 3D FIELD MISSING:       228141           1
  ABOR1     [PROC=2,THRD=1] : IOSTREAM_MIX:GRID_IN - MISSING FIELD

Set the cycle explicitly and the tool will cross-check it against the input
file and refuse to continue on a mismatch:

..  code-block:: yaml

  atmosphere:
    model_cycle: "48r1"    # "43r3", "48r1" or "auto"

``auto`` detects the cycle from the input ICMGG. An explicit value is safer:
it turns a wrong input file into an error message from the tool rather than an
abort from the model an hour later.

Level 2: a new time slice
=========================

Here you supply the reconstruction. The tool expects these files, with
``{exp_id}`` replaced by ``paleo.experiment_id``:

- ``{exp_id}_LSM_v1.0.nc``: land-sea mask, 1 = land. Used in AMIP mode only,
  see above.
- ``{exp_id}_topo_v1.0.nc``: surface elevation in m.
- ``{exp_id}_icemask_v1.0.nc``: 1 = ice free, 2 = ice sheet.
- ``{exp_id}_lake_v1.0.nc``: lake cover.
- ``{exp_id}_soil_v1.0.nc``: soil type.
- ``{exp_id}_mbiome_v1.0.nc``: biome class, mapped to OpenIFS vegetation
  types, cover and LAI.
- ``Modern_std_topo_v1.0.nc``: modern elevation, subtracted to form the
  topography anomaly.
- ``Modern_std_soil_lake_v1.0.nc``: modern soil and lake reference.

All are on a regular 1x1 degree grid. The two ``Modern_std`` files are the
reference the anomalies are taken against and must come from the same
reconstruction family as the time slice, otherwise the anomaly contains the
difference between two different modern datasets as well as the paleo signal.

Configuration:

..  code-block:: yaml

  atmosphere:
    resolution_list: [95]
    truncation_type: "cubic-octahedral"
    experiment_name: "ab45"
    model_cycle: "48r1"

  ocean:
    grid_name: "CORE2"                      # or "AMIP" for an uncoupled run
    mesh_file: "/path/to/paleo/mesh.nc"     # must be the paleo mesh

  paleo:
    enabled: true
    experiment_id: "LP"
    reconstruction_dir: "/path/to/reconstruction/"
    modern_reference_dir: "/path/to/reconstruction/"
    icmsh_input_file: "/path/to/ICMSH{expid}INIT"
    calnoro_binary: null                    # path to enable step 15

The experiment id is not just a label
-------------------------------------

``experiment_name`` is written into the GRIB header of every message
(``experimentVersionNumber``). Build your paleo files from a template and they
inherit that template's id, so name them for the template they came from and
set ``prepifs_expid`` in the runscript to match. Do not build files called
``ICMGGaackINIT`` out of an ``ab45`` template: the filename and the header
will disagree and you will not notice until something else does.

What the tool does not decide for you
-------------------------------------

The boundary condition files are only part of an equilibrium climate setup.
You still have to set:

- **Greenhouse gases.** ``NAMECECMIP`` in the OpenIFS namelist, e.g.
  ``NCMIPFIXYR`` for a fixed year, or ``LANXCO2``/``RNXCO2`` for a multiple of
  the reference concentration.
- **Orbit.** For a time slice you almost always want a fixed orbit rather than
  the default ``variable_year``, either ``ORBMODE: 'fixed_year'`` with
  ``ORBIY``, or the PMIP4 parameters for the period entered directly under
  ``ORBMODE: 'fixed_parameters'``. See :ref:`orbital_parameters` for the modes
  and a worked LIG example.
- **Sea surface conditions.** For a coupled run these come from FESOM2. For an
  AMIP run you need SST and sea ice forcing for the time slice; a modern or
  pre-industrial AMIP forcing set with a paleo land-sea mask is not an
  equilibrium climate.
- **Vegetation.** The tool maps biomes to vegetation type, cover and LAI in the
  ICMGG. The monthly LAI cycle in the ICMCL is only relocated to match the new
  mask, not rebuilt from the biomes.

Using the files in a runscript
==============================

Point the OpenIFS input at the tool output:

..  code-block:: yaml

  oifs:
    prepifs_expid: ab45
    input_sources:
        ICMGG_INIT:  '/path/to/output/.../ICMGGab45INIT_AMIP'
        ICMGG_INIUA: '/path/to/output/.../ICMGGab45INIUA'
        ICMSH_INIT:  '/path/to/output/.../ICMSHab45INIT_LP'

The ICMCL is the exception. It is not an ``input_sources`` entry: esm-tools
builds ``ICMCL_INIT`` from two other variables, so an override placed in
``input_sources`` is silently discarded and you keep the modern climatology
without any warning. Override these instead:

..  code-block:: yaml

  oifs:
    icmcl_dir:  '/path/to/output/.../openifs_input_modified'
    icmcl_file: 'ICMCLab45INIT_LP'

The OASIS files go in the coupler input directory:

..  code-block:: yaml

  oasis3mct:
    lresume: false
    input_dir: '/path/to/output/.../oasis_mct3_input/'

Check that the model really used them
=====================================

A run that starts is not a run that used your files. After a short leg, in the
work directory:

..  code-block:: bash

  # the mask the model read, against the modern template
  grib_ls -p paramId ICMGG${expid}INIT | grep -c 172

  # the ICMCL that was staged: follow the link, do not trust the config
  readlink -f ICMCL${expid}INIT

  # the coupler mask must match the atmosphere mask
  ncdump -v A096.msk masks.nc | head

In ``NODE.001_01``, a CY48R1 run reading a correct multi-layer snowpack shows
five entries:

..  code-block:: bash

  GRIB CODE 228141 READ FROM GRIB FILE INTO SNOWG 01
  GRIB CODE     32 READ FROM GRIB FILE INTO SNOWG 02
  GRIB CODE     33 READ FROM GRIB FILE INTO SNOWG 03
  GRIB CODE    238 READ FROM GRIB FILE INTO SNOWG 04
  GRIB CODE 228038 READ FROM GRIB FILE INTO SNOWG 05

The land point count in the staged ICMGG should differ from the modern
template. If it does not, the reconstruction never reached the model. In a
coupled run that usually means the ocean mesh is a modern one.

Known limitations
=================

- The land-sea mask is interpolated from the 1 degree reconstruction by
  nearest neighbour, which systematically widens coastlines compared with the
  conservative remapping the older bash workflow used.
- The ICMCL monthly LAI is relocated, not rebuilt from the reconstruction
  biomes.
- ``calnoro`` needs a separately compiled Fortran binary. Without it the
  subgrid-scale orography stays that of the template, which is inconsistent
  with a modified topography.
