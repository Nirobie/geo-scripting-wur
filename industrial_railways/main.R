# Team 7
# Bob Souwer & Alejandro salazar
# 16-01-2017

library(rgdal)
library(rgeos)

source('R/buffer_type.R')
source('R/point_intersect.R')

dir.create("data/")
download.file("http://www.mapcruzin.com/download-shapefile/netherlands-places-shape.zip", 
              destfile = "data/netherlands-places-shape.zip", method = "auto", quiet =TRUE)
download.file("http://www.mapcruzin.com/download-shapefile/netherlands-railways-shape.zip", 
              destfile = "data/netherlands-railways-shape.zip",  method = "auto", quiet =TRUE)

unzip("data/netherlands-places-shape.zip", exdir = "data/")
unzip("data/netherlands-railways-shape.zip", exdir = "data/")

places <- readOGR("data/places.shp")
railways <- readOGR("data/railways.shp")

#Projection for buffering
prj_string_RD <- CRS("+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889
                       +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel
                       +towgs84=565.2369,50.0087,465.658,-0.406857330322398,0.350732676542563,
                       -1.8703473836068,4.0812 +units=m +no_defs")

#Reprojects the dataset 
railways_projRD <- spTransform(railways, prj_string_RD)
places_projRD <- spTransform(places, prj_string_RD)

#Select industrial type and create 1000m buffer
industrial_buffer <- buffer_type(railways_projRD, "industrial", 1000)

#Call the intersect function
int_places <- point_intersect(places_projRD, industrial_buffer)

#Plot the industrial railway buffer and intersection city
plot(industrial_buffer, main="City inside industrial railway buffer zone", col = "Grey40")
box()
plot(int_places, add=T, col="red")
text(int_places, labels=int_places$name, pos=4, cex= 0.7)
legend("bottomright", inset=.02, cex=0.8, c("Industrial railway buffer"), fill="Grey40", title="Legend")

#Return Utrecht's population value
int_places@data$population[int_places@data$name == "Utrecht"]

