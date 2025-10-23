from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///green_zones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class GreenZone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

# Create database
with app.app_context():
    db.create_all()

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Map Page
@app.route('/map')
def map():
    return render_template('map.html')

# Services Page
@app.route('/services')
def services():
    return render_template('services.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Form Page to Add New Green Zone
@app.route('/add-zone')
def add_zone():
    return render_template('add_zone.html')

# Handle Form Submission (Add New Zone)
@app.route('/submit-zone', methods=['POST'])
def submit_zone():
    name = request.form['name']
    lat = float(request.form['lat'])
    lon = float(request.form['lon'])

    new_zone = GreenZone(name=name, lat=lat, lon=lon)
    db.session.add(new_zone)
    db.session.commit()

    return redirect(url_for('map'))

# API to Fetch Green Zones (For Map)
@app.route('/green-zones')
def green_zones():
    zones = GreenZone.query.all()
    return jsonify([{"name": zone.name, "lat": zone.lat, "lon": zone.lon} for zone in zones])

if __name__ == '__main__':
    app.run(debug=True, port=8080)
