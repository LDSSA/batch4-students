import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.metrics import accuracy_score

categoricals = [
    'PassengerId',
    'Name',
    'Ticket',
    'Sex',
    'Cabin',
    'Embarked',
]


# Here are a few functions that we will use to do our proof of concepts
# around training and testing for kaggle submissions for the titanic
# competition.

# The reason that we need to have these functions they way they are
# is to manage the preprocessing of the features the same for the 
# training and test set. Don't worry too much about exactly what's
# going on in these functions right now but rather focus on the concepts
# that are being covered after this in the notebook.


def read_and_get_dummies(drop_columns=[]):
    # when working inside of functions, always call your dataframe
    # _df so that you know you're never using any from the outside!
    _df = pd.read_csv('data/titanic.csv')

    # now drop any columns that are specified as needing to be dropped
    for colname in drop_columns:
        _df = _df.drop(colname, axis=1)

    for colname in categoricals:
        if colname in drop_columns:
            continue
        _df[colname] = _df[colname].fillna('null').astype('category')

    # Split the factors and the target
    X, y = _df.drop('Survived', axis=1), _df['Survived']

    # take special note of this call!
    X = pd.get_dummies(X, dummy_na=True).fillna(-1)

    return _df, X, y


def encode_categoricals(drop_columns=[]):
    # when working inside of functions, always call your dataframe
    # _df so that you know you're never using any from the outside!
    _df = pd.read_csv('data/titanic.csv')

    # now drop any columns that are specified as needing to be dropped
    for colname in drop_columns:
        _df = _df.drop(colname, axis=1)

    for colname in categoricals:
        if colname in drop_columns:
            continue
        _df[colname] = pd.Categorical(_df[colname].fillna('null')).codes

    if 'Age' in _df.columns:
        _df['Age'] = _df['Age'].fillna(_df['Age'].mean())

    # Split the factors and the target
    X, y = _df.drop('Survived', axis=1), _df['Survived']

    return _df, X, y


def train_and_test(drop_columns=[], max_depth=None, test_size=0.2, encode_cats=False):
    """
    Train a decision tree and return the classifier, the X_train,
    and the original dataframe so that they can be used on the test
    set later on.
    """
    if encode_cats:
        _df, X, y = encode_categoricals(drop_columns=drop_columns)
    else:
        _df, X, y = read_and_get_dummies(drop_columns=drop_columns)

    # Now let's get our train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=1, test_size=test_size)

    clf = DecisionTreeClassifier(max_depth=max_depth, random_state=1)
    clf.fit(X_train, y_train)

    score = accuracy_score(y_test, clf.predict(X_test))
    print('X_test accuracy {}'.format(score))
    print('X_train shape: {}'.format(X_train.shape))

    return X_train, _df, clf


def train_and_test_logit(drop_columns=[], test_size=0.2):
    """
    Train a logistic regressionand return the classifier, the X_train,
    and the original dataframe so that they can be used on the test
    set later on. Features are scaled with RobustScaler. Does not
    create dummies but rather encodes categoricals as integers.
    """

    _df, X, y = encode_categoricals(drop_columns=drop_columns)
    X = pd.DataFrame(RobustScaler().fit_transform(X), columns=X.columns)

    # Now let's get our train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=1, test_size=test_size)

    clf = LogisticRegression(random_state=1, solver='lbfgs', penalty='none')
    clf.fit(X_train, y_train)

    score = accuracy_score(y_test, clf.predict(X_test))
    print('X_test accuracy {}'.format(score))
    print('X_train shape: {}'.format(X_train.shape))

    return X_train, _df, clf


def produce_test_predictions(train_df, clf, drop_columns=[]):
    _df = pd.read_csv('data/titanic-test.csv')

    for colname in drop_columns:
        _df = _df.drop(colname, axis=1)

    for colname in categoricals:
        if colname in drop_columns:
            continue
        _df[colname] = _df[colname].fillna('null')
        _df[colname] = pd.Categorical(
            _df[colname],
            categories=train_df[colname].cat.categories
        )

    X = pd.get_dummies(_df, dummy_na=True).fillna(-1)

    return pd.DataFrame({
        'PassengerId': pd.read_csv('data/titanic-test.csv').PassengerId,
        'Survived': pd.Series(clf.predict(X))
    })


def _get_min_max_mean(scores, train_sizes):
    return pd.DataFrame({'max': np.max(scores, axis=1),
                         'mean': np.mean(scores, axis=1),
                         'min': np.min(scores, axis=1)},
                        index=train_sizes)


def _plot_results(results, label):
    if label == 'train':
        color = 'blue'
    else:
        color = 'orange'

    ax = results['mean'].plot(label=label, marker='o')
    ax.fill_between(results.index,
                    results['min'],
                    results['max'],
                    facecolor=color,
                    alpha=0.1)


def plot_learning_curve(train_sizes_abs, train_scores, test_scores):
    train_results = _get_min_max_mean(train_scores, train_sizes_abs)
    test_results = _get_min_max_mean(test_scores, train_sizes_abs)
    train_results = _get_min_max_mean(train_scores, train_sizes_abs)
    test_results = _get_min_max_mean(test_scores, train_sizes_abs)

    _plot_results(train_results, 'train')
    _plot_results(test_results, 'test')

    plt.legend()
    plt.xlabel('Number of training examples')
    plt.ylabel('roc_auc_score')
    plt.title('Learning curve')
    plt.show()
