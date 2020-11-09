import os
import datetime
import settings
import logging
import geopandas as gpd


class Utils:
    def __init__(self):
        pass

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
