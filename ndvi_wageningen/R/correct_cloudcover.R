# Team 7
# Bob Souwer & Alejandro salazar
# 13-01-2017

# Correct for cloudcover

cloudcover <- function(x, y){
  x[y != 0] <- NA
  return(x)
}