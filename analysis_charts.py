# Charts creation for the analysis of the data

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd





# read the data from the csv file
    # ! Change the path to the csv file when data are cleaned, actually it's the raw data !
pals_attributes = pd.read_csv('raw_data/Palworld_Data--Palu combat attribute table.csv', skiprows=1, delimiter=',')
pals_attributes.columns = pals_attributes.columns.str.replace(' ', '_')

pals_job_skills = pd.read_csv('raw_data/Palworld_Data-Palu Job Skills Table.csv', skiprows=1, delimiter=',')

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



# Call the functions to create the charts

#pals_product_distribution(pals_job_skills)
pals_size_distribution(pals_attributes)
pals_category_distribution(pals_attributes)
pals_hp_distribution(pals_attributes)   
pals_rarity_distribution(pals_attributes)
pals_food_intake_distribution(pals_job_skills)
