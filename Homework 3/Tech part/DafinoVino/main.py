import json

import flask_login
import pandas as pd
from flask import redirect
from flask import render_template, request, Blueprint, flash, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import db


class Winery:
    def __init__(self, id, name, description, image_link, rating, location):
        self.id = id
        self.name = name
        self.description = description
        self.image_link = image_link
        self.rating = rating
        self.location = location


def instantiate_wineries():
    file = pd.read_csv("static/csv/final_scraped_wineries.csv", encoding='latin1')
    parsed_json = file.to_json(orient='records')
    parsed_json = json.loads(parsed_json)
    # print(parsed_json)
    new_list = list()
    i = 0
    for item in parsed_json:
        new_list.append(Winery(i,
                               item['Winary Name'],
                               item['Winary Description'],
                               item['Winary Image Link'],
                               item['Winary Rating'],
                               item['Winary Location']))
        i += 1
    return new_list


def find_winery_by_id(list_to_search, id):
    list_found = [item for item in list_to_search if item.id == id]
    return list_found[0]


def winery_repository():
    return instantiate_wineries()


def find_winery_by_id_ser(list_to_search, id):
    return find_winery_by_id(list_to_search, id)


main = Blueprint('main', __name__)

wineries_list = winery_repository()


@main.route('/')
def main_page():
    return render_template("mainpage.html")


@main.route('/wineries/<int:user_id>')
def detail_winery(user_id):
    selected_winery = find_winery_by_id_ser(wineries_list, user_id)
    print(selected_winery.name)
    return render_template("detail_view.html", data=selected_winery)


@main.route('/wineries', methods=['GET'])
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


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, current_user=current_user)


@main.route('/saveChanges', methods=['POST'])
def saveChanges():
    new_name = request.form.get('name')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    user = flask_login.current_user
    if not user or not check_password_hash(user.password, old_password):
        flash('Something is incorrect, please try again.')
        return redirect(url_for('main.profile'))

    if new_password != "" and new_password != " ":
        flask_login.current_user.password = generate_password_hash(new_password)
    flask_login.current_user.name = new_name
    db.session.commit()
    return redirect(url_for('main.profile'))
