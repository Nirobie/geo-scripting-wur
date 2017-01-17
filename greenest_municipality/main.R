# Team 7
# Bob Souwer & Alejandro salazar
# 17-01-2017

library(rgdal)
library(raster)

source('R/find_greenest.R')

#Create directory and download the data
dir.create("data")
download.file("https://raw.githubusercontent.com/GeoScripting-WUR/VectorRaster/gh-pages/data/MODIS.zip",
              quiet = TRUE, destfile = 'data/MODIS.zip', method = 'auto')
#Extract the data
unzip('data/MODIS.zip', exdir = 'data')
#Remove zip file
file.remove('data/MODIS.zip')
#Load MODIS file
modis_files <- list.files(path = 'data', pattern = glob2rx('*.grd'), full.names = TRUE)
ndvi <- brick(modis_files)

#Download municipality data
nlMunicipality <- getData('GADM', country = 'NLD', level = 2, path = 'data')

#Reproject municipality (vector) data to MODIS (raster) projection
nlMunicipality_rep <- spTransform(nlMunicipality, CRS(proj4string(ndvi)))
#Multiply NDVI values by MODIS scale factor
ndvi <- ndvi*0.0001
#Extract NDVI values from MODIS data
ndvi_mun <- extract(ndvi, nlMunicipality_rep, sp = TRUE, df = TRUE, fun = mean, na.rm = TRUE)


#Find the greenest municipality in January
green_january <- greenest_by_month(ndvi_mun, "January")
green_january

plot(ndvi[[grep("January", colnames(ndvi@data@values))]], main = "Greenest municipality in January")
plot(nlMunicipality_rep[nlMunicipality_rep$NAME_2 == green_january,], add=T)
text(nlMunicipality_rep[nlMunicipality_rep$NAME_2 == green_january,],
     labels=green_january, pos=4, cex= 0.7)
     
#Find the greenest municipality in August
greenest_by_month(ndvi_mun, "August")

#Find the municipality which is in average greenest throughout the year
greenest_by_year(ndvi_mun)

#Find the greenest province in January
greenest_province(ndvi_mun, "January")
