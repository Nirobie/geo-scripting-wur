# Team 7
# Bob Souwer & Alejandro salazar
# 11-01-2017

is.leap <- function(year) {
  # default to FALSE, and only set it to TRUE if it meets condition
  leapyear <- FALSE
  # check if input is numeric, give an error message if it is not
  if (!is.numeric(year)) {
    stop('That is not a numeric input!')
  }
  if (year >= 1582) {
    # year not divisible by 4
    if (year %% 4 != 0) {
    } 
    # year not divisible by 100 > set leapyear to TRUE
    else if (year %% 100 != 0) { 
      leapyear <- TRUE
    }
    # year not divisible by 400
    else if (year %% 400 != 0) {
    } 
    else {
      leapyear <- TRUE
    }
  }
  # check if argument year is part of Gregorian calendar
  else {
    leapyear <- paste(year, "is out of the valid range")
  }
  return(leapyear)
}