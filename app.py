from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purchases.db'
db_purchase = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
db = SQLAlchemy(app)

class Purchases(db_purchase.Model):
    __tablename__ = "purchases"
    id=db_purchase.Column(db_purchase.Integer, primary_key=True)
    date=db_purchase.Column(db_purchase.String(10))
    store=db_purchase.Column(db_purchase.String(10))
    warranty_period=db_purchase.Column(db_purchase.Integer)

    def __init__(self, date, store, warranty_period):
        self.date=date
        self.store=store
        self.warranty_period=warranty_period

    def __repr__(self):
        return f"{self.date}, {self.store}, {self.warranty_period}"


class Location(db.Model):
    __tablename__ = "locations"
    id=db.Column(db.Integer, primary_key=True)
    location_name=db.Column(db.String(50))
    number_of_offices=db.Column(db.Integer)
    head_quater_contact=db.Column(db.Integer)

    def __init__(self, location_name, number_of_offices, head_quater_contact):
        self.location_name=location_name
        self.number_of_offices=number_of_offices
        self.head_quater_contact=head_quater_contact

    def __repr__ (self):
        return f"{self.location_name}, {self.number_of_offices}, {self.head_quater_contact}"    

@app.route('/')
def index():
    purchases = Purchases.query.all()
    return render_template('index.html', purchases=purchases)


@app.route('/add_purchase', methods=['GET', 'POST'])
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

@app.route('/main')
def main():
    # return 'Online inventory system'
    return render_template("main.html")

@app.route('/')
def index():
    locations = Location.query.all()
    return render_template ('index.html', locations = locations) 


@app.route('/location', methods=['GET', 'POST'])
def add_location_details():
    if request.method == 'GET':
        return render_template('location form.html')

    if request.method == 'POST':
        # Handle the form submission
        location_name = request.form['location_name']
        number_of_offices = request.form['number_of_offices']
        head_quater_contact = request.form['head_quater_contact']
        location = Location(
            location_name=location_name,
            number_of_offices=number_of_offices,
            head_quater_contact=head_quater_contact
        )
        db.session.add(location)
        db.session.commit()
        return redirect('/')


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)