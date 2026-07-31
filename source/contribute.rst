.. _chap_contribute

Contribute
**********

AWI-CM3 and AWI-ESM3 are assembled on the fly from the various git repositories of the constituent models. There are two ways to use and modify either of them, and they apply equally to the ``-cc`` and ``-is`` variants.

Personal model changes
----------------
If you want to work with one of these models scientifically, and need to make small modifications to the model or one of it's components in order to do so, the recommendation is to start from the latest tagged version. You will receive a well tested model, that was tuned for one or two major model resolutions, which is stable in time. No one else will modify your model version. 

In practice you create a git branch based on the tagged version, use it, and then move on. For example like this:

.. code-block:: Bash
   
  master
  v3.0
  v3.1
    L> v3.1+myfeature


*If you want your feature to be used in the long term, this is not the best way to contribute, instead look at the permanent features section.*

Permanent model features
-----------------

If you want to do model development work on either model, and you want your features or improvements to stick around long term, the recommendation is to start from the master version of the component repositories.

.. code-block:: Bash
   
  master
    L> master+myfeature
    L> master+someones_elses_feature1
    L> master+someones_elses_feature2
  v3.0
  v3.1

You will receive the latest version of all model components, including features by colleagues that may or may not work fully. While this can be a bit of a hassle, continuous integration should keep the worst errors at bay. Once you have finished developing and testing your feature, you merge back into the master branch. 

.. code-block:: Bash
   
  master
    L> prep_release_v3.2
        L> v3.2
  v3.0
  v3.1
  
Eventually the master branch will have so many or such important new features merged back, that we decide to make a new model version out of the master branch. A prep-release branch will be created, the model might be retuned if necessary, and a standard set of climate simulations and diagnostics will be run: https://github.com/AWI-ESM/release_evaluation_tool2

Releases carry all three numbers, always ``v3.5.0`` and never ``v3.5``. The early versions v3.0 to v3.2 were named with two, which is why they invite the question of whether ``v3.2`` tracks the newest ``v3.2.x``. It does not, and no other name does either, so the three number form has been used from v3.3.0 onward to stop the question being asked. A two number version names a line of releases rather than anything you can install. See :doc:`model_family` for what that means when you pick a target.
  
*If you want your feature to be used for you next paper as soon as possible, this is not the best way to contribute, instead look at the personal changes section.*

Improving the documentation
---------------------------

To improve this documentation, head over to https://github.com/AWI-ESM/documentation. The documentation is written in reStructuredText. You can edit the documentation online on github, which can be helpful to see the reStructuredText parsed in the preview window. If you want to add files and folders, cloning the repository onto your hard-drive of choice and modifying in shell is likely more intuitive. Please refrain form adding many/large files.

Regardless of whether you work online or on your local copy, you then need to create a new branch since ``main`` is protected, commit your modifications, and create a merge request. You can preview your merge request build version of the documentation thanks to CI/CD.

Marking what a section applies to
---------------------------------

This documentation covers AWI-CM3 and AWI-ESM3 together, including the ``-cc`` and ``-is`` variants, so a reader has to be able to tell at a glance whether what they are reading is meant for them. A section that applies everywhere says nothing about it. A section that does not opens with a single line naming its scope:

.. code-block:: text

   Applies to: AWI-CM3 v3.2 through v3.3.1 only.

A line earns its place when it names a **version boundary**, because that is the thing a reader cannot work out for themselves. Do not add one that only restates the page it sits on: a section about branching off an LPJ-GUESS restart, on a page called LPJ-GUESS, does not need to be told it requires LPJ-GUESS.

Where a scope really is about a component or a feature switch rather than a version, write it that way, because that is how esm_tools gates them in ``choose_version`` and it stays correct when a new variant appears.

Some older sections still carry their scope in the heading instead, for example ``Control Aerosol Scaling (AWI-CM3 v3.2 and v3.3)``. Those are being migrated to the line above. Do not write new ones in that form.

What belongs here and what belongs in an issue
-----------------------------------------------

This is a set of curated guides, not a database of errors. The test before you add something is whether it would still be true in two years, and whether a new user will hit it without having done anything wrong.

Both yes and it belongs here. That ``interactive_mesh: true`` is accepted on any awiesm3 version but silently does nothing unless the coupling string also carries PISM will not stop being true, it catches everybody exactly once, and its whole value is being findable when somebody pastes an error into a search box.

Otherwise it is a ticket. One run that crashed, a bug that will be fixed next month, or a problem that only appears on one person's branch belongs in the issue tracker of whichever repository is at fault. Runtime errors and their recommended fixes have their own home at https://github.com/AWI-ESM/common-errors.
