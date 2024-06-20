import streamlit as st
import pandas as pd


class Analysis:
    def __init__(self):
        self.arr = [1,2]

    def x(self):
        db = pd.read_csv("raw_data/Palworld_Data-Tower BOSS attribute comparison.csv")
        st.line_chart(db)

    def xx(self):
        pass

    def run(self):
        st.write(""" # My first app""")
        st.sidebar.title("bruh")
        select = st.sidebar.selectbox("bruh", self.arr)
        if select == 1:
            self.x()
        elif select == 2:
            self.xx()

if __name__ == "__main__":
    app = Analysis()
    app.run()

