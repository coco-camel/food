# from curses import flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, session, url_for
app = Flask(__name__)

# db setting
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    location_url = db.Column(db.String(10000), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)

class Register (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/main/list", methods=['GET'])
def main():
    restaurant_list = Restaurant.query.all()
    return render_template('search.html', data = restaurant_list)


@app.route("/main/list/location")
def render_location_filter():

    searchQuery = request.args.get("location")

    if searchQuery:
        location = searchQuery
        filter_restaurant = Restaurant.query.filter_by(location = searchQuery).all()
        return render_template("search.html", data = filter_restaurant)
    else: # searchQuery 없을 때 main 화면 렌더링
        return redirect(url_for('main'))
    
    
    # 게시글 삭제
@app.route("/main/list/delete", methods=['DELETE'])
def delete_restaurant():

    delete_restaurant = Restaurant.query.filter_by(id=id).first()
    db.session.delete(delete_restaurant)
    db.session.commit
    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run(debug=True)