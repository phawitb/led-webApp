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
# import firebase_admin
# from firebase_admin import credentials, firestore
# import time
# import random
# import webbrowser

def decimal_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    decimal_minutes = (decimal_degrees - degrees) * 60
    minutes = int(decimal_minutes)
    seconds = (decimal_minutes - minutes) * 60

    return degrees, minutes, seconds

def format_coordinates(latitude, longitude):
    latitude_dms = decimal_to_dms(latitude)
    longitude_dms = decimal_to_dms(longitude)
    
    latitude_str = f"{latitude_dms[0]}°{latitude_dms[1]}'{latitude_dms[2]:.1f}\"N"
    longitude_str = f"{longitude_dms[0]}°{longitude_dms[1]}'{longitude_dms[2]:.1f}\"E"

    return latitude_str + '+' + longitude_str

def create_list(df,n_total):
    for index, row in df.iterrows():
    #     if index ==10:
    #         break
    # for i in range(10):
        COL = st.columns(3)
        # st.divider()
        with COL[0]:
            st.subheader(f":green[{index+1}/{n_total}[{row['sell_order']}]{row['type']}]")

            if not math.isnan(row['lat']):
                decimal_coordinates = (row['lat'], row['lon'])
                print('decimal_coordinates',decimal_coordinates)
                formatted_coordinates = format_coordinates(*decimal_coordinates)
                url = f"https://www.google.com/maps/place/{formatted_coordinates}/@{row['lat']},{row['lon']},17z"
                st.markdown(f"*[{row['tumbon']},{row['aumper']},{row['province']}]({url})*")
            else:
                st.markdown(f"*{row['tumbon']},{row['aumper']},{row['province']}*")

            # st.markdown(f'[Map]({url})')
            
            
            

            area = ''
            a = ['ตร.ว.','งาน','ไร่']
            for i in range(2, -1, -1):
                if isinstance(row[f'size{i}'], int) or isinstance(row[f'size{i}'], float):
                    if row[f'size{i}'] != 0:
                        area += f"{row[f'size{i}']} {a[i]} "
            area = area[:-1]
            st.markdown(f"**:triangular_ruler: {area}**")
            st.markdown(f"วางเงิน {row['pay_down']:,.0f} บาท")
            

            # st.markdown(f"{row['max_price']:,.0f} {row['current_price']:,.0f}")
            date_object = datetime.strptime(str(int(row['lastSta_date'])), "%Y%m%d")
            formatted_date = date_object.strftime("%d/%m/%y")
            st.markdown(f":orange[นัด {int(row['bid_time'])} {formatted_date} {row['lastSta_detail']}]")

            st.markdown(f":blue[{row['status']}]")

            st.subheader(f"[:moneybag: :blue[{row['max_price']:,.0f}]]({row['link']})")
            

            

            
            # st.subheader(':green[ที่ดินพร้อมสิ่งปลูกสร้าง]')
            # st.markdown("*บางกรวย,นนทบุรี*")
            # st.markdown("**2 ไร่ 1 งาน 2 ตร.ว.**")
            # st.subheader(":blue[123,456]")
            # st.markdown("****:red[นัด 1 ปลอดการจำนอง]****")
            



            
            # st.markdown("*Streamlit* is **really** ****cool****.")
            # st.text('บางกรวย,นนทบุรี')
            # st.title('This is a title')
            # st.header('This is a header with a divider')
            # st.subheader('_Streamlit_ is :blue[cool] :sunglasses:')
            # st.divider()
            # st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:')
            # st.text('This is some text.')
            # hc.info_card(title='Some heading GOOD', content='All good!\n\ndvdvd sd sd sd xzcxynfgdsdcvsrfxgdc edzsbzd', sentiment='good',bar_value=77)

        with COL[1]:
            # st.image("https://www.meridianhomes.net.au/wp-content/uploads/2018/01/Meridian-Homes_Double-Story_Cadence-2-1.jpg", caption=f'{i}Sunrise by the mountains',use_column_width='auto')
            # st.image(row['img0'], caption=f'{i}Sunrise by the mountains',use_column_width='auto')
            st.image(row['img0'],use_column_width='auto')
        
            # if st.button(f'Map{index}'):
            # url = "https://www.google.com/maps/place/13%C2%B054'23.3%22N+101%C2%B010'17.6%22E/@13.9064682,101.1689661,17z"

            # if row['lat']:
            # if not math.isnan(row['lat']):
            #     decimal_coordinates = (row['lat'], row['lon'])
            #     print('decimal_coordinates',decimal_coordinates)
            #     formatted_coordinates = format_coordinates(*decimal_coordinates)


                # url = f"https://www.google.com/maps/place/{formatted_coordinates}/@{row['lat']},{row['lon']},17z"
                # st.markdown(f'[Map]({url})')
            # else:
            #     st.markdown(f'No map')

        with COL[2]:
            

            try:
                st.image(row['img1'],use_column_width='auto')
            except:
                pass
                # webbrowser.open_new_tab(url)

            # st.button('Open link', on_click=open_page("https://www.google.com/maps/place/13%C2%B054'23.3%22N+101%C2%B010'17.6%22E/@13.9064682,101.1689661,17z"))
            # if st.button(f'show map{index}'):
                

                # print("row['lat']",row['lat'],type(row['lat']))
                # # if row['lat'] and row['lon']:
                # if not pd.isna(row['lat']):
                #     random_integer = random.randint(1, 100)
                #     m = folium.Map(location=[row['lat']+random_integer*0.000000001, row['lon']], zoom_start=16)
                #     folium.Marker([row['lat'], row['lon']]).add_to(m)

                #     plugins.Fullscreen(                                                         
                #         position = "topleft",                                   
                #         title = "Open full-screen map",                       
                #         title_cancel = "Close full-screen map",                      
                #         force_separate_button = True,                                         
                #     ).add_to(m) 

                #     satellite_tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                #     folium.TileLayer(tiles=satellite_tiles, attr="Esri World Imagery", name="Satellite").add_to(m)
                #     # folium.TileLayer(tiles='Stamen Terrain',name="Satellite2").add_to(map)
                #     folium.LayerControl(position='topleft').add_to(m)


                #     st_folium(m,use_container_width=True,height=300) # width=400,height=400)
                # else:
                #     print('no location',row['link'])

df = st.session_state["df"]
# st.write(df)

# df['aumper'].unique()


data = []
for k in df['aumper'].unique():
    # data.append(stx.TabBarItemData(id=i, title="✍️ To Do", description="Tasks to take care of"))
    data.append(stx.TabBarItemData(id=k, title=k, description=""))
    
chosen_id = stx.tab_bar(data = data)
placeholder = st.container()
df_filter = df[df['aumper']==chosen_id]

n_page = df_filter.shape[0]//10 + 1
data2 = []
for i in range(1,n_page+1):
    # data.append(stx.TabBarItemData(id=i, title="✍️ To Do", description="Tasks to take care of"))
    data2.append(stx.TabBarItemData(id=i, title=i, description=""))

chosen_id2 = stx.tab_bar(data = data2, default=1)
placeholder2 = placeholder.container()

filtered_df2 = df_filter.iloc[int(chosen_id2)*10:int(chosen_id2)*10+10]
st.write(filtered_df2)
create_list(filtered_df2,filtered_df2.shape[0])





# T = st.tabs([str(i) for i in range(1, n_page+1)])
# for i in range(n_page):
#     with T[i]:
#         filtered_df = df.iloc[i*10:i*10+10]
#         create_list(filtered_df,df.shape[0])

# st.write(df_filter)


# if chosen_id ==1:
#     placeholder.markdown(f"## Welcome to `{chosen_id}`")
# else:
#     placeholder.markdown(f"##xxxx `{chosen_id}`")




# st.code("import extra_streamlit_components as stx")
# chosen_id = stx.tab_bar(data=[
#     stx.TabBarItemData(id="tab1", title="✍️ To Do", description="Tasks to take care of"),
#     stx.TabBarItemData(id="tab2", title="📣 Done", description="Tasks taken care of"),
#     stx.TabBarItemData(id="tab3", title="💔 Overdue", description="Tasks missed out")])

# placeholder = st.container()

# if chosen_id == "tab1":
#     placeholder.markdown(f"## Welcome to `{chosen_id}`")
#     placeholder.image("https://placekitten.com/g/1400/600",caption=f"Meowhy from {chosen_id}")

# elif chosen_id == "tab2":
#     placeholder.markdown(f"## Hello, this is `{chosen_id}`")
#     placeholder.image("https://placekitten.com/g/1200/300",caption=f"Hi from {chosen_id}")

# elif chosen_id == "tab3":
#     placeholder.markdown(f"## And this is ... 🥁 ... `{chosen_id}`")
#     placeholder.image("https://placekitten.com/g/900/400",caption=f"Fancy seeing you here at {chosen_id}")

# else:
#     placeholder = st.empty()