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
    employees_rel=db.relationship('Employee', backref='employees_location')
    equipment_rel=db.relationship('Equipment', backref='equipment_loation')
    
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
    type=db.Column(db.String(10))
    phone_number=db.Column(db.Integer)
    department=db.Column(db.String(50))
    location=db.Column(db.Integer, db.ForeignKey('locations.id'))
    location_rel=db.relationship('Location', backref='employees_location')
    equipment_rel=db.relationship('Equipment', backref='equipment_employee')
    
    def __init__(self, employee_name, gender, title, type, phone_number, department, location):
        self.employee_name=employee_name
        self.gender=gender
        self.title=title
        self.type=type
        self.phone_number=phone_number
        self.department=department
        self.location=location

    def __repr__ (self):
        return f"{self.employee_name}, {self.gender}, {self.title}, {self.type}, {self.phone_number}, {self.department}, {self.location}"    
  
   
class Purchase(db.Model):
    __tablename__ = "purchases"
    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.String(10))
    store=db.Column(db.String(10))
    warranty_period=db.Column(db.Integer)
    equipment_rel=db.relationship('Equipment', backref='equipment_purchase')

    def __init__(self, date, store, warranty_period):
        self.date=date
        self.store=store
        self.warranty_period=warranty_period

    def __repr__(self):
        return f"{self.date}, {self.store}, {self.warranty_period}"
    
class Equipment(db.Model):
    __tablename__="equipment"
    barcode_number=db.Column(db.Integer, primary_key=True)
    type=db.Column(db.String(20))
    serial_number=db.Column(db.Integer)
    model_number=db.Column(db.Integer)
    purchase_date=db.Column(db.Integer, db.ForeignKey('purchases.id'))
    employee=db.Column(db.Integer, db.ForeignKey('employees.id'))
    location=db.Column(db.Integer, db.ForeignKey('locations.id'))
    purchase_rel=db.relationship('Purchase', backref='equipment_purchase')
    employee_rel=db.relationship('Employee', backref='equipment_employee')
    location_rel=db.relationship('Location', backref='equipment_location')
    
    def __init__(self, type, serial_number, model_number, purchase_date, employee, location):
        self.type=type
        self.serial_number=serial_number
        self.model_number=model_number
        self.purchase_date=purchase_date
        self.employee=employee
        self.location=location

    def __repr__ (self):
        return f"{self.type}, {self.serial_number}, {self.model_number}, {self.purchase_date}, {self.employee}, {self.location}"    
  
# creating a decorator that creates all the tables in the sqlalchemy model before any request is done
@app.before_request
def create_table():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/entry_point')
def entry_point():
    employees = Employee.query.all()
    employee_count = len(employees)
    purchases = Purchase.query.all()
    purchase_count = len(purchases)
    locations = Location.query.all()
    location_count = len(locations)
    equipment = Equipment.query.all()
    equipment_count = len(equipment)

    return render_template('main.html', 
    employees = employees, employee_count=employee_count,
    purchases = purchases, purchase_count=purchase_count,
    locations = locations, location_count=location_count,
    equipment = equipment, equipment_count=equipment_count
    )


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/location')
def location():
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
        type = request.form['type']
        phone_number = request.form['phone_number']
        department = request.form['department']
        location = request.form['location']
        employee = Employee(
            employee_name=employee_name,
            gender=gender,
            title=title,
            type=type,
            phone_number=phone_number,        
            department=department,
            location=location,
        )
        db.session.add(employee)
        db.session.commit()
        return redirect('/employee')

    # If the request method is not GET or POST, return an error response
    return 'Method Not Allowed', 405

@app.route('/add-equipment', methods=['GET', 'POST'])
def add_equipment_details():
    locations = Location.query.all()
    employees = Employee.query.all()
    purchases = Purchase.query.all()
    if request.method == 'GET':
        return render_template('add_equipment.html', locations=locations, employees=employees, purchases=purchases)

    if request.method == 'POST':
        # Handle the form submission
        type = request.form['type']
        serial_number = request.form['serial_number']
        model_number = request.form['model_number']
        purchase_date = request.form['purchase_date']
        employee = request.form['employee']
        location = request.form['location']
        equipment = Equipment(
            type=type,
            serial_number=serial_number,
            model_number=model_number,
            purchase_date=purchase_date,        
            employee=employee,
            location=location,
        )
        db.session.add(equipment)
        db.session.commit()
        return redirect('/equipment')

    # If the request method is not GET or POST, return an error response
    return 'Method Not Allowed', 405

@app.route('/purchase')
def purchase():
    purchases = Purchase.query.all()
    return render_template('purchaseList.html', purchases=purchases)


@app.route('/add-purchase', methods=['GET', 'POST'])
def add_purchase_details():
    if request.method == 'GET':
        return render_template('purchase_form.html')

    if request.method == 'POST':
        date = request.form['date']
        store = request.form['store']
        warranty_period = request.form['warranty-period']
        purchase = Purchase(date=date, store=store, warranty_period=warranty_period)
        db.session.add(purchase)
        db.session.commit()
        return redirect('/purchase')
    

@app.route('/edit_purchase<int:id>', methods=['GET' ,'POST' ])
def edit_purchase(id):
    purchase = Purchase.query.get(id)
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
    purchase = Purchase.query.get_or_404(id)
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
        employee.type = request.form['type']
        employee.phone_number = request.form['phone_number']
        employee.department = request.form['department']
        employee.location = request.form['location']
        db.session.commit()
        return redirect('/employee')

@app.route('/edit_equipment<int:barcode_number>', methods=['GET' ,'POST' ])
def edit_equipment(barcode_number):
    locations = Location.query.all()
    employees = Employee.query.all()
    purchases = Purchase.query.all()
    equipment = Equipment.query.get(barcode_number)
    if request.method == 'GET':
        return render_template('edit_equipment.html', equipment=equipment, locations=locations, purchases=purchases, employees=employees)
    
    if  request.method == 'POST':
        equipment.type = request.form['type']
        equipment.serial_number = request.form['serial_number']
        equipment.model_number = request.form['model_number']
        equipment.purchase_date = request.form['purchase_date']
        equipment.employee = request.form['employee']
        equipment.location = request.form['location']
        db.session.commit()
        return redirect('/equipment')

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

@app.route('/delete_equipment<int:barcode_number>')
def delete_equipment(barcode_number):
    equipment = Equipment.query.get_or_404(barcode_number)
    db.session.delete(equipment)
    db.session.commit()
    return redirect('/equipment')

@app.route('/equipment')
def equipment_index():
    equipment = Equipment.query.all()
    return render_template('equipmentList.html', equipment = equipment)

@app.route('/employee')
def employee_index():
    employees = Employee.query.all()
    return render_template ('employeeList.html', employees = employees) 

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
