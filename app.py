from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

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


@app.route("/", methods=['GET', 'POST'])
def home():
    if not session.get('login') :
        return render_template('index.html')
    else:
        id = session.get('id')
        return render_template('index.html', id=id)


# 세션의 수명을 0초로 설정하여 브라우저가 닫힐 때 세션을 만료
# 의도는 위의 설명대로지만...
# 아래 코드를 넣으면 로그인 후 메인화면으로 리다이렉트 -> 그 후 다시 로그인 페이지로 돌아가면?!
# 로그인이 풀려있습니다. 왤까요 ㅎ
# app.permanent_session_lifetime = timedelta(seconds=0)


# 로그인 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # 사용자가 로그인 폼을 제출한 경우
        # 클라이언트로부터 전송된 사용자 id, password 가져오기
        id = request.form['id']
        password = request.form['password']
        print(password)

        # 데이터베이스에서 사용자 찾기
        user = Register.query.filter_by(id=id, password=password).first()
        print(user)
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


if __name__ == "__main__":
    app.secret_key = "123123123"
    app.run(debug=True)
