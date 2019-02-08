from flask import Flask, render_template, request
from apiCaller import ApiCaller

app = Flask(__name__)

apiCaller = ApiCaller()


@app.route('/', methods=["POST", "GET"])
def index():
    country_list = apiCaller.get_country_list()
    generic_year_list = apiCaller.get_generic_year_list()
    year_min = 1960
    year_max = 2019
    country = None
    year = 0000
    data_type = None
    labels = generic_year_list
    values = []
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

        data_dict = apiCaller.get_data_range(country, data_type, year_min, year_max)
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        received = True

    return render_template('index.html', country_list=country_list, generic_year_list=generic_year_list,
                           country=country, year=year, data_type=data_type, received=received, labels=labels,
                           values=values)


if __name__ == '__main__':
    app.run()
