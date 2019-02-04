import requests

country_url = "http://api.worldbank.org/v2/country/all?format=json&per_page=350"
country_json = requests.get(country_url).json()
generic_url = "http://api.worldbank.org/v2/en/country/"
population_url = "/indicator/SP.POP.TOTL?format=json&per_page=500"
emissions_url = "/indicator/EN.ATM.CO2E.KT?format=json&per_page=500"
country_list = []
country_id_dict = {}
population_cache = {}
emissions_cache = {}


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
    global population_cache
    country_id = get_country_code(name)
    if country_id not in population_cache:
        population_list = requests.get(generic_url + country_id + population_url).json()[1]
        population_cache[country_id] = {}
        for population in population_list:
            population_cache[country_id][int(population['date'])] = population['value']

    return population_cache[country_id][year]


def get_emissions(name, year):
    global emissions_cache
    country_id = get_country_code(name)
    if country_id not in emissions_cache:
        emissions_list = requests.get(generic_url + country_id + emissions_url).json()[1]
        emissions_cache[country_id] = {}
        for emissions in emissions_list:
            emissions_cache[country_id][int(emissions['date'])] = emissions['value']

    return emissions_cache[country_id][year]
