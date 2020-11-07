import datetime
import logging
import argparse
import settings
import ee.mapclient

from coloredlogs import ColoredFormatter
from utils import utils

import sys
if sys.version_info[0] < 3:
    raise RuntimeError('Python3 required')


def main(sensor, aoi, range_date):
    """
    USAGE: python main.py -aoi /data/prodes/aoi/aoi1.shp -range_dates 2018-05-24 2018-07-23 -verbose True
    :param sensor:
    :param aoi:
    :param range_date
    """
    sensor = utils.Utils().evaluate_sensor(sensor)
    area_of_interest = utils.Utils().evaluate_aoi(aoi)
    ranges = utils.Utils().evaluate_range_dates_args(range_date)

    if sensor == 'sentinel-1':
        logging.info(">>>> No functionalities available for {} sensor.".format(sensor))
        return

    sensor_params = settings.COLLECTION[sensor]
    ee.Initialize()

    collection = (ee.ImageCollection(sensor_params['sr'])
                  .filterDate(ranges[0], ranges[1]))
    # area_of_interest = ee.Geometry.Rectangle([-98.75, 19.15, -98.15, 18.75])
    # mexico_landcover_2010_landsat = ee.Image("users/renekope/MEX_LC_2010_Landsat_v43").clip(area_of_interest)
    # landsat8_collection = ee.ImageCollection('LANDSAT/LC8_L1T_TOA').filterDate('2016-01-01', '2018-04-19').min()
    # landsat8_collection = landsat8_collection.slice(0, 9)

    ee.mapclient.centerMap(-93.7848, 30.3252, 11)
    # ee.mapclient.addToMap(collection.map(NDVI).mean(), sensor_params['vis'])
    # ee.mapclient.addToMap(collection.map(SAVI).mean(), vis)


if __name__ == '__main__':
    """
    usage:
        python main.py -sensor landsat-8 -aoi /data/prodes/aoi/shp/aoi_1.shp -range_date 2020-01-01 2020-07-31 -verbose True
    """
    parser = argparse.ArgumentParser(
        description='Make a stack composition from Sentinel-1 polarization bands, which enhances '
                    'land-changes under the canopies')
    parser.add_argument('-sensor', action="store", dest='sensor',
                        help='GEE options to the sensors. Available: landsat-8, landsat-7, sentinel-1, sentinel-2')
    parser.add_argument('-aoi', action="store", dest='aoi',
                        help='Absolute path to ESRI Shapefile regarding the area of interest')
    parser.add_argument('-range_date', nargs='*', action="store", dest='range_date',
                        help='Range of dates to be downloaded. Keep the following format: YYYY-mm-dd, with no quotes '
                             'or spaces spaces between the numbers. The dates must to be in pairs, where the first '
                             'is start date, following the stop date.')
    parser.add_argument('-verbose', action="store", dest='verbose', help='Print log of processing')
    args = parser.parse_args()

    if eval(args.verbose):
        log = logging.getLogger('')

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        cf = ColoredFormatter("[%(asctime)s] {%(filename)-15s:%(lineno)-4s} %(levelname)-5s: %(message)s ")
        ch.setFormatter(cf)
        log.addHandler(ch)

        fh = logging.FileHandler('logging.log')
        fh.setLevel(logging.INFO)
        ff = logging.Formatter("[%(asctime)s] {%(filename)-15s:%(lineno)-4s} %(levelname)-5s: %(message)s ",
                               datefmt='%Y.%m.%d %H:%M:%S')
        fh.setFormatter(ff)
        log.addHandler(fh)

        log.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    main(args.sensor, args.aoi, args.range_date)

