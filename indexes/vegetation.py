import ee
import ee.mapclient
import folium


class Vegetation:
    """
    Class responsible for vegetation indexes functionalities over earthengine-api
    """
    def __init__(self):
        ee.Initialize()

    def ndvi(self, sensor_params, aoi, ranges):
        """
        """
        ee.mapclient.addToMap(aoi)

        collections = []
        median_images = []
        for item in ranges:
            collection = (ee.ImageCollection(sensor_params['sr']).filterDate(item[0], item[1]).filterBounds(aoi))
            median_image = collection.median().select('B3', 'B2', 'B1')

            collections.append(collection)
            median_images.append(median_image)

        ee.mapclient.addToMap(median_images[0], {'gain': [1.4, 1.4, 1.1]})


        # area_of_interest = ee.Geometry.Rectangle([-98.75, 19.15, -98.15, 18.75])
        # mexico_landcover_2010_landsat = ee.Image("users/renekope/MEX_LC_2010_Landsat_v43").clip(area_of_interest)
        # landsat8_collection = ee.ImageCollection('LANDSAT/LC8_L1T_TOA').filterDate('2016-01-01', '2018-04-19').min()
        # landsat8_collection = landsat8_collection.slice(0, 9)

        # ee.mapclient.centerMap(-93.7848, 30.3252, 11)
        # ee.mapclient.addToMap(collection.map(NDVI).mean(), sensor_params['vis'])
        # ee.mapclient.addToMap(collection.map(SAVI).mean(), vis)