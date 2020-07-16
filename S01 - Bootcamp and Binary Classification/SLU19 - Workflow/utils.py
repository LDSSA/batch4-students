import json
import random
import pandas as pd
from hashlib import sha1

from sklearn.datasets import make_classification


def get_dataset():

    X, y = make_classification(random_state=42)
    X = pd.DataFrame(X)
    X.columns = [str(col) for col in X.columns]

    def create_na(ds: pd.DataFrame, nb_cols: int = 5):
        random.seed(42)
        random_cols = random.choices(population=range(ds.shape[1]), k=nb_cols)
        seeds = range(nb_cols)

        def get_indexes(seed, n, k):
            random.seed(seed)
            return random.choices(population=range(n), k=k)

        for i in seeds:
            ds.iloc[get_indexes(seed=i, n=ds.shape[0], k=15), random_cols[i]] = None

        return ds

    X = create_na(X)

    def create_evil_cols(dataset: pd.DataFrame, n: int = 3):
        for i in range(n):
            dataset['evil_{}'.format(i)] = random.choices(
                population=range(100, 1000), k=100)

        return dataset

    X = create_evil_cols(X)

    def rearrange_cols(ds: pd.DataFrame):
        cols = list(ds.columns)
        random.shuffle(cols)
        return ds.loc[:, cols]

    return rearrange_cols(X), y


def _hash(obj, salt='none'):
    if type(obj) is not str:
        obj = json.dumps(obj)
    to_encode = obj + salt
    return sha1(to_encode.encode()).hexdigest()
