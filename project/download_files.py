import zipfile, urllib2
from os import path, remove

## Download required files and unpack them to the data folder

def downloadData(url, foldername):
	response = urllib2.urlopen(url)
	zipcontent = response.read()
	filename = path.basename(url)
	with open(filename, 'w') as f:
    		f.write(zipcontent)

	zip_ref = zipfile.ZipFile(filename, 'r')
	zip_ref.extractall("data/" + foldername)
	zip_ref.close()
	remove(filename)

## cities url : 'http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_ua10_500k.zip'
## states url : 'http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_state_500k.zip'
## folder names: us_states us_cities