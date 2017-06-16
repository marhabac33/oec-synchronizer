#!/usr/bin/python3
#
# This file holds functions to convert given data to OEC format data.


import datetime
import logging
import os
import math
import re
from oec_sync_utils.constants import *
from oec_sync_utils.mappings import *


def to_oec_date(raw_date):
    ''' (str) -> str
    Given a date string will attempt to convert it into OEC date format. If no
    matching format is found, None is returned.
    '''
    for date_format in ['%y/%m/%d', '%Y/%m/%d', '%Y-%m-%d', '%y-%m-%d']:
        try:
            date = datetime.datetime.strptime(raw_date, date_format)
            date_str = date.strftime(OEC_DATE)
            return date_str
        except:
            continue
    
    logging.exception('%s Date in unknown format. Format: %s',
                      str(datetime.datetime.now()), raw_date)
    return None

def date_comparison(oec_date, csv_date):
    ''' (str, str) -> bool
    Returns True iff OEC date is more recent or the same as the csv date. Will
    also return False if either date is in unrecognised format.
    '''
    oec_date = to_oec_date(oec_date)
    csv_date = to_oec_date(csv_date)
    if (oec_date and csv_date):
        return (datetime.datetime.strptime(oec_date, OEC_DATE) >=
                datetime.datetime.strptime(csv_date, OEC_DATE))
    else:
        return False


def to_oec_right_ascension(ra_value):
    ''' (float) -> str
    Given a right ascension value as a float, will calculate and return a str
    formatted correctly for display in the OEC.
    '''
    ra = float(ra_value) / 360.0 * 24.0
    ra_string = "{:02d} {:02d} {:02d}".format(int(math.floor(ra)),
                                              int(math.floor((ra -
                                                  math.floor(ra)) * 60.0)),
                                              int((ra - math.floor(ra) -
                                                  math.floor((ra -
                                                              math.floor(ra)) *
                                                  60.0) / 60.0) * 60.0 * 60.0))
    return ra_string


def to_oec_declination(dec):
    ''' (float) -> str
    Given a declination value as a float, will calculate and return a str
    formatted correctly for display in the OEC.
    '''
    olddec = dec
    dec = abs(dec)
    dec_string = "{:02d} {:02d} {:02d}".format(int(math.floor(dec)),
                                                int(math.floor(
                                                    (dec - math.floor(dec)) *
                                                    60.0)),
                                                int((dec - math.floor(dec) -
                                                    math.floor((dec -
                                                                math.floor(
                                                                    dec)) *
                                                    60.0) / 60.0) * 60.0 *
                                                    60.0))
    if olddec < 0:
        dec_string = "-"+dec_string
    else:
        dec_string = "+"+dec_string
    return dec_string


def nasa_to_oec_declination(dec_str):
    ''' (str) -> str
    Parse the given declination string into the format used by the OEC
    '''
    result = " ".join(re.findall("[0-9.+-]+", dec_str))
    return result


def to_oec_luminosity(radius_star, temp_star):
    ''' (float, float) -> float
    Given the radius of a star as a float and the tempuratue of a star as a
    float, will return a calulation of the stars luminosity as a float.
    '''
    luminosity = (float(radius_star) * float(radius_star) * float(temp_star) *
                  float(temp_star) * float(temp_star) * float(temp_star) /
                  5778.0 / 5778.0 / 5778.0 / 5778.0)
    return luminosity


def to_oec_distance(luminosity, keplermag):
    ''' (float, float) -> float
    Given the luminosity of a star as a float and the kepler magnitude of a 
    star as a float, will return a calulation of the stars distance as a float.
    Note: Only should be used for kelper objects of intrest KOI.
    '''
    M = (-2.5 * math.log10(luminosity) + 4.74)
    mu = keplermag - M
    distance = math.pow(10.0, mu/5.0 + 1.0)
    return distance


def to_oec_spectraltype(spectraltype):
    ''' (str) -> str
    Given a string spectraltype, parse the string into the format used by the
    OEC
    '''
    result = ""
    for c in spectraltype:
        if c != " ":
            result += c
    return result


def to_oec_value(raw_value, key, tag):
    ''' (str, str) -> str
    Given a data value string and a xml tag/attribute key, either converts
    data value to OEC format, or simply returns the data value unaltered if
    no conversion is nessesary.
    '''
    # Use if, elif, statment to send values identified with trigger keys
    # to appropriate conversion function, else return raw value
    if (tag in ERROR_PLUS_MINUS):
        value = str("{:.15f}".format(math.fabs(float(raw_value))).rstrip(
            '0').rstrip('.'))
    elif (tag in DATES):
        value = to_oec_date(raw_value)
        if (value == None):
            value = raw_value
    elif (key in SYSTEM_RIGHT_ASC):
        value = to_oec_right_ascension(float(raw_value))
    elif (key in DECLINATION):
        value = to_oec_declination(float(raw_value))
    elif (key in NASA_DECLINATION):
        value = raw_value
    else:
        value = raw_value
    return value


def is_different(value1, value2, tolerance):
    ''' (str, str, float) -> bool
    Returns true iff value1 and value2 are different. If both value1 and value2
    are numeric strings will return true iff there numeric value is different
    and that difference is above the given tolerance range.
    '''
    if (value1 == value2):
        return False
    try:
        if (float(value1) == float(value2)):
            return False
        if (float(value1) < float(value2)):
            if ((1 - float(value1)/float(value2)) < tolerance):
                return False
        else:
            if ((1 - float(value2)/float(value1)) < tolerance):
                return False
    except:
        return True
    return True