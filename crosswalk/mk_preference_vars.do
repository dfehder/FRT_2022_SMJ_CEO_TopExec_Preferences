/*
FIRST CREATED: 11/03/2021
CREATED BY: D. FEHDER
DESC: Create the Preference Variable File
*/
version 16

* create log
log using lg-mk-preference.log, replace

* get environmental variables
run env_vars.do

****************************************************************
*      		AGG RAW DATA
****************************************************************

* initialize with the first data set
use "${combo}combine_inter_preferences_raw_1"

* now iterate and agg over the other combine files
forval i = 2/6 {
    * read in and append
    * TDL get rid of error generating requirement for force
    append using "${combo}combine_inter_preferences_raw_`i'", force
}

tempfile pref_agg
save `pref_agg', replace
****************************************************************
*      		IMPORT DATA AND PROCESS
****************************************************************
clear
import delimited "${final}full_matches.csv", varnames(1)

/* drop _merge */

* match to preferences
merge 1:1 lalvoterid using `pref_agg'

tab _merge

keep if _merge == 3
drop _merge
****************************************************************
*      		OUTPUT DATA FILES
****************************************************************
save "${final}execucomp_l2_matched", replace


****************************************************************
*      		CLOSE LOG
****************************************************************
log close