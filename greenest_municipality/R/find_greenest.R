# Team 7
# Bob Souwer & Alejandro salazar
# 17-01-2017

greenest_by_month <- function(ndvi, month) {
  #Gets the column number of the input month
  mo <- grep(month, colnames(ndvi@data))
  #Gets the maximum monthly value
  maxndvi <- max(ndvi@data[,mo])
  #find municipality with max ndvi value
  greenest <- ndvi@data$NAME_2[ndvi@data[,mo] == maxndvi]
  return(greenest)
}

greenest_by_year <- function(ndvi) {
  #Gets the column number of the input month
  ndvi@data$YEARAVG <- rowMeans(ndvi@data[,16:27])
  #Gets the maximum monthly value
  maxndvi <- max(ndvi@data$YEARAVG)
  #find municipality with max ndvi value
  greenest_yr <- ndvi@data$NAME_2[ndvi@data$YEARAVG == maxndvi]
  return(greenest_yr)
}

greenest_province <- function(ndvi, month) {
  #Aggregate monthly NDVI data to provinces
  ndvi_prov <- aggregate(ndvi, by = 'NAME_1', sums = list(list(mean, 16:27)))
  #Gets the column number of the input month
  mo <- grep(month, colnames(ndvi_prov@data))
  #Gets the maximum monthly value
  maxndvi <- max(ndvi_prov@data[,mo])
  #find province with max ndvi value
  greenest_prov <- ndvi_prov@data$NAME_1[ndvi_prov@data[,mo] == maxndvi]
  return(greenest_prov)
}
