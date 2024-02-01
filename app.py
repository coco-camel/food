import json
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
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


@app.route("/", methods=['GET', 'POST'])
def home():
    if not session.get('login'):
        return render_template('index.html')
    else:
        id = session.get('id')
        return render_template('index.html', id=id)


# 회원가입 페이지


@app.route("/join")
def join_screen():
    return render_template("join.html")

# 맛집 추천 페이지


@app.route("/recommend")
def recommend():
    return render_template("page.html")

# 회원가입 로직


@app.route("/user/regist", methods=['GET', 'POST'])
def user_create():
    user = request.form.get("user")
    password = request.form.get("password")

    user_exists = Register.query.filter_by(user=user).first()
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

    recommend_list = Restaurant(name=name, category=category, location=location,
                                description=description, location_url=location_url, image_url=image_url)
    db.session.add(recommend_list)
    db.session.commit()

    return render_template("search.html")

# 로그인 라우트


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # 사용자가 로그인 폼을 제출한 경우
        # 클라이언트로부터 전송된 사용자 id, password 가져오기
        id = request.form['id']
        password = request.form['password']
        # 데이터베이스에서 사용자 찾기
        user = Register.query.filter_by(user=id, password=password).first()
        if user:
            # 로그인 성공 & 세션에 사용자 ID 저장하기
            session['login'] = True
            session['id'] = user.id
            return redirect(url_for('home'))
        else:
            # 로그인 실패
            message = '로그인 실패. 사용자 아이디 또는 비밀번호가 잘못되었습니다.'
            return render_template('login.html', message=message)

    return render_template('login.html', message='로그인을 해주세요.')


@app.route('/logout')
def logout():
    session['login'] = False
    return redirect(url_for('home'))

# 전체출력
@app.route("/main/list", methods=['GET'])
def main():
    restaurant_list = Restaurant.query.all()
    return render_template('search.html', data = restaurant_list)


# 카테고리
@app.route("/main/list/category=<category>", methods=['GET'])
def main_cate(category):
    location = request.args.get("location")
    if category != None and not location:
        restaurant_list = Restaurant.query.filter_by(category=category).all()
    else:
        restaurant_list = Restaurant.query.filter_by(category=category, location=location).all()

    return render_template('search.html', data = restaurant_list, data1 = category)


    
    # 게시글 삭제/수정조작
@app.route("/main/list/delete", methods=['DELETE'])
def delete_post():

    id = request.args.get("delete_id")
    delete_restaurant = Restaurant.query.filter_by(id=id).first()
    db.session.delete(delete_restaurant)
    db.session.commit
    return redirect(url_for('main'))


if __name__ == "__main__":
    app.secret_key = "123123123"
    app.run(debug=True)
