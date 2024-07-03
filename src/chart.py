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
db = Database(user='root', password='root', host='localhost', database='palworld_database')

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
