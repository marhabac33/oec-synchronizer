#!/usr/bin/python3


import csv
import logging
import os
from oec_sync_utils.constants import *
from oec_sync_utils.mappings import *


def read_csv(file_path):
    ''' (str) -> generator of dict{str: str}
    Given a string file path. Reads csv data from the csv file located at the
    given file_path string, and returns a generator object that yields a dict
    (column name: row value) for each row of the csv file.
    '''
    csv_file = open(file_path, 'r')
    # Open file as a dictonary of column name to row data value.
    exo_data = csv.DictReader(csv_file)
    exo_dict_list = []
    # Create a list of dict (column name to row data value) with sanitized
    # data values then close csv file.
    for exoplanet_dict in exo_data:
        # Remove all invalid characters (sanitize data).
        clean_exoplanet_dict = {tag: (' '.join(data.split())) for tag, data in
                                exoplanet_dict.items()}
        exo_dict_list.append(clean_exoplanet_dict)
    csv_file.close()
    # Yield next exoplanet dict when called.
    for exoplanet_dict in exo_dict_list:
        yield exoplanet_dict


def get_csv_identifiers(exoplanet, catalogue_map):
    ''' (dict{str: str}, dict{str: str}) -> tuple(str, str, str)
    Given a dict of a csv exoplanet data row and a dict mapping column names to
    specific row values, will return the a tuple of the system name, exoplanet
    name, and last update of 
    '''
    # System mapping for this catalogue:
    system_map = catalogue_map[SYSTEM_MAP]
    # Exoplanet mapping for this catalogue:
    exoplanet_map = catalogue_map[EXOPLANET_MAP]

    # Get system name:
    if ((system_map[NAME][ELM_TAG][TAG_KEY] in exoplanet) and
        (exoplanet[system_map[NAME][ELM_TAG][TAG_KEY]] != '')):
        system_name = exoplanet[system_map[NAME][ELM_TAG][TAG_KEY]]
    else:
        logging.exception('%s: Unknown system name in %s \n From: %s',
                          str(datetime.datetime.now()),
                          str(exoplanet), file_path)
        system_name = None
    
    # Get Exoplanet name from csv data if available.
    if ((exoplanet_map[NAME][ELM_TAG][TAG_KEY] in exoplanet) and
        (exoplanet[exoplanet_map[NAME][ELM_TAG][TAG_KEY]] != '')):
        planet_name = exoplanet[exoplanet_map[NAME][ELM_TAG][TAG_KEY]]
    else:
        logging.exception('%s: Unknown planet name in %s \n From: %s',
                          str(datetime.datetime.now()),
                          str(exoplanet), file_path)
        planet_name = None

    # Get last update for csv:
    if ((exoplanet_map[UPDATE][ELM_TAG][TAG_KEY] in exoplanet) and
        (exoplanet[exoplanet_map[UPDATE][ELM_TAG][TAG_KEY]] != '')):
        csv_update = exoplanet[exoplanet_map[UPDATE][ELM_TAG][TAG_KEY]]
    else:
        logging.exception('%s: Unknown last update in %s \n From: %s',
                          str(datetime.datetime.now()),
                          str(exoplanet), file_path)
        csv_update = None
    return (system_name, planet_name, csv_update)