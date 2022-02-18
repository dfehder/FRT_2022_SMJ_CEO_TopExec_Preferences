/*
FIRST CREATED: 10/20/2021
CREATED BY: D. FEHDER
DESC: Process Execucomp Data
*/
*version 16
clear

log using lg-proc-1-initialization.log, replace

* for use during testing. Comment out when moving to cluster
* cd /Users/danielfehder/dev/frt_2021b/preprocess_execucomp

run env_vars.do


****************************************************************
*      		IMPORT DATA AND INITIAL PROCESS
****************************************************************

import delimited "${raw}Execucomp.csv"

gen name_index = lower(exec_lname) + "+" + lower(exec_fname)
gen yob_yl = year - age

rename gender gender_exec
rename age age_exec
rename zip zipcode

list name_index in f/10


************************************
*	PROCESS LAST NAME
************************************

* get rid of all the modifiers (Jr, PhD etc) at the end of last names
split exec_lname, parse(",") generate(split_name)

tab split_name2
tab split_name3

gen name_last = lower(split_name1)
drop split_name*


************************************
*	PROCESS FIRST & MIDDLE NAME
************************************

* Process first names 
gen name_first_temp = lower(exec_fname)
* remove period from first names that have an initial
gen name_first = subinstr(name_first_temp, ".", "", .)
drop name_first_temp

* Process middle name to first initial lower case
gen name_middle_initial = lower(substr(exec_mname, 1, 1))

************************************
*	PROCESS GENDER
************************************

tab gender_exec

gen gender = 0
replace gender = 2 if gender_exec == "MALE"
replace gender = 1 if gender_exec == "FEMALE"

tab gender

drop gender_exec


* now save a tempfile to enable future processing
tempfile exec_full
save `exec_full', replace

************************************
*	PROCESS YOB
************************************

* There are slight variations across individual for YOB based on age when 
* the age is entered that year. We deal with this by averaging within individual
* across all years available

collapse (mean) yob_yl, by(execid)

rename yob_yl yob

merge 1:m execid using `exec_full'

tab _merge
keep if _merge == 3
drop _merge
* now drop the year level yob var
drop yob_yl

* save for future use
save `exec_full', replace

************************************
*	COLLAPSE TO INDIVIDUAL X ZIP 
************************************
* this code block gets rid of extra years of individuals 
* and gives only year X place unique hits

* get max year at the Exec X zip level
collapse (max) year, by(execid zipcode)

merge 1:m execid zipcode year using `exec_full'

tab _merge
keep if _merge == 3
drop _merge

* Number of Exec X Zipcode Observations (44,397)
sum execid


************************************
*	PREPARE FINAL DATA SET BASE
************************************

* observations without states are not US based observations (1,085 observations)
drop if missing(state)

* drop if there is no exec info
drop if missing(execid)

* drop the canadian states from the data
drop if state == "ON"
drop if state == "QC"
drop if state == "BC"
* drop puerto rico
drop if state == "PR"

* choose the final variables that will be outputted
keep execid exec_fullname name_last name_first ///
	 name_middle gender city state zipcode coname ///
	 salary bonus year ceoann yob gvkey

	 
* now save a tempfile to enable future processing
tempfile exec_final
save `exec_final', replace 
	 
************************************
*	ADD CBSA IDENTIFIERS
************************************ 


merge m:1 gvkey using "${inter}cross_gvkey2csa"

order execid exec_fullname name_last name_first ///
	  name_middle gender yob year salary bonus ///
	  ceoann coname gvkey city state zipcode 

tab _merge
keep if _merge == 3
drop _merge

save "${inter}execucomp_full", replace


************************************
*	CLOSE LOG 
************************************
log close
