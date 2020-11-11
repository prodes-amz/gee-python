import os
import ee
import settings
import folium
import webbrowser

from utils import utils


class Period:
    """
    Class responsible for multiple operations, such as statistics by month, biweekly, year, so on
    """
    def __init__(self):
        """
        """
        pass

    def mosaick_by_sensor_and_ranges(self, sensor, ranges, map_type, clip_area, composition, is_visualize):
        """
        """
        ee.Initialize()

        sensor_params = settings.COLLECTION[sensor]
        area_of_interest = (ee.FeatureCollection(settings.AOI_URL))

        images = utils.Utils().get_collection_by_range(sensor_params, ranges, area_of_interest, map_type)

        for range, item in images:
            if clip_area is True:
                image = item.clipToCollection(area_of_interest).select(sensor_params['composite']['natural'])
            else:
                image = item.select(sensor_params['composite']['natural'])

            mapname = sensor + "-" + range[0].strftime("%Y%m%d") + \
                      "-to-" + range[1].strftime("%Y%m%d") + "-" + composition + "-" + str(settings.CLOUD_TOLERANCE)
            absolute_map_html_path = os.path.join(settings.PATH_TO_SAVE_MAPS, mapname + ".html")

            mapid = image.getMapId(sensor_params['vis'])
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

    def mosaick_by_multiple_sensors_ranges(self, ranges, map_type, clip_area, composition, is_visualize):
        """
        Source: https://code.earthengine.google.com/20ad3c83a17ca27b28640fb922819208
        """
        ee.Initialize()

        sensor_params = settings.COLLECTION[sensor]
        area_of_interest = (ee.FeatureCollection(settings.AOI_URL))

        images = utils.Utils().get_collection_by_range(sensor_params, ranges, area_of_interest, map_type)

        # collection = ee.ImageCollection('COPERNICUS/S1_GRD') \
        #     .filterDate(start, finish) \
        #     .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
        #     .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
        #     .filter(ee.Filter.eq('instrumentMode', 'IW')) \
        #     .filterMetadata('resolution_meters', 'equals', 10) \
        #     .filterBounds(poly);

        # Difference in days between start and finish
        # diff = finish.difference(start, 'day')

        # Make a list of all dates
        # range = ee.List.sequence(0, diff.subtract(1)).map(function(day){
        # return start.advance(day, 'day')})

        # Funtion for iteraton over the range of dates
        # day_mosaics = function(date, newlist) {
        # date = ee.Date(date)
        # newlist = ee.List(newlist)

        # Filter collection between date and the next day
        # filtered = collection.filterDate(date, date.advance(1, 'day'))

        # Make the mosaic
        # image = ee.Image(filtered.mosaic())

        # Add the mosaic to a list only if the collection has images
        # return ee.List(ee.Algorithms.If(filtered.size(), newlist.add(image), newlist))}

    # Iterate over the range to make a new list, and then cast the list to an imagecollection
    #newcol = ee.ImageCollection(ee.List(range.iterate(day_mosaics, ee.List([]))))
