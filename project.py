from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SECRET_KEY'] = 'da8e6f374f59357fd9ee2ae8569358d39d8ad5f8'
db = SQLAlchemy(app)
manager = LoginManager(app)


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'users{self.id}'

# class Profiles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     product_name = db.Column(db.String(50), nullable=True)
#     product_description = db.Column(db.String(50), nullable=True)
#     price = db.Column(db.Integer)
#     city = db.Column(db.String(100))
#
#
#     def __repr__(self):
#         return f'users{self.id}'


@app.route('/')
def menu():
    item = Users.query.order_by(Users.id).all() #MISSING
    return render_template('menu.html', data=item)


@app.route('/<int:id>')
def flex(id):
    item = Users.query.order_by(Users.id).all() #MISSING
    return f'{item.email}'


@app.route('/main')
@login_required
def main():
    return render_template('main.html')


@app.route('/register', methods=("POST", "GET"))
def register():
    if request.method == "POST":
        try:
            hash = generate_password_hash(request.form['password'])
            u = Users(email=request.form['email'], password=hash)
            db.session.add(u)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Error")
    return render_template('register.html')


@app.route('/login', methods=("POST", "GET"))
def login():
    email = request.form.get('email')
    psw = request.form.get('password')
    if email and psw:
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, psw):
            login_user(user)
            return redirect(url_for('main'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('menu'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.errorhandler(401)
def page_not_found(error):
    return render_template('401.html')


if __name__ == '__main__':
    app.run(debug=True)
