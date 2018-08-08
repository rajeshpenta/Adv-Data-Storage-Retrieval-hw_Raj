

```python
# Dependencies
import pandas as pd
import numpy as np
from datetime import date
# Import SQL Alchemy
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Text, Integer, String, Date, Float
# PyMySQL 
import pymysql
pymysql.install_as_MySQLdb()
```


```python
Base = declarative_base()

clean_measurements_path = '../Resources/clean_hawaii_measurements.csv'
clean_stations_path = '../Resources/clean_hawaii_stations.csv'
# Read clean csv files as pandas df and save data
clean_measurements_df = pd.read_csv(clean_measurements_path,dtype=object)
# covert the date column into python datetime object
clean_measurements_df['date'] = pd.to_datetime(clean_measurements_df['date'])
clean_stations_df = pd.read_csv(clean_stations_path,dtype=object)

measurement_data = clean_measurements_df.to_dict(orient='records')
station_data = clean_stations_df.to_dict(orient='records')
```


```python
# create an engine to a SQLite database
engine = create_engine('sqlite:///hawaii.sqlite')
# create connection
conn = engine.connect()
```


```python
# model measurement table & station table
class Measurement(Base):
    __tablename__='measurement'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Integer)
class Station(Base):
    __tablename__='station'
    id = Column(Integer, primary_key=True)
    station = Column(String(255))
    name = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
```


```python
# Use `create_all` to create the measurements and stations tables in the database
Base.metadata.create_all(engine)
```


```python
# use metadata to reflect tables
meta = MetaData(bind=engine)
meta.reflect()
```


```python
# create tables vaiables and remove pre-existing data
measurement_tbl = sqlalchemy.Table('Measurement', meta, autoload=True)
station_tbl = sqlalchemy.Table('Station', meta, autoload=True)
conn.execute(measurement_tbl.delete())
conn.execute(station_tbl.delete())
```




    <sqlalchemy.engine.result.ResultProxy at 0x115e6b4e0>




```python
# check station data before insert
station_data[0]
```




    {'elevation': '3.0',
     'latitude': '21.2716',
     'longitude': '-157.8168',
     'name': 'WAIKIKI 717.2, HI US',
     'station': 'USC00519397'}




```python
# check measurement data before insert
measurement_data[0]
```




    {'date': Timestamp('2010-01-01 00:00:00'),
     'prcp': '0.08',
     'station': 'USC00519397',
     'tobs': '65'}




```python
# insert the data into the tables
conn.execute(measurement_tbl.insert(), measurement_data)
conn.execute(station_tbl.insert(), station_data)
```




    <sqlalchemy.engine.result.ResultProxy at 0x115e6bc18>




```python
# test if the insert works for measurement
conn.execute("select * from Measurement limit 5").fetchall()
```




    [(1, 'USC00519397', '2010-01-01', 0.08, 65),
     (2, 'USC00519397', '2010-01-02', 0.0, 63),
     (3, 'USC00519397', '2010-01-03', 0.0, 74),
     (4, 'USC00519397', '2010-01-04', 0.0, 76),
     (5, 'USC00519397', '2010-01-06', 0.0, 73)]




```python
# test if the insert works for stations
conn.execute("select * from Station limit 5").fetchall()
```




    [(1, 'USC00519397', 'WAIKIKI 717.2, HI US', 21.2716, -157.8168, 3.0),
     (2, 'USC00513117', 'KANEOHE 838.1, HI US', 21.4234, -157.8015, 14.6),
     (3, 'USC00514830', 'KUALOA RANCH HEADQUARTERS 886.9, HI US', 21.5213, -157.8374, 7.0),
     (4, 'USC00517948', 'PEARL CITY, HI US', 21.3934, -157.9751, 11.9),
     (5, 'USC00518838', 'UPPER WAHIAWA 874.3, HI US', 21.4992, -158.0111, 306.6)]


