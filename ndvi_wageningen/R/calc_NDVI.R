# Team 7
# Bob Souwer & Alejandro salazar
# 13-01-2017

# Calculate NDVI

ndvOver <- function(x, y) {
  ndvi <- (y - x) / (x + y)
  return(ndvi)
}