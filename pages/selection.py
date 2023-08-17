from streamlit_extras.dataframe_explorer import dataframe_explorer
import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header
from st_pages import add_page_title

add_page_title(layout="wide")

colored_header(
    label="Data yang Digunakan",
    description="",
    color_name="violet-70",
)


df = pd.read_csv('assets/inicsv.csv')

# for KPI's Viz
col1, col2= st.columns(2)
col1.metric("Jumlah Data", len(df.index))
col2.metric("Jenis Peraturan", df['Tingkatan'].nunique())