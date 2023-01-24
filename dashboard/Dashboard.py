import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import plotly.express as px


st.set_page_config(page_title='Algorand MEV Dashboard', layout = 'wide', page_icon = './images/logo.jpg')

st.title("Algorand MEV Dashboard")

filepath = "../data/prices.csv"
df = pd.read_csv(filepath)
print(df.head())

st.line_chart(df)
