from flask import Flask, render_template, request
from apiCaller import ApiCaller

app = Flask(__name__)

api_caller = ApiCaller()


@app.route('/', methods=["POST", "GET"])
def index():
    country_list = api_caller.get_country_list()
    generic_year_list = api_caller.get_generic_year_list()
    year_min = int(1960)
    year_max = int(2019)
    country = None
    data_type = None
    labels = generic_year_list
    values = []
    is_empty = False
    received = False

    if request.method == "POST":
        country = request.form.get('selected_country')
        year_min = int(request.form.get('selected_year_min'))
        year_max = int(request.form.get('selected_year_max'))
        per_capita_selector = request.form.get('selected_data')
        if per_capita_selector == "on":
            data_type = "emissions_per_capita"
        else:
            data_type = "emissions"

        data_dict = api_caller.get_data_range(country, data_type, year_min, year_max)
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        received = True
        is_empty = api_caller.get_year_list(country, data_type, year_min, year_max) == []

    return render_template('index.html', country_list=country_list, generic_year_list=generic_year_list,
                           country=country, year_min=year_min, year_max=year_max, data_type=data_type,
                           received=received, labels=labels, values=values, is_empty=is_empty)


if __name__ == '__main__':
    app.run()
