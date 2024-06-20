# Charts creation for the analysis of the data

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import seaborn as sns
import tkinter as tk





# read the data from the csv file
    # ! Change the path to the csv file when data are cleaned, actually it's the raw data !
pals_attributes = pd.read_csv('raw_data/Palworld_Data--Palu combat attribute table.csv', skiprows=1, delimiter=',')
pals_attributes.columns = pals_attributes.columns.str.replace(' ', '_')

pals_job_skills = pd.read_csv('raw_data/Palworld_Data-Palu Job Skills Table.csv', skiprows=1, delimiter=',')

# Function to create the distribution of the size of the pals
def pals_size_distribution(pals_attributes):
    order = ['XS', 'S', 'M', 'L', 'XL']
    colors = ['green', 'yellow', 'orange', 'brown', 'red']  
    pals_size = pals_attributes['Volume_size'].value_counts().loc[order]
    ax = pals_size.plot(kind='bar', color=colors, alpha=0.7)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() / 2, i.get_height() + 0.1, str(i.get_height()), ha='center', va='bottom') 
    plt.title('Size Distribution of Pals')
    plt.xlabel('Size')
    plt.ylabel('Number of Pals')
    plt.xticks(rotation=0) 
    plt.show()




# Function to create the distribution of the category of the pals
def pals_category_distribution(pals_attributes):
    colors = {'Humanoid': 'green', 'FourLegged': 'brown', 'Bird': 'skyblue', 'Other': 'gray', 'Dragon': 'orange', 'Fish': 'darkblue', 'Monster': 'red'}
    pals_category = pals_attributes['GenusCategory'].str.split('::').str[-1].value_counts()
    ax = pals_category.plot(kind='bar', color=[colors.get(i, '#333333') for i in pals_category.index], alpha=0.7)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() / 2, i.get_height() + 0.1, str(i.get_height()), ha='center', va='bottom') 
    plt.title('Category Distribution of Pals')
    plt.xlabel('Category')
    plt.ylabel('Number of Pals')
    plt.xticks(rotation=0)
    plt.show()

# Function to create the distribution of the HP of the pals
def pals_hp_distribution(pals_attributes):
    pals_hp = pals_attributes['HP'].value_counts().sort_index()
    cmap = mcolors.LinearSegmentedColormap.from_list("n",["red","green"])
    colors = cmap(np.linspace(0, 1, len(pals_hp)))
    ax = pals_hp.plot(kind='bar', color=colors, alpha=0.7)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() / 2, i.get_height() + 0.1, str(i.get_height()), ha='center', va='bottom') 
    plt.title('HP Distribution of Pals')
    plt.xlabel('HP')
    plt.ylabel('Number of Pals')
    plt.xticks(rotation=0)
    plt.show()

# Function to create the distribution of the rarity of the pals
def pals_rarity_distribution(pals_attributes):
    colors = {range(1, 5): 'gray', range(5, 9): 'blue', range(9, 11): 'purple', range(11, max(pals_attributes['rarity'])+1): 'orange'}
    translations = {'gray': 'common', 'blue': 'rare', 'purple': 'epic', 'orange': 'legendary'}
    pals_attributes['color'] = pals_attributes['rarity'].apply(lambda x: next(v for k, v in colors.items() if x in k))
    pals_rarity = pals_attributes.sort_values('rarity')['color'].value_counts()[list(colors.values())]
    ax = pals_rarity.plot(kind='bar', color=pals_rarity.index, alpha=0.7)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() / 2, i.get_height() + 0.1, str(i.get_height()), ha='center', va='bottom') 
    plt.title('Rarity Distribution of Pals')
    plt.xlabel('Rarity')
    plt.ylabel('Number of Pals')
    labels = [translations[label.get_text()] for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=0) 
    plt.show()

# Function to create the distribution of food intake of the pals
def pals_food_intake_distribution(pals_job_skills):
    pals_food_intake = pals_job_skills['Food intake'].value_counts().sort_index()
    cmap = plt.get_cmap('Blues')
    colors = cmap(np.linspace(0.2, 1, len(pals_food_intake)))
    ax = pals_food_intake.plot(kind='bar', color=colors, alpha=0.7)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() / 2, i.get_height() + 0.1, str(i.get_height()), ha='center', va='bottom') 
    plt.title('Food Intake Distribution of Pals')
    plt.xlabel('Food Intake')
    plt.ylabel('Number of Pals')
    plt.xticks(rotation=0)
    plt.show()

#def pals_product_distribution(pals_job_skills):
    #product_colors = {'wool': 'gray', 'Egg': 'white', 'Palu Ball Advanced Palu Ball Arrow Gold Coin': 'gold', 'milk': 'lightblue', 'Marshmallow': 'pink', 'red wild berries': 'red', 'Honey': 'yellow', 'fire breathing organ': 'orange', 'high quality cloth': 'purple'}
    #pals_job_skills['product_color'] = pals_job_skills['ranch items'].map(product_colors)
    #pals_job_skills['product_color'].fillna('black', inplace=True)
    #pals_product = pals_job_skills['ranch items'].value_counts()
    #ax = pals_product.plot(kind='bar', color=pals_job_skills['product_color'].unique(), alpha=0.7)
    #for i in ax.patches:
    #    ax.text(i.get_x() + i.get_width() / 2, i.get_height() + 0.1, str(i.get_height()), ha='center', va='bottom') 
    #plt.title('Product Distribution of Pals')
    #plt.xlabel('Product')
    #plt.ylabel('Number of Pals')
    #plt.xticks(rotation=90)
    #plt.show()

# Function to create a bar chart of the top 10 pals by total combat power
def top_10_pals(pals_attributes):
    pals_attributes['total_combat_power'] = pals_attributes['melee_attack'] + pals_attributes['Remote_attack'] + pals_attributes['defense'] + pals_attributes['support'] + pals_attributes['HP']
    pals_sorted = pals_attributes.sort_values('total_combat_power', ascending=False)
    top_10_pals = pals_sorted.head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, 10))
    ax.barh(top_10_pals['Name'], top_10_pals['total_combat_power'], color=colors)
    ax.set_xlabel('Total Combat Power = melee_attack + Remote_attack + defense + support + HP')
    ax.set_ylabel('Pal Name')
    ax.set_title('Top 10 Pals by Total Combat Power')
    ax.invert_yaxis()
    plt.show()


# Function to create a heatmap of the correlation matrix of the combat attributes
def combat_attributes_correlation(pals_attributes):
    combat_attributes = pals_attributes[['melee_attack', 'Remote_attack', 'defense', 'support', 'HP']]
    corr_matrix = combat_attributes.corr()
    plt.figure(figsize=(10, 8))
    cmap = sns.diverging_palette(10, 130, as_cmap=True)  
    sns.heatmap(corr_matrix, annot=True, cmap=cmap, fmt=".2f")
    plt.title('Correlation Matrix of Combat Attributes')
    plt.show()
    window = tk.Tk()
    window.title("Correlation Details")
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if corr_matrix.iloc[i, j] > 0.5:
                correlation_info = f"{corr_matrix.columns[i]} and {corr_matrix.columns[j]} have a strong positive correlation."
            elif corr_matrix.iloc[i, j] < -0.5:
                correlation_info = f"{corr_matrix.columns[i]} and {corr_matrix.columns[j]} have a strong negative correlation."
            else:
                correlation_info = f"{corr_matrix.columns[i]} and {corr_matrix.columns[j]} have a weak correlation."
            tk.Label(window, text=correlation_info).pack() 
    window.mainloop()

# Function to create a bar chart of the mean combat attributes by rarity
def rarity_vs_attributes(pals_attributes):
    colors = {range(1, 5): 'gray', range(5, 9): 'blue', range(9, 11): 'purple', range(11, max(pals_attributes['rarity'])+1): 'orange'}
    translations = {'gray': 'common', 'blue': 'rare', 'purple': 'epic', 'orange': 'legendary'}
    ordered_colors = ['gray', 'blue', 'purple', 'orange']
    attributes_and_rarity = pals_attributes[['melee_attack', 'Remote_attack', 'defense', 'support', 'HP', 'rarity']]
    attributes_and_rarity['color'] = attributes_and_rarity['rarity'].apply(lambda x: next(v for k, v in colors.items() if x in k))
    mean_attributes_by_color = attributes_and_rarity.groupby('color').mean()
    mean_attributes_by_color = mean_attributes_by_color.loc[ordered_colors]
    for attribute in ['melee_attack', 'Remote_attack', 'defense', 'support', 'HP']:
        plt.figure(figsize=(10, 5))
        plt.bar(mean_attributes_by_color.index, mean_attributes_by_color[attribute], color=mean_attributes_by_color.index)
        plt.xlabel('Rarity')
        plt.ylabel('Mean ' + attribute)
        plt.title('Mean ' + attribute + ' by Rarity')
        labels = [translations[label.get_text()] for label in plt.gca().get_xticklabels()]
        plt.gca().set_xticklabels(labels)
        plt.show()


# Call the functions to create the charts
combat_attributes_correlation(pals_attributes)
rarity_vs_attributes(pals_attributes)
#pals_product_distribution(pals_job_skills)
top_10_pals(pals_attributes)
pals_size_distribution(pals_attributes)
pals_category_distribution(pals_attributes)
pals_hp_distribution(pals_attributes)   
pals_rarity_distribution(pals_attributes)
pals_food_intake_distribution(pals_job_skills)
