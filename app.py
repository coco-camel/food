from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request

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


# 로그인 라우트
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':

        # 클라이언트로부터 전송된 사용자 이름 가져오기
        id = request.form['id']

        # 데이터베이스에서 사용자 찾기
        user = Register.query.filter_by(id=id).first()

    if user:
        # 로그인 성공 & 세션에 사용자 ID 저장하기
        db.session.add( Register(id=request.form['id'], password=request.form['password']) )
        # db.session.commit()

        return "로그인 성공!"
    
    else:
        # 로그인 실패
        return "로그인 실패. 사용자 아이디 또는 비밀번호가 잘못되었습니다."




if __name__ == "__main__":
    app.run(debug=True)
