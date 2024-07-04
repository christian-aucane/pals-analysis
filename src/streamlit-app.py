from pathlib import Path
import streamlit as st
from pandas import DataFrame, read_csv
from utils.db.database import Database
from chart import *


def get_transposed_csv(csv_path: str | Path) -> DataFrame:
    return read_csv(csv_path).T


DATA_PATH = Path("raw_data/Palworld_Data-Tower BOSS attribute comparison.csv")
DATA = get_transposed_csv(DATA_PATH)
db = Database(user="root", password="leo", host="localhost",
              database="palworld_database")


def get_data(table_name: str, columns_names: list[str]):
    return db.get_df_from_select(table_name=table_name, columns_names=columns_names)


def display_app() -> None:
    select_box = ['distribution_pie',
                  'distribution_genus_bar',
                  'distribution_rarity_bar',
                  'genus_category_distribution_pie',
                  'genus_category_distribution_rarity_bar',
                  'genus_category_distribution_single_element_bar',
                  'genus_category_distribution_double_element_combined_bar',
                  'hp_distribution_pie',
                  'hp_distribution_bar',
                  'hp_rarity_distribution_bar',
                  'hp_genus_distribution_bar',
                  'plot_hp_combat_attribute_relationships',
                  'plot_hp_combat_attribute_correlation',
                  'rarity_distribution_pie',
                  'plot_rarity_vs_attributes']
    st.sidebar.title("Title")
    selected_box = st.sidebar.selectbox("Select Box", select_box)
    charts = {'distribution_pie':  volume_size_distribution_pie,
              'distribution_genus_bar': volume_size_distribution_genus_bar,
              'distribution_rarity_bar': volume_size_distribution_rarity_bar,
              'genus_category_distribution_pie': genus_category_distribution_pie,
              'genus_category_distribution_rarity_bar': genus_category_distribution_rarity_bar,
              'genus_category_distribution_single_element_bar': genus_category_distribution_single_element_bar,
              'genus_category_distribution_double_element_combined_bar': genus_category_distribution_double_element_combined_bar,
              'hp_distribution_pie': hp_distribution_pie,
              'hp_distribution_bar': hp_distribution_bar,
              'hp_rarity_distribution_bar': hp_rarity_distribution_bar,
              'hp_genus_distribution_bar': hp_genus_distribution_bar,
              'plot_hp_combat_attribute_relationships': plot_hp_combat_attribute_relationships,
              'plot_hp_combat_attribute_correlation': plot_hp_combat_attribute_correlation,
              'rarity_distribution_pie': rarity_distribution_pie,
              'plot_rarity_vs_attributes': plot_rarity_vs_attributes}
    if selected_box:
        charts[selected_box]()


def main() -> None:
    display_app()


if __name__ == "__main__":
    main()
