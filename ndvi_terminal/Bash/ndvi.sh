#!/bin/bash

## Team 7
## Alejandro Salazar & Bob Souwer
## 12-01-2017

cd ../data
echo "*Copy original file to tmp file"
cp LE71700552001036SGS00_SR_Gewata_INT1U.tif input.tif
echo "*Create variables for input and output file"
fn="input.tif"
outfn="ndvi.tif"
resample="resample_ndvi.tif"
reproject="reproject_ndvi.tif"
echo "* now apply gdal_calc: Command line raster calculator with numpy syntax"
gdal_calc.py -A $fn --A_band=4 -B $fn --B_band=3  --outfile=$outfn  --calc="(A.astype(float)-B)/(A.astype(float)+B)" --type='Float32'

echo "* resample to 60m"
gdalwarp -tr 60 60 -r near -overwrite $outfn $resample

echo "* Reproject to Lat/Long WGS84"
gdalwarp -t_srs EPSG:4326 -overwrite $resample $reproject

echo "* remove the input temporary file"
rm input.tif ndvi.tif