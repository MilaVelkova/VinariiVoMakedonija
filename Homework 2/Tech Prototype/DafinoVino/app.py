import json
import re
from flask import Flask
from flask import Flask, render_template, Flask, render_template, request, redirect, url_for
import pandas as pd
import openpyxl
from Service.WineryServiceImplementation import instantiate_wineries
from Model.Winery import Winery

app = Flask(__name__)
app.static_folder = 'static'

wineries_list = instantiate_wineries()


@app.route('/')
def main_page():  # put application's code here
    return render_template("mainpage.html")


@app.route('/wineries/<int:user_id>')
def detail_winery(user_id):
    selected_winery = ""
    for item in wineries_list:
        if item.id == user_id:
            selected_winery = item
    print(selected_winery.name)
    return render_template("detail_view.html", data=selected_winery)


@app.route('/wineries', methods=['GET'])
def wineries():
    page = 0
    print(request.args.get('page'))
    if (request.args.get('page') is not None and
            request.args.get('page') != "" and
            request.args.get('page') != " " and
            int(request.args.get('page')) - 10 >= 0):
        page = int(request.args.get('page'))
    if (request.args.get('page') is not None and
        int(request.args.get('page')) > len(wineries_list)):
        page = 0

    return render_template("wineries.html", page=page, data=wineries_list[page: page + 10])


if __name__ == '__main__':
    app.run()
