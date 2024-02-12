from flask import Flask, render_template, request, redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///OIS.db'
db=SQLAlchemy(app)

class Location(db.Model):
    __tablename__ = "locations"
    id=db.Column(db.Integer, primary_key=True)
    location_name=db.Column(db.String(50))
    number_of_offices=db.Column(db.Integer)
    head_quater_contact=db.Column(db.Integer)
    employees=db.relationship('Employee', backref='employees_location')
    
    def __init__(self, location_name, number_of_offices, head_quater_contact):
        self.location_name=location_name
        self.number_of_offices=number_of_offices
        self.head_quater_contact=head_quater_contact

    def __repr__ (self):
        return f"{self.location_name}, {self.number_of_offices}, {self.head_quater_contact}"   

class Employee(db.Model):
    __tablename__="employees"
    id=db.Column(db.Integer, primary_key=True)
    employee_name=db.Column(db.String(20))
    gender=db.Column(db.String(6))
    title=db.Column(db.String(10))
    phone_number=db.Column(db.Integer)
    department=db.Column(db.String(50))
    location_id=db.Column(db.Integer, db.ForeignKey('locations.id'))
    location=db.relationship('Location', backref='employees_location')
    
    def __init__(self, employee_name, gender, title, phone_number, department, location_id):
        self.employee_name=employee_name
        self.gender=gender
        self.title=title
        self.phone_number=phone_number
        self.department=department
        self.location_id=location_id

    def __repr__ (self):
        return f"{self.employee_name}, {self.gender}, {self.title}, {self.phone_number}, {self.department}, {self.location_id}"    
  
   
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
    

# creating a decorator that creates all the tables in the sqlalchemy model before any request is done
@app.before_request
def create_table():
    db.create_all()

    
@app.route('/')
def entry_point():
    return render_template("main.html")
    
@app.route('/location')
def index():
    locations = Location.query.all()
    return render_template ('locationList.html', locations = locations) 

@app.route('/add-location', methods=['GET', 'POST'])
def add_location_details():
    if request.method == 'GET':
        return render_template('locationForm.html')

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
        return redirect('/location')

    # If the request method is not GET or POST, return an error response
    return 'Method Not Allowed', 405

@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee_details():
    locations = Location.query.all()
    if request.method == 'GET':
        return render_template('add_employee.html', locations=locations)

    if request.method == 'POST':
        # Handle the form submission
        employee_name = request.form['employee_name']
        gender = request.form['gender']
        title = request.form['title']
        phone_number = request.form['phone_number']
        department = request.form['department']
        location_id = request.form['location_id']
        employee = Employee(
            employee_name=employee_name,
            gender=gender,
            title=title,
            phone_number=phone_number,        
            department=department,
            location_id=location_id,
        )
        db.session.add(employee)
        db.session.commit()
        return redirect('/employee')

    # If the request method is not GET or POST, return an error response
    return 'Method Not Allowed', 405

@app.route('/purchase')
def purchase():
    purchases = Purchases.query.all()
    return render_template('purchaseList.html', purchases=purchases)


@app.route('/add-purchase', methods=['GET', 'POST'])
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
        return redirect('/purchase')
    

@app.route('/edit_purchase<int:id>', methods=['GET' ,'POST' ])
def edit_purchase(id):
    purchase = Purchases.query.get(id)
    if request.method == 'GET':
        return render_template('edit_purchase.html' ,purchase=purchase)
    
    if  request.method == 'POST':
        purchase.date = request.form['date']
        purchase.store = request.form['store']
        purchase.warranty_period = request.form['warranty_period']
        db.session.commit()
        return redirect('/purchase')


@app.route('/delete_purchase<int:id>')
def delete_purchase(id):
    purchase = Purchases.query.get_or_404(id)
    db.session.delete(purchase)
    db.session.commit()
    return redirect('/purchase')    


@app.route('/edit_location<int:id>', methods=['GET' ,'POST' ])
def edit_location(id):
    location = Location.query.get(id)
    if request.method == 'GET':
        return render_template('edit_location.html' ,location=location)
    
    if  request.method == 'POST':
        location.location_name = request.form['location_name']
        location.number_of_offices = request.form['number_of_offices']
        location.head_quater_contact = request.form['head_quater_contact']
        db.session.commit()
        return redirect('/location')

@app.route('/edit_employee<int:id>', methods=['GET' ,'POST' ])
def edit_employee(id):
    locations = Location.query.all()
    employee = Employee.query.get(id)
    if request.method == 'GET':
        return render_template('edit_employee.html', employee=employee, locations=locations)
    
    if  request.method == 'POST':
        employee.employee_name = request.form['employee_name']
        employee.gender = request.form['gender']
        employee.title = request.form['title']
        employee.phone_number = request.form['phone_number']
        employee.department = request.form['department']
        employee.location_id = request.form['location_id']
        db.session.commit()
        return redirect('/employee')
    
@app.route('/delete_location<int:id>')
def delete_location(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    return redirect('/location')
    
@app.route('/delete_employee<int:id>')
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect('/employee')

@app.route('/equipment')
def equipment():
    return render_template('add_equipment.html')

@app.route('/employee')
def employee_index():
    employees = Employee.query.all()
    return render_template ('employeeList.html', employees = employees) 

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)