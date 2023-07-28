# Import the dependencies.

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#create homepage route with all available routes /
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/start'>/api/v1.0/start</a><br/>"
        f"<a href='/api/v1.0/start/end'>/api/v1.0/start/end</a><br/>"
    )

#create precipitation route /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation data"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of precipitation
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

#create stations route /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    # Create a dictionary from the row data and append to a list of stations
    stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations.append(stations_dict)

    return jsonify(stations)

#create tobs route /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all tobs data"""
    # Query all tobs data
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').all()

    # Create a dictionary from the row data and append to a list of tobs
    tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs.append(tobs_dict)

    return jsonify(tobs)

#create start route /api/v1.0/start
@app.route("/api/v1.0/<start>")
def start(start):
    """Return a list of all tobs data"""
    # Query all tobs data
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()

    # Create a dictionary from the row data and append to a list of tobs
    start = []
    for min, avg, max in results:
        start_dict = {}
        start_dict["min"] = min
        start_dict["avg"] = avg
        start_dict["max"] = max
        start.append(start_dict)

    return jsonify(start)

#create start/end route /api/v1.0/start/end
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a list of all tobs data"""
    # Query all tobs data
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).all()

    # Create a dictionary from the row data and append to a list of tobs
    start_end = []
    for min, avg, max in results:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["avg"] = avg
        start_end_dict["max"] = max
        start_end.append(start_end_dict)

    return jsonify(start_end)

if __name__ == '__main__':
    app.run(debug=True)
