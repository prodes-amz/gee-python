import datetime
import ee.mapclient


def NDVI(image):
 """A function to compute NDVI."""
 return image.expression('float(b("B4") - b("B3")) / (b("B4") + b("B3"))')


def SAVI(image):
 """A function to compute Soil Adjusted Vegetation Index."""
 return ee.Image(0).expression(
  '(1 + L) * float(nir - red)/ (nir + red + L)',
  {
   'nir': image.select('B4'),
   'red': image.select('B3'),
   'L': 0.2
  })


if __name__ == '__main__':
 ee.Initialize()

 # Filter the L7 collection to a single month.
 collection = (ee.ImageCollection('LANDSAT/LE07/C01/T1_TOA')
               .filterDate(datetime.datetime(2020, 1, 1),
                           datetime.datetime(2020, 7, 31)))

 vis = {
  'min': 0,
  'max': 1,
  'palette': [
   'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163',
   '99B718', '74A901', '66A000', '529400', '3E8601',
   '207401', '056201', '004C00', '023B01', '012E01',
   '011D01', '011301'
  ]}

 ee.mapclient.centerMap(-93.7848, 30.3252, 11)
 ee.mapclient.addToMap(collection.map(NDVI).mean(), vis)
 # ee.mapclient.addToMap(collection.map(SAVI).mean(), vis)


