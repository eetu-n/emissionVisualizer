import requests

country_url = "http://api.worldbank.org/v2/country/all?format=json&per_page=304"
country_json = requests.get(country_url).json()


def get_country_list():
    country_list = []
    for country in country_json[1]:
        country_list.append(country['name'])
    return country_list


def get_country_code(name):
    pass


def get_population(name, year):
    pass


def get_emissions(name, year):
    pass


print(get_country_list())
