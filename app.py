# Name: Tommy Cao
# Date: 12/10/19
# Company: GEVH
# Description: Rental booking feedback

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/booking'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pqybbixwsumvty:1f5f6db8a5c68c429d7e680b047d5ed31940e022bb583d78f80f67d014e2c675@ec2-23-21-91-183.compute-1.amazonaws.com:5432/d7dgdg2brjg45c'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    house = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, house, rating, comments):
        self.customer = customer
        self.house = house
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        house = request.form['house']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, house, rating, comments)
        if customer == '' or house == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, house, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, house, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted booking feedback')


if __name__ == '__main__':
    app.run()