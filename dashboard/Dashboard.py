import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import plotly.express as px
import requests
from PIL import Image

import streamlit.components.v1 as components

st.set_page_config(page_title='Algorand MEV Dashboard', layout = 'wide', page_icon = './images/logo.jpg')

st.title("Algorand MEV Dashboard")

filepath = "prices_responses.csv"
df = pd.read_csv(filepath)


df['upper_bound'] = df['binance_algousdt'] * 1.003
df['lower_bound'] = df['binance_algousdt'] * 0.997


fig = px.line(df, x='timestamp', y=['binance_algousdt', 'humbleswap_algousdc', 'humbleswap_algogousd',
                                   'pact_algousdc', 'pact_algousdt', 'tinyman_algousdc', 'tinyman_algousdt'],
             title="Price Data")


# Add the upper and lower bounds as additional lines
fig.add_scatter(x=df['timestamp'], y=df['upper_bound'], mode='lines', line=dict(width=0.5, color='lightblue'),
                showlegend=False)
fig.add_scatter(x=df['timestamp'], y=df['lower_bound'], mode='lines', line=dict(width=0.5, color='lightblue'),
                showlegend=False)


st.plotly_chart(fig, use_container_width=True)

round = st.text_input('Block Height (round)', '')

image1 = Image.open("images/algo.png")
image2 = Image.open("images/usdt.png")


col0, col1, col2, col3, col4, col5 = st.columns([20, 1, 1, 1, 30, 10])
col0.write("TxID [2LOER3TT4FUJM6FHQZPME6OX56ZMFP2CTGB3RK5HOX44T7PPHGIA]")
col1.image(image1, width=25, use_column_width=False)
col2.write("→")
col3.image(image2, width=25, use_column_width=False)
col4.write("sender: NNEJ6IOFB2D7EUA2VHTFVAUNLY2XZGBMXG5WUW2XJ3IBAJPUW4PNTZ7KIA")
col4.write("receiver: SVZS7Q7QMVHZONDHZJHR4564VTMEX3OQ5DSYBWKR5FJFTPZLVG3EZIWC34")
col5.empty()

if round:
    response = requests.get(f"https://algoindexer.algoexplorerapi.io/v2/blocks/{round}").json()
    if "message" in response and response["message"].startswith("error"):
        st.warning(f"{round} not a valid block-number (round).")
    else:
        st.text("Summary")
        st.text("ALGO → USDC")
        st.text("JSON-Response")
        st.json(response["transactions"], expanded=False)
