/*
FIRST CREATED: 10/20/2021
CREATED BY: D. FEHDER
DESC: Process Execucomp Data
*/
*version 16
clear

log using lg-mk-cross-zip2cbsa.log, replace

run env_vars.do

****************************************************************
*      		IMPORT DATA AND PROCESS COUNTY TO CSA
****************************************************************

* Our county to CSA/MSA crosswalk comes from Bureau of Labor Stats. Downloaded 10/20/2021
* URL: https://www.bls.gov/cew/classifications/areas/county-msa-csa-crosswalk.htm

* import country to CSA codes
import excel "${raw}qcew-county-msa-csa-crosswalk.xlsx", sheet("qcew-county-msa-csa-crosswalk") firstrow allstring

* Create region codes and fill if county has a CSA Code
gen region_code = ""
replace region_code = CSACode if !missing(CSACode)

gen region_type = ""
replace region_type = "CSA" if !missing(CSACode)

gen region_title = ""
replace region_title = CSATitle if !missing(CSACode)

* Now fill with MSAs if missing CSA
replace region_code = MSACode if missing(region_code) & !missing(MSACode)
replace region_type = "MSA" if missing(region_type) & !missing(MSACode)
replace region_title = MSATitle if missing(region_title) & !missing(MSACode)

* Now fill with County if missing MSA or CSA
replace region_code = CountyCode if missing(region_code)
replace region_type = "COUNTY" if missing(region_type)
replace region_title = CountyTitle if missing(region_title)

drop if missing(region_code)

keep CountyCode CountyTitle region_code region_type region_title

rename CountyCode countycode

* now save a tempfile to enable future processing
tempfile county_cross
save `county_cross', replace 


****************************************************************
*      		IMPORT DATA AND PROCESS ZIP TO COUNTY
****************************************************************
clear
* Data comes from HUD (the Q4 2019 version). Downloaded 10/20/2021
* URL: https://www.huduser.gov/portal/datasets/usps_crosswalk.html

import excel "${raw}ZIP_COUNTY_122019.xlsx", sheet("zip_county_122019") firstrow allstring

rename ZIP zipcode
rename COUNTY countycode


****************************************************************
*      		MERGE AND FINALIZE CROSS WALK TO ZIPCODE LEVEL
****************************************************************

merge m:1 countycode using `county_cross'

tab _merge
keep if _merge == 3
drop _merge

collapse (first) region_type region_title, by(zipcode region_code)

* now save a tempfile to enable future processing
tempfile zip_cross
save `zip_cross', replace 

gen cnt=1
collapse (sum) cnt, by(zipcode)

merge 1:m zipcode using `zip_cross'

tab _merge
keep if _merge == 3
drop _merge

save "${inter}cross_zip2csa", replace



************************************
*	CLOSE LOG 
************************************
log close
