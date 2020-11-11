import os
import ee
import ee.mapclient
import datetime
import settings
import logging
import geopandas as gpd


class Utils:
    def __init__(self):
        pass

    def get_collection_by_range(self, sensor_params, ranges, area_of_interest, map_type):
        """
        """
        if map_type is not None:
            # TODO: validate map param first
            set_collection = ee.ImageCollection(sensor_params['derived'][map])
        else:
            set_collection = ee.ImageCollection(sensor_params['toa'])

        images = []
        for item in ranges:
            collection = set_collection.\
                filterDate(item[0], item[1]).\
                filterBounds(area_of_interest).\
                filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', settings.CLOUD_TOLERANCE))
            images.append((item, collection.median()))
        return images

    def evaluate_sensor(self, sensor):
        """
        :param sensor:
        :return
        """
        logging.info(">> Checking sensor {}...".format(sensor))
        flag = True

        if sensor in ['landsat-8', 'landsat8', 'LANDSAT-8', 'LANDSAT8']:
            sensor = 'landsat-8'
        elif sensor in ['landsat-7', 'landsat7', 'LANDSAT-7', 'LANDSAT7']:
            sensor = 'landsat-7'
        elif sensor in ['sentinel-2', 'sentinel2', 'SENTINEL-2', 'SENTINEL2']:
            sensor = 'sentinel-2'
        else:
            logging.warning(">>>> Sensor {} not found. Check it and try again".format(sensor))
            return False, None

        logging.info(">>>> Sensor accepted: {}!".format(sensor))
        return flag, sensor

    def get_aoi_centroid(self, aoi_path):
        """
        """
        pass

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

    def convert_vector_2_featurecollection(self, vector_path):
        """
        :param vector_path:
        :return:
        """
        shapefile = gpd.read_file(vector_path)

        features = []
        for i in range(shapefile.shape[0]):
            geom = shapefile.iloc[i:i + 1, :]
            json_dict = eval(geom.to_json())
            geojson_dict = json_dict['features'][0]
            features.append(ee.Feature(geojson_dict))

        fc = ee.FeatureCollection(features)

        # task = ee.batch.Export.table.toAsset(**{
        #     'collection': features,
        #     'description': 'exportToTableAssetExample',
        #     'assetId': settings.ASSET_URL + '/aoi'
        # })
        # task.start()

        # task = ee.batch.Export.image.toDrive(
        #     image=image_out.visualize(vizParams),
        #     description=FileName,
        #     folder=folderName,
        #     scale=30,
        #     region=Coordinate_List,
        #     fileFormat='GeoTIFF'
        # )
        #
        # task.start()

        return fc

    def evaluate_aoi(self, aoi_path):
        """
        :param aoi_path:
        :return:
        """
        logging.info(">> Checking aoi {}...".format(aoi_path))

        filename = os.path.basename(aoi_path)

        if filename.endswith('.geojson') or filename.endswith('.shp'):
            aoi_obj = gpd.read_file(aoi_path)
            for item in aoi_obj['geometry']:
                if item.geom_type != "Polygon":
                    logging.warning(">>>> The AOI need to be only in Polygon representation. {} found!".
                                    format(item.geom_type))
                    return False, None
                else:
                    logging.info(">>>> AOI accepted! Format known: {}!".format(item.geom_type))
                    return True, aoi_obj
        else:
            logging.warning(">>>> AOI does not have accepted extension: {}".format(filename))
            return False, None
        return True, aoi_obj

    def evaluate_range_dates_args(self, ranges_args):
        """
        :param ranges_args: Sequence of dates in string format
        :return ranges: The list of pairs of range dates, in tuple format. Thus, for 2018-05-01 2018-05-15 str,
        a list with one tuple will be returned [(correspondent datetime 1, correspondent datetime 2)], where first
        and second dates represent start and stop, respectively
        """
        flag = True
        ranges = []

        if ranges_args is None:
            return ranges

        logging.info(">> Checking range dates {}...".format(ranges_args))

        if (len(ranges_args) % 2) != 0:
            flag = False
            raise ValueError(">>>> Dates should be in pairs!")

        for i in range(0, len(ranges_args) - 1, 2):
            try:
                date_aux_1 = datetime.datetime.strptime(ranges_args[i], '%Y-%m-%d')
                date_aux_2 = datetime.datetime.strptime(ranges_args[i + 1], '%Y-%m-%d')
            except ValueError:
                flag = False
                raise ValueError(">>>> Incorrect date format, should be YYYY-MM-DD. Try again!")

            try:
                accept_date_1 = datetime.datetime.strptime(settings.OBSERVED_DATES[0], '%m-%d')
                accept_date_2 = datetime.datetime.strptime(settings.OBSERVED_DATES[1], '%m-%d')
            except ValueError:
                flag = False
                raise ValueError(">>>> Incorrect observed date format, should be MM-DD. "
                                 "Check your settings.py and try again!")

            if date_aux_1 > date_aux_2:
                flag = False
                raise ValueError(">>>> Pair range is incorrect. Stop date {} is bigger than start date {}! Skipped!".
                                 format(ranges_args[i + 1], ranges_args[i]))

            if date_aux_1 == date_aux_2:
                flag = False
                raise ValueError(">>>> Pair range is incorrect. Stop date {} is equal than start date {}! Skipped!".
                                 format(ranges_args[i], ranges_args[i + 1]))

            only_month_and_day_1 = datetime.datetime.strptime(str(date_aux_1.month) + "-" + str(date_aux_1.day),
                                                              "%m-%d")
            only_month_and_day_2 = datetime.datetime.strptime(str(date_aux_2.month) + "-" + str(date_aux_2.day),
                                                              "%m-%d")

            if (only_month_and_day_1 > accept_date_2) or (only_month_and_day_1 < accept_date_1) or \
                    (only_month_and_day_1 >= only_month_and_day_2):
                flag = False
                raise ValueError(">>>> Start date {} is out of the accepted period {}! Try again!".
                                 format(ranges_args[i], settings.OBSERVED_DATES[0]))

            if (only_month_and_day_2 > accept_date_2) or (only_month_and_day_2 < accept_date_1):
                flag = False
                raise ValueError(">>>> Stop date {} is out of the accepted period {}! Try again!".
                                 format(ranges_args[i + 1], settings.OBSERVED_DATES[1]))

            ranges.append((date_aux_1, date_aux_2))

        logging.info(">>>> Range dates accepted: {}!".format(ranges))
        return flag, ranges
