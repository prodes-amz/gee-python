import ee
import ee.mapclient
import settings


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
            set_collection = ee.ImageCollection(sensor_params['toa'])

        images = []
        for item in ranges:
            collection = set_collection.\
                filterDate(item[0], item[1]).\
                filterBounds(area_of_interest).\
                filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', 10))
            images.append(collection.mean())

        ee.mapclient.addToMap(images[0].clipToCollection(area_of_interest))


