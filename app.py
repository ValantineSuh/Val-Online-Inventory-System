
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purchases.db'
db_purchase = SQLAlchemy(app)

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

@app.route('/')
def index():
    purchases = Purchases.query.all()
    return render_template('index.html', purchases=purchases)

@app.route('/')
def entry_point():
    return render_template("main.html")

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
