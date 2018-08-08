
### Step 1 - Data Engineering


```python
# import modules 
import pandas as pd
import numpy as np

measurement = '../Resources/hawaii_measurements.csv'
stations = '../Resources/hawaii_stations.csv'

measurement_data = pd.read_csv(measurement)
stations_data = pd.read_csv(stations)
```


```python
measurement_data.count()
```




    station    19550
    date       19550
    prcp       18103
    tobs       19550
    dtype: int64




```python
stations_data.count()
```




    station      9
    name         9
    latitude     9
    longitude    9
    elevation    9
    dtype: int64




```python
# Fill NaN value with 0
measurement_data['prcp'] = measurement_data['prcp'].fillna(0)
measurement_data.count()
```




    station    19550
    date       19550
    prcp       19550
    tobs       19550
    dtype: int64




```python
# Export clean data to Resources folder
measurement_data.to_csv('../Resources/clean_hawaii_measurements.csv')
stations_data.to_csv('../Resources/clean_hawaii_stations.csv')
```
