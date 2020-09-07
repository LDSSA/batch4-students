import pandas as pd
import numpy as np

from statsmodels.datasets import sunspots

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


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
    airlines = pd.read_csv('data/AirPassengers.csv')[:-1]
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

    plt.legend()
    return figure
    

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

def load_airline_data():
    airlines = pd.read_csv('data/AirPassengers.csv',
                           index_col='Month')

    airlines.columns = ['passengers_thousands']
    airlines = airlines['passengers_thousands']
    airlines.index = pd.to_datetime(airlines.index)

    return airlines.asfreq('MS', method='ffill')


def predict_next_period(model, airlines, n_periods, number_of_periods_ahead):

    X_train, y_train, X_last_period = prepare_for_prediction(airlines.iloc[0:n_periods],
                                                             number_of_periods_ahead)

    model.fit(X_train, y_train)

    next_period_index = [y_train.index.max() + pd.DateOffset(months=number_of_periods_ahead)]
    next_period_prediction_values = model.predict(X_last_period.values.reshape(1, -1))
    next_period_prediction = pd.Series(next_period_prediction_values, next_period_index)
    return next_period_prediction



def load_electricity_consumption_series_v2():
    ts = load_electricity_consumption_series()
    slr = LinearRegression()

    slr.fit(np.arange(ts.shape[0]).reshape(-1, 1), ts)

    slr_pred = slr.predict(np.arange(ts.shape[0]).reshape(-1, 1))
    slr_pred = pd.Series(slr_pred, index=ts.index)
    return (ts - slr_pred + 1000)
