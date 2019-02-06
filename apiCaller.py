import requests


class ApiCaller:
    def __init__(self):
        self.country_list = []
        self.country_id_dict = {}
        self.population_cache = {}
        self.emissions_cache = {}
        self.population_year_cache = {}
        self.emissions_year_cache = {}

    country_url = "http://api.worldbank.org/v2/country/all?format=json&per_page=350"
    country_json = requests.get(country_url).json()
    generic_url = "http://api.worldbank.org/v2/en/country/"
    population_url = "/indicator/SP.POP.TOTL?format=json&per_page=500"
    emissions_url = "/indicator/EN.ATM.CO2E.KT?format=json&per_page=500"

    def get_year_list(self, country, data_type, year_min, year_max):
        if type(country) is not str:
            raise TypeError("country is expected to be of type str, got " + type(country))

        if type(data_type) is not str:
            raise TypeError("data_type is expected to be of type str, got " + type(data_type))

        if data_type != 'emissions' and data_type != 'population':
            raise ValueError("data_type must be 'emissions' or 'population'")

        if type(year_min) is not int:
            raise TypeError("year_min is expected to be of type int, got " + type(year_min))

        if type(year_max) is not int:
            raise TypeError("year_min is expected to be of type int, got " + type(year_max))

        country_id = self.get_country_code(country)
        year_list = []
        if year_min > year_max:
            temp = year_max
            year_max = year_min
            year_min = temp

        if country_id not in self.emissions_year_cache and data_type == 'emissions':
            emissions_list = (requests.get(self.generic_url + country_id + self.emissions_url)).json()
            for x in emissions_list[1]:
                if x['value'] is not None:
                    year_list.insert(0, int(x['date']))

            self.emissions_year_cache[country_id] = year_list

        elif country_id in self.emissions_year_cache:
            year_list = self.population_year_cache[country_id]

        if country_id not in self.population_year_cache and data_type == 'population':
            population_list = (requests.get(self.generic_url + country_id + self.population_url)).json()
            for x in population_list[1]:
                if x['value'] is not None:
                    year_list.insert(0, int(x['date']))

            self.population_year_cache[country_id] = year_list

        elif country_id in self.population_year_cache:
            year_list = self.population_year_cache[country_id]

        year_list = list(set(year_list) & set(range(year_min, year_max + 1)))
        year_list.sort()

        return year_list

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

    def get_country_code(self, country):
        if type(country) is not str:
            raise TypeError("country is expected to be of type str, got " + type(country))

        return self.get_country_id_dict()[country]

    def get_population(self, country, year):
        if type(country) is not str:
            raise TypeError("country is expected to be of type str, got " + type(country))

        if type(year) is not int:
            raise TypeError("year is expected to be of type int, got " + type(year))

        country_id = self.get_country_code(country)
        if country_id not in self.population_cache:
            population_list = requests.get(self.generic_url + country_id + self.population_url).json()[1]
            self.population_cache[country_id] = {}
            for population in population_list:
                self.population_cache[country_id][int(population['date'])] = population['value']

        if type(year) is not int:
            year = int(year)

        return self.population_cache[country_id][year]

    def get_emissions(self, country, year):
        if type(country) is not str:
            raise TypeError("country is expected to be of type str, got " + type(country))

        if type(year) is not int:
            raise TypeError("year is expected to be of type int, got " + type(year))

        country_id = self.get_country_code(country)
        if country_id not in self.emissions_cache:
            emissions_list = requests.get(self.generic_url + country_id + self.emissions_url).json()[1]
            self.emissions_cache[country_id] = {}
            for emissions in emissions_list:
                self.emissions_cache[country_id][int(emissions['date'])] = emissions['value']

        if type(year) is not int:
            year = int(year)

        return self.emissions_cache[country_id][year]

    def get_data_range(self, country, data_type, year_min, year_max):
        if type(country) is not str:
            raise TypeError("country is expected to be of type str, got " + type(country))

        if type(data_type) is not str:
            raise TypeError("data_type must be of type str, got " + type(data_type))

        if type(year_min) is not int:
            raise TypeError("year_min is expected to be of type int, got " + type(year_min))

        if type(year_max) is not int:
            raise TypeError("year_max is expected to be of type int, got " + type(year_max))

        if data_type != "emissions" and data_type != "population":
            raise ValueError("data_type must be either 'emissions' or 'population'")

        year_range = self.get_year_list(country, data_type, year_min, year_max)
        data_range = {}

        if data_type == "emissions":
            for year in year_range:
                data_range[year] = self.get_emissions(country, year)
        elif data_type == "population":
            for year in year_range:
                data_range[year] = self.get_population(country, year)

        return data_range
