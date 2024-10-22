import os
import ee
import logging
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

    def ndvi(self, image, sensor_params):
        """
        Normalized Difference Vegetation Index

        :param image: a unique image from a ImageCollection (earthengine-api object)
        :param sensor_params: the sensor's parameters
        """
        vis = {'min': 0, 'max': 1, 'palette': ['FFFFFF', 'CE7E45', 'FCD163', '66A000', '207401',
                                               '056201', '004C00', '023B01', '012E01', '011301']}

        red = image.select(sensor_params['bands']['red'])
        nir = image.select(sensor_params['bands']['nir'])

        ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
        return ndvi, vis

    def ndwi(self, image, sensor_params):
        """
        Normalized Difference Water Index

        :param image: a unique image from a ImageCollection (earthengine-api object)
        :param sensor_params: the sensor's parameters
        """
        vis = {'min': -1, 'max': 1, 'palette': ["dfdfdf", "00bfff"]}

        blue = image.select(sensor_params['bands']['blue'])
        nir = image.select(sensor_params['bands']['nir'])

        ndvi = blue.add(nir).divide(blue.subtract(nir)).rename('NDWI')
        return ndvi, vis

    def evi(self, image, sensor_params):
        """
        Enhanced Vegetation Index

        :param image: a unique image from a ImageCollection (earthengine-api object)
        :param sensor_params: the sensor's parameters

        Source: https://github.com/renelikestacos/Google-Earth-Engine-Python-Examples/blob/master/
                001_EE_Classification_Landsat_8_TOA.ipynb
        """
        vis = {'min': -1, 'max': 1, 'palette': ['lightgreen', 'white', 'red']}

        blue = image.select(sensor_params['bands']['blue'])
        red = image.select(sensor_params['bands']['red'])
        nir = image.select(sensor_params['bands']['nir'])

        gain_factor = ee.Image(2.5)
        coefficient_1 = ee.Image(6)
        coefficient_2 = ee.Image(7.5)
        factor = ee.Image(1)

        evi = image.expression(
            "Gain_Factor*((NIR-RED)/(NIR+C1*RED-C2*BLUE+L))",
            {
                "Gain_Factor": gain_factor,
                "NIR": nir,
                "RED": red,
                "C1": coefficient_1,
                "C2": coefficient_2,
                "BLUE": blue,
                "L": factor
            }
        )
        return evi, vis

    def arvi(self, image, sensor_params):
        """
        Atmospherically Resistant Vegetation Index

        :param image: a unique image from a ImageCollection (earthengine-api object)
        :param sensor_params: the sensor's parameters
        """
        # TODO: definir pallete
        vis = {'min': -1, 'max': 1, 'palette': ['lightgreen', 'white', 'red']}

        blue = image.select(sensor_params['bands']['blue'])
        red = image.select(sensor_params['bands']['red'])
        nir = image.select(sensor_params['bands']['nir'])

        red_square = red.multiply(red)
        arvi = image.expression(
            "NIR - (REDsq - BLUE)/(NIR+(REDsq-BLUE))", {
                "NIR": nir,
                "REDsq": red_square,
                "BLUE": blue
            }
        )
        return arvi, vis

    def lai(self, image, sensor_params):
        """
        Leaf Area Index

        :param image: a unique image from a ImageCollection (earthengine-api object)
        :param sensor_params: the sensor's parameters
        """
        vis = {'min': -1, 'max': 1, 'palette': ["1bb81d", "98ff0a", "fdff00", "ff0000"]}

        red = image.select(sensor_params['bands']['red'])
        nir = image.select(sensor_params['bands']['nir'])
        coeff1 = ee.Image(0.0305)
        coeff2 = ee.Image(1.2640)

        lai = image.expression(
            "(((NIR/RED)*COEFF1)+COEFF2)",
            {
                "NIR": nir,
                "RED": red,
                "COEFF1": coeff1,
                "COEFF2": coeff2
            }
        )
        return lai, vis

    def savi(self, image, sensor_params):
        """
        Soil-adjusted vegetation index

        :param image: a unique image from a ImageCollection (earthengine-api object)
        :param sensor_params: the sensor's parameters
        """
        vis = {'min': -1, 'max': 1, 'palette': ["ac781c", "d1ff0c", "65e510", "2fa036"]}

        red = image.select(sensor_params['bands']['red'])
        nir = image.select(sensor_params['bands']['nir'])
        coeff1 = ee.Image(0.5)
        coeff2 = ee.Image(1)

        savi = image.expression(
            "((NIR-RED)/(NIR+RED+COEFF1))+(COEFF2+COEFF1)",
            {
                "NIR": nir,
                "RED": red,
                "COEFF1": coeff1,
                "COEFF2": coeff2
            }
        )
        return savi, vis

    def nbr(self, image, sensor_params):
        """
        Difference Normalized Burn Index

        :param image: a unique image from a ImageCollection (earthengine-api object)
        :param sensor_params: the sensor's parameters
        """
        vis = {'min': -1, 'max': 1, 'palette': ["ff0000", "e6ff04", "87ff14", "22943e"]}

        nir = image.select(sensor_params['bands']['nir'])
        swir = image.select(sensor_params['bands']['swir'])

        nbr = image.expression(
            "(NIR-SWIR)/(NIR+SWIR)",
            {
                "NIR": nir,
                "SWIR": swir,
            }
        )
        return nbr, vis

    def nbr2(self, image, sensor_params):
        """
        Difference Normalized Burn Index 2

        :param image: a unique image from a ImageCollection (earthengine-api object)
        :param sensor_params: the sensor's parameters
        """
        vis = {'min': -1, 'max': 1, 'palette': ["ff0000", "e6ff04", "87ff14", "22943e"]}

        swir = image.select(sensor_params['bands']['swir'])
        swir2 = image.select(sensor_params['bands']['swir-2'])

        nbr2 = image.expression(
            "(SWIR-SWIR2)/(SWIR+SWIR2)",
            {
                "SWIR": swir,
                "SWIR2": swir2
            }
        )
        return nbr2, vis

    def vegetation_indexes_monthly(self, sensor, ranges, map_type, reflectance, clip_area, is_visualize):
        """
        """
        ee.Initialize()

        logging.info(">> Generating vegetation index [{}]...".format(map_type))

        sensor_params = settings.COLLECTION[sensor]
        area_of_interest = (ee.FeatureCollection(settings.AOI_URL))

        logging.info(">>>> Filtering collection...")
        # images = utils.Utils().get_vi_by_range(sensor_params, ranges, area_of_interest, map_type)
        images = utils.Utils().get_collection_by_range(sensor, ranges, area_of_interest, reflectance)

        for range, item in images:
            if clip_area is True:
                image = item.clipToCollection(area_of_interest)
            else:
                image = item

            mapname = sensor + "-" + range[0].strftime("%Y%m%d") + \
                      "-to-" + range[1].strftime("%Y%m%d") + "-" + reflectance + "-" + map_type + \
                      "-" + str(settings.CLOUD_TOLERANCE)
            absolute_map_html_path = os.path.join(settings.PATH_TO_SAVE_MAPS, mapname + ".html")

            if map_type == 'ndvi':
                vegetation_index, vis = self.ndvi(image, sensor_params)
            elif map_type == 'ndwi':
                vegetation_index, vis = self.ndwi(image, sensor_params)
            elif map_type == 'nbr':
                vegetation_index, vis = self.nbr(image, sensor_params)
            elif map_type == 'nbr2':
                vegetation_index, vis = self.nbr2(image, sensor_params)
            elif map_type == 'lai':
                vegetation_index, vis = self.lai(image, sensor_params)
            elif map_type == 'savi':
                vegetation_index, vis = self.savi(image, sensor_params)
            elif map_type == 'arvi':
                vegetation_index, vis = self.arvi(image, sensor_params)
            elif map_type == 'evi':
                vegetation_index, vis = self.evi(image, sensor_params)
            else:
                logging.warning(">>>> Incorrect vegetation index: {}".format(map_type))
                return

            mapid = vegetation_index.getMapId(vis)

            map = folium.Map(location=[-22, -50.75], zoom_start=5, height=1200, width=1600)
            folium.TileLayer(
                tiles=mapid['tile_fetcher'].url_format,
                attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
                overlay=True,
                name=sensor + " [" + map_type + "]",
                control=True
            ).add_to(map)
            map.add_child(folium.LayerControl())

            logging.info(">>>> Saving map in {}...".format(absolute_map_html_path))
            map.save(absolute_map_html_path)

            logging.info(">>>> Visualizing throw folium...")
            if is_visualize is True:
                webbrowser.open(absolute_map_html_path)

    def vegetation_indexes(self, sensor, ranges, map_type, reflectance, clip_area, is_visualize):
        """
        """
        ee.Initialize()

        logging.info(">> Generating vegetation index [{}]...".format(map_type))

        sensor_params = settings.COLLECTION[sensor]
        area_of_interest = (ee.FeatureCollection(settings.AOI_URL))

        logging.info(">>>> Filtering collection...")
        # images = utils.Utils().get_vi_by_range(sensor_params, ranges, area_of_interest, map_type)
        images = utils.Utils().get_collection_by_range(sensor, ranges, area_of_interest, reflectance)

        for range, item in images:
            if clip_area is True:
                image = item.clipToCollection(area_of_interest)
            else:
                image = item

            mapname = sensor + "-" + range[0].strftime("%Y%m%d") + \
                      "-to-" + range[1].strftime("%Y%m%d") + "-" + reflectance + "-" + map_type + \
                      "-" + str(settings.CLOUD_TOLERANCE)
            absolute_map_html_path = os.path.join(settings.PATH_TO_SAVE_MAPS, mapname + ".html")

            if map_type == 'ndvi':
                vegetation_index, vis = self.ndvi(image, sensor_params)
            elif map_type == 'ndwi':
                vegetation_index, vis = self.ndwi(image, sensor_params)
            elif map_type == 'nbr':
                vegetation_index, vis = self.nbr(image, sensor_params)
            elif map_type == 'nbr2':
                vegetation_index, vis = self.nbr2(image, sensor_params)
            elif map_type == 'lai':
                vegetation_index, vis = self.lai(image, sensor_params)
            elif map_type == 'savi':
                vegetation_index, vis = self.savi(image, sensor_params)
            elif map_type == 'arvi':
                vegetation_index, vis = self.arvi(image, sensor_params)
            elif map_type == 'evi':
                vegetation_index, vis = self.evi(image, sensor_params)
            else:
                logging.warning(">>>> Incorrect vegetation index: {}".format(map_type))
                return

            mapid = vegetation_index.getMapId(vis)

            map = folium.Map(location=[-22, -50.75], zoom_start=5, height=1200, width=1600)
            folium.TileLayer(
                tiles=mapid['tile_fetcher'].url_format,
                attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
                overlay=True,
                name=sensor + " [" + map_type + "]",
                control=True
            ).add_to(map)
            map.add_child(folium.LayerControl())

            logging.info(">>>> Saving map in {}...".format(absolute_map_html_path))
            map.save(absolute_map_html_path)

            logging.info(">>>> Visualizing throw folium...")
            if is_visualize is True:
                webbrowser.open(absolute_map_html_path)


