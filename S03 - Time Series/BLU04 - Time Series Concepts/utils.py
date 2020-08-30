import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def measure_error(measurement, corect_measure):
    error = measurement-corect_measure
    print('We measured %0.2f Km, which is wrong by %0.2f Km' % 
          (measurement, error))


def measure_the_earth(std, verbose=False):
    
    corect_measure=6371
    
    measurement = np.random.normal(corect_measure, corect_measure * std)
    
    if verbose: 
        measure_error(measurement, corect_measure=corect_measure)
        
    return measurement


def plot_number_of_tries(series):
    
    # oh... you are reading my plotting code? How embarrasing
    ax = series.plot(figsize=(16, 8))
    plt.axhline(6371+10, color='g', ls=':')
    plt.axhline(6371-10, color='g', ls=':')
    plt.ylim([6371-100, 6371+100])
    plt.title('Expanding window of the measures of the radius of the Earth (+/- 10 Km in green)')
    plt.xlabel('Number of measurements')
    plt.ylabel('Mean measurement')
    plt.show()

def load_shampoo_series():
    """
    Sales of shampoo over a three year period
    """
    data = pd.read_csv('data/sales-of-shampoo-over-a-three-ye.csv')
    # To remove the extra row
    data = data[:-1]


    def get_date(v):
        splits = v.split('-')
        year = "200{}".format(splits[0])
        month = "{}".format(splits[1])
        return pd.to_datetime("{}/{}".format(month, year))

    data['Month'] = data['Month'].apply(get_date)

    sales = data.set_index('Month')['Sales of shampoo over a three year period'].sort_index()
    sales.name = 'Sales'
    
    return sales


def load_sunactivity_series():
    data = sunspots.data.load_pandas().data

    data.YEAR = data.YEAR.astype(int)

    data.YEAR = pd.to_datetime(data.YEAR, format="%Y")

    data = data.set_index('YEAR')['SUNACTIVITY']
    
    return data


def show_shampoo_sales_and_trend(figsize=(10, 10)):
    data = load_shampoo_series()
    y = data.values
    X = np.arange(1, y.shape[0]+1).reshape(-1, 1)
    lr = LinearRegression()
    lr.fit(X, y)
    pred = pd.Series(lr.predict(X), index=data.index)

    f = plt.figure(figsize=figsize)
    data.plot(label="data")
    pred.plot(label="trend")
    plt.legend()
    
    return lr.coef_[0]


def load_airlines_series():
    airlines = pd.read_csv('data/international-airline-passengers.csv')[:-1]
    airlines.Month = pd.to_datetime(airlines.Month)
    airlines = airlines.set_index('Month')
    airlines.columns = ['thousands of passengers']
    airlines = airlines['thousands of passengers']
    return airlines


def plot_seasonality_for_airlines(normalize=False):
    airlines = load_airlines_series()
    
    figure = plt.figure(figsize=(10, 8))

    daterange = [year for year in np.arange(1949, 1960+1)]

    for year in daterange:
        s = airlines["{}".format(year)]
        if normalize:
            s = s / s.max()
        s.index = np.arange(s.shape[0])
        s.plot(label=year)

    plt.xlabel('Month')
    plt.ylabel('Nr flights')
    plt.legend()
    plt.show()
    # return figure
    

def load_electricity_consumption_series():
    data = pd.read_csv('data/monthly-av-residential-electrici.csv')
    data = data[:-1]
    data.Month = pd.to_datetime(data.Month)
    data.columns = ['month', 'consumption']
    data = data.set_index('month')
    return data


def load_houses_sold_series():
    d = pd.read_csv('data/New One Family Houses Sold: United States.csv')
    d.DATE = pd.to_datetime(d.DATE)
    d = d.set_index('DATE')
    d.columns = ['houses sold']
    d = d['houses sold']
    return d

def load_electricity_consumption_series_v2():
    ts = load_electricity_consumption_series()
    slr = LinearRegression()

    slr.fit(np.arange(ts.shape[0]).reshape(-1, 1), ts)

    slr_pred = slr.predict(np.arange(ts.shape[0]).reshape(-1, 1))
    slr_pred = pd.Series(slr_pred, index=ts.index)
    return (ts - slr_pred + 1000)

def get_stores_data():
    stores = pd.read_csv('data/stores.csv')
    stores = stores.sample(frac=1, random_state=9999)
    return stores

def get_store_data():
    stores = get_stores_data()
    store = stores.loc[stores.store_nbr==1].drop('store_nbr', axis=1)    
    #store.date = pd.to_datetime(store.date).dt.strftime('%Y/%m/%d')
    store = store.sample(frac=1, random_state=9999)
    return store