* This dofile generates yearly Federal and state EITC parameters using TAXSIM (local V35)
* help taxsimlocal35
* mstat : Marital Status 1 single, 2 married
* depx : number of dependents/children
* state : SOI code state 1-51
* plateau : maximum Federal EITC benefit per year
* phasein : Federal phase-in AGI. Plateau starts at this level of income.
* phaseout : Federal phase-out AGI. Plateau ends at this level of income.
* maxagi : Maximum qualifying AGI.
* plateau_state : State level maximum benefit
* phasein_state : State level phase-in of maximum benefit.
* phaseout_state: State level phase-out of maximum benefit.
* Notice state level EITC may have its own structure.

clear
local k "year mstat depx state plateau phasein phaseout maxagi"
foreach v of local k {
	gen `v' =.
}


forvalues y = 1987(1)2022 {
	di "Year `y'"	
	forvalues s = 1/51{
		di "State: `s'"
			
		forvalues d = 0/3 {			
			
			preserve
			clear
			set obs 901
			gen state = `s'
			gen year = `y'
			gen mstat = 1
			gen depx = `d'
			gen pwages = (_n-1)*100
			
			expand 2 , gen(k)
			replace mstat = mstat+1 if k==1
			gen dep18=depx


taxsimlocal35 , full replace
keep pwages year mstat depx state v25 v39
rename v25 maxeitc
rename v39 maxeitc_state

egen plateau = max(maxeitc)
gen i = pwages if plateau==maxeitc
egen phasein = min(i) , by(mstat)
egen phaseout = max(i) , by(mstat)
drop i
egen maxagi = max(pwages) if maxeitc>0 , by(mstat)

egen plateau_state = max(maxeitc_state) , by(mstat)
gen i = pwages if plateau_state==maxeitc_state & maxeitc_state!=0
egen phasein_state = min(i) , by(mstat)
egen phaseout_state = max(i) , by(mstat)

drop if maxagi ==.

keep year mstat state depx maxagi plateau* phasein* phaseout*

	qui count
	if `r(N)' == 0 {
		set obs 2
		replace state		= `s'
		replace year		= `y'
		replace mstat		= _n
		replace depx		= `d'
		replace phasein		= 0
		replace phaseout	= 0
		replace maxagi		= 0
		replace plateau		= 0
	}

	
	replace plateau_state = 0	if plateau_state==.
	replace phasein_state =0	if phasein_state==.
	replace phaseout_state =0	if phaseout_state==.

duplicates drop year mstat depx state , force

tempfile b
save `b' , replace
restore

append using `b'
			}
		}
	}

