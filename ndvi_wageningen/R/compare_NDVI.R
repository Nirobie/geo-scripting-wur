# Team 7
# Bob Souwer & Alejandro salazar
# 13-01-2017

# Substract two NDVI Rasterimages

substract <- function(x, y) {
  ndvi_time <- x-y
  return(ndvi_time)
}