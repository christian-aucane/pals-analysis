# Charts creation for the analysis of the data

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd



# read the data from the csv file
    # ! Change the path to the csv file when data are cleaned, actually it's the raw data !
pals_attributes = pd.read_csv('raw_data/Palworld_Data--Palu combat attribute table.csv', skiprows=1, delimiter=',')
pals_attributes.columns = pals_attributes.columns.str.replace(' ', '_')


# Function to create the distribution of the size of the pals
def pals_size_distribution(pals_attributes):
    order = ['XS', 'S', 'M', 'L', 'XL']
    colors = ['green', 'yellow', 'orange', 'brown', 'red']  
    pals_size = pals_attributes['Volume_size'].value_counts().loc[order]  # Utilisez 'Volume_size'
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
    plt.title('Distribution des catégories des Pals')
    plt.xlabel('Catégorie')
    plt.ylabel('Nombre de Pals')
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
    plt.ylabel('Pals number')
    plt.xticks(rotation=0)
    plt.show()

# Function to create the distribution of the rarity of the pals
def pals_rarity_distribution(pals_attributes):
    # Créer un dictionnaire de couleurs
    colors = {range(1, 5): 'gray', range(5, 9): 'blue', range(9, 11): 'purple', range(11, max(pals_attributes['rarity'])+1): 'orange'}
    
    # Créer un dictionnaire de traductions
    translations = {'gray': 'common', 'blue': 'rare', 'purple': 'epic', 'orange': 'legendary'}
    
    # Créer une nouvelle colonne 'color' basée sur la colonne 'rarity'
    pals_attributes['color'] = pals_attributes['rarity'].apply(lambda x: next(v for k, v in colors.items() if x in k))
    
    # Trier les valeurs par 'rarity'
    pals_rarity = pals_attributes.sort_values('rarity')['color'].value_counts()[list(colors.values())]
    
    ax = pals_rarity.plot(kind='bar', color=pals_rarity.index, alpha=0.7)
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() / 2, i.get_height() + 0.1, str(i.get_height()), ha='center', va='bottom') 
    plt.title('Rarity Distribution of Pals')
    plt.xlabel('Rarity')
    plt.ylabel('Number of Pals')
    
    # Modifier les étiquettes de l'axe des x
    labels = [translations[label.get_text()] for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=0) 
    
    plt.show()




# Call the functions to create the charts
pals_size_distribution(pals_attributes)
pals_category_distribution(pals_attributes)
pals_hp_distribution(pals_attributes)   
pals_rarity_distribution(pals_attributes)