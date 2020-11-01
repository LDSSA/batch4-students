import sys
import argparse

import ml_metrics as metrics

parser = argparse.ArgumentParser()
parser.add_argument('y_true', help='Path to y_true')
parser.add_argument('y_pred', help='Path to y_pred')


def prepare_lines(content):

    songs = {}
    for l in content:
        l = l.strip().split(',')
        songs[l[0]] = [int(i) for i in l[1:]]

    return songs


def validate_predictions(y_true, y_pred):
    if len(y_pred) != len(y_true):
        raise ValueError(
            'Wrong number of users, expected {} got {}'.format(
                len(y_true), len(y_pred))
        )
        
    test_users = set(y_true.keys())
    pred_users = set(y_pred.keys())
    if test_users != pred_users:
        raise ValueError(
            'Unexpected user ids, please check that you are providing '
            'recommendations for the correct users'
        )
        

def evaluate(y_true, y_pred):

    validate_predictions(y_true, y_pred)
    
    actual = []
    predicted = []

    for user_id in y_true.keys():
        actual.append(y_true[user_id])
        predicted.append(y_pred[user_id])

    return metrics.mapk(actual, predicted, k=100)


if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.y_true) as fh:
        y_true = prepare_lines(fh.readlines())

    with open(args.y_pred) as fh:
        y_pred = prepare_lines(fh.readlines())

    print(evaluate(y_true, y_pred))


