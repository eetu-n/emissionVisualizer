from flask import Flask, render_template
from apiCaller import ApiCaller

app = Flask(__name__)

apiCaller = ApiCaller()


@app.route('/', methods=["POST", "GET"])
def index():
    country_list = apiCaller.get_country_list()

    return render_template('index.html', countryList=country_list)


if __name__ == '__main__':
    app.run()
