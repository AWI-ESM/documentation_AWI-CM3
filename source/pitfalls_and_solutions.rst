.. _chap_pitfall_and_solutions

Pitfalls and solutions
**********************
- You must use 4-digit experiment name, otherwise OpenIFS will be missing certaining input files
- You will likely want to use fesom salinity restoring = 0. Failing to do so will make your model not fully coupled as sss will be read from file. 
- Your runscript must contain it's own name as a variable. Example: scriptname=awicm3-tutorial.run
- Make sure your runscripts "export FUNCTION_PATH" is pointing towards the right installation of the esm-master tool. Otherwise you may see errors that seemingly are not influenced by your modifications of the .functions files
