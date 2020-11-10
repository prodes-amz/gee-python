import ee
import ee.mapclient
import settings
import folium
import webbrowser

from folium import plugins


class Vegetation:
    """
    Class responsible for vegetation indexes functionalities over earthengine-api
    """
    def __init__(self, sensor, ranges, map, clip_area):
        ee.Initialize()

        sensor_params = settings.COLLECTION[sensor]
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
                filter('CLOUDY_PIXEL_PERCENTAGE < 50')
            images.append(collection.median())

        composite = sensor_params['composite']['natural']
        if clip_area is True:
            image = images[0].clipToCollection(area_of_interest).select(composite)
        else:
            image = images[0].select(composite)

        mapid = image.getMapId(sensor_params['vis'])
        map = folium.Map(location=[-22.15, 53.75], zoom_start=9, height=1200, width=1600)
        folium.TileLayer(
            tiles=mapid['tile_fetcher'].url_format,
            attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
            overlay=True,
            name=sensor
        ).add_to(map)

        map.add_child(folium.LayerControl())

        map.save('/home/rodolfo/map.html')
        webbrowser.open('/home/rodolfo/map.html')
