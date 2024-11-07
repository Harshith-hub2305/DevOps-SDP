from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flight model
class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    flight = db.relationship('Flight', backref=db.backref('bookings', lazy=True))

# Create tables in the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    flights = Flight.query.all()  # Get all available flights
    return render_template('index.html', flights=flights)

@app.route('/book/<int:flight_id>', methods=['GET', 'POST'])
def book_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)  # Get selected flight
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Create a booking
        booking = Booking(name=name, email=email, flight_id=flight.id)
        db.session.add(booking)
        db.session.commit()
        
        return redirect(url_for('confirm_booking', booking_id=booking.id))
    
    return render_template('book_flight.html', flight=flight)

@app.route('/confirm/<int:booking_id>')
def confirm_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('confirm_booking.html', booking=booking)

# Admin CRUD Operations

# 1. Create Flight
@app.route('/admin/flight/create', methods=['GET', 'POST'])
def create_flight():
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        origin = request.form['origin']
        destination = request.form['destination']
        date = request.form['date']
        price = request.form['price']
        
        # Create a new flight
        flight = Flight(flight_number=flight_number, origin=origin, destination=destination, date=date, price=price)
        db.session.add(flight)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('create_flight.html')

# 2. Update Flight
@app.route('/admin/flight/edit/<int:flight_id>', methods=['GET', 'POST'])
def edit_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    
    if request.method == 'POST':
        flight.flight_number = request.form['flight_number']
        flight.origin = request.form['origin']
        flight.destination = request.form['destination']
        flight.date = request.form['date']
        flight.price = request.form['price']
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_flight.html', flight=flight)

# 3. Delete Flight
@app.route('/admin/flight/delete/<int:flight_id>', methods=['POST'])
def delete_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    db.session.delete(flight)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
