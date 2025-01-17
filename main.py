import logging
import argparse
import indexes.vegetation as vi

from coloredlogs import ColoredFormatter
from utils import utils

import sys
if sys.version_info[0] < 3:
    raise RuntimeError('Python3 required')


def validate_params(sensor, range_date):
    """
    """
    is_sensor_valid, sensor = utils.Utils().evaluate_sensor(sensor)
    if is_sensor_valid is False:
        raise RuntimeError

    is_ranges_valid, ranges = utils.Utils().evaluate_range_dates_args(range_date)
    if is_ranges_valid is False:
        raise RuntimeError

    return sensor, ranges


def main(args):
    """
    :param args:
    """
    sensor = args.sensor
    range_date = args.range_date
    veg_index = args.vi
    reflectance = args.reflectance
    composite = args.composite

    sensor, range_date = validate_params(sensor, range_date)

    # 1. Mosaic for one sensor, multiple range of dates, cloud coverage according to settings.CLOUD_TOLERANCE
    # pd.Period().mosaick_by_sensor_and_ranges(sensor, ranges=range_date, clip_area=True, composition=composite,
    #                                          is_visualize=True, reflectance=reflectance)

    # 2. Mosaic vegetation index (ndvi, ndwi, arvi, lai, evi, savi, nbr, and nbr2) for one sensor,
    # multiple range of dates, cloud coverage according to settings.CLOUD_TOLERANCE (available only for sentinel-2)
    vi.Vegetation().vegetation_indexes(sensor, ranges=range_date, map_type=veg_index, reflectance=reflectance,
                                       clip_area=True, is_visualize=True)

    # 3. Mosaic vegetation index (ndvi, ndwi, arvi, lai, evi, savi, nbr, and nbr2) for one sensor,
    # multiple range of dates, cloud coverage according to settings.CLOUD_TOLERANCE (available only for sentinel-2)
    # vi.Vegetation().vegetation_indexes_monthly(sensor, ranges=range_date, map_type=veg_index, reflectance=reflectance,
    #                                            clip_area=False, is_visualize=True)


if __name__ == '__main__':
    """
    Usage:
        > python main.py -sensor landsat-8 -range_date 2020-01-01 2020-07-31 -verbose True
    """
    parser = argparse.ArgumentParser(
        description='A collection of useful scripts for multiple applications using '
                    'Google Earth Engine [earthengine-api]')
    parser.add_argument('-sensor', action="store", dest='sensor',
                        help='GEE options to the sensors. Available: landsat-8, landsat-7, sentinel-2')
    parser.add_argument('-range_date', nargs='*', action="store", dest='range_date',
                        help='Range of dates to be downloaded. Keep the following format: YYYY-mm-dd, with no quotes '
                             'or spaces spaces between the numbers. The dates must to be in pairs, where the first '
                             'is start date, following the stop date.')
    parser.add_argument('-vi', action="store", dest='vi', help='Vegetation indexes. Alternatives are: '
                                                               '[ndvi, ndwi, arvi, lai, evi, savi, nbr, and nbr2]')
    parser.add_argument('-composite', action="store", dest='composite', help='Landsat-7, Landsat-8 and Sentinel-2 '
                                                                             'composites. Alternatives are: '
                                                                             '[natural, false, vegetation, '
                                                                             'agriculture]')
    parser.add_argument('-reflectance', action="store", dest='reflectance', help='Reflectance type. Alternatives are: '
                                                                                 '[sr, toa]')
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

    main(args)

