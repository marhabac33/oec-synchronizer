#!/usr/bin/python3
#
# Contains classes, to be used for representing system XML files.


import datetime
import logging
import os
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom
from oec_sync_utils.constants import *
from oec_sync_utils.conversions import *
from oec_sync_utils.mappings import *


class XmlFile(object):
    ''' Represents a basic Open Exoplanet Catalogue (OEC) XML document.'''
    
    def __init__(self, root=None):
        ''' (self, xml.etree.ElementTree.Element) -> None
        Initializes a new XML file with a root value.
        '''
        self._root = root

    def __str__(self):
        ''' (self) -> str
        Returns a properly formatted str representation of the XML file,
        sutible for writing to a file.
        '''
        xml_str = ET.tostring(self._root)
        # Format string for proper output from minidom.
        xml_str = re.sub(b'>\s*', b'>', xml_str)
        xml_str = re.sub(b'\s*<', b'<', xml_str) 
        xml_data = xml.dom.minidom.parseString(xml_str)
        return xml_data.toprettyxml()

    def get_head(self):
        ''' (self) -> xml.etree.ElementTree.Element
        Returns root of the XML tree of the XML file.
        '''
        return self._root

    def get_aliases(self):
        ''' (self) -> list of str
        Returns a list of all aliases for the XML Element and all XML
        Subelements in the XML file.
        '''
        aliases = []
        for alias in self._root.iter(NAME_TAG):
            aliases.append(alias.text)
        return aliases

    def add_element(self, data, mapping, parent, tolerance):
        ''' (self, dict{str: str},
             list[tuple(tuple(str, str), list[tuple(str, str)])],
             xml.etree.ElementTree.Element, float) -> bool
        Given exoplanet data in the form of a dict (column name string: data
        value string), a dict mapping (XML metadata tags/attribute: column
        name string), a tuple containing (tuple containing(string XML tag,
        tag mapping key), and list of [tuples containing (XML attribute
        string, attribute mapping key), and the parent xml element. Will add
        a new XML subelement containing the given tag and attribute values to
        the parent XML element. If no data is available in the exoplanet
        data, then nothing is added for that tag or attribute. Returns True
        iff the element or an attribute of the element was updated, else False.
        '''
        updated = False
        (tag, tag_key) = mapping[ELM_TAG]
        attributes = mapping[ELM_ATT]
        # Make sure mapping exists and contains a value:
        if ((tag_key in data) and (data[tag_key] != '')):
            # Get csv value in OEC format.
            value = to_oec_value(data[tag_key], tag_key, tag)
            add_new = True
            # Check if element is already child of parent, if True then exit.
            for check_element in parent.findall(tag):
                # If an existing element has the given value, do not add.
                if (not is_different(check_element.text, value, tolerance)):
                    add_new = False
                    element = check_element
            if (add_new):
                updated = True
                # Add element as child to parent.
                element = ET.SubElement(parent, tag)
                element.text = value
            # Add attributes:
            for (a_tag, a_key) in attributes:
                if ((a_key in data) and (data[a_key] != '')):
                    # Get csv attribute value in OEC format.
                    a_value = to_oec_value(data[a_key], a_key, a_tag)
                    # If the given attribute exists, do not add
                    if (not is_different(element.get(a_tag), a_value,
                                         tolerance)):
                        continue
                    element.attrib[a_tag] = a_value
                    updated = True
        return updated

    def update_element(self, data, mapping, parent, tolerance):
        ''' (self, dict{str: str},
             list[tuple(tuple(str, str), list[tuple(str, str)])],
             xml.etree.ElementTree.Element, float) -> bool
        To be implemented in future sprint, will be used to update existing XML
        element, instead of creating a new one.
        '''
        updated = False
        (tag, tag_key) = mapping[ELM_TAG]
        attributes = mapping[ELM_ATT]
        # Make sure mapping exists and contains a value:
        if ((tag_key in data) and (data[tag_key] != '')):
            element = parent.find(tag)
            value = to_oec_value(data[tag_key], tag_key, tag)
            if (element != None):
                if (is_different(element.text, value, tolerance)):
                    updated = True
                    element.text = value
            else:
                updated = True
                # Add element as child to parent.
                element = ET.SubElement(parent, tag)
                element.text = value
            # Add attributes:
            for (a_tag, a_key) in attributes:
                if ((a_key in data) and (data[a_key] != '')):
                    a_value = to_oec_value(data[a_key], a_key, a_tag)
                    # If the given attribute exists, do not add
                    if (not is_different(element.get(a_tag), a_value,
                                         tolerance)):
                        continue
                    element.attrib[a_tag] = a_value
                    updated = True
        return updated


class SystemXML(XmlFile):
    ''' Represents a System XML file for the Open Exoplanet Catalogue (OEC).'''
    
    def __init__(self, file_name, file_path=None):
        ''' (self, str, str) -> None
        Initializes a SystemXML object with given name and the data from the
        XML file located at the given file path, or an empty xml tree if no
        file path is given.
        '''
        super(SystemXML, self).__init__()
        self.name = file_name[:-4]
        self.file_name = file_name
        self.file_path = file_path
        # If file path is given, then extract root element from XML tree of
        # XML file.
        if file_path:
            xml_tree = ET.parse(file_path)
            self._root = xml_tree.getroot()
            self._commit_msg = (UPDATE_MSG_START + self.file_name)
        else:
            self._root = ET.Element(ROOT_TAG)
            self._commit_msg = (NEW_MSG_START + self.file_name)
        self._pull_msg = (PULL_MSG + self.file_name)
        self._references = []
        self._last_update = {}
        self._validation = False
        # If file path is given, then map each exoplanet alias to the last
        # update date of that exoplanet.
        if file_path:
            for star in self._root.iter(STAR_TAG):
                for exoplanet in star.iter(PLANET_TAG):
                    date = exoplanet.find(PLANET_LAST_UPDATE_TAG)
                    if (not (date is None)):
                        for alias in exoplanet.iter(NAME_TAG):
                            self._last_update[alias.text] = to_oec_date(
                                date.text)
                    else:
                        for alias in exoplanet.iter(NAME_TAG):
                            self._last_update[alias.text] = None                        

    def last_update(self):
        ''' (self) -> dict{str: str}
        Returns a dictionary mapping each exoplanet alias to a string date of
        the last date that exoplanet was updated, or None if no last update
        date was given for that planet.
        '''
        return self._last_update

    def get_stars(self):
        ''' (self) -> list of Stars
        Returns a list of all Star objects contained in this SystemXML.
        '''
        stars = []
        for star in self._root.iter(STAR_TAG):
            stars.append(Star(star))
        return stars

    def get_star(self, alias, exoplanet=None):
        ''' (self, str[, str]) -> Star
        Returns first Star object with given alias or None if no Star has that
        alias. If exoplanet name string is given will also check each Star for
        an exoplanet of given name and return the first Star with given alias
        or exoplanet of that name or None if no Star has the given alias or
        exoplanet of that name.
        '''
        formatted_alias = re.sub(r'\W+|[_]+', '', alias)
        if (not (exoplanet is None)):
            formatted_exoplanet = re.sub(r'\W+|[_]+', '', exoplanet)
        else:
            formatted_exoplanet = None
        stars = self.get_stars()
        for star in stars:
            aliases = star.get_aliases()
            formatted_aliases = []
            for star_alias in aliases:
                formatted_aliases.append(re.sub(r'\W+|[_]+', '', star_alias))
            if ((alias in aliases) or (exoplanet in aliases) or
                (formatted_alias in formatted_aliases) or
                (formatted_exoplanet in formatted_aliases)):
                return star
        return None

    def add_star(self):
        ''' (self) -> Star
        Creates and returns a new Star object that is a child of the SystemXML
        element or binary element if a binary system.
        '''
        binary = self._root.find(BINARY_TAG)
        if (binary == None):
            star = ET.SubElement(self._root, STAR_TAG)
        else:
            star = ET.SubElement(binary, STAR_TAG)
        return Star(star)

    def add_references(self, exoplanet, catalogue):
        ''' (self, str, str) -> None
        Creates a reference url for the given exoplanet in the given catalogue
        and adds reference to this SystemXML file.
        '''
        if (catalogue == NASA_CON_NAME):
            reference = ('http://exoplanetarchive.ipac.caltech.edu/cgi-bin/' +
                         'DisplayOverview/nph-DisplayOverview?objname=' +
                         exoplanet.replace('+', '%2B').replace(' ', '+') +
                         '&type=CONFIRMED_PLANET')
            self._references.append(reference)
        elif (catalogue == EXO_EU_NAME):
            reference = ('http://exoplanet.eu/catalog/' +
                         exoplanet.replace('+', '%2B').replace(' ', '_'))
            self._references.append(reference)
    
    def references_to_str(self):
        ''' (self) -> str
        Returns a string of references for the SystemXML file seperated by ', '
        or '' if the SystemXML has no references.
        '''
        references_str = ''
        for reference in self._references:
            if not references_str:
                references_str = reference
            else:
                references_str += (', ' + reference)
        return references_str

    def add_validation_msg(self):
        ''' (self) -> None
        Tells the SystemXML to generate the Validation version of pull issue
        messages.
        '''
        self._validation = True

    def commit_msg(self, exoplanet, source, validation_req, original_alias):
        ''' (self, str, str) -> str
        Returns a string commit message including the given source for the
        file.
        '''
        if (source == NASA_URL):
            source_url = ('http://exoplanetarchive.ipac.caltech.edu/cgi-bin/' +
                         'DisplayOverview/nph-DisplayOverview?objname=' +
                         exoplanet.replace('+', '%2B').replace(' ', '+') +
                         '&type=CONFIRMED_PLANET')
        elif (source == EXOPLANET_URL):
            source_url = ('http://exoplanet.eu/catalog/' +
                         exoplanet.replace('+', '%2B').replace(' ', '_'))
        else:
            source_url = None
        if (source is None):
            msg = (self._commit_msg + MSG_END)
        elif (source_url is None):
            msg = (self._commit_msg + MSG_MID + source + MSG_END)
        else:
            msg = (self._commit_msg + MSG_MID + source_url + ', ' + source +
                   MSG_END)
        if (validation_req):
            msg = (VALIDATION_REQUIRED + VALIDATION_START + exoplanet +
                   VALIDATION_MID1 + original_alias + VALIDATION_MID2 +
                   self.file_name + VALIDATION_END + msg)            
        return msg

    def pull_title(self):
        ''' (self) -> str
        Returns a string title for a pull message for the SystemXML file.
        '''
        if (self._validation):
            return (VALIDATION_REQUIRED + self._pull_msg + MSG_END)
        return (self._pull_msg + MSG_END)

    def pull_msg(self):
        ''' (self) -> str
        Returns a string pull message including all references for the data
        contained in the file.
        '''
        if (self.references_to_str() == ''):
            msg = (self._pull_msg + MSG_END)            
        else:
            msg = (self._pull_msg + MSG_MID + self.references_to_str() +
                   MSG_END)
        return msg


class Star(XmlFile):
    ''' Represents a Star in a SystemXML file.'''

    def __init__(self, star):
        ''' (self, xml.etree.ElementTree.SubElement) -> None
        Initializes a Star object which is a subelement of a SystemXML file.
        '''
        super(Star, self).__init__(star)

    def get_exoplanets(self):
        ''' (self) -> list of Exoplanets
        Returns a list of all Exoplanet objects around this Star.
        '''
        exoplanets = []
        for exoplanet in self._root.iter(PLANET_TAG):
            exoplanets.append(Exoplanet(exoplanet))
        return exoplanets

    def get_exoplanet(self, alias):
        ''' (self, str) -> Exoplanet
        Returns first Exoplanet object with given alias or None if no
        Exoplanet has that alias.
        '''
        formatted_alias = re.sub(r'\W+|[_]+', '', alias)
        exoplanets = self.get_exoplanets()
        for exoplanet in exoplanets:
            aliases = exoplanet.get_aliases()
            formatted_aliases = []
            for exoplanet_alias in aliases:
                formatted_aliases.append(re.sub(r'\W+|[_]+', '',
                                                exoplanet_alias))
            if ((alias in aliases) or (formatted_alias in formatted_aliases)):
                return exoplanet
        return None

    def add_exoplanet(self):
        ''' (self) -> Exoplanet
        Creates and returns a new Exoplanet object that is a child of current
        star object.
        '''
        exoplanet = ET.SubElement(self._root, PLANET_TAG)
        return Exoplanet(exoplanet)


class Exoplanet(XmlFile):
    ''' Represents a Exoplanet in a SystemXML file.'''

    def __init__(self, exoplanet):
        ''' (self, xml.etree.ElementTree.SubElement) -> None
        Initializes a Exoplanet object which is a subelement of a Star.
        '''
        super(Exoplanet, self).__init__(exoplanet)

