import zipfile, urllib2
from os import path, remove

## Function to download required files and unpack them to the data folder

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
