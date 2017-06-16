from oec_sync_utils.system_xml import *
import os
import unittest


# String of xml file for use in testing.
SAMPLE_XML_STR = '<?xml version="1.0" ?>\n<system>\n\t<name>test1</name>\n\t<name>test2</name>\n\t<rightascension/>\n\t<declination/>\n\t<distance/>\n\t<star>\n\t\t<name>test1.1</name>\n\t\t<name>test1.2</name>\n\t\t<mass/>\n\t\t<radius/>\n\t\t<temperature/>\n\t\t<magV/>\n\t\t<metallicity/>\n\t\t<spectraltype/>\n\t\t<planet>\n\t\t\t<name>test1.1.a</name>\n\t\t\t<name>test1.2.a</name>\n\t\t\t<list>Confirmed planets</list>\n\t\t\t<mass/>\n\t\t\t<radius/>\n\t\t\t<temperature/>\n\t\t\t<period/>\n\t\t\t<semimajoraxis/>\n\t\t\t<eccentricity/>\n\t\t\t<inclination/>\n\t\t\t<periastron/>\n\t\t\t<longitude/>\n\t\t\t<description>This file is only a sample xml for testing.</description>\n\t\t\t<discoverymethod>RV</discoverymethod>\n\t\t\t<istransiting>1</istransiting>\n\t\t\t<lastupdate>16/09/17</lastupdate>\n\t\t\t<discoveryyear>2014</discoveryyear>\n\t\t\t<image/>\n\t\t\t<imagedescription/>\n\t\t\t<spinorbitalignment/>\n\t\t</planet>\n\t\t<planet>\n\t\t\t<name>test1.1.b</name>\n\t\t\t<name>test1.2.b</name>\n\t\t\t<list>Confirmed planets</list>\n\t\t\t<mass/>\n\t\t\t<radius/>\n\t\t\t<temperature/>\n\t\t\t<period/>\n\t\t\t<semimajoraxis/>\n\t\t\t<eccentricity/>\n\t\t\t<inclination/>\n\t\t\t<periastron/>\n\t\t\t<longitude/>\n\t\t\t<description>This file is only a sample xml for testing.</description>\n\t\t\t<discoverymethod>RV</discoverymethod>\n\t\t\t<istransiting>1</istransiting>\n\t\t\t<lastupdate>16/09/17</lastupdate>\n\t\t\t<discoveryyear>2014</discoveryyear>\n\t\t\t<image/>\n\t\t\t<imagedescription/>\n\t\t\t<spinorbitalignment/>\n\t\t</planet>\n\t</star>\n</system>\n'

COMMIT_STR = 'OEC Synchronizer automatically generated update of test.xml.'
EXO_URL = 'http://exoplanet.eu/catalog/csv'
COMMIT_SOURCE_URL_STR = 'OEC Synchronizer automatically generated update of test.xml from http://exoplanet.eu/catalog/test.csv, http://exoplanet.eu/catalog/csv.'
VALIDATION_COMMIT_STR = "OEC SYNC VALIDATION REQUIRED: OEC Synchronizer thought that test.csv looked like TeSt.csv in test.xml, if pull request is closed without merging, a new file will be generated for this planet on next run. OEC Synchronizer automatically generated update of test.xml."

EXO_EU_NAME = "exoplanet_eu_exoplanets"

PULL_STR = 'OEC Synchronizer automatically generated update for: test.xml.'

PULL_REF_STR = 'OEC Synchronizer automatically generated update for: test.xml from http://exoplanet.eu/catalog/test.'

MAP_DICT = {'test': 'res', 'test1.1': 'res1', 'test2.1': 'res2'}
MAP_TAG = (('test', 'test'), [])
MAP_ATT = (('test', 'test'), [('test1', 'test1.1')])
MAP_ATTS = (('test', 'test'), [('test1', 'test1.1'), ('test2', 'test2.1')])


class TestSystemXML(unittest.TestCase):

    def testStr(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        self.assertEqual(str(test_xml), SAMPLE_XML_STR)

    def testGetAliases(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        self.assertEqual(set(test_xml.get_aliases()),
                         set(['test1', 'test2', 'test1.1', 'test1.2',
                             'test1.1.a', 'test1.2.a', 'test1.1.b',
                             'test1.2.b']))

    def testGetStars(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        stars = test_xml.get_stars()
        self.assertEqual(len(stars), 1)

    def testGetStar(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        star = test_xml.get_star('test1.1')
        self.assertTrue('test1.1' in star.get_aliases())
        star = test_xml.get_star('false')
        self.assertTrue(star is None)
        star = test_xml.get_star('test1.1', 'test1.1.a')
        self.assertTrue('test1.1' in star.get_aliases())
        star = test_xml.get_star('false', 'test1.1.a')
        self.assertTrue('test1.1' in star.get_aliases())
        star = test_xml.get_star('test1.1', 'false')
        self.assertTrue('test1.1' in star.get_aliases())
        star = test_xml.get_star('false', 'false')
        self.assertTrue(star is None)

    def testAddStar(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        test_xml.add_star()
        stars = test_xml.get_stars()
        self.assertEqual(len(stars), 2)

    def testReferences(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        self.assertEqual(test_xml.references_to_str(), '')
        test_xml.add_references('test', EXO_EU_NAME)
        self.assertEqual(test_xml.references_to_str(),
                         'http://exoplanet.eu/catalog/test')
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        test_xml.add_references('test', 'invalid test')
        self.assertEqual(test_xml.references_to_str(), '')
    
    def testCommitMsg(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        self.assertEqual(test_xml.commit_msg('test.csv', None, False, None),
                         COMMIT_STR)
        self.assertEqual(test_xml.commit_msg('test.csv', EXO_URL, False, None),
                         COMMIT_SOURCE_URL_STR)
        self.assertEqual(test_xml.commit_msg('test.csv', None, True, 'TeSt.csv'),
                         VALIDATION_COMMIT_STR)        

    def testPullMsg(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        self.assertEqual(test_xml.pull_msg(), PULL_STR)
        test_xml.add_references('test', EXO_EU_NAME)        
        self.assertEqual(test_xml.pull_msg(), PULL_REF_STR)

    def testGetExoplanets(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        star = test_xml.get_star('test1.1')
        planets = star.get_exoplanets()
        self.assertEqual(len(planets), 2)

    def testGetExoplanet(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        star = test_xml.get_star('test1.1')
        exoplanet = star.get_exoplanet('test1.2.a')
        self.assertTrue('test1.2.a' in exoplanet.get_aliases())
        exoplanet = star.get_exoplanet('false')
        self.assertTrue(exoplanet is None)

    def testAddExoplanet(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        star = test_xml.get_star('test1.1')
        star.add_exoplanet()
        planets = star.get_exoplanets()
        self.assertEqual(len(planets), 3)

    def testAddElement(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        elm = test_xml.get_head().find('test')
        self.assertTrue(elm is None)
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        test_xml.add_element(MAP_DICT, MAP_TAG, test_xml.get_head(), 0)
        elm = test_xml.get_head().find('test')
        self.assertEqual(elm.text, 'res')
        self.assertTrue(not 'test1' in elm.attrib)
        self.assertTrue(not 'test2' in elm.attrib)
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        test_xml.add_element(MAP_DICT, MAP_ATT, test_xml.get_head(), 0)
        elm = test_xml.get_head().find('test')
        self.assertEqual(elm.text, 'res')
        self.assertEqual(elm.attrib['test1'], 'res1')
        self.assertTrue(not 'test2' in elm.attrib)
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        test_xml.add_element(MAP_DICT, MAP_ATTS, test_xml.get_head(), 0)
        elm = test_xml.get_head().find('test')
        self.assertEqual(elm.text, 'res')
        self.assertEqual(elm.attrib['test1'], 'res1')
        self.assertEqual(elm.attrib['test2'], 'res2')

    def testUpdateElement(self):
        test_xml = SystemXML('test.xml', './test_data/test.xml')
        elm = test_xml.get_head().find('test')
        self.assertTrue(elm is None)
        test_xml.update_element(MAP_DICT, MAP_TAG, test_xml.get_head(), 0)
        elm = test_xml.get_head().find('test')
        self.assertEqual(elm.text, 'res')
        self.assertTrue(not 'test1' in elm.attrib)
        self.assertTrue(not 'test2' in elm.attrib)
        test_xml.update_element(MAP_DICT, MAP_ATT, test_xml.get_head(), 0)
        elm = test_xml.get_head().find('test')
        self.assertEqual(elm.text, 'res')
        self.assertEqual(elm.attrib['test1'], 'res1')
        self.assertTrue(not 'test2' in elm.attrib)
        test_xml.update_element(MAP_DICT, MAP_ATTS, test_xml.get_head(), 0)
        elm = test_xml.get_head().find('test')
        self.assertEqual(elm.text, 'res')
        self.assertEqual(elm.attrib['test1'], 'res1')
        self.assertEqual(elm.attrib['test2'], 'res2')


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True:
            raise