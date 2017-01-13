# Team 7
# Bob Souwer & Alejandro salazar
# 13-01-2017

library(raster)

source('R/intersect_files.R')
source('R/correct_cloudcover.R')
source('R/calc_NDVI.R')
source('R/compare_NDVI.R')

## unpack data in folder data
untar("data/LC81970242014109-SC20141230042441.tar.gz", exdir = "data")
untar("data/LT51980241990098-SC20150107121947.tar.gz", exdir = "data")

## write the full names of all the files to a variable
landsat5list <- list.files(path = 'data', pattern = glob2rx('LT*.tif'), full.names = T)
landsat8list <- list.files(path = 'data', pattern = glob2rx('LC*.tif'), full.names = T)

## Make a RasterStack of all the different layers
landsat5 <- stack(landsat5list)
landsat8 <- stack(landsat8list)

## Make sure both rasters have the same extent, by using intersect
landsat5_ext <- intersect_r(landsat5, landsat8)
landsat8_ext <- intersect_r(landsat8, landsat5)

## Check if the intersect function worked properly
compareRaster(landsat5_ext, landsat8_ext, extent=T)

## Extract the cfmask and write it to a variable
fmask5 <- landsat5_ext[[1]]
fmask8 <- landsat8_ext[[1]]
## Remove the cfmask layer
landsat5_nocf <- dropLayer(landsat5_ext, 1)
landsat8_nocf <- dropLayer(landsat8_ext, 1)

## Remove cloudcover using the cfmask layer, with function cloudcover
landsat5CloudFree <- overlay(x = landsat5_nocf, y = fmask5, fun = cloudcover)
landsat8CloudFree <- overlay(x = landsat8_nocf, y = fmask8, fun = cloudcover)

## Calculate NDVI using function ndvOver
ndviland_sat5 <- overlay(x=landsat5CloudFree[[5]], y=landsat5CloudFree[[6]], fun=ndvOver)
ndviland_sat8 <- overlay(x=landsat8CloudFree[[4]], y=landsat8CloudFree[[5]], fun=ndvOver)

plot(ndviland_sat5, main="NDVI Wageningen 1990", axes=T)
plot(ndviland_sat8, main="NDVI Wageningen 2014", axes=T)
## Substract the two different NDVI calculations
ndvi8_5 <- substract(ndviland_sat8, ndviland_sat5)

## Plot result
plot(ndvi8_5, main="Difference in NDVI Wageningen 2014 - 1990", axes=T)

