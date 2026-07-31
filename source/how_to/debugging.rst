*********
Debugging
*********

Use debug flags
===============

In case your model setup produces a segmentation fault it can be helpful to compile and run the model with debug flags. These can be set separatly for different executables in the coupled system. Here we mostly point you towards the locations that need to be modified in order to use debug flags. A comprehensive overview on which flags might help can be found at: https://doku.lrz.de/comparison-of-compiler-options-intel-vs-pgi-vs-gcc-11481685.html#ComparisonofCompilerOptions(intelvs.pgivs.gcc)-Diagnostics,RuntimeCheckingandDebugging

OpenIFS cy43r3 (AWI-CM3 v3.2 and below)
---------------------------------------
You can replace the OpenIFS Fortran compile and linker flags through esm_tools under ``esm_tools/configs/components/oifs/oifs.env.yaml`` by modifying ``OIFS_FFLAGS``. E.g:

.. code-block:: yaml

   oifs:
      compiletime_environment_changes:
         levante:
            add_export_vars:
               OIFS_FFLAGS: '"-r8 -fp-model precise -align array32byte -O3 -qopenmp -g -traceback -convert big_endian -march=core-avx2 -mtune=core-avx2"'

Make sure you pick the right HPC system and use flags that fit to the compiler which is being used (see compiletime log output).


OpenIFS cy48r1 (AWI-CM3 v3.3 and above)
---------------------------------------
TBA.


for FESOM2
----------
For FESOM2 it is currenty neccessary to modify the compiler settings in the source code folder inside the file ``awicm3-v3.2/fesom-2.5/src/CMakeLists.txt``. The exact path my vary with your model version. You will find inside a block with different FORTRAN flags depending on compiler ``Inter/GNU/Cray/NVHPC``, on whether FESOM2 is build as a library or executable, and sometimes on HPC system:

.. code-block:: CMake

   if(${CMAKE_Fortran_COMPILER_ID} STREQUAL  Intel )
      if(${BUILD_FESOM_AS_LIBRARY})
           target_compile_options(${PROJECT_NAME} PRIVATE -r8 -i4 -fp-model precise -no-prec-div -no-prec-sqrt -fimf-use-svml -xHost -ip -init=zero -no-wrap-margin -fpe0) # add -fpe0 for RAPS environment
      else()
           target_compile_options(${PROJECT_NAME} PRIVATE -r8 -i4 -fp-model precise -no-prec-div -no-prec-sqrt -fimf-use-svml -ip -init=zero -no-wrap-margin)
      endif()
      if(${FESOM_PLATFORM_STRATEGY} STREQUAL  levante.dkrz.de )
         target_compile_options(${PROJECT_NAME} PRIVATE -march=core-avx2 -mtune=core-avx2)
      elseif(${FESOM_PLATFORM_STRATEGY} STREQUAL  albedo)
         target_compile_options(${PROJECT_NAME} PRIVATE -march=core-avx2 -O3 -ip -fPIC -qopt-malloc-options=2 -qopt-prefetch=5 -unroll-aggressive) #NEC mpi option
      else()
         target_compile_options(${PROJECT_NAME} PRIVATE -xHost)
      endif()
   #    target_compile_options(${PROJECT_NAME} PRIVATE -g -traceback ) #-check all,noarg_temp_created,bounds,uninit ) #-ftrapuv ) #-init=zero)
   #    target_compile_options(${PROJECT_NAME} PRIVATE -qopenmp -r8 -i4 -fp-model precise -no-prec-div -no-prec-sqrt -fimf-use-svml -xHost -ip -g -traceback -check all,noarg_temp_created,bounds,uninit ) #-ftrapuv ) #-init=zero)
   #    target_compile_options(${PROJECT_NAME} PRIVATE -r8 -i4 -fp-model precise -no-prec-div -no-prec-sqrt -fimf-use-svml -ip -g -traceback -check all,noarg_temp_created,bounds,uninit ) #-ftrapuv ) #-init=zero)
   
   elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL  GNU )
   #    target_compile_options(${PROJECT_NAME} PRIVATE -O3 -finit-local-zero  -finline-functions -fimplicit-none  -fdefault-real-8 -ffree-line-length-none)
      target_compile_options(${PROJECT_NAME} PRIVATE -O2 -g -ffloat-store -finit-local-zero  -finline-functions -fimplicit-none  -fdefault-real-8 -ffree-line-length-none)
      if(CMAKE_Fortran_COMPILER_VERSION VERSION_GREATER_EQUAL 10 )
         target_compile_options(${PROJECT_NAME} PRIVATE -fallow-argument-mismatch) # gfortran v10 is strict about erroneous API calls: "Rank mismatch between actual argument at (1) and actual argument at (2) (scalar and rank-1)"
      endif()
   elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL Cray )
      if(${ENABLE_OPENMP})
         target_compile_options(${PROJECT_NAME} PRIVATE -c -emf -hbyteswapio -hflex_mp=conservative -hfp1 -hadd_paren -Ounroll0 -hipa0 -r am -s real64 -N 1023 -homp)
      else()
         target_compile_options(${PROJECT_NAME} PRIVATE -c -emf -hbyteswapio -hflex_mp=conservative -hfp1 -hadd_paren -Ounroll0 -hipa0 -r am -s real64 -N 1023 -hnoomp)
      endif()
   elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL NVHPC )
      target_compile_definitions(${PROJECT_NAME} PRIVATE ENABLE_NVHPC_WORKAROUNDS)
      target_compile_options(${PROJECT_NAME} PRIVATE -fast -fastsse -O3 -Mallocatable=95 -Mr8 -pgf90libs)
      if(${ENABLE_OPENACC})
         # additional compiler settings
         target_compile_options(${PROJECT_NAME} PRIVATE -acc -ta=tesla:${NV_GPU_ARCH} -Minfo=accel)
         set(CMAKE_EXE_LINKER_FLAGS "-acc -ta=tesla:${NV_GPU_ARCH}")
      endif()
      if(${ENABLE_OPENMP})
         target_compile_options(${PROJECT_NAME} PRIVATE -Mipa=fast)
      else()
         target_compile_options(${PROJECT_NAME} PRIVATE -Mipa=fast,inline)
      endif()
   endif()

In order to change the compiler settings you replace the ``target_compile_options`` that are currently used with the ones that you would like to have. Make sure you pick the right HPC system and use flags that fit to the compiler which is being used (see compiletime log output). Typical debug flags for e.g. Intel would be ``-g -traceback -check all,noarg_temp_created,bounds,uninit``. 

for XIOS
--------

For the IO server debug flags can be set inside the xios source code folder at: ``awicm3-v3.2/xios/arch.fcm``. The exact path may vary by model version. Here you want to add some of the DEV and DEBUG flags to the BASE flags for Fortran or C, as appropriate:

.. code-block:: CMake

   %BASE_CFLAGS    -std=c++11 -diag-disable 1125 -diag-disable 279 -D__XIOS_EXCEPTION
   %PROD_CFLAGS    -O3 -D BOOST_DISABLE_ASSERTS -march=core-avx2 -mtune=core-avx2
   %DEV_CFLAGS     -g -traceback
   %DEBUG_CFLAGS   -DBZ_DEBUG -g -traceback -fno-inline
   
   %BASE_FFLAGS    -D__NONE__
   %PROD_FFLAGS    -O3 -march=core-avx2 -mtune=core-avx2
   %DEV_FFLAGS     -g -O2 -traceback
   %DEBUG_FFLAGS   -g -traceback
