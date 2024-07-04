import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import streamlit as st
import mysql.connector
import numpy as np
import pandas as pd
import seaborn as sns
from utils.db.database import Database

# Fonction pour importer les données depuis MySQL
def import_data():
    # Connexion à MySQL
    palworld_database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="leo",
        database="palworld_database"
    )
    cursor = palworld_database.cursor()

    # Importation du dataset
    cursor.execute("SELECT volume_size, genus_category, rarity, element_1, element_2 FROM pals")
    dataset = cursor.fetchall()

    # Fermeture de la connexion
    cursor.close()
    palworld_database.close()

    return dataset

# Creating an instance of the Database class
db = Database(user='root', password='leo', host='localhost', database='palworld_database')

# Fonction pour créer le graphique en secteur de la distribution des tailles de volume
def volume_size_distribution_pie():
    # Importation du dataset
    dataset = import_data()

    # Extraction de volume_size du dataset
    volume_size = [row[0] for row in dataset]

    # Création d'un dictionnaire pour compter la fréquence de chaque volume_size
    volume_size_freq = {}
    for size in volume_size:
        if size in volume_size_freq:
            volume_size_freq[size] += 1
        else:
            volume_size_freq[size] = 1

    # Définition des couleurs
    colors = {'XS': 'lightgreen', 'S': 'green', 'M': 'yellow', 'L': 'orange', 'XL': 'red'}

    # Ordre des tailles souhaité
    sizes_order = ['XS', 'S', 'M', 'L', 'XL']
    volume_size_freq = {size: volume_size_freq.get(size, 0) for size in sizes_order}

    # Création d'une figure plus grande
    plt.figure(figsize=(10, 10))

    # Création du graphique en secteur
    plt.pie(volume_size_freq.values(), labels=volume_size_freq.keys(), autopct='%1.1f%%', startangle=90, colors=[colors[size] for size in volume_size_freq.keys()], counterclock=False)
    plt.title('Percentage Distribution of Number of Pals by Volume Size')
    st.pyplot(plt)

# Function to plot the distribution of number of pals by volume size and genus category
def volume_size_distribution_genus_bar():
    # Importation du dataset
    dataset = import_data()
    if not dataset:
        return  # Si l'importation échoue, arrêter l'exécution de la fonction

    # Extraction de volume_size et genus_category du dataset
    volume_size = [row[0] for row in dataset]
    genus_category = [row[1] for row in dataset]

    # Création d'un dictionnaire pour compter la fréquence de chaque volume_size pour chaque genus_category
    volume_size_freq = {}
    for i in range(len(volume_size)):
        size = volume_size[i]
        category = genus_category[i]
        if size not in volume_size_freq:
            volume_size_freq[size] = {}
        if category in volume_size_freq[size]:
            volume_size_freq[size][category] += 1
        else:
            volume_size_freq[size][category] = 1

    # Définition des couleurs pour les catégories de genre
    colors = {'Humanoid': 'pink', 'Bird': 'skyblue', 'FourLegged': 'brown', 'Other': 'gray', 'Fish': 'blue', 'Dragon': 'orange', 'Monster': 'red'}

    # Ordre des tailles et catégories souhaité
    sizes_order = ['XS', 'S', 'M', 'L', 'XL']
    categories_order = ['Humanoid', 'Bird', 'FourLegged', 'Other', 'Fish', 'Dragon', 'Monster']

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(sizes_order))
    for category in categories_order:
        values = [volume_size_freq[size].get(category, 0) for size in sizes_order]
        bars = ax.bar(sizes_order, values, bottom=bottom, color=colors[category])
        bottom += values

        # Ajout du texte à l'intérieur des barres
        for bar, value in zip(bars, values):
            height = bar.get_height()
            if height != 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, str(value), ha='center', va='center', color='black', fontsize=8)

    # Ajout du nombre total de pals au-dessus de chaque barre
    for i, total in enumerate(bottom):
        ax.text(sizes_order[i], total, str(int(total)), ha='center', va='bottom', color='black', fontsize=10)

    ax.set_xlabel('Volume Size')
    ax.set_ylabel('Number of Pals')
    ax.set_title('Distribution of Number of Pals by Volume Size and Genus Category')
    ax.legend(categories_order, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0, max(bottom) * 1.1)

    st.pyplot(fig)

# Fonction pour créer le graphique en barres empilées de la distribution des tailles de volume par catégorie de rareté
def volume_size_distribution_rarity_bar():

    # Importation du dataset
    dataset = import_data()
    if not dataset:
        return  # Si l'importation échoue, arrêter l'exécution de la fonction

    # Extraction de volume_size et rarity du dataset
    volume_size = [row[0] for row in dataset]
    rarity = [row[2] for row in dataset]

    # Convertir les nombres de rareté en catégories
    rarity_categories = []
    for r in rarity:
        if 1 <= r <= 4:
            rarity_categories.append('common')
        elif 5 <= r <= 7:
            rarity_categories.append('rare')
        elif 8 <= r <= 10:
            rarity_categories.append('epic')
        else:  # r > 10
            rarity_categories.append('legendary')

    # Création d'un dictionnaire pour compter la fréquence de chaque volume_size pour chaque catégorie de rareté
    volume_size_freq = {}
    for i in range(len(volume_size)):
        size = volume_size[i]
        category = rarity_categories[i]
        if size not in volume_size_freq:
            volume_size_freq[size] = {}
        if category in volume_size_freq[size]:
            volume_size_freq[size][category] += 1
        else:
            volume_size_freq[size][category] = 1

    # Définition des couleurs pour les catégories de rareté
    colors = {'common': 'gray', 'rare': 'blue', 'epic': 'purple', 'legendary': 'orange'}

    # Ordre des tailles et catégories souhaité
    sizes_order = ['XS', 'S', 'M', 'L', 'XL']
    categories_order = ['common', 'rare', 'epic', 'legendary']

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(sizes_order))
    for category in categories_order:
        values = [volume_size_freq[size].get(category, 0) for size in sizes_order]
        bars = ax.bar(sizes_order, values, bottom=bottom, color=colors[category])
        bottom += values

        # Ajout du texte à l'intérieur des barres
        for bar, value in zip(bars, values):
            height = bar.get_height()
            if height != 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, str(value), ha='center', va='center', color='black', fontsize=8)

    # Ajout du nombre total de pals au-dessus de chaque barre
    for i, total in enumerate(bottom):
        ax.text(sizes_order[i], total, str(int(total)), ha='center', va='bottom', color='black', fontsize=10)

    ax.set_xlabel('Volume Size')
    ax.set_ylabel('Number of Pals')
    ax.set_title('Distribution of Number of Pals by Volume Size and Rarity Category')
    ax.legend(categories_order, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0, max(bottom) * 1.1)

    st.pyplot(fig)

# Fonction pour créer le graphique en camembert de la distribution des catégories de genre des Pals
def genus_category_distribution_pie():
    # Importation du dataset
    dataset = import_data()
    if not dataset:
        return  # Si l'importation échoue, arrêter l'exécution de la fonction

    # Extraction de genus_category du dataset
    genus_category = [row[1] for row in dataset]

    # Création d'un dictionnaire pour compter la fréquence de chaque catégorie de genre
    genus_category_freq = {}
    for category in genus_category:
        if category in genus_category_freq:
            genus_category_freq[category] += 1
        else:
            genus_category_freq[category] = 1

    # Définition des couleurs pour les catégories de genre
    colors = {
        'Humanoid': 'pink', 'Bird': 'skyblue', 'FourLegged': 'brown', 
        'Other': 'gray', 'Fish': 'blue', 'Dragon': 'orange', 'Monster': 'red'
    }

    # Création de la figure
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Création du graphique en camembert
    wedges, texts, autotexts = ax.pie(
        genus_category_freq.values(), 
        labels=genus_category_freq.keys(), 
        autopct='%1.1f%%', 
        pctdistance=0.9, 
        startangle=90, 
        colors=[colors[category] for category in genus_category_freq.keys()], 
        counterclock=False
    )
    
    # Style des textes
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_color('white')

    ax.set_title('Percentage Distribution of Number of Pals by Genus Category')
    
    # Afficher le graphique avec Streamlit
    st.pyplot(fig)

# Fonction pour créer le graphique en barres de la distribution des catégories de genre des Pals par rareté
def genus_category_distribution_rarity_bar():
    # Importation du dataset
    dataset = import_data()
    if not dataset:
        return  # Si l'importation échoue, arrêter l'exécution de la fonction

    # Extraction de genus_category et rarity du dataset
    genus_category = [row[1] for row in dataset]
    rarity = [row[2] for row in dataset]

    # Conversion des nombres de rareté en catégories
    rarity_categories = []
    for r in rarity:
        if 1 <= r <= 4:
            rarity_categories.append('common')
        elif 5 <= r <= 7:
            rarity_categories.append('rare')
        elif 8 <= r <= 10:
            rarity_categories.append('epic')
        else:  # r > 10
            rarity_categories.append('legendary')

    # Création d'un dictionnaire pour compter la fréquence de chaque catégorie de genre pour chaque catégorie de rareté
    genus_category_freq = {}
    for i in range(len(genus_category)):
        category = genus_category[i]
        rarity_category = rarity_categories[i]
        if category not in genus_category_freq:
            genus_category_freq[category] = {}
        if rarity_category in genus_category_freq[category]:
            genus_category_freq[category][rarity_category] += 1
        else:
            genus_category_freq[category][rarity_category] = 1

    # Définition des couleurs pour les catégories de rareté
    colors = {'common': 'gray', 'rare': 'blue', 'epic': 'purple', 'legendary': 'orange'}

    # Ordre des catégories de genre et de rareté
    categories_order = ['Humanoid', 'Bird', 'FourLegged', 'Other', 'Fish', 'Dragon', 'Monster']
    rarity_order = ['common', 'rare', 'epic', 'legendary']

    # Création de la figure
    fig, ax = plt.subplots(figsize=(10, 6))  # Augmenter la taille de la figure
    bottom = np.zeros(len(categories_order))
    for rarity_category in rarity_order:
        values = [genus_category_freq[category].get(rarity_category, 0) for category in categories_order]
        bars = ax.bar(categories_order, values, bottom=bottom, color=colors[rarity_category])
        bottom += values

        # Ajout du texte à l'intérieur des barres
        for bar, value in zip(bars, values):
            height = bar.get_height()
            if height != 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, str(value), ha='center', va='center', color='black', fontsize=8)

    # Ajout du nombre total de Pals au-dessus de chaque barre
    for i, total in enumerate(bottom):
        ax.text(categories_order[i], total, str(int(total)), ha='center', va='bottom', color='black', fontsize=10)

    ax.set_xlabel('Genus Category')
    ax.set_ylabel('Number of Pals')
    ax.set_title('Distribution of Number of Pals by Genus Category and Rarity Category')
    ax.legend(rarity_order, bbox_to_anchor=(1.05, 1), loc='upper left')  # Déplacer la légende sur le côté droit du graphique
    ax.set_ylim(0, max(bottom)*1.1)  # Augmenter la valeur maximale de l'axe y de 10%

    # Afficher le graphique avec Streamlit
    st.pyplot(fig)

# Fonction pour créer le graphique en barres de la distribution des catégories de genre des Pals par élément unique
def genus_category_distribution_single_element_bar():
    # Importation du dataset
    dataset = import_data()
    if not dataset:
        return  # Si l'importation échoue, arrêter l'exécution de la fonction

    # Extraction de genus_category, element_1 et element_2 du dataset
    genus_category = [row[1] for row in dataset]
    element_1 = [row[3] for row in dataset]
    element_2 = [row[4] for row in dataset]

    # Création d'un dictionnaire pour compter la fréquence de chaque catégorie de genre pour chaque élément unique
    genus_category_freq = {}
    for i in range(len(genus_category)):
        category = genus_category[i]
        if element_2[i] is None:  # Considérer uniquement les Pals avec un seul élément
            element = element_1[i]
            if category not in genus_category_freq:
                genus_category_freq[category] = {}
            if element in genus_category_freq[category]:
                genus_category_freq[category][element] += 1
            else:
                genus_category_freq[category][element] = 1

    # Définition des couleurs pour les éléments
    colors = {'generally': 'gray', 'fire': '#ff4500', 'water': '#1e90ff', 'dark': 'black', 'electricity': '#ffd700', 'Wood': '#8B4513', 'land': '#32CD32', 'ice': '#87CEFA', 'dragon': '#C71585'}

    # Ordre des éléments et des catégories
    elements_order = ['generally', 'fire', 'water', 'dark', 'electricity', 'Wood', 'land', 'ice', 'dragon']
    categories_order = ['Humanoid', 'Bird', 'FourLegged', 'Other', 'Fish', 'Dragon', 'Monster']

    # Création de la figure
    fig, ax = plt.subplots(figsize=(10, 6))  # Augmenter la taille de la figure
    bottom = np.zeros(len(categories_order))
    for element in elements_order:
        values = [genus_category_freq[category].get(element, 0) if category in genus_category_freq else 0 for category in categories_order]
        bars = ax.bar(categories_order, values, bottom=bottom, color=colors[element])
        bottom += values

        # Ajout du texte à l'intérieur des barres
        for bar, value in zip(bars, values):
            height = bar.get_height()
            if height != 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, str(value), ha='center', va='center', color='white', fontsize=8)

    # Ajout du nombre total de Pals au-dessus de chaque barre
    for i, total in enumerate(bottom):
        ax.text(categories_order[i], total, str(int(total)), ha='center', va='bottom', color='black', fontsize=10)

    ax.set_xlabel('Genus Category')
    ax.set_ylabel('Number of Pals')
    ax.set_title('Distribution of Number of Pals by Genus Category and Element')
    ax.legend(elements_order, bbox_to_anchor=(1.05, 1), loc='upper left')  # Déplacer la légende sur le côté droit du graphique
    ax.set_ylim(0, max(bottom)*1.1)  # Augmenter la valeur maximale de l'axe y de 10%

    # Afficher le graphique avec Streamlit
    st.pyplot(fig)

# Fonction pour créer le graphique en barres de la distribution des catégories de genre des Pals par élément combiné
def genus_category_distribution_double_element_combined_bar():
    # Importation du dataset
    dataset = import_data()
    if not dataset:
        return  # Si l'importation échoue, arrêter l'exécution de la fonction

    # Extraction de genus_category, element_1 et element_2 du dataset
    genus_category = [row[1] for row in dataset]
    element_1 = [row[3] for row in dataset]
    element_2 = [row[4] for row in dataset]

    # Création d'un dictionnaire pour compter la fréquence de chaque catégorie de genre pour chaque élément combiné
    genus_category_freq = {}
    unique_combined_elements = set()  # Pour stocker les éléments combinés uniques
    for i in range(len(genus_category)):
        category = genus_category[i]
        if element_2[i] is not None:  # Considérer uniquement les Pals avec deux éléments
            combined_element = element_1[i] + "/" + element_2[i]
            unique_combined_elements.add(combined_element)  # Ajouter l'élément combiné à l'ensemble
            if category not in genus_category_freq:
                genus_category_freq[category] = {}
            if combined_element in genus_category_freq[category]:
                genus_category_freq[category][combined_element] += 1
            else:
                genus_category_freq[category][combined_element] = 1

    # Définition des couleurs pour chaque élément combiné
    colors = {
        'dragon/dark': '#800000',
        'Wood/dragon': '#008000',
        'water/dragon': '#000080',
        'fire/dark': '#808000',
        'electricity/dragon': '#800080',
        'ice/land': '#008080',
        'dark/land': '#808080',
        'dragon/electricity': '#C0C0C0',
        'dragon/fire': '#FF0000',
        'Wood/water': '#00FF00',
        'ice/dragon': '#0000FF',
        'ice/dark': '#FFFF00',
        'water/ice': '#FF00FF',
        'dragon/water': '#00FFFF',
        'Wood/land': '#000000',
        'land/Wood': '#A52A2A',
        'fire/land': '#D2691E'
    }

    # Ordre des éléments combinés et des catégories
    combined_elements_order = list(unique_combined_elements)  # Utiliser les éléments combinés uniques pour l'ordre
    categories_order = ['Humanoid', 'Bird', 'FourLegged', 'Other', 'Fish', 'Dragon', 'Monster']

    # Création de la figure
    fig, ax = plt.subplots(figsize=(10, 6))  # Augmenter la taille de la figure
    bottom = np.zeros(len(categories_order))
    for combined_element in combined_elements_order:
        values = [genus_category_freq[category].get(combined_element, 0) if category in genus_category_freq else 0 for category in categories_order]
        bars = ax.bar(categories_order, values, bottom=bottom, color=colors.get(combined_element, 'gray'))
        bottom += values

        # Ajout du texte à l'intérieur des barres
        for bar, value in zip(bars, values):
            height = bar.get_height()
            if height != 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, str(value), ha='center', va='center', color='white', fontsize=8)

    # Ajout du nombre total de Pals au-dessus de chaque barre
    for i, total in enumerate(bottom):
        ax.text(categories_order[i], total, str(int(total)), ha='center', va='bottom', color='black', fontsize=10)

    ax.set_xlabel('Genus Category')
    ax.set_ylabel('Number of Pals')
    ax.set_title('Distribution of Number of Pals by Genus Category and Combined Element')
    ax.legend(combined_elements_order, bbox_to_anchor=(1.05, 1), loc='upper left')  # Déplacer la légende sur le côté droit du graphique
    ax.set_ylim(0, max(bottom)*1.1)  # Augmenter la valeur maximale de l'axe y de 10%

    # Afficher le graphique avec Streamlit
    st.pyplot(fig)

def hp_distribution_pie():
    # Importing the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["hp"])

    # Extracting hp from the dataset
    hp = dataset["hp"]

    # Counting the number of pals for each unique HP value
    hp_counts = hp.value_counts().sort_index()

    # Normalizing HP values to 0-1 range for color mapping
    norm = mcolors.Normalize(vmin=hp_counts.index.min(), vmax=hp_counts.index.max())

    # Creating a color map
    cmap = plt.get_cmap('RdYlGn')

    # Creating the pie chart with color gradient
    plt.pie(hp_counts, labels=hp_counts.index, colors=[cmap(norm(value)) for value in hp_counts.index], autopct='%1.1f%%')

    # Change fig size
    fig = plt.gcf()
    fig.set_size_inches(10, 10)

    # Adding a title
    plt.title('Percentage Distribution of Number of Pals by HP')

    # Display the plot with Streamlit
    st.pyplot(fig)

def hp_distribution_bar():
    # Importing the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["hp"])

    # Extracting hp from the dataset
    hp = dataset["hp"]

    # Counting the number of pals for each unique HP value
    hp_counts = hp.value_counts().sort_index()

    # Creating a larger figure
    plt.figure(figsize=(10, 10))  # Increase the size of the figure

    # Normalizing HP values to 0-1 range for color mapping
    norm = mcolors.Normalize(vmin=hp_counts.index.min(), vmax=hp_counts.index.max())

    # Creating a color map
    cmap = plt.get_cmap('RdYlGn')

    # Creating the bar plot with wider bars and color gradient
    bars = plt.bar(hp_counts.index, hp_counts, color=[cmap(norm(value)) for value in hp_counts.index], edgecolor='black', width=1.0)

    plt.title('Distribution of Number of Pals by HP')
    plt.xlabel('HP')
    plt.ylabel('Number of Pals')

    # Setting the xticks to the HP values
    plt.xticks(hp_counts.index)

    # Adding the text above each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, yval, ha='center', va='bottom')

    # Display the plot with Streamlit
    st.pyplot(plt.gcf())

def hp_rarity_distribution_bar():
    # Importing the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["hp", "rarity"])

    # Extracting hp and rarity from the dataset
    hp = dataset["hp"]
    rarity = dataset["rarity"]

    # Convert rarity numbers to categories
    rarity_categories = []
    for r in rarity:
        if 1 <= r <= 4:
            rarity_categories.append('common')
        elif 5 <= r <= 7:
            rarity_categories.append('rare')
        elif 8 <= r <= 10:
            rarity_categories.append('epic')
        else:  # r > 10
            rarity_categories.append('legendary')

    # Adding the rarity categories to the dataset
    dataset['rarity_category'] = rarity_categories

    # Counting the number of pals for each unique HP value for each rarity category
    hp_rarity_counts = dataset.groupby(['hp', 'rarity_category']).size().unstack(fill_value=0)

    # Creating a larger figure
    plt.figure(figsize=(20, 20))  # Increase the size of the figure

    # Creating the bar plot with wider bars and color gradient
    bars = hp_rarity_counts.plot(kind='bar', stacked=True, color=['gray', 'blue', 'purple', 'orange'], edgecolor='black', width=0.5)

    # Adding the text inside and above each bar
    for i, (hp, row) in enumerate(hp_rarity_counts.iterrows()):
        y_offset = 0
        for j, col in enumerate(row):
            value = int(col)
            if value != 0:
                plt.text(i, y_offset + value/2, value, ha='center', va='center', color='black', fontsize=8)
            y_offset += value
        plt.text(i, y_offset, y_offset, ha='center', va='bottom', color='black', fontsize=10)

    # Change fig size
    fig = plt.gcf()
    fig.set_size_inches(10, 10)

    plt.title('Distribution of Number of Pals by HP and Rarity Category')
    plt.xlabel('HP')
    plt.ylabel('Number of Pals')

    # Display the plot with Streamlit
    st.pyplot(plt.gcf())

def hp_genus_distribution_bar():
    # Importing the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["hp", "genus_category"])

    # Extracting hp and genus_category from the dataset
    hp = dataset["hp"]
    genus_category = dataset["genus_category"]

    # Counting the number of pals for each unique HP value for each genus category
    hp_genus_counts = dataset.groupby(['hp', 'genus_category']).size().unstack(fill_value=0)

    # Defining color gradient for genus category
    colors = {'Humanoid': 'pink', 'Bird': 'skyblue', 'FourLegged': 'brown', 'Other': 'gray', 'Fish': 'blue', 'Dragon': 'orange', 'Monster': 'red'}

    # Creating a larger figure
    plt.figure(figsize=(20, 20))  # Increase the size of the figure

    # Creating the bar plot with wider bars and color gradient
    bars = hp_genus_counts.plot(kind='bar', stacked=True, color=[colors[genus] for genus in hp_genus_counts.columns], edgecolor='black', width=0.5)

    # Adding the text inside and above each bar
    for i, (hp, row) in enumerate(hp_genus_counts.iterrows()):
        y_offset = 0
        for j, col in enumerate(row):
            value = int(col)
            if value != 0:
                plt.text(i, y_offset + value/2, value, ha='center', va='center', color='black', fontsize=8)
            y_offset += value
        plt.text(i, y_offset, y_offset, ha='center', va='bottom', color='black', fontsize=10)

    # Change fig size
    fig = plt.gcf()
    fig.set_size_inches(10, 10)

    plt.title('Distribution of Number of Pals by HP and Genus Category')
    plt.xlabel('HP')
    plt.ylabel('Number of Pals')

    # Display the plot with Streamlit
    st.pyplot(plt.gcf())

def plot_hp_combat_attribute_relationships():
    # Importing the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["hp", "melee_attack", "remote_attack", "defense", "support"])

    # Creating the pairplot
    pairplot = sns.pairplot(dataset)

    # Display the plot with Streamlit
    st.pyplot(pairplot.fig)

def plot_hp_combat_attribute_correlation():
    # Importing the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["hp", "melee_attack", "remote_attack", "defense", "support"])

    # Calculating the correlation matrix
    corr = dataset.corr()

    # Creating the heatmap
    plt.figure(figsize=(10, 10))
    heatmap = sns.heatmap(corr, annot=True, cmap='coolwarm')

    # Display the plot with Streamlit
    st.pyplot(heatmap.get_figure())

def rarity_distribution_pie():
    # Importing the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["rarity"])

    # Extracting rarity from the dataset
    rarity = dataset["rarity"]

    # Convert rarity numbers to categories
    rarity_categories = []
    for r in rarity:
        if 1 <= r <= 4:
            rarity_categories.append('common')
        elif 5 <= r <= 7:
            rarity_categories.append('rare')
        elif 8 <= r <= 10:
            rarity_categories.append('epic')
        else:  # r > 10
            rarity_categories.append('legendary')

    # Counting the number of pals for each rarity category
    rarity_counts = pd.Series(rarity_categories).value_counts()

    # Defining color gradient for rarity category
    colors = {'common': 'gray', 'rare': 'blue', 'epic': 'purple', 'legendary': 'orange'}

    # Creating the pie chart with color gradient
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(rarity_counts, labels=rarity_counts.index, colors=[colors[category] for category in rarity_counts.index], autopct='%1.1f%%')

    ax.set_title('Percentage Distribution of Number of Pals by Rarity Category')

    # Display the plot with Streamlit
    st.pyplot(fig)

def plot_rarity_vs_attributes():
    # Import the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["rarity", "hp", "melee_attack", "remote_attack", "defense", "support"])

    # Convert rarity numbers to categories
    rarity_categories = []
    for r in dataset['rarity']:
        if 1 <= r <= 4:
            rarity_categories.append('common')
        elif 5 <= r <= 7:
            rarity_categories.append('rare')
        elif 8 <= r <= 10:
            rarity_categories.append('epic')
        else:  # r > 10
            rarity_categories.append('legendary')

    # Adding the rarity categories to the dataset
    dataset['rarity_category'] = rarity_categories

    # Calculate the average of each attribute for each rarity category
    avg_attributes_by_rarity = dataset.groupby('rarity_category')[["hp", "melee_attack", "remote_attack", "defense", "support"]].mean()

    # Order the data by rarity category
    ordered_categories = ['common', 'rare', 'epic', 'legendary']
    avg_attributes_by_rarity = avg_attributes_by_rarity.reindex(ordered_categories)

    # Create a stacked bar chart with color coding
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_attributes_by_rarity.plot(kind='bar', stacked=True, color={"hp": "red", "melee_attack": "lime", "remote_attack": "orange", "defense": "tan", "support": "green"}, ax=ax)

    # Add attribute values to the bars
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        ax.text(x + width / 2,
                y + height / 2,
                '{:.0f}'.format(height),
                horizontalalignment='center',
                verticalalignment='center')

    # Move the legend to the right side of the plot
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title('How a Pal\'s Rarity Affects Its Base Attribute Values')
    plt.xlabel('Rarity')
    plt.ylabel('Average Attribute Values')

    # Display the plot with Streamlit
    st.pyplot(fig)

def alimentary_distribution_pie():
    # Importing the dataset
    dataset = db.get_df_from_select(table_name="job-skill", columns_names=["food_intake"])

    # Extracting food_intake from the dataset
    food_intake = dataset["food_intake"]

    # Counting the number of pals for each food intake value
    food_intake_counts = food_intake.value_counts().sort_index()

    # Defining color gradient for food intake
    cmap = plt.get_cmap('RdYlGn_r')  # 'RdYlGn_r' is a colormap that goes from red to green
    colors = [cmap(i) for i in np.linspace(0, 1, len(food_intake_counts))]

    # Creating a larger figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Creating the pie chart
    wedges, texts, autotexts = ax.pie(food_intake_counts, labels=food_intake_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)

    # Adding a color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=1, vmax=9))
    fig.colorbar(sm, ax=ax, orientation='vertical', label='Food Intake (1=Low, 9=High)', pad=0.02)

    plt.title('Percentage Distribution of Pals by Food Intake')
    
    # Display the plot with Streamlit
    st.pyplot(fig)

def alimentary_distribution_bar():
    # Importing the dataset
    dataset = db.get_df_from_select(table_name="job-skill", columns_names=["food_intake"])

    # Extracting food_intake from the dataset
    food_intake = dataset["food_intake"]

    # Counting the number of pals for each food intake value
    food_intake_counts = food_intake.value_counts().sort_index()

    # Defining color gradient for food intake
    cmap = plt.get_cmap('RdYlGn_r')  # 'RdYlGn_r' is a colormap that goes from red to green
    colors = [cmap(i) for i in np.linspace(0, 1, len(food_intake_counts))]

    # Creating a larger figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Creating the bar plot
    bars = ax.bar(food_intake_counts.index, food_intake_counts, color=colors, edgecolor='black', width=0.5)

    # Adding the text above each bar
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.05, yval, ha='center', va='bottom')

    # Adding a color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=1, vmax=9))
    fig.colorbar(sm, ax=ax, orientation='vertical', label='Food Intake (1=Low, 9=High)', pad=0.02)

    plt.title('Distribution of Number of Pals by Food Intake')
    plt.xlabel('Food Intake')
    plt.ylabel('Number of Pals')

    # Display the plot with Streamlit
    st.pyplot(fig)

# Function to plot the fighting power distribution of pals into a pie chart
def plot_combat_power_distribution():

    # Replace this with your actual database retrieval logic
    # Import the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["hp", "melee_attack", "remote_attack", "defense", "support"])

    # Calculate combat power
    dataset['combat_power'] = dataset.sum(axis=1)

    # Create a larger figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create a histogram of the combat power distribution
    n, bins, patches = ax.hist(dataset['combat_power'], bins=30, edgecolor='black')

    # Add the actual values above each bar
    for i in range(len(patches)):
        ax.text(patches[i].get_x() + patches[i].get_width()/2., n[i], str(int(n[i])), ha='center')

    # Create a color gradient from green to red based on combat power
    fracs = bins[:-1] / bins[:-1].max()
    norm = mcolors.Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.RdYlGn(norm(thisfrac))
        thispatch.set_facecolor(color)

    # Add combat power formula
    combat_power_formula = "Combat Power = hp + melee_attack + remote_attack + defense + support"
    fig.text(0.5, 0.01, combat_power_formula, wrap=True, horizontalalignment='center', fontsize=12)

    plt.title('Distribution of pals\' combat power')
    plt.xlabel('Combat Power')
    plt.ylabel('Number of pals')

    # Display the plot with Streamlit
    st.pyplot(fig)

# Function to plot the top 10 strongest pals in a horizontal stacked bar chart
def plot_top10_pals():

    # Replace this with your actual database retrieval logic
    # Import the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["name", "hp", "melee_attack", "remote_attack", "defense", "support"])

    # Calculate combat power
    dataset['combat_power'] = dataset[["hp", "melee_attack", "remote_attack", "defense", "support"]].sum(axis=1)

    # Sort the dataset by combat power and take the top 10
    top10_pals = dataset.sort_values(by='combat_power', ascending=True).tail(10)

    # Create a larger figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create a horizontal stacked bar chart
    top10_pals.set_index('name')[["hp", "melee_attack", "remote_attack", "defense", "support"]].plot(kind='barh', stacked=True, 
        color={"hp": "red", "melee_attack": "lime", "remote_attack": "orange", "defense": "tan", "support": "green"}, ax=ax)

    # Add the values for each attribute in the bars
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        ax.text(x+width/2, 
                y+height/2, 
                '{:.0f}'.format(width), 
                horizontalalignment='center', 
                verticalalignment='center')

    # Move the legend to the right side of the plot
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title('Top 10 Strongest Pals')
    plt.xlabel('Combat Power')
    plt.ylabel('Pal Name')

    # Display the plot with Streamlit
    st.pyplot(fig)

# Function to plot the average rarity of pals with the highest attack power
def plot_avg_rarity_of_high_attack_pals():

    # Replace this with your actual database retrieval logic
    # Import the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["rarity", "melee_attack", "remote_attack"])

    # Convert rarity numbers to categories
    rarity_categories = []
    for r in dataset['rarity']:
        if 1 <= r <= 4:
            rarity_categories.append('common')
        elif 5 <= r <= 7:
            rarity_categories.append('rare')
        elif 8 <= r <= 10:
            rarity_categories.append('epic')
        else:  # r > 10
            rarity_categories.append('legendary')

    # Adding the rarity categories to the dataset
    dataset['rarity_category'] = rarity_categories

    # Group by rarity category and calculate average melee attack and average remote attack
    avg_melee_attack_by_rarity = dataset.groupby('rarity_category')['melee_attack'].mean()
    avg_remote_attack_by_rarity = dataset.groupby('rarity_category')['remote_attack'].mean()

    # Order the data by rarity category
    ordered_categories = ['common', 'rare', 'epic', 'legendary']
    avg_melee_attack_by_rarity = avg_melee_attack_by_rarity.reindex(ordered_categories)
    avg_remote_attack_by_rarity = avg_remote_attack_by_rarity.reindex(ordered_categories)

    # Define colors for each rarity category in valid Matplotlib format
    rarity_colors = ['gray', 'blue', 'purple', '#FF8C00']  # Modify these colors as needed

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plotting bars
    ax.bar(ordered_categories, avg_melee_attack_by_rarity, color=rarity_colors, label='Average Melee Attack')
    ax.bar(ordered_categories, avg_remote_attack_by_rarity, bottom=avg_melee_attack_by_rarity, color=[0.5, 0.5, 0.5], label='Average Remote Attack')

    ax.set_title('Average Rarity of Pals with Highest Attack Power')
    ax.set_ylabel('Average Attack Power')
    ax.legend()

    # Add annotation
    ax.text(1.5, -25, "Note: The average attack power is calculated as the mean of melee attack and remote attack for each rarity category.", ha="center", fontsize=8, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

    # Change x-axis labels color
    ax.set_xticks(range(len(ordered_categories)))
    ax.set_xticklabels(ordered_categories, color='black')  # Change 'black' to desired color

    # Display the plot with Streamlit
    st.pyplot(fig)

# Function to plot pal size vs combat performance
def plot_size_vs_performance():

    # Replace this with your actual database retrieval logic
    # Import the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["name", "hp", "melee_attack", "remote_attack", "defense", "support", "volume_size"])

    # Calculate combat power
    dataset['combat_power'] = dataset[["hp", "melee_attack", "remote_attack", "defense", "support"]].sum(axis=1)

    # Define the order
    size_order = ['XS', 'S', 'M', 'L', 'XL']

    # Convert 'volume_size' to a categorical type with the specified order
    dataset['volume_size'] = pd.Categorical(dataset['volume_size'], categories=size_order, ordered=True)

    # Create a larger figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a scatter plot
    ax.scatter(dataset['volume_size'], dataset['combat_power'])

    ax.set_title('Pal Size vs Combat Performance')
    ax.set_xlabel('Size')
    ax.set_ylabel('Combat Power')

    # Add an annotation
    fig.text(0.5, -0.15, 'Combat performance is calculated as the sum of hp, melee_attack, remote_attack, defense, and support.',
             ha='center', fontsize=10, bbox={'facecolor': 'wheat', 'alpha': 0.5, 'pad': 5})

    # Display the plot with Streamlit
    st.pyplot(fig)

# Function to plot pal size vs combat performance
def plot_size_vs_performance_correlation():

    # Replace this with your actual database retrieval logic
    # Import the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["name", "hp", "melee_attack", "remote_attack", "defense", "support", "volume_size"])

    # Calculate combat power
    dataset['combat_power'] = dataset[["hp", "melee_attack", "remote_attack", "defense", "support"]].sum(axis=1)

    # Define the order
    size_order = ['XS', 'S', 'M', 'L', 'XL']

    # Convert 'volume_size' to a categorical type with the specified order
    dataset['volume_size'] = pd.Categorical(dataset['volume_size'], categories=size_order, ordered=True)

    # Convert 'volume_size' to numerical values for correlation calculation
    dataset['volume_size_num'] = dataset['volume_size'].cat.codes

    # Calculate the correlation matrix
    correlation_matrix = dataset[['volume_size_num', 'combat_power']].corr()

    # Create a larger figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create a heatmap
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)

    ax.set_title('Correlation between Pal Size and Combat Performance')

    # Display the plot with Streamlit
    st.pyplot(fig)

# Function to plot the average speed of pals vs combat performance
def plot_speed_vs_performance():

    # Replace this with your actual database retrieval logic
    # Import the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["name", "hp", "melee_attack", "remote_attack", "defense", "support", "volume_size", "slow_walking_speed", "walking_speed", "running_speed"])

    # Calculate combat power
    dataset['combat_power'] = dataset[["hp", "melee_attack", "remote_attack", "defense", "support"]].sum(axis=1)

    # Calculate average speed
    dataset['average_speed'] = dataset[["slow_walking_speed", "walking_speed", "running_speed"]].mean(axis=1)

    # Create a larger figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a scatter plot
    ax.scatter(dataset['average_speed'], dataset['combat_power'])

    ax.set_title('Average Speed of Pals vs Combat Performance')
    ax.set_xlabel('Average Speed of Pals')
    ax.set_ylabel('Combat Performance')

    # Display the plot with Streamlit
    st.pyplot(fig)

# Function to plot the correlation between average speed and combat performance
def plot_speed_vs_performance_correlation():

    # Replace this with your actual database retrieval logic
    # Import the dataset
    dataset = db.get_df_from_select(table_name="pals", columns_names=["name", "hp", "melee_attack", "remote_attack", "defense", "support", "volume_size", "slow_walking_speed", "walking_speed", "running_speed"])

    # Calculate combat power
    dataset['combat_power'] = dataset[["hp", "melee_attack", "remote_attack", "defense", "support"]].sum(axis=1)

    # Calculate average speed
    dataset['average_speed'] = dataset[["slow_walking_speed", "walking_speed", "running_speed"]].mean(axis=1)

    # Calculate the correlation matrix
    correlation_matrix = dataset[['average_speed', 'combat_power']].corr()

    # Create a larger figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Create a heatmap
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)

    ax.set_title('Correlation between Average Speed and Combat Performance')

    # Display the plot with Streamlit
    st.pyplot(fig)

