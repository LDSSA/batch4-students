import random
import pandas as pd

from sklearn.datasets import make_classification


WORDS = open('data/words.txt').read().splitlines()


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

    def create_limbs_cols(dataset: pd.DataFrame, n: int = 4):
        limbs = ['arm', 'leg', 'arm', 'leg']
        for i in range(n):
            dataset['{limb}_{num}'.format(limb=limbs[i], num=i)] = random.choices(
                population=WORDS, k=100)

        return dataset

    X = create_limbs_cols(X)

    def rearrange_cols(ds: pd.DataFrame):
        cols = list(ds.columns)
        random.shuffle(cols)
        return ds.loc[:, cols]

    return rearrange_cols(X), y


workflow_steps = [
    'Get the data', 'Spam', 'Data analysis and preparation', 'Google Hackathon solutions',
    'Evaluate results', 'Iterate', 'Train model', 'Watch Netflix',  'Establish a Baseline',
    'Increase complexity'
]

random.shuffle(workflow_steps)

data_analysis_steps = [
    'Feature engineering', 'Dealing with data problems',
    'Data analysis', 'Feature selection',
    'Spanish Inquisition'
]

random.shuffle(data_analysis_steps)
