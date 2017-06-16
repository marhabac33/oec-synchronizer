from oec_sync_utils import *
import unittest
import os
import socket
import urllib.request as req

class TestCSVDownloader(unittest.TestCase):
	'''Test class to test the csv downloader module'''

	def test_nasa_site(self):
		'''Test Nasa Exoplanet site'''
		dir_name = "test_dir"
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)
			download_csv_file(NASA_URL, NASA_CON_NAME + CSV_END, dir_name)
			path = os.path.join(os.getcwd(), dir_name, (NASA_CON_NAME + CSV_END))
			self.assertTrue(os.path.exists(path))
			os.remove(path)
			os.rmdir(dir_name)
		else:
			self.fail()

	def test_exoplanet_site(self):
		'''Test Nasa Exoplanet site'''
		dir_name = "test_dir"
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)
			download_csv_file(EXOPLANET_URL, EXO_EU_NAME + CSV_END, dir_name)
			path = os.path.join(os.getcwd(), dir_name, (EXO_EU_NAME + CSV_END))
			self.assertTrue(os.path.exists(path))
			os.remove(path)
			os.rmdir(dir_name)
		else:
			self.fail()

	def test_Invalid(self):
		'''check if ValueError cause the return to be None when invalid URL is passed'''
		try:
			self.assertEqual(download_csv_file('InvalidURL', 'invalidurlfile', 'invaliddir'), None)
		except:
			self.fail()


if (__name__ == '__main__'):
	unittest.main()
