import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

## Visualization Functions for exploring zillow data ##

# Pairwise Relationships Viz

def plot_variable_pairs(df):
    train.sample(50)
    sns.pairplot(train.sample(50), kind='reg', corner=True, plot_kws={'line_kws':{'color':'red'}})


# Categorical & Continuous Vars Visualizations

def plot_categorical_and_continuous_vars(df, cat_cols, cont_cols):
    for cont in cont_cols:
        for cat in cat_cols:
            fig = plt.figure(figsize= (20, 10))
            fig.suptitle(f'{cont} vs {cat}')
            

            plt.subplot(131)
            sns.stripplot(data=df, x = cat, y = cont)
           

            plt.subplot(1, 3, 3)
            sns.boxplot(data = df, x = cont, hue = cat)
            
            
            plt.subplot(1, 3, 2)
            sns.barplot(data = df, x = cat, y = cont)

# Plot for above loop
## plot_categorical_and_continuous_vars(train, cat_cols, cont_cols)


