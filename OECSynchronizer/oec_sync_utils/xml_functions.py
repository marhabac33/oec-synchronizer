#!/usr/bin/python3
#
# This file supports the generation of properly formatted OEC system XML files.


import datetime
import logging
import math
import os
import re
import xml.etree.ElementTree as ET
from oec_sync_utils.constants import *
from oec_sync_utils.mappings import *
from oec_sync_utils.system_xml import *


def set_xml_aliases(dir_path, alias_to_xml, uniform_alias_to_xml, repo):
    ''' (str, dict(str: SystemXML), GitRepo) -> None
    Given a file path to the OEC systems folder will iterate through each
    system XML file and create a dict mapping each alias for a system/star/
    planet to a SystemXML object representing that file. Will switch to branch
    of file name in given GitRepo object if such a branch exists
    '''
    for file_name in os.listdir(dir_path):
        # For each file in the given directory ending in .xml, create a xml
        # tree root element.
        if file_name.endswith(XML_END):
            file_path = os.path.join(dir_path, file_name)
            # If origin GitHub repository already has a branch for this file,
            # checkout branch and use that version of the file.
            branch = re.sub(r'\W+|[_]+', '', file_name[:-4])
            if (branch in repo.branches()):
                if (not repo.checkout(branch)):
                    continue
                # Create SystemXML object for the given file.
                xml_file = SystemXML(file_name, file_path)
                # Return to master branch.
                repo.checkout()
            else:
                # Create SystemXML object for the given file.
                xml_file = SystemXML(file_name, file_path)
            # Add each alias the dict as key that points to its file location
            # and the date it was last updated.
            for alias in xml_file.get_aliases():
                alias_to_xml[alias] = xml_file
                # Format aliases to remove spacing, all special characters (non
                # alphanumeric), and change all capital letters to lowercase.
                uniform_alias = re.sub(r'\W+|[_]+', '', alias).lower()
                uniform_alias_to_xml[uniform_alias] = (xml_file, alias)


def new_system_xml(exo_data, csv_map, system_xml, system_name, tolerance):
    ''' (dict{str: str}, list[list[tuple(str, str), list[tuple(str, str)]],
         SystemXML, str) -> bool add_element
    Given exoplanet data from a single csv row in the from of a dict mapping
    column names to column values as str, a list of mappings from XML
    tag/attribute to csv column name, and a SystemXML object; will add/update
    the SystemXML to contain the data in from the csv. new_system_xml will
    write updated SystemXML to systems folder in current directory. Returns
    True iff some update was applied to the xml file (and update was written to
    file) or a new update was created, else False.
    '''
    # Flag indicating if xml file has been updated:
    is_updated = False
    # Identify which catalogue has been given.
    catalogue = csv_map[MAPPING]
    
    root = system_xml.get_head()
    # Update SystemXML System level values:
    for mapping in csv_map[SYSTEM_MAP]:
        if (mapping[ELM_TAG][TAG] == NAME_TAG):
            if (system_xml.add_element(exo_data, mapping, root, tolerance)):
                is_updated = True
        else:
            if (system_xml.update_element(exo_data, mapping, root, tolerance)):
                is_updated = True

    # Binary level tags:

    # Get SystemXML Star element of given name if star of that name is in
    # SystemXML object:
    star_map = csv_map[STAR_MAP]
    if ((star_map[NAME][ELM_TAG][TAG_KEY] in exo_data) and
        (exo_data[star_map[NAME][ELM_TAG][TAG_KEY]] != '')):
        star_name = exo_data[star_map[NAME][ELM_TAG][TAG_KEY]]
    else:
        star_name = None
        
    # Get Exoplanet name from csv data if available.
    exoplanet_map = csv_map[EXOPLANET_MAP]
    if ((exoplanet_map[NAME][ELM_TAG][TAG_KEY] in exo_data) and
        (exo_data[exoplanet_map[NAME][ELM_TAG][TAG_KEY]] != '')):
        exoplanet_name = exo_data[exoplanet_map[NAME][ELM_TAG][TAG_KEY]]
    else:
        exoplanet_name = None

    # Get SystemXML Star element of given name if star of that name is in
    # SystemXML object:
    if (not (star_name is None)):
        star = system_xml.get_star(star_name, exoplanet_name)
    else:
        star = None
    # If Star not in SystemXML, then add Star element to SystemXML
    if (star is None):
        is_updated = True
        star = system_xml.add_star()
    # Update SystemXML System level values:
    for mapping in star_map:
        if (mapping[ELM_TAG][TAG] == NAME_TAG):
            if (star.add_element(exo_data, mapping, star.get_head(),
                                 tolerance)):
                is_updated = True
        else:
            if (star.update_element(exo_data, mapping, star.get_head(),
                                    tolerance)):
                is_updated = True


    # Get SystemXML Exoplanet element of given name if planet of that name is
    # in SystemXML object:
    if (not (exoplanet_name is None)):
        exoplanet = star.get_exoplanet(exoplanet_name)
    else:
        exoplanet = None
    # If Star not in SystemXML, then add Star element to SystemXML
    if (exoplanet is None):
        is_updated = True
        exoplanet = star.add_exoplanet()
    # Update SystemXML System level values:
    for mapping in exoplanet_map:
        if (mapping[ELM_TAG][TAG] == NAME_TAG):
            if (exoplanet.add_element(exo_data, mapping,
                                     exoplanet.get_head(), tolerance)):
                is_updated = True
        elif (mapping[ELM_TAG][TAG] == PLANET_LAST_UPDATE_TAG):
            exoplanet.update_element(exo_data, mapping, exoplanet.get_head(),
                                     tolerance)
        else:
            if (exoplanet.update_element(exo_data, mapping,
                                         exoplanet.get_head(), tolerance)):
                is_updated = True

    # If the planet is from confirmed planet catalogue add confirmed list tag.
    if ((catalogue == NASA_CON_NAME) or (catalogue == EXO_EU_NAME)):
        planet = exoplanet.get_head()
        old_list = planet.find(PLANET_LIST_TAG)
        if not old_list:
            ET.SubElement(planet, PLANET_LIST_TAG).text = CONFIRMED_LIST
    return is_updated
