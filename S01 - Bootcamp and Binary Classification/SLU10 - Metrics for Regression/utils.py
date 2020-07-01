import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def create_dataset(random_state=10):
    x = np.array([i * np.pi/180 for i in range(280)])
    
    rs = np.random.RandomState(random_state)

    y = np.sin(x) + np.random.normal(0, 0.15, len(x))

    data = pd.DataFrame(np.column_stack([x,y]),columns=['x','y'])
    
    return data


def expand_dataset(data, n_expansions):
    data = data.copy()
    for i in range(2, n_expansions):
        colname = 'x_%d'%i
        data[colname] = data['x']**i
    return data


def linear_regression(data):
    y = data['y']
    x = data.drop('y', axis=1)
    
    linreg = LinearRegression(normalize=True)
    
    linreg.fit(x, y)
    
    return linreg