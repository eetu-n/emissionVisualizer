import unittest
from apiCaller import *


class ApiTests(unittest.TestCase):

    # Verify country name list is correct length, and list contains names of countries

    def test_length(self):
        self.assertEqual(304, len(get_country_list()))

    def test_list_1(self):
        self.assertEquals('Aruba', get_country_list()[0])

    def test_list_2(self):
        self.assertEquals('Africa', get_country_list()[2])

    # Verify querying country name returns country ISO 3 code and appropriate error is given with invalid country names

    def test_name_1(self):
        self.assertEqual('dnk', get_country_code('Denmark'))

    def test_name_2(self):
        self.assertEqual('che', get_country_code('Switzerland'))

    def test_name_3(self):
        with self.assertRaises(KeyError):
            get_country_code('NotACountry')

    # Verify querying specific country and year returns correct population, and an invalid year returns proper error

    def test_population_1(self):
        self.assertEqual(9378126, get_population('Sweden', 2010))

    def test_population_2(self):
        self.assertEqual(5338871, get_population('Finland', 2009))

    def test_population_3(self):
        self.assertEqual(7564985, get_population('Austria', 1985))

    def test_population_4(self):
        with self.assertRaises(KeyError):
            get_population('Belarus', 1339)

    # Verify querying specific country and year returns correct CO2 emissions, and appropriate errors for invalid year

    def test_emission_1(self):
        self.assertEqual(58162.287, get_emissions('Norway', 2013))

    def test_emission_2(self):
        self.assertEqual(99944.085, get_emissions('Belgium', 2011))

    def test_emission_3(self):
        self.assertEqual(303275.568, get_emissions('France', 2014))

    def test_emission_4(self):
        with self.assertRaises(KeyError):
            get_emissions('Bulgaria', 3043)
