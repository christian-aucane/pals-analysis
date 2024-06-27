from pathlib import Path
import streamlit as st
from pandas import DataFrame, read_csv
from utils.db.database import Database

def get_transposed_csv(csv_path: str | Path) -> DataFrame:
    return read_csv(csv_path).T


DATA_PATH = Path("raw_data/Palworld_Data-Tower BOSS attribute comparison.csv")
DATA = get_transposed_csv(DATA_PATH)
db = Database(user= "root",password= "leo",host= "localhost",database= "palworld_database")

def get_data(table_name: str, columns_names: list[str]):
    return db.get_df_from_select(table_name=table_name,columns_names=columns_names)

def display_app(data: DataFrame) -> None:
    select_box = [1, 2]
    filters = [
        'name', 'hp', 'melee_attack', 'remote_attack', 'defense', 'support',
        'experience_ratio', 'slow_walking_speed', 'walking_speed',
        'running_speed', 'riding_speed', 'handling_speed', 'ignore_the_bluntness',
        'ignore_displacement', 'biological_grade', 'endurance', 'fecundity']
    filter_graphique = []
    st.sidebar.title("Title")
    _ = st.sidebar.selectbox("Select Box", select_box)
    _ = st.sidebar.multiselect(
        'Select Filter', filters)
    hp = get_data("tower-boss-attribute", ["hp"])
    st.line_chart(hp)


def main() -> None:
    display_app(DATA)


if __name__ == "__main__":
    main()
