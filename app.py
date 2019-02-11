from flask import Flask, render_template, request, jsonify
from apiCaller import ApiCaller

app = Flask(__name__)

api_caller = ApiCaller()


# Returns a color based on the hash of the country name
def get_color(name: str):
    name_hash = str(hash(name) % 10 ** 9)

    def to_hex(num):
        return str(int((num/999)*255))

    r = to_hex(int(name_hash[0:3]))
    b = to_hex(int(name_hash[3:6]))
    g = to_hex(int(name_hash[6:9]))

    return "rgb(" + r + "," + g + "," + b + ')'


@app.route('/', methods=["POST", "GET"])
def index():
    generic_country_list = api_caller.get_country_list()
    generic_year_list = api_caller.get_generic_year_list()
    year_min = int(1960)
    year_max = ApiCaller().get_current_year()
    data_type = None
    data_dict = {}
    labels = generic_year_list
    values = []
    is_empty = False
    received = False
    invalid = False
    input_country_list = []
    country_amount = 0
    color_list = []

    if request.method == "POST":
        input_country_list = request.form.get('input_country_list').split(";")
        for country in input_country_list:
            if country not in generic_country_list:
                input_country_list.remove(country)

        country_amount = len(input_country_list)

        if country_amount == 0:
            invalid = True
        else:
            input_country_list = sorted(input_country_list)
            get_color(input_country_list[0])

        for country in input_country_list:
            color_list.append(get_color(country))

        year_min = int(request.form.get('selected_year_min'))
        year_max = int(request.form.get('selected_year_max'))
        per_capita_selector = request.form.get('selected_data')

        if per_capita_selector == "on":
            data_type = "emissions_per_capita"
        else:
            data_type = "emissions"

        if not invalid:
            data_dict = api_caller.get_multiple_data_range(input_country_list, data_type, year_min, year_max)
            labels = list(data_dict[list(data_dict.keys())[0]].keys())
            for i in range(len(input_country_list)):
                value_list = list(data_dict[list(data_dict.keys())[i]].values())
                for j in range(len(value_list)):
                    if value_list[j] is None:
                        value_list[j] = None
                values.append(value_list)
            is_empty = api_caller.get_year_list(country, data_type, year_min, year_max) == []

        received = True

    return render_template('index.html', generic_country_list=generic_country_list, generic_year_list=generic_year_list,
                           year_min=year_min, year_max=year_max, data_type=data_type, labels=labels, values=values,
                           received=received, is_empty=is_empty, invalid=invalid, input_country_list=input_country_list,
                           country_amount=country_amount, color_list=color_list)


# Api routing section

@app.route('/api', methods=["GET"])
def api():
    return "<h1>Emission Visualizer API</h1>" \
           "<p>The API returns the following data in json format:</p>" \
           "<ul>" \
           "<li>api/country_list returns a list of available countries</li>" \
           "<li>api/country_id_list returns a list of countries with their corresponding ISO3 codes</li>" \
           "<li>api/data returns data for a specific country using the following arguments" \
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
    else:
        return jsonify(api_caller.get_data(request_country, request_data_type, request_year))


if __name__ == '__main__':
    app.run()
