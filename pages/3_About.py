import streamlit as st
import pandas as pd
import requests
import io

st.markdown('### About')

def last_df(province):
    df_filter = df[df['province']==province]
    maxdate = max(list(df_filter['date'].unique()))
    df_filter = df_filter[df_filter['date']==maxdate]
    return df_filter


# def all_province():
#     url = f'https://raw.githubusercontent.com/phawitb/crawler-led3-window/main/currentstage.csv'
#     response = requests.get(url)
#     df = pd.read_csv(io.StringIO(response.text))
#     return list(df['province'].unique())


url = f'https://raw.githubusercontent.com/phawitb/crawler-led3-window/main/currentstage.csv'
response = requests.get(url)
df = pd.read_csv(io.StringIO(response.text))

provinces = list(df['province'].unique())

df2 = last_df(provinces[0])

for p in provinces[1:]:
    # df2.concat(last_df(p))
    df2 = pd.concat([df2,last_df(p)])

df2 = df2.sort_values(by='date',ascending=False).reset_index(drop=True)
df2['date'] = pd.to_datetime(df2['date'], format='%Y%m%d')

st.write(df2)

# df_filter = df[df['province']=='nonthaburi']
# maxdate = max(list(df_filter['date'].unique()))
# df_filter = df_filter[df_filter['date']==maxdate]


# st.write(df)
# st.write(provinces)

# df_filter = df[df['province']=='nonthaburi']
# st.write(df_filter)

# maxdate = max(list(df_filter['date'].unique()))
# st.write(maxdate)

# df_filter = df_filter[df_filter['date']==maxdate]
# st.write(df_filter)

# # PROVINCE = all_province()
# # st.write(PROVINCE)
