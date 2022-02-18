# Execucomp to L2 Matched Crosswalk

This code provides the steps used in Fehder, Raffiee, and Teodoridis (2022) to generate the data set discussed in the paper. The code produces the crosswalk between Execucomp and L2 data set (fileref). If you want access to a csv or stata file containing the crosswalk and also the preference variables described in the paper, please email one of the co-authors with proof of license for the L2 data for yourself or your institution. 

## Overview of the Matching Process ##

The figure below describes the flow of the code for the matching process contained in this repository. This can be used to match executives in Execucomp to the L2 data or it can be adapted to match any two large data sets for which there is limited overlap in variables. For more details, please refer to Fehder, Raffiee, and Teodoridis (2022).

![Flowchart of data flow in repo](https://github.com/ideology-innovation/frt_2021b/blob/main/MatchingFlowchart.jpg)

## Initial Data Sets Used ## 

1. **L2 data** – Voter registration data for the US.

2. **Execucomp data** – The panel data of all the executives of the companies in the US.

  ## Steps to Run the Code ##

(Before running the code, change the file and folder paths in .env file if required)

1. Run the preprocessing code for execucomp data, use the following command in the preprocess_execucomp folder:  ```sbatch preprocess_execucomp.job```
2. Run the preprocessing code for voter dataset, use the following command in the preprocess_l2 folder: ```sbatch l2-0-master.job```
3. Perform record linkage, use the following command in the fastlink folder: ```sbatch run_fastlink.job```
4. Create final crosswalk, use the following command in crosswalk folder: ```sbatch agg_match.job```




