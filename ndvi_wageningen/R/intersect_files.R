# Team 7
# Bob Souwer & Alejandro salazar
# 13-01-2017

# Intersection of two (stacked) raster files, to get the same extent

intersect_r <- function(x,y) {
  raster_int <- intersect(x,y)
return(raster_int)
}