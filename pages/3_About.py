import streamlit as st
import pandas as pd
import requests
import io

st.markdown('### About')

url = f'https://raw.githubusercontent.com/phawitb/crawler-led3-window/main/currentstage.csv'
response = requests.get(url)
df = pd.read_csv(io.StringIO(response.text))

st.write(df)