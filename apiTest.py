import unittest
from apiCaller import ApiCaller


class ApiTests(unittest.TestCase):

    # Verify country name list is correct length, and list contains names of countries

    def test_country_list_1(self):
        api_caller = ApiCaller()
        self.assertEqual('Aruba', api_caller.get_country_list()[0])

    # Test that regions are not included

    def test_country_list_2(self):
        api_caller = ApiCaller()
        self.assertTrue('Africa' not in api_caller.get_country_list())

    def test_country_dict_1(self):
        api_caller = ApiCaller()
        self.assertTrue('Africa' not in api_caller.get_country_id_dict())

    # Make sure both are the same length

    def test_country_dict_2(self):
        api_caller = ApiCaller()
        country_list = api_caller.get_country_list()
        country_dict = api_caller.get_country_id_dict()
        self.assertTrue(len(country_list) == len(country_dict))

    # Verify querying year range for specific country returns years with data

    def test_year_range_1(self):
        api_caller = ApiCaller()
        year_range = [2003, 2004, 2005]
        self.assertEqual(year_range, api_caller.get_year_list('Zimbabwe', 'emissions', 2005, 2003))

    def test_year_range_2(self):
        api_caller = ApiCaller()
        year_range = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
        self.assertEqual(year_range, api_caller.get_year_list('Indonesia', 'population', 2010, 3000))

    def test_year_range_3(self):
        api_caller = ApiCaller()
        year_range = [1986, 1987, 1988]
        self.assertEqual(year_range, api_caller.get_year_list('Aruba', 'emissions_per_capita', 1900, 1988))

        # Test to see if caching functions properly

    def test_year_range_4(self):
        api_caller = ApiCaller()
        year_range = [1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970]
        api_caller.get_year_list('Philippines', 'emissions', 1000, 1970)
        self.assertEqual(year_range, api_caller.get_year_list('Philippines', 'emissions', 1000, 1970))

    def test_year_range_5(self):
        api_caller = ApiCaller()
        year_range = []
        self.assertEqual(year_range, api_caller.get_year_list('Portugal', 'population', 1900, 1923))

    def test_year_range_6(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_year_list('Portugal', 2, 1967, 1970)

    def test_year_range_7(self):
        api_caller = ApiCaller()
        with self.assertRaises(ValueError):
            api_caller.get_year_list('Portugal', 'asd', 1967, 1970)

    def test_year_range_8(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_year_list('Portugal', 'population', 'asd', 1970)

    def test_year_range_9(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_year_list('Portugal', 'population', 1967, 'asd')

    # Verify querying country name returns country ISO 3 code and appropriate error is given with invalid country names

    def test_name_1(self):
        api_caller = ApiCaller()
        self.assertEqual('dnk', api_caller.get_country_code('Denmark'))

    def test_name_2(self):
        api_caller = ApiCaller()
        self.assertEqual('gbr', api_caller.get_country_code('United Kingdom'))

        # Test to see if caching functions properly

    def test_name_3(self):
        api_caller = ApiCaller()
        api_caller.get_country_code('Sweden')
        self.assertEqual('swe', api_caller.get_country_code('Sweden'))

        # Test errors

    def test_name_4(self):
        api_caller = ApiCaller()
        with self.assertRaises(KeyError):
            api_caller.get_country_code('NotACountry')

    def test_name_5(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_country_code(True)

    # Verify querying data returns correct results and proper errors

    def test_data_1(self):
        api_caller = ApiCaller()
        self.assertEqual(9378126, api_caller.get_data('Sweden', 'population', 2010))

    def test_data_2(self):
        api_caller = ApiCaller()
        self.assertEqual(58162.287, api_caller.get_data('Norway', 'emissions', 2013))

    def test_data_3(self):
        api_caller = ApiCaller()
        self.assertEqual(0.369, api_caller.get_data('Costa Rica', 'emissions_per_capita', 1960))

    def test_data_4(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_data(True, 'emissions', 2009)

    def test_data_5(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_data('Belarus', True, 2009)

    def test_data_6(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_data('Sweden', 'emissions', True)

    def test_data_7(self):
        api_caller = ApiCaller()
        with self.assertRaises(KeyError):
            api_caller.get_data('NotACountry', 'emissions', 2009)

    def test_data_8(self):
        api_caller = ApiCaller()
        with self.assertRaises(ValueError):
            api_caller.get_data('Norway', 'notData', 2009)

    def test_data_9(self):
        api_caller = ApiCaller()
        with self.assertRaises(KeyError):
            api_caller.get_data('Canada', 'emissions', 1000)

    # Verify that querying range of years returns correct range of population values

    def test_population_range_1(self):
        api_caller = ApiCaller()
        test_range = {
            2009: 71339185,
            2010: 72326914,
            2011: 73409455}
        self.assertEqual(test_range, api_caller.get_data_range('Turkey', 'population', 2009, 2011))

    def test_population_range_2(self):
        api_caller = ApiCaller()
        test_range = {
            2007: 7180100,
            2008: 7308800}
        self.assertEqual(test_range, api_caller.get_data_range('Israel', 'population', 2007, 2008))

        # Test to see if caching functions properly

    def test_population_range_3(self):
        api_caller = ApiCaller()
        test_range = {
            2005: 16319868,
            2006: 16346101,
            2007: 16381696,
            2008: 16445593}
        api_caller.get_data_range('Netherlands', 'population', 2005, 2008)
        self.assertEqual(test_range, api_caller.get_data_range('Netherlands', 'population', 2005, 2008))

    # Verify that querying range of years returns correct range of emission values

    def test_emissions_range_1(self):
        api_caller = ApiCaller()
        test_range = {
            2010: 493207.833,
            2011: 447828.708,
            2012: 468572.927,
            2013: 458250.322,
            2014: 419820.162}
        self.assertEqual(test_range, api_caller.get_data_range('United Kingdom', 'emissions', 2010, 2014))

    def test_emissions_range_2(self):
        api_caller = ApiCaller()
        test_range = {
            1986: 102874.018,
            1987: 103116.04,
            1988: 100354.789,
            1989: 107461.435,
            1990: 106049.64}
        self.assertEqual(test_range, api_caller.get_data_range('Belgium', 'emissions', 1986, 1990))

        # Test to see if caching functions properly

    def test_emissions_range_3(self):
        api_caller = ApiCaller()
        test_range = {
            1969: 12112.101,
            1970: 21539.958,
            1971: 32280.601}
        api_caller.get_data_range('Nigeria', 'emissions', 1969, 1971)
        self.assertEqual(test_range, api_caller.get_data_range('Nigeria', 'emissions', 1969, 1971))

    # Verify error detection for get_data_range

    def test_data_range_error_1(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_data_range(True, 'emissions', 1969, 1971)

    def test_data_range_error_2(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_data_range('Nigeria', True, 1969, 1971)

    def test_data_range_error_3(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_data_range('Nigeria', 'emissions', False, 1971)

    def test_data_range_error_4(self):
        api_caller = ApiCaller()
        with self.assertRaises(TypeError):
            api_caller.get_data_range('Nigeria', 'emissions', 1969, False)

    def test_data_range_error_5(self):
        api_caller = ApiCaller()
        with self.assertRaises(ValueError):
            api_caller.get_data_range('Nigeria', 'asd', 1969, 1971)
