import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, \
    recall_score, f1_score, roc_auc_score, roc_curve, confusion_matrix

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression

# this is for grading without showing the answers
import hashlib


def hash_answer(answer):
    answer = str(answer)
    return hashlib.sha256((answer).encode()).hexdigest()


def show_confusion_matrix():
    data = pd.read_csv('data/classifier_prediction_scores_reversed.csv').rename(columns={'scores': 'probas'})
    # this is scikit-learn's confusion matrix, we will use it a lot!
    confmat = confusion_matrix(y_true=data['target'],
                               y_pred=data['probas'].map(lambda x: 1 if x > .2 else 0))

    make_confmat_pretty(confmat)
    
def get_realistic_dataset():
    data = pd.read_csv('data/heart_disease_binary.csv')
    return pd.concat([data,
                      pd.concat([data.loc[data.disease == 0] for i in range(20)], axis=0)
                      ], axis=0).sample(frac=1).drop('Unnamed: 0', axis=1)


def paint(row):
    attr = 'color: red'
    base = 'color: black'

    paint = row.copy()
    keep_as_is = ['predicted_proba', 'disease']
    cols_to_color = [c for c in row.index if c not in keep_as_is]

    for col in cols_to_color:
        paint[col] = row[col] != row['disease']

    for col in keep_as_is:
        paint[col] = False

    return paint.replace(True, attr).replace(False, base).values


def threshold_df_at(df, thresh):
    df['threshold at %s' % str(thresh)] = df['predicted_proba'].map(
        lambda x: threshold_probas(x, thresh))

    return df


def threshold_probas(proba, threshold=.5):
    if proba >= threshold:
        return 1
    else:
        return 0


def get_rates(df):
    fpr, trp, thresh = roc_curve(y_score=df.predicted_proba,
                                 y_true=df.disease)

    rates = pd.DataFrame({'False Positive Rate': fpr, 'True Positive Rate': trp},
                         index=thresh).sort_index()
    rates.index.name = 'Threshold'
    return rates.loc[rates.index<=1]


def get_subset(df_):

    df_ = df_.loc[:, ['predicted_proba', 'disease']]

    # horrible hack so that the visualization is clearer 
    df_.loc[[280, 235, 104, 12, 265, 79], 'disease'] = 0 
    
    return df_

def plot_roc_curve(roc_auc, fpr, tpr):
    # Function to plot ROC Curve
    # Inputs: 
    #     roc_auc - AU ROC value (float)
    #     fpr - false positive rate (output of roc_curve()) array
    #     tpr - true positive rate (output of roc_curve()) array
    plt.figure(figsize=(8, 6))
    lw = 2
    plt.plot(fpr, tpr, color='orange', lw=lw, label='ROC curve (AUROC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--', label='random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.grid()
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()


def make_confmat_pretty(confmat):
    # Plot the confusion matrix
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.matshow(confmat, cmap=plt.cm.Blues, alpha=0.4)
    for i in range(confmat.shape[0]):
        for j in range(confmat.shape[1]):
            ax.text(x=j, y=i,
                    s=confmat[i, j],
                    va='center', ha='center')
    plt.xlabel('predicted label')
    plt.ylabel('true label')
    plt.title('Confusion Matrix')
    plt.show()


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

    features = [c for c in data.columns if c != target]

    X_train = data.loc[train_index, features]
    y_train = data.loc[train_index, target]
    X_test = data.loc[test_index, features]
    y_test = data.loc[test_index, target]

    return X_train, y_train, X_test, y_test


    
def load_data():
    cancer = load_breast_cancer()
    true_labels = cancer.target
    classifier = LogisticRegression(solver='liblinear')
    
    sample_size = 40
    classifier.fit(cancer.data[0:sample_size], true_labels[0:sample_size])
    predicted_labels = classifier.predict(cancer.data)
    probas = classifier.predict_proba(cancer.data)[:, 1]

    
    return true_labels, predicted_labels, probas
