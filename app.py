from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purchases.db'
db = SQLAlchemy(app)

class Purchases(db.Model):
    __tablename__ = "purchases"
    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.String(10))
    store=db.Column(db.String(10))
    warranty_period=db.Column(db.Integer)

    def __init__(self, date, store, warranty_period):
        self.date=date
        self.store=store
        self.warranty_period=warranty_period

    def __repr__(self):
        return f"{self.date}, {self.store}, {self.warranty_period}"


# creating a decorator that creates all the tables in the SQLAlchemy model before any request is done
@app.before_request
def create_table():
    db.create_all()


@app.route('/')
def index():
    purchases = Purchases.query.all()
    return render_template('index.html', purchases=purchases)


@app.route('/purchase', methods=['GET', 'POST'])
def add_purchase_details():
    if request.method == 'GET':
        return render_template('purchase_form.html')

    if request.method == 'POST':
        date = request.form['date']
        store = request.form['store']
        warranty_period = request.form['warranty-period']
        purchase = Purchases(date=date, store=store, warranty_period=warranty_period)
        db.session.add(purchase)
        db.session.commit()
        return redirect('/')


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)