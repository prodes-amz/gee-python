import logging
import argparse
import settings
import indexes.vegetation as vi

from coloredlogs import ColoredFormatter
from utils import utils

import sys
if sys.version_info[0] < 3:
    raise RuntimeError('Python3 required')


def validate_params(sensor, aoi, range_date):
    """
    """
    is_sensor_valid, sensor = utils.Utils().evaluate_sensor(sensor)
    if is_sensor_valid is False:
        raise RuntimeError

    is_aoi_valid, aoi = utils.Utils().evaluate_aoi(aoi)
    if is_aoi_valid is False:
        raise RuntimeError

    is_ranges_valid, ranges = utils.Utils().evaluate_range_dates_args(range_date)
    if is_ranges_valid is False:
        raise RuntimeError

    return sensor, aoi, ranges


def main(sensor, aoi, range_date):
    """
    :param sensor:
    :param aoi:
    :param range_date
    """
    sensor, aoi, range_date = validate_params(sensor, aoi, range_date)
    sensor_params = settings.COLLECTION[sensor]

    vi.Vegetation().ndvi(sensor_params, aoi, range_date)


if __name__ == '__main__':
    """
    usage:
        python main.py -sensor landsat-8 -aoi /data/prodes/aoi/shp/aoi_1.shp 
                       -range_date 2020-01-01 2020-07-31 -verbose True
    """
    parser = argparse.ArgumentParser(
        description='...')
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

