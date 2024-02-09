from flask import Flask,render_template,request,redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
db=SQLAlchemy(app)


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
    
# creating a decorator that creates all the tables in the sqlalchemy model before any request is done
@app.before_request
def create_table():
    db.create_all()


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

    # If the request method is not GET or POST, return an error response
    return 'Method Not Allowed', 405


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)