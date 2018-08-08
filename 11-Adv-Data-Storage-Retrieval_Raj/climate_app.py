from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_, desc, func
import pandas as pd
import numpy as np
import datetime 

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///jupyter_notebooks/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)
# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start_date<br/>'
        f'/api/v1.0/start_date/end_date<br/>'
    )

# http://localhost:5000/api/v1.0/precipitation
@app.route('/api/v1.0/precipitation')
def precipitation():
    max_date = (session
            .query(measurement, measurement.date)
            .order_by(measurement.date.desc())
            .first()[1])
    start_date = max_date - datetime.timedelta(365)
    prcp_ls = (session
            .query(measurement.date,measurement.prcp)
            .filter(measurement.date >= start_date)
            .order_by(measurement.date)
            .all())
    prcp_dict = {str(date): prcp for date, prcp in prcp_ls}
    return jsonify(prcp_dict)

# http://localhost:5000/api/v1.0/stations
@app.route('/api/v1.0/stations')
def stations():
    stations = (session
            .query(station.station,station.name)
            .all())
    stations_dict = {station: name for station, name in stations}
    return jsonify(stations_dict)

# http://localhost:5000/api/v1.0/tobs
@app.route('/api/v1.0/tobs')
def tobs(): 
    max_date = (session
            .query(measurement, measurement.date)
            .order_by(measurement.date.desc())
            .first()[1])
    start_date = max_date - datetime.timedelta(365)
    temp_data = (session
                .query(measurement.date, measurement.tobs)
                .filter(and_(measurement.date >= start_date
                            ,measurement.date <= max_date))
                .order_by(measurement.date)
                .all())
    temp_dict = {str(date): tobs for date, tobs in temp_data}
    return jsonify(temp_dict)

# http://localhost:5000/api/v1.0/<start>
@app.route('/api/v1.0/<start>')
def start_only(start):
    #canonicalized = start.replace(" ","")
    start_datetime = datetime.datetime.strptime(start,'%Y-%m-%d')
    temp_data = (session
                .query(measurement.date, measurement.tobs)
                .filter(measurement.date >= start_datetime)
                .all())
    temp_df = pd.DataFrame(temp_data, columns=['date','tobs'])
    average_temp = temp_df['tobs'].mean()
    max_temp = temp_df['tobs'].max()
    min_temp = temp_df['tobs'].min()
    temp_dict = {'Start Date':str(start_datetime),
                 'Average Temperature':str(average_temp),
                 'Highest Temperature':str(max_temp),
                 'Lowest Temperature':str(min_temp)}
    return jsonify(temp_dict)

# http://localhost:5000/api/v1.0/<start>/<end>
@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    start_datetime = datetime.datetime.strptime(start,'%Y-%m-%d')
    end_datetime = datetime.datetime.strptime(end,'%Y-%m-%d')
    temp_data = (session
                .query(measurement.date, measurement.tobs)
                .filter(and_(measurement.date >= start_datetime
                            ,measurement.date <= end_datetime))
                .all())
    temp_df = pd.DataFrame(temp_data, columns=['date','tobs'])
    average_temp = temp_df['tobs'].mean()
    max_temp = temp_df['tobs'].max()
    min_temp = temp_df['tobs'].min()
    temp_dict = {'Start Date':(start_datetime.strftime('%Y-%m-%d')),
                 'End Date':(end_datetime.strftime('%Y-%m-%d')),
                 'Average Temperature':'{:.2f}'.format(average_temp),
                 'Highest Temperature':f'{max_temp}',
                 'Lowest Temperature':f'{min_temp}'}
    return jsonify(temp_dict)
if __name__ == "__main__":
    app.run(debug=True)