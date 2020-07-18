import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
np.random.seed(1000)
import string

def get_house_prices_and_rooms():

    # getting the data 
    interesting_columns = ['house_price', 'number_of_rooms']
    houses_df = pd.read_csv('data/HousingData.csv')[interesting_columns]

    # getting data without outliers 
    number_of_rooms = houses_df['number_of_rooms']
    house_prices_normal = houses_df['house_price']

    # adding an outlier 
    house_prices_with_outliers = house_prices_normal.copy()
    house_prices_with_outliers.loc[3] = 500 
    
    return number_of_rooms, house_prices_normal, house_prices_with_outliers


def plot_house_prices_and_rooms():
    
    number_of_rooms, house_prices_normal, house_prices_with_outliers = get_house_prices_and_rooms()

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 4))

    pd.concat([number_of_rooms, house_prices_normal], axis=1).plot(kind='scatter', 
                                                                   y='number_of_rooms',
                                                                   x='house_price', 
                                                                   ax=axes[0], 
                                                                   title='Nr of rooms and house prices')


    pd.concat([number_of_rooms, house_prices_with_outliers], axis=1).plot(kind='scatter', 
                                                                          y='number_of_rooms', 
                                                                          x='house_price', 
                                                                          ax=axes[1],
                                                                          title='Nr of rooms and house prices (with an outlier)')

    plt.show()




def get_heights_data_metric():
    return pd.DataFrame({
        'ages': [2, 4, 4, 6, 8, 9, 12, 14],
        'heights': [120, 125, 127, 135, 140, 139, 170, 210]
    })


def get_heights_data_freedom_units():
    return pd.DataFrame({
        'ages': [2, 4, 4, 6, 8, 9, 12, 14],
        'heights': [3.93700787, 4.10104987, 4.16666667, 4.42913386, 4.59317585,
                    4.56036745, 5.57742782, 6.88976378]
    })


def _make_square(df, i):
    x_mean = df.ages.mean()
    y_mean = df.heights.mean()

    x = df.iloc[i].ages
    y = df.iloc[i].heights

    alpha = .1

    if x > x_mean and y > y_mean:
        plt.fill_betweenx(x1=x_mean, x2=x, y=(y_mean, y), alpha=alpha,
                          color='b')

    elif x < x_mean and y < y_mean:
        plt.fill_betweenx(x1=x, x2=x_mean, y=(y, y_mean), alpha=alpha,
                          color='b')

    elif x < x_mean and y > y_mean:
        plt.fill_betweenx(x1=x, x2=x_mean, y=(y_mean, y), alpha=alpha,
                          color='r')

    else:
        plt.fill_betweenx(x1=x_mean, x2=x, y=(y, y_mean), alpha=alpha,
                          color='r')


def quick_scatterplot(df, plot_center=False, plot_squares=None):
    df.plot(kind='scatter', x='ages', y='heights', figsize=(12, 6))

    if plot_center:
        plt.scatter(df.ages.mean(), df.heights.mean(), color='k', marker='+',
                    s=250, )

    if plot_squares:
        if plot_squares == 'all':
            for i in range(len(df)):
                _make_square(df, i)

        else:
            _make_square(df, plot_squares)

    plt.show()


def get_data_for_spearman():
    np.random.seed(100)
    x = np.linspace(-100, 100)
    a = pd.Series(x ** 3)[3::] / 100000
    a.index = a.index * 10
    a = a + a.index / 100
    return a.reset_index().rename(columns={'index': 'a', 0: 'b'})


import math

def generate_correlated_data(n_points, corr):
            
    xx = np.array([0, 1])
    yy = np.array([0, 1])
    
    means = [xx.mean(), yy.mean()]  
    stds = [xx.std() / 3, yy.std() / 3]
    
    covs = [[stds[0]**2          , stds[0]*stds[1]*corr], 
            [stds[0]*stds[1]*corr,           stds[1]**2]] 

    m = pd.DataFrame(np.random.multivariate_normal(means, covs, n_points))
    m.columns = ['a', 'b']
    return m 


def plot_scatter(df, color, figsize=None):
    if not figsize:
        figsize=(8, 8)
    f, ax = plt.subplots(figsize=figsize)
    
    label = 'Corr: % 0.2f' % (df[df.columns[0]].corr(df[df.columns[1]]))
    # ax = df.plot(kind='scatter', x=df.columns[0], y=df.columns[1], label=label, figsize=(8, 8), color=color)
    ax = df.plot(kind='scatter', x=df.columns[0], y=df.columns[1], label=label, figsize=(8, 8), color=color, ax=ax)
    # plt.ylim([0, 1.2])
    # plt.xlim([0, 1.2])
    return ax.get_figure()

def scatter_plot(df, ax, color, figsize=None):
    # this should not exist, but needed if for something 
    if not figsize:
        figsize = (8, 8)
    return df.plot(kind='scatter', 
                    x=df.columns[0], 
                    y=df.columns[1], 
                    label='Corr: % 0.2f' % (df[df.columns[0]].corr(df[df.columns[1]])), 
                    figsize=figsize, 
                    color=color, ax=ax)

def multiple_from_angle(x):
    return math.tan(math.radians(x))
    
def generate_example(corr, slope, n_points=500, color='b'):
    
    df = generate_correlated_data(n_points, corr)
    # plot_scatter(df, color=color)
    
    # removing trend 
    df['b'] = df['b'] - df['a']
    # plot_scatter(df, color=color)
    
    # adding trend back in 
    multiple = multiple_from_angle(slope)
    df['b'] = df['b'] + multiple * df['a']
    
    return df 

def plot_correlated_distrs():
    
    f, ax = plt.subplots(figsize=(10, 6))

    med_up = pd.DataFrame([np.linspace(0, 1, 500), np.linspace(0, 1, 500) * .4]).T
    slight_up = pd.DataFrame([np.linspace(0, 1, 500), np.linspace(0, 1, 500) * .2]).T
    tiny_up = pd.DataFrame([np.linspace(0, 1, 500), np.linspace(0, 1, 500) * 0.05]).T
    tiny_down = pd.DataFrame([np.linspace(0, 1, 500), np.linspace(0, 1, 500) * -0.05]).T
    slight_down = pd.DataFrame([np.linspace(0, 1, 500), np.linspace(0, 1, 500) * -.2]).T
    bit_down = pd.DataFrame([np.linspace(0, 1, 500), np.linspace(0, 1, 500) * -.4]).T


    scatter_plot(med_up, ax=ax, color='#003d66')
    scatter_plot(slight_up, ax=ax, color='#66c2ff')
    scatter_plot(tiny_up, ax=ax, color='#99d6ff')
    scatter_plot(tiny_down, ax=ax, color='#ffcccc')
    scatter_plot(slight_down, ax=ax, color='#ff9999')
    scatter_plot(bit_down, ax=ax, color='#800000')
    plt.axhline(0, ls='--', c='grey')

    plt.ylim([-.5,.5])
    plt.show()

def plot_correlation_bars():
    df1 = generate_correlated_data(n_points=400, corr=.85)
    df2 = generate_correlated_data(n_points=400, corr=.98)


    f, ax = plt.subplots(figsize=(8, 8))
    pd.Series(np.linspace(0, 1, 100) + 0.2, index=np.linspace(0, 1, 100) ).plot(ax=ax, color='blue', label='_nolegend_')
    pd.Series(np.linspace(0, 1, 100) - 0.2, index=np.linspace(0, 1, 100) ).plot(ax=ax, color='blue', label='_nolegend_')
    pd.Series(np.linspace(0, 1, 100) + 0.1, index=np.linspace(0, 1, 100) ).plot(ax=ax, color='orange', label='_nolegend_')
    pd.Series(np.linspace(0, 1, 100) - 0.1, index=np.linspace(0, 1, 100) ).plot(ax=ax, color='orange', label='_nolegend_')
    scatter_plot(df1, ax, 'blue')
    scatter_plot(df2, ax, 'orange')
    plt.legend()
    plt.show()

def plot_angled_correlations():
    # some datasets for the sake of lazyness 
    df1 = pd.read_csv('data/df_45.csv')
    df2 = pd.read_csv('data/df_25.csv')

    f, ax = plt.subplots(figsize=(8, 8))
    scatter_plot(df1, ax, 'blue')
    scatter_plot(df2, ax, 'orange')

    plt.show()

def plot_positive_and_negative():
    df1 = generate_example(corr=.95, slope=35)
    df2 = generate_example(corr=.95, slope=-25)

    f, ax = plt.subplots(figsize=(8, 8))
    scatter_plot(df1, ax, 'blue')
    scatter_plot(df2, ax, 'orange')
    plt.ylim([-1, 1])
    plt.show()


def dirty_little_secret():
    text = '''
    Ok, we tricked you, and it was unfair of us. 

    The reality is that this stock dataset was 100% RANDOM NUMBERS.

    The thing to remember is: if you use correlation without knowing the data, you will always find "something". 
    A lot of bad data science comes from over trusting the tools, without knowing the data. 

    If you have enough data and dig into it using correlations you will ALWAYS find something
    ... even if there is nothing to be found. 

    Correlation does not equal causality. 
    And sometimes, it just means you found signal where there was only noise.

    Now go on to the next SLU, and remember the day you modeled random numbers and found good stock picks :)  
    '''
    print(text)



def _make_name():
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return ''.join(np.random.choice(letters, 3))


def _make_random_index(n_rows):
    return pd.date_range(start='1/1/2018', periods=n_rows)


def _make_random_column_names(n_cols):
    return [_make_name() for i in range(n_cols)]


def _make_random_data(n_rows, n_cols, max_val=50):
    return np.random.random(size=(n_rows, n_cols)) * 15


def make_random_dataset(n_rows=100, n_cols=1000):
    df = pd.DataFrame(_make_random_data(n_rows, n_cols),
                      index=_make_random_index(n_rows),
                      columns=_make_random_column_names(n_cols))
    return df


def get_stocks_data_2():
    return make_random_dataset(n_rows=100, n_cols=1000)