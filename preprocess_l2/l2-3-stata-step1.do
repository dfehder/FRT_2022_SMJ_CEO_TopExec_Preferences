/*
CREATED: 7/12/2021
DESC: Import the data sets and then turn into stata files
CREATED BY: D. C. FEHDER
*/
version 16

* create log
log using lg-stata-step1-`1'-`2'.log, replace

* get environmental variables
run env_vars.do

* change to the directory with the data
cd /project/fehder_718/frt_2021b_data/inter/l2_processing/combined

* the parameters are 1: the dataset & 2: the chunk number
import delimited combine_inter_`1'_`2'.csv

****************************************************************
*      		PROCESS STRING VARS TO LOWER CASE
****************************************************************

* define the list of string variables that need to be lower cased
local svars name_first name_last name_middle

foreach s of local svars {
    gen `s'_match = lower(`s')
    drop `s'
    rename `s'_match `s'
}

* Process middle name to first initial lower case
gen name_middle_initial = lower(substr(name_middle, 1, 1))

****************************************************************
*      		EXTRACT YEAR OF BIRTH (YOB)
****************************************************************

gen yob = substr(dob, -4, .)
destring yob, replace

****************************************************************
*      		PROCESS TO CSA
****************************************************************

* create the County identifier
gen vid = substr(lalvoterid, 4,2)
egen county_code_l2 = concat(vid address_county address_fips), punct(" ")

merge m:1 county_code_l2 using "${inter}cross_l2county2csa"

tab _merge
* drop the non-matches since all of the master data are matched
keep if _merge == 3
drop _merge

****************************************************************
*      		DROP UNNECESARRY VARIABLES
****************************************************************

drop county_code_l2 vid CountyTitle address_county address_state address_city address_fips

****************************************************************
*      		EXPORT
****************************************************************

* now save as a stata file
save combine_inter_`1'_`2', replace

clear

****************************************************************
*      		CLOSE LOG
****************************************************************

log close