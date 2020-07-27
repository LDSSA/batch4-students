import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

def prepare_dataset(df):
    df = df.copy()
    df['before_millenium'] = np.where(df['year'] < 2000, 1, 0)
    df['size_set'] = np.where(df['num_parts'] > 100, 'big set', 'small set')
    return df

def get_company_salaries_and_plot():
    
    np.random.seed(100)
    
    # make some companies
    company_a = pd.Series([int(c) for c in np.random.normal(1500, 50, 1000)])
    company_a.name = 'Company A'
    # apply used to intensify the presence of outliers
    company_b = pd.Series([int(c) for c in np.random.normal(1500, 10, 1000)]).apply(lambda x: x + abs(x-1500)**1.78*np.sign(x-1500))
    company_b.name = 'Company B'
    
    # plot the histograms 
    company_a.hist(alpha=.4, label=company_a.name, bins=20, figsize=(12,6), density=True)
    company_b.hist(alpha=.4, label=company_b.name, bins=20, density=True)
    plt.legend()
    plt.xlabel('Salary')
    plt.ylabel('Frequency')
    plt.title('Salary distribution at company A and company B')
    plt.show();
    
    # return them 
    return company_a, company_b

def plot_log_function():
    x = np.arange(0.01, 10, 0.1)
    y = np.log(x)
    plt.figure(figsize=(4,3), dpi=150)
    plt.plot(x, x)
    plt.plot(x, y)
    plt.xlim(0, 10)
    plt.ylim(-3, 10)
    plt.title('Linear and logarithm functions')
    plt.legend(['x', 'log(x)']);
    return True