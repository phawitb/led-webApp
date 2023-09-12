import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import requests
import io
from streamlit_folium import st_folium
from datetime import datetime
# import numpy as np
from folium import plugins
import base64
import extra_streamlit_components as stx
# import datetime
import json
import math

import pygsheets

import pandas as pd

# # Creating a sample DataFrame
# data = {'A': [1, 2, 3, 4, 5],
#         'B': [10, 20, 30, 40, 50],
#         'C': ['apple', 'banana', 'cherry', 'date', 'elderberry']}

# df = pd.DataFrame(data)

# # Filtering based on multiple conditions
# condition1 = df['A'] > 2
# condition2 = df['B'] < 40
# filtered_df = df[condition1 & condition2]

# print(filtered_df)

cookie_manager = stx.CookieManager()
person_id = cookie_manager.get(cookie='person_id')



gc = pygsheets.authorize(service_account_file='led-sheet-47e8afe294c8.json')
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/16dO1zkakREjZxbjB6XFGijHFjjOUDYNpjwoeuUW5gP8/edit?usp=sharing')
worksheet = spreadsheet.sheet1

fav_df = df = worksheet.get_as_df()

def check_favorate(user_id,link):

    
    # st.write(df)
    # st.write(link)

    condition1 = fav_df['user_id'] == user_id
    condition2 = fav_df['link'] == link
    df_f = fav_df[condition1 & condition2]

    if df_f.shape[0] != 0:
        return True
    else:
        return False

    



def update_sheet(user_id,province,link,sta):
    df = worksheet.get_as_df()
    # result = df.isin([user_id,province,link]).all(axis=1)
    # print(df)
    condition1 = df['user_id'] == user_id
    condition2 = df['province'] == province
    condition3 = df['link'] == link
    df_f = df[condition1 & condition2 & condition3]
    index = list(df_f.index)

    if index:
        print('data exist')
        worksheet.update_value(f'A{index[0]+2}', user_id)
        worksheet.update_value(f'B{index[0]+2}', province)
        worksheet.update_value(f'C{index[0]+2}', sta)
        worksheet.update_value(f'D{index[0]+2}', link)
        
    else:
        print('data not exist')
        cells = worksheet.get_all_values(include_tailing_empty_rows=None, include_tailing_empty=False, returnas='matrix')
        last_row = len(cells)

        cells = worksheet.get_all_values(include_tailing_empty_rows=None, include_tailing_empty=False, returnas='matrix')
        last_row = len(cells)
        # print(last_row)
        worksheet.update_value(f'A{last_row+1}', user_id)
        worksheet.update_value(f'B{last_row+1}', province)
        worksheet.update_value(f'C{last_row+1}', sta)
        worksheet.update_value(f'D{last_row+1}', link)
        

    #     
    #     
    #     

    # print(df_f)
    # index = df_f.index

    # if index:
    #     print('data exist')
    # else:
    #     print('data not exist')

    # index = df[df['user_id'] == user_id & df['province'] == province]

    # if not result.any():
    #     cells = worksheet.get_all_values(include_tailing_empty_rows=None, include_tailing_empty=False, returnas='matrix')
    #     last_row = len(cells)
    #     # print(last_row)
    #     worksheet.update_value(f'A{last_row+1}', user_id)
    #     worksheet.update_value(f'B{last_row+1}', province)
    #     worksheet.update_value(f'C{last_row+1}', link)
    #     worksheet.update_value(f'D{last_row+1}', sta)
    # else:
    #     worksheet.update_value(f'A{index+1}', user_id)
    #     worksheet.update_value(f'B{index+1}', province)
    #     worksheet.update_value(f'C{index+1}', link)
    #     worksheet.update_value(f'D{index+1}', sta)



# update_sheet('aaaasdfsdf','aaasdvsdv','vbbbsdvdssc',0)

# user_id = st.session_state["current_id"]
st.write(person_id)
a = check_favorate('legalexecution.app@gmail.com','https://asset.led.go.th/newbid-old/asset_open.asp?law_suit_no=%BC%BA.1778&law_suit_year=2556&deed_no=44778&addrno=-')

st.write(a)