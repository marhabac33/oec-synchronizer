from oec_sync_utils import *
import unittest

class TestSystemFunctions(unittest.TestCase):

	def test_set_xml_aliases(self):
		test_xml_file = SystemXML('functions_test.xml',
		                          'test_data/functions_test.xml')
		test2_xml_file = SystemXML('functions_test.xml',
		                           'test_data/test.xml')
		aliases = test_xml_file.get_aliases()
		aliases2 = test2_xml_file.get_aliases()
		exp_keysexp_result = {}

		for item in aliases:
			exp_keysexp_result[item] = ''
		
		for item in aliases2:
			exp_keysexp_result[item] = ''		

		result = {}
		set_xml_aliases('test_data', result)

		self.assertEqual(set(result.keys()), set(exp_keysexp_result.keys()))


if __name__ == '__main__':
	try:
		unittest.main()
	except SystemExit as inst:
		if inst.args[0] is True:
			raise