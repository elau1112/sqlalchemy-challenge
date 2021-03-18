import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

sqlPath = "sqlite:///sqlalchemy-challenge/Resources/hawaii.sqlite"
engine = create_engine(sqlPath)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def index():
    """List all available api routes."""
    return(
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
   )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    lastd = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    M12 = dt.date((int)(lastd[0][:4]), (int)(lastd[0][5:7]), (int)(lastd[0][8:10])) - dt.timedelta(days = 365)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= M12).\
        order_by(Measurement.date).all()
    session.close()
    #all_prcp = list(np.ravel(results))
    all_prcp = []
    for date, prcp in results:
        #date as the key and prcp as the value
        Precipitation_dict = {date : prcp}
        #Precipitation_dict = {}
        #Precipitation_dict["Date"] = date
        #Precipitation_dict["PRCP"] = prcp
        all_prcp.append(Precipitation_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    all_station = []
    for station in results:
        Stations_dict = {}
        Stations_dict["Station"] = station
        all_station.append(Stations_dict)
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    lastd = session.query(Measurement.date).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date.desc()).first()
    M12 = dt.date((int)(lastd[0][:4]), (int)(lastd[0][5:7]), (int)(lastd[0][8:10])) - dt.timedelta(days = 365)

    results = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= M12).\
        order_by(Measurement.date).all()
    session.close()
    all_temp = []
    for date, tobs, station in results:
        Temp_dict = {}
        Temp_dict["Date"] = date
        Temp_dict["TOBS"] = tobs
        Temp_dict["Station"] = station
        all_temp.append(Temp_dict)
    return jsonify(all_temp)

@app.route("/api/v1.0/<start>")
def startd(start):
    session = Session(engine)
    
    startd = dt.datetime.strptime(start, '%Y-%m-%d')

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=startd).all()

    some_temp=[]
    for tmin, tavg, tmax in results:
        sTemp={}
        sTemp["TMIN"] = tmin
        sTemp["TAVG"] = tavg
        sTemp["TMAX"] = tmax
        some_temp.append(sTemp)
    return jsonify(some_temp)


@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    session = Session(engine)
    
    startd = dt.datetime.strptime(start, '%Y-%m-%d')
    lastdd = dt.datetime.strptime(end, '%Y-%m-%d')

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=startd).\
        filter(Measurement.date <=lastdd).all()

    some_temp2=[]
    for tmin, tavg, tmax in results:
        sTemp2={}
        sTemp2["TMIN"] = tmin
        sTemp2["TAVG"] = tavg
        sTemp2["TMAX"] = tmax
        some_temp2.append(sTemp2)
    return jsonify(some_temp2)

if __name__ == '__main__':
    app.run(debug=True)