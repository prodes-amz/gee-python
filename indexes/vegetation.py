import ee
import ee.mapclient
import settings
import datetime


class Vegetation:
    """
    Class responsible for vegetation indexes functionalities over earthengine-api
    """
    def __init__(self, sensor_params, ranges, map):
        ee.Initialize()

        area_of_interest = (ee.FeatureCollection(settings.AOI_URL))

        if map is not None:
            # TODO: validate map param first
            set_collection = ee.ImageCollection(sensor_params['derived'][map])
        else:
            set_collection = ee.ImageCollection(sensor_params['sr'])

        images = []
        for item in ranges:
            collection = set_collection.\
                filterDate(item[0], item[1]).\
                filterBounds(area_of_interest).\
                filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 0.5)
            images.append(collection)

        ee.mapclient.addToMap(images[0].mean().clipToCollection(area_of_interest), sensor_params['vis'])

    def download_image(self, image):
        """
        """
        path = image.getDownloadUrl({
            'scale': 30,
            'crs': 'EPSG:4326',
            'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
        })

    def pan_sharp(self):
        """
        """
        image1 = ee.Image('LANDSAT/LE07/C01/T1/LE07_230068_19990815')

        rgb = image1.select('B3', 'B2', 'B1').unitScale(0, 255)
        gray = image1.select('B8').unitScale(0, 155)

        # Convert to HSV, swap in the pan band, and convert back to RGB.
        huesat = rgb.rgbToHsv().select('hue', 'saturation')
        upres = ee.Image.cat(huesat, gray).hsvToRgb()

        # Display before and after layers using the same vis parameters.
        visparams = {'min': [.15, .15, .25], 'max': [1, .9, .9], 'gamma': 1.6}
        ee.mapclient.addToMap(rgb, visparams, 'Orignal')
        ee.mapclient.addToMap(upres, visparams, 'Pansharpened')

