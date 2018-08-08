

```python
# dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc, and_

import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import datetime
from datetime import date
import seaborn as sns
```


```python
engine = create_engine("sqlite:///hawaii.sqlite", echo=False)
```


```python
# reflect database into ORM classes & check classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
```




    ['measurement', 'station']




```python
# create references to the tables
measurement = Base.classes.measurement
station = Base.classes.station
```


```python
session = Session(engine)
```

### Precipitation Analysis
Design a query to retrieve the last 12 months of precipitation data.


```python
# retrieve latest date in the data
max_date = (session
            .query(measurement, measurement.date)
            .order_by(measurement.date.desc())
            .first()[1])
print(f'The latest date on record is {max_date}')
```

    The latest date on record is 2017-08-23



```python
# find the date 12 months prior to the latest date
start_date = max_date - datetime.timedelta(365)
print(f'The start date is {start_date}')
```

    The start date is 2016-08-23



```python
# Extract data & load into a pandas df
prcp_ls = (session
            .query(measurement.date,measurement.prcp)
            .filter(measurement.date > start_date)
            .order_by(measurement.date)
            .all())
prcp_df = pd.DataFrame(prcp_ls, columns=['Date','Precipitation'])
prcp_df = prcp_df.set_index('Date')
prcp_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Precipitation</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2016-08-24</th>
      <td>0.08</td>
    </tr>
    <tr>
      <th>2016-08-24</th>
      <td>2.15</td>
    </tr>
    <tr>
      <th>2016-08-24</th>
      <td>2.28</td>
    </tr>
    <tr>
      <th>2016-08-24</th>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2016-08-24</th>
      <td>1.22</td>
    </tr>
  </tbody>
</table>
</div>




```python
# plot the prcp data into chart
prcp_df.plot()
plt.title("Precipitation Last 12 Months")
plt.xlabel("Date")
plt.xticks(rotation='vertical')
plt.ylabel("Prcp")
sns.set
plt.show()
```


![png](output_9_0.png)



```python
# prcp statistic summary
prcp_df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Precipitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2223.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.159951</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.441220</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.010000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.110000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>6.700000</td>
    </tr>
  </tbody>
</table>
</div>



### Station Analysis
1. Design a query to find the most active stations
2. Design a query to retrieve the last 12 months of temperature observation data


```python
# find number of stations
num_stations = (session
               .query(station.station)
               .count())
print(f'The number of stations is {num_stations}')
```

    The number of stations is 9



```python
# find the most active station 
active_station = (session
                 .query(measurement.station, func.count(measurement.date))
                 .group_by(measurement.station)
                 .order_by(desc(func.count(measurement.date)))
                 .all())
most_active_station = active_station[0][0]
num_obser = active_station[0][1]
print(f'The most active station is {most_active_station}')
print(f'The number of observation for {most_active_station} is {num_obser}')
```

    The most active station is USC00519281
    The number of observation for USC00519281 is 2772



```python
# list the stations and observation counts in descending order
active_st_df = pd.DataFrame(active_station, columns=['Station ID','Number of Observation'])
active_st_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Station ID</th>
      <th>Number of Observation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519281</td>
      <td>2772</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00519397</td>
      <td>2724</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00513117</td>
      <td>2709</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00519523</td>
      <td>2669</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00516128</td>
      <td>2612</td>
    </tr>
  </tbody>
</table>
</div>




```python
# extract temp observation data & load into a pandas df
temp_obser = (session
             .query(measurement.date, measurement.tobs)
             .filter(and_(measurement.date > start_date
                          ,measurement.station == most_active_station))
             .all())
temp_obs_df = pd.DataFrame(temp_obser, columns=['Date','Temp'])
temp_obs_df = temp_obs_df.set_index('Date')
temp_obs_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Temp</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2016-08-24</th>
      <td>77</td>
    </tr>
    <tr>
      <th>2016-08-25</th>
      <td>80</td>
    </tr>
    <tr>
      <th>2016-08-26</th>
      <td>80</td>
    </tr>
    <tr>
      <th>2016-08-27</th>
      <td>75</td>
    </tr>
    <tr>
      <th>2016-08-28</th>
      <td>73</td>
    </tr>
  </tbody>
</table>
</div>




```python
# plot the temp distribution into a histogram
temp_obs_df.plot.hist(title = f'Frequency of Temp at {most_active_station} for last 12 months'
                      ,bins = 12)
sns.set
plt.show()
```


![png](output_16_0.png)


### Temperature Analysis
1. Write a function called `calc_temps` that will accept a start date and end date in the format `%Y-%m-%d` and return the minimum, average, and maximum temperatures for that range of dates.
2. Use the `calc_temps` function to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e. use "2017-01-01" if your trip start date was "2018-01-01")
3. Plot the min, avg, and max temperature from your previous query as a bar chart.


```python
def calc_temps(start_date,end_date):
    start_datetime = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_datetime = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    # get dates for prior year
    py_start_date = start_datetime - datetime.timedelta(365)
    py_end_date = end_datetime - datetime.timedelta(365)
    # query all temperature data between prior year dates
    temp_data = (session
                .query(measurement.date, measurement.tobs)
                .filter(and_(measurement.date >= py_start_date
                            ,measurement.date <= py_end_date))
                .all())
    # load extracted data into dataframe
    temp_df = pd.DataFrame(temp_data, columns=['date','tobs'])
    # find avg, max, and min
    average_temp = temp_df['tobs'].mean()
    max_temp = temp_df['tobs'].max()
    min_temp = temp_df['tobs'].min()
    return average_temp, max_temp, min_temp
```


```python
trip_start_date = input('When do you want to start your trip (YYYY-MM-DD)?')
```

    When do you want to start your trip (YYYY-MM-DD)?2018-02-14



```python
trip_end_date = input('When do you want to start your trip (YYYY-MM-DD)?')
```

    When do you want to start your trip (YYYY-MM-DD)?2018-04-01



```python
selection = calc_temps(trip_start_date,trip_end_date)
average_temp = selection[0]
max_temp = selection[1]
min_temp = selection[2]
print(f'The average temperature is {average_temp}')
print(f'The maximum temperature is {max_temp}')
print(f'The minimum temperature is {min_temp}')
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)
yerr = max_temp - min_temp
x_axis=1
```

    The average temperature is 71.8540925266904
    The maximum temperature is 82
    The minimum temperature is 61



```python
fig, ax = plt.subplots()
plot_bar = ax.bar(x_axis,average_temp,yerr=yerr,color='orange',align='center',alpha=0.5)
ax.set(xticks=range(x_axis)
       ,title=f"Trip Temp between {trip_start_date} to {trip_end_date}"
       ,ylabel="Temp (F)")
ax.margins(.2,.2)
sns.set
plt.show()
```


![png](output_22_0.png)

