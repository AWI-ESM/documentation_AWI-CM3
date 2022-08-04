.. _chap_contribute

Contribute
**********

AWI-CM3 is assembled on the fly from the various git repositories of the constituent models. There are two ways to use and modify AWI-CM3.

Personal changes
----------------
If you want to work with AWI-CM3 scientifically, and need to make small modifications to the model or one of it's components in order to do so, the recommendation is to start from the latest tagged version. You will receive a well tested model, that was tuned for one or two major model resolutions, which is stable in time. No one else will modify your model version. 

In practice you create a git branch based on the tagged version, use it, and then move on. For example like this:

.. code-block:: Bash
   
  master
  v3.0
  v3.1
    L> v3.1+myfeature


*If you want your feature to be used in the long term, this is not the best way to contribute, instead look at the permanent features section.*

Permanent features
-----------------

If you want to do model development work on AWI-CM3, and you want your features or improvements to stick around long term, the recommendation is to start from the master version. 

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
  
Eventually the master branch will have so many or such important new features merged back, that we decide to make a new model version out of the master branch. A prep-release branch will be created, the model might be retuned if necessary, and a standard set of climate simulations and diagnostics will be run: https://github.com/AWI-CM3/release_evaluation_tool
  
*If you want your feature to be used for you next paper as soon as possible, this is not the best way to contribute, instead look at the personal changes section.*
