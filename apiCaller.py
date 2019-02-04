import requests

country_url = "http://api.worldbank.org/v2/country/all?format=json&per_page=304"
country_json = requests.get(country_url).json()
country_amount = country_json[0]['total']

# Return list of countries


def get_country_list():
    pass


def get_country_code(name):
    pass


def get_population(name, year):
    pass


def get_emissions(name, year):
    pass
