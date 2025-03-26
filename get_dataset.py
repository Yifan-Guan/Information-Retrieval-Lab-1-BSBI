import urllib.request
import zipfile

data_url = 'http://web.stanford.edu/class/cs276/pa/pa1-data.zip'
data_dir = 'pa1-data'
urllib.request.urlretrieve(data_url, data_dir+'.zip')
zip_ref = zipfile.ZipFile(data_dir+'.zip', 'r')
zip_ref.extractall()
zip_ref.close()