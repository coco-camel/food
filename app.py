import json
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

# db setting
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = os.urandom(24)
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

# 회원가입 페이지
@app.route("/join")
def join_screen():
    return render_template("join.html");

# 맛집 추천 페이지
@app.route("/recommend")
def recommend():
    return render_template("page.html")

# 회원가입 로직
@app.route("/user/regist", methods=['GET', 'POST'])
def user_create():
    user = request.form.get("user")
    password = request.form.get("password")

    user_exists = Register.query.filter_by(user = user).first()
    password_exists = Register.query.filter_by(password=password).first()

    if user_exists:
        flash("이미 존재하는 아이디입니다.")
        return redirect(url_for("join_screen"))
    elif password_exists:
        flash("고유한 비밀번호를 입력해주세요.")
        return redirect(url_for("join_screen"))
    else:
        user_account = Register(user=user, password=password)
        db.session.add(user_account)
        db.session.commit()
        return redirect(url_for("home"))

# 게시글 작성
@app.route("/main/list/write", methods=['GET', 'POST'])
def recommend_restaurant():
    name = request.form.get("name")
    category = request.form.get("category")
    location = request.form.get("location")
    description = request.form.get("description")
    location_url = request.form.get("location_url")
    image_url = request.form.get("image_url")
    
    print(name, category, location, description, location_url, image_url)

    recommend_list = Restaurant(name=name, category=category, location=location, description=description, location_url=location_url, image_url=image_url)
    db.session.add(recommend_list)
    db.session.commit()

    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)
