import streamlit as st
import pandas as pd


class Analysis:
    def __init__(self):
        self.arr = [1,2]

    def load_data(self):
        self.db = pd.read_csv("raw_data/Palworld_Data-Tower BOSS attribute comparison.csv").T
        st.line_chart(self.db)

    def xx(self):
        pass

    def run(self):
        st.write(""" # My first app""")
        st.sidebar.title("bruh")
        select = st.sidebar.selectbox("bruh", self.arr)
        self.categories = st.sidebar.multiselect('Select Filter',self.arr)
        if select == 1:
            self.load_data()
        elif select == 2:
            self.xx()

if __name__ == "__main__":
    app = Analysis()
    app.run()

