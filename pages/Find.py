import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import requests
import io
from streamlit_folium import st_folium
from datetime import datetime
import numpy as np

st.set_page_config(layout="wide")
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


tab1, tab2 = st.tabs(["📈 Lists", "🗃 Map"])
# data = np.random.randn(10, 1)
# tab1.subheader("A tab with a chart")
# tab1.line_chart(data)
# tab2.subheader("A tab with the data")
# tab2.write(data)


COLORS = {
    'ที่ดินพร้อมสิ่งปลูกสร้าง' : 'red',
    'ที่ดินว่างเปล่า' : 'green',
    'ห้องชุด' : 'blue',
    'หุ้น' : 'gray'
}

if "current_id" not in st.session_state:
    st.session_state["current_id"] = 0
if "df" not in st.session_state:
    st.session_state["df"] = pd.DataFrame()
if "stage" not in st.session_state:
    st.session_state["stage"] = 0

def get_pos(lat,lng):
    return lat,lng

def get_data(province):
    # province = 'nonthaburi'
    url = f'https://raw.githubusercontent.com/phawitb/crawler-led3-window/main/df_{province}.csv'
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    return df


def create_map(df):
    #init map
    # df['lat'].mean()
    # df['lon'].mean()
    initial_location = [df['lat'].mean(),df['lon'].mean()]  # New York City coordinates
    # initial_location = [13.9162258,100.3809889]  # New York City coordinates
    map = folium.Map(location=initial_location, zoom_start=12)

    # L = ['A','B','C']
    L = list(df['type'].unique())
    # L.sort()

    # print('LLLL',L)
    # ['ที่ดินพร้อมสิ่งปลูกสร้าง', 'ที่ดินว่างเปล่า', 'หุ้น', 'ห้องชุด']
    Layers = []
    for l in L:
        la = folium.FeatureGroup(name=l)
        map.add_child(la)

        Layers.append(la)

    for index, row in df.iterrows():
        # print("row['size0']",row['size0'],type(row['size0']))
        # print('imgggggggg',str(row['img0']))

        color = COLORS[row['type']]
        fill_color = COLORS[row['type']]
        if row['size0'] < 30 and row['size1'] == 0 and row['size2'] == 0 and row['type']=='ที่ดินพร้อมสิ่งปลูกสร้าง':
            color = 'orange'
            fill_color = 'orange'




        if str(row['img0']) == 'nan':
            fill_opacity = 0.3
            fill_color = 'black'
            # print('bbbbbbbbbb')
        else:
            fill_opacity = 0.8
            # fill_color = COLORS[row['type']]
        if str(row['lon']) != 'nan':
            # print(row['lat'], row['lon'],row['img0'])
            # max_price,lastSta_date,lastSta_detail
            A = ''
            if row['size2'] != 0:
                A += f"{row['size2']} ไร่ "
            if row['size1'] != 0 or row['size2']>0:
                A += f"{row['size1']} งาน "
            if row['size0'] != 0 or row['size2']>0 or row['size1']>0:
                A += f"{row['size0']} ตร.ว."

            # # <iframe id="myIFrame" width="{}" height="{}" src={}""".format(100,100,'https://google.com') + """ frameborder="0"></iframe>
            # htm = """ 
            #     <!doctype html>
            # <html>
            # <iframe id="myIFrame" width="{}" height="{}" src={}.format(100,100,'https://google.com') frameborder="0"></iframe>
            # <script type="text/javascript">
            # var resizeIFrame = function(event) {
            #     var loc = document.location;
            #     if (event.origin != loc.protocol + '//' + loc.host) return;

            #     var myIFrame = document.getElementById('myIFrame');
            #     if (myIFrame) {
            #         myIFrame.style.height = event.data.h + "px";
            #         myIFrame.style.width  = event.data.w + "px";
            #     }
            # };
            # if (window.addEventListener) {
            #     window.addEventListener("message", resizeIFrame, false);
            # } else if (window.attachEvent) {
            #     window.attachEvent("onmessage", resizeIFrame);
            # }
            # </script>
            # </html>"""

            # htm = f"""<h2>{row['type']}</h2>
            #   <h5>{row['tumbon']},{row['aumper']},{row['province']}</h5>
            #   <h5>{A}</h5>
            #   <h5>นัด{int(row['bid_time'])} : {datetime.strptime(str(int(row['lastSta_date'])), "%Y%m%d").strftime("%d/%m/%Y")} {row['lastSta_detail']}</h5>
            #   <h5>{row['status']}</h5>
            #   <h4><a href="{row['link']}" target="_blank">{'{:,}'.format(int(row['max_price']))}</a></h4>
            #   <img src="{row['img0']}" alt="Trulli" style="max-width:100%;max-height:100%">"""

            H = [f"<h2>{row['type']}</h2>",
                f"<h5>{row['tumbon']},{row['aumper']},{row['province']}</h5>",
                f"<h5>{A}</h5>",
                f"<h5>นัด{int(row['bid_time'])} : {datetime.strptime(str(int(row['lastSta_date'])), '%Y%m%d').strftime('%d/%m/%Y')} {row['lastSta_detail']}</h5>",
                f"<h5>{row['status']}</h5>",
                f"<h4><a href='{row['link']}' target='_blank'>{'{:,}'.format(int(row['max_price']))}</a></h4>",
                f"<img src='{row['img0']}' alt='Trulli' style='max-width:100%;max-height:100%'>"]

            htm = ''
            for h in H:
                try:
                    htm += h
                except:
                    pass
            
          


            popup=folium.Popup(htm, max_width=400)
  


            
            marker = folium.Circle(popup=popup,location=[float(row['lat']), float(row['lon'])], radius=100,weight=1, fill=True, color=color,fill_color=fill_color,fill_opacity=fill_opacity)


#    <script>
#             function convertToCSV(dataArray) {{
#                 const csvContent = dataArray.map(row => row.join(',')).join('\n');
#                 return csvContent;
#             }}

#             function downloadCSV(content, filename) {{
#                 const blob = new Blob([content], {{ type: 'text/csv' }});
#                 const url = URL.createObjectURL(blob);
#                 const a = document.createElement('a');
#                 a.href = url;
#                 a.download = filename;
#                 a.click();
#                 URL.revokeObjectURL(url);
#             }}

#             const data = [
#                 ['Name', 'Age', 'Country'],
#                 ['John', '25', 'USA'],
#                 ['Alice', '30', 'Canada'],
#                 ['Bob', '22', 'UK']
#             ];

#             const saveButton = document.getElementById('saveButton');
#             saveButton.addEventListener('click', () => {{
#                 const csvContent = convertToCSV(data);
#                 downloadCSV(csvContent, 'data.csv');
#             }});
#             </script>


# date_string = 
# datetime.strptime(str(int(row['lastSta_date'])), "%Y%m%d").strftime("%Y-%m-%d")

# {'{:,}'.format(int(row['max_price']))}
    #         color='blue',
    # fill=True,
    # fill_color='blue',
    # fill_opacity=0.4,


            # marker = folium.Marker(location=[float(row['lat']), float(row['lon'])], popup=row['max_price'],icon=folium.Icon(color=COLORS[row['type']]))
            # marker = folium.Circle(popup=row['max_price'],location=[float(row['lat']), float(row['lon'])], radius=5, fill=True, color=COLORS[row['type']])

            i = L.index(row['type'])
            marker.add_to(Layers[i])




    satellite_tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    folium.TileLayer(tiles=satellite_tiles, attr="Esri World Imagery", name="Satellite").add_to(map)
    # folium.TileLayer(tiles='Stamen Terrain',name="Satellite2").add_to(map)
    folium.LayerControl().add_to(map)

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

#slide bar============================
st.sidebar.header("Find")
selected_province = st.sidebar.selectbox('Province',['Select Province','nonthaburi', 'nakhonpathom','samutsakorn','songkhla','chonburi'])
if selected_province != 'Select Province':
    df = get_data(selected_province)
    selected_aumpher = st.sidebar.multiselect('Aumpher',list(df['aumper'].unique()))
    selected_min, selected_max = st.sidebar.select_slider('Price',options=['0','100k','500k','1M','3M','5M','10M','500M'],value=('0', '500M'))

    #find all dates
    all_date = []
    for i in list(df['bid_dates'].unique()):
        # print(i,type(i))
        if str(i) != 'nan':
            all_date = all_date+eval(i)
    all_date = set(all_date)
    all_date = ['All Date'] + [datetime.strptime(x, '%Y%m%d').strftime('%Y/%m/%d') for x in all_date]
    selected_date = st.sidebar.selectbox('Date',all_date)


    # L = list(df['type'].unique())
    types = {}
    for l in list(df['type'].unique()):
        types[l] = st.sidebar.checkbox(l,value=True)

    size_min, size_max = st.sidebar.select_slider('Size(ตร.ว.)',options=['0','20','30','40','50','100','200','400','max'],value=('0', 'max'))
    print('size_min, size_max',size_min, size_max)


    dfs = filter_df(df,selected_province,selected_aumpher,selected_min,selected_max,selected_date,types,size_min, size_max)
    dfs = dfs.reset_index(drop=True)
    st.session_state["df"] = dfs



# tab1.write(st.session_state["df"])
# tab1.dataframe(st.session_state["df"])
df = st.session_state["df"]
df = df[['sell_order','type','img0','img1']]
tab1.write(df)
# tab1.data_editor(
#     df,
#     column_config={
#         "img0": st.column_config.ImageColumn("img0", help="Streamlit app preview screenshots",width='large'),
#         "img1": st.column_config.ImageColumn("img1", help="Streamlit app preview screenshots")

#     },
#     hide_index=True,
#     height = 1000,
#     # use_container_width = True
# )

with tab2:
    map = create_map(st.session_state["df"])
    map.get_root().html.add_child(folium.Element('<style>#map-container { height: 100vh !important; width: 100% !important; }</style>'))
    m = folium_static(map,height=1000, width=1800)

    

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
