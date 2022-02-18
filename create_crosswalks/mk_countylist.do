/*
FIRST CREATED: 10/23/2021
CREATED BY: D. FEHDER
DESC: loop over all combined files and get the names of counties
*/
version 16


log using lg-stata-mk-county-cnts.log, replace

****************************************************************
*      		START WITH FIRST DATA SET
****************************************************************
* change to the directory with the data
cd /project/fehder_718/frt_2021b_data/inter/l2_processing/combined

use combine_inter_l2_match_1

* GET UNIQUE COUNTY LABELS AND CREATE COUNTER
*gen county_code  = address_county + " " + address_state
gen vid = substr(lalvoterid, 4,2)
egen county_code = concat(vid address_county address_fips), punct(" ")
gen cnt= 1

* NOW COLLAPSE TO COUNTY AND COUNT
collapse (first) address_fips (sum) cnt, by(county_code vid)

* now save a tempfile to enable future processing
tempfile county_cross
save `county_cross', replace 

forval i = 2/6 {
	* read in the rest of the files and append
	clear
	use combine_inter_l2_match_`i'
	
	* GET UNIQUE COUNTY LABELS AND CREATE COUNTER
	gen vid = substr(lalvoterid, 4,2)
	egen county_code = concat(vid address_county address_fips), punct(" ")
	gen cnt= 1

	* NOW COLLAPSE TO COUNTY AND COUNT
	collapse (first) address_fips (sum) cnt, by(county_code vid)
	
	append using `county_cross', force
	save `county_cross', replace

}

save county_counts, replace

****************************************************************
*      		CLOSE LOG
****************************************************************
log close
