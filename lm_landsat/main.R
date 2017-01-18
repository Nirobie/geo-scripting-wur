# Team 7
# Bob Souwer & Alejandro salazar
# 13-01-2017

### To do list:
## remove outliers from data

# libraries
library(raster)

## Load data
load("data/GewataB1.rda")
load("data/GewataB2.rda")
load("data/GewataB3.rda")
load("data/GewataB4.rda")
load("data/GewataB5.rda")
load("data/GewataB7.rda")
load("data/vcfGewata.rda")

## Remove outliers from GeWata bands
alldata_landsat <- brick(GewataB1, GewataB2, GewataB3, GewataB4, GewataB5, GewataB7)
hist(alldata_landsat)

## Outliers correction (determined by eye)
GewataB1[GewataB1 > 800] <- NA
GewataB2[GewataB2 > 1050] <- NA
GewataB3[GewataB3 > 1400] <- NA
GewataB4[GewataB4 > 4000] <- NA
GewataB4[GewataB4 < 600] <- NA
GewataB5[GewataB5 > 3800] <- NA
GewataB7[GewataB7 > 2500] <- NA

## Outliers corection for VCF data (everything over 100 is NA)
vcfGewata[vcfGewata > 100] <- NA
hist(vcfGewata)

## Create rasterBrick from landsat7 bands and vcf data
alldata <- brick(GewataB1, GewataB2, GewataB3, GewataB4, GewataB5, GewataB7, vcfGewata)
names(alldata) <- c("band1", "band2", "band3", "band4", "band5", "band7", "VCF") 

## Extract all data to a data.frame
df <- as.data.frame(getValues(alldata))

## Relationship between landsat and vcf
pairs(alldata)

## Create the lm model
modellm <- lm(VCF ~ band1 + band2 + band3 + band4 + band5 + band7, data = df)
summary(modellm)

predLM <- predict(alldata, model=modellm, na.rm=TRUE)
plot(predLM)
plot(alldata$VCF)

## Calculated RMSE

rmse <-sqrt(mean((predLM-alldata$VCF)^2,na.rm=TRUE))
sq_diff_raster <- predLM-alldata$VCF

sq_diff <- as.data.frame(predLM-alldata$VCF)
rmse3 <- sqrt(mean(sq_diff$layer^2, na.rm = TRUE))

rmse2 <-sqrt(cellStats((predLM-alldata$VCF)^2, "mean", na.rm = T))

plot(sq_diff_raster)
