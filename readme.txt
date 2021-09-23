This guide will explain what is required to run the software produced in this project. Specifically, it will be explained how to run the final build, although the same pre-requisites are required for most code in this project.
All scripts were written in python 3.7.6. All scripts which compare crystals require the following libraries to be installed:
•	Python’s standard libraries (eg. time)
•	Numpy
•	Pandas
•	CCDC
Numpy and Pandas can easily be downloaded and installed through a library manager such as pip or conda. CCDC on the other hand, which is the Cambridge Structural Database API, must be down-loaded manually, it can then be installed with a library manager. An official guide on how to do this is available online.
A license and product key (provided by CSD) are required to download and use the CCDC library. These must be applied for. Academic institutions qualify for the full CSD enterprise level package, which also give the user access to crystal data (stored in CIF files). It also provides access to the soft-ware: Mercury, which this project used for validation testing.
Once all the pre-requisite libraries have been installed, any of the scripts can be ran. Most accept the input of a directory of CIF files, and output two csv files containing the RMSD and Matched mole-cules values for each pair of crystals in that directory.
The final build is a function which accepts the following inputs:
•	File directory of exclusively CIF files (string)
•	Packing shell size parameter value (integer /optional)
•	Distance tolerance parameter value (integer /optional)
•	Angle tolerance parameter values (integer /optional)

