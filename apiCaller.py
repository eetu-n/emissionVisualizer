import requests

country_url = "http://api.worldbank.org/v2/country/all?format=json&per_page=350"
country_json = requests.get(country_url).json()
country_list = []
country_id_dict = {}


def get_country_list():
    global country_list
    if len(country_list) == 0:
        country_list = []
        for country in country_json[1]:
            country_list.append(country['name'])

    return country_list


def get_country_id_dict():
    global country_id_dict
    if len(country_id_dict) == 0:
        for country in country_json[1]:
            country_id_dict[country['name']] = country['id'].lower()

    return country_id_dict


def get_country_code(name):
    return get_country_id_dict()[name]


def get_population(name, year):
    pass


def get_emissions(name, year):
    pass
