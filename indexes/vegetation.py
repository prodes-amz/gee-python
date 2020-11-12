import os
import ee
import ee.mapclient
import settings
import folium
import webbrowser

from utils import utils


class Vegetation:
    """
    Class responsible for vegetation indexes functionalities over earthengine-api
    """
    def __init__(self):
        pass

    def ndvi(self, red, nir):
        """
        """
        return nir.subtract(red).divide(nir.add(red)).rename('NDVI')

    def vegetation_indexes(self, sensor, ranges, map_type, clip_area, is_visualize):
        ee.Initialize()

        sensor_params = settings.COLLECTION[sensor]
        area_of_interest = (ee.FeatureCollection(settings.AOI_URL))

        images = utils.Utils().get_vi_by_range(sensor_params, ranges, area_of_interest, map_type)

        for range, item in images:
            if clip_area is True:
                image = item.clipToCollection(area_of_interest)
            else:
                image = item

            mapname = sensor + "-" + range[0].strftime("%Y%m%d") + \
                      "-to-" + range[1].strftime("%Y%m%d") + "-" + map_type + "-" + str(settings.CLOUD_TOLERANCE)
            absolute_map_html_path = os.path.join(settings.PATH_TO_SAVE_MAPS, mapname + ".html")

            vegetation_index = self.ndvi(image.select(sensor_params['bands']['red'], sensor_params['bands']['nir']))

            mapid = image.getMapId()
            map = folium.Map(location=[19.15, -98.75], zoom_start=9, height=1200, width=1600)
            folium.TileLayer(
                tiles=mapid['tile_fetcher'].url_format,
                attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
                overlay=True,
                name=sensor
            ).add_to(map)
            map.add_child(folium.LayerControl())
            map.save(absolute_map_html_path)

            if is_visualize is True:
                webbrowser.open(absolute_map_html_path)
