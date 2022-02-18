/*
FIRST CREATED: 10/24/2021
CREATED BY: D. FEHDER
DESC: PROCESS RAW EXECUCOMP FILE DOWN TO UNIQUE ADDRESSES AND COMPANIES
*/
clear

* change directories to dev path during local development
cd /Users/danielfehder/dev/frt_2021b/create_crosswalks/

* get environmental variables
run env_vars.do

****************************************************************
*      		FINALIZE THE EXECUCOMP CROSS WALK
****************************************************************

import delimited exec_gvkey_county_final.csv, varnames(1)
drop if in_sample == 0
keep gvkey coname countycode

merge m:1 countycode using "${inter}cross_county2csa"

tab _merge

* drop the non-matches since all of the master data are matched
keep if _merge == 3
drop _merge

save "${inter}cross_gvkey2csa", replace

****************************************************************
*      		FINALIZE THE EXECUCOMP CROSS WALK
****************************************************************
clear
import delimited l2_county_final.csv, varnames(1)

keep county_code_l2 countycode state_code

* check for duplicates
duplicates report countycode
duplicates list countycode

merge 1:1 countycode using "${inter}cross_county2csa"

tab _merge

* drop the non-matches since all of the master data are matched
keep if _merge == 3
drop _merge

save "${inter}cross_l2county2csa", replace
