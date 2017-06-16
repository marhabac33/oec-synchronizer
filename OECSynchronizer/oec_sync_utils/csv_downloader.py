#!/usr/bin/python3

import csv
import datetime
import logging
import os
import socket
import urllib.request as req


def download_csv_file(url, raw_filename, csv_dir):
    ''' (str, str, str) -> str
    Downloads file from the given url string and saves it to the given
    directory under the given filename; returns the filepath to the created
    file. If download fails for any reason warning message will be logged to
    oec_log and None will be returned.
    '''
    # Create file name/path.
    file_path = os.path.join(csv_dir, raw_filename)
    # Open the URL as a file like object, decode data from binary to utf-8,
    # and read data to string.
    try:
        raw_data = req.urlopen(url, timeout=45).read().decode('utf-8')
    except req.HTTPError:
        logging.exception('%s: Could not access url URL: %s on %s',
                          req.HTTPError, url, str(datetime.datetime.now()))
        return None
    except req.URLError:
        logging.exception('%s: Could not access url URL: %s on %s',
                          req.URLError, url, str(datetime.datetime.now()))
        return None
    except ValueError:
        logging.exception('%s: Could not access url URL: %s on %s', ValueError,
                          url, str(datetime.datetime.now()))
        return None
    except socket.timeout:
        logging.exception('Warning socket timed out, check url - URL %s on %s',
                          url, str(datetime.datetime.now()))
        return None
    else:
        logging.info('%s csv download successful on %s', url,
                     str(datetime.datetime.now()))
    # Open file for writing.
    try:
        file = open(file_path, "w")
    except IOError:
        logging.exception('Could not open %s for writing on %s', file_path,
                          str(datetime.datetime.now()))
        return None
    else:
        # Write raw_data to .csv file.
        file.write(raw_data)
        file.close()
    return file_path

