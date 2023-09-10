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

# import firebase_admin
# from firebase_admin import credentials, firestore
# import time
# import random
# import webbrowser





# from streamlit_js_eval import streamlit_js_eval

# # screen_width = streamlit_js_eval(js_expressions='screen.width', key = 'SCR')
# st.write(f"Screen width is {streamlit_js_eval(js_expressions='screen.width', key = 'SCR')}")
# st.write(f"Screen height is {streamlit_js_eval(js_expressions='screen.height', key = 'SCR1')}")


# container_width = st.get_container_width
# screen_width = st.screen_width

# st.write(container_width) 
# st.write(screen_width)
# try:
#     cred = credentials.Certificate("led-webapp-752a2-firebase-adminsdk-7je9x-b7d6cf18d0.json")
#     firebase_admin.initialize_app(cred)
# except:
#     pass

# st.sidebar.markdown(
#     """
#     <style>
#     .full-width-button {
#         width: 100%;
#         padding: 10px;
#         box-sizing: border-box;
#     }
#     </style>
#     """
#     , unsafe_allow_html=True
# )

# st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'
# st.session_state.sidebar_state = 'expanded'
st.set_page_config(layout="wide",initial_sidebar_state=st.session_state.sidebar_state)
st.markdown(
"""
<style>
.css-1aumxhk {
    padding: 0;
    border: none;
    box-shadow: none;
}
</style>
""",
unsafe_allow_html=True
)


# tab1,tab2,tab3 = st.tabs(["📈 Lists", "🗃 Map","🌟Favorate"])

COLORS = {
    'ที่ดินพร้อมสิ่งปลูกสร้าง' : 'red',
    'ที่ดินว่างเปล่า' : 'green',
    'ห้องชุด' : 'blue',
    'หุ้น' : 'gray'
}

cookie_manager = stx.CookieManager()
person_id = cookie_manager.get(cookie='person_id')


if "current_id" not in st.session_state:
    st.session_state["current_id"] = None
if "df" not in st.session_state:
    st.session_state["df"] = pd.DataFrame()
if "stage" not in st.session_state:
    st.session_state["stage"] = None
if "selected_province" not in st.session_state:
    st.session_state["selected_province"] = None
if "find" not in st.session_state:
    st.session_state["find"] = {}
if "screen_width" not in st.session_state:
    st.session_state["screen_width"] = 1800
# if 'sidebar_state' not in st.session_state:
#     st.session_state.sidebar_state = 'expanded'

st.session_state["current_id"] = person_id

# cookie_manager = stx.CookieManager()

def get_pos(lat,lng):
    return lat,lng

def get_data(province):
    # province = 'nonthaburi'
    url = f'https://raw.githubusercontent.com/phawitb/crawler-led3-window/main/df_{province}.csv'
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    return df


def create_map(df):
    initial_location = [df['lat'].mean(),df['lon'].mean()]  
    map = folium.Map(location=initial_location, zoom_start=12)

    L = list(df['type'].unique())
    
    Layers = []
    for l in L:
        la = folium.FeatureGroup(name=l)
        map.add_child(la)

        Layers.append(la)

    for index, row in df.iterrows():

        color = COLORS[row['type']]
        fill_color = COLORS[row['type']]
        if row['size0'] < 30 and row['size1'] == 0 and row['size2'] == 0 and row['type']=='ที่ดินพร้อมสิ่งปลูกสร้าง':
            color = 'orange'
            fill_color = 'orange'

        if str(row['img0']) == 'nan':
            fill_opacity = 0.3
            fill_color = 'black'

        else:
            fill_opacity = 0.8
            
        if str(row['lon']) != 'nan':
            A = ''
            if row['size2'] != 0:
                A += f"{row['size2']} ไร่ "
            if row['size1'] != 0 or row['size2']>0:
                A += f"{row['size1']} งาน "
            if row['size0'] != 0 or row['size2']>0 or row['size1']>0:
                A += f"{row['size0']} ตร.ว."

            htm = ""
            try:
                htm += f"<h2>{row['type']}</h2>"
            except:
                pass
            try:
                htm += f"<h5>{row['tumbon']},{row['aumper']},{row['province']}</h5>"
            except:
                pass
            try:
                htm += f"<h5>{A}</h5>"
            except:
                pass
            try:
                htm += f"<h5>นัด{int(row['bid_time'])} : {datetime.strptime(str(int(row['lastSta_date'])), '%Y%m%d').strftime('%d/%m/%Y')} {row['lastSta_detail']}</h5>"
            except:
                pass
            try:
                htm += f"<h5>{row['status']}</h5>"
            except:
                pass
            try:
                htm += f"<h4><a href='{row['link']}' target='_blank'>{'{:,}'.format(int(row['max_price']))}</a></h4>"
            except:
                pass
            try:
                htm += f"<img src='{row['img0']}' alt='Trulli' style='max-width:100%;max-height:100%'>"
            except:
                pass

            row['user_id'] = st.session_state["current_id"]
            row['province_eng'] = st.session_state["selected_province"]

            encoded_text = base64.b64encode(json.dumps(dict(row)).encode('utf-8'))
            #htm += f"<h4><a href=http://localhost:8505/favorateApi/?name={encoded_text} target='_blank'>F</a></h4>"
            htm += f"<h4><a href=https://led-webappgit-n6mlx9qfep6a8quj6qol94.streamlit.app/favorateApi/?name={encoded_text} target='_blank'>F</a></h4>"
            
            popup=folium.Popup(htm, max_width=400)
            marker = folium.Circle(popup=popup,location=[float(row['lat']), float(row['lon'])], radius=100,weight=1, fill=True, color=color,fill_color=fill_color,fill_opacity=fill_opacity)

            i = L.index(row['type'])
            marker.add_to(Layers[i])

    plugins.Fullscreen(                                                         
        position = "topleft",                                   
        title = "Open full-screen map",                       
        title_cancel = "Close full-screen map",                      
        force_separate_button = True,                                         
    ).add_to(map) 

    satellite_tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    folium.TileLayer(tiles=satellite_tiles, attr="Esri World Imagery", name="Satellite").add_to(map)
    # folium.TileLayer(tiles='Stamen Terrain',name="Satellite2").add_to(map)
    folium.LayerControl(position='topleft').add_to(map)

    return map

def filter_equal(df,col,L):
    df2 = df[df[col]==L[0]]
    for a in L[1:]:
        df2 = df2._append(df[df[col]==a])
    return df2

def filter_range(df,col,mi,mx):
    df['max_price'].fillna(-1, inplace = True)
    df2 = df[df[col]>mi]
    df2 = df2[df2[col]<mx]
    return df2

def strprice2int(s):
    if 'k' in s or 'M' in s:
        if s[-1] == 'k':
            x = 1000
        if s[-1] == 'M':
            x = 1000000
        return int(s[:-1])*x
    else:
        return int(s)

def filter_df(df,selected_province,selected_aumpher,selected_min,selected_max,selected_date,types,size_min, size_max):
    print('selectttt',selected_province,selected_aumpher,selected_min, selected_max,selected_date,types,size_min, size_max)

    df['tarangwa'] = df['size0']+df['size1']*100+df['size2']*400

    if size_min != 'max':
        size_min = int(size_min)
    else:
        size_min = 10000
    if size_max != 'max':
        size_max = int(size_max)
    else:
        size_max = 100000
    df = filter_range(df,'tarangwa',size_min,size_max)


    T = []
    for t in types.keys():
        if types[t]:
            T.append(t)
    #filter df
    if not selected_aumpher:
        selected_aumpher = list(df['aumper'].unique())
    selected_date = selected_date.replace('/','')
    dfs = filter_equal(df,'aumper',selected_aumpher)
    dfs = filter_range(dfs,'max_price',strprice2int(selected_min),strprice2int(selected_max))
    dfs = filter_equal(dfs,'type',T)
    if selected_date != 'All Date':
        matchDate = []
        for index, row in dfs.iterrows():
            if selected_date in eval(row['bid_dates']):
                matchDate.append(True)
            else:
                matchDate.append(False)
        dfs['matchDate'] = matchDate
    else:
        dfs['matchDate'] = True
    dfs = dfs[dfs['matchDate'] == True]
    return dfs

def create_list(df):
    for index, row in df.iterrows():
    #     if index ==10:
    #         break
    # for i in range(10):
        COL = st.columns(3)
        # st.divider()
        with COL[0]:
            st.subheader(f":green[{index+1}/{df.shape[0]}[{row['sell_order']}]{row['type']}]")
            st.markdown(f"***{row['tumbon']},{row['aumper']},{row['province']}***")

            area = ''
            a = ['ตร.ว.','งาน','ไร่']
            for i in range(2, -1, -1):
                if isinstance(row[f'size{i}'], int) or isinstance(row[f'size{i}'], float):
                    if row[f'size{i}'] != 0:
                        area += f"{row[f'size{i}']} {a[i]} "
            area = area[:-1]
            st.markdown(f"**{area}**")
            # st.markdown("*Streamlit* is **really** ***cool***.")
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
            st.image(row['img0'], caption=f'{i}Sunrise by the mountains',use_column_width='auto')
        
        with COL[2]:
            # if st.button(f'Map{index}'):
            url = "https://www.google.com/maps/place/13%C2%B054'23.3%22N+101%C2%B010'17.6%22E/@13.9064682,101.1689661,17z"
            st.markdown(f'[Visit OpenAI]({url})')
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

#slide bar============================
if st.session_state["current_id"]:

    st.sidebar.header("Find")
    selected_province = st.sidebar.selectbox('Province',['Select Province','nonthaburi', 'nakhonpathom','samutsakorn','songkhla','chonburi'])
    if selected_province != 'Select Province':
        st.session_state["selected_province"] = selected_province

        # tab1,tab2,tab3 = st.tabs(["📈 Lists", "🗃 Map","🌟Favorate"])
        # tab1,tab2 = st.tabs(["📈 Lists", "🗃 Map"])
        df = get_data(selected_province)
        # print(df.to_dict())
        cookie_manager.set('province', selected_province, expires_at=datetime(year=2025, month=2, day=2))
        selected_aumpher = st.sidebar.multiselect('Aumpher',list(df['aumper'].unique()))
        selected_min, selected_max = st.sidebar.select_slider('Price',options=['0','100k','500k','1M','3M','5M','10M','500M'],value=('0', '500M'))

        #find all dates
        all_date = []
        for i in list(df['bid_dates'].unique()):
            if str(i) != 'nan':
                all_date = all_date+eval(i)
        all_date = set(all_date)
        all_date = ['All Date'] + [datetime.strptime(x, '%Y%m%d').strftime('%Y/%m/%d') for x in all_date]
        selected_date = st.sidebar.selectbox('Date',all_date)

        types = {}
        for l in list(df['type'].unique()):
            types[l] = st.sidebar.checkbox(l,value=True)

        size_min, size_max = st.sidebar.select_slider('Size(ตร.ว.)',options=['0','20','30','40','50','100','200','400','max'],value=('0', 'max'))
        print('size_min, size_max',size_min, size_max)

        #FIND
        st.session_state["find"]['selected_province'] = selected_province
        st.session_state["find"]['selected_aumpher'] = selected_aumpher
        st.session_state["find"]['selected_min'] = selected_min
        st.session_state["find"]['selected_max'] = selected_max
        st.session_state["find"]['all_date'] = all_date
        st.session_state["find"]['selected_date'] = selected_date
        st.session_state["find"]['types'] = types
        st.session_state["find"]['size_min'] = size_min
        st.session_state["find"]['size_max'] = size_max
        

        dfs = filter_df(df,selected_province,selected_aumpher,selected_min,selected_max,selected_date,types,size_min, size_max)
        dfs = dfs.reset_index(drop=True)
        st.session_state["df"] = dfs

        #-------------------------------------------------------
        if st.sidebar.button('Map'): #,use_container_width=True):
            st.session_state.sidebar_state = 'collapsed'
            st.session_state["stage"] = 'map'
            st.experimental_rerun()
        if st.sidebar.button('Lists'): #,use_container_width=True):
            st.session_state.sidebar_state = 'collapsed'
            st.session_state["stage"] = 'lists'
            st.experimental_rerun()



        df = st.session_state["df"]

        if st.session_state["stage"] == 'map':
            # if st.button('Lists'):
            #     st.session_state["stage"] = 'lists'
            map = create_map(st.session_state["df"])
            map.get_root().html.add_child(folium.Element('<style>#map-container { height: 100vh !important; width: 100% !important; }</style>'))
            # m = folium_static(map,height=1000, width=1800)
            m = folium_static(map,height=1000, width=st.session_state["screen_width"])

            
            # st_folium(map,use_container_width=True,height=300)

        elif st.session_state["stage"] == 'lists':
            # if st.button('Map'):
            #     st.session_state["stage"] = 'lists'
            n_page = df.shape[0]//10 + 1
            T = st.tabs([str(i) for i in range(1, n_page+1)])
            for i in range(n_page):
                with T[i]:
                    filtered_df = df.iloc[i*10:i*10+10]
                    create_list(filtered_df)
        else:
            st.write('Please select province in slidebar!')

            



        # with tab1:
        # st.write('tab1')
        # if st.button('Map'):
        #     map = create_map(st.session_state["df"])
        #     map.get_root().html.add_child(folium.Element('<style>#map-container { height: 100vh !important; width: 100% !important; }</style>'))
        #     m = folium_static(map,height=1000, width=1800)

        # # with tab2:
        # if st.button('Lists'):
        #     st.write('tab2')
            
        #     n_page = df.shape[0]//10 + 1
        #     T = st.tabs([str(i) for i in range(1, n_page+1)])
        #     for i in range(n_page):
        #         with T[i]:
        #             filtered_df = df.iloc[i*10:i*10+10]
        #             create_list(filtered_df)


    else:
        st.write('Please select province in slidebar!')

        # if st.session_state.sidebar_state != 'expanded':
        #     st.session_state.sidebar_state = 'expanded'
        #     st.experimental_rerun()

        # st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
        # Force an app rerun after switching the sidebar state.
       




else:
    st.title('Please login')




            # st.write(df)
            # st.set_page_config(layout="wide")
     
            # st.write(df.shape[0])
            # for i in range()
            # with T:

            
            # with t1:
            #     filtered_df = df.iloc[0:10]
            #     create_list(filtered_df)
            # with t2:
            #     filtered_df = df.iloc[10:20]
            #     create_list(filtered_df)

        


        # with tab3:
        #     st.title('Favorate')
        #     st.write(df)

        #     db = firestore.client()
        #     collection_ref = db.collection('favorate')
        #     doc_ref = collection_ref.document(person_id)
        #     #show favorate data
        #     doc_snapshot = doc_ref.get()
        #     if doc_snapshot.exists:
        #         data = doc_snapshot.to_dict()
        #         st.write(data)


        # st_folium(map,use_container_width=True,height=1000) # width=400,height=400)


        

        # print('types',types)
        # # selected_date = st.sidebar.selectbox('Date',('all', '06/06/2023', '09/06/2023','12/06/2023'))
        # if st.sidebar.button('🌎 Map'):
        #     st.session_state["stage"] = 1
        #     dfs = filter_df(df,selected_province,selected_aumpher,selected_min,selected_max,selected_date,types,size_min, size_max)


        #     map = create_map(dfs)
        #     # map.get_root().html.add_child(folium.Element('<style>#map-container { height: 100vh !important; width: 100% !important; }</style>'))
        #     m = folium_static(map,height=1000, width=1800)

        # if st.sidebar.button('🏠 Order-ID'):
        #     st.session_state["stage"] = 2
        #     dfs = filter_df(df,selected_province,selected_aumpher,selected_min,selected_max,selected_date,types,size_min, size_max)
        #     dfs = dfs.reset_index(drop=True)
        #     st.session_state["df"] = dfs
