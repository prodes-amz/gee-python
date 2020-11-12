import os

from decouple import config

DL_DATASET = config('DL_DATASET')
PATH_TO_SAVE_MAPS = os.path.join(DL_DATASET, 'maps')

AOI_URL = "users/rodolfolotte/amazon-biom"

# cloud tolerance: 0: no cloud
#                100: cloud aplenty
CLOUD_TOLERANCE = 1
OBSERVED_DATES = ('01-01', '12-31')
VALID_ENTRIES_EXTENSION = (".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".tif", ".tiff", ".TIF", ".TIFF")
VALID_PREDICTION_EXTENSION = (".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".tif", ".tiff", ".TIF", ".TIFF")

# Source: https://developers.google.com/earth-engine/datasets/catalog/
COLLECTION = {
    'landsat-8': {
        'raw': 'LANDSAT/LC08/C01/T1',
        'sr': 'LANDSAT/LC08/C01/T1_SR',
        'toa': 'LANDSAT/LC08/C01/T1_TOA',
        'derived': {
            'bai': 'LANDSAT/LC08/C01/T1_8DAY_BAI',
            'evi': 'LANDSAT/LC08/C01/T1_8DAY_EVI',
            'ndvi': 'LANDSAT/LC08/C01/T1_8DAY_NDVI',
            'nbrt': 'LANDSAT/LC08/C01/T1_8DAY_NBRT',
            'ndsi': 'LANDSAT/LC08/C01/T1_8DAY_NDSI',
            'ndwi': 'LANDSAT/LC08/C01/T1_8DAY_NDWI'
        },
        'vis': {
            'min': 0,
            'max': 0.5,
            'gamma': [0.95, 1.1, 1]
        },
        'composite': {
            'natural': ['B4', 'B3', 'B2'],
            'false': ['B7', 'B6', 'B4'],
            'vegetation': ['B5', 'B4', 'B3'],
            'agriculture': ['B6', 'B5', 'B2']
        }
    },
    'landsat-7': {
        'raw': 'LANDSAT/LE07/C01/T1',
        'sr': 'LANDSAT/LE07/C01/T1_SR',
        'toa': 'LANDSAT/LE07/C01/T1_TOA',
        'derived': {
            'bai': 'LANDSAT/LE07/C01/T1_8DAY_BAI',
            'evi': 'LANDSAT/LE07/C01/T1_8DAY_EVI',
            'ndvi': 'LANDSAT/LE07/C01/T1_8DAY_NDVI',
            'nbrt': 'LANDSAT/LE07/C01/T1_8DAY_NBRT',
            'ndsi': 'LANDSAT/LC07/C01/T1_8DAY_NDSI',
            'ndwi': 'LANDSAT/LC07/C01/T1_8DAY_NDWI'
        },
        'vis': {
            'min': 0,
            'max': 1,
            'palette': [
                'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163',
                '99B718', '74A901', '66A000', '529400', '3E8601',
                '207401', '056201', '004C00', '023B01', '012E01',
                '011D01', '011301'
            ]
        },
        'composite': {
            'natural': ['B3', 'B2', 'B1'],
            'false': ['B4', 'B3', 'B2'],
            'vegetation': ['B4', 'B2', 'B1'],
            'agriculture': ['B5', 'B4', 'B2']
        }
    },
    'sentinel-1': {
        'grd': 'COPERNICUS/S1_GRD',
        'mode': 'IW',
        'pol': ['VV', 'HH', 'VH', 'HV']
    },
    'sentinel-2': {
        'raw': '',
        'sr': 'COPERNICUS/S2_SR',
        'toa': 'COPERNICUS/S2',
        'derived': {},
        'vis': {
            'min': 0,
            'max': 2000,
            'gamma': [0.9, 1.3, 1.1]
        },
        'composite': {
            'natural': ['B4', 'B3', 'B2'],
            'false': ['B12', 'B11', 'B8'],
            'vegetation': ['B8', 'B3', 'B2'],
            'agriculture': ['B11', 'B8', 'B3']
        }
    }
}
