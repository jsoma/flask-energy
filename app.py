from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

# We want a Flask app!
app = Flask(__name__)

# Database connection details
database_path = os.path.join(os.path.dirname(__file__), 'energy.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# Define the tables
class Plants(db.Model):
    __tablename__ = 'powerplants'
    
    plant_code = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String)
    utility_name = db.Column(db.String)
    utility_id = db.Column(db.Integer)
    sector_name = db.Column(db.String)
    city = db.Column(db.String)
    county = db.Column(db.String)
    zip = db.Column(db.Integer)
    street_address = db.Column(db.String)
    primary_source = db.Column(db.String)
    total_mw = db.Column(db.Float)
    coal_mw = db.Column(db.Float)
    ng_mw = db.Column(db.Float)
    crude_mw = db.Column(db.Float)
    bio_mw = db.Column(db.Float)
    hydro_mw = db.Column(db.Float)
    nuclear_mw = db.Column(db.Float)
    solar_mw = db.Column(db.Float)
    wind_mw = db.Column(db.Float)
    geo_mw = db.Column(db.Float)
    other_mw = db.Column(db.Float)
    source_des = db.Column(db.String)
    tech_desc = db.Column(db.String)
    source = db.Column(db.String)
    period = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


# Define the routes
@app.route('/')
def list():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    plants = Plants.query.paginate(page=page, per_page=per_page)

    return render_template('list.html', plants=plants)

@app.route('/sources/<source>')
def by_source(source):
    page = request.args.get('page', 1, type=int)
    per_page = 20

    plants = Plants.query.filter_by(primary_source=source).paginate(page=page, per_page=per_page)

    # "Please explain how partials can make this cleaner"
    return render_template('by_source.html', plants=plants, source=source)


@app.route('/plants/<plant_code>')
def plant(plant_code):
    plant = Plants.query.get(plant_code)

    return render_template('show.html', plant=plant)


if __name__ == '__main__':
    app.run(debug=True)