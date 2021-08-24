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
        },
        'bands': {
            'coastal': 'B1',
            'blue': 'B2',
            'green': 'B3',
            'red': 'B4',
            'nir': 'B5',
            'swir': 'B6',
            'swir-2': 'B7',
            'pan': 'B8',
            'cirrus': 'B9',
            'termal': 'B10',
            'termal-2': 'B11',
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
            'max': 0.5,
            'gamma': [0.95, 1.1, 1]
        },
        'composite': {
            'natural': ['B3', 'B2', 'B1'],
            'false': ['B4', 'B3', 'B2'],
            'vegetation': ['B4', 'B2', 'B1'],
            'agriculture': ['B5', 'B4', 'B2']
        },
        'bands': {
            'blue': 'B1',
            'green': 'B2',
            'red': 'B3',
            'nir': 'B4',
            'swir': 'B5',
            'thermal': 'B6',
            'mid-ir': 'B7',
            'pan': 'B8',
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
        },
        'bands': {
            'coastal': 'B1',
            'blue': 'B2',
            'green': 'B3',
            'red': 'B4',
            'red-edge-1': 'B5',
            'red-edge-2': 'B6',
            'red-edge-3': 'B7',
            'nir': 'B8',
            'veg-red-edge': 'B8A',
            'water': 'B9',
            'cirrus': 'B10',
            'swir': 'B11',
            'swir-2': 'B12'
        }
    }
}
