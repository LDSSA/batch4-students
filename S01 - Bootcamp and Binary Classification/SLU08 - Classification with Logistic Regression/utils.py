import time
from IPython import display
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
import math

import warnings
warnings.filterwarnings("ignore")

def get_data_iris():
	X, Y = load_iris(True)
	X = pd.DataFrame(X, columns = ['SEPAL_LENGTH', 'SEPAL_WIDTH', 'PETAL_LENGTH', 'PETAL_WIDTH'])
	Y = pd.Series(Y, name = 'SPECIES')
	return X, Y

def plot_pair_plots(X, Y):
	data = pd.concat((X,Y),axis=1)
	sns.pairplot(data,hue="SPECIES")

def get_sepal_vs_petal_width():
    X, y = get_data_iris()
    df = pd.concat([X[['SEPAL_WIDTH', 'PETAL_WIDTH', ]], y], axis=1)
    df = df.loc[df.SPECIES.isin([1, 2])]
    df.SPECIES = df.SPECIES.map({1: 0, 2: 1})
    return df

def super_simple_classifier_plot(X, Y):
	data = pd.concat((X,Y),axis=1)
	data.loc[data["SPECIES"]!=0, "SPECIES"] = 1
	sns.lmplot("SEPAL_LENGTH", "PETAL_WIDTH",data=data, hue="SPECIES", fit_reg=False)
	plt.plot(np.linspace(4,8,1000), [0.8]*1000, 'r-')

def linear_separation_plot(X, Y):
	data = pd.concat((X,Y),axis=1)
	xx, yy = np.mgrid[4:8:.01, 0:2.8:.01]
	grid = np.c_[xx.ravel(), yy.ravel()]
	for species in [2,1,0]:
		labels = data.loc[data.SPECIES != species,'SPECIES'].unique()
		clf = LogisticRegression(random_state=0).fit(data.loc[data.SPECIES != species,['SEPAL_LENGTH','PETAL_WIDTH']],
			data.loc[data.SPECIES != species,'SPECIES'])
		probs = clf.predict_proba(grid)[:, 1].reshape(xx.shape)
		f, ax = plt.subplots(figsize=(8, 6))
		contour = ax.contourf(xx, yy, probs, 25, cmap="RdBu",
		                      vmin=0, vmax=1)
		ax_c = f.colorbar(contour)

		ax_c.set_label("$P(Species = %0.1i)$"%labels[1])
		ax_c.set_ticks([0, .25, .5, .75, 1])

		ax.scatter(data.loc[data.SPECIES != species,'SEPAL_LENGTH'], data.loc[data.SPECIES != species,'PETAL_WIDTH'],
			c=data.loc[data.SPECIES != species,'SPECIES'],
			s=50,cmap="RdBu", vmin=-.2, vmax=1.2,edgecolor="white", linewidth=1)
		ax.set(aspect="equal",
		       xlim=(4, 8), ylim=(0, 2.8),
		       xlabel="SEPAL_LENGTH", ylabel="PETAL_WIDTH", title="Logistic Regression Classification Between Species %0.1i and %0.1i" % (labels[0], labels[1]))
		plt.show()

def predict_probability_point(X, Y, point):
	data = pd.concat((X,Y),axis=1)
	a, b = point
	clf = LogisticRegression(random_state=0).fit(data.loc[data.SPECIES != 0,['SEPAL_WIDTH','PETAL_WIDTH']],
			data.loc[data.SPECIES != 0,'SPECIES'])
	probs = clf.predict_proba(np.array([[a,b]]))[:, 1]
	print("The probability of point (%0.1f,%0.1f) belonging to Species 1 is %0.2f" % (a, b, probs))


def final_classification_plot(X, Y, threshold_values):
    data = pd.concat((X,Y),axis=1)
    data = data.loc[data['SPECIES']!=0]
    xx, yy = np.mgrid[0.7:2.8:.01, 1.9:4:.01]
    grid = np.c_[xx.ravel(), yy.ravel()]
    for threshold in threshold_values:
        clf = LogisticRegression(random_state=0).fit(data.loc[:,['PETAL_WIDTH','SEPAL_WIDTH']],
                                                     data.loc[:,'SPECIES'])
        probs = clf.predict_proba(grid)[:, 1]
        probs[probs>=threshold] = 1
        probs[probs<threshold] = 0
        probs = probs.reshape(xx.shape)
        f, ax = plt.subplots(figsize=(8, 6))
        contour = ax.contourf(xx, yy, probs, 25, cmap="RdBu",
                      vmin=0, vmax=1)
        ax.scatter(data['PETAL_WIDTH'], data['SEPAL_WIDTH'],
                   c=data['SPECIES'],
                   s=50,cmap="tab10", vmin=-.2, vmax=1.2,edgecolor="white", linewidth=1)
        ax.set(aspect="equal",
               xlim=(0.7, 2.8), ylim=(1.9, 4),
               xlabel="PETAL_WIDTH", ylabel="SEPAL_WIDTH", title="Logistic Regression Classification Using threshold = %0.2f" % (threshold))
        plt.show()


def get_split(x, coef1, coef2, intercept):
    y = (0.5 - (coef1 * x) - intercept) / coef2
    return y


def get_separation_line(x_range, linear_reg):
    line_x = x_range

    line_y = [get_split(i,
                        linear_reg.coef_[0],
                        linear_reg.coef_[1],
                        linear_reg.intercept_)
              for i in line_x]

    return line_x, line_y


def get_sepal_length_vs_petal_width():
    X, y = get_data_iris()
    df = pd.concat([X[['SEPAL_LENGTH', 'PETAL_WIDTH', ]], y], axis=1)
    df.SPECIES = df.SPECIES.map({0: 1, 1: 0, 2: 0})

    return df


def plot_line(df, x, y, c, linear_reg):
    ax = df.plot(kind='scatter', x=x,
                 y=y, c=c,
                 cmap='seismic', s=45, figsize=(12, 8), sharex=False, );

    line_x, line_y = get_separation_line(x_range=np.linspace(1, 2.5, 100),
                                         linear_reg=linear_reg)

    plt.plot(line_x, line_y, c="k", ls='--', alpha=.5,
             label=['Prediction = 0.5'])
    plt.legend()
    plt.ylim([df.SEPAL_WIDTH.min() - .5, df.SEPAL_WIDTH.max() + .5])
    plt.show()


def plot_line_and_annot(df, lin_reg, x='PETAL_WIDTH', y='SEPAL_WIDTH',
                        c='predictions_linreg', ):
    ax = df.plot(kind='scatter', x=x, y=y, c=c, cmap='seismic',
                 s=45, figsize=(12, 8), sharex=False, );

    line_x, line_y = get_separation_line(x_range=np.linspace(1, 2.5, 100),
                                         linear_reg=lin_reg)

    plt.plot(line_x, line_y, c="k", ls='--', alpha=.5,
             label=['Prediction = 0.5'])
    plt.legend()
    plt.ylim([df.SEPAL_WIDTH.min() - .5, df.SEPAL_WIDTH.max() + .5])

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.2)

    ax.text(.5, 0.61, '50%', transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    text = '~100% sure\nit is a Versicolour'

    ax.text(.07, 0.1, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='center', bbox=props)

    text = '~100% sure\nis a Virginica'

    ax.text(.93, 0.9, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='center', bbox=props)

    text = '~80% sure\nis a Virginica'

    ax.text(.8, 0.75, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='center', bbox=props)

    text = '~60% sure\nis a Virginica'

    ax.text(.6, 0.42, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='center', bbox=props)

    plt.show()


def draw_logit_curve(df):
    pca = PCA(n_components=1)
    X = pca.fit_transform(df[df.columns[0:2]])
    lr = LogisticRegression()
    lr.fit(X, df['SPECIES'])
    margin = 5
    space = np.linspace(-margin, margin, 100)
    pd.Series(lr.predict_proba(space.reshape(-1, 1))[:, 1], index=space).plot()
    plt.xlabel('Distance to line')
    plt.ylabel('Probability of being red')
    plt.show()


def get_new_version_of_dataset(df_full):
    df_new = df_full[['SEPAL_WIDTH', 'PETAL_WIDTH', 'SPECIES']].copy()
    df_new = df_new.loc[df_new['SPECIES'].isin([1, 2])]

    df_new['SPECIES'] = df_new['SPECIES'].replace({1: 0, 2: 1})
    df_new['STEM_TENSILE_STRENGTH'] = (df_new['PETAL_WIDTH'] + 1) * 10e8

    return df_new


def gradient_descent_classification_plot(X, Y, iter):
	data = pd.concat((X,Y),axis=1)
	xx, yy = np.mgrid[4:8:.01, 0:2.8:.01]
	grid = np.c_[xx.ravel(), yy.ravel()]
	species = 2
	labels = data.loc[data.SPECIES != species,'SPECIES'].unique()
	clf = LogisticRegression(max_iter=1, warm_start = True, solver = 'sag',random_state=0).fit(data.loc[data.SPECIES != species,['SEPAL_LENGTH','PETAL_WIDTH']],
			data.loc[data.SPECIES != species,'SPECIES'])
	probs = clf.predict_proba(grid)[:, 1].reshape(xx.shape)
	f, ax = plt.subplots(figsize=(8, 6))

	for i in range(iter):
		display.clear_output(wait=True)
		time.sleep(0.1)
		contour = ax.contourf(xx, yy, probs, 25, cmap="RdBu",
		vmin=0, vmax=1)

		ax.scatter(data.loc[data.SPECIES != species,'SEPAL_LENGTH'], data.loc[data.SPECIES != species,'PETAL_WIDTH'],
		c=data.loc[data.SPECIES != species,'SPECIES'],
		s=50,cmap="RdBu", vmin=-.2, vmax=1.2,edgecolor="white", linewidth=1)
		ax.set(aspect="equal",
		       xlim=(4, 8), ylim=(0, 2.8),
		       xlabel="SEPAL_LENGTH", ylabel="PETAL_WIDTH", title="Logistic Regression Classification Between Species %0.1i and %0.1i \n (iteration %0.1i)" % (labels[0], labels[1], i+1))
		if(i==0):
			ax_c = f.colorbar(contour)
			ax_c.set_label("$P(Species = %0.1i)$"%labels[1])
			ax_c.set_ticks([0, .25, .5, .75, 1])
		display.display(plt.gcf());
		clf.fit(data.loc[data.SPECIES != species,['SEPAL_LENGTH','PETAL_WIDTH']],
		data.loc[data.SPECIES != species,'SPECIES'])
		probs = clf.predict_proba(grid)[:, 1].reshape(xx.shape)
	plt.clf();

def plot_maximum_log_likelihood():
	x = np.linspace(0,1,1000)
	cost_one = []
	cost_zero = []
	for i in x:
		cost_one.append(logloss(1,i))
		cost_zero.append(logloss(0,i))
	f, axs = plt.subplots(nrows=1,ncols=2)
	ax = axs[0]
	ax.set(xlabel="$\hat{p}$", ylabel="Maximum Log-Likelihood", title="Maximum Log-Likelihood for y = 0")
	ax.plot(x,cost_zero)
	ax = axs[1]
	ax.set(xlabel="$\hat{p}$", ylabel="Maximum Log-Likelihood", title="Maximum Log-Likelihood for y = 1")
	ax.plot(x,cost_one)
	plt.tight_layout()
	plt.show()

def logloss(true_label, predicted, eps=1e-15):
  p = np.clip(predicted, eps, 1 - eps)
  if true_label == 1:
    return -np.log(p)
  else:
    return -np.log(1 - p)

def univariate_classifier(X, Y):
    binary_plotter(X,Y)
    petal_width = pd.Series(np.linspace(0,3))
    y_hat = pd.Series(2.61 + petal_width*-3.9779452)
    classifier = pd.concat((petal_width, y_hat), axis=1)
    plt.plot(classifier.iloc[:,0], classifier.iloc[:,1], color='red')


def univariate_classifier_logit(X, Y):
    binary_plotter(X,Y)
    petal_width = pd.Series(np.linspace(0,3))
    y_hat = pd.Series(1/(1+math.e**-(2.61 + petal_width*-3.9779452)))
    classifier = pd.concat((petal_width, y_hat), axis=1)
    plt.plot(classifier.iloc[:,0], classifier.iloc[:,1], color='red')


def binary_plotter(X, Y):
    data = pd.concat((X,Y),axis=1)
    data['SPECIES'] = np.where(data.SPECIES == 0, 1, 0)
    sns.lmplot("PETAL_WIDTH", "SPECIES",data=data, hue="SPECIES", fit_reg=False)


def multivariate_plot(X, Y):
    data = pd.concat((X,Y),axis=1)
    data = data.loc[data.SPECIES != 0]
    data['SPECIES'] = np.where(data.SPECIES == 2, 1, 0)
    sns.lmplot("PETAL_WIDTH", "SEPAL_WIDTH",data=data, hue="SPECIES", fit_reg=False)
	#plt.plot(np.linspace(4,8,1000), [0.8]*1000, 'r-')


def multivariate_simple_classifier(X, Y):
	multivariate_plot(X, Y)
	plt.plot(np.linspace(4,8,1000), [0.8]*1000, 'r-')


def bar_plot_output(series):
    series.value_counts().plot.bar()
    plt.xlabel('Class')
    plt.ylabel('Number of observations')