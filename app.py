from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id_


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    name = request.form['name']
    if User.query.filter_by(name = name).all():
        return "Вже бачилися, " + name

    create_name = User(name=name)

    try:
        db.session.add(create_name)
        db.session.commit()
        return "Привіт: " + name
    except:
        return "Помилка при записі ім'я в базу данних"


@app.route('/users')
def all_users():
    names = User.query.order_by(User.date.desc()).all()
    return render_template('all_users.html', names=names)


@app.route('/users/<int:id>')
def post_detail(id):
    name = User.query.get(id)
    return render_template('name_detail.html', name=name)


@app.route('/users/<int:id>/delete')
def name_delete(id):
    name = User.query.get_or_404(id)

    try:
        db.session.delete(name)
        db.session.commit()
        return redirect('/users')
    except:
        return 'При видалені виникла помилка'


@app.route('/users/<int:id>/update', methods=['GET', 'POST'])
def name_update(id):
    name = User.query.get(id)
    if request.method == 'POST':
        name.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/users')
        except:
            return 'При оновлені виникла помилка'
    else:
        return render_template('name_update.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
