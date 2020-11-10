import ee
import ee.mapclient
import settings
import folium
import webbrowser

from folium import plugins


class Period:
    """
    Class responsible for multiple operations, such as statistics by month, biweekly, year, so on
    """
    def __init__(self, sensor, ranges, map, clip_area):
        """
        """
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
            collection = set_collection. \
                filterDate(item[0], item[1]). \
                filterBounds(area_of_interest)
            images.append(collection.median())

        if clip_area is True:
            image = images[0].clipToCollection(area_of_interest).select(sensor_params['composite']['natural'])
        else:
            image = images[0].select(sensor_params['composite']['natural'])

        mapid = image.getMapId(sensor_params['vis'])

        map = folium.Map(location=[19.15, -98.75], zoom_start=9, height=1200, width=1600)
        folium.TileLayer(
            tiles=mapid['tile_fetcher'].url_format,
            attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
            overlay=True,
            name=sensor
        ).add_to(map)

        map.add_child(folium.LayerControl())
        map.save('/home/rodolfo/map.html')
        webbrowser.open('/home/rodolfo/map.html')