import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement=base.classes.measurement
station=base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation") 
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    scores=session.query(measurement.date, measurement.prcp).all()
    session.close()

    dates=[]
    for date, prcp in scores:
        dicti={}
        dicti['date']=date
        dicti['prcp']=prcp
        dates.append(dicti)

    return jsonify(dates)

@app.route ("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations= session.query(measurement.station).group_by(measurement.station).all()
    session.close()
    
    all_stations = list(np.ravel(stations))
    return jsonify(all_stations)

@app.route ("/api/v1.0/tobs")
def tobs():
    session= Session(engine)
    largest_station=session.query(measurement.tobs, measurement.date).filter(measurement.station=='USC00519281').\
    filter(measurement.date>='2016-08-23').all()
    session.close()

     temps=[]
    for date, tobs in scores:
        dicti={}
        dicti['date']=date
        dicti['tobs']=tobs
        tempss.append(dicti)

    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    # query for min, max, and avg temp
    summary_temp = session.query(Measurement.date,\
    func.min(Measurement.tobs).label("Minimum Temp"),\
    func.max(Measurement.tobs).label("Maximum Temp"),\
    func.avg(Measurement.tobs).label("Mean Temp")).\
    filter(Measurement.date>=start).\
    group_by(Measurement.date).all()

    session.close()

    data = []
    for date, min, max, avg in summary_temp:
        dict = {}
        dict["Date"] = date
        dict["Minimum Temp"] = min
        dict["Maximum Temp"] = max
        dict["Mean Temp"] = avg
        data.append(dict)

    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    session = Session(engine)

    # query for min, max, and avg temp
    summary_temp = session.query(Measurement.date,\
    func.min(Measurement.tobs).label("Minimum Temp"),\
    func.max(Measurement.tobs).label("Maximum Temp"),\
    func.avg(Measurement.tobs).label("Mean Temp")).\
    filter(and_(Measurement.date>=start,Measurement.date<=end)).\
    group_by(Measurement.date).all()

    session.close()

    data = []
    for date, min, max, avg in summary_temp:
        dict = {}
        dict["Date"] = date
        dict["Minimum Temp"] = min
        dict["Maximum Temp"] = max
        dict["Mean Temp"] = avg
        data.append(dict)
        
    return jsonify(data)

    
if __name__ == '__main__':
    app.run(debug=True)