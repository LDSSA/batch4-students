
import numpy as np
import pandas as pd

from random import randint
import matplotlib.pyplot as plt

from mlxtend.plotting import plot_decision_regions

from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression


def tv(a, b, c, x):
    return (a * (x ** 2)) + (b * x) + c


def fit_lin_reg(df):
    fig, ax = plt.subplots()
    df.plot(kind='scatter', x='age', y='minutes_per_day', ax=ax, alpha=.5);
    fit_line(df['age'], df['minutes_per_day'])
    plt.legend()
    plt.show()


def fit_line(x, y):
    lr = LinearRegression()
    lr.fit(x.values.reshape(-1, 1), y)

    y_plot = lr.predict(x.values.reshape(-1, 1))

    plt.plot(x, y_plot, ls=':', c='r',
             label='prediction')


def fit_knn(x, y):
    model = KNeighborsRegressor(1)

    model.fit(x.values.reshape(-1, 1), y)

    y_plot = model.predict(x.values.reshape(-1, 1))
    plt.plot(x, y_plot, ls=':', c='r', label='prediction')


def fit_high_variance_algo(df):
    fig, ax = plt.subplots()
    df.plot(kind='scatter', x='age', y='minutes_per_day', ax=ax, alpha=.5);
    fit_knn(df['age'], df['minutes_per_day'])
    plt.legend()
    plt.show()


def generate_time_on_tv():
    space = [int(i) for i in np.linspace(10, 80, 100)]
    df = pd.DataFrame({'age': pd.Series(space)}).set_index('age', drop=False)

    a = 0.1467
    b = -14.67
    c = 382
    df['minutes_per_day_raw'] = df.index.map(lambda x: tv(a, b, c, x))

    np.random.seed(100)
    df['noise'] = [randint(0, 30) for i in range(len(df))]

    df['minutes_per_day'] = df['minutes_per_day_raw'] + df['noise']

    df.loc[35, 'minutes_per_day'] = 130
    df.loc[70, 'minutes_per_day'] = 50

    return df


def draw_points(X, y):
    plt.figure(figsize=(10, 10))
    plot_decision_regions(X.values, y.values, clf=lr, legend=2)
    plt.title("Logistic Regression (LR)")
    plt.show()


def plot_super_conservative(X, y):
    lr = LogisticRegression()
    lr.fit(X, y)
    preds = lr.predict(X)
    plt.figure(figsize=(10, 10))
    plot_decision_regions(X.values, y.values, clf=lr, legend=2)
    plt.title("Logistic Regression (LR)")
    plt.xlabel('Color')
    plt.ylabel('IBU')
    plt.show()
    return preds


def plot_super_flexible(X, y):
    knn_k1 = KNeighborsClassifier(n_neighbors=1)
    knn_k1.fit(X, y)
    preds = knn_k1.predict(X)
    plt.figure(figsize=(10, 10))
    plot_decision_regions(X.values, y.values, clf=knn_k1, legend=2)
    plt.title("KNN (k=1)")
    plt.xlabel('Color')
    plt.ylabel('IBU')
    plt.show()
    return preds


def plot_just_right(X, y):
    knn_k9 = KNeighborsClassifier(n_neighbors=9)
    knn_k9.fit(X, y)
    preds = knn_k9.predict(X)
    plt.figure(figsize=(10, 10))
    plot_decision_regions(X.values, y.values, clf=knn_k9, legend=2)
    plt.title("KNN (k=9)")
    plt.xlabel('Color')
    plt.ylabel('IBU')
    plt.show()
    return preds


def generate_test_data(m, n):
    np.random.seed(100)
    values = np.random.randint(0, m, size=(m, n))
    df = pd.DataFrame(values)
    X = df.copy()
    y = X.pop(0)
    return X, y


def get_data():
    columns = ['Sample code number', 'Clump Thickness',
               'Uniformity of Cell Size', 'Uniformity of Cell Shape',
               'Marginal Adhesion', 'Single Epithelial Cell Size',
               'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli',
               'Mitoses', 'Class']
    data = pd.read_csv('data/breast-cancer-wisconsin.csv', names=columns,
                       index_col=0)
    data["Bare Nuclei"] = data["Bare Nuclei"].replace(['?'], np.nan)
    data = data.dropna()
    data["Bare Nuclei"] = data["Bare Nuclei"].map(int)
    data.Class = data.Class.map(lambda x: 1 if x == 4 else 0)
    test_index = data.sample(frac=.2, random_state=1000).index
    train_index = [i for i in data.index if i not in test_index]
    target = 'Class'

    train_data = data.loc[train_index]

    X_test = data.loc[test_index, [c for c in data.columns if c != target]]
    y_test = data.loc[test_index, target]

    return train_data, X_test, y_test


def create_dataset(random_state=10):
    x = np.array([i * np.pi/180 for i in range(280)])

    rs = np.random.RandomState(random_state)
    y = np.sin(x) + np.random.normal(0, 0.15, len(x))

    data = pd.DataFrame(np.column_stack([x, y]), columns=['x', 'y'])

    return data


def expand_dataset(data, n_expansions, feature_name='x'):
    data = data.copy()
    for i in range(2, n_expansions):
        colname = f'{feature_name}^{i}'
        data[colname] = data[feature_name]**i
    return data


def fit_and_plot_linear_regression(data):
    y = data['y']
    X = data.drop('y', axis=1)

    lr = LinearRegression(normalize=True)

    lr.fit(X, y)

    plt.scatter(X['x'], data['y'], c='orange', s=5)
    plt.plot(X['x'], lr.predict(X))
    plt.xlabel('X')
    plt.ylabel('y')
    plt.title('Linear Regression (R²: {})'.format(lr.score(X, y)))
