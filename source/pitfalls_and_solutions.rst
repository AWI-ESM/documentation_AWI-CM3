.. _chap_pitfall_and_solutions

Pitfalls and solutions
**********************
- You must use 4-digit experiment name, otherwise OpenIFS will be missing certaining input files
- You will likely want to use fesom salinity restoring = 0. Failing to do so will make your model not fully coupled as sss will be read from file. 
