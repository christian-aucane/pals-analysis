from pathlib import Path
import streamlit as st
from pandas import DataFrame, read_csv


def get_transposed_csv(csv_path: str | Path) -> DataFrame:
    return read_csv(csv_path).T


DATA_PATH = Path("raw_data/Palworld_Data-Tower BOSS attribute comparison.csv")
DATA = get_transposed_csv(DATA_PATH)


def display_app(data: DataFrame) -> None:
    select_box = [1, 2]
    filters = [1, 2]
    st.write(""" # My first app""")
    st.sidebar.title("Title")
    _ = st.sidebar.selectbox("Select Box", select_box)
    _ = st.sidebar.multiselect(
        'Select Filter', filters)
    st.line_chart(data)


def main() -> None:
    display_app(DATA)


if __name__ == "__main__":
    main()
