import unittest
from oec_sync_utils import *

class testConversions(unittest.TestCase):
    
    def testRightAcension(self):
        right_ascension = getattr(conversions, 'to_oec_right_ascension')
        self.assertEqual(right_ascension(286.865479), '19 07 27')
        self.assertEqual(right_ascension(185.1791667), '12 20 43')
        self.assertEqual(right_ascension(0), '00 00 00')
        self.assertEqual(right_ascension(4.82111), '00 19 17')
    def testDeclination(self):
        declination = getattr(conversions, 'to_oec_declination')
        self.assertEqual(declination(-13.98648), '-13 59 11')
        self.assertEqual(declination(41.989086), '+41 59 20')
        self.assertEqual(declination(0), '+00 00 00')
        self.assertEqual(declination(52.552778), '+52 33 10')
    def testLuminosity(self):
        luminosity = getattr(conversions, 'to_oec_luminosity')
        self.assertEqual(round(luminosity(19,4742),2), 163.77)
        self.assertEqual(round(luminosity(0.72,5088),2), 0.31)
        self.assertEqual(round(luminosity(0,0),0), 0.00) 
    def testDateComparison(self):
        comparison = getattr(conversions, 'date_comparison')
        date1 = "2015/10/12"
        date2 = "2016/8/13"
        self.assertFalse(comparison(date1,date2), "date2 is more recent")
        self.assertTrue(comparison(date2,date1), "date2 is more recent")        
        
if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True:
            raise

