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
*      		IMPORT DATA AND SUBSET TO COMPANY LEVEL
****************************************************************

import delimited "${raw}Execucomp.csv"

* create address variable
egen full_address = concat(address city state zip), punct(", ")

gen full_address = address + ", " + city + ", " + state + " " + zip

* collapse with gvkey and address in case one firm has muliple addresses
collapse (first) coname, by(full_address gvkey)

order gvkey coname full_address

* check for duplicates
duplicates report gvkey

* now save the data
save company_address, replace
