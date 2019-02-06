import unittest
from apiCaller import ApiCaller


class ApiTests(unittest.TestCase):
    global apiCaller
    apiCaller = ApiCaller()

    # Verify country name list is correct length, and list contains names of countries

    def test_country_list_length(self):
        self.assertEqual(304, len(apiCaller.get_country_list()))

    def test_country_list_1(self):
        self.assertEqual('Aruba', apiCaller.get_country_list()[0])

    def test_country_list_2(self):
        self.assertEqual('Africa', apiCaller.get_country_list()[2])

    # Verify querying year range for specific country returns years with data

    def test_year_range_1(self):
        year_range = [2003, 2004, 2005]
        self.assertEqual(year_range, apiCaller.get_year_list('Zimbabwe', 'emissions', 2005, 2003))

    def test_year_range_2(self):
        year_range = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
        self.assertEqual(year_range, apiCaller.get_year_list('Indonesia', 'population', 2010, 3000))

    def test_year_range_3(self):
        year_range = [1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970]
        self.assertEqual(year_range, apiCaller.get_year_list('Philippines', 'emissions', 1000, 1970))

    def test_year_range_4(self):
        year_range = []
        self.assertEqual(year_range, apiCaller.get_year_list('Portugal', 'population', 1900, 1923))

    def test_year_range_5(self):
        with self.assertRaises(TypeError):
            apiCaller.get_year_list('Portugal', 2, 1967, 1970)

    def test_year_range_6(self):
        with self.assertRaises(ValueError):
            apiCaller.get_year_list('Portugal', 'asd', 1967, 1970)

    def test_year_range_7(self):
        with self.assertRaises(TypeError):
            apiCaller.get_year_list('Portugal', 'population', 'asd', 1970)

    def test_year_range_8(self):
        with self.assertRaises(TypeError):
            apiCaller.get_year_list('Portugal', 'population', 1967, 'asd')

    # Verify querying country name returns country ISO 3 code and appropriate error is given with invalid country names

    def test_name_1(self):
        self.assertEqual('dnk', apiCaller.get_country_code('Denmark'))

    def test_name_2(self):
        self.assertEqual('gbr', apiCaller.get_country_code('United Kingdom'))

    def test_name_3(self):
        with self.assertRaises(KeyError):
            apiCaller.get_country_code('NotACountry')

    def test_name_4(self):
        with self.assertRaises(TypeError):
            apiCaller.get_country_code(True)

    # Verify querying specific country and year returns correct population, and an invalid year returns proper error

    def test_population_1(self):
        self.assertEqual(9378126, apiCaller.get_population('Sweden', 2010))

    def test_population_2(self):
        self.assertEqual(5338871, apiCaller.get_population('Finland', 2009))

    def test_population_3(self):
        self.assertEqual(7564985, apiCaller.get_population('Austria', 1985))

    def test_population_4(self):
        with self.assertRaises(KeyError):
            apiCaller.get_population('Belarus', 1339)

    def test_population_5(self):
        with self.assertRaises(TypeError):
            apiCaller.get_population(True, 2009)

    def test_population_6(self):
        with self.assertRaises(TypeError):
            apiCaller.get_population('Belarus', True)

    # Verify querying specific country and year returns correct CO2 emissions, and appropriate errors for invalid year

    def test_emission_1(self):
        self.assertEqual(58162.287, apiCaller.get_emissions('Norway', 2013))

    def test_emission_2(self):
        self.assertEqual(99944.085, apiCaller.get_emissions('Belgium', 2011))

    def test_emission_3(self):
        self.assertEqual(303275.568, apiCaller.get_emissions('France', 2014))

    def test_emission_4(self):
        with self.assertRaises(KeyError):
            apiCaller.get_emissions('Bulgaria', 3043)

    def test_emission_5(self):
        with self.assertRaises(TypeError):
            apiCaller.get_emissions(True, 2011)

    def test_emission_6(self):
        with self.assertRaises(TypeError):
            apiCaller.get_emissions('Bulgaria', True)

    # Verify that querying range of years returns correct range of population values

    def test_population_range_1(self):
        test_range = {
            2009: 71339185,
            2010: 72326914,
            2011: 73409455}
        self.assertEqual(test_range, apiCaller.get_data_range('Turkey', 'population', 2009, 2011))

    def test_population_range_2(self):
        test_range = {
            2007: 7180100,
            2008: 7308800}
        self.assertEqual(test_range, apiCaller.get_data_range('Israel', 'population', 2007, 2008))

    def test_population_range_3(self):
        test_range = {
            2005: 16319868,
            2006: 16346101,
            2007: 16381696,
            2008: 16445593}
        self.assertEqual(test_range, apiCaller.get_data_range('Netherlands', 'population', 2005, 2008))

    # Verify that querying range of years returns correct range of emission values

    def test_emissions_range_1(self):
        test_range = {
            2010: 493207.833,
            2011: 447828.708,
            2012: 468572.927,
            2013: 458250.322,
            2014: 419820.162}
        self.assertEqual(test_range, apiCaller.get_data_range('United Kingdom', 'emissions', 2010, 2014))

    def test_emissions_range_2(self):
        test_range = {
            1986: 102874.018,
            1987: 103116.04,
            1988: 100354.789,
            1989: 107461.435,
            1990: 106049.64}
        self.assertEqual(test_range, apiCaller.get_data_range('Belgium', 'emissions', 1986, 1990))

    def test_emissions_range_3(self):
        test_range = {
            1969: 12112.101,
            1970: 21539.958,
            1971: 32280.601}
        self.assertEqual(test_range, apiCaller.get_data_range('Nigeria', 'emissions', 1969, 1971))

    # Verify error detection for get_data_range

    def test_data_error_1(self):
        with self.assertRaises(TypeError):
            apiCaller.get_data_range(True, 'emissions', 1969, 1971)

    def test_data_error_2(self):
        with self.assertRaises(TypeError):
            apiCaller.get_data_range('Nigeria', True, 1969, 1971)

    def test_data_error_3(self):
        with self.assertRaises(TypeError):
            apiCaller.get_data_range('Nigeria', 'emissions', False, 1971)

    def test_data_error_4(self):
        with self.assertRaises(TypeError):
            apiCaller.get_data_range('Nigeria', 'emissions', 1969, False)

    def test_data_error_5(self):
        with self.assertRaises(ValueError):
            apiCaller.get_data_range('Nigeria', 'asd', 1969, 1971)
