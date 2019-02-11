from flask import Flask, render_template, request, jsonify
from apiCaller import ApiCaller

app = Flask(__name__)

api_caller = ApiCaller()


@app.route('/', methods=["POST", "GET"])
def index():
    country_list = api_caller.get_country_list()
    generic_year_list = api_caller.get_generic_year_list()
    year_min = int(1960)
    year_max = api_caller.get_current_year()
    country = None
    data_type = None
    labels = generic_year_list
    values = []
    is_empty = False
    received = False
    invalid = False

    if request.method == "POST":
        country = request.form.get('country_selector')
        if country not in country_list:
            invalid = True

        year_min = int(request.form.get('selected_year_min'))
        year_max = int(request.form.get('selected_year_max'))
        per_capita_selector = request.form.get('selected_data')

        if per_capita_selector == "on":
            data_type = "emissions_per_capita"
        else:
            data_type = "emissions"

        if not invalid:
            data_dict = api_caller.get_data_range(country, data_type, year_min, year_max)
            labels = list(data_dict.keys())
            values = list(data_dict.values())
            is_empty = api_caller.get_year_list(country, data_type, year_min, year_max) == []

        received = True

    return render_template('index.html', country_list=country_list, generic_year_list=generic_year_list,
                           country=country, year_min=year_min, year_max=year_max, data_type=data_type,
                           labels=labels, values=values, received=received, is_empty=is_empty, invalid=invalid)


# Api routing section

@app.route('/api', methods=["GET"])
def api():
    return "<h1>Emission Visualizer API</h1>" \
           "<p>The API returns the following data in json format:</p>" \
           "<ul>" \
           "<li>A list of countries with api/country_list</li>" \
           "<li>A list of countries with their corresponding ISO3 codes with api/country_id_list</li>" \
           "<li>Data per country can be found through api/data, with the following argument options" \
           "<ul>" \
                "<li>Specify a country with country=[ISO] (required)</li>" \
                "<li>Specify type of data with data_type= emissions, emissions_per_capita or population " \
                "(defaults to emissions)</li>" \
                "<li>Specify specific year with year=int (defaults to a year range instead)</li>" \
                "<li>Specify a year range with year_min=int and year_max=int (defaults to all available data)</li>" \
           "</ul></li></ul>"


@app.route('/api/country_id_list', methods=["GET"])
def country_id_list():
    return jsonify(api_caller.get_country_id_dict())


@app.route('/api/country_list', methods=["GET"])
def country_list():
    return jsonify(api_caller.get_country_list())


@app.route('/api/data', methods=["GET"])
def data():
    request_data_type = request.args.get('data_type')
    request_year = request.args.get('year')
    request_country = request.args.get('country')
    request_year_min = request.args.get('year_min')
    request_year_max = request.args.get('year_max')

    if request_year is not None:
        request_year = int(request_year)

    if request_year_min is None:
        request_year_min = 1960
    else:
        request_year_min = int(request_year_min)

    if request_year_max is None:
        request_year_max = api_caller.get_current_year()
    else:
        request_year_max = int(request_year_max)

    if request_data_type is None:
        request_data_type = 'emissions'

    if request_country is None:
        return "<h1>Please specify a valid country</h1>" \
               "<p>Use country=ISO in the arguments.</p>"
    else:
        request_country = api_caller.get_country_name(request_country)

    if request_year is None:
        return jsonify(api_caller.get_data_range(request_country, request_data_type,
                                                 request_year_min, request_year_max))
    elif request_data_type == 'emissions':
        return jsonify(api_caller.get_emissions(request_country, request_year))

    elif request_data_type == 'emissions_per_capita':
        return jsonify(api_caller.get_emissions_per_capita(request_country, request_year))

    elif request_data_type == 'population':
        return jsonify(api_caller.get_population(request_country, request_year))

    return 'Something went wrong'


if __name__ == '__main__':
    app.run()
