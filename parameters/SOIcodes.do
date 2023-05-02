htmltab2stata , url(https://taxsim.nber.org/statesoi.html)
rename myvar1 state_soi
rename myvar2 state_name
destring state_soi, replace

replace state_name = strtrim(state_name)
replace state_name = "District of Columbia" if state_name=="DC"
replace state_name = "North Carolina" if state_name=="NorthCarolina"
replace state_name = "South Carolina" if state_name=="SouthCarolina"
replace state_name = "New Hampshire" if state_name=="NewHampshire"
replace state_name = "New Jersey" if state_name=="NewJersey"
replace state_name = "New Mexico" if state_name=="NewMexico"
replace state_name = "New York" if state_name=="NewYork"
replace state_name = "North Dakota" if state_name=="NorthDakota"
replace state_name = "Rhode Island" if state_name=="RhodeIsland"
replace state_name = "South Dakota" if state_name=="SouthDakota"
replace state_name = "West Virginia" if state_name=="WestVirginia"
replace state_name = strtrim(state_name )

statastates, name(state_name) nogen
labmask state_soi, value(state_name)
labmask state_fips, value(state_name)

 export delimited using "US_soitofips", nolabel replace
