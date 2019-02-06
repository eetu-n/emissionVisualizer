from flask import Flask, render_template, request
from apiCaller import ApiCaller

app = Flask(__name__)

apiCaller = ApiCaller()


@app.route('/', methods=["POST", "GET"])
def index():
    country_list = apiCaller.get_country_list()
    year_list = apiCaller.temp_get_year_list()
    country = "blank"
    year = 0000
    data = "blank"
    received = False

    if request.method == "POST":
        country = request.form.get('selected_country')
        year = request.form.get('selected_year')
        data = request.form.get('selected_data')
        received = True

    return render_template('index.html', country_list=country_list, year_list=year_list, country=country, year=year,
                           data=data, received=received)


if __name__ == '__main__':
    app.run()
