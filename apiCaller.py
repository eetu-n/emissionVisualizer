import requests


class ApiCaller:
    def __init__(self):
        self.country_list = []
        self.year_list = []
        self.country_id_dict = {}
        self.population_cache = {}
        self.emissions_cache = {}

    country_url = "http://api.worldbank.org/v2/country/all?format=json&per_page=350"
    country_json = requests.get(country_url).json()
    generic_url = "http://api.worldbank.org/v2/en/country/"
    population_url = "/indicator/SP.POP.TOTL?format=json&per_page=500"
    emissions_url = "/indicator/EN.ATM.CO2E.KT?format=json&per_page=500"

    def temp_get_year_list(self):
        if len(self.year_list) == 0:
            for x in range(1900, 2019):
                self.year_list.append(x)

        return self.year_list

    def get_country_list(self):
        if len(self.country_list) == 0:
            for country in self.country_json[1]:
                self.country_list.append(country['name'])

        return self.country_list

    def get_country_id_dict(self):
        if len(self.country_id_dict) == 0:
            for country in self.country_json[1]:
                self.country_id_dict[country['name']] = country['id'].lower()

        return self.country_id_dict

    def get_country_code(self, name):
        return self.get_country_id_dict()[name]

    def get_population(self, name, year):
        country_id = self.get_country_code(name)
        if country_id not in self.population_cache:
            population_list = requests.get(self.generic_url + country_id + self.population_url).json()[1]
            self.population_cache[country_id] = {}
            for population in population_list:
                self.population_cache[country_id][int(population['date'])] = population['value']

        if not isinstance(year, int):
            year = int(year)

        return self.population_cache[country_id][year]

    def get_emissions(self, name, year):
        country_id = self.get_country_code(name)
        if country_id not in self.emissions_cache:
            emissions_list = requests.get(self.generic_url + country_id + self.emissions_url).json()[1]
            self.emissions_cache[country_id] = {}
            for emissions in emissions_list:
                self.emissions_cache[country_id][int(emissions['date'])] = emissions['value']

        if not isinstance(year, int):
            year = int(year)

        return self.emissions_cache[country_id][year]
